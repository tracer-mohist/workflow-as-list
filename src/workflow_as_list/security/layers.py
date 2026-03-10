# src/workflow_as_list/security/layers.py
"""Security layer checks - 7 independent layers.

Each layer is independent. Layer failure does not crash the system.
Returns detailed error messages for debugging.

REFERENCE: docs/design/security/005-layers.md
"""

from typing import Literal

from ..models import Config
from .blacklist import check_blacklist
from .validator import (
    check_encoding,
    check_features,
    check_token_length,
    check_whitelist,
)


def check_audit_status(
    status: Literal["pending_audit", "approved", "rejected"],
) -> tuple[bool, str | None]:
    """Check if workflow has human approval.

    WHY: Human must review and approve before execution.
    """
    if status == "approved":
        return True, None
    elif status == "rejected":
        return False, "Workflow was rejected by human auditor"
    else:  # pending_audit
        return False, "Workflow pending human audit"


def run_security_checks(
    content: str,
    config: Config,
    audit_status: str = "pending_audit",
    skip_audit_check: bool = False,
) -> tuple[bool, list[str]]:
    """Run all 6 security layers.

    Args:
        content: Workflow file content
        config: Application configuration
        audit_status: Current audit status
        skip_audit_check: Skip Layer 5 (for check command)

    Returns:
        (passed, errors) - passed is True if all checks pass

    NOTE: Layer 7 is TBD (reserved for future extension).
    """
    errors = []

    # Layer 1: Encoding
    passed, error = check_encoding(content)
    if not passed:
        errors.append(f"[Layer 1] {error}")
        return False, errors  # Stop early - non-ASCII breaks everything

    # Layer 2: Blacklist
    passed, matches = check_blacklist(content, config.blacklist)
    if not passed:
        errors.append(f"[Layer 2] Blacklist patterns found: {matches}")

    # Layer 3: Token length
    passed, token_count = check_token_length(
        content, config.token_min, config.token_max
    )
    if not passed:
        assert token_count is not None
        errors.append(
            f"[Layer 3] Token count {token_count} not in range [{config.token_min}, {config.token_max}]"
        )

    # Layer 4: Feature scan
    passed, issues = check_features(content)
    if not passed:
        errors.append(f"[Layer 4] Syntax issues: {issues}")

    # Layer 5: Audit status (skip during check/registration)
    if not skip_audit_check:
        passed, error = check_audit_status(audit_status)  # type: ignore
        if not passed:
            errors.append(f"[Layer 5] {error}")

    # Layer 6: Whitelist (opt-in)
    passed, error = check_whitelist(content, config.whitelist, config.enable_whitelist)
    if not passed:
        errors.append(f"[Layer 6] {error}")

    return len(errors) == 0, errors
