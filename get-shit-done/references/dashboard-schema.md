# Dashboard JSON Schema

Standard schema for `.planning/dashboard.json`. All commands that update the dashboard MUST use this exact format.

## Full Schema

```json
{
  "project": {
    "name": "string - project name from PROJECT.md",
    "core_value": "string - core value from PROJECT.md",
    "current_milestone": "string - e.g., 'v1.0 MVP'",
    "description": "string - what this is from PROJECT.md"
  },
  "current_position": {
    "milestone": "string - e.g., 'v1.0'",
    "phase_number": "number | null",
    "phase_name": "string | null",
    "phase_total": "number",
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
          "number": "number",
          "name": "string",
          "status": "pending | in_progress | complete",
          "tasks_complete": "number",
          "tasks_total": "number",
          "summary": "string | null"
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
  "todos": [
    {
      "id": "string",
      "subject": "string",
      "status": "pending | in_progress | complete",
      "priority": "string | null"
    }
  ],
  "milestones_history": [
    {
      "version": "string",
      "name": "string",
      "completed_at": "ISO8601 string",
      "phases_count": "number"
    }
  ],
  "conversion": {
    "is_conversion_project": "boolean",
    "elements_converted": "number | null",
    "elements_total": "number | null",
    "stack": "string | null"
  },
  "meta": {
    "generated_at": "ISO8601 string",
    "wxcode_version": "string"
  }
}
```

## Initial State (New Project)

For newly initialized projects, use these defaults:

```json
{
  "project": {
    "name": "[from PROJECT.md]",
    "core_value": "[from PROJECT.md]",
    "current_milestone": "[from ROADMAP.md or 'v1.0']",
    "description": "[from PROJECT.md 'What This Is']"
  },
  "current_position": {
    "milestone": "v1.0",
    "phase_number": null,
    "phase_name": null,
    "phase_total": "[count from ROADMAP.md]",
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
  "blockers": "[from STATE.md or empty]",
  "todos": "[from STATE.md or empty]",
  "milestones_history": [],
  "conversion": {
    "is_conversion_project": "[true if CONVERSION.md exists]",
    "elements_converted": "[from CONVERSION.md or null]",
    "elements_total": "[from CONVERSION.md or null]",
    "stack": "[from CONVERSION.md or null]"
  },
  "meta": {
    "generated_at": "[current ISO8601 timestamp]",
    "wxcode_version": "[from VERSION file]"
  }
}
```

## Update Notification

After writing the JSON, output exactly:

```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json
```

This allows external watchers to detect updates.

## Data Sources

| Field | Source |
|-------|--------|
| project.* | `.planning/PROJECT.md` |
| current_position.* | `.planning/STATE.md` |
| phases | `.planning/ROADMAP.md` + `.planning/phases/*/` |
| requirements | `.planning/REQUIREMENTS.md` |
| blockers | `.planning/STATE.md` |
| todos | `.planning/STATE.md` |
| milestones_history | `.milestones/*.md` |
| conversion.* | `.planning/CONVERSION.md` |
