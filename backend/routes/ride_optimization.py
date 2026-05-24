"""
Ride optimization API routes — thin layer over RideService.
"""

from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.ride_service import ride_service

router = APIRouter()


class RideRequest(BaseModel):
    ride_id: str
    source: List[float]
    destination: List[float]
    start_time: str
    share_allowed: bool
    passenger_count: int


@router.get("/health")
def health_check():
    return ride_service.health()


@router.post("/create")
def create_ride(data: RideRequest):
    try:
        return ride_service.create_ride(data.model_dump())
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/start/{ride_id}")
def start_ride(ride_id: str):
    try:
        return ride_service.start_ride(ride_id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/complete/{ride_id}")
def complete_ride(ride_id: str):
    try:
        return ride_service.complete_ride(ride_id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/cancel/{ride_id}")
def cancel_ride(ride_id: str):
    try:
        return ride_service.cancel_ride(ride_id)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/active")
def get_active_rides():
    try:
        return ride_service.get_active_rides()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/groups")
def get_active_groups():
    try:
        return ride_service.get_active_groups()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/recommendations")
def get_recommendations():
    try:
        return ride_service.get_recommendations()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/history")
def get_ride_history():
    try:
        return ride_service.get_ride_history()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
