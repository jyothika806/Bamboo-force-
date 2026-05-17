from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.routes.verify import (
    router as verify_router
)

from backend.routes.liveness import (
    router as liveness_router
)

from backend.routes.ride_optimization import (
    router as ride_router
)
from backend.routes.risk_prediction import (
    router as risk_router
)

# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(

    title="Bamboo Force AI",

    version="1.0.0"
)

# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =====================================================
# ROUTES
# =====================================================

app.include_router(

    verify_router,

    prefix="/api/verify",

    tags=["Face Verification"]
)

app.include_router(

    liveness_router,

    prefix="/api/liveness",

    tags=["Liveness Detection"]
)

app.include_router(

    ride_router,

    prefix="/api/ride",

    tags=["Ride Optimization"]
)
app.include_router(

    risk_router,

    prefix="/api/risk",

    tags=["Risk Prediction"]
)
# =====================================================
# ROOT
# =====================================================

@app.get("/")

def home():

    return {

        "message":
            "Bamboo Force AI Backend Running"
    }