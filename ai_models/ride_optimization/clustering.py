# =========================================================
# BAMBOO FORCE AI
# SMART RIDE CLUSTERING ENGINE
# =========================================================

from uuid import uuid4

from ai_models.ride_optimization.match_rides import (
    match_rides
)
from ai_models.ride_optimization.state_manager import (
    state
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



# =========================================================
# OCCUPANCY SCORE
# =========================================================

def calculate_occupancy_score(
    passenger_count,
    vehicle
):

    capacity = VEHICLE_CAPACITY.get(
        vehicle,
        1
    )

    return round(

        passenger_count / capacity,

        2
    )

# =========================================================
# TRAFFIC REDUCTION SCORE
# =========================================================

def calculate_traffic_reduction(
    passenger_count
):

    return round(

        min(
            1.0,
            (passenger_count - 1) / 6
        ),

        2
    )

# =========================================================
# CLUSTER EFFICIENCY SCORE
# =========================================================

def calculate_cluster_efficiency(
    occupancy_score,
    traffic_score
):

    efficiency = (

        occupancy_score * 0.6

        + traffic_score * 0.4
    )

    return round(
        efficiency,
        2
    )

# =========================================================
# CREATE CLUSTER
# =========================================================

def create_cluster(group):

    cluster_id = str(
        uuid4()
    )[:8]

    passenger_count = group.get(
        "passenger_count",
        1
    )

    vehicle = group.get(
        "recommended_vehicle",
        "AUTO"
    )

    occupancy_score = (
        calculate_occupancy_score(

            passenger_count,

            vehicle
        )
    )

    traffic_score = (
        calculate_traffic_reduction(
            passenger_count
        )
    )

    efficiency_score = (
        calculate_cluster_efficiency(

            occupancy_score,

            traffic_score
        )
    )

    cluster = {

        "cluster_id":
            cluster_id,

        "group_id":
            group.get(
                "group_id"
            ),

        "rides":
            group.get(
                "rides",
                []
            ),

        "passenger_count":
            passenger_count,

        "recommended_vehicle":
            vehicle,

        "occupancy_score":
            occupancy_score,

        "traffic_reduction_score":
            traffic_score,

        "cluster_efficiency":
            efficiency_score,

        "dynamic_chain_ready":
            passenger_count >= 2,

        "cluster_status":
            "ACTIVE"
    }

    with state.lock:

        state.active_clusters[
            cluster_id
        ] = cluster

    return cluster

# =========================================================
# CREATE RIDE CLUSTERS
# =========================================================

def create_ride_clusters():

    state.clear_clusters()

    groups = match_rides()

    clusters = []

    for group in groups:

        cluster = create_cluster(
            group
        )

        clusters.append(
            cluster
        )

    return clusters

# =========================================================
# GET ACTIVE CLUSTERS
# =========================================================

def get_active_clusters():

    return state.active_clusters

# =========================================================
# CLUSTER METRICS
# =========================================================

def get_cluster_metrics():

    total_clusters = len(
        state.active_clusters
    )

    total_passengers = sum(

        cluster.get(
            "passenger_count",
            0
        )

        for cluster in state.active_clusters.values()
    )

    avg_efficiency = 0

    if total_clusters > 0:

        avg_efficiency = round(

            sum(

                cluster.get(
                    "cluster_efficiency",
                    0
                )

                for cluster
                in state.active_clusters.values()
            )

            / total_clusters,

            2
        )

    return {

        "total_clusters":
            total_clusters,

        "total_passengers":
            total_passengers,

        "average_cluster_efficiency":
            avg_efficiency,

        "system_status":
            "ACTIVE"
    }

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    clusters = create_ride_clusters()

    print("\n[SMART CLUSTERS]\n")

    for cluster in clusters:

        print(cluster)

    print("\n[CLUSTER METRICS]\n")

    print(
        get_cluster_metrics()
    )