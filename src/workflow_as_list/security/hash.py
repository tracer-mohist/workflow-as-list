# src/workflow_as_list/security/hash.py
"""Hash computation - SHA256 for workflow immutability.

REFERENCE: docs/design/security/005-layers.md — Hash for immutability check
"""

import hashlib
from pathlib import Path


def compute_hash(file_path: Path) -> str:
    """Compute SHA256 hash of workflow file.

    WHY: Immutability check during execution.
    """
    content = file_path.read_bytes()
    return hashlib.sha256(content).hexdigest()
