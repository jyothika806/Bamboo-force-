# =========================================================
# BAMBOO FORCE AI
# FASTAPI MAIN APPLICATION
# =========================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =========================================================
# IMPORT ROUTERS
# =========================================================

from backend.routes.verify import (
    router as verify_router
)

from backend.routes.ride_optimization import (
    router as ride_router
)

from backend.routes.detect_behavior import (
    router as behavior_router
)

# OPTIONAL
# Uncomment when created

# from backend.routes.risk_prediction import (
#     router as risk_router
# )

# from backend.routes.liveness import (
#     router as liveness_router
# )

# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(

    title="Bamboo Force AI",

    description="AI Powered Secure Ride Ecosystem",

    version="1.0.0"
)

# =========================================================
# ENABLE CORS
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =========================================================
# REGISTER ROUTERS
# =========================================================

app.include_router(

    verify_router,

    prefix="/api/verify",

    tags=["Face Verification"]
)

app.include_router(

    ride_router,

    prefix="/api/ride",

    tags=["Ride Optimization"]
)

app.include_router(

    behavior_router,

    prefix="/api/behavior",

    tags=["Behavior Detection"]
)

# OPTIONAL
# Uncomment later

# app.include_router(
#     risk_router,
#     prefix="/api/risk",
#     tags=["Risk Prediction"]
# )

# app.include_router(
#     liveness_router,
#     prefix="/api/liveness",
#     tags=["Liveness Detection"]
# )

# =========================================================
# HOME ROUTE
# =========================================================

@app.get("/")

def home():

    return {

        "system":
            "Bamboo Force AI",

        "status":
            "RUNNING",

        "backend":
            "FastAPI",

        "version":
            "1.0.0",

        "available_routes": [

            "/api/verify",

            "/api/ride",

            "/api/behavior"
        ]
    }

# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")

def health_check():

    return {

        "success": True,

        "server": "ONLINE",

        "backend": "ACTIVE",

        "ai_engine": "RUNNING"
    }

# =========================================================
# STARTUP EVENT
# =========================================================

@app.on_event("startup")

async def startup_event():

    print("\n=========================================")
    print(" BAMBOO FORCE AI BACKEND STARTED ")
    print("=========================================")
    print(" Server Running : http://127.0.0.1:8000")
    print(" API Docs       : /docs")
    print(" Health Route   : /health")
    print("=========================================\n")