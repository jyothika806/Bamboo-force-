import os
import joblib
import pandas as pd
import torch
import torch.nn as nn

from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler

from ai_models.ride_risk_prediction.autoencoder_model import (
    RideRiskAutoEncoder
)
# =========================================================
# DEVICE SETUP
# =========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"\n[INFO] Using Device: {DEVICE}")

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "engineered_dataset.csv"
)

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

os.makedirs(
    CHECKPOINT_DIR,
    exist_ok=True
)

# =========================================================
# LOAD DATASET
# =========================================================

print("\n[INFO] Loading engineered dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"[INFO] Dataset Shape: {df.shape}")

# =========================================================
# REMOVE LABEL COLUMN
# =========================================================

if "safe" in df.columns:
    df = df.drop(columns=["safe"])

# =========================================================
# USE ONLY ENGINEERED FEATURES
# =========================================================

selected_features = [

    "aggression_score",
    "driving_stability",
    "emergency_risk",
    "telemetry_reliability",
    "suspicious_route_score",
    "overall_risk_score"
]

df = df[selected_features]

print(f"\n[INFO] Selected Features:")

for feature in selected_features:
    print(f" - {feature}")

# =========================================================
# REMOVE MISSING VALUES
# =========================================================

df = df.dropna()

# =========================================================
# NORMALIZATION
# =========================================================

print("\n[INFO] Normalizing features...")

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(df)

# =========================================================
# SAVE SCALER
# =========================================================

joblib.dump(
    scaler,
    SCALER_PATH
)

print("[INFO] Scaler saved")

# =========================================================
# TENSOR CONVERSION
# =========================================================

tensor_data = torch.tensor(
    scaled_data,
    dtype=torch.float32
)

dataset = TensorDataset(
    tensor_data
)

dataloader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True
)

# =========================================================
# MODEL SETUP
# =========================================================

input_dim = tensor_data.shape[1]

model = RideRiskAutoEncoder(
    input_dim=input_dim
).to(DEVICE)

criterion = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    weight_decay=1e-5
)

# =========================================================
# TRAINING CONFIG
# =========================================================

EPOCHS = 50

best_loss = float("inf")

print("\n[INFO] Training started...\n")

# =========================================================
# TRAINING LOOP
# =========================================================

for epoch in range(EPOCHS):

    model.train()

    total_loss = 0

    for batch in dataloader:

        inputs = batch[0].to(DEVICE)

        # ============================================
        # FORWARD PASS
        # ============================================

        outputs = model(inputs)

        loss = criterion(
            outputs,
            inputs
        )

        # ============================================
        # BACKPROPAGATION
        # ============================================

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)

    print(
        f"Epoch [{epoch+1}/{EPOCHS}] "
        f"Loss: {avg_loss:.6f}"
    )

    # ============================================
    # SAVE BEST MODEL
    # ============================================

    if avg_loss < best_loss:

        best_loss = avg_loss

        torch.save(
            model.state_dict(),
            MODEL_PATH
        )

        print(
            f"[INFO] Best model updated "
            f"(Loss: {best_loss:.6f})"
        )

# =========================================================
# TRAINING COMPLETE
# =========================================================

print("\n[SUCCESS] Training completed!")

print(f"\n[INFO] Model saved to:\n{MODEL_PATH}")

print(
    f"\n[INFO] Best Reconstruction Loss: "
    f"{best_loss:.6f}"
)