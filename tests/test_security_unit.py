# tests/test_security_unit.py
"""Unit tests for security module.

NOTE: Follows Limited Testing Strategy - test critical logic only.
REFERENCE: docs/limited-testing-strategy.md
REFERENCE: docs/design/security/005-layers.md
"""

import tempfile
from pathlib import Path

from workflow_as_list.security import (
    check_blacklist,
    check_encoding,
    check_features,
    check_token_length,
    check_whitelist,
    compute_hash,
)


class TestCheckEncoding:
    """Layer 1: Encoding check tests."""

    def test_ascii_content_passes(self):
        """Scenario: Content is ASCII-only.
        Expected: Returns (True, None).
        If fails: All ASCII workflows rejected.
        """
        content = "This is ASCII content"
        passed, error = check_encoding(content)
        assert passed is True
        assert error is None

    def test_non_ascii_content_fails(self):
        """Scenario: Content contains non-ASCII characters.
        Expected: Returns (False, error message).
        If fails: Security boundary broken.
        """
        content = "This contains emoji: 😀"
        passed, error = check_encoding(content)
        assert passed is False
        assert error is not None
        assert "Non-ASCII" in error


class TestCheckBlacklist:
    """Layer 2: Blacklist check tests."""

    def test_clean_content_passes(self):
        """Scenario: Content has no blacklisted patterns.
        Expected: Returns (True, []).
        If fails: Clean content rejected.
        """
        content = "Safe workflow content"
        blacklist = ["rm -rf", "sudo"]
        passed, matches = check_blacklist(content, blacklist)
        assert passed is True
        assert matches == []

    def test_blacklisted_content_fails(self):
        """Scenario: Content contains blacklisted pattern.
        Expected: Returns (False, [matched_patterns]).
        If fails: Dangerous patterns allowed.
        """
        content = "This workflow uses rm -rf /tmp"
        blacklist = ["rm -rf", "sudo"]
        passed, matches = check_blacklist(content, blacklist)
        assert passed is False
        assert "rm -rf" in matches


class TestCheckTokenLength:
    """Layer 3: Token length check tests."""

    def test_valid_length_passes(self):
        """Scenario: Content length in valid range [282, 358].
        Expected: Returns (True, token_count).
        If fails: Valid workflows rejected.
        """
        content = "x" * 300  # 300 bytes
        passed, token_count = check_token_length(content, 282, 358)
        assert passed is True
        assert token_count == 300

    def test_too_short_fails(self):
        """Scenario: Content below minimum length.
        Expected: Returns (False, token_count).
        If fails: Under-length workflows accepted.
        """
        content = "x" * 100
        passed, token_count = check_token_length(content, 282, 358)
        assert passed is False
        assert token_count == 100

    def test_too_long_fails(self):
        """Scenario: Content exceeds maximum length.
        Expected: Returns (False, token_count).
        If fails: Over-length workflows accepted.
        """
        content = "x" * 500
        passed, token_count = check_token_length(content, 282, 358)
        assert passed is False
        assert token_count == 500


class TestCheckFeatures:
    """Layer 4: Feature scan tests."""

    def test_valid_workflow_passes(self):
        """Scenario: Workflow follows 5-rule syntax.
        Expected: Returns (True, []).
        If fails: Valid workflows rejected.
        """
        content = """(start) First step
Second step
@start[3]: condition?
import: other.wf"""
        passed, issues = check_features(content)
        assert passed is True
        assert issues == []

    def test_malformed_tag_fails(self):
        """Scenario: Tag missing closing parenthesis.
        Expected: Returns (False, [issue]).
        If fails: Malformed tags accepted.
        """
        content = "(tag without closing First step"
        passed, issues = check_features(content)
        assert passed is False
        assert any("Malformed tag" in issue for issue in issues)

    def test_malformed_jump_fails(self):
        """Scenario: Jump missing colon separator.
        Expected: Returns (False, [issue]).
        If fails: Malformed jumps accepted.
        """
        content = "@tag[3] missing colon"
        passed, issues = check_features(content)
        assert passed is False
        assert any("missing condition separator" in issue for issue in issues)


class TestCheckWhitelist:
    """Layer 6: Whitelist check tests (opt-in)."""

    def test_disabled_whitelist_passes(self):
        """Scenario: Whitelist not enabled.
        Expected: Returns (True, None).
        If fails: Disabled whitelist blocks content.
        """
        content = "Any content"
        passed, error = check_whitelist(content, [], enabled=False)
        assert passed is True
        assert error is None

    def test_empty_whitelist_fails(self):
        """Scenario: Whitelist enabled but empty.
        Expected: Returns (False, error).
        If fails: Empty whitelist accepts all.
        """
        content = "Any content"
        passed, error = check_whitelist(content, [], enabled=True)
        assert passed is False
        assert "empty" in error.lower()

    def test_matching_whitelist_passes(self):
        """Scenario: Content matches whitelist pattern.
        Expected: Returns (True, None).
        If fails: Whitelisted content rejected.
        """
        content = "This contains proxy keyword"
        whitelist = ["proxy", "config"]
        passed, error = check_whitelist(content, whitelist, enabled=True)
        assert passed is True
        assert error is None


class TestComputeHash:
    """Hash computation tests."""

    def test_hash_is_deterministic(self):
        """Scenario: Same file produces same hash.
        Expected: Identical hashes.
        If fails: Immutability check broken.
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("test content")
            f.flush()
            path = Path(f.name)

        hash1 = compute_hash(path)
        hash2 = compute_hash(path)
        assert hash1 == hash2

    def test_hash_changes_with_content(self):
        """Scenario: Different content produces different hash.
        Expected: Different hashes.
        If fails: Hash collision, immutability broken.
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f1:
            f1.write("content 1")
            f1.flush()
            path1 = Path(f1.name)

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f2:
            f2.write("content 2")
            f2.flush()
            path2 = Path(f2.name)

        hash1 = compute_hash(path1)
        hash2 = compute_hash(path2)
        assert hash1 != hash2
