# Contributing to workflow-as-list

Thank you for your interest in contributing.

This document provides guidelines and instructions for contributing to workflow-as-list.

---

## Quick Start

Want to contribute? Here is how to get started:

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/workflow-as-list.git
cd workflow-as-list

# 3. Install for development (using uv)
uv sync --dev

# 4. Create a branch (use issue/<number>-<description> format)
git checkout -b issue/19-your-feature-name

# 5. Make your changes, test, and commit (follow Conventional Commits)
# 6. Push and open a Pull Request (required - no direct pushes to main)
```

Important: We use Pull Requests for all changes. No direct pushes to main.

---

## Commit Message Convention

We follow Conventional Commits v1.0.0.

Full Guide: See `.github/COMMIT_CONVENTION.md`

### Quick Reference

Type: `feat(scope)`
- When to Use: New product feature
- Example: `feat(cli): add check command`

Type: `fix(scope)`
- When to Use: Product bug fix
- Example: `fix(security): handle null response`

Type: `chore(scope)`
- When to Use: Development tools, scripts
- Example: `chore(scripts): add check-headers.py`

Type: `style`
- When to Use: Formatting, linting
- Example: `style(tests): fix ruff linting`

Type: `refactor(scope)`
- When to Use: Code restructuring
- Example: `refactor(executor): split into modules`

Type: `docs(scope)`
- When to Use: Documentation
- Example: `docs(readme): update installation`

Type: `ci`
- When to Use: CI/CD configuration
- Example: `ci: add GitHub Actions workflow`

Type: `test(scope)`
- When to Use: Test files
- Example: `test: add unit tests for security`

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Rules:
- Type: lowercase (feat, fix, chore, ...)
- Scope: lowercase, optional (cli, scripts, tests, ...)
- Description: imperative mood (add not added)
- Body: wrap at 72 characters
- Footer: BREAKING CHANGE:, Closes #123, etc.

### Examples

Good:
```bash
git commit -m "feat(cli): add check command"
git commit -m "chore(scripts): add check-headers.py"
git commit -m "style(tests): fix ruff linting"
```

Bad (do not do this):
```bash
git commit -m "feat(scripts): add tool"  # Scripts are chore, not feat
git commit -m "fix: lint errors"         # Lint is style, not fix
git commit -m "Updated file"             # No type, no scope
```

### Common Mistakes

Wrong: `feat(scripts): ...`
Correct: `chore(scripts): ...`
Why: Scripts are dev tools

Wrong: `fix(tests): lint`
Correct: `style(tests): lint`
Why: Lint is style, not bug

Wrong: `refactor(scripts): ...`
Correct: `chore(scripts): ...`
Why: Scripts refactor is chore

---

## Development Workflow

### 1. Branch Naming

Feature branch (linked to issue):
```bash
git checkout -b issue/19-add-check-command
```

Bug fix branch:
```bash
git checkout -b issue/42-fix-security-crash
```

Documentation branch:
```bash
git checkout -b docs/add-contributing-guide
```

### 2. Making Changes

```bash
# Make your changes
# Run tests
uv run pytest

# Run linter
uv run ruff check .
uv run ruff format --check .

# Commit
git add .
git commit -m "feat(cli): add check command"

# Push
git push -u origin issue/19-add-check-command
```

### 3. Pull Request

1. Go to https://github.com/tracer-mohist/workflow-as-list
2. Click New Pull Request
3. Select your branch
4. Fill in PR template
5. Wait for CI (test + lint must pass)
6. Address review comments
7. Merge (squash merge preferred)

---

## Code Style

### Python

Formatter: Ruff (`uv run ruff format .`)
Linter: Ruff (`uv run ruff check .`)
Imports: Sorted automatically by Ruff
Line length: 88 characters (Ruff default)

### Testing

Framework: pytest
Location: `tests/` directory
Naming: `test_<module>_<type>.py` (e.g., `test_security_unit.py`)

### Documentation

Format: Markdown
Style: Follow 6-Layer Prompt Engineering Framework (see `docs/prompt-engineering/README.md`)
Location: `docs/` directory

---

## Questions?

General: Open an issue
Code: Check existing issues and PRs
Conventions: See `.github/COMMIT_CONVENTION.md`

---

Last Updated: 2026-03-12
Related: workflow-as-list#19 (Conventional Commits cleanup)
