# Dashboard JSON Schema — Project (Global)

Schema for `.planning/dashboard.json`. This is the **project-level** dashboard with aggregated view of all milestones.

## Full Schema

```json
{
  "project": {
    "name": "string - project name from PROJECT.md",
    "core_value": "string - core value from PROJECT.md",
    "description": "string - what this is from PROJECT.md"
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
      "mongodb_id": "string | null - from MCP create_milestone",
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

## Initial State (New Project)

```json
{
  "project": {
    "name": "[from PROJECT.md]",
    "core_value": "[from PROJECT.md]",
    "description": "[from PROJECT.md 'What This Is']"
  },
  "conversion": {
    "is_conversion_project": true,
    "elements_converted": 0,
    "elements_total": "[from MCP get_conversion_stats]",
    "stack": "[from CONVERSION.md]"
  },
  "milestones": [],
  "current_milestone": null,
  "progress": {
    "milestones_complete": 0,
    "milestones_total": 0,
    "milestones_percentage": 0
  },
  "meta": {
    "generated_at": "[current ISO8601 timestamp]",
    "wxcode_version": "[from VERSION file]"
  }
}
```

## Data Sources

| Field | Source |
|-------|--------|
| project.* | `.planning/PROJECT.md` |
| conversion.is_conversion_project | `.planning/CONVERSION.md` exists |
| conversion.elements_* | MCP `get_conversion_stats` (source of truth) |
| conversion.stack | `.planning/CONVERSION.md` |
| milestones[] | Scan `.planning/dashboard_*.json` files |
| current_milestone | `.planning/STATE.md` or latest in_progress |

## Update Notification

After writing the JSON, output exactly:

```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json
```

## When to Update

Update this dashboard when:
- New milestone is created (`/wxcode:new-milestone`)
- Milestone status changes (started, completed, failed)
- Conversion progress changes (element marked as converted)
