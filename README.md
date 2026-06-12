# 🤟 AI Deteksi Bahasa Isyarat BISINDO & SIBI

Sistem AI untuk mendeteksi bahasa isyarat BISINDO dan SIBI menggunakan kamera dan menampilkan hasil terjemahannya dalam bentuk teks. Sistem ini dirancang untuk tunarungu dengan fokus pada akurasi tinggi.

---

## 📁 Struktur Proyek

```
yuda/
├── README.md                          # File ini
├── requirements.txt                   # Dependencies
├── Roadmap.md                         # Detailed roadmap
│
├── src/                               # Source code
│   ├── phase1_setup/
│   │   └── verify_environment.py      # Verify instalasi
│   ├── phase2_dataset/
│   │   ├── dataset_preparation.py     # Setup folder structure
│   │   └── record_dataset.py          # Record dataset via kamera
│   ├── phase3_feature_extraction/
│   │   └── extract_landmarks.py       # Ekstrak 21 hand landmarks
│   ├── phase4_model_training/
│   │   └── stage1_random_forest.py    # Train Random Forest (Stage 1)
│   └── phase5_realtime_integration/
│       └── realtime_prediction.py     # Real-time detection
│
├── utils/                             # Shared utilities
│   ├── __init__.py
│   ├── mediapipe_extractor.py         # MediaPipe integration
│   ├── data_utils.py                  # Dataset management
│   └── model_utils.py                 # Model evaluation & saving
│
├── dataset/                           # Dataset folder
│   ├── sibi/                          # SIBI dataset (A-Z)
│   │   ├── A/
│   │   ├── B/
│   │   └── ...
│   └── bisindo/                       # BISINDO dataset (A-Z)
│       ├── A/
│       ├── B/
│       └── ...
│
├── data/                              # Processed data
│   ├── landmarks_sibi.pkl             # Extracted landmarks
│   └── landmarks_bisindo.pkl
│
├── models/                            # Trained models
│   ├── random_forest_sibi.pkl
│   ├── random_forest_sibi_scaler.pkl
│   ├── random_forest_sibi_classes.json
│   └── ...
│
└── notebooks/                         # Jupyter notebooks (opsional)
    └── exploration.ipynb              # Data exploration & analysis
```

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Verify Environment

```bash
python src/phase1_setup/verify_environment.py
```

### Step 3: Prepare Dataset Folder

```bash
python src/phase2_dataset/dataset_preparation.py
```

### Step 4: Get Dataset

Pilih salah satu:

**Option A: Download dari Kaggle/Roboflow**
- Visit [Kaggle](https://kaggle.com) atau [Roboflow Universe](https://universe.roboflow.com)
- Search "SIBI", "BISINDO", atau "sign language"
- Extract ke folder `dataset/sibi/` atau `dataset/bisindo/`

**Option B: Record Dataset Sendiri**

```bash
python src/phase2_dataset/record_dataset.py
```

Ikuti on-screen instructions untuk merekam 100+ images per huruf.

### Step 5: Extract Landmarks

```bash
python src/phase3_feature_extraction/extract_landmarks.py
```

### Step 6: Train Model

```bash
python src/phase4_model_training/stage1_random_forest.py
```

### Step 7: Test Real-time Detection

```bash
python src/phase5_realtime_integration/realtime_prediction.py
```

---

## 📖 Detailed Phase Information

### PHASE 1: Setup Environment
- Verify semua libraries terinstall
- Check compatibility
- Setup folder structure

**File:** `src/phase1_setup/verify_environment.py`

### PHASE 2: Dataset Preparation
- Buat folder structure untuk 26 huruf (A-Z)
- Support untuk SIBI dan BISINDO
- Option untuk recording manual atau download publik

**Files:**
- `src/phase2_dataset/dataset_preparation.py` - Setup folder
- `src/phase2_dataset/record_dataset.py` - Record dataset

**Requirements:**
- Minimum 100 images per letter (recommended: 200-500)
- Variasi: sudut tangan, pencahayaan, latar belakang
- Kamera dengan resolusi cukup bagus

### PHASE 3: Feature Extraction
- Deteksi 21 hand landmarks menggunakan MediaPipe
- Ekstrak 63 koordinat (x, y, z) per frame
- Simpan sebagai pickle file untuk training

**File:** `src/phase3_feature_extraction/extract_landmarks.py`

**Input:** Image files dari `dataset/`
**Output:** `data/landmarks_sibi.pkl` atau `data/landmarks_bisindo.pkl`

### PHASE 4: Model Training

#### Stage 1: Random Forest (Basic)
- Train pada 63 landmarks
- Cocok untuk static letters (huruf diam)
- Fast training, good accuracy (95%+ possible)

**File:** `src/phase4_model_training/stage1_random_forest.py`

**Output:** 
- `models/random_forest_sibi.pkl` (model)
- `models/random_forest_sibi_scaler.pkl` (scaler)
- `models/random_forest_sibi_classes.json` (class names)

#### Stage 2: CNN + Transfer Learning (Advanced)
- Coming soon
- Train langsung pada image (224x224)
- Better untuk variasi hand pose
- Requires GPU

#### Stage 3: LSTM (Sequence)
- Coming soon
- Untuk detection word/sentence (gerakan berurutan)
- Sequence modeling

### PHASE 5: Real-time Integration
- Load trained model
- Capture video dari kamera
- Real-time prediction dengan display
- Confidence threshold filtering

**File:** `src/phase5_realtime_integration/realtime_prediction.py`

**Features:**
- Live hand detection visualization
- Prediction smoothing (majority voting)
- FPS counter
- Confidence score display
- Reset history (R key)

---

## 📊 Dataset Guidelines

### Struktur Folder

```
dataset/sibi/
├── A/
│   ├── A_0001.jpg
│   ├── A_0002.jpg
│   └── ... (100-500+ images)
├── B/
│   ├── B_0001.jpg
│   ├── B_0002.jpg
│   └── ...
└── ... (A-Z)
```

### Rekomendasi Kualitas

| Aspek | Rekomendasi |
|-------|------------|
| Resolusi | Min 640x480, ideal 1280x720 |
| Lighting | Terang, konsisten, natural |
| Background | Solid (lebih mudah) atau varied |
| Sudut Tangan | Multiple angles (30°-180°) |
| Jarak Kamera | 30-60 cm |
| Images per Letter | 200-500+ (minimum 100) |
| Variasi Orang | Multiple people (optional but recommended) |

### Recording Tips

1. **Pencahayaan:** Gunakan natural light atau ring light
2. **Background:** Gunakan warna kontras dengan tangan
3. **Positioning:** Pastikan tangan ada di center of frame
4. **Consistency:** Maintain pose sampai capture
5. **Variety:** Rekam dari berbagai sudut dan jarak

---

## 🤖 Model Performance

### Random Forest (Stage 1)

| Metric | Expected Value |
|--------|--------------|
| Accuracy | 90-96% |
| Training Time | 1-5 minutes |
| Inference Time | ~1ms per frame |
| Memory Usage | ~50-100 MB |
| GPU Required | No |

**Best for:** Static letters, simple classification

### CNN (Stage 2) - Coming Soon

| Metric | Expected Value |
|--------|--------------|
| Accuracy | 95-99% |
| Training Time | 10-60 minutes (GPU) |
| Inference Time | ~5-10ms per frame |
| Memory Usage | ~200-500 MB |
| GPU Required | Yes (recommended) |

**Best for:** Direct image classification, better generalization

### LSTM (Stage 3) - Coming Soon

| Metric | Expected Value |
|--------|--------------|
| Accuracy | 95-99%+ |
| Training Time | 30+ minutes (GPU) |
| Inference Time | ~20-50ms per sequence |
| Memory Usage | ~500MB-1GB |
| GPU Required | Strongly recommended |

**Best for:** Word/sentence detection, sequence modeling

---

## 🔧 Troubleshooting

### Camera tidak bisa dibuka
```python
# Check if camera is available
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
```

### Hand tidak terdeteksi
1. Improve lighting (use more light)
2. Ensure hand is visible and clear
3. Try getting closer to camera
4. Adjust MediaPipe confidence threshold

### Low accuracy
1. Check dataset quality
2. Increase dataset size (more images per class)
3. Ensure dataset diversity (angles, lighting)
4. Try different model (CNN instead of Random Forest)
5. Adjust model hyperparameters

### Slow inference
1. Check if running on CPU (move to GPU if available)
2. Reduce input resolution
3. Use simpler model (Random Forest instead of CNN)
4. Check system resources

---

## 💾 Configuration

### MediaPipe Settings

File: `utils/mediapipe_extractor.py`

```python
MediaPipeHandExtractor(
    max_num_hands=1,                    # Jumlah tangan yang dideteksi
    min_detection_confidence=0.7        # Detection threshold
)
```

### Model Hyperparameters

File: `src/phase4_model_training/stage1_random_forest.py`

```python
trainer.train(
    n_estimators=100,      # Jumlah trees
    max_depth=20,          # Max tree depth
    random_state=42        # Random seed
)
```

---

## 📝 Logging

Semua modules menggunakan Python logging. Check console output untuk debug info.

**Levels:**
- `INFO` - Normal operation messages
- `WARNING` - Potential issues
- `ERROR` - Critical problems

---

## 🎯 Next Steps

### Short Term (Week 1-2)
1. ✅ Setup environment
2. ✅ Prepare dataset structure
3. Get 200+ images per letter
4. Extract landmarks
5. Train Random Forest

### Medium Term (Week 3-4)
1. Implement CNN model
2. Transfer learning setup
3. Improve accuracy to 95%+
4. Real-time testing

### Long Term (Month 2-3)
1. Implement LSTM for sequences
2. Multi-language support
3. Word/sentence detection
4. UI/Web interface

---

## 📚 Resources

### MediaPipe Documentation
https://mediapipe.dev/

### Scikit-learn Random Forest
https://scikit-learn.org/stable/modules/ensemble.html#random-forests

### TensorFlow/Keras
https://www.tensorflow.org/guide

### Sign Language Datasets
- [Kaggle](https://kaggle.com) - Search "sign language"
- [Roboflow Universe](https://universe.roboflow.com)
- [YouTube Hand Pose Database](https://www.youtube.com/results?search_query=hand+pose+dataset)

---

## 📄 License

This project is for educational and accessibility purposes.

---

## 👥 Contributing

Contributions are welcome! Areas for improvement:
- Add CNN/LSTM implementations
- Optimize performance
- Improve accuracy
- Add more languages
- Create web UI
- Add documentation

---

## 🙏 Credits

Built with:
- [MediaPipe](https://mediapipe.dev/) - Hand detection
- [OpenCV](https://opencv.org/) - Computer vision
- [Scikit-learn](https://scikit-learn.org/) - Machine learning
- [TensorFlow](https://www.tensorflow.org/) - Deep learning

---

## 📞 Support

For issues and questions:
1. Check the Roadmap.md for detailed info
2. Review troubleshooting section
3. Check console output for error messages
4. Verify dataset quality

---

**Happy coding! 🚀**
