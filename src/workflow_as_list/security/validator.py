# src/workflow_as_list/security/validator.py
"""Input validators - encoding, syntax, token length checks.

REFERENCE: docs/design/security/005-layers.md
- Layer 1: Encoding check
- Layer 3: Token length check (design guidance)
- Layer 4: Feature scan
"""


def check_encoding(content: str) -> tuple[bool, str | None]:
    """Check if content is ASCII-only.

    Why: Maximum encoding compatibility across platforms and agents.
    """
    try:
        content.encode("ascii")
        return True, None
    except UnicodeEncodeError as e:
        return (
            False,
            f"Non-ASCII character at position {e.start}: {repr(e.object[e.start : e.end])}",
        )


def check_token_length(
    content: str, lower_bound: int = 282, upper_bound: int = 358
) -> tuple[bool, int, str | None]:
    """Check token length and provide design guidance.

    Why: Optimal cognitive load for agent execution.
    Note: Token count = byte count for ASCII content.

    Returns:
        (is_valid, token_count, suggestion)

        is_valid: True if task can proceed (warnings allowed)
        token_count: Byte count of content
        suggestion: Non-empty if guidance needed

    Guidance cases:
        - Below lower_bound: Warning (optional improvement)
          Suggestion: Add constraints, preconditions, or outcomes

        - Above upper_bound: Error (required action)
          Suggestion: Apply Divide and Conquer strategy
    """
    token_count = len(content.encode("utf-8"))

    if token_count > upper_bound:
        return (
            False,
            token_count,
            (
                "Token count exceeds recommended maximum.\n"
                "Why: Complex descriptions increase execution ambiguity.\n"
                "Required: Apply Divide and Conquer strategy.\n"
                "Pattern: One parent task + multiple focused subtasks."
            ),
        )

    if token_count < lower_bound:
        return (
            True,
            token_count,
            (
                "Token count below recommended minimum.\n"
                "Why: Brief descriptions may lack context for reliable execution.\n"
                "Optional: Consider adding constraints, preconditions, or outcomes.\n"
                "Note: Ignore if task is intentionally simple."
            ),
        )

    return True, token_count, None


def check_features(content: str) -> tuple[bool, list[str]]:
    """Scan for workflow features and validate syntax patterns.

    Checks:
    - Line format (content, nested content, tags, jumps, imports)
    - Tag format: (tag)
    - Jump format: @tag[N]: condition?
    - Import format: import: path

    Why: Ensure workflow follows 5-rule syntax before execution.
    """
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        # Skip empty lines
        if not line.strip():
            continue

        # Check for valid line patterns
        stripped = line.lstrip()

        # Tag pattern: (tag) at start
        if stripped.startswith("("):
            if ")" not in stripped[:20]:  # Reasonable tag length limit
                issues.append(f"Line {i}: Malformed tag - missing closing parenthesis")

        # Jump pattern: @tag[N]
        if "@" in stripped:
            idx = stripped.index("@")
            rest = stripped[idx:]
            if ":" not in rest:
                issues.append(f"Line {i}: Jump missing condition separator ':'")
            if "[" in rest and "]" not in rest.split(":")[0]:
                issues.append(f"Line {i}: Jump limit malformed - missing ']'")

        # Import pattern
        if stripped.startswith("import:"):
            parts = stripped.split("import:")
            if len(parts) != 2 or not parts[1].strip():
                issues.append(f"Line {i}: Import missing path")

    if issues:
        return False, issues
    return True, []


def check_whitelist(
    content: str, whitelist: list[str], enabled: bool = False
) -> tuple[bool, str | None]:
    """Check if content matches whitelist (if enabled).

    Why: Additional security layer for high-trust workflows.
    Note: Opt-in only. Empty whitelist + enabled = reject all.
    """
    if not enabled:
        return True, None  # Skip if not enabled

    if not whitelist:
        return False, "Whitelist enabled but empty - all content rejected"

    # Check if content contains at least one whitelisted pattern
    for pattern in whitelist:
        if pattern in content:
            return True, None

    return False, "Content does not match any whitelisted pattern"
