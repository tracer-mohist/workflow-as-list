# CHANGELOG


## v0.1.1 (2026-03-13)

### Bug Fixes

- Resolve tilde path expansion bug
  ([`fa719ed`](https://github.com/tracer-mohist/workflow-as-list/commit/fa719edc041c8f3d6ceee50942cf95199f2d789d))

- config.py: Use Path.home() instead of '~' string literal - models.py: Use default_factory with
  Path.home() for config_dir - .gitignore: Add ~/ to prevent committing accidental tilde directories

NOTE: Path('~') does not auto-expand in Python. Must use Path.home() or .expanduser()

Refs: v0.1.1 state management

### Chores

- Remove completed todo tracking files
  ([`4303589`](https://github.com/tracer-mohist/workflow-as-list/commit/430358982e83286dac16c6be8fa9f0607053e94d))

- Remove examples directory (low practical value)
  ([`a8e853c`](https://github.com/tracer-mohist/workflow-as-list/commit/a8e853c1577efc1bdf6fd102db28832f9dfdc6e1))

### Continuous Integration

- **release**: Fix checkout for semantic-release detached HEAD
  ([`802267f`](https://github.com/tracer-mohist/workflow-as-list/commit/802267f3cf63bf9da7917ac8ed993a91349ec324))

- **release**: Fix semantic-release command
  ([`f927bc6`](https://github.com/tracer-mohist/workflow-as-list/commit/f927bc6fcdbbcdf7b48f70101bb1e0d225c91d40))

- **release**: Trigger semantic-release on push to main
  ([`6594ee1`](https://github.com/tracer-mohist/workflow-as-list/commit/6594ee154d74c57302e6cf5c9b7a939ac78a596a))

### Documentation

- Add v0.1.1 plan (state management + server control)
  ([`d14af35`](https://github.com/tracer-mohist/workflow-as-list/commit/d14af3599a74ea1c8ba1abcb01b52d5e3c4816de))

- Clarify test commits never trigger versions
  ([`d22b39d`](https://github.com/tracer-mohist/workflow-as-list/commit/d22b39d84e11c4fd9a5726ab80fa97ed8bd4a48e))

- Add section: Test Commits Never Trigger Versions - Emphasize: test: type for all test-related
  commits - Explain: tests verify existing functionality, don't add features

REFERENCE: Conventional Commits v1.0.0

- Update path references in AGENTS.md
  ([`ffe517c`](https://github.com/tracer-mohist/workflow-as-list/commit/ffe517cee9714611819322039cdee95891270944))

- ~/.config/wf/ → ~/.workflow-as-list/ - Consistent with PROJECT_ROOT refactor

- **examples**: Add examples README as index
  ([`06a5d7f`](https://github.com/tracer-mohist/workflow-as-list/commit/06a5d7fe1b9a3bee9dbf9ee053f17349c6f609d2))

- Directory structure (domain/use-case) - Usage: copy, check, run - Guidelines: real problems, clear
  comments - Example list by domain

NOTE: Keep README minimal (<100 lines). Examples speak for themselves.

- **examples**: Add style guide to README
  ([`56e4ebc`](https://github.com/tracer-mohist/workflow-as-list/commit/56e4ebcb14d156b9857dfa72d7e5c5f8ad54cd9b))

- File header style (Purpose/Usage/Pre/Post conditions) - Comment style (explain why, not what) -
  References: Design by Contract, Unix philosophy - Keep README minimal (82 lines)

INSPIRATION: - Script header comments (self-documenting) - Bertand Meyer's Design by Contract - Unix
  comment philosophy (why > what)

### Refactoring

- Unify all paths under PROJECT_ROOT
  ([`daf49dd`](https://github.com/tracer-mohist/workflow-as-list/commit/daf49dd32b1c28a460d6e220687738d8dbd7546b))

- constants.py: BASE_DIR → PROJECT_ROOT (with docstring explaining why) - config.py: Use
  PROJECT_ROOT from constants - models.py: Update docstrings (execution storage path)

Why: - Single location for all state (agent-friendly) - Easy cleanup: rm -rf ~/.workflow-as-list/ -
  Easy backup: one directory - State visible: no scattered configs

Breaks: - Old path references in docs (to be cleaned) - Migration from ~/.config/wf/ (planned)

- **cli**: Split CLI into package (256 line rule)
  ([`308af4a`](https://github.com/tracer-mohist/workflow-as-list/commit/308af4a48b7363759d94434eddd81f358bee1ee4))

- Split cli.py into cli/ package (9 submodules) - Add check-code-quality.py script - All source
  files < 256 lines - Server management CLI (start/stop/status/logs) - Centralized constants in
  constants.py

REFERENCE: docs/v0.1.1-plan.md

ISSUES: #22, #23, #24


## v0.1.0 (2026-03-12)

### Chores

- Initialize project structure
  ([`61c328c`](https://github.com/tracer-mohist/workflow-as-list/commit/61c328c47fe47d7146f5f42ef4432e681d51a474))

Clean git history with proper Conventional Commits.

Project features: - CLI with 7 subcommands (check, approve, reject, run, list, show, serve) -
  7-layer security checks (encoding, blacklist, token length, features, audit, whitelist) - Executor
  with progressive exposure (one step at a time) - HTTP server with OpenAPI documentation -
  Automated releases via python-semantic-release - CI/CD with GitHub Actions (test + lint)

Tech stack: - Python 3.12+ - uv for package management - Ruff for linting and formatting - pytest
  for testing - FastAPI + Typer + Pydantic

NOTE: This is a fresh start for better future. - Removed Chinese commit messages (encoding
  compatibility) - Fixed Conventional Commits usage (scripts are chore, not feat) - Proper project
  structure with modular design

References: - Conventional Commits: https://www.conventionalcommits.org/en/v1.0.0/ - Issues: #19
  (commit cleanup), #20 (CI fix)

### Code Style

- Fix ruff formatting
  ([`c7ca4e7`](https://github.com/tracer-mohist/workflow-as-list/commit/c7ca4e795b8c72101643348fda9bcf42bfd1a410))

- Format scripts/check-headers.py - Format src/workflow_as_list/executor/state.py - Fix any linting
  issues

### Continuous Integration

- Add validate.yml + documentation refactor
  ([`bba546a`](https://github.com/tracer-mohist/workflow-as-list/commit/bba546a3a47575b7572d1ca3e7bd858de358f191))

- Fix release workflow trigger condition
  ([`53766b6`](https://github.com/tracer-mohist/workflow-as-list/commit/53766b665ee02911609e756c0d6b996f9fa08bea))

Change from branch trigger to tag trigger.

Before: on: push: branches: [main] # ❌ Wrong: triggers on every push

After: on: push: tags: - 'v*' # ✅ Correct: only on tag push

This ensures: - No unnecessary workflow runs - No accidental releases - Wasted CI minutes saved -
  Clean release history

Related: #20

- Optimize for uv + Ruff stack
  ([`7ff21fa`](https://github.com/tracer-mohist/workflow-as-list/commit/7ff21faf54f6b1d72f4a8b89ff1bc066178d22ea))

Workflow-as-list specific configuration: - ci.yml: uv sync + pytest + Ruff (check + format) -
  release.yml: python-semantic-release via uv

NOTE: Separated from traceflux (different tool stack).

REFERENCE: docs/ci-cd-best-practices.md

- Separate CI and Release workflows + add concurrency
  ([`ef10021`](https://github.com/tracer-mohist/workflow-as-list/commit/ef100210a0a24400cb6a12c6b0caaac8c5c9a290))

Changes: - ci.yml: Only test + lint (no release job) - release.yml: Only release (no test + lint,
  already passed) - Add concurrency control (cancel redundant runs)

Benefits: - No duplicate test+lint on tag push - Faster release workflow - Save CI minutes - Cancel
  redundant runs on new pushes

NOTE: Follows traceflux pattern and professional project best practices.

REFERENCE: docs/ci-cd-best-practices.md

### Documentation

- **readme**: Trigger CI validation test
  ([`c9f50b4`](https://github.com/tracer-mohist/workflow-as-list/commit/c9f50b43fc791700b00d10d6674c7ada7b3cd5b9))
