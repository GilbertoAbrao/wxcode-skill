# Dashboard JSON Schema — Milestone

Schema for `.planning/dashboard_<milestone>.json`. This is the **milestone-level** dashboard with detailed phases, plans, and tasks for a specific milestone.

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
    "plan_number": "string | null - e.g., '1.2'",
    "plan_total": "number | null",
    "status": "not_started | in_progress | complete | blocked"
  },
  "progress": {
    "phases_complete": "number",
    "phases_total": "number",
    "phases_percentage": "number (0-100)",
    "plans_complete": "number",
    "plans_total": "number",
    "plans_percentage": "number (0-100)",
    "tasks_complete": "number",
    "tasks_total": "number",
    "tasks_percentage": "number (0-100)",
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
          "summary": "string | null - from SUMMARY.md if complete",
          "tasks": [
            {
              "id": "string - e.g., '1.1.1'",
              "name": "string - e.g., 'Create AcessoUsuario Model'",
              "file": "string | null - target file path",
              "status": "pending | in_progress | complete",
              "description": "string - what the task implements"
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

## Example (Real Data)

```json
{
  "milestone": {
    "folder_name": "v1.0-PAGE_Login",
    "mongodb_id": "507f1f77bcf86cd799439011",
    "wxcode_version": "v1.0",
    "element_name": "PAGE_Login",
    "status": "in_progress",
    "created_at": "2026-01-30T13:43:00Z",
    "completed_at": null
  },
  "current_position": {
    "phase_number": 1,
    "phase_name": "login-implementation",
    "plan_number": "1.2",
    "plan_total": 3,
    "status": "in_progress"
  },
  "progress": {
    "phases_complete": 0,
    "phases_total": 1,
    "phases_percentage": 0,
    "plans_complete": 1,
    "plans_total": 3,
    "plans_percentage": 33,
    "tasks_complete": 3,
    "tasks_total": 8,
    "tasks_percentage": 37,
    "requirements_complete": 2,
    "requirements_total": 10,
    "requirements_percentage": 20
  },
  "phases": [
    {
      "number": 1,
      "name": "login-implementation",
      "goal": "Implement complete login flow with authentication",
      "status": "in_progress",
      "requirements_covered": ["DB-01", "DB-02", "AUTH-01", "AUTH-02", "UI-01"],
      "plans": [
        {
          "number": "1.1",
          "name": "Database Layer",
          "status": "complete",
          "summary": "Created AcessoUsuario model and configured database initialization",
          "tasks": [
            {
              "id": "1.1.1",
              "name": "Create AcessoUsuario Model",
              "file": "app/models/acesso_usuario.py",
              "status": "complete",
              "description": "SQLAlchemy model for user authentication table"
            },
            {
              "id": "1.1.2",
              "name": "Update Models Package Init",
              "file": "app/models/__init__.py",
              "status": "complete",
              "description": "Export AcessoUsuario from models package"
            },
            {
              "id": "1.1.3",
              "name": "Add Database Initialization",
              "file": "app/main.py",
              "status": "complete",
              "description": "Add startup event to initialize database connection"
            }
          ]
        },
        {
          "number": "1.2",
          "name": "Authentication Service",
          "status": "in_progress",
          "summary": null,
          "tasks": [
            {
              "id": "1.2.1",
              "name": "Create Auth Service",
              "file": "app/services/auth.py",
              "status": "complete",
              "description": "Authentication service with login validation"
            },
            {
              "id": "1.2.2",
              "name": "Create Session Manager",
              "file": "app/services/session.py",
              "status": "pending",
              "description": "Session management with JWT tokens"
            }
          ]
        },
        {
          "number": "1.3",
          "name": "Login UI",
          "status": "pending",
          "summary": null,
          "tasks": [
            {
              "id": "1.3.1",
              "name": "Create Login Template",
              "file": "app/templates/login.html",
              "status": "pending",
              "description": "Jinja2 template matching legacy PAGE_Login layout"
            },
            {
              "id": "1.3.2",
              "name": "Create Login Route",
              "file": "app/routes/auth.py",
              "status": "pending",
              "description": "FastAPI route for login page and form submission"
            },
            {
              "id": "1.3.3",
              "name": "Add Login Styles",
              "file": "app/static/css/login.css",
              "status": "pending",
              "description": "CSS styles for login page"
            }
          ]
        }
      ]
    }
  ],
  "requirements": {
    "total": 10,
    "complete": 2,
    "categories": [
      {
        "id": "DB",
        "name": "Database",
        "complete": 2,
        "total": 2,
        "percentage": 100,
        "items": [
          {
            "id": "DB-01",
            "description": "AcessoUsuario model exists",
            "complete": true,
            "phase": 1
          },
          {
            "id": "DB-02",
            "description": "Database connection configured",
            "complete": true,
            "phase": 1
          }
        ]
      },
      {
        "id": "AUTH",
        "name": "Authentication",
        "complete": 0,
        "total": 4,
        "percentage": 0,
        "items": [
          {
            "id": "AUTH-01",
            "description": "User can login with valid credentials",
            "complete": false,
            "phase": 1
          }
        ]
      }
    ]
  },
  "blockers": [],
  "meta": {
    "generated_at": "2026-01-30T15:30:00Z",
    "wxcode_version": "1.2.3"
  }
}
```

## Data Sources

| Field | Source |
|-------|--------|
| `milestone.*` | Created by `/wxcode:new-milestone` |
| `milestone.mongodb_id` | MCP `create_milestone` response |
| `current_position.*` | `.planning/STATE.md` |
| `phases` | `.planning/ROADMAP.md` |
| `phases[].plans` | `.planning/phases/*/*.md` files |
| `phases[].plans[].tasks` | Parsed from `*-PLAN.md` (see below) |
| `phases[].plans[].summary` | From `*-SUMMARY.md` if exists |
| `requirements` | `.planning/REQUIREMENTS.md` |
| `blockers` | `.planning/STATE.md` |

## Task Parsing

Tasks are extracted from PLAN.md files by parsing the `## Tasks` section:

**Source format (PLAN.md):**
```markdown
## Tasks

### Task 1.1.1: Create AcessoUsuario Model

**File:** `app/models/acesso_usuario.py`

**Description:** Create SQLAlchemy model for the AcessoUsuario table...
```

**Parsed result:**
```json
{
  "id": "1.1.1",
  "name": "Create AcessoUsuario Model",
  "file": "app/models/acesso_usuario.py",
  "status": "pending",
  "description": "Create SQLAlchemy model for the AcessoUsuario table..."
}
```

## Status Logic

**Task status:**
- `pending` — PLAN.md exists, plan not yet executed
- `in_progress` — Plan currently being executed
- `complete` — SUMMARY.md exists for this plan

**Plan status:**
- `pending` — No tasks started
- `in_progress` — Some tasks complete, some pending
- `complete` — All tasks complete (SUMMARY.md exists)

**Phase status:**
- `pending` — No plans started
- `in_progress` — Some plans complete, some pending
- `complete` — All plans complete

## Update Notification

After writing the JSON, output exactly:

```
[WXCODE:DASHBOARD_UPDATED] .planning/dashboard_<milestone>.json
```

## When to Update

| Command | What to Update |
|---------|----------------|
| `/wxcode:new-milestone` | Create initial dashboard |
| `/wxcode:plan-phase` | Add plans and tasks |
| `/wxcode:execute-phase` | Update task/plan status |
| `/wxcode:verify-work` | Update requirement completion |
| `/wxcode:complete-milestone` | Set milestone.status = "completed" |
