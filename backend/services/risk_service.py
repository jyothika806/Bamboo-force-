"""
Risk prediction service — wraps ride_risk_prediction autoencoder.

Uses centralized ModelRegistry instead of importing detect_anomaly.py
(which loads datasets at module import time).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pandas as pd
import torch

from backend.core.model_registry import get_model_registry


class RiskService:
    """API-facing service for ride risk analysis."""

    FEATURE_COLUMNS: List[str] = [
        "aggression_score",
        "driving_stability",
        "emergency_risk",
        "telemetry_reliability",
        "suspicious_route_score",
        "overall_risk_score",
    ]

    def health(self) -> Dict[str, Any]:
        registry = get_model_registry()
        return {
            "success": True,
            "service": "Risk Prediction Active",
            "models": registry.health(),
        }

    def predict_risk(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict risk from telemetry features or passenger_count fallback.
        """
        if self._has_telemetry_features(data):
            anomaly = self.detect_anomaly(data)
            if anomaly.get("status") == "ERROR":
                return {
                    "success": False,
                    "error": anomaly.get("message", "Risk prediction failed"),
                    "details": anomaly,
                }
            risk_level = self._anomaly_to_level(anomaly)
            return {
                "success": True,
                "risk_level": risk_level,
                "anomaly_result": anomaly,
                "received_data": data,
            }

        passenger_count = int(data.get("passenger_count", 1))
        risk_level = "LOW"
        if passenger_count >= 7:
            risk_level = "HIGH"
        elif passenger_count >= 5:
            risk_level = "MEDIUM"

        return {
            "success": True,
            "risk_level": risk_level,
            "received_data": data,
            "note": "Heuristic fallback — provide telemetry features for ML prediction",
        }

    def detect_anomaly(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            registry = get_model_registry()
            bundle = registry.get_risk_bundle()

            input_df = pd.DataFrame([input_data])
            missing = [
                col
                for col in bundle.feature_columns
                if col not in input_df.columns
            ]
            if missing:
                return {"status": "ERROR", "missing_features": missing}

            input_df = input_df[bundle.feature_columns]
            scaled = bundle.scaler.transform(input_df)
            tensor_input = torch.tensor(
                scaled, dtype=torch.float32
            ).to(bundle.device)

            with torch.no_grad():
                reconstructed = bundle.model(tensor_input)
                loss = bundle.criterion(reconstructed, tensor_input)

            anomaly_score = loss.item()
            status = (
                "SUSPICIOUS"
                if anomaly_score > bundle.threshold
                else "NORMAL"
            )

            return {
                "anomaly_score": round(anomaly_score, 6),
                "threshold": bundle.threshold,
                "status": status,
            }
        except RuntimeError as exc:
            return {"status": "ERROR", "message": str(exc)}
        except Exception as exc:
            return {"status": "ERROR", "message": str(exc)}

    def analyze_driver(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Driver-focused risk analysis using telemetry features."""
        driver_data = {
            "aggression_score": float(
                data.get("aggression_score", 0.5)
            ),
            "driving_stability": float(
                data.get("driving_stability", 0.5)
            ),
            "emergency_risk": float(data.get("emergency_risk", 0.3)),
            "telemetry_reliability": float(
                data.get("telemetry_reliability", 0.7)
            ),
            "suspicious_route_score": float(
                data.get("suspicious_route_score", 0.2)
            ),
            "overall_risk_score": float(
                data.get("overall_risk_score", 0.4)
            ),
        }
        result = self.detect_anomaly(driver_data)
        return {"success": True, "analysis_type": "driver", "data": result}

    def analyze_route(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Route-focused risk analysis using telemetry features."""
        route_data = {
            "aggression_score": float(
                data.get("aggression_score", 0.3)
            ),
            "driving_stability": float(
                data.get("driving_stability", 0.6)
            ),
            "emergency_risk": float(data.get("emergency_risk", 0.4)),
            "telemetry_reliability": float(
                data.get("telemetry_reliability", 0.8)
            ),
            "suspicious_route_score": float(
                data.get("suspicious_route_score", 0.7)
            ),
            "overall_risk_score": float(
                data.get("overall_risk_score", 0.5)
            ),
        }
        result = self.detect_anomaly(route_data)
        return {"success": True, "analysis_type": "route", "data": result}

    def live_risk(self) -> Dict[str, Any]:
        return {
            "success": True,
            "system_status": "ACTIVE",
            "risk_score": 0.21,
        }

    def get_history(self) -> Dict[str, Any]:
        return {"success": True, "history": []}

    def _has_telemetry_features(self, data: Dict[str, Any]) -> bool:
        return any(key in data for key in self.FEATURE_COLUMNS)

    @staticmethod
    def _anomaly_to_level(anomaly: Dict[str, Any]) -> str:
        if anomaly.get("status") == "SUSPICIOUS":
            score = anomaly.get("anomaly_score", 0)
            threshold = anomaly.get("threshold", 0.000537)
            if score > threshold * 3:
                return "HIGH"
            return "MEDIUM"
        return "LOW"


risk_service = RiskService()
