from ai_models.ride_optimization.match_rides import (
    match_rides,
    add_ride
)

# =========================================================
# VEHICLE CONFIGURATION
# =========================================================

VEHICLE_CAPACITY = {

    "BIKE": 1,
    "AUTO": 3,
    "CAB": 4,
    "VAN": 7
}

VEHICLE_TRAFFIC_IMPACT = {

    "BIKE": 0.90,
    "AUTO": 0.60,
    "CAB": 0.50,
    "VAN": 0.30
}

VEHICLE_FUEL_FACTOR = {

    "BIKE": 1.0,
    "AUTO": 1.8,
    "CAB": 2.5,
    "VAN": 3.2
}

# =========================================================
# OCCUPANCY EFFICIENCY
# =========================================================

def calculate_occupancy_efficiency(group):

    passengers = group[
        "passenger_count"
    ]

    vehicle = group[
        "recommended_vehicle"
    ]

    capacity = VEHICLE_CAPACITY[
        vehicle
    ]

    occupancy_ratio = (
        passengers / capacity
    )

    # ============================================
    # UNDERUTILIZATION PENALTY
    # ============================================

    if occupancy_ratio < 0.40:

        occupancy_ratio *= 0.50

    return round(
        occupancy_ratio,
        4
    )

# =========================================================
# TRAFFIC REDUCTION SCORE
# =========================================================

def calculate_traffic_reduction(group):

    vehicle = group[
        "recommended_vehicle"
    ]

    passengers = group[
        "passenger_count"
    ]

    vehicles_saved = max(
        0,
        passengers - 1
    )

    traffic_impact = (
        VEHICLE_TRAFFIC_IMPACT[
            vehicle
        ]
    )

    score = (

        vehicles_saved
        * (1 - traffic_impact)
    )

    return round(
        min(1.0, score / 5),
        4
    )

# =========================================================
# FUEL EFFICIENCY
# =========================================================

def calculate_fuel_efficiency(group):

    vehicle = group[
        "recommended_vehicle"
    ]

    passengers = group[
        "passenger_count"
    ]

    fuel_factor = (
        VEHICLE_FUEL_FACTOR[
            vehicle
        ]
    )

    efficiency = (
        passengers / fuel_factor
    )

    return round(
        min(1.0, efficiency / 3),
        4
    )

# =========================================================
# CONGESTION PENALTY
# =========================================================

def calculate_congestion_penalty(group):

    vehicle = group[
        "recommended_vehicle"
    ]

    passengers = group[
        "passenger_count"
    ]

    if vehicle == "BIKE" and passengers == 1:

        return 0.30

    elif vehicle == "AUTO" and passengers < 2:

        return 0.20

    elif vehicle == "CAB" and passengers < 2:

        return 0.35

    return 0.05

# =========================================================
# DELAY PENALTY
# =========================================================

def calculate_delay_penalty(group):

    ride_count = len(
        group["rides"]
    )

    penalty = (
        ride_count * 0.05
    )

    return round(
        min(0.30, penalty),
        4
    )

# =========================================================
# FINAL OPTIMIZATION SCORE
# =========================================================

def calculate_optimization_score(group):

    occupancy_score = (
        calculate_occupancy_efficiency(
            group
        )
    )

    traffic_score = (
        calculate_traffic_reduction(
            group
        )
    )

    fuel_score = (
        calculate_fuel_efficiency(
            group
        )
    )

    congestion_penalty = (
        calculate_congestion_penalty(
            group
        )
    )

    delay_penalty = (
        calculate_delay_penalty(
            group
        )
    )

    # ============================================
    # FINAL WEIGHTED SCORE
    # ============================================

    final_score = (

        occupancy_score * 0.35

        + traffic_score * 0.30

        + fuel_score * 0.25

        - congestion_penalty

        - delay_penalty
    )

    return round(

        max(
            0,
            min(1, final_score)
        ),

        4
    )

# =========================================================
# OPTIMIZE GROUPS
# =========================================================

def optimize_groups(groups):

    optimized_groups = []

    total_passengers = 0

    optimized_vehicle_count = len(
        groups
    )

    # ============================================
    # PROCESS GROUPS
    # ============================================

    for group in groups:

        total_passengers += group[
            "passenger_count"
        ]

        optimization_score = (
            calculate_optimization_score(
                group
            )
        )

        optimized_group = {

            "group_id":
                group["group_id"],

            "rides":
                group["rides"],

            "recommended_vehicle":
                group[
                    "recommended_vehicle"
                ],

            "passenger_count":
                group[
                    "passenger_count"
                ],

            "occupancy_efficiency":
                calculate_occupancy_efficiency(
                    group
                ),

            "traffic_reduction":
                calculate_traffic_reduction(
                    group
                ),

            "fuel_efficiency":
                calculate_fuel_efficiency(
                    group
                ),

            "optimization_score":
                optimization_score
        }

        optimized_groups.append(
            optimized_group
        )

    # ============================================
    # SYSTEM-WIDE METRICS
    # ============================================

    if total_passengers == 0:

        traffic_reduction_ratio = 0

    else:

        traffic_reduction_ratio = (

            1
            - (
                optimized_vehicle_count
                / total_passengers
            )
        )

    system_metrics = {

        "total_passengers":
            total_passengers,

        "vehicles_after_optimization":
            optimized_vehicle_count,

        "traffic_reduction_ratio":
            round(
                traffic_reduction_ratio,
                4
            ),

        "estimated_congestion_reduction":
            round(
                traffic_reduction_ratio
                * 0.8,
                4
            )
    }

    return {

        "optimized_groups":
            optimized_groups,

        "system_metrics":
            system_metrics
    }

# =========================================================
# RUN DYNAMIC OPTIMIZATION
# =========================================================

def run_dynamic_optimization():

    groups = match_rides()

    return optimize_groups(
        groups
    )

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    # ============================================
    # TEST RIDES
    # ============================================

    test_rides = [

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

    for ride in test_rides:

        add_ride(
            ride
        )

    # ============================================
    # RUN OPTIMIZATION
    # ============================================

    results = run_dynamic_optimization()

    # ============================================
    # PRINT GROUP RESULTS
    # ============================================

    print("\n[OPTIMIZED GROUPS]\n")

    for group in results[
        "optimized_groups"
    ]:

        print(group)

    # ============================================
    # PRINT SYSTEM METRICS
    # ============================================

    print("\n[SYSTEM METRICS]\n")

    print(

        results[
            "system_metrics"
        ]
    )