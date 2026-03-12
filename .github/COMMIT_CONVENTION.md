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

feat: New product feature
fix: Product bug fix
docs: Documentation only
style: Formatting, linting (no code logic change)
refactor: Code restructuring (no feature change)
test: Test files only
chore: Development tools, scripts, maintenance
ci: CI/CD configuration
revert: Revert previous commit

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
