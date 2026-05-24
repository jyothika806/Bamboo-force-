# =========================================================
# BAMBOO FORCE AI
# FINAL URBAN MOBILITY OPTIMIZATION ENGINE
# =========================================================

import uuid
import time



from ai_models.ride_optimization.clustering import (
    create_ride_clusters
)

from ai_models.ride_optimization.recommendation import (
    generate_recommendations
)

from ai_models.ride_optimization.ride_manager import (
    ride_manager_instance
)
from ai_models.ride_optimization.state_manager import (
    state
)
from ai_models.ride_optimization.match_rides import (
    match_rides
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
# MAIN OPTIMIZATION ENGINE
# =========================================================

class UrbanMobilityOptimizationEngine:

    def __init__(self):

        # =============================================
        # CORE SYSTEMS
        # =============================================

        
        
        self.ride_manager = ride_manager_instance
        # =============================================
        # ENGINE STORAGE
        # =============================================


        self.optimization_history = []

        self.system_started_at = (
            time.time()
        )

    # =====================================================
    # ADD NEW RIDE
    # =====================================================

    def add_new_ride(
        self,
        ride_data
    ):

        # =============================================
        # AUTO GENERATE RIDE ID
        # =============================================

        ride_id = ride_data.get(
            "ride_id",
            str(uuid.uuid4())[:8]
        )

        ride_data["ride_id"] = ride_id

        # =============================================
        # DEFAULT VALUES
        # =============================================

        ride_data.setdefault(
            "passenger_count",
            1
        )

        ride_data.setdefault(
            "share_allowed",
            True
        )

        ride_data["created_at"] = (
            time.time()
        )

        # =============================================
        # CREATE RIDE
        # =============================================

        result = (

            self.ride_manager
            .create_ride(
                ride_data
            )
        )

        print("\n[DEBUG RIDE CREATED]\n")

        print(
            self.ride_manager
            .get_active_rides()
        )
        return result
    # =====================================================
    # GET ACTIVE RIDES
    # =====================================================

    def get_active_rides(self):

        return (

            self.ride_manager
            .get_active_rides()
        )

    # =====================================================
    # FIND BEST MATCHES
    # =====================================================

    def find_best_matches(self):

        active_rides = (
            self.get_active_rides()
        )

        if len(active_rides) <= 1:

            return []

        return match_rides()

    # =====================================================
    # CREATE OPTIMIZED GROUPS
    # =====================================================

    def generate_optimized_groups(self):

        active_rides = (
            self.get_active_rides()
        )

        if not active_rides:

            return []

        groups = create_ride_clusters()


        return groups

    # =====================================================
    # GENERATE AI RECOMMENDATIONS
    # =====================================================

    def generate_ai_recommendations(self):

        groups = list(
            state.active_clusters.values()
        )

        if not groups:

            return {}

        return generate_recommendations(
            groups
        )

    # =====================================================
    # OCCUPANCY EFFICIENCY
    # =====================================================

    def calculate_occupancy_efficiency(
        self,
        group
    ):

        passengers = group.get(
            "passenger_count",
            1
        )

        vehicle = group.get(
            "recommended_vehicle",
            "BIKE"
        )

        capacity = VEHICLE_CAPACITY.get(
            vehicle,
            1
        )

        occupancy_ratio = (
            passengers / capacity
        )

        if occupancy_ratio < 0.40:

            occupancy_ratio *= 0.50

        return round(

            min(
                1.0,
                occupancy_ratio
            ),

            4
        )

    # =====================================================
    # TRAFFIC REDUCTION
    # =====================================================

    def calculate_traffic_reduction(
        self,
        group
    ):

        vehicle = group.get(
            "recommended_vehicle",
            "BIKE"
        )

        passengers = group.get(
            "passenger_count",
            1
        )

        vehicles_saved = max(
            0,
            passengers - 1
        )

        traffic_impact = (

            VEHICLE_TRAFFIC_IMPACT.get(
                vehicle,
                0.90
            )
        )

        score = (

            vehicles_saved
            * (1 - traffic_impact)
        )

        return round(

            min(
                1.0,
                score / 5
            ),

            4
        )

    # =====================================================
    # FUEL EFFICIENCY
    # =====================================================

    def calculate_fuel_efficiency(
        self,
        group
    ):

        vehicle = group.get(
            "recommended_vehicle",
            "BIKE"
        )

        passengers = group.get(
            "passenger_count",
            1
        )

        fuel_factor = (

            VEHICLE_FUEL_FACTOR.get(
                vehicle,
                1.0
            )
        )

        efficiency = (
            passengers / fuel_factor
        )

        return round(

            min(
                1.0,
                efficiency / 3
            ),

            4
        )

    # =====================================================
    # CONGESTION PENALTY
    # =====================================================

    def calculate_congestion_penalty(
        self,
        group
    ):

        vehicle = group.get(
            "recommended_vehicle",
            "BIKE"
        )

        passengers = group.get(
            "passenger_count",
            1
        )

        if vehicle == "BIKE" and passengers == 1:

            return 0.30

        if vehicle == "AUTO" and passengers < 2:

            return 0.20

        if vehicle == "CAB" and passengers < 2:

            return 0.35

        return 0.05

    # =====================================================
    # DELAY PENALTY
    # =====================================================

    def calculate_delay_penalty(
        self,
        group
    ):

        ride_count = len(

            group.get(
                "rides",
                []
            )
        )

        penalty = (
            ride_count * 0.05
        )

        return round(

            min(
                0.30,
                penalty
            ),

            4
        )

    # =====================================================
    # FINAL OPTIMIZATION SCORE
    # =====================================================

    def calculate_optimization_score(
        self,
        group
    ):

        occupancy_score = (

            self.calculate_occupancy_efficiency(
                group
            )
        )

        traffic_score = (

            self.calculate_traffic_reduction(
                group
            )
        )

        fuel_score = (

            self.calculate_fuel_efficiency(
                group
            )
        )

        congestion_penalty = (

            self.calculate_congestion_penalty(
                group
            )
        )

        delay_penalty = (

            self.calculate_delay_penalty(
                group
            )
        )

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

    # =====================================================
    # ENABLE DYNAMIC RIDE CHAINING
    # =====================================================

    def enable_dynamic_chaining(self):

        groups = list(
            state.active_clusters.values()
        )

        optimized_groups = []

        for group in groups:

            passenger_count = group.get(
                "passenger_count",
                1
            )

            group[
                "ride_chain_possible"
            ] = (
                passenger_count >= 2
            )

            group[
                "occupancy_efficiency"
            ] = (
                self.calculate_occupancy_efficiency(
                    group
                )
            )

            group[
                "traffic_reduction"
            ] = (
                self.calculate_traffic_reduction(
                    group
                )
            )

            group[
                "fuel_efficiency"
            ] = (
                self.calculate_fuel_efficiency(
                    group
                )
            )

            group[
                "optimization_score"
            ] = (
                self.calculate_optimization_score(
                    group
                )
            )

            optimized_groups.append(
                group
            )

        return optimized_groups

    # =====================================================
    # SYSTEM TRAFFIC IMPACT
    # =====================================================

    def calculate_system_traffic_impact(self):

        total_rides = len(
            self.get_active_rides()
        )

        total_groups = len(
            state.active_clusters
        )

        if total_rides == 0:

            return {

                "traffic_reduction_score":
                    0.0,

                "estimated_vehicle_reduction":
                    0,

                "estimated_congestion_reduction":
                    0.0
            }

        saved_vehicles = max(

            0,

            total_rides
            - total_groups
        )

        reduction_score = (
            saved_vehicles / total_rides
        )

        congestion_reduction = (
            reduction_score * 0.80
        )

        return {

            "traffic_reduction_score":
                round(
                    reduction_score,
                    4
                ),

            "estimated_vehicle_reduction":
                saved_vehicles,

            "estimated_congestion_reduction":
                round(
                    congestion_reduction,
                    4
                )
        }

    # =====================================================
    # RUN COMPLETE AI OPTIMIZATION
    # =====================================================

    def run_dynamic_optimization(self):

        
        # =============================================
        # STEP 2 — CREATE GROUPS
        # =============================================

        self.generate_optimized_groups()

        # =============================================
        # STEP 3 — AI RECOMMENDATIONS
        # =============================================

        recommendations = (

            self.generate_ai_recommendations()
        )

        # =============================================
        # STEP 4 — DYNAMIC CHAINING
        # =============================================

        optimized_groups = (

            self.enable_dynamic_chaining()
        )

        # =============================================
        # STEP 5 — TRAFFIC ANALYSIS
        # =============================================

        traffic_analysis = (

            self.calculate_system_traffic_impact()
        )

        # =============================================
        # FINAL RESULT
        # =============================================

        result = {

            "system_status":
                "ACTIVE",

            "optimization_timestamp":
                time.time(),

            "total_active_rides":
                len(
                    self.get_active_rides()
                ),

            "total_groups":
                len(
                    state.active_clusters
                ),

            

            "optimized_groups":
                optimized_groups,

            "recommendations":
                recommendations,

            "traffic_analysis":
                traffic_analysis
        }

        # =============================================
        # STORE HISTORY
        # =============================================

        self.optimization_history.append(
            result
        )

        return result

    # =====================================================
    # COMPLETE RIDE
    # =====================================================

    def complete_ride(
        self,
        ride_id
    ):

        return (

            self.ride_manager
            .complete_ride(
                ride_id
            )
        )

    # =====================================================
    # CANCEL RIDE
    # =====================================================

    def cancel_ride(
        self,
        ride_id
    ):

        return (

            self.ride_manager
            .cancel_ride(
                ride_id
            )
        )

    # =====================================================
    # UPDATE RIDE LOCATION
    # =====================================================

    def update_ride_location(

        self,
        ride_id,
        location
    ):

        return (

            self.ride_manager
            .update_ride_location(

                ride_id,

                location
            )
        )

    # =====================================================
    # CLEANUP SYSTEM
    # =====================================================

    def cleanup_system(self):

        return (

            self.ride_manager
            .cleanup_stale_rides()
        )

    # =====================================================
    # GET ACTIVE GROUPS
    # =====================================================

    def get_active_groups(self):

        return state.active_clusters

    # =====================================================
    # GET RIDE HISTORY
    # =====================================================

    def get_ride_history(self):

        return (

            self.ride_manager
            .get_ride_history()
        )

    # =====================================================
    # SYSTEM METRICS
    # =====================================================

    def get_system_metrics(self):

        total_rides = len(
            self.get_active_rides()
        )

        total_groups = len(
            state.active_clusters
        )

        occupancy = 0

        if total_groups > 0:

            occupancy = (
                total_rides / total_groups
            )

        return {

            "system_status":
                "RUNNING",

            "system_uptime_seconds":
                round(

                    time.time()
                    - self.system_started_at,

                    2
                ),

            "total_rides":
                total_rides,

            "total_groups":
                total_groups,

            "average_occupancy":
                round(
                    occupancy,
                    2
                ),

            "optimization_cycles":
                len(
                    self.optimization_history
                )
        }

# =========================================================
# GLOBAL ENGINE INSTANCE
# =========================================================

optimization_engine = (
    UrbanMobilityOptimizationEngine()
)

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    sample_rides = [

        {

            "ride_id": "R001",

            "source": [
                17.3850,
                78.4867
            ],

            "destination": [
                17.4435,
                78.3772
            ],

            "passenger_count": 2,

            "share_allowed": True
        },

        {

            "ride_id": "R002",

            "source": [
                17.3870,
                78.4800
            ],

            "destination": [
                17.4410,
                78.3790
            ],

            "passenger_count": 1,

            "share_allowed": True
        },

        {

            "ride_id": "R003",

            "source": [
                17.5000,
                78.6000
            ],

            "destination": [
                17.6500,
                78.7200
            ],

            "passenger_count": 1,

            "share_allowed": False
        }
    ]

    # =============================================
    # LOAD RIDES
    # =============================================

    for ride in sample_rides:

        optimization_engine.add_new_ride(
            ride
        )

    # =============================================
    # RUN OPTIMIZATION
    # =============================================

    result = (

        optimization_engine
        .run_dynamic_optimization()
    )

    # =============================================
    # OUTPUT
    # =============================================

    print("\n[SMART CITY AI OPTIMIZATION RESULT]\n")

    print(result)

    print("\n[SYSTEM METRICS]\n")

    print(

        optimization_engine
        .get_system_metrics()
    )