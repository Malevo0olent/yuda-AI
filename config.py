# ============================================================
# config.py
# Centralized configuration untuk project
# ============================================================

from pathlib import Path
import json

# Paths
PROJECT_ROOT = Path(__file__).parent
DATASET_ROOT = PROJECT_ROOT / "dataset"
MODELS_ROOT = PROJECT_ROOT / "models"
DATA_ROOT = PROJECT_ROOT / "data"
UTILS_ROOT = PROJECT_ROOT / "utils"
SRC_ROOT = PROJECT_ROOT / "src"
NOTEBOOKS_ROOT = PROJECT_ROOT / "notebooks"

# Create directories if not exist
for directory in [DATASET_ROOT, MODELS_ROOT, DATA_ROOT]:
    directory.mkdir(exist_ok=True)

# MediaPipe Configuration
MEDIAPIPE_CONFIG = {
    "max_num_hands": 1,
    "min_detection_confidence": 0.7,
    "min_tracking_confidence": 0.5,
    "model_complexity": 1,  # 0 or 1
}

# Camera Configuration
CAMERA_CONFIG = {
    "frame_width": 640,
    "frame_height": 480,
    "fps": 30,
}

# Training Configuration
TRAINING_CONFIG = {
    "random_forest": {
        "n_estimators": 100,
        "max_depth": 20,
        "min_samples_split": 5,
        "min_samples_leaf": 2,
        "random_state": 42,
        "n_jobs": -1,
    },
    "test_size": 0.2,
    "random_state": 42,
}

# Prediction Configuration
PREDICTION_CONFIG = {
    "confidence_threshold": 0.5,
    "history_size": 5,  # For smoothing predictions
}

# Dataset Configuration
DATASET_CONFIG = {
    "sibi": {
        "classes": [chr(ord('A') + i) for i in range(26)],
        "language": "Indonesian Sign Language (SIBI)",
    },
    "bisindo": {
        "classes": [chr(ord('A') + i) for i in range(26)],
        "language": "Indonesian Sign Language (BISINDO)",
    },
}

# Model Paths
MODEL_PATHS = {
    "random_forest_sibi": MODELS_ROOT / "random_forest_sibi.pkl",
    "random_forest_bisindo": MODELS_ROOT / "random_forest_bisindo.pkl",
}

# Data Paths
DATA_PATHS = {
    "landmarks_sibi": DATA_ROOT / "landmarks_sibi.pkl",
    "landmarks_bisindo": DATA_ROOT / "landmarks_bisindo.pkl",
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}


def get_config(section: str = None) -> dict:
    \"\"\"Get configuration dictionary.\"\"\"
    config = {
        "project_root": str(PROJECT_ROOT),
        "dataset_root": str(DATASET_ROOT),
        "models_root": str(MODELS_ROOT),
        "data_root": str(DATA_ROOT),
        "mediapipe": MEDIAPIPE_CONFIG,
        "camera": CAMERA_CONFIG,
        "training": TRAINING_CONFIG,
        "prediction": PREDICTION_CONFIG,
        "dataset": DATASET_CONFIG,
    }
    
    if section and section in config:
        return config[section]
    
    return config


def print_config():
    \"\"\"Print configuration.\"\"\"
    config = get_config()
    print("\\n" + "="*60)
    print("PROJECT CONFIGURATION")
    print("="*60)
    print(json.dumps(config, indent=2, default=str))
    print("="*60 + "\\n")


if __name__ == "__main__":
    print_config()
