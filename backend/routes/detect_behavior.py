from flask import Blueprint, request, jsonify

from ai_models.ride_risk_prediction.detect_anomaly import (
    detect_anomaly
)

# =========================================================
# BLUEPRINT
# =========================================================

detect_behavior_bp = Blueprint(
    "detect_behavior",
    __name__
)

# =========================================================
# DETECT BEHAVIOR ROUTE
# =========================================================

@detect_behavior_bp.route(
    "/detect_behavior",
    methods=["POST"]
)

def detect_behavior():

    try:

        # ============================================
        # GET JSON DATA
        # ============================================

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message": "No JSON data received"

            }), 400

        # ============================================
        # RUN AI DETECTION
        # ============================================

        result = detect_anomaly(data)

        # ============================================
        # HANDLE MODEL ERRORS
        # ============================================

        if result.get("status") == "ERROR":

            return jsonify({

                "success": False,

                "error": result

            }), 400

        # ============================================
        # SUCCESS RESPONSE
        # ============================================

        return jsonify({

            "success": True,

            "behavior_analysis": result

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500