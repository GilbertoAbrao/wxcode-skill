# Dashboard JSON Schema — Milestone

Schema for `.planning/dashboard_<milestone>.json`. This is the **milestone-level** dashboard with detailed phases and requirements for a specific milestone.

Example filename: `.planning/dashboard_v1.0-PAGE_Login.json`

## Full Schema

```json
{
  "milestone": {
    "folder_name": "string - e.g., 'v1.0-PAGE_Login'",
    "mongodb_id": "string | null - from MCP create_milestone",
    "wxcode_version": "string - e.g., 'v1.0'",
    "element_name": "string - e.g., 'PAGE_Login'",
    "status": "pending | in_progress | completed | failed",
    "created_at": "ISO8601 string",
    "completed_at": "ISO8601 string | null"
  },
  "current_position": {
    "phase_number": "number | null",
    "phase_name": "string | null",
    "plan_number": "number | null",
    "plan_total": "number | null",
    "status": "not_started | in_progress | complete | blocked"
  },
  "progress": {
    "phases_complete": "number",
    "phases_total": "number",
    "phases_percentage": "number (0-100)",
    "requirements_complete": "number",
    "requirements_total": "number",
    "requirements_percentage": "number (0-100)"
  },
  "phases": [
    {
      "number": "number",
      "name": "string",
      "goal": "string",
      "status": "pending | in_progress | complete",
      "requirements_covered": ["REQ-ID", "..."],
      "plans": [
        {
          "number": "string - e.g., '1.1'",
          "name": "string - e.g., 'Database Layer'",
          "status": "pending | in_progress | complete",
          "tasks_complete": "number",
          "tasks_total": "number",
          "summary": "string | null - from SUMMARY.md if complete",
          "tasks": [
            {
              "id": "string - e.g., '1.1.1'",
              "name": "string - e.g., 'Create AcessoUsuario Model'",
              "file": "string | null - e.g., 'app/models/acesso_usuario.py'",
              "status": "pending | in_progress | complete",
              "description": "string - brief description of what the task does"
            }
          ]
        }
      ]
    }
  ],
  "requirements": {
    "total": "number",
    "complete": "number",
    "categories": [
      {
        "id": "string - e.g., 'AUTH'",
        "name": "string - e.g., 'Authentication'",
        "complete": "number",
        "total": "number",
        "percentage": "number (0-100)",
        "items": [
          {
            "id": "string - e.g., 'AUTH-01'",
            "description": "string",
            "complete": "boolean",
            "phase": "number | null"
          }
        ]
      }
    ]
  },
  "blockers": ["string", "..."],
  "meta": {
    "generated_at": "ISO8601 string",
    "wxcode_version": "string"
  }
}
```

## Initial State (New Milestone)

```json
{
  "milestone": {
    "folder_name": "[version]-[element_name]",
    "mongodb_id": "[from MCP create_milestone]",
    "wxcode_version": "[version]",
    "element_name": "[element_name]",
    "status": "in_progress",
    "created_at": "[current ISO8601 timestamp]",
    "completed_at": null
  },
  "current_position": {
    "phase_number": null,
    "phase_name": null,
    "plan_number": null,
    "plan_total": null,
    "status": "not_started"
  },
  "progress": {
    "phases_complete": 0,
    "phases_total": "[count from ROADMAP.md]",
    "phases_percentage": 0,
    "requirements_complete": 0,
    "requirements_total": "[count from REQUIREMENTS.md]",
    "requirements_percentage": 0
  },
  "phases": "[parse from ROADMAP.md - empty plans array for each]",
  "requirements": "[parse from REQUIREMENTS.md]",
  "blockers": [],
  "meta": {
    "generated_at": "[current ISO8601 timestamp]",
    "wxcode_version": "[from VERSION file]"
  }
}
```

## Data Sources

| Field | Source |
|-------|--------|
| milestone.mongodb_id | MCP `create_milestone` response |
| milestone.* | Created during `/wxcode:new-milestone` |
| current_position.* | `.planning/STATE.md` |
| phases | `.planning/ROADMAP.md` + `.planning/phases/*/` |
| phases[].plans[].tasks | Parse from `*-PLAN.md` files (## Tasks section) |
| requirements | `.planning/REQUIREMENTS.md` |
| blockers | `.planning/STATE.md` |

## Task Parsing

Extract tasks from PLAN.md files by parsing the `## Tasks` section:

```markdown
## Tasks

### Task 1.1.1: Create AcessoUsuario Model
**File:** `app/models/acesso_usuario.py`
**Description:** Create SQLAlchemy model...
```

Maps to:
```json
{
  "id": "1.1.1",
  "name": "Create AcessoUsuario Model",
  "file": "app/models/acesso_usuario.py",
  "status": "pending",
  "description": "Create SQLAlchemy model..."
}
```

Task status is determined by:
- `pending`: PLAN.md exists, no SUMMARY.md
- `in_progress`: Currently being executed
- `complete`: SUMMARY.md exists for this plan

## Update Notification

After writing the JSON, output exactly:

```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard_<milestone>.json
```

## When to Update

Update this dashboard when:
- Milestone is created (`/wxcode:new-milestone`)
- Phase is planned (`/wxcode:plan-phase`)
- Phase is executed (`/wxcode:execute-phase`)
- Work is verified (`/wxcode:verify-work`)
- Milestone is completed (`/wxcode:complete-milestone`)
