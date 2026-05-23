from geopy.geocoders import (
    Nominatim
)

# =====================================================
# GEOLOCATOR
# =====================================================

geolocator = Nominatim(
    user_agent="bamboo_force_ai"
)

# =====================================================
# GET COORDINATES
# =====================================================

def get_coordinates(place):

    try:

        location = geolocator.geocode(
            place,
                timeout=5
        )

        if location:

            return (

                location.latitude,

                location.longitude
            )

        return None

    except Exception as e:

        print(
            "Geocoding Error:",
            e
        )

        return None


# =====================================================
# TESTING
# =====================================================

if __name__ == "__main__":

    coords = get_coordinates(
        "Hitech City Hyderabad"
    )

    print(coords)