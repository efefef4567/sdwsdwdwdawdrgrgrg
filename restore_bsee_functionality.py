#!/usr/bin/env python3
"""
Script to restore BSEE functionality by uncommenting previously disabled code
"""

import os
import re
from pathlib import Path

class BSEEFunctionalityRestorer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.restored_files = []

    def restore_file(self, file_path: Path) -> bool:
        """Restore functionality by uncommenting disabled code"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if this file was commented out (has many DISABLED lines)
            if "# DISABLED:" not in content or content.count("# DISABLED:") < 5:
                # This wasn't a heavily commented file, skip it
                return False

            original_content = content

            # Restore functionality by removing "# DISABLED: " prefixes
            lines = content.split('\n')
            restored_lines = []

            for line in lines:
                # Remove "# DISABLED: " prefix to restore original code
                if line.strip().startswith('# DISABLED: '):
                    restored_line = line.replace('# DISABLED: ', '', 1)
                    restored_lines.append(restored_line)
                else:
                    restored_lines.append(line)

            restored_content = '\n'.join(restored_lines)

            # Write back the restored content
            if restored_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(restored_content)
                print(f"✅ Restored: {file_path.relative_to(self.project_root)}")
                self.restored_files.append(file_path)
                return True

        except Exception as e:
            print(f"⚠️ Error restoring {file_path}: {e}")

        return False

    def restore_all_bsee_files(self):
        """Restore all BSEE functionality"""
        print("🔄 Restoring BSEE functionality...")

        # Define BSEE directories to restore
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

        print(f"📁 Found {len(all_files)} BSEE files to check")

        restored_count = 0
        for file_path in all_files:
            if self.restore_file(file_path):
                restored_count += 1

        print(f"✅ Successfully restored {restored_count} BSEE files")
        return self.restored_files


def main():
    """Main function"""
    print("🚀 BSEE Functionality Restorer")
    print("=" * 40)

    restorer = BSEEFunctionalityRestorer(".")
    restored_files = restorer.restore_all_bsee_files()

    if restored_files:
        print(f"\n✅ Successfully restored {len(restored_files)} BSEE files!")
        print("🔄 BSEE functionality has been re-enabled!")
        return 0
    else:
        print(f"\n⚠️ No files needed restoration.")
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())