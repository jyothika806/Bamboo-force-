# =========================================================
# BAMBOO FORCE AI
# CENTRALIZED THREAD-SAFE STATE MANAGER
# =========================================================

import json
import logging
from pathlib import Path
from threading import RLock
from typing import Optional

logger = logging.getLogger(__name__)

# Default persistence path (backend/data/ride_state.json)
_DEFAULT_STATE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "backend"
    / "data"
    / "ride_state.json"
)


class SystemState:

    def __init__(self):

        self.lock = RLock()
        self.persist_path = _DEFAULT_STATE_PATH

        self.active_rides = {}
        self.active_groups = {}
        self.active_clusters = {}
        self.active_passengers = {}
        self.ride_history = []
        self.completed_rides = {}

        self.ride_expiry_seconds = 3600

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

    def to_dict(self) -> dict:
        with self.lock:
            return {
                "active_rides": self.active_rides,
                "active_groups": self.active_groups,
                "active_clusters": self.active_clusters,
                "active_passengers": self.active_passengers,
                "completed_rides": self.completed_rides,
                "ride_history": self.ride_history,
                "ride_expiry_seconds": self.ride_expiry_seconds,
            }

    def load_from_dict(self, data: dict) -> None:
        if not data:
            return

        with self.lock:
            self.active_rides = data.get("active_rides", {}) or {}
            self.active_groups = data.get("active_groups", {}) or {}
            self.active_clusters = data.get("active_clusters", {}) or {}
            self.active_passengers = data.get("active_passengers", {}) or {}
            self.completed_rides = data.get("completed_rides", {}) or {}
            self.ride_history = self._normalize_ride_history(
                data.get("ride_history", [])
            )
            self.ride_expiry_seconds = data.get(
                "ride_expiry_seconds", 3600
            )

    @staticmethod
    def _normalize_ride_history(value) -> list:
        """Ensure ride_history is always a list (legacy saves may use dict)."""
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            return list(value.values())
        return []

    def load_from_disk(self, path: Optional[Path] = None) -> bool:
        target = path or self.persist_path

        if not target.exists():
            logger.info("No persisted ride state at %s", target)
            return False

        try:
            with open(target, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            self.load_from_dict(data)
            logger.info("Loaded ride state from %s", target)
            return True
        except Exception as exc:
            logger.warning("Failed to load ride state: %s", exc)
            return False

    def save_to_disk(self, path: Optional[Path] = None) -> bool:
        target = path or self.persist_path

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            snapshot = self.to_dict()

            with open(target, "w", encoding="utf-8") as handle:
                json.dump(snapshot, handle, indent=2)

            logger.debug("Saved ride state to %s", target)
            return True
        except Exception as exc:
            logger.warning("Failed to save ride state: %s", exc)
            return False


state = SystemState()