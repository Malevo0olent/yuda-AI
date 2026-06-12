#!/usr/bin/env python
import shutil
import os
from pathlib import Path

source_root = Path("C:/Users/ASUS/ai_env/data")
dest_root = Path("d:/yuda/dataset/sibi")

# Get all folders A-Z
letters = [chr(i) for i in range(65, 91)]  # A-Z in ASCII

print("Copying data from C:\\Users\\ASUS\\ai_env\\data to d:\\yuda\\dataset\\sibi\n")

for letter in letters:
    source_folder = source_root / letter
    dest_folder = dest_root / letter
    
    if source_folder.exists():
        try:
            if dest_folder.exists():
                shutil.rmtree(dest_folder)
            shutil.copytree(source_folder, dest_folder)
            num_files = len(list(dest_folder.glob("**/*.jpg")))
            print(f"✓ {letter}: {num_files} files copied")
        except Exception as e:
            print(f"✗ {letter}: Error - {e}")
    else:
        print(f"✗ {letter}: Source folder not found")

print("\n✓ All data copied successfully!")
