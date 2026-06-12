# ============================================================
# utils/mediapipe_extractor.py
# Modul untuk ekstraksi fitur menggunakan MediaPipe
# ============================================================

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class MediaPipeHandExtractor:
    """
    Ekstrak 21 landmark tangan (63 koordinat x,y,z) menggunakan MediaPipe.
    Ini adalah fitur input untuk model ML/DL.
    """
    
    def __init__(self, max_num_hands: int = 1, min_detection_confidence: float = 0.7):
        """
        Args:
            max_num_hands: Jumlah maksimal tangan yang dideteksi
            min_detection_confidence: Confidence threshold untuk deteksi tangan
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def extract_landmarks(self, image: np.ndarray) -> Tuple[Optional[np.ndarray], bool]:
        """
        Ekstrak 21 landmark dari frame gambar.
        
        Returns:
            landmarks: Array bentuk (63,) berisi [x1,y1,z1, x2,y2,z2, ..., x21,y21,z21]
            success: Boolean, True jika tangan terdeteksi
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 0:
            landmarks = []
            for landmark in results.multi_hand_landmarks[0].landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            return np.array(landmarks, dtype=np.float32), True
        else:
            return None, False
    
    def draw_landmarks_on_image(self, image: np.ndarray, landmarks: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Gambar 21 landmark di atas frame (untuk visualisasi).
        
        Args:
            image: Frame gambar (BGR)
            landmarks: Array (63,) atau None untuk deteksi otomatis
            
        Returns:
            image_with_landmarks: Frame dengan landmark digambar
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image_bgr,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        return image_bgr
    
    def get_hand_bounding_box(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Dapatkan bounding box tangan: (x_min, y_min, x_max, y_max)
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0].landmark
            x_coords = [lm.x * w for lm in landmarks]
            y_coords = [lm.y * h for lm in landmarks]
            
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))
            
            # Tambah padding
            padding = 20
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(w, x_max + padding)
            y_max = min(h, y_max + padding)
            
            return (x_min, y_min, x_max, y_max)
        
        return None
    
    def release(self):
        """Tutup MediaPipe resources."""
        self.hands.close()


class VideoProcessor:
    """
    Memproses video dari kamera atau file untuk ekstraksi landmark.
    """
    
    def __init__(self, source: int = 0, frame_width: int = 640, frame_height: int = 480):
        """
        Args:
            source: Camera index (0 = default camera) atau path file video
            frame_width: Lebar frame
            frame_height: Tinggi frame
        """
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Tidak bisa membuka video source: {source}")
        
        self.extractor = MediaPipeHandExtractor()
    
    def get_frame(self) -> Tuple[bool, Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Ambil frame berikutnya dan ekstrak landmark.
        
        Returns:
            success: Boolean
            frame: Frame BGR original
            landmarks: Array (63,) atau None
        """
        ret, frame = self.cap.read()
        
        if not ret:
            return False, None, None
        
        landmarks, detected = self.extractor.extract_landmarks(frame)
        
        if detected:
            return True, frame, landmarks
        else:
            return True, frame, None
    
    def release(self):
        """Tutup video capture."""
        self.cap.release()
        self.extractor.release()


if __name__ == "__main__":
    # Test ekstraksi
    print("Testing MediaPipe Hand Extractor...")
    extractor = MediaPipeHandExtractor()
    processor = VideoProcessor(source=0)
    
    print("Tekan 'q' untuk keluar...")
    while True:
        ret, frame, landmarks = processor.get_frame()
        
        if not ret:
            break
        
        # Gambar landmark
        frame_with_landmarks = extractor.draw_landmarks_on_image(frame)
        
        if landmarks is not None:
            cv2.putText(frame_with_landmarks, f"Tangan terdeteksi! Landmarks: {len(landmarks)//3}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame_with_landmarks, "Tangan tidak terdeteksi", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow("MediaPipe Hand Detection", frame_with_landmarks)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    processor.release()
    cv2.destroyAllWindows()
