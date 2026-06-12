# ============================================================
# src/phase1_setup/verify_environment.py
# Verifikasi bahwa semua dependencies terinstall dengan benar
# ============================================================

import sys
import importlib
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def check_package(package_name: str, import_name: str = None) -> bool:
    """Check apakah package terinstall."""
    if import_name is None:
        import_name = package_name
    
    try:
        mod = importlib.import_module(import_name)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✓ {package_name:20s} - {version}")
        return True
    except ImportError:
        print(f"✗ {package_name:20s} - NOT INSTALLED")
        return False


def main():
    print("\n" + "="*60)
    print("ENVIRONMENT VERIFICATION")
    print("="*60)
    print("Checking installed packages...\n")
    
    packages = [
        ("OpenCV", "cv2"),
        ("MediaPipe", "mediapipe"),
        ("NumPy", "numpy"),
        ("Pandas", "pandas"),
        ("Scikit-Learn", "sklearn"),
        ("TensorFlow", "tensorflow"),
        ("Keras", "keras"),
        ("Matplotlib", "matplotlib"),
        ("Pillow", "PIL"),
    ]
    
    results = []
    for package_name, import_name in packages:
        result = check_package(package_name, import_name)
        results.append(result)
    
    print("\n" + "="*60)
    
    if all(results):
        print("✓ Semua packages terinstall dengan benar!")
        print("\nLangkah berikutnya:")
        print("1. Organisir dataset SIBI/BISINDO di folder 'dataset/'")
        print("2. Run phase2_dataset_preparation.py")
        print("="*60 + "\n")
        return True
    else:
        failed = [pkg[0] for pkg, res in zip(packages, results) if not res]
        print(f"✗ Packages yang belum terinstall: {', '.join(failed)}")
        print("\nJalankan:")
        print("  pip install -r requirements.txt")
        print("="*60 + "\n")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
