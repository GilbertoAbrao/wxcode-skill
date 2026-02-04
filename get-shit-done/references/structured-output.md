# WXCODE Structured Output Format

Reference for emitting structured output that external parsers can consume.

## Purpose

WXCODE commands emit structured data alongside human-readable markdown to enable:
- Chat interfaces to render rich UI components
- Dashboards to track progress in real-time
- Log parsers to extract semantic information
- Automation tools to react to state changes

## Format

All structured output uses HTML comments (invisible in markdown renderers):

```
<!-- WXCODE:TYPE:JSON_PAYLOAD -->
```

Where:
- `TYPE` is one of: `HEADER`, `TOOL`, `TOOL_RESULT`, `STATUS`, `NEXT_ACTION`, `ERROR`
- `JSON_PAYLOAD` is a single-line JSON object (no newlines)

---

## Output Types

### HEADER

Emitted at the start of a command execution.

```markdown
<!-- WXCODE:HEADER:{"command":"execute-phase","args":"10","title":"WXCODE ▶ EXECUTING PHASE 10"} -->

## WXCODE ▶ EXECUTING PHASE 10
```

**Schema:**
```json
{
  "command": "string",      // Command name without /wxcode: prefix
  "args": "string|null",    // Arguments passed
  "title": "string",        // Human-readable title
  "phase": "number|null",   // Phase number if applicable
  "plan": "string|null"     // Plan ID if applicable
}
```

### TOOL

Emitted before a tool call.

```markdown
<!-- WXCODE:TOOL:{"tool":"Bash","description":"Get model profile","command":"cat .planning/config.json"} -->

**Running:** Get model profile
```

**Schema:**
```json
{
  "tool": "string",         // Tool name: Bash, Read, Write, Edit, MCP, etc.
  "description": "string",  // Human-readable description
  "command": "string|null", // For Bash: the command
  "file": "string|null",    // For Read/Write/Edit: the file path
  "mcp_tool": "string|null" // For MCP: the tool name
}
```

### TOOL_RESULT

Emitted after a tool completes.

```markdown
<!-- WXCODE:TOOL_RESULT:{"tool":"Bash","success":true,"output":"balanced","duration_ms":45} -->
```

**Schema:**
```json
{
  "tool": "string",         // Tool name
  "success": "boolean",     // Whether tool succeeded
  "output": "string|null",  // Truncated output (max 200 chars)
  "error": "string|null",   // Error message if failed
  "duration_ms": "number"   // Execution time
}
```

### STATUS

Emitted when execution status changes.

```markdown
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing task 3 of 5","progress":60} -->

⏳ Executing task 3 of 5...
```

**Schema:**
```json
{
  "status": "string",       // pending, in_progress, completed, failed, paused
  "message": "string",      // Human-readable status message
  "progress": "number|null",// Percentage 0-100 if applicable
  "task": "string|null",    // Current task name
  "phase": "number|null",   // Current phase
  "plan": "string|null"     // Current plan
}
```

### NEXT_ACTION

Emitted at the end of a command with suggested next steps.

```markdown
<!-- WXCODE:NEXT_ACTION:{"command":"verify-work","description":"Validate the implemented features"} -->

**Next:** `/wxcode:verify-work` — Validate the implemented features
```

**Schema:**
```json
{
  "command": "string",      // Suggested command (without /wxcode: prefix)
  "args": "string|null",    // Suggested arguments
  "description": "string",  // Why this is the next step
  "priority": "string"      // required, recommended, optional
}
```

### ERROR

Emitted when an error occurs.

```markdown
<!-- WXCODE:ERROR:{"code":"MCP_UNAVAILABLE","message":"Cannot connect to wxcode-kb MCP server"} -->

❌ **Error:** Cannot connect to wxcode-kb MCP server
```

**Schema:**
```json
{
  "code": "string",         // Error code for programmatic handling
  "message": "string",      // Human-readable error message
  "recoverable": "boolean", // Whether execution can continue
  "suggestion": "string|null" // How to fix the error
}
```

---

## Usage in Commands

### Emitting Structured Output

In command markdown files, emit structured output before the human-readable version:

```markdown
<!-- WXCODE:HEADER:{"command":"plan-phase","args":"3","title":"WXCODE ▶ PLANNING PHASE 3"} -->

## WXCODE ▶ PLANNING PHASE 3

Let me analyze the phase requirements and create a detailed plan.

<!-- WXCODE:TOOL:{"tool":"Read","description":"Load roadmap","file":".planning/ROADMAP.md"} -->

**Reading:** `.planning/ROADMAP.md`

<!-- WXCODE:TOOL_RESULT:{"tool":"Read","success":true,"duration_ms":12} -->

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Creating plan","progress":50} -->

⏳ Creating plan...

[... plan content ...]

<!-- WXCODE:STATUS:{"status":"completed","message":"Plan created successfully","progress":100} -->

✅ **Plan created:** `.planning/phases/03/01-PLAN.md`

<!-- WXCODE:NEXT_ACTION:{"command":"execute-phase","args":"3","description":"Execute the planned tasks","priority":"recommended"} -->

**Next:** `/wxcode:execute-phase 3` — Execute the planned tasks
```

### Parsing Structured Output

External parsers can extract structured data with regex:

```javascript
const WXCODE_PATTERN = /<!-- WXCODE:(\w+):({.*?}) -->/g;

function parseWxcodeOutput(markdown) {
  const events = [];
  let match;

  while ((match = WXCODE_PATTERN.exec(markdown)) !== null) {
    events.push({
      type: match[1],
      data: JSON.parse(match[2])
    });
  }

  return events;
}
```

```python
import re
import json

WXCODE_PATTERN = r'<!-- WXCODE:(\w+):({.*?}) -->'

def parse_wxcode_output(markdown: str) -> list[dict]:
    events = []
    for match in re.finditer(WXCODE_PATTERN, markdown):
        events.append({
            'type': match.group(1),
            'data': json.loads(match.group(2))
        })
    return events
```

---

## Best Practices

1. **Always emit both** - Structured output AND human-readable markdown
2. **Keep JSON single-line** - No newlines in JSON payload
3. **Truncate long outputs** - Max 200 chars in `output` fields
4. **Use consistent status values** - pending, in_progress, completed, failed, paused
5. **Include timing** - `duration_ms` helps with performance tracking
6. **Emit HEADER first** - Every command should start with a HEADER

---

## Error Codes

| Code | Description |
|------|-------------|
| `MCP_UNAVAILABLE` | MCP server not connected |
| `FILE_NOT_FOUND` | Required file missing |
| `PHASE_NOT_FOUND` | Phase doesn't exist in roadmap |
| `PLAN_NOT_FOUND` | Plan file not found |
| `GIT_DIRTY` | Uncommitted changes blocking operation |
| `VALIDATION_FAILED` | Plan or phase validation failed |
| `AUTH_REQUIRED` | Authentication gate encountered |
| `TOOL_FAILED` | Tool execution failed |
