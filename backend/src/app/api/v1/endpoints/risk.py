from fastapi import APIRouter
from src.app.services.forecast import forecast_emission

router = APIRouter()


@router.get("/risk/{country}")
def get_risk_score(country: str):
    return forecast_emission(country)
