# Commit Message Convention

**Based on**: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

---

## Quick Reference

### Commit Types

| Type | When to Use | SemVer Impact |
|------|-------------|---------------|
| `feat` | New **product** feature (user-facing) | MINOR (v1.0.0 → v1.1.0) |
| `fix` | **Product** bug fix | PATCH (v1.0.0 → v1.0.1) |
| `chore` | Development tools, scripts, maintenance | None |
| `style` | Formatting, linting (no logic change) | None |
| `refactor` | Code restructuring (no behavior change) | None |
| `docs` | Documentation only | None |
| `ci` | CI/CD configuration | None |
| `test` | Test files only | None |
| `build` | Build system, dependencies | None |
| `perf` | Performance improvements | None |

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Rules**:
- Type: lowercase (feat, fix, chore, ...)
- Scope: lowercase, optional (cli, server, scripts, ...)
- Description: imperative mood ("add" not "added")
- Body: optional context, wrap at 72 chars
- Footer: BREAKING CHANGE, Closes #123, etc.

---

## Type Guidelines

### ✅ DO Use `feat` For

- New CLI commands: `feat(cli): add check command`
- New API endpoints: `feat(server): add /workflows endpoint`
- New user-facing features: `feat(parser): support import directive`

### ❌ DON'T Use `feat` For

- Development scripts: `chore(scripts): add check-headers.py`
- Test files: `test: add unit tests for security`
- Documentation: `docs(readme): update installation`

---

### ✅ DO Use `fix` For

- Product bugs: `fix(security): handle null response`
- CLI crashes: `fix(cli): prevent crash on missing file`
- Logic errors: `fix(executor): correct step indexing`

### ❌ DON'T Use `fix` For

- Lint errors: `style(tests): fix ruff linting`
- Formatting: `style: remove trailing whitespace`
- Test fixes: `test: fix flaky test`

---

### ✅ DO Use `chore` For

- Scripts: `chore(scripts): add check-headers.py`
- Dependencies: `chore(deps): upgrade ruff to v0.15.5`
- Config files: `chore: update .gitignore`
- Scripts refactor: `chore(scripts): simplify calc-task-range.py`

---

### ✅ DO Use `style` For

- Lint fixes: `style: resolve ruff errors`
- Formatting: `style: format code with black`
- Import order: `style: sort imports with isort`

---

### ✅ DO Use `refactor` For

- Product code restructuring: `refactor(executor): split into modules`
- Simplifying logic: `refactor(security): simplify validation`

### ❌ DON'T Use `refactor` For

- Scripts: `chore(scripts): refactor calc-task-range.py`

---

### ✅ DO Use `docs` For

- README updates: `docs(readme): add installation guide`
- API documentation: `docs(api): document /workflows endpoint`
- Comments: `docs: add docstrings to executor`

---

### ✅ DO Use `ci` For

- GitHub Actions: `ci: add release workflow`
- CI configuration: `ci: update test matrix`

---

### ✅ DO Use `test` For

- Unit tests: `test: add unit tests for security`
- Integration tests: `test: add pipeline integration test`
- E2E tests: `test: add E2E workflow tests`

---

## Examples

### Good Commits

```
feat(cli): add check command

Add new 'check' subcommand to validate and register workflows.

Closes: #12
```

```
fix(security): handle null response from server

The race condition occurred when server returned null.
Added null check to prevent crash.
```

```
chore(scripts): add check-headers.py automation tool

Python version of check-headers.mjs for automated header insertion.

Supports multiple comment styles: // # -- /* <!--
```

```
style(tests): fix ruff linting

- Fix import ordering (I001)
- Remove unused imports (F401)
```

```
refactor(executor): split into modular components

- Create executor/ directory
- Split parser.py and state.py
- Each file <200 lines

BREAKING CHANGE: Import path changed from executor.py to executor/parser.py
```

```
docs(readme): update installation instructions

Add uv installation method and Python version requirements.
```

```
ci: add GitHub Actions workflow

- test job (pytest)
- lint job (ruff)
- release job (on tag push)
```

---

### Bad Commits

```
❌ feat(scripts): add check-headers.py
✅ chore(scripts): add check-headers.py
Reason: Scripts are development tools, not product features
```

```
❌ fix(tests): resolve ruff linting
✅ style(tests): resolve ruff linting
Reason: Lint is code style, not a bug
```

```
❌ refactor(scripts): simplify calc-task-range.py
✅ chore(scripts): simplify calc-task-range.py
Reason: Scripts refactor is maintenance, not product refactor
```

```
❌ Updated file.txt
✅ docs: update README installation guide
Reason: Missing type and scope
```

```
❌ fix: minor improvements
✅ style: remove trailing whitespace
Reason: Too vague, be specific
```

---

## Breaking Changes

Commits with BREAKING CHANGE introduce incompatible API changes:

```
feat(api)!: remove /users endpoint

BREAKING CHANGE: /users endpoint removed, use /api/users instead.
```

```
refactor!: drop support for Python 3.10

BREAKING CHANGE: Minimum Python version is now 3.11.
```

---

## Scope Guidelines

### Valid Scopes

| Scope | When to Use |
|-------|-------------|
| `cli` | CLI commands, argument parsing |
| `server` | HTTP server, API endpoints |
| `executor` | Workflow execution logic |
| `security` | Security checks, validation |
| `parser` | Workflow syntax parsing |
| `scripts` | Development scripts |
| `tests` | Test files |
| `docs` | Documentation |
| `ci` | CI/CD configuration |
| `deps` | Dependencies |

### Scope Rules

1. Use scope when change affects specific component
2. Omit scope for cross-cutting changes
3. Keep scope lowercase, short, and clear

---

## Tools

### Commit Linting (Future)

Add to CI:
```yaml
- name: Lint commit messages
  uses: wagoid/commitlint-github-action@v5
  with:
    config-file: .commitlintrc.json
```

### Pre-commit Hook (Optional)

```bash
# .git/hooks/commit-msg
#!/bin/sh
npx --no -- commitlint --edit "$1"
```

---

## References

- [Conventional Commits Spec](https://www.conventionalcommits.org/en/v1.0.0/)
- [Angular Convention](https://github.com/angular/angular/blob/master/CONTRIBUTING.md)
- [Semantic Versioning](https://semver.org/)
- [workflow-as-list#19](https://github.com/tracer-mohist/workflow-as-list/issues/19)

---

**Last Updated**: 2026-03-10  
**Status**: Draft (pending review)
