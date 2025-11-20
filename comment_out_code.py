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
    """Main function to comment out all BSEE batch processing code"""
    print("🔧 Commenting out BSEE batch processing code...")

    batch_dir = Path("./sdwsdwdwdawdrgrgrg/bsee/batch/")

    if not batch_dir.exists():
        print(f"❌ Batch directory not found: {batch_dir}")
        return

    # Get all Python files in batch directory
    python_files = list(batch_dir.glob("*.py"))

    if not python_files:
        print("❌ No Python files found in batch directory")
        return

    print(f"📁 Found {len(python_files)} Python files to process...")

    success_count = 0
    for py_file in python_files:
        if comment_out_python_file(py_file):
            success_count += 1

    print(f"✅ Successfully processed {success_count}/{len(python_files)} files")
    print("🚫 BSEE batch processing functionality has been disabled")
    print("📝 Code structure preserved for future reactivation")

if __name__ == "__main__":
    main()