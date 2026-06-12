# ============================================================
# src/phase4_model_training/stage1_random_forest.py
# PHASE 4 STAGE 1: Latih Random Forest pada static letters
# ============================================================

import sys
from pathlib import Path
import numpy as np
import pickle
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils import ModelEvaluator, ModelSaver


class RandomForestTrainer:
    """
    Latih Random Forest model untuk deteksi huruf statis.
    """
    
    def __init__(self, landmarks_file: str):
        """
        Args:
            landmarks_file: Path ke file pickle berisi landmarks
        """
        self.landmarks_file = Path(landmarks_file)
        self.model = None
        self.scaler = StandardScaler()
        self.class_names = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_landmarks(self) -> bool:
        """Load landmarks dari file pickle."""
        try:
            with open(self.landmarks_file, 'rb') as f:
                data = pickle.load(f)
            
            X = np.array(data['landmarks'])
            y = np.array(data['labels'])
            self.class_names = data['class_names']
            
            logger.info(f"Loaded {len(X)} landmarks with {len(self.class_names)} classes")
            
            # Split data
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Normalize
            self.X_train = self.scaler.fit_transform(self.X_train)
            self.X_test = self.scaler.transform(self.X_test)
            
            logger.info(f"Train size: {len(self.X_train)}, Test size: {len(self.X_test)}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error loading landmarks: {e}")
            return False
    
    def train(self, n_estimators: int = 100, max_depth: int = 20, random_state: int = 42):
        """
        Latih Random Forest model.
        
        Args:
            n_estimators: Jumlah trees dalam forest
            max_depth: Max depth per tree
            random_state: Random seed
        """
        logger.info(f"Training Random Forest ({n_estimators} trees, max_depth={max_depth})...")
        
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,
            verbose=1
        )
        
        self.model.fit(self.X_train, self.y_train)
        
        logger.info("Training complete!")
    
    def evaluate(self) -> dict:
        """Evaluate model pada test set."""
        logger.info("Evaluating model...")
        
        y_pred = self.model.predict(self.X_test)
        metrics = ModelEvaluator.evaluate(self.y_test, y_pred, self.class_names)
        
        ModelEvaluator.print_metrics(metrics, self.class_names)
        
        return metrics
    
    def save_model(self, output_path: str = "d:/yuda/models/random_forest_sibi.pkl"):
        """Simpan model."""
        if self.model is None:
            logger.error("Model belum dilatih!")
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model
        with open(output_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        # Save scaler
        scaler_path = output_path.parent / f"{output_path.stem}_scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save class names
        classes_path = output_path.parent / f"{output_path.stem}_classes.json"
        with open(classes_path, 'w') as f:
            json.dump(self.class_names, f)
        
        logger.info(f"Model saved to {output_path}")
        logger.info(f"Scaler saved to {scaler_path}")
        logger.info(f"Classes saved to {classes_path}")
    
    def predict(self, landmarks: np.ndarray, return_confidence: bool = False):
        """
        Prediksi label untuk landmarks.
        
        Args:
            landmarks: Array (63,)
            return_confidence: Return confidence scores?
        
        Returns:
            prediction: Predicted class index
            confidence: Confidence score (optional)
        """
        if self.model is None:
            raise RuntimeError("Model belum dilatih!")
        
        # Normalize
        landmarks_normalized = self.scaler.transform([landmarks])
        
        # Predict
        prediction = self.model.predict(landmarks_normalized)[0]
        
        if return_confidence:
            # Get probability
            probabilities = self.model.predict_proba(landmarks_normalized)[0]
            confidence = probabilities[prediction]
            return prediction, confidence
        else:
            return prediction


def main():
    print("\n" + "="*60)
    print("PHASE 4 - STAGE 1: RANDOM FOREST TRAINING")
    print("="*60)
    
    # Choose language
    language = input("\nTrain model for which language? (sibi/bisindo): ").strip().lower()
    if language not in ["sibi", "bisindo"]:
        language = "sibi"
    
    landmarks_file = f"d:/yuda/data/landmarks_{language}.pkl"
    
    # Check if file exists
    if not Path(landmarks_file).exists():
        print(f"\n✗ Landmarks file not found: {landmarks_file}")
        print(f"Run: python src/phase3_feature_extraction/extract_landmarks.py first")
        return
    
    # Create trainer
    trainer = RandomForestTrainer(landmarks_file)
    
    # Load landmarks
    print(f"\nLoading landmarks from {landmarks_file}...")
    if not trainer.load_landmarks():
        print("✗ Failed to load landmarks")
        return
    
    # Train model
    print(f"\nTraining Random Forest model...")
    trainer.train(n_estimators=100, max_depth=20)
    
    # Evaluate
    print(f"\nEvaluating model...")
    metrics = trainer.evaluate()
    
    # Save model
    output_path = f"d:/yuda/models/random_forest_{language}.pkl"
    print(f"\nSaving model to {output_path}...")
    trainer.save_model(output_path)
    
    print(f"\n{'='*60}")
    print("Training complete!")
    print(f"\nNext steps:")
    print(f"1. Run Phase 4 Stage 2 (CNN + Transfer Learning)")
    print(f"2. Or skip to Phase 5 (Real-time Integration) to test this model")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
