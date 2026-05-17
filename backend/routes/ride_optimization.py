from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ai_models.ride_optimization.optimization_engine import (
    optimization_engine
)


from ai_models.ride_optimization.recommendation import (
    generate_recommendations
)
from ai_models.ride_optimization.ride_manager import (
    ride_manager_instance
)

ride_manager = ride_manager_instance
# =========================================================
# ROUTER
# =========================================================

router = APIRouter()

# =========================================================
# GLOBAL INSTANCE
# =========================================================



# =========================================================
# PYDANTIC MODEL
# =========================================================

class RideRequest(BaseModel):

    ride_id: str

    source: List[float]

    destination: List[float]

    start_time: str

    share_allowed: bool

    passenger_count: int

# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")

def health_check():

    return {

        "success": True,

        "backend": "ACTIVE",

        "optimization_engine": "RUNNING",

        "server": "ONLINE"
    }

# =========================================================
# CREATE RIDE
# =========================================================
@router.post("/create")

def create_ride(data: RideRequest):

    try:

        payload = data.model_dump()

        result = (
            optimization_engine
            .add_new_ride(payload)
            
        )

        optimization_engine.run_dynamic_optimization()

        return {

            "success": True,

            "message":
                "Ride created successfully",

            "data":
                result
        }

    except Exception as error:

        print(error)

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )
# =========================================================
# START RIDE
# =========================================================

@router.post("/start/{ride_id}")

def start_ride(ride_id: str):

    try:

        result = optimization_engine.start_ride(
            ride_id
        )

        return result

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )

# =========================================================
# COMPLETE RIDE
# =========================================================

@router.post("/complete/{ride_id}")

def complete_ride(ride_id: str):

    try:

        result = (
            optimization_engine.complete_ride(
                ride_id
            )
        )

        return result

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )

# =========================================================
# CANCEL RIDE
# =========================================================

@router.post("/cancel/{ride_id}")

def cancel_ride(ride_id: str):

    try:

        result = (
            optimization_engine.cancel_ride(
                ride_id
            )
        )

        return result

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )

# =========================================================
# ACTIVE RIDES
# =========================================================

@router.get("/active")

def get_active_rides():

    try:

        rides = (
            optimization_engine
            .ride_manager
            .get_active_rides()
        )

        return {

            "success": True,

            "data": rides
        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )

# =========================================================
# ACTIVE GROUPS
# =========================================================

@router.get("/groups")

def get_active_groups():

    try:

        groups = (
            optimization_engine
            .get_active_groups()
        )

        return {

            "success": True,

            "data": groups
        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )

# =========================================================
# RECOMMENDATIONS
# =========================================================

@router.get("/recommendations")

def get_recommendations():

    try:

    

        recommendations = (
            generate_recommendations(
                groups
            )
        )

        return {

            "success": True,

            "data": recommendations
        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )

# =========================================================
# RIDE HISTORY
# =========================================================

@router.get("/history")

def get_ride_history():

    try:

        history = (
            optimization_engine.get_ride_history()
        )

        return {

            "success": True,

            "data": history
        }

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=str(error)
        )