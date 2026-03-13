# Agent Integration Guide

Purpose: Guide for external LLM agents integrating with workflow-as-list.

Last Updated: 2026-03-13
REFERENCE: principles/communication/prompt-engineering/README.md

---

## Execution Model Overview

workflow-as-list is a **reader**, not an executor.

### Progressive Reading Design

Agent workflow follows progressive reading pattern:

1. Read current step content
2. Understand and execute operations
3. Advance to next step
4. Repeat until completion

Key constraint: Cannot advance without reading first.

### Reader Metaphor

Like reading a book:
- Open to current page (read)
- Read and understand
- Turn page when ready (next)
- Cannot skip unread pages (enforced)

---

## CLI Integration

### Start Execution

```bash
workflow run <workflow-name>
# Returns: execution_id (e.g., commit-abc123)
```

### Read Current Step

```bash
workflow exec read <execution-id>
# Displays:
# - Step content
# - Step metadata (comments)
# - Marks step as read
```

### Advance to Next Step

```bash
workflow exec next <execution-id>
# Checks: Current step must be read first
# Advances: current_step counter
# Returns: Progress confirmation
```

### Example Session

```bash
# Start
workflow run commit
# Output: Execution started: commit-abc123

# Read step 1
workflow exec read commit-abc123
# Output: Step 1/23: Analyze changed files...

# Agent executes: git diff --cached --name-only

# Advance
workflow exec next commit-abc123
# Output: Advanced to step 2/23

# Repeat...
```

---

## API Integration

### Create Execution

```http
POST /workflows/{name}/run
```

Response:
```json
{
  "execution_id": "commit-abc123",
  "workflow_name": "commit",
  "status": "pending",
  "current_step": 0,
  "steps_total": 23
}
```

### Get Execution Status

```http
GET /executions/{execution_id}
```

Response:
```json
{
  "execution_id": "commit-abc123",
  "workflow_name": "commit",
  "status": "running",
  "current_step": 5,
  "steps_read": [0, 1, 2, 3, 4],
  "steps_total": 23
}
```

### Advance Step

```http
POST /executions/{execution_id}/next
Content-Type: application/json

{}
```

NOTE: API checks if current_step is in steps_read before advancing.

Response:
```json
{
  "current_step": {...},
  "next_step": {...},
  "step_index": 6,
  "steps_total": 23,
  "completed": false
}
```

---

## Agent Workflow (Pseudocode)

```python
def execute_workflow(workflow_name: str):
    # 1. Create execution
    execution = POST /workflows/{name}/run
    execution_id = execution["execution_id"]
    
    while True:
        # 2. Read current step
        step_content = read_step(execution_id)
        
        # 3. Understand and execute
        result = agent_execute(step_content)
        
        # 4. Store output (optional)
        store_output(execution_id, step_index, result)
        
        # 5. Advance to next step
        response = POST /executions/{id}/next
        
        # 6. Check completion
        if response["completed"]:
            break
```

---

## Output Storage

Location: `~/.workflow-as-list/outputs/{execution_id}/{step_index}.txt`

Agent writes outputs directly:
```python
output_path = f"~/.workflow-as-list/outputs/{execution_id}/{step}.txt"
with open(output_path, "w") as f:
    f.write(output_content)
```

Why separate files:
- Output may be large
- Keep execution JSON small
- Enable streaming

---

## Best Practices

### Read Before Next

Always read current step before advancing:
```python
# Correct
read_step(execution_id)
execute_operations()
advance_step(execution_id)

# Wrong (will fail)
advance_step(execution_id)  # Error: step not read
```

### Store Outputs Per Step

Store output after each step completes:
```python
for step in workflow:
    result = execute(step)
    store_output(execution_id, step_index, result)
```

### Handle Interruptions

Execution state persists. Agent can resume:
```python
execution = get_execution(execution_id)
current_step = execution["current_step"]
# Resume from current_step
```

### Check Steps Read

Verify progressive reading:
```python
execution = get_execution(execution_id)
if current_step not in execution["steps_read"]:
    raise Error("Must read current step first")
```

---

## Error Handling

### Step Not Read

```
Error: Current step not read yet
Next: Read first: workflow exec read <id>
```

Solution: Call `read` before `next`.

### Execution Not Found

```
Error: Execution not found: <id>
```

Solution: Check execution_id, or create new execution.

### Workflow Not Found

```
Error: Workflow not found: <name>
```

Solution: Check workflow name, run `workflow list` to see available.

---

## Related

- README.md — Overview and CLI reference
- docs/design/runtime/007-execution.md — Execution state design
- docs/design/cli/003-commands.md — CLI commands
- principles/communication/prompt-engineering/ — Documentation standards
