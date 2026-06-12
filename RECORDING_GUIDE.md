# 🤟 Panduan Recording Dataset BISINDO/SIBI dari Penutur Asli

Panduan lengkap untuk merekam dan mengumpulkan dataset berkualitas tinggi dari penutur bahasa isyarat asli.

---

## 📋 Pre-Recording Checklist

### Persiapan Teknis
- [ ] Kamera dengan resolusi min 1080p (1920×1080)
- [ ] Tripod atau cara tetap untuk stabilitas kamera
- [ ] Pencahayaan: 2-3 ring light atau LED
- [ ] Background: Warna solid atau semi-solid (biru/putih/hijau)
- [ ] Ruangan yang tenang (no background noise untuk audio opsional)
- [ ] Charging cable untuk kamera
- [ ] Storage: Min 100GB untuk sesi recording

### Persiapan Administrasi
- [ ] Informed consent forms (siap dalam bahasa mudah dipahami)
- [ ] Kompensasi/honorarium (jika diperlukan)
- [ ] Jadwal recording yang fleksibel
- [ ] Tim: Min 2 orang (operator + monitor)

### Setup Software
```bash
# Python script untuk merekam & auto-extract landmarks
# Lokasi: src/phase2_dataset/record_dataset.py
python src/phase2_dataset/record_dataset.py
```

---

## 🎬 Setup Lokasi Recording (Studio)

### Tata Letak Ideal

```
┌─────────────────────────────────────┐
│          RING LIGHT (Top)           │
│                                     │
│  LED         PENUTUR        LED     │
│  (Left)      ISYARAT       (Right)  │
│              (Center)              │
│                                     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░      BACKGROUND: Solid Color  ░  │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│                                     │
│              KAMERA                 │
│         (150-200cm jauhnya)         │
│                                     │
└─────────────────────────────────────┘

JARAK OPTIMAL:
- Kamera ke penutur: 150-200cm
- Penutur dalam frame: Head to waist
- Sudut kamera: Sejajar dengan mata
```

### Pencahayaan: 3-Light Setup (Professional)

| Posisi | Fungsi | Watt | Sudut |
|--------|--------|------|-------|
| Depan (Key) | Main light | 50-100W | 45° ke tangan |
| Kanan (Fill) | Hilangkan shadow | 30-50W | Lembut |
| Belakang (Back) | Separation dari bg | 30-50W | Behind penutur |

**Hasil:** Tangan jelas, ada dimensi, minimal shadow.

---

## 👥 Merekam dari Penutur Asli

### Tahap 1: Persiapan dengan Penutur

#### 1.1 Perkenalan & Consent
```
Durasi: 10-15 menit

1. Sambut penutur dengan ramah
2. Jelaskan tujuan project (accessibility untuk tunarungu)
3. Tunjukkan contoh kamera & cara merekam
4. Tanyakan soal comfort level
5. Dapatkan written consent
6. Diskusikan kompensasi
```

#### 1.2 Warm-up & Familiarization
```
Durasi: 15-20 menit

1. Ajak ngobrol casual (comfort building)
2. Coba kamera recording 1-2 menit (test gerak)
3. Lihat preview bersama
4. Sesuaikan lighting/positioning jika perlu
5. Pastikan penutur nyaman
```

### Tahap 2: Recording Procedure

#### Setup Framework

```python
# Recording protocol untuk setiap sesi
class RecordingSession:
    def __init__(self, penutur_name, language="sibi"):
        self.penutur = penutur_name
        self.language = language
        self.start_time = datetime.now()
        self.recorded_letters = {}
    
    def record_letter(self, letter, num_samples=50):
        """
        Record satu huruf dengan multiple poses
        
        Poses yang harus di-record:
        1. Depan (neutral)
        2. Tangan kiri
        3. Tangan kanan
        4. Tangan atas
        5. Tangan bawah
        6. Dekat kamera
        7. Jauh dari kamera
        """
        pass
```

#### Protokol Per Huruf

**Untuk setiap huruf A-Z:**

1. **Instruktif (30 detik)**
   - Jelaskan huruf apa yang akan direkam
   - Tunjukkan bentuk tangan
   - Tanya: "Siap?"

2. **Recording (5-10 detik × multiple takes)**
   - Hold pose: 2 detik
   - Ganti sudut/pose
   - Record 5-7 poses berbeda per huruf
   - Target: 50-100 frames per huruf

3. **Review (30 detik)**
   - Tunjukkan hasil ke penutur
   - Tanya: "OK atau ulangi?"
   - Ambil keputusan

**Total per huruf: ~2-3 menit**

#### Variasi Pose untuk Setiap Huruf

```
POSE 1: Frontal Neutral
  - Tangan di depan badan
  - Normal height
  - Direct to camera

POSE 2: Left Side
  - 45° ke kiri
  - Same height
  - Full hand visible

POSE 3: Right Side
  - 45° ke kanan
  - Same height
  - Full hand visible

POSE 4: High Position
  - Tangan lebih tinggi (eye level)
  - Frontal
  - Untuk huruf yang dibuat di atas

POSE 5: Low Position
  - Tangan lebih rendah (chest level)
  - Frontal
  - Untuk huruf yang dibuat di bawah

POSE 6: Dynamic Motion (jika letter-specific)
  - Gerakan natural penutur
  - Multiple frames
  - Capture movement

POSE 7: Close-up
  - Tangan lebih dekat (~1 meter)
  - Detail fingers jelas
  - Untuk analisis fine details

POSE 8: Distance
  - Tangan lebih jauh (~3 meter)
  - Full body context
  - Natural distance communication
```

### Tahap 3: Quality Control During Recording

#### Real-time Monitoring

```python
# Monitoring script untuk saat recording
def monitor_recording_quality():
    checklist = {
        'hand_visible': True,      # Tangan terlihat 100%?
        'background_clean': True,  # Background solid?
        'no_blur': True,           # Tidak blur?
        'lighting_good': True,     # Pencahayaan OK?
        'pose_variety': True,      # Ada variasi pose?
        'natural_movement': True,  # Gerak natural, bukan kaku?
    }
    
    for check, status in checklist.items():
        if not status:
            print(f"⚠️  {check}: PERLU IMPROVE")
            return False
    
    return True
```

#### Batching Strategy

**Optimal Recording Workflow:**

```
Session: 120 menit (2 jam)
├─ Warm-up: 15 min
├─ Recording: 90 min
│   ├─ Blok 1 (Huruf A-M): 45 min
│   │   └─ Per huruf: 2-3 min × 13 = ~39 min + breaks
│   │
│   ├─ Break: 10 min (penutur refresh)
│   │
│   └─ Blok 2 (Huruf N-Z): 45 min
│       └─ Per huruf: 2-3 min × 13 = ~39 min + breaks
│
└─ Cleanup & Review: 15 min

HASIL: 26 huruf × 50+ samples = 1,300+ images per session
```

---

## 📸 Recording Teknis Step-by-Step

### Setup Kamera

```python
import cv2

# Kamera settings yang optimal
cap = cv2.VideoCapture(0)

# Resolution: 1080p
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# FPS: 30fps untuk smooth
cap.set(cv2.CAP_PROP_FPS, 30)

# Exposure: Auto (jika ada ring light)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)

# Autofocus: Enable
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
```

### Recording Script Template

```python
import cv2
from pathlib import Path
from datetime import datetime

class IsyaratRecorder:
    def __init__(self, penutur_name, language="sibi"):
        self.penutur = penutur_name
        self.language = language
        self.output_dir = Path(f"dataset/{language}")
        self.session_dir = self.output_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_dir.mkdir(exist_ok=True)
        self.cap = cv2.VideoCapture(0)
        self.setup_camera()
    
    def setup_camera(self):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
    
    def record_letter(self, letter, num_poses=7):
        """Record satu huruf dengan multiple poses"""
        letter_dir = self.output_dir / letter
        letter_dir.mkdir(exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Recording: {letter.upper()}")
        print(f"Penutur: {self.penutur}")
        print(f"{'='*60}")
        print("\nPoses to record:")
        poses = [
            "1. Frontal Neutral",
            "2. Left Side (45°)",
            "3. Right Side (45°)",
            "4. High Position",
            "5. Low Position",
            "6. Close-up",
            "7. Distance/Full Body"
        ]
        for pose in poses:
            print(f"  {pose}")
        
        print("\nPress SPACE to capture, 'n' for next letter, 'q' to quit")
        
        frame_count = 0
        pose_count = 0
        
        while pose_count < num_poses:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Display info
            cv2.putText(frame, f"Letter: {letter.upper()}", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
            cv2.putText(frame, f"Pose: {pose_count+1}/{num_poses}", (20, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Frames: {frame_count}", (20, 140),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow(f"Recording - {self.penutur}", frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):
                # Save frame
                filename = f"{letter}_{frame_count:04d}.jpg"
                filepath = letter_dir / filename
                cv2.imwrite(str(filepath), frame)
                frame_count += 1
                pose_count += 1
                print(f"  ✓ Saved: {filename}")
            
            elif key == ord('n'):
                break
            
            elif key == ord('q'):
                return False
        
        print(f"✓ Completed {letter.upper()}: {frame_count} frames")
        return True
    
    def record_all_letters(self):
        """Record semua huruf A-Z"""
        letters = [chr(ord('A') + i) for i in range(26)]
        
        for letter in letters:
            success = self.record_letter(letter, num_poses=7)
            if not success:
                break
            
            print("\nPress ENTER for next letter, 'q' to stop:")
            if input().strip().lower() == 'q':
                break
        
        print(f"\n✓ Recording session complete!")
        print(f"Files saved in: {self.session_dir}")
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()


# Usage
recorder = IsyaratRecorder(penutur_name="Budi", language="sibi")
recorder.record_all_letters()
recorder.release()
```

---

## 📊 Data Collection Strategy

### Multiple Penutur (Rekomendasi)

**Untuk accuracy terbaik:**

| Jumlah Penutur | Frames per Letter | Total Frames | Accuracy |
|----------------|------------------|--------------|----------|
| 1 penutur      | 50-100          | 1,300-2,600 | 85-90%   |
| 2-3 penutur    | 30-50 × 2-3     | 1,560-3,900 | 90-95%   |
| 4-5 penutur    | 20-30 × 4-5     | 2,080-3,900 | 95%+     |

**Alasan:** Variasi regional & individual dalam cara membuat isyarat.

### Recording Schedule

**Untuk 5 penutur × 26 huruf:**

```
Week 1: Penutur 1 & 2
├─ Day 1: Penutur 1 - Huruf A-M (90 min)
├─ Day 2: Penutur 1 - Huruf N-Z (90 min)
├─ Day 3: Penutur 2 - Huruf A-M (90 min)
└─ Day 4: Penutur 2 - Huruf N-Z (90 min)

Week 2: Penutur 3 & 4
├─ Day 1: Penutur 3 - Huruf A-M
├─ Day 2: Penutur 3 - Huruf N-Z
├─ Day 3: Penutur 4 - Huruf A-M
└─ Day 4: Penutur 4 - Huruf N-Z

Week 3: Penutur 5 + Quality Check
├─ Day 1: Penutur 5 - Huruf A-M
├─ Day 2: Penutur 5 - Huruf N-Z
├─ Day 3-4: Review & Re-record (jika perlu)

TOTAL: 3 minggu untuk 5 penutur
```

---

## ✅ Quality Assurance

### Post-Recording Validation

```python
import cv2
from pathlib import Path

def validate_dataset(dataset_path):
    issues = []
    
    for letter_dir in Path(dataset_path).iterdir():
        if not letter_dir.is_dir():
            continue
        
        images = list(letter_dir.glob("*.jpg"))
        
        if len(images) < 50:
            issues.append(f"❌ {letter_dir.name}: Only {len(images)} images (min 50)")
            continue
        
        print(f"✓ {letter_dir.name}: {len(images)} images")
        
        # Check sample images
        for img_file in images[:3]:
            img = cv2.imread(str(img_file))
            
            if img is None:
                issues.append(f"  ❌ Invalid file: {img_file.name}")
            
            if img.mean() < 50:
                issues.append(f"  ⚠️  Too dark: {img_file.name}")
            
            if img.mean() > 200:
                issues.append(f"  ⚠️  Too bright: {img_file.name}")
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} issues:")
        for issue in issues[:10]:
            print(f"  {issue}")
    else:
        print("\n✓ All validation passed!")
    
    return len(issues) == 0

# Usage
validate_dataset("dataset/sibi")
```

### Manual Review Checklist

```
Per sesi recording:

□ Semua 26 huruf terekam
□ Setiap huruf min 50 images
□ Tangan fully visible di semua images
□ No blur/motion artifacts
□ Consistent lighting
□ Varied poses/angles
□ Natural movements (not robotic)
□ No spectators/distractions di background
□ Clear contrast dengan background
□ Face/head included (context)
□ All files named correctly
□ Files organized per letter
□ Backup ke drive eksternal
```

---

## 💰 Ethical Considerations

### Working with Deaf Community

✅ **DO:**
- Kompensasi yang fair untuk waktu & effort
- Respect privacy & intellectual property
- Involve community in project planning
- Share results & benefits dengan community
- Get proper consent & approval
- Use culturally appropriate language
- Celebrate penutur dalam credits
- Consider accessibility dalam presentation

❌ **DON'T:**
- Exploit community labor tanpa kompensasi
- Use data untuk hal yang tidak sesuai
- Share data tanpa permission
- Stereotype atau "tokenize" penutur
- Record tanpa consent
- Use data komersial tanpa approval

### Suggested Compensation
- IDR 300,000 - 500,000 per sesi 2 jam
- Atau equivalent dengan local market rate
- Include transport/meals jika di luar kota

---

## 📱 Alternative: Using Smartphone

Jika tidak punya kamera profesional:

```python
# Android/iPhone recording via USB
import subprocess

# Record ke file menggunakan ffmpeg
cmd = """
ffmpeg -f dshow -i video="USB Video Device" -vf scale=1920:1080 output.mp4
"""

# Atau gunakan aplikasi:
# - DroidCam (Android)
# - Epocam (iPhone)
# Connect via USB -> OpenCV cv2.VideoCapture()
```

---

## 🎓 Data Documentation

**Setiap sesi recording, dokumentasikan:**

```json
{
  "session_id": "20260613_001",
  "date": "2026-06-13",
  "language": "sibi",
  "penutur": [
    {
      "name": "Budi Santoso",
      "age": 35,
      "deaf_since": "birth",
      "sibi_fluency": "native",
      "region": "Jakarta",
      "notes": "Fast, clear signer"
    }
  ],
  "equipment": {
    "camera": "Canon EOS R5",
    "resolution": "1920x1080",
    "fps": 30,
    "lighting": "3-light setup"
  },
  "total_images": 1300,
  "images_per_letter": 50,
  "quality_score": 9.2,
  "notes": "Good lighting, clear poses"
}
```

---

## 🚀 Quick Start Recording

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate di Windows
pip install -r requirements.txt

# 2. Prepare dataset folder
python src/phase2_dataset/dataset_preparation.py

# 3. Start recording
python src/phase2_dataset/record_dataset.py

# 4. Follow on-screen instructions untuk setiap huruf

# 5. Validate
python -c "from utils import DatasetManager; DatasetManager('dataset').print_dataset_info('sibi')"

# 6. Extract landmarks
python src/phase3_feature_extraction/extract_landmarks.py

# 7. Train model
python src/phase4_model_training/stage1_random_forest.py
```

---

## ✨ Tips Sukses

1. **Build rapport dulu** - Habiskan 15-20 min untuk kenalan
2. **Break sering** - Recording bisa capai mental, istirahat setiap 45 min
3. **Positive reinforcement** - Apresiasi setiap sesi ("Bagus sekali!")
4. **Technical support** - Siapkan orang yang tau camera/tech
5. **Flexible scheduling** - Sesuaikan dengan kenyamanan penutur
6. **Show appreciation** - Tunjukkan hasil AI ke penutur, lihat mereka excited!
7. **Follow up** - Terima kasih & update progress ke penutur

---

**Semoga recording dataset-nya lancar! 🎬🤟**
