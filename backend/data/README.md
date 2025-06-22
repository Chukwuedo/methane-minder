# Carbon Mapper Methane Plume Dataset

This dataset contains enriched methane plume observations extracted from the Carbon Mapper public dashboard. The data has been processed into a geospatially-aware format with both point and polygon geometries, cleaned metadata, and references to associated image assets (TIFF/PNG). The primary focus region is the Permian Basin, Texas, USA.

---

## 📂 Contents

- `plumes_enriched.parquet`: GeoParquet file with full geometries and metadata.
- `plumes.geojson` (optional): GeoJSON export for use with lightweight web mapping tools.
- `plumes_data_dictionary.csv`: Human-readable glossary for all dataset fields.
- `readme_template.md`: This file.

---

## 🗺️ Spatial Reference

- Coordinate Reference System: **EPSG:4326 (WGS84)**
- Geometry Types:
  - Primary: **Polygon** (bounding box of the plume area)
  - Fallback: **Point** (latitude/longitude center)

---

## 🧱 Schema Overview

| Field                | Description                                 |
|----------------------|---------------------------------------------|
| plume_id             | Unique identifier for each plume            |
| datetime             | Observation timestamp (UTC)                 |
| gas                  | Type of gas detected (e.g., CH₄)            |
| ipcc_sector          | Emission source category (e.g., Energy)     |
| emission_auto        | Emission estimate in kg/hr                  |
| wind_speed_avg_auto  | Average wind speed (m/s)                    |
| instrument           | Sensor used (e.g., AVIRIS-NG)               |
| platform             | Data acquisition platform (e.g., aircraft)  |
| plume_bounds         | Bounding box extent (lat/lon min/max)       |
| geometry             | Final geometry used (polygon or point)      |
| plume_assets         | Dictionary of linked asset URLs             |

Full definitions available in `plumes_data_dictionary.csv`.

---

## 🪄 Processing Steps

1. CSV ingested from Carbon Mapper dashboard
2. Bounding box string converted to `shapely` `Polygon`
3. Point geometry fallback added
4. Geometry assigned using `geopandas`
5. Plume image and GeoTIFF references bundled as JSON metadata
6. Exported to `.parquet` using EPSG:4326

---

## 📝 License & Usage

This dataset was derived from Carbon Mapper’s open data portal and is intended for **educational, research, and non-commercial** use. Always refer to the [official data license](https://carbonmapper.org/data) for attribution guidelines.