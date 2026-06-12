# ============================================================
# utils/data_utils.py
# Utilitas untuk manajemen dataset dan preprocessing
# ============================================================

import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Tuple, Dict
import pickle
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class DatasetManager:
    """
    Kelola dataset SIBI/BISINDO.
    """
    
    def __init__(self, dataset_root: str):
        """
        Args:
            dataset_root: Path root dataset (d:\yuda\dataset)
        """
        self.dataset_root = Path(dataset_root)
        self.sibi_path = self.dataset_root / "sibi"
        self.bisindo_path = self.dataset_root / "bisindo"
    
    def create_directory_structure(self, letters: List[str] = None, language: str = "sibi"):
        """
        Buat struktur folder untuk huruf-huruf.
        
        Args:
            letters: List of letters (default: A-Z)
            language: 'sibi' atau 'bisindo'
        """
        if letters is None:
            letters = [chr(ord('A') + i) for i in range(26)]
        
        base_path = self.sibi_path if language == "sibi" else self.bisindo_path
        base_path.mkdir(parents=True, exist_ok=True)
        
        for letter in letters:
            letter_path = base_path / letter
            letter_path.mkdir(exist_ok=True)
            logger.info(f"Created folder: {letter_path}")
    
    def get_class_list(self, language: str = "sibi") -> List[str]:
        """
        Dapatkan list kelas (huruf) yang tersedia.
        """
        base_path = self.sibi_path if language == "sibi" else self.bisindo_path
        
        if not base_path.exists():
            return []
        
        classes = sorted([d.name for d in base_path.iterdir() if d.is_dir()])
        return classes
    
    def get_dataset_stats(self, language: str = "sibi") -> Dict:
        """
        Hitung statistik dataset.
        """
        base_path = self.sibi_path if language == "sibi" else self.bisindo_path
        stats = {}
        total_images = 0
        
        classes = self.get_class_list(language)
        
        for class_name in classes:
            class_path = base_path / class_name
            num_images = len([f for f in class_path.iterdir() if f.suffix.lower() in ['.jpg', '.png', '.jpeg']])
            stats[class_name] = num_images
            total_images += num_images
        
        return {
            'total_images': total_images,
            'num_classes': len(classes),
            'class_distribution': stats
        }
    
    def print_dataset_info(self, language: str = "sibi"):
        """
        Print informasi dataset.
        """
        stats = self.get_dataset_stats(language)
        print(f"\n{'='*50}")
        print(f"Dataset Info: {language.upper()}")
        print(f"{'='*50}")
        print(f"Total images: {stats['total_images']}")
        print(f"Number of classes: {stats['num_classes']}")
        print(f"\nClass Distribution:")
        for cls, count in stats['class_distribution'].items():
            print(f"  {cls}: {count} images")
        print(f"{'='*50}\n")


class LandmarkDataLoader:
    """
    Load dan preprocess landmark data untuk training.
    """
    
    def __init__(self, landmarks_file: str = None):
        """
        Args:
            landmarks_file: Path ke file pickle berisi landmarks yang sudah diekstrak
        """
        self.landmarks_file = landmarks_file
        self.scaler = StandardScaler()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_landmarks(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load landmarks dari file pickle.
        
        Returns:
            X: Array (n_samples, 63)
            y: Array (n_samples,) - label index
        """
        if self.landmarks_file is None:
            raise ValueError("landmarks_file tidak ditetapkan")
        
        with open(self.landmarks_file, 'rb') as f:
            data = pickle.load(f)
        
        X = np.array(data['landmarks'])
        y = np.array(data['labels'])
        
        logger.info(f"Loaded {len(X)} landmarks dengan {len(np.unique(y))} classes")
        
        return X, y
    
    def save_landmarks(self, landmarks: List[np.ndarray], labels: List[int], output_file: str):
        """
        Simpan landmarks ke file pickle.
        """
        data = {
            'landmarks': landmarks,
            'labels': labels
        }
        
        with open(output_file, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Saved {len(landmarks)} landmarks to {output_file}")
    
    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42):
        """
        Split data ke training dan testing sets.
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Train size: {len(self.X_train)}, Test size: {len(self.X_test)}")
    
    def normalize_data(self):
        """
        Normalize landmarks menggunakan StandardScaler.
        """
        if self.X_train is None:
            raise ValueError("Data tidak di-split terlebih dahulu")
        
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        logger.info("Data normalized")
    
    def get_train_test_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Dapatkan training dan testing data.
        """
        return self.X_train, self.X_test, self.y_train, self.y_test


class ImageDataLoader:
    """
    Load images langsung dari dataset folder untuk CNN training.
    """
    
    def __init__(self, dataset_path: str, target_size: Tuple[int, int] = (224, 224)):
        """
        Args:
            dataset_path: Path ke dataset folder (sibi/ atau bisindo/)
            target_size: Target size untuk resize images
        """
        self.dataset_path = Path(dataset_path)
        self.target_size = target_size
        self.classes = []
        self.class_to_idx = {}
    
    def load_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load semua images dari dataset.
        
        Returns:
            X: Array (n_samples, height, width, 3)
            y: Array (n_samples,) - label index
        """
        images = []
        labels = []
        
        # Get all class folders
        class_folders = sorted([d for d in self.dataset_path.iterdir() if d.is_dir()])
        
        for idx, class_folder in enumerate(class_folders):
            self.classes.append(class_folder.name)
            self.class_to_idx[class_folder.name] = idx
            
            # Load images dari class folder
            image_files = list(class_folder.glob('*.jpg')) + list(class_folder.glob('*.png'))
            
            for img_file in image_files:
                try:
                    img = cv2.imread(str(img_file))
                    if img is not None:
                        img = cv2.resize(img, self.target_size)
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = img / 255.0  # Normalisasi ke [0, 1]
                        images.append(img)
                        labels.append(idx)
                except Exception as e:
                    logger.warning(f"Error loading {img_file}: {e}")
        
        logger.info(f"Loaded {len(images)} images dari {len(self.classes)} classes")
        
        return np.array(images), np.array(labels)
    
    def split_data(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
        """Split data ke train dan test sets."""
        return train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)


if __name__ == "__main__":
    # Test DatasetManager
    print("Testing DatasetManager...")
    manager = DatasetManager("d:/yuda/dataset")
    
    # Create directory structure
    manager.create_directory_structure(language="sibi")
    
    # Print dataset info
    manager.print_dataset_info(language="sibi")
