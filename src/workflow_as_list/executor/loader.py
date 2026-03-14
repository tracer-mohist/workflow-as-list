# src/workflow_as_list/executor/loader.py
"""Workflow loader - expands imports with per-import caching.

REFERENCE: #40 - Import caching mechanism for human-readable workflow files

Design:
- Each import: URL/path → cached independently to .imports/<name>
- Each import line gets annotation: # you see: <cache-path> <sha256:hash>
- Annotation points to the IMPORT's cache, not parent file
- Users can directly open cache file to read imported content

Usage:
    loader = WorkflowLoader(base_path)
    expanded = loader.load(workflow_path)
"""

import hashlib
import re
from pathlib import Path

IMPORTS_DIR = Path(".imports")


class WorkflowLoader:
    """Load and expand workflow imports with per-import caching."""

    def __init__(self, base_path: Path):
        """Initialize loader with project base path."""
        self.base_path = base_path
        self.imports_dir = base_path / IMPORTS_DIR
        self.imports_dir.mkdir(exist_ok=True)

    def load(self, workflow_path: Path, cache: bool = True) -> str:
        """Load workflow file with imports expanded.

        Args:
            workflow_path: Path to workflow file
            cache: Whether to cache imported content

        Returns:
            Expanded workflow content
        """
        content = workflow_path.read_text()
        expanded = self._expand_imports(content, workflow_path.parent, cache)

        if cache:
            # Add annotations to source file
            self._add_annotations_to_source(workflow_path, content)

        return expanded

    def _add_annotations_to_source(self, workflow_path: Path, content: str) -> None:
        """Add cache annotations to source file for each import.

        Only adds annotation if it doesn't already exist in the source file.
        """
        lines = content.split("\n")
        output = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith("import:"):
                # Check if previous line is already an annotation for this import
                has_annotation = False
                if i > 0 and "# you see:" in lines[i - 1]:
                    has_annotation = True

                if not has_annotation:
                    import_path = stripped.split("import:", 1)[1].strip()

                    # Fetch and cache this import
                    imported_content = self._fetch_import(
                        import_path, workflow_path.parent
                    )
                    expanded = self._expand_imports(
                        imported_content, workflow_path.parent, False
                    )

                    cache_path = self._get_import_cache_path(
                        import_path, workflow_path.parent
                    )
                    cache_path.write_text(expanded)

                    hash_value = self.compute_hash(expanded)
                    rel_cache_path = cache_path.relative_to(self.base_path)

                    # Create annotation with explicit "project root" prefix in path
                    indent = len(line) - len(line.lstrip())
                    annotation = (
                        " " * indent
                        + f"# you see: <project root:{rel_cache_path}> <{hash_value}>"
                    )
                    output.append(annotation)

            output.append(line)

        # Write back to source file
        workflow_path.write_text("\n".join(output))

    def _expand_imports(self, content: str, base_path: Path, cache: bool = True) -> str:
        """Recursively expand imports with per-import caching.

        Each import is cached independently and annotated.
        """
        lines = content.split("\n")
        output = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("import:"):
                # Extract import path/URL
                import_path = stripped.split("import:", 1)[1].strip()

                # Fetch imported content
                imported_content = self._fetch_import(import_path, base_path)

                # Recursively expand nested imports
                expanded = self._expand_imports(imported_content, base_path, cache)

                if cache:
                    # Cache this import independently
                    cache_path = self._get_import_cache_path(import_path, base_path)
                    cache_path.write_text(expanded)

                    # Compute hash for this import
                    hash_value = self.compute_hash(expanded)

                    # Get relative cache path for annotation
                    rel_cache_path = cache_path.relative_to(self.base_path)

                    # Add annotation BEFORE import line (with matching indent)
                    indent = len(line) - len(line.lstrip())
                    annotation = (
                        " " * indent
                        + f"# you see: <project root:{rel_cache_path}> <{hash_value}>"
                    )
                    output.append(annotation)

                # Preserve original import as comment
                output.append(f"# {line}")

                # Add boundary markers with expanded content
                output.append(f"# === START: Imported from {import_path} ===")
                output.extend(expanded.split("\n"))
                output.append("# === END: Imported ===")
            else:
                output.append(line)

        return "\n".join(output)

    def _fetch_import(self, import_path: str, base_path: Path) -> str:
        """Fetch import content (local file or remote URL)."""
        if import_path.startswith(("http://", "https://")):
            return self._fetch_remote(import_path)
        else:
            return self._fetch_local(import_path, base_path)

    def _fetch_local(self, path: str, base_path: Path) -> str:
        """Fetch local file import."""
        file_path = Path(path) if Path(path).is_absolute() else base_path / path
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

    def _get_import_cache_path(self, import_path: str, base_path: Path) -> Path:
        """Get cache file path using hash-only naming (security + flat structure).

        Design:
        - Cache files named by content hash only (no original filename)
        - Prevents path traversal and injection attacks
        - Flat structure (no deep directories)
        - Deduplication: same content = same cache file
        - User reads import line for source, cache filename is internal
        """
        # Fetch content to compute hash
        imported_content = self._fetch_import(import_path, base_path)
        content_hash = hashlib.sha256(imported_content.encode("utf-8")).hexdigest()[:16]

        # Format: <hash-prefix>.workflow.list (no original filename for security)
        cache_filename = f"{content_hash}.workflow.list"
        cache_path = self.imports_dir / cache_filename

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        return cache_path

    def compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content."""
        hash_value = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return f"sha256:{hash_value}"

    def validate_cache_annotation(self, annotation: str) -> tuple[str, str] | None:
        """Validate cache annotation format: # you see: <project root:path> <algo:hash>."""
        pattern = r"# you see: <project root:([\w./-]+)> <(sha256|md5):([a-f0-9]+)>"
        match = re.match(pattern, annotation.strip())
        if not match:
            return None
        cache_path, algo, hash_value = match.groups()
        if ".." in cache_path:
            return None  # Security: prevent directory traversal
        if not cache_path.startswith(".imports/") and cache_path != ".imports":
            return None  # Security: must be under .imports/
        return (cache_path, f"{algo}:{hash_value}")
