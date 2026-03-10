# src/workflow_as_list/security/blacklist.py
"""Blacklist management - dangerous pattern detection.

REFERENCE: docs/design/security/005-layers.md — Layer 2: Blacklist check
"""


def check_blacklist(content: str, blacklist: list[str]) -> tuple[bool, list[str]]:
    """Check if content contains any blacklisted substrings.

    WHY: Prevent dangerous patterns (e.g., shell injection, file deletion).
    """
    matches = []
    for pattern in blacklist:
        if pattern in content:
            matches.append(pattern)

    if matches:
        return False, matches
    return True, []
