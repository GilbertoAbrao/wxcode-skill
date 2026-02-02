# Dashboard Schema Migration — Prompt for UI Agent

## Context

The WXCODE dashboard system has been redesigned to support conversion projects with multiple milestones. The previous single-dashboard approach has been split into two separate schemas.

## What Changed

### Before (Single Dashboard)

```
.planning/
└── dashboard.json    # Everything in one file
```

Single schema mixing project-level and milestone-level data.

### After (Split Dashboards)

```
.planning/
├── dashboard.json                      # Project-level (global)
├── dashboard_v1.0-PAGE_Login.json      # Milestone-specific
├── dashboard_v1.1-PAGE_Dashboard.json  # Milestone-specific
└── ...
```

Two separate schemas with clear responsibilities.

---

## Schema Differences

### Project Dashboard (`dashboard.json`)

**Purpose:** Global view of the conversion project.

**Key fields:**
- `project`: Name, core value, description
- `conversion`: Progress from MCP (elements_converted, elements_total), stack
- `milestones[]`: List of all milestones with status
- `current_milestone`: Which milestone is active
- `progress`: Aggregated milestone progress

**Does NOT contain:**
- Individual phases
- Requirements details
- Plan-level information

### Milestone Dashboard (`dashboard_<milestone>.json`)

**Purpose:** Detailed view of a single milestone's execution.

**Key fields:**
- `milestone`: Folder name, mongodb_id, element_name, status
- `current_position`: Phase/plan being worked on
- `phases[]`: Detailed phase and plan information
- `requirements`: Categorized requirements with completion status
- `progress`: Phase and requirement progress for THIS milestone

**Does NOT contain:**
- Other milestones
- Project-level conversion stats

---

## MongoDB Integration

### New Field in Milestone Model

Add these fields to the `Milestone` model:

```python
wxcode_version: Optional[str]       # e.g., "v1.0"
milestone_folder_name: Optional[str] # e.g., "v1.0-PAGE_Login"
```

### New MCP Tool Required

Create `create_milestone` tool with parameters:
- `output_project_id` (string, required)
- `element_name` (string, required)
- `element_id` (string, optional — lookup by name if not provided)
- `wxcode_version` (string, required)
- `milestone_folder_name` (string, required)
- `confirm` (boolean, default false)

Returns:
```json
{
  "error": false,
  "milestone_id": "507f1f77bcf86cd799439011",
  "element_name": "PAGE_Login",
  "wxcode_version": "v1.0",
  "milestone_folder_name": "v1.0-PAGE_Login",
  "status": "in_progress",
  "created": true
}
```

### Conversion Progress (Hybrid Approach)

For `conversion.*` fields in the project dashboard:

| Field | Source |
|-------|--------|
| `is_conversion_project` | CONVERSION.md exists |
| `elements_converted` | MCP `get_conversion_stats` (source of truth) |
| `elements_total` | MCP `get_conversion_stats` (source of truth) |
| `stack` | CONVERSION.md |

---

## UI Changes Required

### 1. Watch for Two Dashboard Types

Listen for notifications:
```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard_v1.0-PAGE_Login.json
```

### 2. Parse Dashboard Type from Path

```javascript
function getDashboardType(path) {
  if (path.endsWith('dashboard.json')) {
    return 'project';
  } else if (path.includes('dashboard_')) {
    return 'milestone';
  }
}
```

### 3. Extract Milestone Folder from Filename

```javascript
function getMilestoneFolderName(path) {
  // .planning/dashboard_v1.0-PAGE_Login.json → v1.0-PAGE_Login
  const match = path.match(/dashboard_(.+)\.json$/);
  return match ? match[1] : null;
}
```

### 4. UI Should NOT Create Milestones Directly

**Before:** UI creates Milestone in MongoDB, then calls `/wxcode:new-milestone --milestone-id=xxx`

**After:** UI calls `/wxcode:new-milestone` which creates the Milestone in MongoDB via MCP.

This ensures the milestone is created with `wxcode_version` and `milestone_folder_name` set correctly from the start.

### 5. Display Considerations

**Project View:**
- Show conversion progress bar (elements_converted / elements_total)
- List milestones with status badges
- Click milestone → show milestone dashboard

**Milestone View:**
- Show phase progress
- Show requirement completion by category
- Show current position (which phase/plan is active)

---

## File Locations

Schema files:
- `~/.claude/get-shit-done/references/dashboard-schema-project.md`
- `~/.claude/get-shit-done/references/dashboard-schema-milestone.md`

The old `dashboard-schema.md` has been removed.

---

## Migration Steps

1. **Update Milestone model** — Add `wxcode_version` and `milestone_folder_name` fields
2. **Create MCP tool** — Implement `create_milestone`
3. **Update UI** — Handle split dashboard files
4. **Remove old behavior** — UI should not create Milestones directly
5. **Test flow** — Run `/wxcode:new-milestone` and verify both dashboards are created
