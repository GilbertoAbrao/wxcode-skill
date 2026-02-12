---
name: wxcode:dashboard
description: Generate project progress JSON and notify watchers
allowed-tools:
  - Bash
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
@~/.claude/wxcode-skill/references/dashboard-schema-project.md
@~/.claude/wxcode-skill/references/dashboard-schema-milestone.md
</execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"dashboard","args":"$ARGUMENTS","title":"WXCODE ▶ GENERATING DASHBOARD"} -->
## WXCODE ▶ GENERATING DASHBOARD
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"progress","args":"","description":"Check project progress","priority":"recommended"} -->
```
</structured_output>



<process>

## Step 0: Emit Header

```
<!-- WXCODE:HEADER:{"command":"dashboard","args":"$ARGUMENTS","title":"WXCODE ▶ GENERATING DASHBOARD"} -->
## WXCODE ▶ GENERATING DASHBOARD
```

## Step 1: Parse Arguments

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Parsing arguments","progress":5} -->
```

```bash
REGEN_ALL=""
[[ "$ARGUMENTS" == *"--all"* ]] && REGEN_ALL="--all"
```

## Step 2: Read Planning Files

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Reading planning files","progress":15} -->
```

Read and parse:
- `.planning/ROADMAP.md` — phases and requirements mapping
- `.planning/REQUIREMENTS.md` — requirement definitions
- `.planning/STATE.md` — current position
- `.planning/phases/*/` — plan files with tasks

Extract from ROADMAP.md:
- Phase numbers, names, goals
- Requirement mappings per phase
- Success criteria

Extract from PLAN.md files:
- Tasks from XML `<task>` blocks
- Wave assignments
- Dependencies

## Step 3: Generate Project Dashboard

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Generating project dashboard","progress":30} -->
```

Write `.planning/dashboard.json` following the project dashboard schema.

Emit notification:
```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json
```

## Step 4: Enrich with MCP Data (Conversion Projects Only)

**Skip if not a conversion project** (no `.planning/CONVERSION.md`).

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Getting MCP conversion stats","progress":45} -->
```

Call MCP to get conversion progress:
```
mcp__wxcode-kb__get_conversion_stats(project_name=PROJECT_NAME)
```

**Use MCP to get:**
- `elements_converted` — count of converted elements
- `elements_total` — total elements to convert

Update `.planning/dashboard.json` with these values in the `conversion` object.

## Step 5: Generate Milestone Dashboards (if --all)

**Skip if `--all` not specified.**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Generating milestone dashboards","progress":60} -->
```

For each milestone folder in `.planning/milestones/` or `.milestones/`:
1. Read milestone-specific ROADMAP.md, REQUIREMENTS.md
2. Parse PLAN.md files for tasks
3. Generate `dashboard_<milestone>.json`

Emit notification for each:
```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard_<milestone>.json
```

## Step 6: Regenerate Schema Dashboard (Conversion Projects + --all)

**Skip if not `--all` OR not a conversion project.**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Generating schema dashboard","progress":80} -->
```

Invoke `/wxcode:schema-dashboard` to:
1. Parse all ORM model files (SQLAlchemy, Prisma, TypeORM, etc.)
2. Compare against legacy schema from MCP
3. Generate `.planning/schema-dashboard.json` (for UI datamodel panel)
4. Generate `.planning/SCHEMA-STATUS.md` (human-readable)

## Step 7: Completion

```
<!-- WXCODE:STATUS:{"status":"completed","message":"All dashboards generated","progress":100} -->
```

Display summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DASHBOARDS REGENERATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Dashboard | Status |
|-----------|--------|
| Project | ✓ .planning/dashboard.json |
| v1.0-PAGE_Login | ✓ .planning/dashboard_v1.0-PAGE_Login.json |
| Schema (datamodel) | ✓ .planning/schema-dashboard.json |

Total: [N] dashboards updated
```

**Note:** Schema dashboard only appears for conversion projects with `--all` flag.

Emit final marker:
```
<!-- WXCODE:HEADER:{"command":"dashboard","args":"$ARGUMENTS","title":"WXCODE ► DASHBOARDS REGENERATED"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"progress","args":"","description":"Check project progress","priority":"recommended"} -->
```

</process>

<success_criteria>

- [ ] HEADER emitted at start
- [ ] STATUS emitted during each step
- [ ] Project dashboard JSON is valid
- [ ] Written to `.planning/dashboard.json`
- [ ] `[WXCODE:DASHBOARD_UPDATED]` notification emitted

**With --all:**
- [ ] All milestone dashboards regenerated
- [ ] Phases have nested `plans[]` arrays
- [ ] Plans have nested `tasks[]` arrays
- [ ] Progress calculated correctly
- [ ] Notification emitted for each dashboard

**Completion:**
- [ ] STATUS:completed emitted
- [ ] NEXT_ACTION emitted

**With --all (conversion projects):**
- [ ] Schema dashboard regenerated
- [ ] `.planning/schema-dashboard.json` created/updated
- [ ] `.planning/SCHEMA-STATUS.md` created/updated
- [ ] Coverage compared against legacy MCP schema

</success_criteria>

<troubleshooting>

**If dashboard is incomplete:**

1. Check `.planning/` structure exists
2. Verify ROADMAP.md has proper phase format
3. Check STATE.md for current position

**If tasks are empty:**

1. Check PLAN.md files use XML format: `<task><name>...</name></task>`
2. Check file naming: `01-01-PLAN.md` (not `1.1-PLAN.md`)
3. Check phases directory: `.planning/phases/01-*/`

**If MCP data missing (conversion projects):**

1. Check MCP wxcode-kb is connected: `/wxcode:mcp-health-check`
2. Verify project exists in MongoDB
3. Check `.planning/CONVERSION.md` has correct project reference

</troubleshooting>

<integration>

## When to Use --all

Use `/wxcode:dashboard --all` when:
- Dashboards are out of sync with actual files
- After manual edits to planning docs
- After schema migration
- For troubleshooting/recovery
- After git operations that modified .planning/
- After adding/modifying database models (regenerates schema dashboard)
- UI datamodel panel needs refresh

## Automatic Updates

Other commands should invoke `/wxcode:dashboard --all` after state changes:
- `/wxcode:new-milestone` — after milestone creation
- `/wxcode:execute-phase` — after phase completion
- `/wxcode:complete-milestone` — after milestone archival

</integration>
