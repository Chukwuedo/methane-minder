from fastapi import APIRouter, HTTPException
import geopandas as gpd
from pathlib import Path
from typing import List, Dict, Any
import logging

router = APIRouter()
DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"

PLUMES_GEOJSON_PATH = DATA_DIR / "plumes.geojson"


@router.get("/plumes/latest")
def get_plumes() -> List[Dict[str, Any]]:
    """
    Get the latest 10 methane plumes with their location and emission data.

    Returns:
        List of plume objects with lat, lon, emission data, and metadata
    """
    try:
        if not PLUMES_GEOJSON_PATH.exists():
            raise HTTPException(status_code=404, detail="Plumes data file not found")

        gdf = gpd.read_file(PLUMES_GEOJSON_PATH)

        if gdf.empty:
            return []

        # Sort by datetime to get the most recent plumes first
        if "datetime" in gdf.columns:
            gdf = gdf.sort_values("datetime", ascending=False)

        output = []
        for _, row in gdf.head(100).iterrows():
            # Handle missing emission values properly
            emission_value = row.get("emission_auto")
            if emission_value is None or emission_value == "":
                emission_value = None

            plume_data = {
                "plume_id": row.get("plume_id", "unknown"),
                "lat": (
                    float(row.plume_latitude)
                    if row.plume_latitude is not None
                    else None
                ),
                "lon": (
                    float(row.plume_longitude)
                    if row.plume_longitude is not None
                    else None
                ),
                "emission_auto": emission_value,  # kg/hr
                "emission_uncertainty": row.get("emission_uncertainty_auto"),
                "datetime": row.get("datetime"),
                "gas": row.get("gas", "CH4"),
                "sector": row.get("ipcc_sector", "Unknown"),
                "platform": row.get("platform", "Unknown"),
                "provider": row.get("provider", "Unknown"),
            }

            # Only include plumes with valid coordinates
            if plume_data["lat"] is not None and plume_data["lon"] is not None:
                output.append(plume_data)

        return output

    except Exception as e:
        logging.error(f"Error reading plumes data: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing plumes data")
