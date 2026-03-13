# CHANGELOG


## v0.2.0 (2026-03-13)

### Bug Fixes

- Remove test_serve_help test (serve command removed in #34)
  ([`7b6cada`](https://github.com/tracer-mohist/workflow-as-list/commit/7b6cada3accb6bc5c5b5c88db7cb5b2ea5a4b6ca))

- Delete test for removed serve command - Aligns with limited testing strategy (test only existing
  logic)

Reference: principles/automation/testing-strategy.md - Tests verify necessary conditions, not
  sufficient conditions - Remove tests for removed functionality

### Features

- Add command mapping for type selection
  ([`0a867cf`](https://github.com/tracer-mohist/workflow-as-list/commit/0a867cf9fe772cda9f7b5bfbe8025a8e3f99f8bb))

- (analyze) task: Run git diff --cached --name-only - Command output as context for type selection -
  Clear directory-to-type mapping in comments

Design: - Command as functor (repository state → file list) - Output as prompt context (factual
  basis, not memory) - Intermediate layer abstraction

Why: - Prevent incorrect type selection (non-src with feat/fix) - Reduce cognitive load (show
  changed files) - Avoid accidental version bumps - Command串 = 映射函数，输出 = 提示词

Mathematical insight: - Command: Group action on repository state - Output: Orbit (changed files) -
  Composition: Multiple commands → structured context

REFERENCE: principles/communication/prompt-engineering/theory/recursive-chain.md

- Add Server API POST /executions/{id}/next
  ([#32](https://github.com/tracer-mohist/workflow-as-list/pull/32),
  [`7ecccc5`](https://github.com/tracer-mohist/workflow-as-list/commit/7ecccc5ba346477c9d13ff9e7476ba93f845683e))

- Add workflow exec command for execution management (#30, #31)
  ([`3e1d09c`](https://github.com/tracer-mohist/workflow-as-list/commit/3e1d09c13217c759571c211d4700491b9d995a31))

### Refactoring

- Commit.workflow.list to correct comment format
  ([`147abf5`](https://github.com/tracer-mohist/workflow-as-list/commit/147abf5812d079cf27dbbc0497d721f0d1951961))

- Move all comments above task lines (format A) - Follow recursive-chain theory (low entropy, high
  prediction quality) - Comments explain WHY, not WHAT - Same indent level as task

Why: - Format B (comments below) breaks recursive chain - LLM token prediction needs前置 context -
  Attention entropy lower with format A - Example sets standard for future workflows

Design: - # WHY: explains design intent - # NOTE: supplementary info - Comments above task (not
  below) - File header comments attach to first task

REFERENCE: principles/communication/prompt-engineering/theory/recursive-chain.md

- Remove workflow serve command ([#34](https://github.com/tracer-mohist/workflow-as-list/pull/34),
  [`e69ce59`](https://github.com/tracer-mohist/workflow-as-list/commit/e69ce598fc1923985e4bd78c3d2b3a66b0672f24))

- Delete src/workflow_as_list/cli/serve.py - Remove serve registration from cli/__init__.py - Update
  docs/design/cli/003-commands.md

Why: - Redundant with workflow server start - Lower efficiency (blocks terminal) - No unique value

Users can use: - workflow server start (background mode) - uv run uvicorn
  src.workflow_as_list.server:app (foreground debugging)

- Workflow exec next shows current + next step
  ([#30](https://github.com/tracer-mohist/workflow-as-list/pull/30),
  [`781143b`](https://github.com/tracer-mohist/workflow-as-list/commit/781143b031fd5c60129e4ce5b2240623fd5e6878))


## v0.1.2 (2026-03-13)

### Bug Fixes

- Check token length per line (not whole file)
  ([`62cad0a`](https://github.com/tracer-mohist/workflow-as-list/commit/62cad0ac56678e682b591f1905bb6f390e991329))

- validator.py: Check each line's byte count, not entire file - layers.py: Handle per-line errors
  and warnings - tests: Update test cases for per-line checking

Why: - Token limit (282-358) is per task, not per file - Each line is a task description - Previous
  implementation was incorrect

Design: - Skip comments and empty lines - Check each content line's byte count - Return errors
  (exceeds) and warnings (below)

Reference: docs/research/theory/003-limits.md - TaskToken_range = [√(N × 0.618), √N] - Per task
  description, not entire workflow

### Chores

- Add GitHub Issue Forms templates
  ([`eb2af70`](https://github.com/tracer-mohist/workflow-as-list/commit/eb2af7059b609ac78dfd3749d4cce7986bd2d6f1))

- 01_design_decision.yml: ADR with commit hash binding - 02_feature_request.yml: Feature requests -
  03_question.yml: Questions - 04_bug_report.yml: Bug reports

Design: - Simple English (prompt-engineering Layer 1) - Minimal fields (only what's needed) - Clear
  placeholders (show, don't tell) - LABEL: annotations (NOTE:, TIP:) - No emoji, no ** emphasis - No
  config.yml (unnecessary complexity)

Why: - Issues as /tmp for temporary decisions - Docs for long-term knowledge - Clear separation:
  knowledge vs process - Traceable decisions (commit hash)

REFERENCE: docs/github-issue-templates-research.md

- Garden docs (deprecation cycle)
  ([`1f7ce1c`](https://github.com/tracer-mohist/workflow-as-list/commit/1f7ce1c094b451d1dc02431c5b5833115f5487e4))

- Remove docs/v0.1.1-plan.md (completed, migrated to issues) - Update README.md with directory
  structure - Create issues for remaining documentation tasks

Design: - Deprecation cycle: mark → migrate → remove - Issues track pending work (not docs) - README
  documents current state

Issues created: - #25: Update README.md with directory structure - #26: Update AGENTS.md
  architecture diagram

REFERENCE: docs/github-issue-templates-research.md (Issues as /tmp)

### Documentation

- Add commit workflow (Divide and Conquer example)
  ([`c81bc1a`](https://github.com/tracer-mohist/workflow-as-list/commit/c81bc1a11c5f143c9fed03bab5db890162261c34))

- commit.workflow.list: Main flow with imports - commit-validate.workflow.list: Check sensitive
  files - commit-type.workflow.list: Choose correct type - commit-message.workflow.list: Compose
  message per spec

Design: - Apply Divide and Conquer (4 subtasks) - Each <358 bytes (token limit) - Import for
  modularity - Comments explain WHY (Unix style)

Why: - Demonstrate import feature - Show Divide and Conquer pattern - Help with Conventional Commits
  - Prevent incorrect type usage

REFERENCE: - https://www.conventionalcommits.org/en/v1.0.0/ - .github/COMMIT_CONVENTION.md -
  examples/README.md (file header style)

- Add commit-type helper workflow
  ([`168b317`](https://github.com/tracer-mohist/workflow-as-list/commit/168b3178cfb72138dacb1abbbf51493b3a76e3fe))

- commit-type.workflow.list: Help choose correct Conventional Commits type - Simple reference:
  src/=feat/fix, tests/=test, docs/=docs, etc.

Why: - Prevent incorrect type usage (feat for non-src changes) - Quick reference for agent - Avoid
  accidental version bumps

NOTE: This is documentation, not a feature. Use as reference before writing commit message.

REFERENCE: .github/COMMIT_CONVENTION.md

- Add example workflows (git commit helper)
  ([`b43af45`](https://github.com/tracer-mohist/workflow-as-list/commit/b43af4562c5aa57ac971c1857745f1c98d72a546))

- commit.workflow.list: Main workflow with imports - commit-validate.workflow.list: Validate staged
  changes - commit-message.workflow.list: Compose Conventional Commit

Design: - Apply Divide and Conquer (split into subtasks) - Each subtask <358 bytes (token limit) -
  Import for modularity - Comments explain WHY, not WHAT

Why: - First real-world example - Demonstrate import feature - Show Divide and Conquer in action -
  Provide reusable template

NOTE: Examples are documentation, not features. No version bump needed.

REFERENCE: examples/README.md

- Simplify commit workflow (single file)
  ([`6ff37e6`](https://github.com/tracer-mohist/workflow-as-list/commit/6ff37e658ed74e60d922038009562ab291897be7))

- Single commit.workflow.list (no sub-files) - Multi-level list structure (nested) - 350 bytes (<358
  token limit) - 19 steps

Design: - Nested lists for logical grouping - No import dependencies - Self-contained - Simple and
  clear

Why: - Easier to maintain (one file) - No dependency management - Clearer structure - Follows Unix
  philosophy

REFERENCE: examples/README.md

### Refactoring

- Rename TOKEN_MIN/MAX to TOKEN_HUB_LOWER/UPPER
  ([`519c80a`](https://github.com/tracer-mohist/workflow-as-list/commit/519c80ac34e57fe6023b066823ae243656ff3caa))

- constants.py: Rename with docstrings explaining purpose - validator.py: Return (is_valid, count,
  suggestion) tuple - layers.py: Distinguish warning (below lower) vs error (above upper) -
  config.py: Update config field names - models.py: Update Config model fields - tests: Update test
  cases for new behavior - docs: Update documentation references - scripts: Update
  calc-task-range.py

Why: - Token bounds are both upper limits (√N formula variants) - Lower bound (282): Warning -
  consider adding context - Upper bound (358): Error - apply Divide and Conquer

Design: - Use consensus terminology (Divide and Conquer) - Self-contained messages (no external doc
  references) - Abstract guidance (not specific examples)

- Use CONFIG_FILE constant instead of redefining path
  ([`450dc73`](https://github.com/tracer-mohist/workflow-as-list/commit/450dc73c175dbf1bb4f1bd7f7ef3dd30cb68f119))

- config.py: Import and use CONFIG_FILE from constants - Why: DRY principle - single source of truth
  for paths - Agent-friendly: no need to remember where paths are defined


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
