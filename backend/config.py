# =========================================================
# BAMBOO FORCE AI - CENTRALIZED CONFIGURATION
# =========================================================
# WHY THIS EXISTS:
# - Eliminates scattered config across files
# - Makes deployment different for dev/staging/prod trivial
# - Allows environment-based overrides (12-factor app)
# - Single source of truth for all settings
# =========================================================

import os
from pathlib import Path
from typing import Dict, List

# =========================================================
# BASE PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# =========================================================
# ENVIRONMENT
# =========================================================

ENV = os.getenv("ENVIRONMENT", "development")
DEBUG = ENV in ["development", "staging"]

# =========================================================
# APPLICATION CONFIG
# =========================================================

class AppConfig:
    """Central app configuration"""
    
    # API Settings
    API_TITLE = "Bamboo Force AI"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "AI-powered smart mobility platform"
    
    # Server
    HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    PORT = int(os.getenv("SERVER_PORT", "8000"))
    WORKERS = int(os.getenv("WORKERS", "4"))
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = LOGS_DIR / f"bamboo_force_{ENV}.log"


# =========================================================
# AI MODEL CONFIGURATION
# =========================================================

class AIModelConfig:
    """Configuration for all AI models"""
    
    # =====================================================
    # VIDEO LIVENESS MODEL
    # =====================================================
    
    class VideoLiveness:
        """MobileNetV2 + LSTM Liveness Detection"""
        
        # Model paths
        MODEL_PATH = MODELS_DIR / "video_liveness_model.pth"
        
        # Hardware
        DEVICE = os.getenv("TORCH_DEVICE", "cpu")
        USE_GPU = DEVICE.startswith("cuda")
        
        # Input specs
        FRAME_SIZE = (112, 112)
        SEQUENCE_LENGTH = 10
        FPS = 30
        
        # Inference
        CONFIDENCE_THRESHOLD = 0.85
        BATCH_SIZE = 1
        
        # Performance
        MAX_INFERENCE_TIME_MS = 100
        CACHE_ENABLED = True
        CACHE_TTL_SECONDS = 300
    
    # =====================================================
    # FACE VERIFICATION MODEL
    # =====================================================
    
    class FaceVerification:
        """Face Recognition + Embedding Matching"""
        
        # Embedding settings
        EMBEDDING_DIM = 128
        EMBEDDING_STORAGE_DIR = DATA_DIR / "embeddings"
        
        # Thresholds
        FACE_DISTANCE_THRESHOLD = 0.6
        MIN_FACES_PER_IMAGE = 1
        
        # Performance
        BATCH_SIZE = 4
        MAX_PROCESSING_TIME_MS = 200
    
    # =====================================================
    # RIDE OPTIMIZATION MODEL
    # =====================================================
    
    class RideOptimization:
        """AI Ride Matching & Route Optimization"""
        
        # Geospatial
        SIMILARITY_THRESHOLD = 0.75
        MAX_MATCHING_DISTANCE_KM = 5.0
        
        # Vehicle configuration
        VEHICLE_CAPACITY = {
            "BIKE": 1,
            "AUTO": 3,
            "CAB": 4,
            "VAN": 7
        }
        
        VEHICLE_TRAFFIC_IMPACT = {
            "BIKE": 0.90,
            "AUTO": 0.60,
            "CAB": 0.50,
            "VAN": 0.30
        }
        
        # Optimization
        OPTIMIZATION_CYCLES = 100
        TIMEOUT_SECONDS = 30


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

class DatabaseConfig:
    """Database connection settings"""
    
    # PostgreSQL (Production)
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    
    if DB_TYPE == "postgresql":
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = int(os.getenv("DB_PORT", "5432"))
        DB_NAME = os.getenv("DB_NAME", "bamboo_force")
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DATABASE_URL = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@"
            f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        # SQLite (Development)
        DATABASE_URL = f"sqlite:///{DATA_DIR}/bamboo_force.db"
    
    # Connection pool
    POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
    MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
    POOL_RECYCLE = 3600


# =========================================================
# CACHE CONFIGURATION (REDIS)
# =========================================================

class CacheConfig:
    """Redis cache settings"""
    
    ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    
    if ENABLED:
        REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
        REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
        REDIS_DB = int(os.getenv("REDIS_DB", "0"))
        REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
        
        REDIS_URL = (
            f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
            if REDIS_PASSWORD
            else f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
        )
    
    # TTLs
    DEFAULT_TTL = 3600
    MODEL_CACHE_TTL = 86400
    RIDE_CACHE_TTL = 300


# =========================================================
# API RATE LIMITING
# =========================================================

class RateLimitConfig:
    """Rate limiting settings"""
    
    ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    REQUESTS_PER_MINUTE = int(os.getenv("REQUESTS_PER_MINUTE", "100"))
    REQUESTS_PER_HOUR = int(os.getenv("REQUESTS_PER_HOUR", "10000"))


# =========================================================
# PATHS & DIRECTORIES
# =========================================================

class PathConfig:
    """Data storage paths"""
    
    # Face verification
    FACE_EMBEDDINGS_DIR = DATA_DIR / "embeddings"
    FACE_DATA_DIR = DATA_DIR / "face_data"
    ID_IMAGES_DIR = DATA_DIR / "id_images"
    LIVE_FACES_DIR = DATA_DIR / "live_faces"
    
    # AI Models
    MODEL_CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
    
    # Logs
    LOG_DIR = LOGS_DIR
    
    # Create all
    for path in [
        FACE_EMBEDDINGS_DIR, FACE_DATA_DIR, ID_IMAGES_DIR,
        LIVE_FACES_DIR, MODEL_CHECKPOINTS_DIR, LOG_DIR
    ]:
        path.mkdir(parents=True, exist_ok=True)


# =========================================================
# FEATURE FLAGS
# =========================================================

class FeatureFlags:
    """Feature toggles for gradual rollout"""
    
    # GPU Inference
    ENABLE_GPU_INFERENCE = os.getenv("ENABLE_GPU_INFERENCE", "false").lower() == "true"
    
    # Async Processing
    ENABLE_ASYNC_VERIFICATION = os.getenv("ENABLE_ASYNC_VERIFICATION", "true").lower() == "true"
    
    # WebSocket Support
    ENABLE_WEBSOCKET = os.getenv("ENABLE_WEBSOCKET", "true").lower() == "true"
    
    # Advanced Optimization
    ENABLE_ADVANCED_MATCHING = os.getenv("ENABLE_ADVANCED_MATCHING", "true").lower() == "true"
    
    # Monitoring
    ENABLE_PROMETHEUS_METRICS = os.getenv("ENABLE_PROMETHEUS_METRICS", "true").lower() == "true"


# =========================================================
# EXPORT CONFIG INSTANCE
# =========================================================

config = AppConfig()
ai_config = AIModelConfig()
db_config = DatabaseConfig()
cache_config = CacheConfig()
path_config = PathConfig()
feature_flags = FeatureFlags()
