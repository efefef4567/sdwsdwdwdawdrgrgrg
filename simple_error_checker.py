#!/usr/bin/env python3
"""
Simple Error Detection Tool
Checks for syntax errors and basic issues in Python files
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Any


class SimpleErrorChecker:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.errors = []

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories and cache
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)

        return python_files

    def check_syntax_errors(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check for syntax errors by parsing AST"""
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try to parse the AST
            ast.parse(content)

        except SyntaxError as e:
            errors.append({
                'file_path': str(file_path.relative_to(self.project_root)),
                'error_type': 'SyntaxError',
                'error_message': f"Line {e.lineno}: {e.msg}",
                'line_number': e.lineno or 0,
                'column': e.offset or 0
            })
        except UnicodeDecodeError as e:
            errors.append({
                'file_path': str(file_path.relative_to(self.project_root)),
                'error_type': 'UnicodeError',
                'error_message': f"Encoding error: {str(e)}",
                'line_number': 0,
                'column': 0
            })
        except Exception as e:
            errors.append({
                'file_path': str(file_path.relative_to(self.project_root)),
                'error_type': 'FileError',
                'error_message': f"Error reading file: {str(e)}",
                'line_number': 0,
                'column': 0
            })

        return errors

    def check_import_errors(self, file_path: Path) -> List[Dict[str, Any]]:
        """Basic import error checking"""
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Check for obvious import issues
            for i, line in enumerate(lines, 1):
                line = line.strip()

                # Check for malformed import statements
                if line.startswith('from ') and 'import' in line:
                    # Check for missing quotes in string imports
                    if "'" not in line and '"' not in line and '.' in line:
                        # Might be a relative import issue
                        if line.count('.') > 3:  # Too many relative levels
                            errors.append({
                                'file_path': str(file_path.relative_to(self.project_root)),
                                'error_type': 'PotentialImportError',
                                'error_message': f"Line {i}: Excessive relative import levels: {line[:50]}...",
                                'line_number': i,
                                'column': 0
                            })

                # Check for BSEE imports that should be disabled
                if 'from bsee.batch import' in line or 'from bsee.engine import' in line:
                    if line.strip().startswith('from bsee.'):
                        errors.append({
                            'file_path': str(file_path.relative_to(self.project_root)),
                            'error_type': 'DisabledImport',
                            'error_message': f"Line {i}: BSEE import found (should be disabled): {line[:50]}...",
                            'line_number': i,
                            'column': 0
                        })

        except Exception as e:
            errors.append({
                'file_path': str(file_path.relative_to(self.project_root)),
                'error_type': 'AnalysisError',
                'error_message': f"Error analyzing imports: {str(e)}",
                'line_number': 0,
                'column': 0
            })

        return errors

    def analyze_project(self) -> List[Dict[str, Any]]:
        """Analyze all Python files in the project"""
        print(f"🔍 Analyzing project at: {self.project_root}")

        # Find all Python files
        python_files = self.find_python_files()
        print(f"📁 Found {len(python_files)} Python files")

        all_errors = []
        analyzed_count = 0

        for file_path in python_files:
            analyzed_count += 1

            # Skip files that are already commented out (contain "DISABLED")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "DISABLED:" in content and content.count("# DISABLED:") > 10:
                        print(f"⏭️  Skipping {analyzed_count}/{len(python_files)}: {file_path.relative_to(self.project_root)} (already disabled)")
                        continue
            except:
                pass

            print(f"🔎 Analyzing {analyzed_count}/{len(python_files)}: {file_path.relative_to(self.project_root)}")

            try:
                file_errors = []

                # Check syntax errors
                syntax_errors = self.check_syntax_errors(file_path)
                file_errors.extend(syntax_errors)

                # Check import errors (only if no syntax errors)
                if not syntax_errors:
                    import_errors = self.check_import_errors(file_path)
                    file_errors.extend(import_errors)

                if file_errors:
                    all_errors.extend(file_errors)
                    print(f"  ❌ Found {len(file_errors)} error(s)")
                    for error in file_errors:
                        print(f"    - {error['error_type']}: {error['error_message']}")
                else:
                    print(f"  ✅ No errors found")

            except Exception as e:
                # Error in the analysis itself
                all_errors.append({
                    'file_path': str(file_path.relative_to(self.project_root)),
                    'error_type': 'AnalysisError',
                    'error_message': f"Error during analysis: {str(e)}",
                    'line_number': 0,
                    'column': 0
                })
                print(f"  ❌ Analysis error: {str(e)}")

        self.errors = all_errors
        print(f"\n📊 Analysis complete. Found {len(all_errors)} total errors across {len(python_files)} files.")

        return all_errors

    def get_error_summary(self) -> Dict[str, int]:
        """Get a summary of error types"""
        summary = {}
        for error in self.errors:
            error_type = error.get('error_type', 'Unknown')
            summary[error_type] = summary.get(error_type, 0) + 1
        return summary


def main():
    """Main function"""
    print("🚀 BSEE Simple Error Detection Tool")
    print("=" * 50)

    checker = SimpleErrorChecker(".")
    errors = checker.analyze_project()

    # Print summary
    summary = checker.get_error_summary()
    print(f"\n📋 Error Summary:")
    for error_type, count in sorted(summary.items()):
        print(f"  {error_type}: {count}")

    if errors:
        print(f"\n❌ Found {len(errors)} total errors that need fixing!")
        return 1
    else:
        print(f"\n✅ No errors found! Project looks good.")
        return 0


if __name__ == "__main__":
    sys.exit(main())