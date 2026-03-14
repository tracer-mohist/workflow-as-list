# CHANGELOG


## v0.7.0 (2026-03-14)

### Chores

- Remove test workflow files ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`e9398b7`](https://github.com/tracer-mohist/workflow-as-list/commit/e9398b761e7221a0db71389917e6220616ba1995))

- Removed workflow/test-local-import.workflow.list - Removed
  workflow/test-remote-import.workflow.list - Removed .imports/ cache directory

Test files served their purpose during #40 implementation. Cache is regenerated on-demand when
  imports are used.

REFERENCE: #40 (Import caching mechanism - completed)

### Features

- Prohibit pure-import files ([#41](https://github.com/tracer-mohist/workflow-as-list/pull/41),
  [`08e0b78`](https://github.com/tracer-mohist/workflow-as-list/commit/08e0b783b4383877f241c89efbd32ebac67b1a57))

- Added validate_no_pure_import() to WorkflowParser - Updated cli/check.py with validation - Updated
  SYNTAX.md documentation

REFERENCE: #41


## v0.6.2 (2026-03-14)

### Bug Fixes

- Verified duplicate annotation fix for remote imports
  ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`3c7671b`](https://github.com/tracer-mohist/workflow-as-list/commit/3c7671be99e35d894ad3b3b419d380ebd31b1088))

- Reset test files and verified fix works for both local and remote imports - Multiple runs of
  'workflow check --expanded' no longer create duplicates - Fix: Check if previous line has '# you
  see:' before adding annotation

Tested: - Local import: ✅ No duplicates - Remote import: ✅ No duplicates

REFERENCE: #40 (Import caching mechanism)


## v0.6.1 (2026-03-14)

### Bug Fixes

- Prevent duplicate annotation on repeated runs
  ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`2a1fbf0`](https://github.com/tracer-mohist/workflow-as-list/commit/2a1fbf00bc89d466972bbe6e5c82ab63ae8e36af))

- Check if previous line already has '# you see:' annotation - Only add annotation if not already
  present - Tested: multiple runs don't create duplicates

Bug: Running 'workflow check --expanded' multiple times added duplicate annotations

Fix: Check source file for existing annotation before adding

REFERENCE: #40 (Import caching mechanism)


## v0.6.0 (2026-03-14)

### Documentation

- Add comprehensive test results ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`68ec814`](https://github.com/tracer-mohist/workflow-as-list/commit/68ec81497a264842b1f709f43ad7c27cba6e4a6e))

- .test-results.md: Full CLI + Server API + Import caching test results - 12/12 CLI commands passed
  - 2/3 Server API endpoints passed (/health not implemented) - 3/3 Import caching features passed

REFERENCE: #40 (Import caching mechanism)

- Add comprehensive test results (49 tests, 93.87% pass)
  ([`8b44288`](https://github.com/tracer-mohist/workflow-as-list/commit/8b44288b3c0b221a7354717d2c251c6b88a9b603))

- 46/49 CLI commands passed - 8/9 Server API endpoints passed (/health not implemented) - 4/4 Import
  caching features passed - 2 skipped (no execution instances)

Test coverage: - 9 main commands + all subcommands + all options - All OpenAPI endpoints - Import
  caching (local + remote)

REFERENCE: #40 (Import caching mechanism)

### Features

- Add /health endpoint + manual exec read/next tests
  ([`a2bbc0c`](https://github.com/tracer-mohist/workflow-as-list/commit/a2bbc0c2ad9d776219b1b9f18aded2bf971e5f6a))

- Added GET /health endpoint - Manually tested exec read/next ✅ - Updated test results: 49/49 passed
  (100%)

REFERENCE: #40


## v0.5.6 (2026-03-14)

### Bug Fixes

- Hash-only cache naming (security fix)
  ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`9d95d13`](https://github.com/tracer-mohist/workflow-as-list/commit/9d95d13d45903de7354f8a29e0711529661b2ca3))

- Remove original filename (prevent injection) - Format: .imports/<hash>.workflow.list - Tested:
  local + remote imports

REFERENCE: #40


## v0.5.5 (2026-03-14)

### Bug Fixes

- Annotation format <project root:path> <hash>
  ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`3be3439`](https://github.com/tracer-mohist/workflow-as-list/commit/3be343924283046e95c0a58b187cbe849c5d55d9))

- Format: # you see: <project root:.imports/file> <sha256:...> - Clearer than '(project root)'
  suffix - All metadata in angle brackets

REFERENCE: #40


## v0.5.4 (2026-03-14)

### Bug Fixes

- Hash-based cache naming + project root annotation
  ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`94bf511`](https://github.com/tracer-mohist/workflow-as-list/commit/94bf5117926b670b07d95502d9cddb37cf5fbf62))

- Flat cache: .imports/<hash>-<filename> - Annotation: '(project root)' to avoid ambiguity

REFERENCE: #40


## v0.5.3 (2026-03-14)

### Bug Fixes

- Per-import caching with correct annotations
  ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`73ea7d1`](https://github.com/tracer-mohist/workflow-as-list/commit/73ea7d180d059620b51c36782e3b7152ac61e7ea))

- Each import cached independently - Annotation points to import's cache - Works for local and
  remote imports

REFERENCE: #40


## v0.5.2 (2026-03-14)

### Bug Fixes

- Cache annotation indentation matches import line
  ([`b021645`](https://github.com/tracer-mohist/workflow-as-list/commit/b021645e39ebc3c80087a04e3f52f560c3c9c9ac))

- Annotation inherits import line indentation - Format: ' # you see: <path> <hash>' (with leading
  spaces)

REFERENCE: #40


## v0.5.1 (2026-03-14)

### Bug Fixes

- Cache annotation format (before import, with brackets)
  ([`9a7f53d`](https://github.com/tracer-mohist/workflow-as-list/commit/9a7f53db3a780d4c8cc6283aa95d5c1a1e717cc1))

- Annotation before import line (not after) - Path wrapped in brackets: <path> - Format: # you see:
  <.imports/...> <sha256:...>

REFERENCE: #40 (Import caching mechanism)


## v0.5.0 (2026-03-14)

### Documentation

- Update traceflux-plan.md Phase 2 status
  ([`f65c441`](https://github.com/tracer-mohist/workflow-as-list/commit/f65c44172cebc98d559358565bcffd2bdc4f5562))

- Marked remote import workflows as complete - Added note about DSL import: feature validation

### Features

- Add import caching mechanism with loader
  ([#40](https://github.com/tracer-mohist/workflow-as-list/pull/40),
  [`68dbc75`](https://github.com/tracer-mohist/workflow-as-list/commit/68dbc759066b68b07883dfc2e9300fe074afcc32))

- New module: src/workflow_as_list/executor/loader.py - WorkflowLoader class with import expansion -
  Cache to .imports/ directory (auto-gitignore) - Add # you see: <path> <sha256:hash> annotation -
  Hash verification for cache invalidation - Updated show.py: --expanded flag shows inlined imports
  - Updated check.py: --expanded flag validates expanded content - Test workflow:
  workflow/test-import.workflow.list

NOTE: 239 lines (under 256 limit)

REFERENCE: #40 (Import caching mechanism)

- Add workflow init command for project onboarding
  ([#42](https://github.com/tracer-mohist/workflow-as-list/pull/42),
  [`53493b8`](https://github.com/tracer-mohist/workflow-as-list/commit/53493b8d403d284423e0551f73811d3ad16f2f09))

- New command: workflow init - Detects AGENTS.md/README.md/CONTRIBUTING.md - Adds workflow-as-list
  documentation - Creates .workflow-as-list/config.ini - Updates .gitignore - Creates
  workflow/README.md - Options: --docs-only, --config-only, --force

NOTE: 217 lines (under 256 limit)


## v0.4.0 (2026-03-14)

### Chores

- **scripts**: Refactor check-headers.py to extract logging module
  ([`7d9fd76`](https://github.com/tracer-mohist/workflow-as-list/commit/7d9fd76ab420b48c400aa6cf3af9ce74bde67418))

- Extract Log class to scripts/logging.py (42 lines) - Reduce check-headers.py from 286 to 239 lines
  - Add headers to 23 files via check-headers.py run - Passes check-code-quality.py limit (256
  lines)

Why: - Modularity: logging reusable across scripts - Maintainability: smaller, focused files -
  Consistency: all scripts under 256 line limit

- **scripts**: Remove emoji from logging output
  ([`5b0e9eb`](https://github.com/tracer-mohist/workflow-as-list/commit/5b0e9ebfde240457130471a6c594cc524bba63a9))

- Replace emoji with ASCII markers in logging.py - ✓ → [OK], ✗ → [FAIL], ⚠ → [WARN], → → >> - Add
  prompt-engineering compliance note - REFERENCE: docs/prompt-engineering/README.md (no emoji in
  content)

Why: - Cross-platform consistency (emoji rendering varies) - Tool call pollution prevention -
  Encoding compatibility

- **workflow**: Add main.workflow.list (minimal entry point)
  ([`dfb830d`](https://github.com/tracer-mohist/workflow-as-list/commit/dfb830d2ec6e097459d505b0e92ba5b59cb07f4a))

Design principles: - Design by Contract (pre/post/invariant documented) - Unix comment style (WHY
  not WHAT) - YAGNI (no meta-layer, no auto-learning yet) - KISS (20 steps, 3 decision points)

Changes: - Add workflow/main.workflow.list (minimal viable) - Remove workflow/commit.workflow.list
  (not needed now)

Why: - Need entry point for self-hosting - Complexity added when needed, not before - Comments
  explain rationale, not mechanics

### Documentation

- Add Agent integration guide ([#33](https://github.com/tracer-mohist/workflow-as-list/pull/33),
  [`9520536`](https://github.com/tracer-mohist/workflow-as-list/commit/952053602619cea922380e3686bb05a3ca5373b5))

- Create docs/AGENT-INTEGRATION.md - Document progressive reading workflow - CLI integration
  examples - API integration examples - Agent workflow pseudocode - Output storage guide - Best
  practices and error handling

Apply prompt-engineering framework: - Layer 1: Simple English, ASCII - Layer 2: Lists over tables,
  no **, no emoji - Layer 6: LABEL: annotation format (NOTE:, REFERENCE:, TIP:)

Closes: #33

- Add language name (WorkflowAsList DSL)
  ([`c12bf09`](https://github.com/tracer-mohist/workflow-as-list/commit/c12bf094eb94dbd3c5fdf6b7db4279c5f785e940))

- README.md: Add language name and file extension - SYNTAX.md: Add language name and file extension
  - No abbreviations (follows 'no shorthand' principle)

Why: - Clear language identity - Consistent naming across docs - Avoids confusion (WAL has other
  meanings) - File extension .workflow.list is descriptive

- Refactor READMEs as functor definitions
  ([`6c0cc74`](https://github.com/tracer-mohist/workflow-as-list/commit/6c0cc7421573ae224a0993f59585e262f682e300))

- Remove directory tree enumeration (lazy evaluation) - Add naming rules (path/action decomposition)
  - Add constraints (what must be true) - Add query commands (ls -R for structure)

Why: - README is a functor (mapping rules), not a cache - Enumeration becomes stale (maintenance
  debt) - Rules are stable (zero maintenance)

examples/README.md: 179 → 52 lines (-127) workflow/README.md: 178 → 47 lines (-131)

- Simplify README.md (point to live docs)
  ([`ae96bb6`](https://github.com/tracer-mohist/workflow-as-list/commit/ae96bb63b57df2afcd38b76280f92914ef092602))

- Remove CLI Commands list (point to workflow --help) - Remove Server API list (point to /docs) -
  Remove Repository Structure tree (ls is better) - Add Quick Start section (Install + Explore +
  Write) - Add Core Concept section (Progressive Reading) - Reduce from ~4400 to ~1800 bytes (60%
  reduction)

Why: - Live docs (--help, /docs) never go stale - README teaches how to explore, not what exists -
  Follows intermediate layer principle (equivalent substitution) - Follows prompt-engineering
  framework (lists, no **, no emoji)

Result: - 2-3 minute read time - Long-term maintainable - High readability

- Update README.md (pipx install, file structure, remove license)
  ([`3519d1a`](https://github.com/tracer-mohist/workflow-as-list/commit/3519d1aa7cc7e0ad9366130259db3800529b0043))

- Update Installation section: - pipx for users (GitHub Releases) - uv for contributors
  (development) - Remove License section (LICENSE file exists) - Add Repository Structure section
  (file navigation) - Verify API and CLI lists match code

Why: - pipx is simpler for end users - Clear separation: users vs contributors - File structure
  helps navigation - DRY principle (no duplicate license)

Closes: #38

- Update README.md with progressive reading model (#25, #29)
  ([`64d04a7`](https://github.com/tracer-mohist/workflow-as-list/commit/64d04a7ccfd2638103bb5caf5b6610324c2219de))

- Add execution model section (progressive reading metaphor) - Update CLI commands (exec read/next,
  remove serve) - Add Server API reference - Update directory structure - Apply prompt-engineering
  framework: - Layer 1: Simple English, ASCII - Layer 2: Lists over tables, no **, no emoji - Layer
  6: LABEL: annotation format (NOTE:, REFERENCE:, TIP:)

Closes: #25, #29

- **examples**: Add README.md with design philosophy
  ([`e1b7b4a`](https://github.com/tracer-mohist/workflow-as-list/commit/e1b7b4a2c2523b4441b69903d06af8ec2fe3b8a7))

- Document naming convention (domain/action.workflow.list) - Explain layer separation (examples vs
  workflow) - Record bootstrap principle and progressive design - REFERENCE: memory/2026-03-13.md
  (naming discussion)

Why: - Examples need clear guidance for users - Design decisions should be documented - Future
  contributors need context

- **workflow**: Add decision-capture workflow (Issue vs Docs routing)
  ([`a7d7400`](https://github.com/tracer-mohist/workflow-as-list/commit/a7d7400245431bc891be0db54f5adbef4dc9fb0a))

- **workflow**: Add README.md explaining self-hosted workflows
  ([`315b09a`](https://github.com/tracer-mohist/workflow-as-list/commit/315b09a637a6873ca35bcf33d158e04e12565e1f))

- Document purpose (manage workflow-as-list development) - Explain why self-hosting (validation,
  feedback, trust) - Describe relationship with examples/ - List current and TODO workflows

Why: - workflow/ needs clear documentation - Distinguish from examples/ (self vs generic) - Future
  contributors need context

- **workflow**: Simplify README.md
  ([`763bd35`](https://github.com/tracer-mohist/workflow-as-list/commit/763bd35fa6123320aeee3bf612b4fcff92e24705))

- Remove detailed directory structure (hard to maintain) - Remove TODO list (becomes stale) - Keep
  only core purpose and why - Focus on principles, not instructions

Why: - Less maintenance burden - Core message stays relevant longer

### Refactoring

- Move decision-capture to examples/decision/route (generic template)
  ([`b852c96`](https://github.com/tracer-mohist/workflow-as-list/commit/b852c96ea1dfd1f476411aba316800dd4abe7db8))

- Moved from workflow/ to examples/decision/route.workflow.list - Updated to be project-agnostic
  (removes workflow-as-list specific assumptions) - Enables reuse across projects via import: URL

NOTE: workflow/ is for project-specific workflows, examples/ is for reusable templates

### Testing

- Add integration and E2E tests (#14, #15)
  ([`4bb9e17`](https://github.com/tracer-mohist/workflow-as-list/commit/4bb9e1742ec4dac0e83158e74c4f5c6d4da0f1d1))


## v0.3.0 (2026-03-13)

### Features

- Implement progressive reading with steps_read tracking
  ([#28](https://github.com/tracer-mohist/workflow-as-list/pull/28),
  [`b1263bd`](https://github.com/tracer-mohist/workflow-as-list/commit/b1263bd1a620e5d602e36dce570d00eafeef3eaf))


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
