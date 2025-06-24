import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings
from typing import Dict, Any

from src.data import HISTORICAL_EMISSION_DATA


def forecast_emission(country: str) -> Dict[str, Any]:
    """
    Forecast methane emissions for a given country using Exponential Smoothing.

    Args:
        country: Name of the country to forecast emissions for

    Returns:
        Dictionary containing forecast, baseline, and risk assessment
    """
    try:
        # Read and filter data
        df = pd.read_csv(HISTORICAL_EMISSION_DATA)
        country_df = df[df["Entity"] == country].copy()

        if country_df.empty:
            return {
                "error": f"No data available for country: {country}",
                "forecast": None,
                "baseline": None,
                "risk": "unknown",
            }

        # Prepare time series data
        country_df = country_df[["Year", "annual_emissions_ch4_total_co2eq"]]
        country_df = country_df.rename(
            columns={"Year": "year", "annual_emissions_ch4_total_co2eq": "emissions"}
        )

        # Sort by year and remove any duplicates
        country_df = country_df.sort_values("year").drop_duplicates("year")

        # Create datetime index for proper time series handling
        country_df["date"] = pd.to_datetime(country_df["year"], format="%Y")
        country_df.set_index("date", inplace=True)

        # Ensure we have enough data points for forecasting
        if len(country_df) < 3:
            return {
                "error": (
                    f"Insufficient data for forecasting "
                    f"(need at least 3 years, got {len(country_df)})"
                ),
                "forecast": None,
                "baseline": (
                    country_df["emissions"].mean() if not country_df.empty else None
                ),
                "risk": "unknown",
            }

        # Suppress warnings for cleaner output
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # Use simpler exponential smoothing model
            model = ExponentialSmoothing(
                country_df["emissions"],
                trend="add",
                seasonal=None,
                initialization_method="estimated",
            )
            fit = model.fit(optimized=True)
            forecast = fit.forecast(1).iloc[0]

        baseline = country_df["emissions"].mean()

        # Calculate risk assessment
        risk = (
            "high"
            if forecast > baseline * 1.30
            else "medium"
            if forecast > baseline
            else "low"
        )

        return {
            "country": country,
            "forecast": round(forecast, 2),
            "baseline": round(baseline, 2),
            "risk": risk,
            "data_points": len(country_df),
            "latest_year": int(country_df["year"].max()),
            "error": None,
        }

    except Exception as e:
        return {
            "error": f"Error forecasting emissions for {country}: {str(e)}",
            "forecast": None,
            "baseline": None,
            "risk": "unknown",
        }
