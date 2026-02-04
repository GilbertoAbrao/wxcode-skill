---
name: wxcode:create-start-dev
description: Create start-dev.sh from stack template via MCP
allowed-tools:
  - Read
  - Write
  - Bash
  - Skill
  - mcp__wxcode-kb__*
---

<structured_output>
## Structured Output (MANDATORY)

**At command start:**
```
<!-- WXCODE:HEADER:{"command":"create-start-dev","args":"$ARGUMENTS","title":"WXCODE ▶ CREATING START-DEV"} -->
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"start-dev","args":"","description":"Start development server","priority":"recommended"} -->
```
</structured_output>

<objective>

Generate a `start-dev.sh` script for the current project based on its stack configuration stored in MongoDB.

**IMPORTANT:** ALWAYS recreate the file, even if it already exists. Never skip creation.

The script will:
- Kill any processes running on required ports
- Start development server(s) for the stack
- Redirect logs to `/tmp/{project_name}.log`
- Store PID files for process management

After creation, automatically execute `/wxcode:start-dev` to start the server.

</objective>

<process>

## Phase 0: MCP Health Check (Precondition)

**Before proceeding, verify MCP wxcode-kb is available.**

**Attempt 1:** Call `mcp__wxcode-kb__health_check`

**If success:** Continue to Phase 1.

**If fails:** Wait 10 seconds, then **Attempt 2**

**Attempt 2:** Call `mcp__wxcode-kb__health_check`

**If success:** Continue to Phase 1.

**If fails:** Wait 10 seconds, then **Attempt 3**

**Attempt 3:** Call `mcp__wxcode-kb__health_check`

**If success:** Continue to Phase 1.

**If fails after 3 attempts:**

```
╔══════════════════════════════════════════════════════════════╗
║  ERROR: MCP wxcode-kb not available                          ║
╚══════════════════════════════════════════════════════════════╝

This command requires the wxcode-kb MCP server.

**To fix:**
1. Ensure wxcode-kb MCP server is running
2. Verify MCP is configured in Claude Code settings
3. Restart Claude Code if recently configured

**Cannot proceed without MCP.**
```

**STOP and abort command.**

---

## Phase 1: Identify Project Stack

**1.1 Find stack configuration:**

Check for stack info in order of precedence:

```
1. .planning/CONVERSION.md → output_project.stack_id field
2. PROJECT.md → Stack field in metadata
3. pyproject.toml / package.json → infer from dependencies
```

Read the relevant file:

```bash
# Check CONVERSION.md first (conversion projects)
if [ -f ".planning/CONVERSION.md" ]; then
  grep -E "stack_id|stack:" .planning/CONVERSION.md
fi

# Then PROJECT.md (standard projects)
if [ -f "PROJECT.md" ]; then
  grep -E "^Stack:|stack_id:" PROJECT.md
fi
```

Extract the `stack_id` value (e.g., `fastapi-jinja2`, `nextjs-app-router`, etc.)

**1.2 Validate stack:**

If no stack found:
```
Error: Could not determine project stack.

Ensure one of these files exists with stack info:
- .planning/CONVERSION.md (with stack_id field)
- PROJECT.md (with Stack field)

Available stacks:
- Server-Rendered: fastapi-jinja2, fastapi-htmx, django-templates, rails-erb, laravel-blade
- SPA: fastapi-react, fastapi-vue, nestjs-react, nestjs-vue, laravel-react
- Fullstack: nextjs-app-router, nextjs-pages, nuxt3, sveltekit, remix
```
Exit.

## Phase 2: Fetch Stack Conventions via MCP

**2.1 Get stack conventions (includes start_dev_template):**

```
mcp__wxcode-kb__get_stack_conventions:
  stack_id: "<DETECTED_STACK_ID>"
```

**2.2 Extract template data from response:**

From the `start_dev_template` field in the response, get:
- `start_dev_template.ports.backend` → PORT_BACKEND
- `start_dev_template.ports.frontend` → PORT_FRONTEND (if SPA)
- `start_dev_template.script` → Template script

**2.3 Handle missing template:**

If `start_dev_template` not found:
```
Error: No start-dev template found for stack '[STACK_ID]'.

The stack exists but has no start_dev_template configured.
Please add the template to the stacks collection in MongoDB.
```
Exit.

## Phase 3: Generate Script

**3.1 Substitute placeholders with actual values:**

The template script contains placeholders. Replace them with the actual port numbers from `start_dev_template.ports`:

| Placeholder | Replace with |
|-------------|--------------|
| `{{PORT_BACKEND}}` | `start_dev_template.ports.backend` (e.g., `7300`) |
| `{{PORT_FRONTEND}}` | `start_dev_template.ports.frontend` (e.g., `7381`) |

**Example transformation:**

Template line:
```bash
PORT={{PORT_BACKEND}}
```

After substitution (for fastapi-jinja2 with port 7300):
```bash
PORT=7300
```

**IMPORTANT:** The final start-dev.sh must have NO placeholders remaining. All `{{...}}` must be replaced with actual values.

**3.2 Write the file:**

Use the Write tool to create `start-dev.sh` in the project root with the fully substituted script content.

**3.3 Set permissions:**

```bash
chmod +x start-dev.sh
```

## Phase 4: Display Result

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► CREATE-START-DEV
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Created start-dev.sh

## Configuration

| Property | Value |
|----------|-------|
| Stack | [STACK_ID] |
| Backend Port | [PORT_BACKEND] |
| Frontend Port | [PORT_FRONTEND or N/A] |
| Log File | /tmp/[PROJECT_NAME].log |

## Usage

./start-dev.sh          # Start server(s)
/wxcode:start-dev       # Or use the skill

## Access URLs

[For single-server stacks:]
http://localhost:[PORT_BACKEND]

[For SPA stacks:]
http://localhost:[PORT_FRONTEND] (frontend)
http://localhost:[PORT_BACKEND] (API)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Phase 5: Start Development Server

After displaying the result, automatically invoke:

```
/wxcode:start-dev
```

This starts the development server immediately after script creation.

</process>

<output>

Creates `start-dev.sh` in project root with:
- Executable permissions (chmod +x)
- Port configuration from stack template
- Process management (kill existing, save PIDs)
- Log redirection to /tmp/

</output>

<success_criteria>

- [ ] Project stack identified from config files
- [ ] Template fetched from MongoDB via MCP
- [ ] Placeholders substituted with actual ports
- [ ] start-dev.sh created (ALWAYS, even if exists)
- [ ] Permissions set (chmod +x)
- [ ] Configuration summary displayed
- [ ] /wxcode:start-dev invoked automatically

</success_criteria>
