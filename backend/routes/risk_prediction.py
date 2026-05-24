"""
Risk prediction API routes — thin layer over RiskService.
"""

import logging

from fastapi import APIRouter, HTTPException

from backend.services.risk_service import risk_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def risk_health():
    try:
        return risk_service.health()
    except Exception as error:
        logger.error(f"Risk health check failed: {error}")
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/predict")
async def predict_risk(data: dict):
    try:
        return risk_service.predict_risk(data)
    except Exception as error:
        logger.error(f"Risk prediction failed: {error}")
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/analyze_driver")
async def analyze_driver(data: dict):
    try:
        return risk_service.analyze_driver(data)
    except Exception as error:
        logger.error(f"Driver analysis failed: {error}")
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/analyze_route")
async def analyze_route(data: dict):
    try:
        return risk_service.analyze_route(data)
    except Exception as error:
        logger.error(f"Route analysis failed: {error}")
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/live")
async def live_risk():
    try:
        return risk_service.live_risk()
    except Exception as error:
        logger.error(f"Live risk check failed: {error}")
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/history")
async def risk_history():
    try:
        return risk_service.get_history()
    except Exception as error:
        logger.error(f"Risk history retrieval failed: {error}")
        raise HTTPException(status_code=500, detail=str(error)) from error
