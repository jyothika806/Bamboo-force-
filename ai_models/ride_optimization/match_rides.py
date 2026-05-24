# =========================================================
# BAMBOO FORCE AI
# DYNAMIC RIDE MATCHING ENGINE
# =========================================================

from uuid import uuid4

from ai_models.ride_optimization.route_similarity import (
    calculate_similarity
)
from ai_models.ride_optimization.state_manager import (
    state
)
from ai_models.ride_optimization.maps_service import (
    get_coordinates
)
# =========================================================
# CONFIGURATION
# =========================================================

SIMILARITY_THRESHOLD = 0.70

MAX_GROUP_PASSENGERS = 7

VEHICLE_CAPACITY = {

    "BIKE": 1,
    "AUTO": 3,
    "CAB": 4,
    "VAN": 7
}


# =========================================================
# ADD RIDE
# =========================================================

def add_ride(ride):

    ride_id = ride.get(
        "ride_id"
    )

    if not ride_id:

        return {

            "status": "FAILED",

            "message":
                "Ride ID missing"
        }

    with state.lock:

        state.active_rides[
            ride_id
        ] = ride

    return {

        "status":
            "RIDE_ADDED",

        "ride_id":
            ride_id
    }
    

# =========================================================
# REMOVE RIDE
# =========================================================

def remove_ride(ride_id):

    with state.lock:

        if ride_id in state.active_rides:

            del state.active_rides[
                ride_id
            ]

            return {

                "status":
                    "RIDE_REMOVED",

                "ride_id":
                    ride_id
            }

    return {

        "status":
            "NOT_FOUND",

        "ride_id":
            ride_id
    }
# =========================================================
# GET ACTIVE RIDES
# =========================================================

def get_active_rides():

    return state.active_rides

# =========================================================
# GET ACTIVE GROUPS
# =========================================================

def get_active_groups():

    return state.active_groups

# =========================================================
# CLEAR ALL RIDES
# =========================================================

def clear_rides():

    state.clear_rides()

    state.clear_groups()
    return {

        "status":
            "ALL_RIDES_CLEARED"
    }

# =========================================================
# RECOMMEND VEHICLE
# =========================================================

def recommend_vehicle(passenger_count):

    if passenger_count <= 1:

        return "BIKE"

    elif passenger_count <= 3:

        return "AUTO"

    elif passenger_count <= 4:

        return "CAB"

    return "VAN"

# =========================================================
# COMPATIBILITY CHECK
# =========================================================

def is_compatible(
    ride_a,
    ride_b
):

    # =====================================================
    # SHARE PREFERENCE
    # =====================================================

    if not ride_a.get(
        "share_allowed",
        True
    ):

        return False

    if not ride_b.get(
        "share_allowed",
        True
    ):

        return False

    # =====================================================
    # PASSENGER LIMIT
    # =====================================================

    total_passengers = (

        ride_a.get(
            "passenger_count",
            1
        )

        + ride_b.get(
            "passenger_count",
            1
        )
    )

    if total_passengers > MAX_GROUP_PASSENGERS:

        return False

    # =====================================================
    # ROUTE SIMILARITY
    # =====================================================

    similarity_score = calculate_similarity(

        ride_a,
        ride_b
    )

    return similarity_score >= SIMILARITY_THRESHOLD

# =========================================================
# CREATE GROUP
# =========================================================

def create_group(rides):

    total_passengers = sum(

        ride.get(
            "passenger_count",
            1
        )

        for ride in rides
    )

    vehicle = recommend_vehicle(
        total_passengers
    )

    vehicle_capacity = VEHICLE_CAPACITY[
        vehicle
    ]

    optimization_score = round(

        total_passengers
        / vehicle_capacity,

        2
    )

    group_id = str(
        uuid4()
    )[:8]

    group = {

        "group_id":
            group_id,

        "rides": [

            ride.get(
                "ride_id"
            )

            for ride in rides
        ],

        "passenger_count":
            total_passengers,

        "recommended_vehicle":
            vehicle,

        "optimization_score":
            optimization_score,

        "match_confidence":
            optimization_score,

        "estimated_vehicle_reduction":
            max(
                0,
                total_passengers - 1
            ),

        "group_status":
            "ACTIVE"
    }

    
    with state.lock:

        state.active_groups[
            group_id
        ] = group

    return group

# =========================================================
# MATCH RIDES
# =========================================================

def match_rides():

    state.clear_groups()

    matched_groups = []

    visited = set()

    ride_ids = list(
        state.active_rides.keys()
    )

    total_rides = len(
        ride_ids
    )

    # =====================================================
    # GREEDY MATCHING
    # =====================================================

    for i in range(total_rides):

        ride_id_a = ride_ids[i]

        if ride_id_a in visited:

            continue

        ride_a = state.active_rides[
            ride_id_a
        ]

        current_group = [ride_a]

        current_passengers = ride_a.get(
            "passenger_count",
            1
        )

        visited.add(
            ride_id_a
        )

        # =================================================
        # FIND COMPATIBLE RIDES
        # =================================================

        for j in range(i + 1, total_rides):

            ride_id_b = ride_ids[j]

            if ride_id_b in visited:

                continue

            ride_b = state.active_rides[
                ride_id_b
            ]

            additional_passengers = ride_b.get(
                "passenger_count",
                1
            )

            # =============================================
            # CAPACITY CHECK
            # =============================================

            if (

                current_passengers
                + additional_passengers

            ) > MAX_GROUP_PASSENGERS:

                continue

            # =============================================
            # COMPATIBILITY CHECK
            # =============================================

            if all(

                is_compatible(
                    existing_ride,
                    ride_b
                )

                for existing_ride
                in current_group
            ):

                current_group.append(
                    ride_b
                )

                current_passengers += (
                    additional_passengers
                )

                visited.add(
                    ride_id_b
                )

        # =================================================
        # CREATE GROUP
        # =================================================

        matched_groups.append(

            create_group(
                current_group
            )
        )

    return matched_groups

# =========================================================
# REAL-TIME UPDATE
# =========================================================

def update_ride_pool(new_ride):

    add_ride(new_ride)

    return match_rides()
# =========================================================
# SYSTEM METRICS
# =========================================================

def get_matching_metrics():

    total_rides = len(
        state.active_rides
    )

    total_groups = len(
        state.active_groups
    )

    total_saved_vehicles = sum(

        group.get(
            "estimated_vehicle_reduction",
            0
        )

        for group in state.active_groups.values()
    )

    return {

        "total_active_rides":
            total_rides,

        "total_active_groups":
            total_groups,

        "estimated_vehicle_reduction":
            total_saved_vehicles,

        "system_status":
            "RUNNING"
    }

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    rides = [

        {
            "ride_id": "R001",

            "source": (
                17.3850,
                78.4867
            ),

            "destination": (
                17.4435,
                78.3772
            ),

            "start_time": 10,

            "share_allowed": True,

            "passenger_count": 1
        },

        {
            "ride_id": "R002",

            "source": (
                17.3900,
                78.4900
            ),

            "destination": (
                17.4480,
                78.3800
            ),

            "start_time": 12,

            "share_allowed": True,

            "passenger_count": 2
        },

        {
            "ride_id": "R003",

            "source": (
                17.5000,
                78.6000
            ),

            "destination": (
                17.7000,
                78.9000
            ),

            "start_time": 50,

            "share_allowed": True,

            "passenger_count": 1
        }
    ]

    # =====================================================
    # LOAD RIDES
    # =====================================================

    for ride in rides:

        add_ride(
            ride
        )

    # =====================================================
    # RUN MATCHING
    # =====================================================

    groups = match_rides()

    print("\n[OPTIMIZED RIDE GROUPS]\n")

    for group in groups:

        print(group)

    print("\n[SYSTEM METRICS]\n")

    print(
        get_matching_metrics()
    )