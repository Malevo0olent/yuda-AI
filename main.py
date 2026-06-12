# ============================================================
# main.py
# Main entry point untuk project
# ============================================================

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_banner():
    banner = """
╔════════════════════════════════════════════════════════════════╗
║         🤟 AI DETEKSI BAHASA ISYARAT BISINDO & SIBI 🤟        ║
║                 Sign Language Recognition System              ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    menu = """
PILIH FASE/AKTIVITAS:

┌─ PHASE 1: Setup Environment
│
├─1. Verify environment (check dependencies)
│
├─────────────────────────────────────────────────
│
├─ PHASE 2: Dataset Preparation
│
├─2. Setup dataset folder structure
├─3. Record dataset via kamera
│
├─────────────────────────────────────────────────
│
├─ PHASE 3: Feature Extraction
│
├─4. Extract hand landmarks dari images
│
├─────────────────────────────────────────────────
│
├─ PHASE 4: Model Training
│
├─5. Train Random Forest model (Stage 1)
├─6. (Soon) Train CNN + Transfer Learning (Stage 2)
├─7. (Soon) Train LSTM model (Stage 3)
│
├─────────────────────────────────────────────────
│
├─ PHASE 5: Real-time Integration
│
├─8. Run real-time sign language detection
│
├─────────────────────────────────────────────────
│
├─ UTILITIES
│
├─9. Show configuration
├─10. View dataset info
└─0. Exit

    """
    print(menu)


def run_script(script_path: str):
    """Run a Python script."""
    if not Path(script_path).exists():
        print(f"\n✗ Script not found: {script_path}")
        return
    
    print(f"\nRunning: {script_path}\n")
    os.system(f"python {script_path}")


def show_config():
    """Show configuration."""
    from config import print_config
    print_config()


def show_dataset_info():
    """Show dataset information."""
    import sys
    sys.path.insert(0, str(project_root))
    from utils import DatasetManager
    
    manager = DatasetManager(str(project_root / "dataset"))
    
    print("\n" + "="*60)
    print("DATASET INFORMATION")
    print("="*60)
    
    # SIBI
    print("\n[SIBI Dataset]")
    try:
        stats = manager.get_dataset_stats("sibi")
        print(f"  Total images: {stats['total_images']}")
        print(f"  Classes: {stats['num_classes']}")
        if stats['total_images'] > 0:
            print(f"  Average per class: {stats['total_images'] // max(1, stats['num_classes'])}")
    except Exception as e:
        print(f"  Error: {e}")
    
    # BISINDO
    print("\n[BISINDO Dataset]")
    try:
        stats = manager.get_dataset_stats("bisindo")
        print(f"  Total images: {stats['total_images']}")
        print(f"  Classes: {stats['num_classes']}")
        if stats['total_images'] > 0:
            print(f"  Average per class: {stats['total_images'] // max(1, stats['num_classes'])}")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\n" + "="*60 + "\n")


def main():
    print_banner()
    
    script_mapping = {
        "1": ("src/phase1_setup/verify_environment.py", "Verifying environment..."),
        "2": ("src/phase2_dataset/dataset_preparation.py", "Setting up dataset folders..."),
        "3": ("src/phase2_dataset/record_dataset.py", "Starting dataset recorder..."),
        "4": ("src/phase3_feature_extraction/extract_landmarks.py", "Extracting landmarks..."),
        "5": ("src/phase4_model_training/stage1_random_forest.py", "Training Random Forest..."),
        "8": ("src/phase5_realtime_integration/realtime_prediction.py", "Starting real-time detection..."),
    }
    
    while True:
        print_menu()
        
        try:
            choice = input("\n➤ Enter choice (0-10): ").strip()
            
            # Skip if empty input
            if not choice:
                continue
            
            if choice == "0":
                print("\n👋 Goodbye!\n")
                break
            
            elif choice == "9":
                show_config()
            
            elif choice == "10":
                show_dataset_info()
            
            elif choice in script_mapping:
                script_path, description = script_mapping[choice]
                print(f"\n{description}")
                run_script(str(project_root / script_path))
            
            else:
                print("\n✗ Invalid choice! Please enter 0-10")
            
            input("\n\nPress ENTER to continue...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            input("Press ENTER to continue...")


if __name__ == "__main__":
    main()
