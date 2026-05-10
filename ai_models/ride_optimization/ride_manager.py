import time
import threading

from ai_models.ride_optimization.match_rides import (
    add_ride,
    remove_ride,
    match_rides
)

from ai_models.ride_optimization.optimization_engine import (
    optimize_groups
)

# =========================================================
# RIDE MANAGER
# =========================================================

class RideManager:

    def __init__(self):

        # =========================================
        # ACTIVE SYSTEM STATE
        # =========================================

        self.active_rides = {}

        self.active_groups = {}

        self.active_passengers = {}

        self.ride_history = []

        # =========================================
        # THREAD-SAFE LOCK
        # =========================================

        self.lock = threading.RLock()

        # =========================================
        # CONFIGURATION
        # =========================================

        self.ride_expiry_seconds = 3600

    # =====================================================
    # EVENT LOGGER
    # =====================================================

    def log_event(

        self,
        event_type,
        ride_id,
        metadata=None
    ):

        event = {

            "event": event_type,

            "ride_id": ride_id,

            "timestamp": time.time(),

            "metadata":
                metadata or {}
        }

        self.ride_history.append(
            event
        )

    # =====================================================
    # REGISTER PASSENGER
    # =====================================================

    def register_passenger(

        self,
        passenger_id,
        ride_id
    ):

        self.active_passengers[
            passenger_id
        ] = {

            "ride_id":
                ride_id,

            "joined_at":
                time.time(),

            "status":
                "ACTIVE"
        }

    # =====================================================
    # CREATE RIDE
    # =====================================================

    def create_ride(self, ride):

        with self.lock:

            ride["status"] = "WAITING"

            ride["created_at"] = time.time()

            ride["current_location"] = (
                ride["source"]
            )

            # =====================================
            # STORE LOCALLY
            # =====================================

            self.active_rides[
                ride["ride_id"]
            ] = ride

            # =====================================
            # STORE GLOBALLY
            # =====================================

            add_ride(ride)

            # =====================================
            # REGISTER PASSENGERS
            # =====================================

            passenger_count = ride.get(

                "passenger_count",
                1
            )

            for index in range(

                passenger_count
            ):

                passenger_id = (

                    f"{ride['ride_id']}"
                    f"_P{index+1}"
                )

                self.register_passenger(

                    passenger_id,
                    ride["ride_id"]
                )

            # =====================================
            # LOG EVENT
            # =====================================

            self.log_event(

                "RIDE_CREATED",

                ride["ride_id"]
            )

        # =========================================
        # DYNAMIC RE-OPTIMIZATION
        # =========================================

        self.trigger_reoptimization()

        return ride

    # =====================================================
    # START RIDE
    # =====================================================

    def start_ride(self, ride_id):

        with self.lock:

            if ride_id not in self.active_rides:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            self.active_rides[
                ride_id
            ]["status"] = "IN_PROGRESS"

            self.log_event(

                "RIDE_STARTED",

                ride_id
            )

            return {

                "success": True,

                "ride_id": ride_id,

                "status": "IN_PROGRESS"
            }

    # =====================================================
    # COMPLETE RIDE
    # =====================================================

    def complete_ride(self, ride_id):

        with self.lock:

            if ride_id not in self.active_rides:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            self.active_rides[
                ride_id
            ]["status"] = "COMPLETED"

            remove_ride(
                ride_id
            )

            self.log_event(

                "RIDE_COMPLETED",

                ride_id
            )

            del self.active_rides[
                ride_id
            ]

            return {

                "success": True,

                "ride_id": ride_id,

                "status": "COMPLETED"
            }

    # =====================================================
    # CANCEL RIDE
    # =====================================================

    def cancel_ride(self, ride_id):

        with self.lock:

            if ride_id not in self.active_rides:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            self.active_rides[
                ride_id
            ]["status"] = "CANCELLED"

            remove_ride(
                ride_id
            )

            self.log_event(

                "RIDE_CANCELLED",

                ride_id
            )

            del self.active_rides[
                ride_id
            ]

            return {

                "success": True,

                "ride_id": ride_id,

                "status": "CANCELLED"
            }

    # =====================================================
    # UPDATE LIVE LOCATION
    # =====================================================

    def update_ride_location(

        self,
        ride_id,
        location
    ):

        with self.lock:

            if ride_id not in self.active_rides:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            self.active_rides[
                ride_id
            ]["current_location"] = (
                location
            )

            self.log_event(

                "LOCATION_UPDATED",

                ride_id,

                {

                    "location":
                        location
                }
            )

            return {

                "success": True,

                "ride_id": ride_id,

                "location": location
            }

    # =====================================================
    # JOIN EXISTING GROUP
    # =====================================================

    def join_group(

        self,
        group_id,
        new_ride
    ):

        with self.lock:

            if group_id not in self.active_groups:

                return {

                    "success": False,

                    "message":
                        "Group not found"
                }

            group = self.active_groups[
                group_id
            ]

            vehicle_capacity = {

                "BIKE": 1,
                "AUTO": 3,
                "CAB": 4,
                "VAN": 7
            }

            vehicle = group[
                "recommended_vehicle"
            ]

            current_count = group[
                "passenger_count"
            ]

            additional_count = new_ride.get(

                "passenger_count",
                1
            )

            if (

                current_count
                + additional_count

            ) > vehicle_capacity[
                vehicle
            ]:

                return {

                    "success": False,

                    "message":
                        "Vehicle full"
                }

            # =====================================
            # CREATE NEW RIDE
            # =====================================

            self.create_ride(
                new_ride
            )

            # =====================================
            # UPDATE GROUP
            # =====================================

            group["rides"].append(

                new_ride["ride_id"]
            )

            group["passenger_count"] += (
                additional_count
            )

            self.log_event(

                "PASSENGER_JOINED_GROUP",

                new_ride["ride_id"],

                {

                    "group_id":
                        group_id
                }
            )

        # =========================================
        # RE-OPTIMIZATION
        # =========================================

        self.trigger_reoptimization()

        return {

            "success": True,

            "group_id": group_id
        }

    # =====================================================
    # TRIGGER DYNAMIC RE-OPTIMIZATION
    # =====================================================

    def trigger_reoptimization(self):

        with self.lock:

            groups = match_rides()

            optimization_results = (

                optimize_groups(
                    groups
                )
            )

            # =====================================
            # RESET GROUPS
            # =====================================

            self.active_groups.clear()

            for group in optimization_results[
                "optimized_groups"
            ]:

                self.active_groups[
                    group["group_id"]
                ] = group

                # =================================
                # UPDATE RIDE STATUS
                # =================================

                for ride_id in group[
                    "rides"
                ]:

                    if (

                        ride_id
                        in self.active_rides
                    ):

                        self.active_rides[
                            ride_id
                        ]["status"] = (
                            "MATCHED"
                        )

            self.log_event(

                "SYSTEM_REOPTIMIZED",

                "GLOBAL"
            )

            return optimization_results

    # =====================================================
    # CLEANUP STALE RIDES
    # =====================================================

    def cleanup_stale_rides(self):

        current_time = time.time()

        stale_rides = []

        with self.lock:

            for ride_id, ride in list(

                self.active_rides.items()
            ):

                age = (

                    current_time
                    - ride["created_at"]
                )

                if (

                    age
                    > self.ride_expiry_seconds
                ):

                    stale_rides.append(
                        ride_id
                    )

            for ride_id in stale_rides:

                remove_ride(
                    ride_id
                )

                del self.active_rides[
                    ride_id
                ]

                self.log_event(

                    "STALE_RIDE_REMOVED",

                    ride_id
                )

        return stale_rides

    # =====================================================
    # GETTERS
    # =====================================================

    def get_active_rides(self):

        return self.active_rides

    def get_active_groups(self):

        return self.active_groups

    def get_ride_history(self):

        return self.ride_history

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    manager = RideManager()

    # =============================================
    # TEST RIDES
    # =============================================

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

    # =============================================
    # CREATE RIDES
    # =============================================

    for ride in rides:

        manager.create_ride(
            ride
        )

    # =============================================
    # ACTIVE GROUPS
    # =============================================

    print("\n[ACTIVE GROUPS]\n")

    print(

        manager.get_active_groups()
    )

    # =============================================
    # UPDATE LOCATION
    # =============================================

    print("\n[LOCATION UPDATE]\n")

    print(

        manager.update_ride_location(

            "R001",

            (
                17.4000,
                78.4900
            )
        )
    )

    # =============================================
    # START RIDE
    # =============================================

    print("\n[START RIDE]\n")

    print(

        manager.start_ride(
            "R001"
        )
    )

    # =============================================
    # COMPLETE RIDE
    # =============================================

    print("\n[COMPLETE RIDE]\n")

    print(

        manager.complete_ride(
            "R001"
        )
    )

    # =============================================
    # RIDE HISTORY
    # =============================================

    print("\n[RIDE HISTORY]\n")

    for event in manager.get_ride_history():

        print(event)