#!/usr/bin/env python3
# scripts/check-docs-quality.py
"""Documentation quality checker for workflow-as-list.

Enforces 6-layer prompt engineering framework:
- No markdown tables
- No ** emphasis syntax
- No emoji in content
- README.md < 200 lines

REFERENCE: docs/prompt-engineering/README.md
"""

import sys
from pathlib import Path


def check_file_lines(path: Path, max_lines: int = 200) -> tuple[bool, int]:
    """Check if file has fewer than max_lines."""
    if not path.exists():
        return True, 0  # Skip non-existent files

    content = path.read_text()
    line_count = len(content.split("\n"))
    return line_count <= max_lines, line_count


def check_no_tables(path: Path) -> tuple[bool, int]:
    """Check if file contains markdown tables (|...|)."""
    if not path.exists():
        return True, 0

    content = path.read_text()
    table_lines = sum(
        1
        for line in content.split("\n")
        if "|" in line and line.strip().startswith("|")
    )
    return table_lines == 0, table_lines


def check_no_emphasis_stars(path: Path) -> tuple[bool, int]:
    """Check if file contains ** emphasis syntax."""
    if not path.exists():
        return True, 0

    content = path.read_text()
    count = content.count("**")
    return count == 0, count


def check_no_emoji(path: Path) -> tuple[bool, list[str]]:
    """Check if file contains emoji characters."""
    if not path.exists():
        return True, []

    content = path.read_text()
    # Basic emoji range check (common emoji Unicode ranges)
    emoji_ranges = [
        (0x1F600, 0x1F64F),  # Emoticons
        (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
        (0x1F680, 0x1F6FF),  # Transport and Map
        (0x1F1E0, 0x1F1FF),  # Flags
        (0x2600, 0x26FF),  # Misc symbols
        (0x2700, 0x27BF),  # Dingbats
    ]

    found_emoji = []
    for char in content:
        code = ord(char)
        for start, end in emoji_ranges:
            if start <= code <= end:
                found_emoji.append(char)
                break

    return len(found_emoji) == 0, found_emoji


def main():
    """Run all documentation quality checks."""
    if len(sys.argv) < 2:
        print("Usage: check-docs-quality.py <project-root>")
        sys.exit(1)

    project_root = Path(sys.argv[1])
    docs_to_check = [
        project_root / "README.md",
        project_root / "AGENTS.md",
        project_root / "CONTRIBUTING.md",
    ]

    errors = []
    warnings = []

    for doc_path in docs_to_check:
        if not doc_path.exists():
            warnings.append(f"[WARN] File not found: {doc_path.name}")
            continue

        # Check line count (README only, max 200 lines)
        if doc_path.name == "README.md":
            passed, count = check_file_lines(doc_path, max_lines=200)
            if not passed:
                errors.append(f"[ERROR] {doc_path.name} has {count} lines (max 200)")

        # Check for tables
        passed, count = check_no_tables(doc_path)
        if not passed:
            errors.append(
                f"[ERROR] {doc_path.name} contains {count} table lines (should be 0)"
            )

        # Check for ** emphasis
        passed, count = check_no_emphasis_stars(doc_path)
        if not passed:
            errors.append(
                f"[ERROR] {doc_path.name} contains ** syntax {count} times (should be 0)"
            )

        # Check for emoji
        passed, found = check_no_emoji(doc_path)
        if not passed:
            errors.append(f"[ERROR] {doc_path.name} contains emoji: {found}")

    # Print results
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  {warning}")
        print()

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  {error}")
        print()
        print(f"FAILED: {len(errors)} error(s) found")
        sys.exit(1)
    else:
        print("All documentation quality checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
