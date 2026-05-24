# 🚀 Bamboo Force AI

AI-powered smart mobility, transportation safety, ride optimization, and intelligent driver verification platform.

Bamboo Force AI combines:

* 🚗 AI Ride Optimization
* 🛡️ Driver Verification
* 🎥 Face Liveness Detection
* 📊 Ride Risk Prediction
* 🧠 Smart Mobility Intelligence

into one integrated transportation safety ecosystem.

---

# 🌟 Vision

Bamboo Force AI aims to build a:

* safer
* smarter
* AI-driven
* sustainable

urban mobility platform capable of:

* preventing spoof attacks
* detecting suspicious rides
* optimizing shared transportation
* improving ride security
* reducing traffic congestion
* enabling intelligent transportation systems

---

# 🧠 Core AI Modules

## 🎥 Video Liveness Detection

AI-powered anti-spoof face verification system using:

* MobileNetV2
* LSTM temporal modeling
* real-time webcam analysis

Detects:

* fake faces
* replay attacks
* printed photos
* spoofed authentication attempts

📂 Module:

```text
ai_models/video_model/
```

---

## 🛡️ Face Verification System

Secure driver identity verification system using:

* face embeddings
* KYC verification
* live face scanning
* facial comparison

Supports:

* driver registration
* ride authentication
* passenger-driver verification

📂 Module:

```text
ai_models/face_verification/
```

---

## 🚖 Ride Optimization Engine

AI-powered urban ride-sharing optimization system.

Features:

* dynamic ride matching
* shared ride clustering
* route similarity analysis
* occupancy optimization
* congestion reduction
* smart vehicle allocation

📂 Module:

```text
ai_models/ride_optimization/
```

---

## 📊 Ride Risk Prediction System

Deep learning anomaly detection system for ride safety intelligence.

Analyzes:

* driving aggression
* emergency risk
* suspicious routes
* telemetry instability
* unsafe ride behavior

Uses:

* feature engineering
* autoencoders
* anomaly detection
* reconstruction loss analysis

📂 Module:

```text
ai_models/ride_risk_prediction/
```

---

# 🏗️ System Architecture

```text
                    Bamboo Force AI
                            │
    ┌───────────────────────┼───────────────────────┐
    │                       │                       │
    ▼                       ▼                       ▼

Face Verification     Ride Optimization     Ride Risk Prediction
        │                     │                       │
        ▼                     ▼                       ▼

Video Liveness      Shared Ride AI        Safety Intelligence
        │                     │                       │
        └──────────────┬──────┴──────────────┬────────┘
                       ▼                     ▼

               Smart Mobility Intelligence
                       │
                       ▼

              Secure Transportation System
```

---

# ⚙️ Technologies Used

## AI / ML

* PyTorch
* Deep Learning
* Autoencoders
* LSTM Networks
* MobileNetV2

## Computer Vision

* OpenCV
* face_recognition

## Data Science

* NumPy
* Pandas
* Scikit-learn
* Joblib

## Backend / APIs

* Flask
* Python

## Smart Mobility

* Route Similarity Algorithms
* Ride Clustering
* Traffic Optimization
* Shared Ride Intelligence

---

# 📂 Project Structure

```text
Bamboo-force-/
│
├── ai_models/
│   │
│   ├── face_verification/
│   │
│   ├── video_model/
│   │
│   ├── ride_optimization/
│   │
│   └── ride_risk_prediction/
│
├── backend/
│
├── frontend/
│
├── tests/
│
├── utils/
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Getting Started

## 1️⃣ Clone Repository

```bash
git clone https://github.com/jyothika806/Bamboo-force-.git
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Run Individual Modules

## 🎥 Video Liveness Detection

```bash
python -m ai_models.video_model.main
```

---

## 🛡️ Driver Verification

```bash
python -m ai_models.face_verification.register_driver
```

```bash
python -m ai_models.face_verification.verify_assigned_driver
```

---

## 🚖 Ride Optimization

```bash
python -m ai_models.ride_optimization.optimization_engine
```

---

## 📊 Ride Risk Prediction

### Generate Dataset

```bash
python -m ai_models.ride_risk_prediction.generate_data
```

### Feature Engineering

```bash
python -m ai_models.ride_risk_prediction.feature_engineering
```

### Train Model

```bash
python -m ai_models.ride_risk_prediction.train
```

### Detect Suspicious Ride

```bash
python -m ai_models.ride_risk_prediction.detect_anomaly
```

---

# � FastAPI Backend Deployment

## Start Backend Server

```bash
# Development mode
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Production mode
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Environment Configuration

Create a `.env` file in the project root:

```env
# Backend Configuration
APP_NAME=Bamboo Force AI
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=production

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Configuration
CORS_ORIGINS=["*"]

# AI Model Configuration
DEVICE=cpu
VIDEO_LIVENESS_MODEL_PATH=video_liveness_model.pth
RISK_AUTOENCODER_PATH=ai_models/ride_risk_prediction/checkpoints/autoencoder.pth
RISK_SCALER_PATH=ai_models/ride_risk_prediction/checkpoints/scaler.save
RISK_ANOMALY_THRESHOLD=0.000537

# Camera Configuration
CAMERA_INDEX=0
CAMERA_MAX_KYC_FRAMES=110

# Liveness Detection Settings
LIVENESS_THRESHOLD=0.3
ALLOW_LOW_CONFIDENCE_LIVENESS=false
```

## Frontend Configuration

Update `frontend/config.js` for production:

```javascript
window.APP_CONFIG = {
    baseUrl: "https://your-domain.com",  // Change to production URL
    requestTimeoutMs: 30000,
};
```

---

# 🌐 Production Deployment

## Docker Deployment (Recommended)

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t bamboo-force-ai .

# Run container
docker run -p 8000:8000 bamboo-force-ai
```

## Cloud Deployment

### Requirements

- Python 3.10+
- 4GB RAM minimum
- GPU optional (for faster inference)
- Port 8000 open

### Deployment Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start Backend**
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

4. **Serve Frontend**
   - Use nginx, Apache, or any static file server
   - Point to the `frontend/` directory
   - Update `frontend/config.js` with production URL

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# API health
curl http://localhost:8000/api/ride/health
```

---

# �🔐 Security & Safety Features

* AI-based anti-spoof detection
* Driver identity verification
* Ride anomaly detection
* Emergency risk analysis
* Shared ride optimization
* Smart transportation intelligence
* Traffic reduction strategies

---

# 🌍 Smart Mobility Applications

* Ride-sharing platforms
* Smart transportation systems
* Driver authentication systems
* Urban traffic optimization
* Shared commute platforms
* AI-powered transportation safety
* Smart city mobility systems

---

# 📥 Datasets

Large datasets and trained checkpoints may not be uploaded to GitHub because of file size limitations.

Datasets include:

* face verification datasets
* spoof detection videos
* synthetic ride telemetry datasets
* engineered AI safety datasets

---

# 🔮 Future Improvements

## AI Improvements

* Transformer-based temporal modeling
* Reinforcement learning optimization
* Advanced anomaly detection
* Sequential telemetry modeling

## Smart Mobility

* Live GPS integration
* Google Maps API integration
* Real-time traffic prediction
* AI ETA prediction
* Dynamic surge optimization

## Security

* Multi-face verification
* Cloud authentication APIs
* Real-time fraud detection
* Federated edge AI systems

## Deployment

* Docker deployment
* Cloud APIs
* Mobile application integration
* Real-time AI inference servers

---

# 🏆 Project Highlights

✅ Multi-module AI transportation platform
✅ Deep learning + computer vision integration
✅ Smart mobility optimization engine
✅ Real-time ride anomaly detection
✅ AI-powered driver verification
✅ Transportation security intelligence
✅ Hackathon-ready architecture

---

# 👩‍💻 Author

Kaveti Jyothika

AI | Computer Vision | Smart Mobility | Transportation Intelligence

---

# 🚀 Bamboo Force AI

### Secure. Smart. Sustainable.
