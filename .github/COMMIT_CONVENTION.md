<!-- .github/COMMIT_CONVENTION.md -->
# Commit Message Convention

**Standard**: Conventional Commits v1.0.0

**Reference**: https://www.conventionalcommits.org/en/v1.0.0/

---

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

---

## Type

Required. Must be lowercase.

### Version-Triggering Types

These types trigger semantic version bumps (only for `src/` changes):

feat: New product feature → MINOR bump (0.1.0 → 0.2.0)
fix: Product bug fix → PATCH bump (0.1.0 → 0.1.1)
BREAKING CHANGE: Breaking API change → MAJOR bump (0.1.0 → 1.0.0)

### Non-Version-Triggering Types

These types do NOT trigger version bumps:

docs: Documentation only
style: Formatting, linting (no code logic change)
refactor: Code restructuring (no feature change)
test: Test files only (unit tests, integration tests, E2E tests)
chore: Development tools, scripts, maintenance
ci: CI/CD configuration
revert: Revert previous commit

**Important**: Test-related commits should use `test:` type, NOT `feat:` or `fix:`.
Adding tests does not add user-facing features or fix product bugs.

---

## Scope and Directory Rules

### src/ Directory (Product Code)

Only changes to `src/` should use `feat:` or `fix:`:

```
src/workflow_as_list/cli.py          → feat(cli): add run command
src/workflow_as_list/executor/       → fix(executor): handle null response
src/workflow_as_list/security/       → feat(security): add whitelist support
```

### Non-src/ Directories

Changes outside `src/` should NOT use `feat:` or `fix:`:

```
tests/test_*.py                      → test: add unit tests
scripts/*.py                         → chore(scripts): add tool
docs/*.md                            → docs: update README
.github/workflows/*.yml              → ci: add validate workflow
pyproject.toml                       → chore(deps): update dependencies
```

### Test Commits Never Trigger Versions

**Rule**: Test-related commits ALWAYS use `test:` type.

Examples:
```
test: add unit tests for parser
test(cli): add integration tests for check command
test: add E2E tests for workflow execution
```

**Why**: Tests verify existing functionality, they don't add features or fix bugs.

### Why This Matters

Semantic release analyzes commit types to determine version bumps:
- `feat` commits → minor version (new features)
- `fix` commits → patch version (bug fixes)
- Other types → no version change

Using `feat(scripts)` or `fix(tests)` would incorrectly trigger version bumps for non-product changes.

---

## Scope

Optional. Must be lowercase if present.

Examples:
- cli: CLI commands
- executor: Parser, state management
- security: Security layers
- server: HTTP API
- scripts: Utility scripts
- tests: Test files
- docs: Documentation
- ci: GitHub Actions

---

## Description

Required. Imperative mood.

Good:
- add check command
- fix security validation
- update README

Bad:
- added check command (past tense)
- fixing security validation (progressive)
- README update (noun phrase)

---

## Body

Optional. Wrap at 72 characters.

Use for:
- Explaining why (not what)
- Documenting alternatives considered
- Noting assumptions

---

## Footer

Optional. Use for:

BREAKING CHANGE: <description>
- Triggers major version bump
- Must include migration notes

Closes #123
- Links to GitHub issue

Fixes #456
- Links to bug fix

---

## Examples

Good commits:
```
feat(cli): add check command

New subcommand to validate and register workflows.

Closes #12
```

```
fix(security): handle null response in blacklist check

Blacklist patterns may be empty list.

Fixes #45
```

```
chore(scripts): add check-headers.py

Automated license header verification.
```

```
style(tests): fix ruff linting

No code logic change.
```

```
ci: add commitlint to validate.yml

Commit message format enforcement on PR.
```

Bad commits (do not use):
```
feat(scripts): add tool
# Scripts are chore, not feat
```

```
fix: lint errors
# Lint is style, not fix
```

```
Updated file
# No type, no scope, no context
```

---

## Enforcement

Pre-commit: Run locally before commit
CI: Enforced on pull requests (commitlint GitHub Action)

---

Last Updated: 2026-03-12
