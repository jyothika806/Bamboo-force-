import os
import joblib
import pandas as pd
import torch
import torch.nn as nn

from ai_models.ride_risk_prediction.autoencoder_model import (
    RideRiskAutoEncoder
)

# =========================================================
# DEVICE
# =========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"\n[INFO] Using Device: {DEVICE}")

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHECKPOINT_DIR = os.path.join(
    BASE_DIR,
    "checkpoints"
)

MODEL_PATH = os.path.join(
    CHECKPOINT_DIR,
    "autoencoder.pth"
)

SCALER_PATH = os.path.join(
    CHECKPOINT_DIR,
    "scaler.save"
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "engineered_dataset.csv"
)

# =========================================================
# LOAD DATASET
# =========================================================

print("\n[INFO] Loading engineered dataset...")

df = pd.read_csv(DATASET_PATH)

if "safe" in df.columns:
    df = df.drop(columns=["safe"])
FEATURE_COLUMNS = [

    "aggression_score",
    "driving_stability",
    "emergency_risk",
    "telemetry_reliability",
    "suspicious_route_score",
    "overall_risk_score"
]

input_dim = len(FEATURE_COLUMNS)

print(f"[INFO] Total Features: {input_dim}")

# =========================================================
# LOAD MODEL
# =========================================================

model = RideRiskAutoEncoder(
    input_dim=input_dim
).to(DEVICE)

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)

model.eval()

print("[INFO] Autoencoder loaded")

# =========================================================
# LOAD SCALER
# =========================================================

scaler = joblib.load(
    SCALER_PATH
)

print("[INFO] Scaler loaded")

# =========================================================
# LOSS FUNCTION
# =========================================================

criterion = nn.MSELoss()

# =========================================================
# DETECT ANOMALY
# =========================================================

def detect_anomaly(input_data):

    try:

        # ============================================
        # CREATE DATAFRAME
        # ============================================

        input_df = pd.DataFrame(
            [input_data]
        )

        # ============================================
        # VALIDATE FEATURES
        # ============================================

        missing_features = [

            feature

            for feature in FEATURE_COLUMNS

            if feature not in input_df.columns
        ]

        if len(missing_features) > 0:

            return {

                "status": "ERROR",

                "missing_features": missing_features
            }

        # ============================================
        # COLUMN ALIGNMENT
        # ============================================

        input_df = input_df[
            FEATURE_COLUMNS
        ]

        # ============================================
        # NORMALIZATION
        # ============================================

        scaled_input = scaler.transform(
            input_df
        )

        # ============================================
        # TENSOR CONVERSION
        # ============================================

        tensor_input = torch.tensor(
            scaled_input,
            dtype=torch.float32
        ).to(DEVICE)

        # ============================================
        # INFERENCE
        # ============================================

        with torch.no_grad():

            reconstructed = model(
                tensor_input
            )

            loss = criterion(
                reconstructed,
                tensor_input
            )

        anomaly_score = loss.item()

        # ============================================
        # THRESHOLD
        # ============================================

        THRESHOLD = 0.000750

        if anomaly_score > THRESHOLD:

            status = "SUSPICIOUS"

        else:

            status = "NORMAL"

        # ============================================
        # RESULT
        # ============================================

        result = {

            "anomaly_score": round(
                anomaly_score,
                6
            ),

            "threshold": THRESHOLD,

            "status": status
        }

        return result

    except Exception as e:

        return {

            "status": "ERROR",

            "message": str(e)
        }

# =========================================================
# TEST SAMPLE
# =========================================================

if __name__ == "__main__":

    sample_ride = {

        "aggression_score": 0.85,
        "driving_stability": 0.20,
        "emergency_risk": 0.90,
        "telemetry_reliability": 0.30,
        "suspicious_route_score": 0.80,
        "overall_risk_score": 0.88
    }

    result = detect_anomaly(
        sample_ride
    )

    print("\n[RESULT] Detection Result:\n")

    print(result)