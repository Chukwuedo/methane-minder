import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, box
import uuid
import ast
from pathlib import Path
from src.data import PLUMES_RAW_CSV, PLUMES_ENRICHED_PARQUET, PLUMES_GEOJSON


# --- Step 1: Load CSV File ---
if not PLUMES_RAW_CSV.exists():
    raise FileNotFoundError(f"CSV file not found: {PLUMES_RAW_CSV}")
df = pd.read_csv(PLUMES_RAW_CSV)


# --- Step 2: Clean and Cast Columns ---
float_columns = [
    "plume_latitude",
    "plume_longitude",
    "emission_auto",
    "emission_uncertainty_auto",
    "wind_speed_avg_auto",
    "wind_speed_std_auto",
    "wind_direction_avg_auto",
    "wind_direction_std_auto",
    "gsd",
    "off_nadir",
]

for col in float_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

date_columns = ["datetime", "published_at", "modified"]
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

df["plume_id"] = (
    df["plume_id"]
    .fillna("")
    .apply(lambda x: str(uuid.uuid4()) if x.strip() == "" else x)
)

# --- Step 3: Standardize Text Fields ---
text_columns = [
    "gas",
    "ipcc_sector",
    "emission_cmf_type",
    "instrument",
    "mission_phase",
    "processing_software",
    "sensitivity_mode",
    "wind_source_auto",
    "platform",
    "provider",
]
for col in text_columns:
    df[col] = df[col].astype(str).fillna("Unknown").str.strip().str.title()

# --- Step 4: Point and Polygon Geometries ---
df["point_geom"] = gpd.points_from_xy(df["plume_longitude"], df["plume_latitude"])


# --- Step 4: Parse Bounding Box into Polygon Geometry ---
def parse_bounds(bounds):
    try:
        # Some bounds may come in as a string, so we use ast.literal_eval safely
        if isinstance(bounds, str):
            bounds = ast.literal_eval(bounds)
        min_lon, min_lat, max_lon, max_lat = bounds
        return box(min_lon, min_lat, max_lon, max_lat)
    except Exception:
        return None


df["polygon_geom"] = df["plume_bounds"].apply(parse_bounds)

# --- Step 5: Choose Primary Geometry (Polygon with Point Fallback) ---
df["geometry"] = df["polygon_geom"].fillna(df["point_geom"])

# --- Step 6: Include Plume Assets as Dictionary ---
asset_cols = ["plume_tif", "plume_png", "con_tif", "rgb_tif", "rgb_png"]


def bundle_assets(row):
    return {col: row[col] for col in asset_cols if pd.notnull(row[col])}


df["plume_assets"] = df.apply(bundle_assets, axis=1)

# --- Step 7: Create GeoDataFrame and Export ---
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# Save to GeoParquet (exclude temporary geometry columns)
geoparquet_cols = [
    col for col in df.columns if col not in ["point_geom", "polygon_geom"]
]
geoparquet_output_path = PLUMES_ENRICHED_PARQUET

gdf[geoparquet_cols].to_parquet(geoparquet_output_path, index=False)
print(f"GeoParquet export complete: {geoparquet_output_path}")

# Save to GeoJSON (with simplified fields to avoid nested JSON issues)
geojson_output_path = PLUMES_GEOJSON

geojson_cols = [col for col in df.columns if col not in ["point_geom", "polygon_geom"]]
gdf[geojson_cols].to_file(geojson_output_path, driver="GeoJSON")
print(f"GeoJSON export complete: {geojson_output_path}")
