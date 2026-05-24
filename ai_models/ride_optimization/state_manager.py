# =========================================================
# BAMBOO FORCE AI
# CENTRALIZED THREAD-SAFE STATE MANAGER
# =========================================================

from threading import RLock


class SystemState:

    def __init__(self):

        # =============================================
        # THREAD LOCK
        # =============================================

        self.lock = RLock()

        # =============================================
        # SHARED STATE
        # =============================================

        self.active_rides = {}

        self.active_groups = {}

        self.active_clusters = {}
        self.active_passengers = {}
        self.ride_history = {}

        self.completed_rides = {}
    # =============================================
    # CLEAR METHODS
    # =============================================

    def clear_rides(self):

        with self.lock:

            self.active_rides.clear()

    def clear_groups(self):

        with self.lock:

            self.active_groups.clear()

    def clear_clusters(self):

        with self.lock:

            self.active_clusters.clear()

    def clear_all(self):

        with self.lock:

            self.active_rides.clear()

            self.active_groups.clear()

            self.active_clusters.clear()


# =========================================================
# GLOBAL STATE INSTANCE
# =========================================================

state = SystemState()