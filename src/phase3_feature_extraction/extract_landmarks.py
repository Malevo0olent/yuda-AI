# ============================================================
# src/phase3_feature_extraction/extract_landmarks.py
# Ekstrak 21 hand landmarks menggunakan MediaPipe
# ============================================================

import sys
from pathlib import Path
import cv2
import numpy as np
import pickle
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils import MediaPipeHandExtractor, DatasetManager


class LandmarkExtractor:
    """
    Ekstrak landmarks dari images di dataset.
    """
    
    def __init__(self, dataset_root: str):
        self.dataset_root = Path(dataset_root)
        self.extractor = MediaPipeHandExtractor()
        self.manager = DatasetManager(str(self.dataset_root))
    
    def extract_from_images(self, language: str = "sibi") -> tuple:
        """
        Ekstrak landmarks dari semua images di dataset.
        
        Args:
            language: 'sibi' atau 'bisindo'
        
        Returns:
            landmarks: List of np.ndarray (63,)
            labels: List of int (class index)
            class_names: List of str (class names)
        """
        base_path = self.dataset_root / language
        
        if not base_path.exists():
            logger.error(f"Dataset path tidak ditemukan: {base_path}")
            return None, None, None
        
        classes = sorted([d.name for d in base_path.iterdir() if d.is_dir()])
        
        if not classes:
            logger.error(f"Tidak ada class folders di {base_path}")
            return None, None, None
        
        logger.info(f"Found {len(classes)} classes: {', '.join(classes)}")
        
        all_landmarks = []
        all_labels = []
        skipped = 0
        extracted = 0
        
        for class_idx, class_name in enumerate(classes):
            class_path = base_path / class_name
            image_files = sorted(list(class_path.glob('*.jpg')) + list(class_path.glob('*.png')))
            
            logger.info(f"Extracting landmarks from {class_name} ({len(image_files)} images)...")
            
            for img_file in tqdm(image_files, desc=class_name):
                try:
                    img = cv2.imread(str(img_file))
                    
                    if img is None:
                        skipped += 1
                        continue
                    
                    landmarks, detected = self.extractor.extract_landmarks(img)
                    
                    if detected and landmarks is not None:
                        all_landmarks.append(landmarks)
                        all_labels.append(class_idx)
                        extracted += 1
                    else:
                        skipped += 1
                
                except Exception as e:
                    logger.warning(f"Error processing {img_file}: {e}")
                    skipped += 1
        
        logger.info(f"\nExtraction complete!")
        logger.info(f"Extracted: {extracted}, Skipped: {skipped}")
        
        return all_landmarks, all_labels, classes
    
    def save_landmarks(self, landmarks: list, labels: list, class_names: list, output_path: str):
        """
        Simpan landmarks ke file pickle.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'landmarks': landmarks,
            'labels': labels,
            'class_names': class_names,
        }
        
        with open(output_path, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Landmarks saved to {output_path}")
    
    def release(self):
        self.extractor.release()


def main():
    print("\n" + "="*60)
    print("PHASE 3: LANDMARK EXTRACTION")
    print("="*60)
    
    # Choose language
    language = input("\nExtract landmarks for which language? (sibi/bisindo): ").strip().lower()
    if language not in ["sibi", "bisindo"]:
        language = "sibi"
    
    print(f"\nStarting landmark extraction for {language.upper()}...")
    
    extractor = LandmarkExtractor("d:/yuda/dataset")
    
    try:
        # Extract landmarks
        landmarks, labels, class_names = extractor.extract_from_images(language)
        
        if landmarks is None:
            print("✗ Extraction failed!")
            return
        
        # Save landmarks
        output_file = f"d:/yuda/data/landmarks_{language}.pkl"
        extractor.save_landmarks(landmarks, labels, class_names, output_file)
        
        # Print statistics
        print(f"\n{'='*60}")
        print(f"Extraction Statistics:")
        print(f"{'='*60}")
        print(f"Language: {language.upper()}")
        print(f"Total landmarks: {len(landmarks)}")
        print(f"Total classes: {len(class_names)}")
        print(f"Classes: {', '.join(class_names)}")
        print(f"\nClass distribution:")
        
        unique_labels = np.unique(labels)
        for class_idx, class_name in enumerate(class_names):
            count = np.sum(np.array(labels) == class_idx)
            print(f"  {class_name}: {count} landmarks")
        
        print(f"\nOutput file: {output_file}")
        print(f"\nNext steps:")
        print(f"1. Run Phase 4 to train models using these landmarks")
        print(f"{'='*60}\n")
    
    finally:
        extractor.release()


if __name__ == "__main__":
    main()
