#!/usr/bin/env python3
"""
Script to fix common syntax errors in Python files
"""

import ast
import re
from pathlib import Path
from typing import List, Dict, Any

class SyntaxErrorFixer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.fixed_files = []

    def fix_file(self, file_path: Path) -> bool:
        """Fix syntax errors in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Apply fixes
            fixed_content = self._apply_fixes(original_content)

            # Check if fixes actually fixed the syntax
            try:
                ast.parse(fixed_content)
                # If successful, write back the fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"✅ Fixed: {file_path.relative_to(self.project_root)}")
                self.fixed_files.append(file_path)
                return True
            except SyntaxError as e:
                print(f"❌ Still broken: {file_path.relative_to(self.project_root)} - Line {e.lineno}: {e.msg}")
                return False

        except Exception as e:
            print(f"⚠️ Error processing {file_path}: {e}")
            return False

    def _apply_fixes(self, content: str) -> str:
        """Apply common syntax fixes"""
        # Fix 1: Remove extra quotes at end of lines ("""" pattern)
        content = re.sub(r'""""$', '"', content, flags=re.MULTILINE)

        # Fix 2: Remove extra quotes before parentheses (""""")
        content = re.sub(r'""""\)', '")', content)

        # Fix 3: Fix malformed function calls with extra quotes
        content = re.sub(r'\)""', ')', content)

        # Fix 4: Fix malformed string concatenation with extra quotes
        content = re.sub(r'""""\s*\n', '"\n', content)

        # Fix 5: Fix extra quotes in function arguments
        content = re.sub(r'(\w+)""(\s*\()', r'\1\2', content)

        # Fix 6: Fix extra quotes after method calls
        content = re.sub(r'(\))""\s*$', r')', content, flags=re.MULTILINE)

        # Fix 7: Fix malformed dictionary/list syntax
        content = re.sub(r'{""', '{', content)
        content = re.compile(r'([^:]+):""([^"]*)""').sub(r'\1: "\2"', content)

        # Fix 8: Fix unmatched brackets/braces in common patterns
        # Fix malformed ttk.Label calls
        content = re.sub(r'(ttk\.Label\([^,]+, [^,]+,"""([^"]+)""",?)', r'\1"', content)
        content = re.sub(r',?(\s*\)))', r'\1', content)

        # Fix 9: Fix malformed filedialog.askopenfilename calls
        content = re.sub(r'(filedialog\.askopenfilename\([^)]*)""(\s*\))', r'\1\2', content)

        # Fix 10: General cleanup of quote patterns
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Remove trailing quotes followed immediately by newlines
            line = re.sub(r'""$', '', line)
            # Fix quotes before method calls
            line = re.sub(r'""(\.)', r'\1', line)
            # Fix extra quotes in string literals
            line = re.sub(r'""([^"]*)""', r'"\1"', line)
            lines[i] = line

        content = '\n'.join(lines)

        return content

    def fix_all_files(self) -> List[Path]:
        """Fix all Python files with syntax errors"""
        print("🔧 Fixing syntax errors in Python files...")

        # Find all Python files with syntax errors
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)

        print(f"📁 Checking {len(python_files)} Python files...")

        syntax_error_files = []
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
            except SyntaxError:
                syntax_error_files.append(file_path)
            except UnicodeDecodeError:
                continue

        print(f"❌ Found {len(syntax_error_files)} files with syntax errors")

        # Fix each file
        fixed_count = 0
        for file_path in syntax_error_files:
            if self.fix_file(file_path):
                fixed_count += 1

        print(f"✅ Fixed {fixed_count}/{len(syntax_error_files)} files")
        return self.fixed_files


def main():
    """Main function"""
    import os
    print("🚀 BSEE Syntax Error Fixer")
    print("=" * 40)

    fixer = SyntaxErrorFixer(".")
    fixed_files = fixer.fix_all_files()

    if fixed_files:
        print(f"\n✅ Successfully fixed {len(fixed_files)} files!")
        return 0
    else:
        print(f"\n❌ No files were fixed.")
        return 1


if __name__ == "__main__":
    import sys
    import os
    sys.exit(main())