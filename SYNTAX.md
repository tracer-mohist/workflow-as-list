<!-- SYNTAX.md -->
# WorkflowAsList DSL Syntax Specification

**Language**: WorkflowAsList DSL

**File Extension**: `.workflow.list`

**Purpose**: Formal syntax definition with human-readable explanations.

**Audience**: Humans and LLMs implementing WorkflowAsList parsers or validators.

**Status**: Stable (2026-03-08).

---

## Overview

WorkflowAsList syntax is defined in two formats:

- `SYNTAX.ebnf` - Formal EBNF specification (machine-readable)
- `SYNTAX.md` - This document (human-readable)

NOTE: Both formats describe the same syntax. Use EBNF for precision, use this document for understanding.

---

## Core Concept

WorkflowAsList is a **thinking constraint DSL**, not an execution language.

**Concise** (Information Theory): Remove redundancy, preserve meaning.

**Practical** (Set Theory): Bounded scope, minimal complete.

**Elegant** (Logical Flow): Logical coherence, consistent ordering.

---

## Five Rules (Summary)

1. List item - Line starts with `- `
2. Nested content - Indent with 2 spaces per level
3. Tag - `(identifier)` modifies any line
4. Jump - `@tag[N]: condition?` loops back (max N times)
5. Import - `import: path` includes external file

REFERENCE: See `README.md` for quick reference and examples.

---

## Constraints

### No Pure Import Files (#41)

**Rule**: A workflow file MUST have at least one local step.

**Invalid**:
```
# ❌ Pure import (no local steps)
import: ./base.workflow.list
```

**Invalid**:
```
# ❌ Import as first line (no ignition)
import: ./base.workflow.list

- (local) My step
```

**Valid**:
```
# ✅ Local step before import (ignition)
- (start) Workflow Name
  import: ./base.workflow.list

# ✅ Local step after import
- (analyze) Analyze files
  import: ./common/analyze.workflow.list
```

**Rationale**:
- Import should be a dependency, not a replacement
- Local steps provide execution context ("ignition")
- User psychology: "This is workflow" not "This is meta"

REFERENCE: See #41 for design discussion.

---

## Detailed Syntax

### 1. List Item

**Format**: `- content`

**EBNF**:
```ebnf
line = "- " , content_text , eol ;
```

**Rules**:
- Every workflow line starts with `- ` (dash followed by space)
- Content follows after the marker
- Line ends with newline

**Example**:
```
- Read project structure
- Analyze dependencies
- Generate report
```

NOTE: Empty lines are not valid workflow lines.

---

### 2. Nested Content

**Format**: Indent with 2 spaces per nesting level

**EBNF**:
```ebnf
indent = { "  " } ;
line_content = indent , [ tag ] , content_text , [ jump ] ;
```

**Rules**:
- Each nesting level adds exactly 2 spaces
- Root level has no indent (0 spaces)
- Indent defines parent-child relationship

**Example**:
```
- Root task (level 0)
  - Sub-task A (level 1)
    - Sub-sub-task (level 2)
  - Sub-task B (level 1)
```

TIP: Use consistent indentation. Mixing tabs and spaces breaks parsing.

---

### 3. Tag

**Format**: `(identifier)`

**EBNF**:
```ebnf
tag = "(" , identifier , ")" ;
identifier = letter , { letter | digit | "-" } ;
letter = "A" | "B" | ... | "Z" | "a" | "b" | ... | "z" ;
```

**Rules**:
- Tag enclosed in parentheses
- Identifier starts with letter
- Identifier contains letters, digits, or hyphens
- ASCII only (no Unicode in identifiers)
- Tag can appear on any line type (universality)

**Example**:
```
- (start) Initialize system
- (validate) Check input
- (error) Handle failure
```

NOTE: Tags serve as jump targets. Choose meaningful names.

---

### 4. Jump

**Format**: `@tag[N]: condition?`

**EBNF**:
```ebnf
jump = "@" , identifier , "[" , max_iterations , "]" , ":" , condition ;
max_iterations = digit_excluding_zero , { digit } ;
condition = { character - "?" } , "?" ;
```

**Rules**:
- Starts with `@` followed by tag identifier
- Max iterations in square brackets (positive integer)
- Colon separates from condition
- Condition ends with question mark
- Jump loops back to tagged line

**Example**:
```
- (retry) Attempt connection
  - Send request
  - Wait for response

- @retry[3]: Connection successful?
```

TIP: Max iterations prevents infinite loops. Choose reasonable limits (1-10 typical).

---

### 5. Import

**Format**: `import: path`

**EBNF**:
```ebnf
import_statement = "import:" , path ;
path = local_path | remote_url ;
local_path = { path_character } ;
remote_url = url_scheme , "://" , url_authority , { url_path_character } ;
url_scheme = "http" | "https" ;
```

**Rules**:
- Keyword `import:` followed by space
- Path can be local file or remote URL
- Local paths: relative (`./`) or absolute (`/`)
- Remote URLs: must start with `http://` or `https://`
- Relative paths resolved from current workflow location

**Examples**:
```
(* Local file imports *)
import: ./common/setup.workflow.list
import: ../shared/validation.workflow.list
import: /home/user/workflows/base.workflow.list

(* Remote URL imports *)
import: https://raw.githubusercontent.com/user/repo/main/workflow.list
import: https://example.com/workflows/shared.workflow.list
```

**Security Considerations**:
- HTTPS preferred over HTTP (encrypted transport)
- LLM should validate URL trustworthiness
- Avoid importing from untrusted sources
- Consider caching remote imports for offline use

NOTE: Import inserts all lines from external file/URL at import location.

---

## Complete Example

```
- (start) Analyze Codebase
  import: ./common/read-structure.workflow.list
  
- (parse) Parse Source Files
  - Extract function definitions
  - Extract variable declarations
  - Build call graph
  
- @parse[2]: All files parsed?

- (report) Generate Report
  - Summarize findings
  - List potential issues
  - Suggest improvements
  
import: ./common/save-report.workflow.list
import: https://raw.githubusercontent.com/tracer/workflows/main/templates/report-format.workflow.list
```

**Walkthrough**:
1. Tag `(start)` marks entry point
2. Import loads shared workflow (local file)
3. Tag `(parse)` marks parsing section
4. Jump `@parse[2]` loops max 2 times
5. Tag `(report)` marks reporting section
6. Second import saves output (local file)
7. Third import loads template (remote URL)

---

## Constraints

### Identifier Naming

**Allowed**:
- `start`, `analyze`, `step-1`, `retryLoop`

**Not Allowed**:
- `1start` (starts with digit)
- `my_tag` (underscore not allowed)
- `开始` (non-ASCII)

### Jump Validation

**Valid**:
- Jump target tag exists in workflow
- Max iterations is positive integer
- Condition is question format

**Invalid**:
- Jump to non-existent tag
- Max iterations is 0 or negative
- Condition missing question mark

### Import Validation

**Valid**:
- File exists at path (local)
- URL is reachable (remote)
- File has `.workflow.list` extension (recommended)
- No circular imports

**Invalid**:
- File not found (local)
- URL returns 404 or times out (remote)
- Circular import chain
- Untrusted source without validation

**Security Best Practices**:
- Use HTTPS for remote imports
- Verify URL source before importing
- Cache remote imports for reproducibility
- Document import sources in workflow header

---

## Implementation Notes

### For LLMs

**Directional Instructions**:
- READ the workflow from top to bottom
- FOLLOW indentation for nesting
- EVALUATE jump conditions semantically
- RESPECT max iteration limits
- RESOLVE import paths relative to current file

NOTE: No parser required. LLM reads and follows directly.

### For Validators

**Optional Validation Steps**:
1. Check syntax against EBNF
2. Verify jump targets exist
3. Validate import paths
4. Detect circular imports

TIP: Validation is optional. WorkflowAsList designed for LLM interpretation, not strict parsing.

---

## Design Decisions

### Why 2 Spaces for Indent?

**Why**: Balance readability and screen space.

**Alternatives Considered**:
- 4 spaces (too wide for deep nesting)
- Tabs (inconsistent rendering across editors)
- No indent (loses hierarchy)

**Assumptions**:
- Maximum nesting depth is 5-6 levels
- Users prefer visual clarity

### Why ASCII Identifiers Only?

**Why**: Maximum compatibility across systems.

**Alternatives Considered**:
- Unicode identifiers (better for non-English users)
- No restrictions (maximum flexibility)

**Assumptions**:
- English identifiers sufficient for most users
- Compatibility > localization for DSL keywords

### Why Question Mark for Conditions?

**Why**: Clear visual marker for LLM evaluation.

**Alternatives Considered**:
- No marker (implicit condition)
- Keyword prefix (`if:`, `when:`)

**Assumptions**:
- Question format natural for LLMs
- Visual distinction helps human readers

---

## Related Files

- `README.md` - Quick start and examples
- `SYNTAX.ebnf` - Formal EBNF specification

---

## Version History

**Version 1.0** (2026-03-08):
- Initial specification
- 5 rules defined
- EBNF formalization complete

---

AUTHOR: Tracer (迹，Ji)
LICENSE: MIT
LAST UPDATED: 2026-03-08
