#!/usr/bin/env python3
"""
Script to comment out all Python code in BSEE batch processing module
This disables functionality while preserving code structure
"""

import os
from pathlib import Path

def comment_out_python_file(file_path):
    """Comment out all lines in a Python file except for existing comments"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        commented_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip empty lines
            if not stripped:
                commented_lines.append(line)
                continue

            # Keep existing comments and docstrings as-is
            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                commented_lines.append(line)
                continue

            # Comment out code lines
            if not stripped.startswith('#'):
                commented_lines.append(f"# DISABLED: {line}")
            else:
                commented_lines.append(line)

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(commented_lines)

        print(f"✓ Commented out: {file_path}")
        return True

    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to comment out all BSEE functionality"""
    print("🔧 Commenting out BSEE functionality...")

    # Define directories to comment out
    bsee_dirs = [
        Path("./bsee/batch/"),
        Path("./bsee/processing/"),
        Path("./bsee/engine/"),
        Path("./bsee/operations/"),
        Path("./bsee/strategies/"),
        Path("./bsee/metrics/"),
        Path("./bsee/scoring/"),
        Path("./bsee/cost/"),
        Path("./bsee/utils/"),
    ]

    all_files = []

    # Collect all Python files from BSEE directories
    for bsee_dir in bsee_dirs:
        if bsee_dir.exists():
            python_files = list(bsee_dir.rglob("*.py"))
            all_files.extend(python_files)
            print(f"📁 Found {len(python_files)} files in {bsee_dir}")

    if not all_files:
        print("❌ No BSEE Python files found")
        return

    print(f"📁 Total BSEE files to process: {len(all_files)}")

    success_count = 0
    for py_file in all_files:
        # Skip __pycache__ and already commented files
        if "__pycache__" in str(py_file):
            continue
        if comment_out_python_file(py_file):
            success_count += 1

    print(f"✅ Successfully processed {success_count}/{len(all_files)} files")
    print("🚫 BSEE functionality has been completely disabled")
    print("📝 Code structure preserved for future reactivation")

if __name__ == "__main__":
    main()