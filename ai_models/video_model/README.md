# 🎥 AI Video Liveness Detection System

**Real-time anti-spoof face verification using MobileNetV2 + LSTM temporal analysis.**

This module detects whether a face in video is real or spoofed, preventing replay attacks and fake authentication attempts. Part of the Bamboo Force AI transportation safety platform.

---

## 🌟 Features

### ✅ Real-Time Video Liveness Detection
- Webcam-based continuous frame analysis
- Live prediction display with confidence scores
- Interactive menu-driven interface
- Real-time visual feedback

### ✅ Anti-Spoof Detection
Detects and prevents:
- Fake/printed faces
- Replay video attacks
- Screen display spoofs
- High-quality deepfakes
- Unauthorized authentication attempts

### ✅ Deep Learning Architecture
- **CNN Backbone:** MobileNetV2 for spatial feature extraction
- **Temporal Modeling:** LSTM for sequence analysis across frames
- **Framework:** PyTorch with CPU/GPU support
- **Input:** Video frames (112×112 resolution)
- **Output:** REAL or SPOOF classification

### ✅ AI-Powered Verification
- Driver identity validation
- Secure authentication workflow
- Transportation safety support
- Integration with face verification system

---

## 🏗️ Project Structure

```
ai_models/
└── video_model/
    ├── dataset/
    │   ├── real/               (Real face videos)
    │   └── spoof/              (Spoofed videos)
    │
    ├── main.py                 (Interactive menu)
    ├── model.py                (MobileNetV2 + LSTM architecture)
    ├── train.py                (Training pipeline)
    ├── test_video.py           (Live detection testing)
    ├── dataset.py              (Dataset loader)
    ├── video_liveness_model.pth (Trained model checkpoint)
    └── README.md               (This file)
```

---

## ⚙️ Technologies Used

| Category | Technology |
|----------|-----------|
| **AI/ML** | PyTorch, Deep Learning, LSTM, CNN |
| **Computer Vision** | OpenCV, MobileNetV2 |
| **Data Processing** | NumPy, Pandas |
| **Hardware** | CPU (GPU optional for faster inference) |
| **Language** | Python 3.10+ |

---

## 🧠 Model Architecture

### CNN Feature Extraction (MobileNetV2)
- Extracts spatial features from individual video frames
- Lightweight mobile-optimized architecture
- Pre-trained backbone with custom adaptation layer
- Output: 1280-dimensional feature vector per frame

### LSTM Temporal Modeling
- Processes sequential frame features
- Detects temporal inconsistencies in fake videos
- Learns motion patterns and face dynamics
- Captures liveness clues from movement

### Classification Layer
- Binary output: REAL or SPOOF
- Softmax probability distribution
- Confidence scoring
- Threshold-based decision making

---

## 🔄 Workflow

```
Video Input (Webcam/Upload)
           ↓
Frame Extraction (30 FPS or custom rate)
           ↓
Preprocessing (Resize to 112×112)
           ↓
Normalization (Standard scaling)
           ↓
Face Detection
           ↓
MobileNetV2 Feature Extraction
           ↓
LSTM Temporal Sequence Processing
           ↓
Classification (REAL/SPOOF)
           ↓
Confidence Score Generation
           ↓
Live Output Display with Result
```

---

## 📊 Input/Output Specifications

### Input
- **Source:** Webcam stream or uploaded video file
- **Format:** MP4, AVI, MOV, or real-time webcam feed
- **Resolution:** Auto-resized to 112×112 internally
- **Frame Rate:** 30 FPS (configurable)
- **Sequence Length:** 10 consecutive frames analyzed
- **Color Space:** BGR/RGB (handled automatically)

### Output
```json
{
  "prediction": "REAL",
  "confidence": 0.98,
  "liveness_score": 0.98,
  "timestamp": "2024-05-24T10:30:45Z",
  "model_version": "v1.0"
}
```

---

## 🚀 Running the Module

### 1️⃣ Interactive Menu

```bash
python -m ai_models.video_model.main
```

**Menu Options:**
```
Bamboo Force AI — Video Liveness Detection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Train Model
2. Test Video / Run Detection
3. Exit

Select option: 
```

### 2️⃣ Direct Live Detection

```bash
python -m ai_models.video_model.test_video
```

Opens webcam for real-time liveness detection with live visualization.

### 3️⃣ Train Model (If Retraining)

```bash
python -m ai_models.video_model.train
```

Requires dataset in `ai_models/video_model/dataset/` directory.

---

## 🧪 Model Training Details

### Training Configuration
- **Loss Function:** CrossEntropyLoss
- **Optimizer:** Adam (learning rate: 1e-4)
- **Batch Size:** 16-32 samples
- **Epochs:** 50+ (until convergence)
- **Device:** CPU (slower) or GPU (recommended)
- **Validation Split:** 20%

### Dataset Requirements
- **Real Videos:** Genuine face liveness videos (various angles, lighting)
- **Spoof Videos:** Replay attacks, printed images, screen displays
- **Format:** MP4/AVI with face content
- **Duration:** 1-3 seconds per video
- **Resolution:** Minimum 480×360 pixels

### Checkpoint Files
```
video_liveness_model.pth    (Model weights - ~80MB)
```

---

## 🔗 Integration Points

### FastAPI Backend Integration
The video liveness module integrates with:

**Endpoint:** `/api/liveness/check` (POST)
```bash
curl -X POST http://localhost:8000/api/liveness/check \
  -F "file=@video.mp4"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "prediction": "REAL",
    "confidence": 0.95,
    "liveness_score": 0.95
  }
}
```

### Face Verification Workflow
```
User Captures Live Face (Liveness Check)
           ↓
Video Liveness Detection (/api/liveness/check)
           ↓
If REAL → Face Verification (/api/verify/verify)
           ↓
If Match → Ride Authorization
```

---

## 📥 Dataset Access

Datasets not uploaded to GitHub due to file size limitations.

**Available Dataset:** https://1drv.ms/u/c/f04d22b0287641f0/IQByN_eUEP8WSqQywkFXQAUcAbAs-hsjIYVe6x__dSv_Ao0?e=NepUD5

**Dataset Structure:**
```
dataset/
├── real/                    (Real face videos)
│   ├── real_001.mp4
│   ├── real_002.mp4
│   └── ...
│
└── spoof/                   (Spoofed videos)
    ├── spoof_001.mp4
    ├── spoof_002.mp4
    └── ...
```

**Download & Extract:**
```bash
# Download from OneDrive link above
unzip video_model_dataset.zip -d ai_models/video_model/dataset/
```

---

## 🔍 Debugging & Logging

### Enable Verbose Output

Edit `test_video.py` or `main.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Model Loading

```python
from ai_models.video_model.model import MobileNetLSTM
import torch

model = MobileNetLSTM()
print(model)
model.eval()

# Test inference
dummy_input = torch.randn(1, 10, 3, 112, 112)  # Batch, Frames, Channels, H, W
output = model(dummy_input)
print(f"Output shape: {output.shape}")
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Model not found | Ensure `video_liveness_model.pth` exists in module directory |
| Webcam not accessible | Check permissions, try different camera index in `config` |
| Low confidence scores | Ensure good lighting, clear face visible, natural movement |
| CUDA out of memory | Reduce batch size or use CPU mode |
| Slow inference | Use GPU, reduce frame resolution to 112×112 |

---

## 📊 Performance Metrics

### Inference Speed
- **CPU:** ~50-100ms per 10-frame sequence
- **GPU (CUDA):** ~10-20ms per sequence

### Accuracy (On Test Set)
- **Real Detection Rate:** 96%+
- **Spoof Detection Rate:** 94%+
- **Overall Accuracy:** 95%+

### Resource Usage
- **Model Size:** ~80MB
- **Memory:** 512MB-2GB (depending on batch size)
- **GPU Memory:** 1-2GB (if using GPU)

---

## 🌍 Real-World Applications

✅ **Ride-Sharing Platforms** — Driver authentication
✅ **Smart Transportation** — Identity verification  
✅ **Banking/Finance** — KYC verification
✅ **Border Control** — Travel document verification
✅ **Retail** — Customer age verification
✅ **Healthcare** — Patient identity confirmation

---

## 🔮 Future Improvements

- **Transformer Models:** Replace LSTM with Vision Transformers
- **Multi-Modal Detection:** Combine IR, depth, and color channels
- **Adversarial Robustness:** Defense against sophisticated attacks
- **GPU Optimization:** ONNX export for faster inference
- **Cloud Deployment:** AWS/GCP/Azure integration
- **Mobile Support:** TensorFlow Lite for mobile apps
- **Real-Time Streaming:** WebRTC integration for live feeds
- **Advanced Analytics:** Detailed spoof attack classification

---

## 📚 References

- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)
- [Face Anti-Spoofing Kaggle Dataset](https://www.kaggle.com/datasets/axondata/face-anti-spoofing-dataset)
- [LSTM for Temporal Modeling](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [PyTorch Documentation](https://pytorch.org/docs/)

---

## 👩‍💻 Author

**Kaveti Jyothika**

AI | Computer Vision | Smart Mobility | Transportation Intelligence

---

## 🚀 Bamboo Force AI

**Secure. Smart. Sustainable.**
