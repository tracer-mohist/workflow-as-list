# src/workflow_as_list/executor/loader.py
"""Workflow loader - expands imports with caching.

REFERENCE: #40 - Import caching mechanism for human-readable workflow files

Design:
- import: URL/path → fetch and cache to .imports/
- Add annotation: # you see: <cache-path> <sha256:hash>
- Cache persists across executions
- Hash verification detects content changes

Usage:
    loader = WorkflowLoader(base_path)
    expanded = loader.load(workflow_path)
"""

import hashlib
import re
from pathlib import Path

IMPORTS_DIR = Path(".imports")


class WorkflowLoader:
    """Load and expand workflow imports with caching."""

    def __init__(self, base_path: Path):
        """Initialize loader with project base path.

        Args:
            base_path: Project root directory
        """
        self.base_path = base_path
        self.imports_dir = base_path / IMPORTS_DIR
        self.imports_dir.mkdir(exist_ok=True)

    def load(self, workflow_path: Path, cache: bool = True) -> str:
        """Load workflow file with imports expanded.

        Args:
            workflow_path: Path to workflow file
            cache: Whether to cache expanded content

        Returns:
            Expanded workflow content
        """
        content = workflow_path.read_text()
        expanded = self._expand_imports(content, workflow_path.parent)

        if cache:
            # Save to cache and add annotation
            cache_path = self.get_cache_path(str(workflow_path), self.base_path)
            cache_path.write_text(expanded)

            # Compute hash and create annotation
            hash_value = self.compute_hash(expanded)
            rel_cache_path = cache_path.relative_to(self.base_path)

            # Check if annotation already exists
            if not self._has_cache_annotation(content, str(rel_cache_path)):
                # Add annotation to source file
                annotated = self._add_annotation_to_content(
                    content, workflow_path, rel_cache_path, hash_value
                )
                workflow_path.write_text(annotated)

        return expanded

    def _has_cache_annotation(self, content: str, cache_path: str) -> bool:
        """Check if content already has cache annotation for this path."""
        return f"# you see: {cache_path}" in content

    def _add_annotation_to_content(
        self, content: str, workflow_path: Path, cache_path: Path, hash_value: str
    ) -> str:
        """Add cache annotation BEFORE import line (not after)."""
        lines = content.split("\n")
        output = []
        added = set()  # Track which imports have annotations

        for i, line in enumerate(lines):
            # Check if this is an import line without annotation
            if line.strip().startswith("import:"):
                # Check if next line is already an annotation
                has_annotation = False
                if i + 1 < len(lines) and "# you see:" in lines[i + 1]:
                    has_annotation = True

                if not has_annotation and str(workflow_path) not in added:
                    # Add annotation BEFORE import line
                    annotation = f"# you see: <{cache_path}> <{hash_value}>"
                    output.append(annotation)
                    added.add(str(workflow_path))

            output.append(line)

        return "\n".join(output)

    def _expand_imports(self, content: str, base_path: Path) -> str:
        """Recursively expand imports in content.

        Args:
            content: Workflow content
            base_path: Base path for resolving relative imports

        Returns:
            Expanded content with cache annotations
        """
        lines = content.split("\n")
        output = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("import:"):
                # Preserve original import line as comment
                output.append(f"# {line}")

                # Extract import path/URL
                import_path = stripped.split("import:", 1)[1].strip()

                # Fetch and expand imported content
                imported_content = self._fetch_import(import_path, base_path)

                # Recursively expand nested imports
                expanded = self._expand_imports(imported_content, base_path)

                # Add boundary markers
                output.append(f"# === START: Imported from {import_path} ===")
                output.extend(expanded.split("\n"))
                output.append("# === END: Imported ===")
            else:
                output.append(line)

        return "\n".join(output)

    def _fetch_import(self, import_path: str, base_path: Path) -> str:
        """Fetch import content (local file or remote URL).

        Args:
            import_path: Path or URL to import
            base_path: Base path for resolving relative paths

        Returns:
            Imported content
        """
        if import_path.startswith(("http://", "https://")):
            return self._fetch_remote(import_path)
        else:
            return self._fetch_local(import_path, base_path)

    def _fetch_local(self, path: str, base_path: Path) -> str:
        """Fetch local file import.

        Args:
            path: Relative or absolute path
            base_path: Base path for resolving relative paths

        Returns:
            File content
        """
        if Path(path).is_absolute():
            file_path = Path(path)
        else:
            file_path = base_path / path

        if not file_path.exists():
            raise FileNotFoundError(f"Import not found: {file_path}")

        return file_path.read_text()

    def _fetch_remote(self, url: str) -> str:
        """Fetch remote URL import."""
        import urllib.request

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return response.read().decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch {url}: {e}") from e

    def compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content.

        Args:
            content: Content to hash

        Returns:
            SHA-256 hash in format "sha256:<hex>"
        """
        hash_value = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"sha256:{hash_value}"

    def get_cache_path(self, import_path: str, base_path: Path) -> Path:
        """Get cache file path for an import.

        Args:
            import_path: Original import path/URL
            base_path: Base path for resolving relative paths

        Returns:
            Cache file path in .imports/ directory
        """
        if import_path.startswith(("http://", "https://")):
            # URL: create path from URL structure
            # https://raw.githubusercontent.com/user/repo/main/file.workflow.list
            # → .imports/raw.githubusercontent.com/user/repo/main/file.workflow.list
            url_parts = (
                import_path.replace("https://", "").replace("http://", "").split("/")
            )
            cache_path = self.imports_dir / "/".join(url_parts)
        else:
            # Local path: preserve relative structure
            if Path(import_path).is_absolute():
                rel_path = Path(import_path).relative_to(base_path)
            else:
                rel_path = Path(import_path)
            cache_path = self.imports_dir / rel_path

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        return cache_path

    def validate_cache_annotation(self, annotation: str) -> tuple[str, str] | None:
        """Validate cache annotation format: # you see: <path> <algo:hash>."""
        pattern = r"# you see: ([\w./-]+) <(sha256|md5):([a-f0-9]+)>"
        match = re.match(pattern, annotation.strip())
        if not match:
            return None
        cache_path, algo, hash_value = match.groups()
        if ".." in cache_path:
            return None  # Security: prevent directory traversal
        if not cache_path.startswith(".imports/") and cache_path != ".imports":
            return None  # Security: must be under .imports/
        return (cache_path, f"{algo}:{hash_value}")
