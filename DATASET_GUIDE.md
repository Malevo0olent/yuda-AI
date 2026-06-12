# 📸 DATASET CREATION GUIDE

Panduan lengkap untuk membuat dataset berkualitas tinggi.

---

## 📋 Checklist Sebelum Memulai

- [ ] Kamera dengan resolusi min 640x480 (lebih tinggi lebih baik)
- [ ] Pencahayaan yang cukup terang
- [ ] Background yang kontras dengan tangan
- [ ] Space yang cukup untuk gerak tangan
- [ ] Python environment sudah siap
- [ ] Folder structure sudah dibuat

---

## 🎬 Recording Setup

### Pencahayaan

| Tipe | Hasil | Tips |
|------|-------|------|
| Natural Light | ⭐⭐⭐⭐⭐ | Terbaik! Gunakan window/outdoor |
| Ring Light | ⭐⭐⭐⭐ | Sangat bagus untuk studio |
| Desk Lamp | ⭐⭐⭐ | Acceptable, pastikan tidak ada shadow |
| Dark Room | ⭐ | HINDARI! Terlalu gelap |

### Background

| Jenis | Cocok? | Catatan |
|------|--------|---------|
| Solid color (putih/biru) | ✅ Terbaik | Kontras tinggi, mudah deteksi |
| Pola seragam | ✅ Bagus | Office/rumah background |
| Berubah-ubah | ⚠️ Acceptable | Lebih challenging tapi lebih realistic |
| Sangat ramai | ❌ Hindari | Bisa meracuni model |

### Positioning

```
╔═══════════════════════╗
║   ← 30-60cm →        ║
║   ┌─────────────┐    ║
║   │  KAMERA     │    ║
║   └─────────────┘    ║
║                      ║
║   ┌─────────────┐    ║
║   │ TANGAN (A) │    ║
║   └─────────────┘    ║
║                      ║
╚═══════════════════════╝

- Jarak: 30-60 cm dari kamera
- Height: Tangan di tengah frame
- Angle: Mulai dari depan (0°), variasi ke samping
```

---

## 📝 Recording Procedure

### Menggunakan Script Record

```bash
python src/phase2_dataset/record_dataset.py
```

**Langkah-langkah:**

1. Pilih: "Record single letter" atau "Record all letters"
2. Pilih language: SIBI atau BISINDO
3. Position tangan sesuai letter
4. TEKAN SPACE untuk capture
5. TEKAN Q untuk selesai letter
6. TEKAN ENTER untuk next letter

### Manual Recording

Jika script recording kurang sempurna:

1. Buka kamera standar
2. Record video berisi gesture huruf
3. Extract frames menggunakan:

```python
import cv2

video_path = "path/to/video.mp4"
output_dir = "dataset/sibi/A"
cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % 5 == 0:  # Setiap 5 frame
        cv2.imwrite(f"{output_dir}/A_{frame_count:04d}.jpg", frame)
    frame_count += 1

cap.release()
```

---

## 📊 Dataset Quality Standards

### Minimum Requirements

| Aspek | Minimum | Recommended | Optimal |
|-------|---------|-------------|---------|
| Images per Letter | 50 | 200 | 500+ |
| Total Dataset | 1300 (26×50) | 5200 (26×200) | 13000+ |
| Lighting Consistency | 60% | 80% | 95%+ |
| Hand Visibility | 100% | 100% | 100% |
| Background Variation | 1 type | 2-3 types | 5+ types |
| Angle Variation | 1 angle | 3+ angles | 8+ angles |

### Quality Checklist per Letter

Sebelum pindah ke letter berikutnya:

- [ ] Minimal 50 images
- [ ] Hand visible dan clear di 95%+ images
- [ ] Variasi angle (front, side, rotated)
- [ ] Variasi jarak (close, medium, far)
- [ ] Variasi pencahayaan (bright, normal, dim)
- [ ] No blurry images
- [ ] Konsisten dengan requirements letter

---

## 🔄 Dataset Organization

### Folder Structure

```
dataset/
├── sibi/
│   ├── A/
│   │   ├── A_0001.jpg ✓
│   │   ├── A_0002.jpg ✓
│   │   ├── ...
│   │   └── A_0200.jpg ✓
│   ├── B/
│   │   ├── B_0001.jpg ✓
│   │   ├── ...
│   │   └── B_0200.jpg ✓
│   └── ... (C-Z)
│
└── bisindo/
    ├── A/
    └── ... (same structure)
```

### File Naming Convention

```
FORMAT: [LETTER]_[NUMBER].jpg

EXAMPLES:
- A_0001.jpg ✓ (Good)
- A_0001.png ✓ (OK, convert to jpg for consistency)
- A_0001.jpeg ✓ (OK)
- letter_a_1.jpg ✗ (Wrong)
- A.jpg ✗ (Missing number)
```

---

## 🎯 Recording Tips & Tricks

### Recording Technique

1. **Get comfortable position**
   - Duduk dengan posisi natural
   - Arm relaxed
   - No strain

2. **Make clear gesture**
   - Hold letter for 1-2 seconds
   - Move hand to show different angles
   - Don't shake

3. **Capture variety**
   - Record each letter multiple times
   - Change position between captures
   - Use different backgrounds

4. **Quality control**
   - Check lighting in preview
   - Ensure no motion blur
   - Verify hand is visible

### Common Mistakes to Avoid

| ❌ Mistake | ✅ Fix |
|-----------|--------|
| Too dark | Increase lighting |
| Hand cut off | Position hand in center |
| Blurry | Keep hand steady, good lighting |
| Wrong letter | Double check before recording |
| Same angle every time | Rotate hand, move position |
| Too close/far | Maintain 30-60cm distance |
| Camera angle changes | Lock camera position |

---

## 📈 Dataset Statistics

### Expected Progress

**Week 1:**
- SIBI: 26 letters × 50 images = 1,300 images

**Week 2:**
- SIBI: 26 letters × 200 images = 5,200 images
- Start BISINDO: 26 letters × 100 images = 2,600 images

**Month 2:**
- SIBI: 26 letters × 500 images = 13,000 images
- BISINDO: 26 letters × 300 images = 7,800 images
- **Total: 20,800 images**

### Data Distribution Check

```python
from pathlib import Path
from collections import Counter

dataset_path = Path("dataset/sibi")
counts = {}

for letter_dir in dataset_path.iterdir():
    if letter_dir.is_dir():
        images = len(list(letter_dir.glob("*.jpg")))
        counts[letter_dir.name] = images

# Check
min_count = min(counts.values())
max_count = max(counts.values())
avg_count = sum(counts.values()) / len(counts)

print(f"Min: {min_count}, Max: {max_count}, Avg: {avg_count:.0f}")
print(f"Imbalance: {(max_count - min_count) / avg_count * 100:.1f}%")

# Should be < 20% imbalance ideally
```

---

## 🧹 Data Cleaning

### Remove Bad Images

```python
import cv2
from pathlib import Path

# Find blurry or invalid images
dataset_path = Path("dataset/sibi/A")

for img_file in dataset_path.glob("*.jpg"):
    img = cv2.imread(str(img_file))
    
    if img is None:
        print(f"INVALID: {img_file}")
        # Delete or move to trash
    
    # Check if mostly black (underexposed)
    if img.mean() < 50:
        print(f"TOO DARK: {img_file}")
    
    # Check if mostly white (overexposed)
    if img.mean() > 200:
        print(f"TOO BRIGHT: {img_file}")
```

### Augmentation (Optional)

Jika dataset masih kurang:

```python
from imgaug import augmenters as iaa
import cv2
from pathlib import Path

augmenter = iaa.Sequential([
    iaa.Fliplr(0.5),
    iaa.Affine(rotate=(-10, 10)),
    iaa.Multiply((0.8, 1.2)),  # Brightness
])

# Augment each image
dataset_path = Path("dataset/sibi/A")
for img_file in dataset_path.glob("*.jpg"):
    img = cv2.imread(str(img_file))
    aug_img = augmenter(image=img)
    cv2.imwrite(str(img_file.parent / f"{img_file.stem}_aug.jpg"), aug_img)
```

---

## ✅ Validation Checklist

Sebelum proceed ke Phase 3:

- [ ] All 26 letters have folders
- [ ] Each letter memiliki minimum 50 images
- [ ] No invalid/corrupted images
- [ ] Naming convention konsisten
- [ ] Good lighting pada 90%+ images
- [ ] Hand visible pada 95%+ images
- [ ] Angle variation per letter
- [ ] Background variation adequate

---

## 📞 Troubleshooting

**Q: Berapa banyak images yang cukup?**
- Minimum: 100 per letter (2,600 total)
- Good: 200 per letter (5,200 total)
- Excellent: 500+ per letter (13,000+ total)

**Q: Berapa lama waktu yang dibutuhkan?**
- 100 per letter: 2-3 jam
- 200 per letter: 4-6 jam
- 500 per letter: 10-15 jam

**Q: Bisa pakai images dari Google?**
- Ya, tapi kualitas bervariasi
- Lebih baik record sendiri untuk konsistensi
- Mix dari multiple sources: OK

**Q: Apakah urutan penting?**
- Tidak, tapi record lengkap satu letter sebelum pindah

---

## 🎓 Best Practices

1. **Batch Recording**
   - Record semua dengan pencahayaan konsisten
   - Ganti satu variable sekaligus (angle, lighting, bg)

2. **Quality First**
   - Lebih baik 100 images berkualitas tinggi
   - Daripada 500 images berkualitas rendah

3. **Regular Backup**
   - Backup dataset regularly
   - Use external drive untuk safety

4. **Progressive Collection**
   - Start dengan minimal dataset
   - Test model
   - Add more data untuk improve accuracy

---

**Happy recording! 📸**
