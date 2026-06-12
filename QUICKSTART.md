# ⚡ QUICK START GUIDE

Panduan cepat untuk memulai proyek AI Deteksi Bahasa Isyarat.

---

## 🚀 5 Langkah Pertama

### 1. Install Dependencies (5 menit)

```bash
pip install -r requirements.txt
```

Verify instalasi:
```bash
python src/phase1_setup/verify_environment.py
```

### 2. Prepare Dataset (2 menit)

```bash
python src/phase2_dataset/dataset_preparation.py
```

Ini membuat folder structure untuk 26 huruf A-Z.

### 3. Get Dataset (Bervariasi)

**Option A - Download Publik (5 menit)**
- Visit [Kaggle](https://kaggle.com)
- Search: "SIBI" atau "sign language"
- Download & extract ke `dataset/sibi/` atau `dataset/bisindo/`

**Option B - Record Sendiri (1-2 jam)**
```bash
python src/phase2_dataset/record_dataset.py
```

Target: 100-500+ images per huruf untuk akurasi terbaik.

### 4. Extract Landmarks (10-30 menit)

```bash
python src/phase3_feature_extraction/extract_landmarks.py
```

Mengektrak 21 hand landmarks dari setiap image.

### 5. Train Model (5-15 menit)

```bash
python src/phase4_model_training/stage1_random_forest.py
```

Melatih Random Forest dengan 100+ trees.

---

## 🎥 Test Real-time Detection

```bash
python src/phase5_realtime_integration/realtime_prediction.py
```

Tekan 'Q' untuk quit, 'R' untuk reset history.

---

## 📊 Expected Accuracy

| Stage | Model | Accuracy | Time |
|-------|-------|----------|------|
| 1 | Random Forest | 90-96% | ⚡ Fast |
| 2 | CNN | 95-99% | 💻 Medium |
| 3 | LSTM | 95-99%+ | ⏳ Slow |

---

## 🎯 Minimal Viable Setup (30 minutes)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Setup folders
python src/phase2_dataset/dataset_preparation.py

# 3. (MANUAL) Download 10-15 images per letter dari Google Images
#    Put them in: dataset/sibi/A/, dataset/sibi/B/, etc.

# 4. Extract
python src/phase3_feature_extraction/extract_landmarks.py

# 5. Train
python src/phase4_model_training/stage1_random_forest.py

# 6. Test
python src/phase5_realtime_integration/realtime_prediction.py
```

⚠️ **Note:** With only 10-15 images per letter, accuracy will be low (~60-70%).

For production use, aim for 200+ images per letter.

---

## 💡 Tips

1. **Start dengan SIBI** - lebih mirip alfabet latin
2. **Gunakan pencahayaan baik** - sangat penting untuk deteksi akurat
3. **Variasi dataset** - sudut, pencahayaan, background
4. **Test setiap fase** - jangan loncat
5. **Gunakan GPU jika tersedia** - Phase 2 (CNN) lebih cepat

---

## 🆘 Common Issues

**Camera not detected:**
```bash
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

**Low accuracy:**
- More dataset needed (100+ per letter minimum)
- Better lighting
- Better background contrast

**Slow inference:**
- Use CPU first (easiest)
- Move to GPU (if available)
- Use Random Forest (not CNN)

---

## 📖 Full Documentation

See `README.md` untuk dokumentasi lengkap.

---

**Happy coding! 🚀**
