# ============================================================
# src/phase2_dataset/record_dataset.py
# Record dataset images menggunakan kamera
# ============================================================

import sys
from pathlib import Path
import cv2
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils import MediaPipeHandExtractor, DatasetManager


class DatasetRecorder:
    """
    Record dataset SIBI/BISINDO menggunakan kamera.
    """
    
    def __init__(self, dataset_root: str, language: str = "sibi"):
        """
        Args:
            dataset_root: Root path dataset
            language: 'sibi' atau 'bisindo'
        """
        self.dataset_root = Path(dataset_root)
        self.language = language
        self.base_path = self.dataset_root / language
        self.extractor = MediaPipeHandExtractor()
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            raise RuntimeError("Tidak bisa membuka kamera!")
    
    def record_letter(self, letter: str, num_images: int = 100):
        """
        Record images untuk satu huruf.
        
        Args:
            letter: Huruf yang akan direcord (A, B, C, dll)
            num_images: Jumlah images yang akan direcord
        """
        letter_path = self.base_path / letter
        
        if not letter_path.exists():
            print(f"✗ Folder tidak ditemukan: {letter_path}")
            print(f"Jalankan dataset_preparation.py terlebih dahulu")
            return
        
        # Count existing images
        existing_images = len(list(letter_path.glob('*.jpg')))
        
        print(f"\n{'='*60}")
        print(f"Recording letter: {letter.upper()}")
        print(f"Language: {self.language.upper()}")
        print(f"Existing images: {existing_images}")
        print(f"Target: {num_images} images")
        print(f"{'='*60}")
        print("\nInstructions:")
        print("1. Position hand in front of camera")
        print("2. Make the letter shape")
        print("3. Press SPACE to capture")
        print("4. Press 'q' to finish this letter")
        print("5. Vary hand position, angle, and lighting\n")
        
        count = 0
        
        while count < num_images:
            ret, frame = self.cap.read()
            
            if not ret:
                break
            
            # Flip frame for selfie view
            frame = cv2.flip(frame, 1)
            
            # Draw landmarks
            frame_with_landmarks = self.extractor.draw_landmarks_on_image(frame)
            
            # Add status text
            status_text = f"Recording {letter.upper()}: {count}/{num_images}"
            cv2.putText(frame_with_landmarks, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame_with_landmarks, "SPACE=capture, Q=next", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)
            
            cv2.imshow(f"Recording - {letter.upper()}", frame_with_landmarks)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord(' '):
                # Check if hand is detected
                _, detected = self.extractor.extract_landmarks(frame)
                
                if detected:
                    # Save image
                    filename = f"{letter}_{existing_images + count + 1:04d}.jpg"
                    filepath = letter_path / filename
                    cv2.imwrite(str(filepath), frame)
                    count += 1
                    print(f"  ✓ Captured: {filename}")
                else:
                    print("  ✗ Hand not detected! Try again.")
        
        print(f"\n✓ Finished recording {letter.upper()}. Total: {count} new images\n")
    
    def record_all_letters(self, num_images_per_letter: int = 100):
        """
        Record semua huruf A-Z.
        """
        letters = [chr(ord('A') + i) for i in range(26)]
        
        print(f"\n{'='*60}")
        print(f"Recording all letters for {self.language.upper()}")
        print(f"{'='*60}")
        print(f"Total: {len(letters)} letters x {num_images_per_letter} images = {len(letters) * num_images_per_letter} images")
        print(f"Estimated time: {(len(letters) * num_images_per_letter) / 60:.1f} minutes\n")
        
        for letter in letters:
            self.record_letter(letter, num_images_per_letter)
            
            # Ask if user wants to continue
            print("\nPress ENTER to continue, or type 'q' to quit:")
            user_input = input().strip().lower()
            if user_input == 'q':
                break
        
        print(f"\n{'='*60}")
        print("Recording finished!")
        print("Next: Run verify_dataset_quality.py to check dataset")
        print(f"{'='*60}\n")
    
    def release(self):
        """Close camera and resources."""
        self.cap.release()
        self.extractor.release()
        cv2.destroyAllWindows()


def main():
    print("\n" + "="*60)
    print("DATASET RECORDING TOOL")
    print("="*60)
    print("\nOptions:")
    print("1. Record single letter")
    print("2. Record all letters (A-Z)")
    print("3. Record SIBI or BISINDO?")
    
    choice = input("\nEnter option (1-3): ").strip()
    
    if choice == "3":
        lang = input("Choose language (sibi/bisindo): ").strip().lower()
        if lang not in ["sibi", "bisindo"]:
            lang = "sibi"
    else:
        lang = "sibi"
    
    recorder = DatasetRecorder("d:/yuda/dataset", language=lang)
    
    try:
        if choice == "1":
            letter = input("Enter letter to record (A-Z): ").strip().upper()
            num = int(input("Number of images (default 100): ") or "100")
            recorder.record_letter(letter, num)
        
        elif choice == "2":
            num = int(input("Images per letter (default 100): ") or "100")
            recorder.record_all_letters(num)
        
        else:
            print("Invalid option")
    
    finally:
        recorder.release()


if __name__ == "__main__":
    main()
