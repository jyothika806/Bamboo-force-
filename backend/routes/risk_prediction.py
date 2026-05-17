from fastapi import APIRouter

router = APIRouter()

# =========================================================
# HEALTH
# =========================================================

@router.get("/health")
async def risk_health():

    return {

        "success": True,

        "service": "Risk Prediction Active"
    }

# =========================================================
# PREDICT RISK
# =========================================================

@router.post("/predict")
async def predict_risk(

    data: dict
):

    passenger_count = data.get(
        "passenger_count",
        1
    )

    risk_level = "LOW"

    if passenger_count >= 5:

        risk_level = "MEDIUM"

    if passenger_count >= 7:

        risk_level = "HIGH"

    return {

        "success": True,

        "risk_level": risk_level,

        "received_data": data
    }

# =========================================================
# LIVE RISK
# =========================================================

@router.get("/live")
async def live_risk():

    return {

        "success": True,

        "system_status": "ACTIVE",

        "risk_score": 0.21
    }

# =========================================================
# RISK HISTORY
# =========================================================

@router.get("/history")
async def risk_history():

    return {

        "success": True,

        "history": []
    }