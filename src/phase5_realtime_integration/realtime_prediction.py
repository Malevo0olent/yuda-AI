import sys
from pathlib import Path
import cv2
import numpy as np
import pickle
import json
import logging
from collections import deque
from datetime import datetime

# Konfigurasi logging dasar
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tambahkan direktori induk proyek ke sys.path untuk impor modul
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils import MediaPipeHandExtractor, PredictionFormatter


class RealtimeSignLanguageDetector:
    """
    Deteksi bahasa isyarat secara real-time dari kamera.
    """
    
    def __init__(self, model_path: str, language: str = "sibi"):
        """
        Inisialisasi detektor.
        
        Args:
            model_path: Path ke file model terlatih (.pkl).
            language: 'sibi' atau 'bisindo'.
        """
        self.model_path = Path(model_path)
        self.language = language
        self.model = None
        self.scaler = None
        self.class_names = None
        
        # Ekstraktor landmark tangan
        self.extractor = MediaPipeHandExtractor()
        
        # Inisialisasi kamera
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            raise RuntimeError("Camera tidak bisa dibuka!")
        
        # Antrean untuk menghaluskan prediksi
        self.prediction_history = deque(maxlen=5)
        self.confidence_history = deque(maxlen=5)
        
        # Muat model
        if not self._load_model():
            raise RuntimeError(f"Gagal memuat model dari {model_path}")
    
    def _load_model(self) -> bool:
        """Muat model, scaler, dan daftar nama kelas dari disk."""
        try:
            # Muat model pickle
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            # Muat scaler terkait
            scaler_path = self.model_path.parent / f"{self.model_path.stem}_scaler.pkl"
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            
            # Muat daftar nama kelas JSON
            classes_path = self.model_path.parent / f"{self.model_path.stem}_classes.json"
            with open(classes_path, 'r') as f:
                self.class_names = json.load(f)
            
            logger.info("Model berhasil dimuat.")
            logger.info(f"Kelas: {', '.join(self.class_names)}")
            
            return True
        
        except Exception as e:
            logger.error(f"Gagal memuat model: {e}")
            return False
    
    def predict_from_landmarks(self, landmarks: np.ndarray) -> tuple:
        """
        Prediksi kelas dari landmark tangan.
        
        Returns:
            Nama kelas prediksi, skor keyakinan (0-1).
        """
        try:
            # Normalisasi landmark
            landmarks_normalized = self.scaler.transform([landmarks])
            
            # Prediksi kelas dan probabilitas
            prediction = self.model.predict(landmarks_normalized)[0]
            probabilities = self.model.predict_proba(landmarks_normalized)[0]
            confidence = probabilities[prediction]
            
            # Dapatkan nama kelas
            class_name = self.class_names[prediction]
            
            # Simpan dalam riwayat untuk penghalusan
            self.prediction_history.append(prediction)
            self.confidence_history.append(confidence)
            
            return class_name, confidence
        
        except Exception as e:
            logger.error(f"Error pada prediksi: {e}")
            return None, 0
    
    def get_smoothed_prediction(self) -> tuple:
        """
        Hitung prediksi yang dihaluskan berdasarkan suara terbanyak.
        """
        if not self.prediction_history:
            return None, 0
        
        # Cari prediksi yang paling sering muncul
        from collections import Counter
        most_common_id = Counter(self.prediction_history).most_common(1)[0][0]
        most_common_name = self.class_names[most_common_id]
        
        # Rata-rata keyakinan
        avg_confidence = np.mean(list(self.confidence_history))
        
        return most_common_name, avg_confidence
    
    def run(self, show_fps: bool = True, min_confidence: float = 0.7):
        """
        Jalankan loop deteksi real-time.
        
        Args:
            show_fps: Tampilkan counter FPS di layar.
            min_confidence: Ambang keyakinan minimum untuk menampilkan prediksi.
        """
        print("\n" + "="*60)
        print(f"Deteksi Real-time {self.language.upper()}")
        print("="*60)
        print("\nInstruksi:")
        print("- Posisikan tangan di depan kamera")
        print("- Bentuk isyarat huruf")
        print("- Prediksi ditampilkan jika keyakinan > {:.0%}".format(min_confidence))
        print("- Tekan 'q' untuk keluar")
        print("- Tekan 'r' untuk reset riwayat")
        print("="*60 + "\n")
        
        import time
        frame_count = 0
        start_time = time.time()
        
        while True:
            # Baca frame dari kamera
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            # Balikkan frame secara horizontal (efek selfie)
            frame = cv2.flip(frame, 1)
            
            # Ekstrak landmark tangan
            landmarks, detected = self.extractor.extract_landmarks(frame)
            
            # Salin frame asli untuk menggambar
            frame_with_landmarks = self.extractor.draw_landmarks_on_image(frame)
            
            if detected and landmarks is not None:
                # Lakukan prediksi
                class_name, confidence = self.predict_from_landmarks(landmarks)
                smoothed_name, smoothed_conf = self.get_smoothed_prediction()
                
                # Gambar kotak pembatas tangan
                bbox = self.extractor.get_hand_bounding_box(frame)
                if bbox:
                    x_min, y_min, x_max, y_max = bbox
                    cv2.rectangle(frame_with_landmarks, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                
                # Tampilkan prediksi saat ini
                cv2.putText(frame_with_landmarks, f"Current: {class_name} ({confidence:.1%})",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                
                # Tampilkan prediksi yang dikonfirmasi (jika keyakinan cukup tinggi)
                if smoothed_conf >= min_confidence:
                    cv2.putText(frame_with_landmarks, f"Confirmed: {smoothed_name} ({smoothed_conf:.1%})",
                                (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    
                    # Cetak juga ke konsol saat pertama kali dikonfirmasi
                    if len(self.prediction_history) == 1:
                        print(f"  → {smoothed_name} ({smoothed_conf:.1%})")
            
            else:
                # Tampilkan pesan jika tidak ada tangan terdeteksi
                cv2.putText(frame_with_landmarks, "No hand detected",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Tampilkan counter FPS
            if show_fps:
                frame_count += 1
                elapsed = time.time() - start_time
                if elapsed > 0:
                    fps = frame_count / elapsed
                    fps_text = f"FPS: {fps:.1f}"
                    # Teks di pojok kanan atas
                    cv2.putText(frame_with_landmarks, fps_text,
                                (frame_with_landmarks.shape[1] - 150, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # Teks instruksi tombol
            cv2.putText(frame_with_landmarks, "Q=quit, R=reset",
                        (10, frame_with_landmarks.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            
            # Tampilkan frame hasil
            cv2.imshow(f"Real-time Detection - {self.language.upper()}", frame_with_landmarks)
            
            # Tangani penekanan tombol
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                # Reset riwayat untuk menghapus prediksi yang terjebak
                self.prediction_history.clear()
                self.confidence_history.clear()
                print("  [Reset history]")
    
    def release(self):
        """Lepaskan sumber daya kamera dan MediaPipe."""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        if hasattr(self, 'extractor'):
            self.extractor.release()
        cv2.destroyAllWindows()


def main():
    print("\n" + "="*60)
    print("PHASE 5: REAL-TIME SIGN LANGUAGE DETECTION")
    print("="*60)
    
    # Masukan pengguna untuk memilih bahasa isyarat
    language = input("\nBahasa isyarat? (sibi/bisindo): ").strip().lower()
    if language not in ["sibi", "bisindo"]:
        language = "sibi"
    
    # Tentukan path file model
    model_path = f"d:/yuda/models/random_forest_{language}.pkl"
    
    # Periksa apakah model tersedia
    if not Path(model_path).exists():
        print(f"\n✗ Model tidak ditemukan: {model_path}")
        print("Latih model terlebih dahulu dengan: python src/phase4_model_training/stage1_random_forest.py")
        return
    
    detector = None
    
    try:
        # Buat instansi detektor
        detector = RealtimeSignLanguageDetector(model_path, language=language)
        
        # Jalankan loop deteksi utama
        detector.run(min_confidence=0.5)
    
    except Exception as e:
        logger.error(f"Error saat menjalankan program utama: {e}")
    
    finally:
        # Pastikan sumber daya dilepaskan meskipun terjadi error
        if detector:
            detector.release()
        print("\nDeteksi dihentikan.")


if __name__ == "__main__":
    main()
