#!/usr/bin/env python3
# scripts/check-code-quality.py
"""Code quality checker for workflow-as-list.

Checks:
- Source file line count (max 256 lines)
- Suggests refactoring when files grow too large

REFERENCE: docs/v0.1.1-plan.md — Evolutionary architecture
"""

import sys
from pathlib import Path

# Configuration
MAX_LINES = 256
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}
EXCLUDE_FILES = {
    "__init__.py",  # Package init files can be exceptions
}


def count_lines(file_path: Path) -> tuple[int, int, int]:
    """Count total, code, and blank lines.

    Returns: (total, code, blank)
    """
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    total = len(lines)
    blank = sum(1 for line in lines if not line.strip())
    code = total - blank

    return total, code, blank


def check_file(file_path: Path, max_lines: int = MAX_LINES) -> tuple[bool, str]:
    """Check if file exceeds line limit.

    Returns: (passed, message)
    """
    if file_path.suffix != ".py":
        return True, "Not a Python file"

    if file_path.name in EXCLUDE_FILES:
        return True, f"Excluded file: {file_path.name}"

    total, code, blank = count_lines(file_path)

    if total > max_lines:
        message = (
            f"[WARN] {file_path.relative_to(file_path.parent.parent)}: "
            f"{total} lines (max {max_lines})\n"
            f"  Code: {code}, Blank: {blank}\n"
            f"  Suggestion: Consider splitting into modules"
        )
        return False, message

    return True, f"[OK] {file_path.name}: {total} lines"


def check_directory(
    root: Path, max_lines: int = MAX_LINES, recursive: bool = True
) -> tuple[list[str], list[str]]:
    """Check all Python files in directory.

    Returns: (passed_files, failed_files)
    """
    passed = []
    failed = []

    if recursive:
        py_files = list(root.rglob("*.py"))
    else:
        py_files = list(root.glob("*.py"))

    for file_path in py_files:
        # Skip excluded directories
        if any(excl in file_path.parts for excl in EXCLUDE_DIRS):
            continue

        ok, message = check_file(file_path, max_lines)
        if ok:
            passed.append(message)
        else:
            failed.append(message)

    return passed, failed


def main():
    """Run code quality checks."""
    if len(sys.argv) < 2:
        print("Usage: check-code-quality.py <directory> [--max-lines N]")
        print("  Default max lines: 256")
        sys.exit(1)

    root = Path(sys.argv[1])
    max_lines = MAX_LINES

    # Parse optional --max-lines argument
    if "--max-lines" in sys.argv:
        idx = sys.argv.index("--max-lines")
        if idx + 1 < len(sys.argv):
            max_lines = int(sys.argv[idx + 1])

    if not root.exists():
        print(f"Error: Directory not found: {root}")
        sys.exit(1)

    print(f"Checking Python files in {root}/")
    print(f"Max lines per file: {max_lines}")
    print("-" * 60)

    passed, failed = check_directory(root, max_lines)

    # Print results
    if passed:
        print("\nPassed files:")
        for msg in passed:
            print(f"  {msg}")

    if failed:
        print("\nFiles exceeding limit:")
        for msg in failed:
            print(f"  {msg}")

        print("\n" + "=" * 60)
        print("Refactoring suggestions:")
        print("  1. Group related functions into submodules")
        print("  2. Move classes to separate files")
        print("  3. Extract constants to constants.py")
        print("  4. Use __init__.py for package navigation")
        print("=" * 60)

    # Summary
    print(f"\nSummary: {len(passed)} passed, {len(failed)} failed")

    if failed:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
