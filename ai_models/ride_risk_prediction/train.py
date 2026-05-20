import os
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
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
# TRAIN / VALIDATION SPLIT
# =========================================================

train_data, val_data = train_test_split(
    scaled_data,
    test_size=0.2,
    random_state=42,
    shuffle=True
)

print(f"[INFO] Training Samples: {len(train_data)}")
print(f"[INFO] Validation Samples: {len(val_data)}")
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

train_tensor = torch.tensor(
    train_data,
    dtype=torch.float32
)

val_tensor = torch.tensor(
    val_data,
    dtype=torch.float32
)

train_dataset = TensorDataset(train_tensor)
val_dataset = TensorDataset(val_tensor)


train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=64,
    shuffle=False
)
# =========================================================
# MODEL SETUP
# =========================================================

input_dim = train_tensor.shape[1]

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

    for batch in train_loader:

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

    avg_loss = total_loss / len(train_loader)

    print(
        f"Epoch [{epoch+1}/{EPOCHS}] "
        f"Loss: {avg_loss:.6f}"
    )
    # =========================================================
    # VALIDATION
    # =========================================================

    model.eval()

    val_loss = 0

    with torch.no_grad():

        for batch in val_loader:

            inputs = batch[0].to(DEVICE)

            outputs = model(inputs)

            loss = criterion(outputs, inputs)

            val_loss += loss.item()

    avg_val_loss = val_loss / len(val_loader)

    print(
        f"Validation Loss: {avg_val_loss:.6f}"
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
# =========================================================
# CALCULATE DYNAMIC THRESHOLD
# =========================================================

model.eval()

all_losses = []

with torch.no_grad():

    for batch in train_loader:

        inputs = batch[0].to(DEVICE)

        outputs = model(inputs)

        loss = criterion(outputs, inputs)

        all_losses.append(loss.item())

mean_loss = np.mean(all_losses)

std_loss = np.std(all_losses)

threshold = mean_loss + 2 * std_loss

print(f"\n[INFO] Mean Loss: {mean_loss:.6f}")
print(f"[INFO] Std Loss: {std_loss:.6f}")
print(f"[INFO] Suggested Threshold: {threshold:.6f}")