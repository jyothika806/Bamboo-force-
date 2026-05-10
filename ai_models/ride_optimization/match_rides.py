from collections import defaultdict
from uuid import uuid4

from ai_models.ride_optimization.route_similarity import (
    calculate_similarity
)


# =========================================================
# CONFIGURATION
# =========================================================

SIMILARITY_THRESHOLD = 0.70

MAX_GROUP_SIZE = 4

VEHICLE_CAPACITY = {

    "BIKE": 1,
    "AUTO": 3,
    "CAB": 4,
    "VAN": 7
}

# =========================================================
# ACTIVE RIDE STORAGE
# =========================================================

ACTIVE_RIDES = {}

ACTIVE_GROUPS = {}

# =========================================================
# ADD RIDE
# =========================================================

def add_ride(ride):

    ACTIVE_RIDES[
        ride["ride_id"]
    ] = ride

# =========================================================
# REMOVE RIDE
# =========================================================

def remove_ride(ride_id):

    if ride_id in ACTIVE_RIDES:

        del ACTIVE_RIDES[ride_id]

# =========================================================
# GET VEHICLE TYPE
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
# CHECK COMPATIBILITY
# =========================================================

def is_compatible(ride_a, ride_b):

    # ============================================
    # SHARE PREFERENCE
    # ============================================

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

    # ============================================
    # PASSENGER LIMIT
    # ============================================

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

    if total_passengers > MAX_GROUP_SIZE:
        return False

    # ============================================
    # ROUTE SIMILARITY
    # ============================================

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

    group_id = str(
        uuid4()
    )[:8]

    optimization_score = round(

        min(
            1.0,
            total_passengers / 4
        ),

        2
    )

    group = {

        "group_id": group_id,

        "rides": [

            ride["ride_id"]

            for ride in rides
        ],

        "passenger_count":
            total_passengers,

        "recommended_vehicle":
            vehicle,

        "optimization_score":
            optimization_score
    }

    ACTIVE_GROUPS[
        group_id
    ] = group

    return group

# =========================================================
# DYNAMIC MATCHING ENGINE
# =========================================================

def match_rides():

    matched_groups = []

    visited = set()

    ride_ids = list(
        ACTIVE_RIDES.keys()
    )

    total_rides = len(
        ride_ids
    )

    # ============================================
    # GREEDY DYNAMIC MATCHING
    # ============================================

    for i in range(total_rides):

        ride_id_a = ride_ids[i]

        if ride_id_a in visited:
            continue

        ride_a = ACTIVE_RIDES[
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

        # ========================================
        # FIND BEST MATCHES
        # ========================================

        for j in range(i + 1, total_rides):

            ride_id_b = ride_ids[j]

            if ride_id_b in visited:
                continue

            ride_b = ACTIVE_RIDES[
                ride_id_b
            ]

            additional_passengers = ride_b.get(
                "passenger_count",
                1
            )

            # ====================================
            # CAPACITY CHECK
            # ====================================

            if (

                current_passengers
                + additional_passengers

            ) > MAX_GROUP_SIZE:

                continue

            # ====================================
            # COMPATIBILITY
            # ====================================

            if is_compatible(

                ride_a,
                ride_b
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

        # ========================================
        # CREATE OPTIMIZED GROUP
        # ========================================

        matched_groups.append(

            create_group(
                current_group
            )
        )

    return matched_groups

# =========================================================
# DYNAMIC REAL-TIME UPDATE
# =========================================================

def update_ride_pool(new_ride):

    # ============================================
    # ADD NEW RIDE
    # ============================================

    add_ride(new_ride)

    # ============================================
    # RE-OPTIMIZE
    # ============================================

    return match_rides()

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

    # ============================================
    # ADD RIDES
    # ============================================

    for ride in rides:

        add_ride(
            ride
        )

    # ============================================
    # MATCH RIDES
    # ============================================

    groups = match_rides()

    print("\n[RESULT] Optimized Ride Groups:\n")

    for group in groups:

        print(group)