# 🚀 AI Ride Risk Prediction System

AI-powered ride safety intelligence and anomaly detection engine for Bamboo Force AI.

This module analyzes ride telemetry, driver behavior, emergency indicators, and route patterns to detect suspicious or unsafe rides using deep learning.

---

# 🌟 Features

- AI-Based Ride Risk Prediction
- Deep Learning Anomaly Detection
- Driver Behavior Analysis
- Telemetry Risk Monitoring
- Emergency Risk Detection
- Route Risk Intelligence
- Synthetic Ride Safety Dataset
- Autoencoder-Based Risk Modeling
- Real-Time Suspicious Ride Detection

---

# 🧠 AI Architecture

The system uses:

- Feature Engineering
- MinMax Normalization
- PyTorch Autoencoder
- Reconstruction Loss Analysis
- Anomaly Detection

Unsafe or suspicious rides generate higher reconstruction errors and are classified as anomalies.

---

# 🏗️ Project Structure

```text
ai_models/
└── ride_risk_prediction/
    ├── checkpoints/
    │   ├── autoencoder.pth
    │   └── scaler.save
    │
    ├── datasets/
    │   ├── dataset.csv
    │   └── engineered_dataset.csv
    │
    ├── autoencoder_model.py
    ├── generate_data.py
    ├── feature_engineering.py
    ├── train.py
    ├── detect_anomaly.py
    └── README.md

```
# ⚙️ Technologies Used

- Python
- PyTorch
- Pandas
- NumPy
- Scikit-learn
- Joblib
---

# 📊 Dataset Information

The dataset is synthetically generated to simulate:

- risky driving behavior
- emergency situations
- unsafe route conditions
- telemetry instability
- suspicious ride activity
---

# 🧠 Engineered Features

## Driving Aggression

Calculated using:

- speed
- sudden braking
- sharp turns
## Driving Stability

Measures ride smoothness and control.

## Emergency Risk

Uses:

- panic button activity
- crash detection
## Telemetry Reliability

Analyzes:

- GPS signal loss
- telemetry consistency
## Suspicious Route Score

Detects:

- unexpected route changes
- unsafe travel timing
## Overall Risk Score

Combined AI risk metric.

# 🔄 AI Workflow

```
    Raw Ride Telemetry
            ↓
    Feature Engineering
            ↓
    Normalization
            ↓
    Autoencoder Training
            ↓
    Reconstruction Loss
            ↓
    Anomaly Detection
            ↓
    NORMAL / SUSPICIOUS

```
---

# 🚀 Run the Project

## 1️⃣ Generate Dataset
- python -m ai_models.ride_risk_prediction.generate_data

## 2️⃣ Run Feature Engineering
- python -m ai_models.ride_risk_prediction.feature_engineering

## 3️⃣ Train Autoencoder
- python -m ai_models.ride_risk_prediction.train

## 4️⃣ Detect Suspicious Ride
- python -m ai_models.ride_risk_prediction.detect_anomaly

---

# 📥 Dataset Access

Dataset files may not be uploaded to GitHub due to file size limitations.

## Download Dataset

- 👉 YOUR_ONEDRIVE_LINK_HERE

---

# 🧪 Example Detection Output
```
    {
        "anomaly_score": 0.082341,
        "threshold": 0.05,
        "status": "SUSPICIOUS"
    }
```
---

# 🌍 Future Improvements

- Real-time telemetry streaming
- GPS route intelligence
- Driver behavior forecasting
- Live anomaly alerts
- Deep sequential models (LSTM/Transformers)
- Federated edge learning
- Smart city safety integration
- Real-time emergency response system

---

# ⚠️ Important Note

This project currently uses a synthetic dataset created for educational, research, and hackathon purposes.

# 👩‍💻 Author

Kaveti Jyothika

AI | Smart Mobility | Transportation Intelligence

# 🚀 Bamboo Force AI

Secure. Smart. Sustainable.


---

## 🚀 BIGGEST ML IMPROVEMENT YOU SHOULD DO LATER

This one is IMPORTANT:

## ✅ TRAIN ONLY ON SAFE RIDES

Currently:
you train autoencoder on everything.

But anomaly detection should learn:

```text
NORMAL behavior only

Then:
anything abnormal becomes anomaly.

That would make your project MUCH more technically correct.