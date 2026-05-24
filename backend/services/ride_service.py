"""
Ride optimization service — thin wrapper around optimization_engine.

Reuses ai_models.ride_optimization without modification.
"""

from typing import Any, Dict

from ai_models.ride_optimization.optimization_engine import (
    optimization_engine,
)
from ai_models.ride_optimization.state_manager import state


class RideService:
    """API-facing service for ride lifecycle and optimization."""

    def __init__(self) -> None:
        self._engine = optimization_engine

    def _persist(self) -> None:
        state.save_to_disk()

    def health(self) -> Dict[str, Any]:
        return {
            "success": True,
            "backend": "ACTIVE",
            "optimization_engine": "RUNNING",
            "server": "ONLINE",
        }

    def create_ride(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result = self._engine.add_new_ride(payload)
        self._engine.run_dynamic_optimization()
        self._persist()
        return {
            "success": True,
            "message": "Ride created successfully",
            "data": result,
        }

    def start_ride(self, ride_id: str) -> Dict[str, Any]:
        result = self._engine.start_ride(ride_id)
        self._persist()
        return result

    def complete_ride(self, ride_id: str) -> Dict[str, Any]:
        result = self._engine.complete_ride(ride_id)
        self._persist()
        return result

    def cancel_ride(self, ride_id: str) -> Dict[str, Any]:
        result = self._engine.cancel_ride(ride_id)
        self._persist()
        return result

    def get_active_rides(self) -> Dict[str, Any]:
        rides = self._engine.ride_manager.get_active_rides()
        return {"success": True, "data": rides}

    def get_active_groups(self) -> Dict[str, Any]:
        groups = self._engine.get_active_groups()
        return {"success": True, "data": groups}

    def get_recommendations(self) -> Dict[str, Any]:
        recommendations = self._engine.generate_ai_recommendations()
        return {"success": True, "data": recommendations}

    def get_ride_history(self) -> Dict[str, Any]:
        history = self._engine.get_ride_history()
        return {"success": True, "data": history}


ride_service = RideService()
