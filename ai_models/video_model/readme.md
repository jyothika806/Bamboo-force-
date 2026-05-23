#  🎥 AI Video Liveness Detection System

AI-powered real-time face liveness detection and anti-spoof verification system using PyTorch, OpenCV, MobileNetV2, and LSTM-based temporal analysis.

---

# 🚀 Overview

This module is part of the Bamboo Force AI platform and focuses on:

- Real-time liveness detection
- Face spoof prevention
- Video-based authentication
- AI-powered driver verification
- Secure transportation identity validation

The system analyzes multiple video frames continuously and predicts whether the detected face is:

- REAL
- SPOOF

using deep learning models.

---

# 🧠 Features

## ✅ Real-Time Video Liveness Detection
- Webcam-based live prediction
- Continuous frame analysis
- Real-time visual feedback

## ✅ Anti-Spoof Detection
Detects:
- Fake faces
- Printed images
- Replay attacks
- Spoofed authentication attempts

## ✅ Deep Learning Architecture
Uses:
- MobileNetV2 CNN backbone
- LSTM temporal sequence modeling
- PyTorch inference pipeline

## ✅ AI-Powered Verification
- Driver identity validation
- Secure authentication workflow
- Transportation safety support

---

# 🏗️ Project Structure

```text
ai_models/
└── video_model/
    ├── dataset/
    │   ├── real/
    │   └── spoof/
    │
    ├── main.py
    ├── model.py
    ├── train.py
    ├── test_video.py
    ├── dataset.py
    └── video_liveness_model.pth
```
---

# ⚙️ Technologies Used

## AI / ML
- PyTorch
- MobileNetV2
- LSTM Neural Networks
## Computer Vision
- OpenCV
- NumPy
## Programming
- Python

---

# 🧠 Model Architecture

## CNN Feature Extraction

- MobileNetV2 extracts spatial facial features from video frames.

## Temporal Analysis

- LSTM processes sequential frame information to detect motion consistency and spoof patterns.

## Classification

- Final output predicts:

    REAL
    SPOOF

---

# 🔄 Workflow

```
    Video Input
        ↓
    Frame Extraction
        ↓
    Preprocessing
        ↓
    CNN Feature Extraction
        ↓
    LSTM Temporal Analysis
        ↓
    REAL / SPOOF Prediction
        ↓
    Live Output Display

```
---
# 🚀 Running the Project

## 1️⃣ Install Requirements
- pip install -r requirements.txt

## 2️⃣ Train the Model
- python -m ai_models.video_model.train

## 3️⃣ Run Real-Time Detection
- python -m ai_models.video_model.test_video

    OR

- python -m ai_models.video_model.main

---
# 🖥️ Main Menu System

The main.py file provides an interactive menu:
```
    1. Train Model
    2. Test Video / Run Detection
    3. Exit
```

# 📂 Dataset

The dataset is not uploaded to GitHub due to large file size limitations.
  
The **video model dataset** is adapted from the [Kaggle Face Anti-Spoofing Dataset](https://www.kaggle.com/datasets/axondata/face-anti-spoofing-dataset) with rearrangements for training.
### Download Instructions

```bash
# Example for video model dataset
wget "https://drive.google.com/drive/folders/1FxK1aHGYsIrpsVpa_wAM3FfuTiIbb3D1?usp=sharing" -O data/video_model_dataset.zip
unzip data/video_model_dataset.zip -d ai_models/video_model/dataset
```

# 📥 Download Dataset

Dataset Link: https://1drv.ms/u/c/f04d22b0287641f0/IQByN_eUEP8WSqQywkFXQAUcAbAs-hsjIYVe6x__dSv_Ao0?e=NepUD5

👉 Download Dataset

# 📁 Dataset Structure
```
    dataset/
    ├── real/
    │   ├── real1.mp4
    │   ├── real2.mp4
    │   └── ...
    │
    └── spoof/
        ├── spoof1.mp4
        ├── spoof2.mp4
        └── ...
```
# 🧪 Training Details

## Input
- Video frames
- Sequence length: 10 frames
- Resolution: 112x112

## Training
- CrossEntropyLoss
- Adam Optimizer
- PyTorch CPU inference


# 🔐 Security Applications

This module can be used for:

- Driver verification systems
- Smart mobility security
- Ride-sharing authentication
- AI-based transportation safety
- Secure identity verification

# 🌍 Future Improvements
- GPU acceleration
- Advanced spoof attack detection
- Transformer-based temporal modeling
- Cloud deployment APIs
- Smart city integration
- Real-time transportation intelligence

# 👩‍💻 Author
Kaveti Jyothika

AI | Computer Vision | Smart Mobility | Transportation Intelligence

# 🚀 Bamboo Force AI
Secure. Smart. Sustainable.