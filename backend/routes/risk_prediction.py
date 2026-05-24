"""
Risk prediction API routes — thin layer over RiskService.
"""

from fastapi import APIRouter

from backend.services.risk_service import risk_service

router = APIRouter()


@router.get("/health")
async def risk_health():
    return risk_service.health()


@router.post("/predict")
async def predict_risk(data: dict):
    return risk_service.predict_risk(data)


@router.post("/analyze_driver")
async def analyze_driver(data: dict):
    return risk_service.analyze_driver(data)


@router.post("/analyze_route")
async def analyze_route(data: dict):
    return risk_service.analyze_route(data)


@router.get("/live")
async def live_risk():
    return risk_service.live_risk()


@router.get("/history")
async def risk_history():
    return risk_service.get_history()
