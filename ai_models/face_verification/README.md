# 🚀 AI Face Verification System

AI-powered driver verification and ride authentication system for Bamboo Force AI.

---

# 🌟 Features

- Driver KYC Verification
- Face Encoding & Matching
- Driver Authentication
- Ride Verification
- Embedding Storage
- Secure Transportation Identity Validation

---

# 🧠 Modules

## 📷 camera.py
Captures images using webcam.

## 🪪 capture_document.py
Captures driver ID document.

## ✅ check_document.py
Checks:
- image quality
- blur
- face presence

## ✂️ extract_id_face.py
Extracts face from ID card.

## 🧬 encode.py
Generates normalized 128D face embeddings.

## 🔍 compare.py
Compares face embeddings using Euclidean distance.

## 🧾 register_driver.py
Handles:
- driver registration
- KYC scan
- embedding storage
- face verification

## 🚗 verify_assigned_driver.py
Verifies arriving driver before ride authorization.

---

# 🏗️ Workflow

```text
Document Capture
      ↓
Document Validation
      ↓
Face Extraction
      ↓
Face Encoding
      ↓
Embedding Storage
      ↓
Live Driver Scan
      ↓
Face Verification
      ↓
Ride Authorization
```
---

# ⚙️ Technologies Used
- Python
- OpenCV
- face_recognition
- NumPy
- Flask APIs
---
# 📂 Dataset

Dataset not uploaded to GitHub because of file size limitations.

# 📥 Download Dataset

- 👉 https://1drv.ms/f/c/f04d22b0287641f0/IgDhM0IFet2BT5EQFi8OGd2QASfhjJ6e-K99srM8krXk8BY?e=j9hAs8

- 👉 https://1drv.ms/f/c/f04d22b0287641f0/IgBZQu5kmST0RJ8zFDFkw0bYAZbTB1EASrMNNKNk7zEdd1s?e=SAPAWe
---

# 📁 Folder Structure
```
data/
├── test_faces/
│   ├── ids/
│   ├── live_faces/
│   └── cropped_face.jpg
│
embeddings/
├── DR001.pkl

```
---

## 🚀 Run Driver Registration
- python -m ai_models.face_verification.register_driver

## 🚀 Run Ride Verification
- python -m ai_models.face_verification.verify_assigned_driver

---

# 🌍 Future Improvements
- Real-time liveness integration
- Multi-face detection
- Cloud-based verification APIs
- Advanced anti-spoof protection
- Smart mobility security integration

---

# 👩‍💻 Author
Kaveti Jyothika

AI | Smart Mobility | Transportation Intelligence

---

# 🚀 Bamboo Force AI
Secure. Smart. Sustainable.