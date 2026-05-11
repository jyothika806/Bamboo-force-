# =========================================================
# BAMBOO FORCE AI
# REAL-TIME RIDE LIFECYCLE MANAGER
# =========================================================

import time
import threading

from ai_models.ride_optimization.match_rides import (
    add_ride,
    remove_ride
)

from ai_models.ride_optimization.clustering import (
    create_ride_clusters
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

        self.completed_rides = {}

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

            "event":
                event_type,

            "ride_id":
                ride_id,

            "timestamp":
                time.time(),

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

    def create_ride(
        self,
        ride
    ):

        with self.lock:

            ride_id = ride.get(
                "ride_id"
            )

            if not ride_id:

                return {

                    "success": False,

                    "message":
                        "Ride ID missing"
                }

            # =====================================
            # DEFAULT VALUES
            # =====================================

            ride.setdefault(
                "passenger_count",
                1
            )

            ride.setdefault(
                "share_allowed",
                True
            )

            ride["status"] = "WAITING"

            ride["created_at"] = (
                time.time()
            )

            ride["current_location"] = (
                ride.get(
                    "source",
                    (0, 0)
                )
            )

            # =====================================
            # STORE LOCALLY
            # =====================================

            self.active_rides[
                ride_id
            ] = ride

            # =====================================
            # STORE GLOBALLY
            # =====================================

            add_ride(
                ride
            )

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

                    f"{ride_id}"
                    f"_P{index + 1}"
                )

                self.register_passenger(

                    passenger_id,

                    ride_id
                )

            # =====================================
            # LOG EVENT
            # =====================================

            self.log_event(

                "RIDE_CREATED",

                ride_id
            )

        # =========================================
        # DYNAMIC REOPTIMIZATION
        # =========================================

        self.trigger_reoptimization()

        return {

            "success": True,

            "ride_id":
                ride_id,

            "status":
                "WAITING"
        }

    # =====================================================
    # START RIDE
    # =====================================================

    def start_ride(
        self,
        ride_id
    ):

        with self.lock:

            ride = self.active_rides.get(
                ride_id
            )

            if not ride:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            ride["status"] = (
                "IN_PROGRESS"
            )

            ride["started_at"] = (
                time.time()
            )

            self.log_event(

                "RIDE_STARTED",

                ride_id
            )

            return {

                "success": True,

                "ride_id":
                    ride_id,

                "status":
                    "IN_PROGRESS"
            }

    # =====================================================
    # COMPLETE RIDE
    # =====================================================

    def complete_ride(
        self,
        ride_id
    ):

        with self.lock:

            ride = self.active_rides.get(
                ride_id
            )

            if not ride:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            ride["status"] = (
                "COMPLETED"
            )

            ride["completed_at"] = (
                time.time()
            )

            self.completed_rides[
                ride_id
            ] = ride

            remove_ride(
                ride_id
            )

            del self.active_rides[
                ride_id
            ]

            self.log_event(

                "RIDE_COMPLETED",

                ride_id
            )

        # =========================================
        # REOPTIMIZATION
        # =========================================

        self.trigger_reoptimization()

        return {

            "success": True,

            "ride_id":
                ride_id,

            "status":
                "COMPLETED"
        }

    # =====================================================
    # CANCEL RIDE
    # =====================================================

    def cancel_ride(
        self,
        ride_id
    ):

        with self.lock:

            ride = self.active_rides.get(
                ride_id
            )

            if not ride:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            ride["status"] = (
                "CANCELLED"
            )

            ride["cancelled_at"] = (
                time.time()
            )

            remove_ride(
                ride_id
            )

            del self.active_rides[
                ride_id
            ]

            self.log_event(

                "RIDE_CANCELLED",

                ride_id
            )

        # =========================================
        # REOPTIMIZATION
        # =========================================

        self.trigger_reoptimization()

        return {

            "success": True,

            "ride_id":
                ride_id,

            "status":
                "CANCELLED"
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

            ride = self.active_rides.get(
                ride_id
            )

            if not ride:

                return {

                    "success": False,

                    "message":
                        "Ride not found"
                }

            ride["current_location"] = (
                location
            )

            ride["last_location_update"] = (
                time.time()
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

                "ride_id":
                    ride_id,

                "location":
                    location
            }

    # =====================================================
    # DYNAMIC REOPTIMIZATION
    # =====================================================

    def trigger_reoptimization(self):

        with self.lock:

            optimization_results = (
                create_ride_clusters()
            )

            # =====================================
            # RESET GROUPS
            # =====================================

            self.active_groups.clear()

            for group in optimization_results:

                cluster_id = group.get(
                    "cluster_id"
                )

                self.active_groups[
                    cluster_id
                ] = group

                # =================================
                # UPDATE MATCHED STATUS
                # =================================

                for ride_id in group.get(
                    "rides",
                    []
                ):

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
                    - ride.get(
                        "created_at",
                        current_time
                    )
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

    def get_completed_rides(self):

        return self.completed_rides

    def get_ride_history(self):

        return self.ride_history

    # =====================================================
    # SYSTEM METRICS
    # =====================================================

    def get_system_metrics(self):

        return {

            "active_rides":
                len(
                    self.active_rides
                ),

            "active_groups":
                len(
                    self.active_groups
                ),

            "completed_rides":
                len(
                    self.completed_rides
                ),

            "active_passengers":
                len(
                    self.active_passengers
                ),

            "history_events":
                len(
                    self.ride_history
                ),

            "system_status":
                "RUNNING"
        }

# =========================================================
# TESTING
# =========================================================

if __name__ == "__main__":

    manager = RideManager()

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
        }
    ]

    # =====================================================
    # CREATE RIDES
    # =====================================================

    for ride in rides:

        manager.create_ride(
            ride
        )

    print("\n[ACTIVE RIDES]\n")

    print(
        manager.get_active_rides()
    )

    print("\n[ACTIVE GROUPS]\n")

    print(
        manager.get_active_groups()
    )

    print("\n[SYSTEM METRICS]\n")

    print(
        manager.get_system_metrics()
    )