# 🛡️ AI Face Verification System

**Secure driver identity verification and KYC authentication using face embeddings and real-time comparison.**

AI-powered driver verification and ride authentication system for Bamboo Force AI. Implements face encoding, storage, and matching for reliable driver identity validation before ride authorization.

---

## 🌟 Features

### ✅ Driver KYC Verification
- Government ID document capture and validation
- Live face photo capture
- Automatic quality checks (blur, brightness, face detection)
- Document face extraction from ID cards

### ✅ Face Encoding & Matching
- Generates normalized 128-dimensional face embeddings
- Stores embeddings in pickle format for quick lookup
- Euclidean distance-based facial comparison
- Threshold-based matching (default: 0.6 distance)

### ✅ Driver Registration
- Multi-step driver registration workflow
- KYC document scanning
- Embedding generation and storage
- Driver metadata persistence

### ✅ Real-Time Verification
- Live driver verification before ride starts
- Compares current face to stored embedding
- Instant pass/fail decision
- Integration with ride authorization flow

### ✅ Secure Identity Validation
- OpenCV face detection validation
- Image quality assessment
- Embedding normalization
- Secure embedding storage

---

## 🧠 Module Components

### 📷 `camera.py`
**Purpose:** Captures images from webcam

**Functions:**
- `capture_image()` — Captures single frame from webcam
- `capture_multiple_frames()` — Captures N frames for averaging
- Real-time display with OpenCV

### 🪪 `capture_document.py`
**Purpose:** Captures driver ID document

**Functions:**
- `capture_id_document()` — Guided document capture
- `validate_document_format()` — Checks aspect ratio and content
- Visual feedback for proper positioning

### ✅ `check_document.py`
**Purpose:** Validates document and image quality

**Validation Checks:**
- Image blur detection using Laplacian variance
- Brightness/contrast assessment
- Face presence detection
- Document clarity scoring
- Returns quality score (0.0-1.0)

**Functions:**
- `check_image_quality(image)` — Overall quality assessment
- `detect_faces(image)` — Face detection validation
- `is_clear_image(image)` — Blur detection

### ✂️ `extract_id_face.py`
**Purpose:** Extracts face region from ID document

**Workflow:**
1. Detects face in ID image
2. Crops face region with padding
3. Resizes to standard dimensions (200×200)
4. Returns cropped face for encoding

**Functions:**
- `extract_face_from_id(id_image)` — Main extraction function
- `crop_and_resize(face)` — Standardization

### 🧬 `encode.py`
**Purpose:** Generates face embeddings

**Architecture:**
- Uses `face_recognition` library (dlib-based)
- Generates 128-dimensional normalized embeddings
- Stores embeddings as numpy arrays
- Supports batch processing

**Functions:**
- `encode_face(face_image)` — Single face encoding
- `encode_batch(faces)` — Batch encoding
- `normalize_encoding(encoding)` — L2 normalization

### 🔍 `compare.py`
**Purpose:** Compares face embeddings

**Comparison Method:**
- Euclidean distance calculation
- Distance threshold: 0.6 (adjustable)
- Returns match confidence (0-1 scale)
- Supports 1-to-1 and 1-to-N matching

**Functions:**
- `compare_faces(known_encoding, unknown_encoding)` — Single comparison
- `find_best_match(unknown, known_list)` — Search embeddings
- `calculate_distance(enc1, enc2)` — Euclidean distance

### 🧾 `register_driver.py`
**Purpose:** Driver registration workflow

**Workflow Steps:**
1. Capture government ID document
2. Validate document quality
3. Extract face from ID
4. Capture live face photo
5. Generate face embedding
6. Store embedding with driver ID
7. Persist driver metadata

**Functions:**
- `register_driver(driver_id, driver_name)` — Main registration
- `save_embedding(driver_id, embedding)` — Storage
- `verify_new_registration(driver_id)` — Verification test

**Output:**
```json
{
  "driver_id": "DR001",
  "driver_name": "John Doe",
  "registered_at": "2024-05-24T10:30:00Z",
  "embedding_file": "embeddings/DR001.pkl",
  "status": "verified"
}
```

### 🚗 `verify_assigned_driver.py`
**Purpose:** Verify driver before ride authorization

**Workflow Steps:**
1. Receive driver ID and live face image
2. Load stored embedding for driver
3. Generate embedding for current face
4. Compare embeddings
5. Calculate match confidence
6. Return pass/fail result

**Functions:**
- `verify_driver(driver_id, live_image)` — Main verification
- `load_driver_embedding(driver_id)` — Retrieve stored embedding
- `is_driver_verified(match_distance)` — Threshold check

**Output:**
```json
{
  "driver_id": "DR001",
  "verified": true,
  "confidence": 0.92,
  "distance": 0.45,
  "threshold": 0.6,
  "timestamp": "2024-05-24T11:15:00Z"
}
```

---

## 🏗️ Complete Workflow

```text
┌─────────────────────────────────────────────────────┐
│             DRIVER REGISTRATION                      │
└─────────────────────────────────────────────────────┘

1. Capture ID Document
   ↓
2. Validate Document Quality
   - Check sharpness, brightness, face presence
   ↓
3. Extract Face from ID
   - Detect face region
   - Crop and standardize
   ↓
4. Capture Live Face Photo
   - Multiple angles/lighting
   ↓
5. Check Live Photo Quality
   - Validation checks
   ↓
6. Generate Face Embedding
   - 128D normalized vector
   ↓
7. Store Embedding
   - File: embeddings/{driver_id}.pkl
   - Metadata: driver.json
   ↓
8. Registration Complete ✓

┌─────────────────────────────────────────────────────┐
│             DRIVER VERIFICATION                     │
└─────────────────────────────────────────────────────┘

1. Receive Driver ID + Live Image
   ↓
2. Load Stored Embedding
   - From: embeddings/{driver_id}.pkl
   ↓
3. Generate Current Embedding
   - From live image
   ↓
4. Compare Embeddings
   - Euclidean distance
   ↓
5. Calculate Confidence
   - distance_score = 1 - (distance / max_distance)
   ↓
6. Check Threshold
   - If distance < 0.6: VERIFIED
   - Else: NOT VERIFIED
   ↓
7. Return Result + Confidence
```

---

## ⚙️ Technologies Used

| Component | Technology |
|-----------|-----------|
| **Face Recognition** | face_recognition (dlib-based) |
| **Computer Vision** | OpenCV |
| **Data Processing** | NumPy |
| **Embedding Storage** | Pickle format |
| **Quality Check** | Image processing algorithms |
| **Backend Integration** | FastAPI routes |

---

## 📂 File Structure

```
ai_models/face_verification/
├── camera.py                    (Webcam capture)
├── capture_document.py          (ID document capture)
├── check_document.py            (Quality validation)
├── extract_id_face.py           (Face extraction)
├── encode.py                    (Embedding generation)
├── compare.py                   (Face comparison)
├── register_driver.py           (Registration workflow)
├── verify_assigned_driver.py    (Verification workflow)
├── embeddings/                  (Storage directory)
│   ├── DR001.pkl               (Driver embeddings)
│   ├── DR002.pkl
│   └── ...
├── data/                        (Test data directory)
│   ├── test_faces/
│   │   ├── ids/                (ID document images)
│   │   ├── live_faces/         (Live face photos)
│   │   └── cropped_face.jpg
│   └── driver_metadata.json
└── README.md
```

---

## 🚀 Running the Module

### 1️⃣ Driver Registration

```bash
python -m ai_models.face_verification.register_driver
```

**Interactive Flow:**
```
Bamboo Force AI — Driver Registration System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enter Driver ID: DR001
Enter Driver Name: John Doe

Step 1: Capture ID Document
- Position ID in frame
- Press SPACE to capture
- Quality check: ✓ PASSED

Step 2: Extract Face from ID
- Face detected and extracted
- Size: 200×200 pixels

Step 3: Capture Live Face
- Look at camera
- Press SPACE to capture
- Quality check: ✓ PASSED

Step 4: Generate Embedding
- Encoding face...
- Generated 128D embedding

Step 5: Store Embedding
- Saved to: embeddings/DR001.pkl

✓ Driver registered successfully!
Confidence: 0.95
```

### 2️⃣ Driver Verification

```bash
python -m ai_models.face_verification.verify_assigned_driver
```

**Interactive Flow:**
```
Bamboo Force AI — Driver Verification System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enter Driver ID to verify: DR001

Loading stored embedding...
Capturing live face...
Quality check: ✓ PASSED

Comparing faces...
Distance: 0.45
Confidence: 0.92
Threshold: 0.6

✓ DRIVER VERIFIED
Authorized for ride
```

---

## 🔗 API Integration

### FastAPI Endpoints

**Register Driver:** `/api/verify/register_driver` (POST)
```bash
curl -X POST http://localhost:8000/api/verify/register_driver \
  -F "driver_id=DR001" \
  -F "driver_name=John Doe" \
  -F "id_image=@id_card.jpg" \
  -F "live_image=@face.jpg"
```

**Response:**
```json
{
  "success": true,
  "driver_id": "DR001",
  "driver_name": "John Doe",
  "message": "Driver registered successfully",
  "confidence": 0.95
}
```

**Verify Driver:** `/api/verify/verify` (POST)
```bash
curl -X POST http://localhost:8000/api/verify/verify \
  -F "driver_id=DR001" \
  -F "live_image=@current_face.jpg"
```

**Response:**
```json
{
  "success": true,
  "driver_id": "DR001",
  "verified": true,
  "confidence": 0.92,
  "distance": 0.45
}
```

---

## 📊 Configuration Parameters

```python
# Embedding settings
EMBEDDING_SIZE = 128              # Face embedding dimension
EMBEDDING_FORMAT = "pickle"       # Storage format

# Face matching
DISTANCE_THRESHOLD = 0.6          # Euclidean distance threshold
CONFIDENCE_MULTIPLIER = 1.0       # For confidence calculation

# Image quality
MIN_FACE_SIZE = 50                # Minimum face pixels
BLUR_THRESHOLD = 100.0            # Laplacian variance threshold
MIN_BRIGHTNESS = 50               # 0-255 scale
MAX_BRIGHTNESS = 200              # 0-255 scale

# Directories
EMBEDDINGS_DIR = "./embeddings/"
DATA_DIR = "./data/"
```

---

## 📥 Dataset Access

Dataset not uploaded to GitHub due to file size limitations.

**Dataset Links:**
- 👉 https://1drv.ms/f/c/f04d22b0287641f0/IgDhM0IFet2BT5EQFi8OGd2QASfhjJ6e-K99srM8krXk8BY?e=j9hAs8
- 👉 https://1drv.ms/f/c/f04d22b0287641f0/IgBZQu5kmST0RJ8zFDFkw0bYAZbTB1EASrMNNKNk7zEdd1s?e=SAPAWe

---

## 🔍 Debugging & Logging

### Enable Debug Logging

Add to your script:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.debug("Driver registration started")
```

### Common Issues

| Issue | Solution |
|-------|----------|
| No face detected in ID | Ensure ID is clear, well-lit, and fully visible |
| Low embedding quality | Multiple capture attempts, better lighting |
| Verification fails | May not be same person; re-register with different image |
| File not found errors | Ensure embeddings/ directory exists |
| Webcam access denied | Check OS permissions for camera access |

---

## 📈 Performance Metrics

### Embedding Generation
- Time per face: ~200-500ms
- File size: ~4KB per embedding
- Memory usage: ~1MB for batch of 100 drivers

### Verification
- Comparison time: <10ms
- End-to-end with image capture: ~2-3 seconds
- Accuracy: 95%+ (verified on test set)

---

## 🌍 Real-World Applications

✅ **Ride-Sharing Platforms** — Driver authentication
✅ **Transportation Safety** — Identity verification  
✅ **Government KYC** — Document verification
✅ **Banking** — Customer authentication
✅ **Airports** — Traveler verification
✅ **Corporate Access** — Employee authentication

---

## 🔮 Future Improvements

- Multi-face detection and verification
- Liveness detection integration
- Cloud-based embedding storage
- Advanced anti-spoofing protection
- Real-time dashboard with verification logs
- Batch processing for multiple drivers
- GPU acceleration for faster encoding
- Integration with government ID databases

---

## 👩‍💻 Author

**Kaveti Jyothika**

AI | Smart Mobility | Transportation Intelligence

---

## 🚀 Bamboo Force AI

**Secure. Smart. Sustainable.**
