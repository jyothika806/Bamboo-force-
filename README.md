# 🚖 Bamboo Force

Bamboo Force is a multi‑AI integrated project designed to enhance ride safety, trust, and efficiency.  
It combines face verification, risk prediction, and ride optimization into one system.

---

## 📌 Project Overview

Bamboo Force has three main models:

1. **Face Verification**
   - **User-side verification**: Confirms the assigned driver has arrived.
   - **Driver KYC + Liveness Check**: Uses video-based AI to detect spoofing and ensure the driver is real.

2. **Risk Prediction**
   - Analyzes ride factors (driver history, location, time, etc.).
   - Predicts risk level (Low / Medium / High).

3. **Optimization**
   - Optimizes rides to reduce **cost, traffic, and carbon emissions**.

---

## 📊 Datasets

Due to size constraints, datasets are hosted externally.  
The **video model dataset** is adapted from the [Kaggle Face Anti-Spoofing Dataset](https://www.kaggle.com/datasets/axondata/face-anti-spoofing-dataset) with rearrangements for training.

- [Video Model Dataset (Google Drive)](https://drive.google.com/drive/folders/1FxK1aHGYsIrpsVpa_wAM3FfuTiIbb3D1?usp=sharing)
- [Face Verification Dataset](LINK_HERE)
- [Risk Prediction Dataset](LINK_HERE)

### Download Instructions

```bash
# Example for video model dataset
wget "https://drive.google.com/drive/folders/1FxK1aHGYsIrpsVpa_wAM3FfuTiIbb3D1?usp=sharing" -O data/video_model_dataset.zip
unzip data/video_model_dataset.zip -d ai_models/video_model/dataset

