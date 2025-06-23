# This file makes the app directory a Python package
from pathlib import Path

# Define the data directory path
DATA_DIR = Path(__file__).parent

# Define specific file paths
PLUMES_RAW_CSV = DATA_DIR / "plumes_raw_data.csv"
PLUMES_ENRICHED_PARQUET = DATA_DIR / "plumes_enriched.parquet"
PLUMES_GEOJSON = DATA_DIR / "plumes.geojson"
PLUMES_DATA_DICTIONARY = DATA_DIR / "plumes_data_dictionary.csv"
HISTORICAL_EMISSION_DATA = DATA_DIR / "methane-emissions.csv"

# Export commonly used paths
__all__ = [
    "DATA_DIR",
    "PLUMES_RAW_CSV",
    "PLUMES_ENRICHED_PARQUET",
    "PLUMES_GEOJSON",
    "PLUMES_DATA_DICTIONARY",
    "HISTORICAL_EMISSION_DATA",
]
