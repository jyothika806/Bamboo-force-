# =========================================================
# BAMBOO FORCE AI
# ROUTE SIMILARITY ENGINE
# =========================================================

import math

from collections import defaultdict

# =========================================================
# CONFIGURATION
# =========================================================

EARTH_RADIUS_KM = 6371

MAX_SOURCE_DISTANCE = 3
MAX_DESTINATION_DISTANCE = 5

MIN_DIRECTION_SIMILARITY = 0.5

SIMILARITY_THRESHOLD = 0.70

MAX_TIME_DIFFERENCE = 15

ZONE_PRECISION = 2

MAX_GROUP_PASSENGERS = 7

# =========================================================
# HAVERSINE DISTANCE
# =========================================================

def haversine_distance(
    lat1,
    lon1,
    lat2,
    lon2
):

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)

    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = (

        math.sin(delta_lat / 2) ** 2

        + math.cos(lat1_rad)
        * math.cos(lat2_rad)

        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(

        math.sqrt(a),

        math.sqrt(1 - a)
    )

    return EARTH_RADIUS_KM * c

# =========================================================
# DIRECTION VECTOR
# =========================================================

def get_direction_vector(ride):

    source = ride.get(
        "source",
        (0, 0)
    )

    destination = ride.get(
        "destination",
        (0, 0)
    )

    return (

        destination[0] - source[0],

        destination[1] - source[1]
    )

# =========================================================
# COSINE SIMILARITY
# =========================================================

def cosine_similarity(
    vector_a,
    vector_b
):

    dot_product = (

        vector_a[0] * vector_b[0]

        + vector_a[1] * vector_b[1]
    )

    magnitude_a = math.sqrt(

        vector_a[0] ** 2

        + vector_a[1] ** 2
    )

    magnitude_b = math.sqrt(

        vector_b[0] ** 2

        + vector_b[1] ** 2
    )

    if magnitude_a == 0 or magnitude_b == 0:

        return 0

    return dot_product / (
        magnitude_a * magnitude_b
    )

# =========================================================
# CREATE GEO ZONE
# =========================================================

def create_zone(
    lat,
    lon
):

    return (

        round(lat, ZONE_PRECISION),

        round(lon, ZONE_PRECISION)
    )

# =========================================================
# GROUP RIDES BY SOURCE ZONE
# =========================================================

def group_rides_by_zone(rides):

    grouped_rides = defaultdict(list)

    for ride in rides:

        source = ride.get(
            "source",
            (0, 0)
        )

        zone = create_zone(

            source[0],

            source[1]
        )

        grouped_rides[zone].append(
            ride
        )

    return grouped_rides

# =========================================================
# TIME COMPATIBILITY
# =========================================================

def is_time_compatible(
    ride_a,
    ride_b
):

    return abs(

        ride_a.get(
            "start_time",
            0
        )

        - ride_b.get(
            "start_time",
            0
        )

    ) <= MAX_TIME_DIFFERENCE

# =========================================================
# CALCULATE ROUTE SIMILARITY
# =========================================================

def calculate_similarity(
    ride_a,
    ride_b
):

    source_a = ride_a.get(
        "source",
        (0, 0)
    )

    source_b = ride_b.get(
        "source",
        (0, 0)
    )

    destination_a = ride_a.get(
        "destination",
        (0, 0)
    )

    destination_b = ride_b.get(
        "destination",
        (0, 0)
    )

    # =====================================================
    # SOURCE DISTANCE
    # =====================================================

    source_distance = haversine_distance(

        source_a[0],
        source_a[1],

        source_b[0],
        source_b[1]
    )

    if source_distance > MAX_SOURCE_DISTANCE:

        return 0

    # =====================================================
    # DESTINATION DISTANCE
    # =====================================================

    destination_distance = haversine_distance(

        destination_a[0],
        destination_a[1],

        destination_b[0],
        destination_b[1]
    )

    if destination_distance > MAX_DESTINATION_DISTANCE:

        return 0

    # =====================================================
    # DIRECTION SIMILARITY
    # =====================================================

    direction_vector_a = get_direction_vector(
        ride_a
    )

    direction_vector_b = get_direction_vector(
        ride_b
    )

    direction_similarity = cosine_similarity(

        direction_vector_a,

        direction_vector_b
    )

    if direction_similarity < MIN_DIRECTION_SIMILARITY:

        return 0

    # =====================================================
    # NORMALIZED SCORES
    # =====================================================

    source_score = (

        1

        - (
            source_distance
            / MAX_SOURCE_DISTANCE
        )
    )

    destination_score = (

        1

        - (
            destination_distance
            / MAX_DESTINATION_DISTANCE
        )
    )

    # =====================================================
    # FINAL WEIGHTED SCORE
    # =====================================================

    similarity_score = (

        source_score * 0.35

        + destination_score * 0.35

        + direction_similarity * 0.30
    )

    return round(
        similarity_score,
        4
    )

# =========================================================
# FIND SIMILAR RIDES
# =========================================================

def find_similar_rides(rides):

    matched_rides = []

    grouped_rides = group_rides_by_zone(
        rides
    )

    for zone, zone_rides in grouped_rides.items():

        if len(zone_rides) <= 1:

            continue

        total_rides = len(
            zone_rides
        )

        for i in range(total_rides):

            ride_a = zone_rides[i]

            for j in range(i + 1, total_rides):

                ride_b = zone_rides[j]

                # =================================================
                # SHARE FILTER
                # =================================================

                if not ride_a.get(
                    "share_allowed",
                    True
                ):

                    continue

                if not ride_b.get(
                    "share_allowed",
                    True
                ):

                    continue

                # =================================================
                # TIME FILTER
                # =================================================

                if not is_time_compatible(

                    ride_a,

                    ride_b
                ):

                    continue

                # =================================================
                # PASSENGER LIMIT
                # =================================================

                combined_passengers = (

                    ride_a.get(
                        "passenger_count",
                        1
                    )

                    + ride_b.get(
                        "passenger_count",
                        1
                    )
                )

                if combined_passengers > MAX_GROUP_PASSENGERS:

                    continue

                # =================================================
                # SIMILARITY CALCULATION
                # =================================================

                similarity_score = calculate_similarity(

                    ride_a,

                    ride_b
                )

                # =================================================
                # MATCH FOUND
                # =================================================

                if similarity_score >= SIMILARITY_THRESHOLD:

                    matched_rides.append({

                        "ride_a":
                            ride_a.get(
                                "ride_id"
                            ),

                        "ride_b":
                            ride_b.get(
                                "ride_id"
                            ),

                        "similarity_score":
                            similarity_score,

                        "share_recommended":
                            True,

                        "match_type":
                            "DYNAMIC_SHARED_ROUTE",

                        "estimated_vehicle_reduction":
                            1
                    })

    return matched_rides

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

            "share_allowed": False,

            "passenger_count": 1
        }
    ]

    results = find_similar_rides(
        rides
    )

    print("\n[SIMILAR RIDE MATCHES]\n")

    for result in results:

        print(result)