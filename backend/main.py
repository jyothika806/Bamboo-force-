"""
Bamboo Force AI — FastAPI application entry point.

Phase 1: centralized model loading, service layer, thin routes.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.core.model_registry import get_model_registry
from backend.routes.liveness import router as liveness_router
from backend.routes.ride_optimization import router as ride_router
from backend.routes.risk_prediction import router as risk_router
from backend.routes.verify import router as verify_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load AI models once at startup."""
    settings = get_settings()
    settings.ensure_directories()

    registry = get_model_registry()
    load_status = registry.load_all(settings)
    logger.info("Model load status: %s", load_status)
    logger.info("Model registry health: %s", registry.health())

    app.state.settings = settings
    app.state.model_registry = registry

    yield

    logger.info("Shutting down Bamboo Force AI backend")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        verify_router,
        prefix="/api/verify",
        tags=["Face Verification"],
    )
    app.include_router(
        liveness_router,
        prefix="/api/liveness",
        tags=["Liveness Detection"],
    )
    app.include_router(
        ride_router,
        prefix="/api/ride",
        tags=["Ride Optimization"],
    )
    app.include_router(
        risk_router,
        prefix="/api/risk",
        tags=["Risk Prediction"],
    )

    return app


app = create_app()


@app.get("/")
def home():
    registry = get_model_registry()
    return {
        "message": "Bamboo Force AI Backend Running",
        "version": get_settings().app_version,
        "models": registry.health(),
    }


@app.get("/health")
def health():
    registry = get_model_registry()
    return {
        "status": "ok",
        "models": registry.health(),
    }
