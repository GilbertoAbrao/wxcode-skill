---
name: wxcode:dashboard
description: Generate project progress JSON and notify watchers
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - mcp__wxcode-kb__*
---

<objective>

Generate comprehensive JSON snapshots of project progress for external UI rendering.

**Usage:**
- `/wxcode:dashboard` — Regenerate project dashboard only
- `/wxcode:dashboard --all` — Regenerate project + ALL milestone dashboards

**Two Dashboard Types:**

1. **Project Dashboard** (`.planning/dashboard.json`)
   - Global view of all milestones
   - Conversion progress from MCP
   - Created/updated by this command

2. **Milestone Dashboard** (`.planning/dashboard_<milestone>.json`)
   - Detailed phases, plans, tasks for ONE milestone
   - Workflow stages tracking
   - Created/updated by milestone-specific commands OR `--all` flag

**Output:**
1. Writes JSON to `.planning/dashboard.json`
2. With `--all`: Also writes each `.planning/dashboard_<milestone>.json`
3. Emits watcher notification for each updated file

**Use case:** IDE integrations, dashboards, progress visualization, file watchers, recovery after desync

</objective>

<execution_context>
@~/.claude/get-shit-done/references/dashboard-schema-project.md
@~/.claude/get-shit-done/references/dashboard-schema-milestone.md
</execution_context>

<project_dashboard_schema>

```json
{
  "project": {
    "name": "string - from PROJECT.md",
    "core_value": "string - from PROJECT.md",
    "description": "string - from PROJECT.md"
  },
  "conversion": {
    "is_conversion_project": "boolean",
    "elements_converted": "number | null - FROM MCP (source of truth)",
    "elements_total": "number | null - FROM MCP (source of truth)",
    "stack": "string | null - from CONVERSION.md"
  },
  "milestones": [
    {
      "folder_name": "string - e.g., 'v1.0-PAGE_Login'",
      "mongodb_id": "string | null",
      "wxcode_version": "string - e.g., 'v1.0'",
      "element_name": "string - e.g., 'PAGE_Login'",
      "status": "pending | in_progress | completed | failed",
      "created_at": "ISO8601 string",
      "completed_at": "ISO8601 string | null"
    }
  ],
  "current_milestone": "string | null - folder_name of active milestone",
  "progress": {
    "milestones_complete": "number",
    "milestones_total": "number",
    "milestones_percentage": "number (0-100)"
  },
  "meta": {
    "generated_at": "ISO8601 string",
    "wxcode_version": "string"
  }
}
```

</project_dashboard_schema>

<milestone_dashboard_schema>

```json
{
  "milestone": {
    "folder_name": "string",
    "mongodb_id": "string | null",
    "wxcode_version": "string",
    "element_name": "string",
    "status": "pending | in_progress | completed | failed",
    "created_at": "ISO8601 string",
    "completed_at": "ISO8601 string | null"
  },
  "workflow": {
    "current_stage": "string",
    "stages": [
      { "id": "created", "name": "Milestone Created", "status": "pending|in_progress|complete", "completed_at": "ISO8601|null" },
      { "id": "requirements", "name": "Requirements Defined", "status": "...", "completed_at": "..." },
      { "id": "roadmap", "name": "Roadmap Created", "status": "...", "completed_at": "..." },
      { "id": "planning", "name": "All Phases Planned", "status": "...", "completed_at": "..." },
      { "id": "executing", "name": "Execution In Progress", "status": "...", "completed_at": "..." },
      { "id": "verified", "name": "Work Verified", "status": "...", "completed_at": "..." },
      { "id": "archived", "name": "Milestone Archived", "status": "...", "completed_at": "..." }
    ]
  },
  "current_position": {
    "phase_number": "number | null",
    "phase_name": "string | null",
    "plan_number": "string | null",
    "plan_total": "number | null",
    "status": "not_started | in_progress | complete | blocked"
  },
  "progress": {
    "phases_complete": "number",
    "phases_total": "number",
    "phases_percentage": "number",
    "plans_complete": "number",
    "plans_total": "number",
    "plans_percentage": "number",
    "tasks_complete": "number",
    "tasks_total": "number",
    "tasks_percentage": "number",
    "requirements_complete": "number",
    "requirements_total": "number",
    "requirements_percentage": "number"
  },
  "phases": [
    {
      "number": "number",
      "name": "string",
      "goal": "string",
      "status": "pending | in_progress | complete",
      "requirements_covered": ["REQ-ID"],
      "plans": [
        {
          "number": "string",
          "name": "string",
          "status": "pending | in_progress | complete",
          "summary": "string | null",
          "tasks": [
            {
              "id": "string",
              "name": "string",
              "file": "string | null",
              "status": "pending | in_progress | complete",
              "description": "string"
            }
          ]
        }
      ]
    }
  ],
  "requirements": {
    "total": "number",
    "complete": "number",
    "categories": [...]
  },
  "blockers": [],
  "meta": {
    "generated_at": "ISO8601 string",
    "wxcode_version": "string"
  }
}
```

</milestone_dashboard_schema>

<process>

## Step 0: Parse Arguments

```bash
REGEN_ALL=false
[[ "$ARGUMENTS" == *"--all"* ]] && REGEN_ALL=true
```

## Step 1: Check Project Exists

```bash
[ -f .planning/PROJECT.md ] || echo "ERROR: No project found" && exit 1
```

If no project, output error and STOP.

## Step 2: Detect Project Type

```bash
IS_CONVERSION=false
[ -f .planning/CONVERSION.md ] && IS_CONVERSION=true
```

## Step 3: Gather Project Data

**Read PROJECT.md:**
- Extract project name (first H1 or "Name:" field)
- Extract "Core Value" section
- Extract "What This Is" section for description

## Step 4: Gather Conversion Data (if conversion project)

**Use MCP as Source of Truth:**

```
mcp__wxcode-kb__get_conversion_stats(project_name=PROJECT_NAME)
```

- `elements_converted` → from MCP response
- `elements_total` → from MCP response

**Read CONVERSION.md:**
- Extract `stack` (target stack ID)

## Step 5: Find All Milestones

**Scan for milestone folders:**

```bash
# Active milestones (in .planning/milestones/ subfolders with ROADMAP.md)
find .planning/milestones -name "ROADMAP.md" -type f 2>/dev/null | xargs -I {} dirname {}

# Also check for current milestone folder pattern
ls -d .planning/v*-* 2>/dev/null
```

Build list of milestone folders to process.

## Step 6: Build Milestones Array for Project Dashboard

For each milestone folder found:

1. **Parse folder name:**
   - `v1.0-PAGE_Login` → wxcode_version=`v1.0`, element_name=`PAGE_Login`

2. **Determine status:**
   - Check if in `.planning/milestones/` (archived) → `completed`
   - Check for SUMMARY.md files → `in_progress` or `completed`
   - Otherwise → `pending`

3. **Get mongodb_id (if available):**
   - Read existing `dashboard_<milestone>.json` if exists
   - Or leave as null

4. **Get timestamps:**
   - `created_at`: folder creation time or first commit
   - `completed_at`: if status=completed, last modification time

Add to `milestones[]` array.

## Step 7: Determine Current Milestone

**From `.planning/STATE.md`:**
- Look for "Current Milestone" or "Current Position" section
- Or find latest `in_progress` milestone

## Step 8: Calculate Project Progress

```
milestones_complete = count where status == "completed"
milestones_total = total count
milestones_percentage = (complete / total) * 100
```

## Step 9: Get WXCODE Version

```bash
cat ~/.claude/get-shit-done/VERSION 2>/dev/null || echo "unknown"
```

## Step 10: Write Project Dashboard

Write to `.planning/dashboard.json` following schema.

Output notification:
```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json
```

---

## Step 11: Regenerate Milestone Dashboards (if --all)

**If REGEN_ALL=false:** STOP here.

**If REGEN_ALL=true:** Continue for each milestone found.

### For Each Milestone:

#### 11.1: Set Milestone Context

**Detect milestone folder structure:**

```bash
# Two possible structures:
#
# Structure A: Nested milestone folder
#   .planning/v1.0-PAGE_Login/ROADMAP.md
#   .planning/v1.0-PAGE_Login/phases/01-*/
#
# Structure B: Flat structure (single active milestone)
#   .planning/ROADMAP.md
#   .planning/phases/01-*/

# Detect which structure exists:
if [ -d ".planning/${MILESTONE_NAME}" ]; then
  # Structure A: Nested milestone folder
  MILESTONE_FOLDER=".planning/${MILESTONE_NAME}"
elif [ -f ".planning/ROADMAP.md" ]; then
  # Structure B: Flat structure
  MILESTONE_FOLDER=".planning"
else
  echo "ERROR: Cannot determine milestone folder structure"
fi
```

**For archived milestones:**
```bash
MILESTONE_FOLDER=".planning/milestones/${MILESTONE_NAME}"
```

#### 11.2: Detect Workflow Stages

**Locate key files (structure-aware):**

```bash
# ROADMAP.md location
ROADMAP_PATH="${MILESTONE_FOLDER}/ROADMAP.md"

# REQUIREMENTS.md location
REQUIREMENTS_PATH="${MILESTONE_FOLDER}/REQUIREMENTS.md"

# Phases directory
if [ -d "${MILESTONE_FOLDER}/phases" ]; then
  PHASES_DIR="${MILESTONE_FOLDER}/phases"
elif [ -d ".planning/phases" ]; then
  PHASES_DIR=".planning/phases"
fi
```

**Stage Status Logic:**

| Stage | Status: complete | Status: in_progress |
|-------|------------------|---------------------|
| `created` | Folder exists | — |
| `requirements` | REQUIREMENTS.md exists with content | — |
| `roadmap` | ROADMAP.md exists with phases | — |
| `planning` | ALL phases have at least one PLAN.md | SOME phases have PLAN.md |
| `executing` | ALL phases have SUMMARY.md | SOME phases have SUMMARY.md (but not all) |
| `verified` | UAT.md exists with status "passed" | — |
| `archived` | In `.planning/milestones/` folder | — |

**Determine `current_stage`:**

1. Find the first stage with status `in_progress` → that's current
2. If no `in_progress`, find first stage with status `pending` → that's current
3. If all stages complete → current_stage = "archived"

**Example:** 3 of 4 phases have SUMMARY.md:
- `planning` = complete (all have PLAN.md)
- `executing` = in_progress (some but not all have SUMMARY.md)
- `current_stage` = "executing"

#### 11.3: Parse ROADMAP.md

**ROADMAP.md already located in 11.2:**
```bash
ROADMAP_PATH="${MILESTONE_FOLDER}/ROADMAP.md"
# Structure A: .planning/v1.0-PAGE_Login/ROADMAP.md
# Structure B: .planning/ROADMAP.md
# Archived: .planning/milestones/v1.0-PAGE_Login/ROADMAP.md
```

**Extract phases from ROADMAP.md:**

Look for phase sections or tables:
```markdown
## Phases

### Phase 1: Database Model
**Goal:** Create AcessoUsuario model for user authentication

### Phase 2: Authentication Service
**Goal:** Implement login validation logic
```

Or table format:
```markdown
| # | Phase | Goal | Requirements |
|---|-------|------|--------------|
| 1 | Database Model | Create AcessoUsuario model | DATA-01, DATA-02 |
| 2 | Authentication Service | Implement login validation | AUTH-01, AUTH-02 |
```

For each phase, gather:
- number, name, goal
- requirements_covered (from table or section)
- Initialize `plans: []` array (populated in next step)

#### 11.4: Parse PLAN.md Files

**CRITICAL: Locate PLAN.md files in correct path.**

**Detect phases directory (two possible structures):**

```bash
# Structure A: Nested milestone (phases inside milestone folder)
# .planning/v1.0-PAGE_Login/phases/01-*/

# Structure B: Flat structure (phases directly in .planning)
# .planning/phases/01-*/

# Detect which structure exists:
if [ -d "${MILESTONE_FOLDER}/phases" ]; then
  PHASES_DIR="${MILESTONE_FOLDER}/phases"
elif [ -d ".planning/phases" ]; then
  PHASES_DIR=".planning/phases"
else
  echo "ERROR: No phases directory found"
  exit 1
fi
```

**For each phase, find its plans:**

```bash
# List phase directories
ls -d ${PHASES_DIR}/0*-*/

# Example structures:
#
# Structure A (nested):
# .planning/v1.0-PAGE_Login/phases/
#   01-database-model/
#     1.1-PLAN.md
#     1.1-SUMMARY.md
#
# Structure B (flat):
# .planning/phases/
#   01-database-model/
#     1.1-PLAN.md
#     1.1-SUMMARY.md
```

**For each phase directory:**

```bash
# Find all PLAN.md files in this phase
ls ${PHASES_DIR}/01-database-model/*-PLAN.md
```

**For each `*-PLAN.md` file found:**

1. **Extract plan number** from filename:
   - `1.1-PLAN.md` → plan number = `"1.1"`
   - `2.1-PLAN.md` → plan number = `"2.1"`

2. **Extract plan name** from frontmatter or first heading:
   ```yaml
   ---
   name: Database Layer
   wave: 1
   ---
   ```
   Or from `# Database Layer` heading.

3. **Check for SUMMARY.md** to determine status:
   ```bash
   # If 1.1-SUMMARY.md exists → plan is complete
   [ -f "${PHASE_DIR}/1.1-SUMMARY.md" ] && PLAN_STATUS="complete" || PLAN_STATUS="pending"
   ```

4. **Parse `<task>` XML blocks** from PLAN.md content.

**Task parsing (XML format):**

Tasks in PLAN.md files use XML format:

```xml
<task type="auto">
  <name>Task 1: Create AcessoUsuario Model</name>
  <files>app/models/acesso_usuario.py</files>
  <action>
    Create SQLAlchemy model for the AcessoUsuario table...
  </action>
  <verify>python -c "from app.models import AcessoUsuario"</verify>
  <done>Model created with all columns</done>
</task>

<task type="auto">
  <name>Task 2: Update Models Init</name>
  <files>app/models/__init__.py</files>
  <action>Export AcessoUsuario from package</action>
  <verify>Import works</verify>
  <done>Model exported</done>
</task>
```

**For each `<task>` block, extract:**

1. **id**: Generate from plan number + task sequence
   - First task in plan 1.1 → `"1.1.1"`
   - Second task in plan 1.1 → `"1.1.2"`
   - First task in plan 2.1 → `"2.1.1"`

2. **name**: Content of `<name>` tag (strip "Task N: " prefix)

3. **file**: First file from `<files>` tag

4. **status**: Same as plan status (complete if SUMMARY.md exists)

5. **description**: Content of `<action>` tag (first line)

**Build plan object with tasks:**

```json
{
  "number": "1.1",
  "name": "Database Layer",
  "status": "complete",
  "summary": "Created AcessoUsuario model",
  "tasks": [
    {
      "id": "1.1.1",
      "name": "Create AcessoUsuario Model",
      "file": "app/models/acesso_usuario.py",
      "status": "complete",
      "description": "Create SQLAlchemy model for the AcessoUsuario table"
    },
    {
      "id": "1.1.2",
      "name": "Update Models Init",
      "file": "app/models/__init__.py",
      "status": "complete",
      "description": "Export AcessoUsuario from package"
    }
  ]
}
```

**Add plan to phase's `plans[]` array.**

**Repeat for all phases and all plans.**

#### 11.5: Parse REQUIREMENTS.md

Extract requirements by category:
```markdown
### Authentication
- [x] **AUTH-01**: User can login
- [ ] **AUTH-02**: User can logout
```

Build requirements object with completion status.

#### 11.6: Determine Current Position

From STATE.md or by scanning:
- Find first incomplete phase
- Find first incomplete plan in that phase
- Set status accordingly

#### 11.7: Calculate Milestone Progress

**Count from populated `phases[]` array built in previous steps:**

```javascript
// Phases
phases_total = phases.length
phases_complete = phases.filter(p => p.status === "complete").length
phases_percentage = Math.round((phases_complete / phases_total) * 100)

// Plans (flatten all phases)
plans_total = phases.reduce((sum, p) => sum + p.plans.length, 0)
plans_complete = phases.reduce((sum, p) =>
  sum + p.plans.filter(pl => pl.status === "complete").length, 0)
plans_percentage = plans_total > 0 ? Math.round((plans_complete / plans_total) * 100) : 0

// Tasks (flatten all plans from all phases)
tasks_total = phases.reduce((sum, p) =>
  sum + p.plans.reduce((s, pl) => s + pl.tasks.length, 0), 0)
tasks_complete = phases.reduce((sum, p) =>
  sum + p.plans.reduce((s, pl) =>
    s + pl.tasks.filter(t => t.status === "complete").length, 0), 0)
tasks_percentage = tasks_total > 0 ? Math.round((tasks_complete / tasks_total) * 100) : 0

// Requirements (from REQUIREMENTS.md parsing)
requirements_total = count all requirement items
requirements_complete = count [x] checked items
requirements_percentage = Math.round((requirements_complete / requirements_total) * 100)
```

**CRITICAL:** If `plans_total` or `tasks_total` is 0, check that:
1. PLAN.md files were found in `${MILESTONE_FOLDER}/phases/*/`
2. Task XML blocks were parsed correctly from PLAN.md content

#### 11.8: Write Milestone Dashboard

Write to `.planning/dashboard_<milestone>.json`

Output notification:
```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard_<milestone>.json
```

---

## Step 12: Summary

Display summary of what was regenerated:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DASHBOARDS REGENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Dashboard | Status |
|-----------|--------|
| Project | ✓ .planning/dashboard.json |
| v1.0-PAGE_Login | ✓ .planning/dashboard_v1.0-PAGE_Login.json |
| v1.1-PAGE_Dashboard | ✓ .planning/dashboard_v1.1-PAGE_Dashboard.json |

Total: [N] dashboards updated
```

</process>

<success_criteria>

**Basic (no --all):**
- [ ] Project dashboard JSON is valid
- [ ] Written to `.planning/dashboard.json`
- [ ] Notification emitted
- [ ] Conversion data from MCP (not inferred)
- [ ] Milestones array populated from folder scan

**With --all:**
- [ ] All milestone folders discovered
- [ ] Each milestone dashboard regenerated from source files
- [ ] Workflow stages correctly detected
- [ ] Phases parsed from ROADMAP.md
- [ ] Plans parsed from PLAN.md files
- [ ] Tasks extracted from plan files
- [ ] Requirements parsed with completion status
- [ ] Progress calculated correctly
- [ ] Notification emitted for each dashboard
- [ ] Summary displayed

</success_criteria>

<integration>

## When to Use --all

Use `/wxcode:dashboard --all` when:
- Dashboards are out of sync with actual files
- After manual edits to planning docs
- After schema migration
- For troubleshooting/recovery
- After git operations that modified .planning/

## Automatic Updates

Individual commands still update dashboards incrementally:
- `/wxcode:new-milestone` → creates milestone dashboard
- `/wxcode:plan-phase` → updates plans/tasks
- `/wxcode:execute-phase` → updates task status
- `/wxcode:complete-milestone` → archives milestone

Use `--all` for full regeneration when needed.

</integration>
