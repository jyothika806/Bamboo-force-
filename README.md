# 🚀 Bamboo Force AI

**AI-powered smart mobility and transportation safety platform that analyzes real-time factors like time, location risk, and driver rating to help users make safer travel decisions.**

Bamboo Force AI integrates multiple deep learning modules into a unified transportation safety ecosystem combining:

* 🎥 **Video Liveness Detection** — AI-powered anti-spoof face verification
* 🛡️ **Face Verification System** — Secure driver identity authentication  
* 🚖 **Ride Optimization Engine** — Smart ride-sharing and occupancy optimization
* 📊 **Ride Risk Prediction** — Deep learning anomaly detection for unsafe rides

---

## 🌟 Vision

Bamboo Force AI enables:

* **Safer** transportation through AI-driven risk detection
* **Smarter** ride-sharing via intelligent optimization
* **Sustainable** urban mobility through congestion reduction
* **Secure** driver verification and identity authentication

---

## 🏗️ System Architecture

```
                      Bamboo Force AI Platform
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
    
  Face Verification    Ride Optimization    Ride Risk Prediction
      System              Engine              System
         │                   │                   │
         ├───────────────┬───┴─────────────┬───┤
         │               │                 │   │
         ▼               ▼                 ▼   ▼
    
         FastAPI Backend (Service Layer)
         │
         ├─ /api/verify          (Face Verification APIs)
         ├─ /api/liveness        (Video Liveness Detection APIs)
         ├─ /api/ride            (Ride Optimization APIs)
         └─ /api/risk            (Risk Prediction APIs)
         │
         ▼
    Frontend Dashboard (HTML/CSS/JS)
    
    ┌──────────────────────────────────┐
    │  Bamboo Force AI Dashboard       │
    │                                  │
    │  • Safety Verification           │
    │  • Risk Intelligence             │
    │  • Ride Optimization             │
    │  • Analytics                     │
    └──────────────────────────────────┘
```

---

## 🧠 Core AI Modules

### 🎥 Video Liveness Detection
**Real-time face anti-spoof system using MobileNetV2 + LSTM**

* Detects fake faces, replay attacks, printed photos
* Analyzes video frames with temporal LSTM modeling
* PyTorch-based deep learning inference
* Real-time webcam integration
* Output: `REAL` or `SPOOF` classification

**Module:** `ai_models/video_model/`

---

### 🛡️ Face Verification System  
**Secure driver identity verification and KYC authentication**

* Captures driver ID documents and live face scans
* Generates normalized 128D face embeddings
* Stores driver embeddings for future verification
* Euclidean distance-based facial comparison
* Validates document quality and face presence
* Extracts faces from ID cards automatically

**Module:** `ai_models/face_verification/`

---

### 🚖 Ride Optimization Engine
**AI-powered urban mobility and ride-sharing optimization**

* Dynamic real-time ride matching
* Smart ride clustering for shared rides
* Route similarity analysis (Haversine + cosine similarity)
* Occupancy and fuel efficiency optimization
* Traffic reduction scoring
* Passenger grouping and vehicle allocation
* Ride lifecycle management
* Thread-safe centralized state management

**Module:** `ai_models/ride_optimization/`

---

### 📊 Ride Risk Prediction System
**Deep learning anomaly detection for ride safety intelligence**

* Analyzes driving behavior and emergency risk indicators
* Detects suspicious routes and unsafe patterns
* Monitors telemetry stability and anomalies
* PyTorch autoencoder-based risk modeling
* Reconstruction loss analysis for anomaly scoring
* Synthetic dataset for training and validation
* Real-time suspicious ride flagging

**Module:** `ai_models/ride_risk_prediction/`

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend API** | FastAPI, Python 3.10+ |
| **Frontend** | HTML5, CSS3, JavaScript |
| **AI/ML** | PyTorch, Scikit-learn, NumPy, Pandas |
| **Computer Vision** | OpenCV, face_recognition, MobileNetV2 |
| **Optimization** | Route algorithms, Geospatial analysis, Clustering |
| **Data Processing** | Joblib, Pandas, NumPy, MinMax scaling |

---

## 📂 Project Structure

```
Bamboo-force-/
│
├── ai_models/
│   ├── video_model/                  (Video liveness detection)
│   │   ├── main.py
│   │   ├── model.py
│   │   ├── train.py
│   │   ├── test_video.py
│   │   ├── dataset.py
│   │   ├── video_liveness_model.pth
│   │   └── README.md
│   │
│   ├── face_verification/            (Driver face authentication)
│   │   ├── register_driver.py
│   │   ├── verify_assigned_driver.py
│   │   ├── camera.py
│   │   ├── encode.py
│   │   ├── compare.py
│   │   ├── check_document.py
│   │   ├── capture_document.py
│   │   ├── extract_id_face.py
│   │   └── README.md
│   │
│   ├── ride_optimization/            (Ride-sharing optimization)
│   │   ├── optimization_engine.py
│   │   ├── route_similarity.py
│   │   ├── match_rides.py
│   │   ├── clustering.py
│   │   ├── recommendation.py
│   │   ├── ride_manager.py
│   │   ├── state_manager.py
│   │   └── README.md
│   │
│   └── ride_risk_prediction/         (Anomaly detection)
│       ├── generate_data.py
│       ├── feature_engineering.py
│       ├── train.py
│       ├── detect_anomaly.py
│       ├── autoencoder_model.py
│       ├── datasets/
│       ├── checkpoints/
│       └── README.md
│
├── backend/                           (FastAPI application)
│   ├── main.py                       (App entry point)
│   ├── app.py
│   ├── config.py                     (Configuration & settings)
│   ├── core/
│   │   ├── model_registry.py         (Model loading & lifecycle)
│   │   └── ...
│   ├── routes/                       (API endpoints)
│   │   ├── liveness.py               (/api/liveness endpoints)
│   │   ├── verify.py                 (/api/verify endpoints)
│   │   ├── ride_optimization.py      (/api/ride endpoints)
│   │   ├── risk_prediction.py        (/api/risk endpoints)
│   │   └── auth.py                   (Empty - future auth)
│   ├── services/                     (Business logic)
│   │   ├── liveness_service.py
│   │   ├── face_verification_service.py
│   │   ├── face_service.py
│   │   ├── ride_service.py
│   │   └── risk_service.py
│   └── utils/                        (Helper utilities)
│
├── frontend/                          (Web dashboard)
│   ├── index.html                    (Main dashboard page)
│   ├── script.js                     (Dashboard interactions)
│   ├── style.css                     (Styling)
│   ├── config.js                     (Frontend configuration)
│   ├── components/                   (Component directory)
│   ├── pages/                        (Additional pages)
│   ├── js/                           (Additional JS modules)
│   └── css/                          (Additional stylesheets)
│
├── tests/                             (Test directory)
│   └── (Currently empty)
│
├── utils/                             (Utility scripts)
│   └── (Shared utilities)
│
├── requirements.txt                   (Python dependencies)
├── .env.example                       (Environment template)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/jyothika806/Bamboo-force-.git
cd Bamboo-force-
```

### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment

Create `.env` file in project root:

```env
# Application Settings
APP_NAME=Bamboo Force AI
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=production

# Server Configuration
HOST=127.0.0.1
PORT=8000
CORS_ORIGINS=["http://localhost:3000","*"]

# AI Model Paths
DEVICE=cpu
VIDEO_LIVENESS_MODEL_PATH=ai_models/video_model/video_liveness_model.pth
RISK_AUTOENCODER_PATH=ai_models/ride_risk_prediction/checkpoints/autoencoder.pth
RISK_SCALER_PATH=ai_models/ride_risk_prediction/checkpoints/scaler.save

# Thresholds
RISK_ANOMALY_THRESHOLD=0.000537
LIVENESS_THRESHOLD=0.3

# Camera Settings
CAMERA_INDEX=0
CAMERA_MAX_KYC_FRAMES=110
ALLOW_LOW_CONFIDENCE_LIVENESS=false

# File Paths
RIDE_STATE_PATH=./ride_state/
TEMP_DIR=./temp/
EMBEDDINGS_DIR=./embeddings/
```

---

## 🏃 Running the Application

### Start FastAPI Backend

**Development mode:**
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

**Production mode:**
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The backend will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Serve Frontend

Open `frontend/index.html` in your browser or serve via a static server:

```bash
# Using Python built-in server
python -m http.server 3000 --directory frontend

# Or use any HTTP server (nginx, Apache, etc.)
```

The frontend will be available at: `http://localhost:3000`

---

## 🚀 Running Individual AI Modules

### Video Liveness Detection

```bash
# Interactive menu
python -m ai_models.video_model.main

# Or direct test
python -m ai_models.video_model.test_video
```

### Face Verification System

```bash
# Register a new driver
python -m ai_models.face_verification.register_driver

# Verify an assigned driver
python -m ai_models.face_verification.verify_assigned_driver
```

### Ride Optimization Engine

```bash
# Run the optimization engine
python -m ai_models.ride_optimization.optimization_engine

# Run ride matching
python -m ai_models.ride_optimization.match_rides

# Run recommendation engine
python -m ai_models.ride_optimization.recommendation
```

### Ride Risk Prediction

```bash
# Generate synthetic dataset
python -m ai_models.ride_risk_prediction.generate_data

# Feature engineering
python -m ai_models.ride_risk_prediction.feature_engineering

# Train autoencoder model
python -m ai_models.ride_risk_prediction.train

# Detect suspicious ride
python -m ai_models.ride_risk_prediction.detect_anomaly
```

---

## 🌐 API Overview

### Base URL
```
http://localhost:8000
```

### API Routes

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Backend health check |
| `/` | GET | Home with model status |
| **Face Verification** |
| `/api/verify/register_driver` | POST | Register driver with ID & face |
| `/api/verify/verify` | POST | Verify driver identity |
| **Liveness Detection** |
| `/api/liveness/check` | POST | Check video liveness (upload) |
| **Ride Optimization** |
| `/api/ride/health` | GET | Ride service health |
| `/api/ride/create` | POST | Create new ride request |
| `/api/ride/start/{ride_id}` | POST | Start a ride |
| `/api/ride/complete/{ride_id}` | POST | Complete a ride |
| `/api/ride/cancel/{ride_id}` | POST | Cancel a ride |
| `/api/ride/active` | GET | Get active rides |
| `/api/ride/groups` | GET | Get active ride groups |
| `/api/ride/recommendations` | GET | Get optimization recommendations |
| `/api/ride/history` | GET | Get ride history |
| **Risk Prediction** |
| `/api/risk/predict` | POST | Predict ride risk |

---

## 🔄 Complete Workflow

### User Authentication & Safety Verification
```
1. User registers/logs in
2. Driver Registration:
   - Captures ID document
   - Captures live face photo
   - System extracts face from ID
   - Generates face embedding
   - Stores embedding for future verification
   
3. Driver Verification (Before Each Ride):
   - Captures live face photo
   - Performs liveness detection (anti-spoof)
   - Compares with stored embedding
   - Returns verification result
```

### Ride Optimization Workflow
```
1. User creates ride request
2. System registers ride in state manager
3. Geo-zone filtering for nearby rides
4. Route similarity analysis
5. Dynamic ride matching
6. Smart clustering for shared rides
7. AI recommendation generation
8. Optimization metrics calculated
9. Real-time updates to frontend
```

### Risk Detection Workflow
```
1. Ride telemetry collected during journey
2. Features engineered from raw data
3. Data normalized using saved scaler
4. Autoencoder generates reconstruction
5. Reconstruction loss calculated
6. Anomaly score compared to threshold
7. Result: NORMAL or SUSPICIOUS
```

---

## 🔐 Security & Safety Features

✅ **AI Anti-Spoof Detection** — Prevents fake face authentication  
✅ **Driver Identity Verification** — Facial embedding comparison  
✅ **Ride Anomaly Detection** — Deep learning-based safety intelligence  
✅ **Emergency Risk Analysis** — Panic button and crash detection  
✅ **Shared Ride Optimization** — Safe passenger matching  
✅ **Real-Time Risk Monitoring** — Continuous telemetry analysis  
✅ **Document Validation** — Quality checks and face extraction  

---

## 📊 Current Implementation Status

| Component | Status | Details |
|-----------|--------|---------|
| **Video Liveness** | ✅ Implemented | MobileNetV2 + LSTM, real-time detection |
| **Face Verification** | ✅ Implemented | Document capture, embedding storage, verification |
| **Ride Optimization** | ✅ Implemented | Matching, clustering, route analysis, state management |
| **Risk Prediction** | ✅ Implemented | Autoencoder anomaly detection, synthetic dataset |
| **FastAPI Backend** | ✅ Implemented | Service layer, routes, model registry |
| **Frontend Dashboard** | ✅ Implemented | Interactive UI, module controls, status display |
| **Docker Support** | ⚠️ Template Ready | Dockerfile provided, not yet tested in production |
| **Database** | ❌ Not Implemented | Currently uses in-memory state + file persistence |
| **Real-time GPS** | ❌ Not Implemented | Ready for integration |
| **Mobile App** | ❌ Not Implemented | Hackathon scope covers web only |

---

## 📥 Datasets & Checkpoints

Large datasets and trained model checkpoints are not uploaded to GitHub due to file size limitations.

**Available Datasets:**
* Face verification datasets (ID cards, live faces)
* Video liveness datasets (real/spoof video pairs)
* Synthetic ride telemetry data (for risk prediction)

**Download Links:**
* Face Verification: https://1drv.ms/f/c/f04d22b0287641f0/IgDhM0IFet2BT5EQFi8OGd2QASfhjJ6e-K99srM8krXk8BY?e=j9hAs8
* Video Liveness: https://1drv.ms/u/c/f04d22b0287641f0/IQByN_eUEP8WSqQywkFXQAUcAbAs-hsjIYVe6x__dSv_Ao0?e=NepUD5
* Risk Prediction: https://1drv.ms/f/c/f04d22b0287641f0/IgCXFAcC21J6S7bGOco6rxSSAXv-n1meG-4N-r6hd8HRezE?e=5Mf1Ub

---

## 🌍 Smart Mobility Applications

* Ride-sharing platforms (Uber, Ola, Grab)
* Smart transportation systems
* Driver authentication and KYC
* Urban traffic optimization
* Shared commute platforms
* AI-powered transportation safety
* Smart city mobility systems
* Autonomous fleet management

---

## 🔮 Future Scope

### AI Improvements
- Transformer-based temporal modeling
- Reinforcement learning optimization
- Advanced multi-modal anomaly detection
- Federated edge learning

### Smart Mobility Features  
- Live GPS integration
- Google Maps API integration
- Real-time traffic prediction
- AI-powered ETA prediction
- Dynamic surge pricing optimization
- Driver assignment AI
- Demand forecasting

### Infrastructure
- PostgreSQL database integration
- Redis distributed caching
- WebSocket real-time updates
- Docker deployment pipeline
- Cloud API integration (AWS/GCP/Azure)
- Mobile app (iOS/Android)

### Security & Compliance
- Multi-face verification
- Cloud authentication APIs
- Real-time fraud detection
- Compliance with local regulations
- Data privacy and encryption

---

## 👩‍💻 Author

**Kaveti Jyothika**

AI | Computer Vision | Smart Mobility | Transportation Intelligence

---

## 📄 License

This project is open source and available for educational, research, and hackathon purposes.

---

## 🚀 Bamboo Force AI

### Secure. Smart. Sustainable.

**AI-powered ride safety prediction system making transportation safer, smarter, and more sustainable.**
