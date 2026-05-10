from flask import Blueprint, request, jsonify

from ai_models.ride_optimization.ride_manager import (
    RideManager
)

from ai_models.ride_optimization.recommendation import (
    RecommendationEngine
)

# =========================================================
# BLUEPRINT
# =========================================================

ride_optimization_bp = Blueprint(

    "ride_optimization",

    __name__
)

# =========================================================
# GLOBAL INSTANCES
# =========================================================

ride_manager = RideManager()

recommendation_engine = RecommendationEngine(
    ride_manager
)

# =========================================================
# STANDARD RESPONSE
# =========================================================

def api_response(

    success,
    message=None,
    data=None,
    status_code=200
):

    response = {

        "success": success
    }

    if message:

        response["message"] = message

    if data is not None:

        response["data"] = data

    return jsonify(response), status_code

# =========================================================
# VALIDATE RIDE INPUT
# =========================================================

def validate_ride_payload(data):

    required_fields = [

        "ride_id",
        "source",
        "destination",
        "start_time",
        "share_allowed",
        "passenger_count"
    ]

    missing_fields = [

        field

        for field in required_fields

        if field not in data
    ]

    if missing_fields:

        return False, {

            "missing_fields":
                missing_fields
        }

    # =============================================
    # LOCATION VALIDATION
    # =============================================

    for field in [

        "source",
        "destination"
    ]:

        location = data.get(field)

        if (

            not isinstance(location, list)

            and not isinstance(location, tuple)

        ):

            return False, {

                "message":
                    f"{field} must be list/tuple"
            }

        if len(location) != 2:

            return False, {

                "message":
                    f"{field} must contain lat/lon"
            }

    # =============================================
    # PASSENGER VALIDATION
    # =============================================

    if data["passenger_count"] <= 0:

        return False, {

            "message":
                "Invalid passenger count"
        }

    return True, None

# =========================================================
# HEALTH CHECK
# =========================================================

@ride_optimization_bp.route(

    "/health",

    methods=["GET"]
)

def health_check():

    return api_response(

        True,

        "Ride optimization service active"
    )

# =========================================================
# CREATE RIDE
# =========================================================

@ride_optimization_bp.route(

    "/create_ride",

    methods=["POST"]
)

def create_ride():

    try:

        data = request.get_json()

        if not data:

            return api_response(

                False,

                "No JSON data received",

                status_code=400
            )

        # =========================================
        # VALIDATION
        # =========================================

        is_valid, error = (
            validate_ride_payload(data)
        )

        if not is_valid:

            return api_response(

                False,

                data=error,

                status_code=400
            )

        # =========================================
        # DUPLICATE CHECK
        # =========================================

        active_rides = (
            ride_manager.get_active_rides()
        )

        if data["ride_id"] in active_rides:

            return api_response(

                False,

                "Ride ID already exists",

                status_code=409
            )

        # =========================================
        # CREATE RIDE
        # =========================================

        ride = ride_manager.create_ride(
            data
        )

        return api_response(

            True,

            "Ride created successfully",

            ride,

            201
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# START RIDE
# =========================================================

@ride_optimization_bp.route(

    "/start_ride/<ride_id>",

    methods=["POST"]
)

def start_ride(ride_id):

    try:

        result = ride_manager.start_ride(
            ride_id
        )

        return api_response(

            result["success"],

            data=result
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# COMPLETE RIDE
# =========================================================

@ride_optimization_bp.route(

    "/complete_ride/<ride_id>",

    methods=["POST"]
)

def complete_ride(ride_id):

    try:

        result = ride_manager.complete_ride(
            ride_id
        )

        return api_response(

            result["success"],

            data=result
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# CANCEL RIDE
# =========================================================

@ride_optimization_bp.route(

    "/cancel_ride/<ride_id>",

    methods=["POST"]
)

def cancel_ride(ride_id):

    try:

        result = ride_manager.cancel_ride(
            ride_id
        )

        return api_response(

            result["success"],

            data=result
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# UPDATE LOCATION
# =========================================================

@ride_optimization_bp.route(

    "/update_location/<ride_id>",

    methods=["POST"]
)

def update_location(ride_id):

    try:

        data = request.get_json()

        if not data:

            return api_response(

                False,

                "No JSON data received",

                status_code=400
            )

        location = data.get("location")

        if not location:

            return api_response(

                False,

                "location field required",

                status_code=400
            )

        if len(location) != 2:

            return api_response(

                False,

                "location must contain lat/lon",

                status_code=400
            )

        result = (

            ride_manager.update_ride_location(

                ride_id,

                tuple(location)
            )
        )

        return api_response(

            result["success"],

            data=result
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# JOIN GROUP
# =========================================================

@ride_optimization_bp.route(

    "/join_group/<group_id>",

    methods=["POST"]
)

def join_group(group_id):

    try:

        data = request.get_json()

        if not data:

            return api_response(

                False,

                "No JSON data received",

                status_code=400
            )

        result = ride_manager.join_group(

            group_id,
            data
        )

        return api_response(

            result["success"],

            data=result
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# REOPTIMIZE SYSTEM
# =========================================================

@ride_optimization_bp.route(

    "/reoptimize",

    methods=["POST"]
)

def reoptimize():

    try:

        results = (

            ride_manager
            .trigger_reoptimization()
        )

        return api_response(

            True,

            "System reoptimized",

            results
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# CLEANUP STALE RIDES
# =========================================================

@ride_optimization_bp.route(

    "/cleanup",

    methods=["POST"]
)

def cleanup():

    try:

        removed = (

            ride_manager
            .cleanup_stale_rides()
        )

        return api_response(

            True,

            "Cleanup completed",

            {

                "removed_rides":
                    removed
            }
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# ACTIVE RIDES
# =========================================================

@ride_optimization_bp.route(

    "/active_rides",

    methods=["GET"]
)

def get_active_rides():

    try:

        rides = (
            ride_manager.get_active_rides()
        )

        return api_response(

            True,

            data=rides
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# ACTIVE GROUPS
# =========================================================

@ride_optimization_bp.route(

    "/active_groups",

    methods=["GET"]
)

def get_active_groups():

    try:

        groups = (
            ride_manager.get_active_groups()
        )

        return api_response(

            True,

            data=groups
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# RECOMMENDATIONS
# =========================================================

@ride_optimization_bp.route(

    "/recommendations",

    methods=["GET"]
)

def get_recommendations():

    try:

        recommendations = (

            recommendation_engine
            .generate_all_recommendations()
        )

        return api_response(

            True,

            data=recommendations
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )

# =========================================================
# RIDE HISTORY
# =========================================================

@ride_optimization_bp.route(

    "/ride_history",

    methods=["GET"]
)

def get_ride_history():

    try:

        history = (
            ride_manager.get_ride_history()
        )

        return api_response(

            True,

            data=history
        )

    except Exception as error:

        return api_response(

            False,

            str(error),

            status_code=500
        )