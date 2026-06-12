# ============================================================
# utils/model_utils.py
# Utilitas untuk training dan evaluasi model
# ============================================================

import numpy as np
import pickle
from pathlib import Path
from typing import Tuple
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import json
import logging

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """
    Evaluasi performa model.
    """
    
    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray, class_names: list = None) -> dict:
        """
        Hitung metrics evaluasi.
        
        Returns:
            dict dengan accuracy, precision, recall, f1, confusion_matrix, dll
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
            'f1': f1_score(y_true, y_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
        }
        
        if class_names:
            report = classification_report(y_true, y_pred, target_names=class_names, zero_division=0, output_dict=True)
            metrics['classification_report'] = report
        
        return metrics
    
    @staticmethod
    def print_metrics(metrics: dict, class_names: list = None):
        """
        Print metrics ke console.
        """
        print("\n" + "="*60)
        print("MODEL EVALUATION RESULTS")
        print("="*60)
        print(f"Accuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1-Score:  {metrics['f1']:.4f}")
        
        if 'classification_report' in metrics and class_names:
            print("\nClassification Report:")
            print("-"*60)
            for class_name in class_names:
                if class_name in metrics['classification_report']:
                    report = metrics['classification_report'][class_name]
                    print(f"{class_name:5s} - Precision: {report['precision']:.4f}, "
                          f"Recall: {report['recall']:.4f}, F1: {report['f1-score']:.4f}")
        
        print("="*60 + "\n")


class ModelSaver:
    """
    Simpan dan load model.
    """
    
    @staticmethod
    def save_sklearn_model(model, filepath: str, metadata: dict = None):
        """
        Simpan model sklearn (Random Forest, SVM, dll).
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        
        # Simpan metadata jika ada
        if metadata:
            metadata_path = filepath.replace('.pkl', '_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {filepath}")
    
    @staticmethod
    def load_sklearn_model(filepath: str):
        """
        Load model sklearn.
        """
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        
        logger.info(f"Model loaded from {filepath}")
        return model
    
    @staticmethod
    def save_keras_model(model, filepath: str):
        """
        Simpan Keras/TensorFlow model.
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        model.save(filepath)
        logger.info(f"Model saved to {filepath}")
    
    @staticmethod
    def load_keras_model(filepath: str):
        """
        Load Keras/TensorFlow model.
        """
        from tensorflow import keras
        model = keras.models.load_model(filepath)
        logger.info(f"Model loaded from {filepath}")
        return model


class PredictionFormatter:
    """
    Format hasil prediksi untuk output.
    """
    
    @staticmethod
    def format_output(prediction: int, class_names: list, confidence: float = None) -> str:
        """
        Format prediksi ke string yang readable.
        
        Args:
            prediction: Index kelas
            class_names: List nama kelas
            confidence: Confidence score (0-1)
        
        Returns:
            Formatted string
        """
        class_name = class_names[prediction] if prediction < len(class_names) else "Unknown"
        
        if confidence:
            return f"{class_name} ({confidence:.2%})"
        else:
            return class_name
    
    @staticmethod
    def format_multiple_predictions(predictions: list, class_names: list, confidences: list = None) -> str:
        """
        Format multiple predictions (untuk sequence/LSTM).
        """
        result = []
        
        for i, pred in enumerate(predictions):
            conf = confidences[i] if confidences else None
            result.append(PredictionFormatter.format_output(pred, class_names, conf))
        
        return " ".join(result)


if __name__ == "__main__":
    # Test
    print("Testing ModelEvaluator...")
    y_true = np.array([0, 0, 1, 1, 2, 2])
    y_pred = np.array([0, 0, 1, 2, 2, 2])
    
    metrics = ModelEvaluator.evaluate(y_true, y_pred, class_names=['A', 'B', 'C'])
    ModelEvaluator.print_metrics(metrics, class_names=['A', 'B', 'C'])
