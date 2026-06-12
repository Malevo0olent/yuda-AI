# ============================================================
# src/phase2_dataset/dataset_preparation.py
# Organisir dan validasi dataset SIBI/BISINDO
# ============================================================

import sys
from pathlib import Path
import cv2
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils import DatasetManager


class DatasetPreparer:
    """
    Siapkan dan validasi dataset.
    """
    
    def __init__(self, dataset_root: str = "dataset"):
        self.manager = DatasetManager(dataset_root)
    
    def create_sibi_structure(self):
        """Buat struktur folder untuk SIBI (26 huruf A-Z)."""
        print("\n" + "="*60)
        print("Creating SIBI folder structure...")
        print("="*60)
        
        letters = [chr(ord('A') + i) for i in range(26)]
        self.manager.create_directory_structure(letters=letters, language="sibi")
        
        print(f"✓ Created folders for {len(letters)} SIBI letters")
    
    def create_bisindo_structure(self):
        """Buat struktur folder untuk BISINDO (26 huruf A-Z)."""
        print("\n" + "="*60)
        print("Creating BISINDO folder structure...")
        print("="*60)
        
        letters = [chr(ord('A') + i) for i in range(26)]
        self.manager.create_directory_structure(letters=letters, language="bisindo")
        
        print(f"✓ Created folders for {len(letters)} BISINDO letters")
    
    def show_dataset_info(self, language: str = "sibi"):
        """Tampilkan informasi dataset."""
        print(f"\n{'='*60}")
        print(f"Dataset Information: {language.upper()}")
        print(f"{'='*60}")
        self.manager.print_dataset_info(language=language)
    
    def validate_dataset_quality(self, language: str = "sibi", min_images_per_class: int = 10):
        """
        Validasi kualitas dataset.
        """
        print(f"\n{'='*60}")
        print(f"Dataset Validation: {language.upper()}")
        print(f"{'='*60}")
        
        base_path = Path(self.manager.dataset_root) / language
        
        if not base_path.exists():
            print(f"✗ Dataset folder tidak ditemukan: {base_path}")
            return False
        
        classes = self.manager.get_class_list(language=language)
        
        if not classes:
            print(f"✗ Tidak ada class folders di {language}")
            return False
        
        print(f"\nValidating {len(classes)} classes...\n")
        
        issues = []
        
        for class_name in classes:
            class_path = base_path / class_name
            
            # Count images
            image_files = list(class_path.glob('*.jpg')) + list(class_path.glob('*.png')) + list(class_path.glob('*.jpeg'))
            
            # Check image count
            if len(image_files) < min_images_per_class:
                msg = f"✗ {class_name:5s} - {len(image_files)} images (minimum: {min_images_per_class})"
                print(msg)
                issues.append(class_name)
            else:
                print(f"✓ {class_name:5s} - {len(image_files)} images")
            
            # Validate image format
            for img_file in image_files[:3]:  # Check first 3 images only
                try:
                    img = cv2.imread(str(img_file))
                    if img is None:
                        print(f"  ✗ Invalid image format: {img_file.name}")
                        issues.append(str(img_file))
                except Exception as e:
                    print(f"  ✗ Error reading {img_file.name}: {e}")
                    issues.append(str(img_file))
        
        print(f"\n{'='*60}")
        if issues:
            print(f"✗ Found {len(issues)} issues!")
            print("Fix these before training:")
            for issue in issues[:5]:  # Show first 5
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
            print(f"{'='*60}\n")
            return False
        else:
            print("✓ Dataset validation passed!")
            print(f"{'='*60}\n")
            return True


class DatasetDownloadGuide:
    """
    Panduan download dataset publik.
    """
    
    @staticmethod
    def print_download_guide():
        """Print panduan download dataset."""
        print("\n" + "="*60)
        print("DATASET DOWNLOAD GUIDE")
        print("="*60)
        print("""
OPTION 1: Kaggle Datasets
------------------------
1. Visit: https://www.kaggle.com
2. Search: "sign language", "SIBI", "BISINDO"
3. Download dataset
4. Extract ke folder: dataset/sibi/ atau dataset/bisindo/

OPTION 2: Roboflow Universe
---------------------------
1. Visit: https://universe.roboflow.com
2. Search: "sign language"
3. Download as images
4. Extract ke folder: dataset/sibi/ atau dataset/bisindo/

OPTION 3: Create Your Own Dataset
----------------------------------
1. Run: python src/phase2_dataset/record_dataset.py
2. Follow on-screen instructions
3. Record 50-100 images per letter
4. Ensure variations in:
   - Hand position (left, center, right)
   - Lighting (bright, normal, dim)
   - Background (clean, cluttered, varied)
   - Hand angle (front, side, rotated)

TIPS:
-----
- Start with SIBI first (more similar to Latin alphabet)
- Each letter should have 100-500+ images
- Ensure good lighting and clear hand visibility
- Use consistent camera angle and distance
""")
        print("="*60 + "\n")


def main():
    preparer = DatasetPreparer(dataset_root="d:/yuda/dataset")
    
    print("\n" + "="*70)
    print("PHASE 2: DATASET PREPARATION")
    print("="*70)
    
    # Create folder structures
    preparer.create_sibi_structure()
    preparer.create_bisindo_structure()
    
    # Show info
    preparer.show_dataset_info("sibi")
    preparer.show_dataset_info("bisindo")
    
    # Print download guide
    DatasetDownloadGuide.print_download_guide()
    
    # Validate
    print("\nNext steps:")
    print("1. Download or record dataset images")
    print("2. Organize images into class folders (A/, B/, etc.)")
    print("3. Run: python src/phase2_dataset/record_dataset.py (for custom recording)")
    print("4. Run: python verify_dataset_quality.py (to validate)")
    print("\nThen proceed to Phase 3: Feature Extraction")


if __name__ == "__main__":
    main()
