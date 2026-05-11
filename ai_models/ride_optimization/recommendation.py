# =========================================================
# BAMBOO FORCE AI
# AI RECOMMENDATION ENGINE
# =========================================================

from statistics import mean

# =========================================================
# VEHICLE CONFIGURATION
# =========================================================

VEHICLE_BASE_COST = {

    "BIKE": 60,
    "AUTO": 120,
    "CAB": 200,
    "VAN": 350
}

VEHICLE_CAPACITY = {

    "BIKE": 1,
    "AUTO": 3,
    "CAB": 4,
    "VAN": 7
}

# =========================================================
# RECOMMENDATION ENGINE
# =========================================================

class RecommendationEngine:

    # =====================================================
    # OCCUPANCY EFFICIENCY
    # =====================================================

    def calculate_occupancy_efficiency(

        self,
        vehicle,
        passenger_count
    ):

        capacity = VEHICLE_CAPACITY.get(
            vehicle,
            1
        )

        occupancy = (
            passenger_count / capacity
        )

        return round(
            min(1.0, occupancy),
            4
        )

    # =====================================================
    # ESTIMATE COST SAVINGS
    # =====================================================

    def estimate_cost_savings(

        self,
        vehicle,
        passenger_count
    ):

        base_cost = VEHICLE_BASE_COST.get(
            vehicle,
            100
        )

        if passenger_count <= 1:

            return 0

        shared_cost = (
            base_cost
            / passenger_count
        )

        savings = (
            base_cost
            - shared_cost
        )

        return round(
            max(0, savings),
            2
        )

    # =====================================================
    # TRAFFIC REDUCTION SCORE
    # =====================================================

    def calculate_traffic_score(

        self,
        passenger_count
    ):

        score = min(
            1.0,
            passenger_count / 5
        )

        return round(
            score,
            4
        )

    # =====================================================
    # ENVIRONMENTAL SCORE
    # =====================================================

    def calculate_environment_score(

        self,
        passenger_count
    ):

        score = min(
            1.0,
            passenger_count / 6
        )

        return round(
            score,
            4
        )

    # =====================================================
    # RIDE CHAINING POTENTIAL
    # =====================================================

    def calculate_chain_potential(

        self,
        passenger_count
    ):

        if passenger_count >= 3:

            return "HIGH"

        elif passenger_count == 2:

            return "MEDIUM"

        return "LOW"

    # =====================================================
    # CONFIDENCE SCORE
    # =====================================================

    def calculate_confidence_score(

        self,
        group
    ):

        vehicle = group.get(
            "recommended_vehicle",
            "BIKE"
        )

        capacity = VEHICLE_CAPACITY.get(
            vehicle,
            1
        )

        occupancy = (

            group.get(
                "passenger_count",
                1
            )

            / capacity
        )

        optimization_score = group.get(

            "optimization_score",
            0.5
        )

        confidence = (

            occupancy * 0.5

            + optimization_score * 0.5
        )

        return round(
            min(1.0, confidence),
            4
        )

    # =====================================================
    # VEHICLE STRATEGY
    # =====================================================

    def recommend_vehicle_strategy(

        self,
        vehicle,
        passenger_count
    ):

        occupancy = (

            self.calculate_occupancy_efficiency(

                vehicle,

                passenger_count
            )
        )

        # =================================================
        # UNDERUTILIZATION
        # =================================================

        if occupancy < 0.40:

            if vehicle == "VAN":

                return {

                    "action":
                        "DOWNGRADE",

                    "recommended_vehicle":
                        "CAB",

                    "reason":
                        "Vehicle underutilized"
                }

            if vehicle == "CAB":

                return {

                    "action":
                        "DOWNGRADE",

                    "recommended_vehicle":
                        "AUTO",

                    "reason":
                        "Reduce congestion"
                }

        # =================================================
        # OVERUTILIZATION
        # =================================================

        if occupancy > 0.90:

            if vehicle == "AUTO":

                return {

                    "action":
                        "UPGRADE",

                    "recommended_vehicle":
                        "CAB",

                    "reason":
                        "Improve ride comfort"
                }

        return {

            "action":
                "KEEP",

            "recommended_vehicle":
                vehicle,

            "reason":
                "Current allocation optimized"
        }

    # =====================================================
    # PASSENGER RECOMMENDATION
    # =====================================================

    def generate_passenger_recommendation(

        self,
        group
    ):

        passenger_count = group.get(
            "passenger_count",
            1
        )

        vehicle = group.get(
            "recommended_vehicle",
            "BIKE"
        )

        strategy = (

            self.recommend_vehicle_strategy(

                vehicle,

                passenger_count
            )
        )

        return {

            "group_id":
                group.get(
                    "group_id",
                    "UNKNOWN"
                ),

            "recommended_vehicle":
                strategy[
                    "recommended_vehicle"
                ],

            "vehicle_action":
                strategy[
                    "action"
                ],

            "reason":
                strategy[
                    "reason"
                ],

            "estimated_cost_savings":
                self.estimate_cost_savings(

                    vehicle,

                    passenger_count
                ),

            "traffic_reduction_score":
                self.calculate_traffic_score(

                    passenger_count
                ),

            "environmental_score":
                self.calculate_environment_score(

                    passenger_count
                ),

            "ride_chain_potential":
                self.calculate_chain_potential(

                    passenger_count
                ),

            "confidence_score":
                self.calculate_confidence_score(
                    group
                ),

            "recommended_sharing":
                passenger_count > 1
        }

    # =====================================================
    # DRIVER RECOMMENDATION
    # =====================================================

    def generate_driver_recommendation(

        self,
        group
    ):

        rides = sorted(
            group.get("rides", [])
        )

        return {

            "group_id":
                group.get(
                    "group_id",
                    "UNKNOWN"
                ),

            "pickup_sequence":
                rides,

            "occupancy_target":
                group.get(
                    "passenger_count",
                    1
                ),

            "recommended_vehicle":
                group.get(
                    "recommended_vehicle",
                    "BIKE"
                ),

            "driving_strategy":
                "MINIMIZE_CONGESTION",

            "route_strategy":
                "DYNAMIC_SHARED_ROUTE",

            "chain_ready":
                group.get(
                    "passenger_count",
                    1
                ) >= 2
        }

    # =====================================================
    # SYSTEM RECOMMENDATION
    # =====================================================

    def generate_system_recommendation(

        self,
        groups
    ):

        if not groups:

            return {

                "system_status":
                    "LOW_ACTIVITY"
            }

        total_passengers = sum(

            group.get(
                "passenger_count",
                1
            )

            for group in groups
        )

        avg_occupancy = mean([

            group.get(
                "passenger_count",
                1
            )

            for group in groups
        ])

        avg_optimization = mean([

            group.get(
                "optimization_score",
                0
            )

            for group in groups
        ])

        return {

            "system_status":
                "ACTIVE",

            "total_groups":
                len(groups),

            "total_passengers":
                total_passengers,

            "average_group_occupancy":
                round(avg_occupancy, 2),

            "average_optimization_score":
                round(avg_optimization, 4),

            "city_strategy":
                "MAXIMIZE_SHARED_OCCUPANCY",

            "recommended_focus":
                "TRAFFIC_REDUCTION"
        }

# =========================================================
# GLOBAL RECOMMENDATION FUNCTION
# =========================================================

def generate_recommendations(groups):

    engine = RecommendationEngine()

    passenger_recommendations = []

    driver_recommendations = []

    for group in groups:

        passenger_recommendations.append(

            engine.generate_passenger_recommendation(
                group
            )
        )

        driver_recommendations.append(

            engine.generate_driver_recommendation(
                group
            )
        )

    system_recommendation = (

        engine.generate_system_recommendation(
            groups
        )
    )

    return {

        "passenger_recommendations":
            passenger_recommendations,

        "driver_recommendations":
            driver_recommendations,

        "system_recommendation":
            system_recommendation
    }

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    sample_groups = [

        {

            "group_id": "G001",

            "rides": [
                "R001",
                "R002"
            ],

            "passenger_count": 3,

            "recommended_vehicle":
                "AUTO",

            "optimization_score":
                0.92
        },

        {

            "group_id": "G002",

            "rides": [
                "R003"
            ],

            "passenger_count": 1,

            "recommended_vehicle":
                "BIKE",

            "optimization_score":
                0.65
        }
    ]

    recommendations = (
        generate_recommendations(
            sample_groups
        )
    )

    print("\n[PASSENGER RECOMMENDATIONS]\n")

    for recommendation in recommendations[
        "passenger_recommendations"
    ]:

        print(recommendation)

    print("\n[DRIVER RECOMMENDATIONS]\n")

    for recommendation in recommendations[
        "driver_recommendations"
    ]:

        print(recommendation)

    print("\n[SYSTEM RECOMMENDATION]\n")

    print(

        recommendations[
            "system_recommendation"
        ]
    )