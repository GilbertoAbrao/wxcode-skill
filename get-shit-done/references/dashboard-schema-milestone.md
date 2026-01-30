# Dashboard JSON Schema — Milestone

Schema for `.planning/dashboard_<milestone>.json`. This is the **milestone-level** dashboard with detailed phases, plans, tasks, and workflow stages for a specific milestone.

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
  "workflow": {
    "current_stage": "string - one of the stage ids below",
    "stages": [
      {
        "id": "created",
        "name": "Milestone Created",
        "description": "Folder created, MongoDB record, initial research",
        "status": "pending | in_progress | complete",
        "completed_at": "ISO8601 string | null"
      },
      {
        "id": "requirements",
        "name": "Requirements Defined",
        "description": "REQUIREMENTS.md generated with acceptance criteria",
        "status": "pending | in_progress | complete",
        "completed_at": "ISO8601 string | null"
      },
      {
        "id": "roadmap",
        "name": "Roadmap Created",
        "description": "ROADMAP.md with phase breakdown",
        "status": "pending | in_progress | complete",
        "completed_at": "ISO8601 string | null"
      },
      {
        "id": "planning",
        "name": "All Phases Planned",
        "description": "PLAN.md exists for all phases",
        "status": "pending | in_progress | complete",
        "completed_at": "ISO8601 string | null"
      },
      {
        "id": "executing",
        "name": "Execution In Progress",
        "description": "Plans being executed, code being written",
        "status": "pending | in_progress | complete",
        "completed_at": "ISO8601 string | null"
      },
      {
        "id": "verified",
        "name": "Work Verified",
        "description": "UAT passed, all requirements met",
        "status": "pending | in_progress | complete",
        "completed_at": "ISO8601 string | null"
      },
      {
        "id": "archived",
        "name": "Milestone Archived",
        "description": "Moved to milestones/, marked converted in MCP",
        "status": "pending | in_progress | complete",
        "completed_at": "ISO8601 string | null"
      }
    ]
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

## Workflow Stages

The `workflow` section tracks the milestone lifecycle with 7 stages:

| Stage ID | Name | Triggered By |
|----------|------|--------------|
| `created` | Milestone Created | `/wxcode:new-milestone` creates folder |
| `requirements` | Requirements Defined | REQUIREMENTS.md written |
| `roadmap` | Roadmap Created | ROADMAP.md written |
| `planning` | All Phases Planned | All phases have at least one PLAN.md |
| `executing` | Execution In Progress | First SUMMARY.md created |
| `verified` | Work Verified | `/wxcode:verify-work` passes UAT |
| `archived` | Milestone Archived | `/wxcode:complete-milestone` completes |

### Stage Transitions

```
created → requirements → roadmap → planning → executing → verified → archived
```

Each stage:
- Starts as `pending`
- Becomes `in_progress` when work begins on that stage
- Becomes `complete` with `completed_at` timestamp when finished

### UI Visualization

```
Workflow Progress
─────────────────────────────────────────────────────
[✓] Milestone Created          30 Jan 13:43
[✓] Requirements Defined       30 Jan 13:45
[✓] Roadmap Created            30 Jan 13:50
[✓] All Phases Planned         30 Jan 14:30
[●] Execution In Progress      ← current_stage
[ ] Work Verified
[ ] Milestone Archived
─────────────────────────────────────────────────────
```

## Example (Complete)

```json
{
  "milestone": {
    "folder_name": "v1.0-PAGE_Login",
    "mongodb_id": "507f1f77bcf86cd799439011",
    "wxcode_version": "v1.0",
    "element_name": "PAGE_Login",
    "status": "completed",
    "created_at": "2026-01-30T13:43:00Z",
    "completed_at": "2026-01-30T15:57:00Z"
  },
  "workflow": {
    "current_stage": "archived",
    "stages": [
      {
        "id": "created",
        "name": "Milestone Created",
        "description": "Folder created, MongoDB record, initial research",
        "status": "complete",
        "completed_at": "2026-01-30T13:43:00Z"
      },
      {
        "id": "requirements",
        "name": "Requirements Defined",
        "description": "REQUIREMENTS.md generated with acceptance criteria",
        "status": "complete",
        "completed_at": "2026-01-30T13:45:00Z"
      },
      {
        "id": "roadmap",
        "name": "Roadmap Created",
        "description": "ROADMAP.md with phase breakdown",
        "status": "complete",
        "completed_at": "2026-01-30T13:50:00Z"
      },
      {
        "id": "planning",
        "name": "All Phases Planned",
        "description": "PLAN.md exists for all phases",
        "status": "complete",
        "completed_at": "2026-01-30T14:30:00Z"
      },
      {
        "id": "executing",
        "name": "Execution In Progress",
        "description": "Plans being executed, code being written",
        "status": "complete",
        "completed_at": "2026-01-30T15:45:00Z"
      },
      {
        "id": "verified",
        "name": "Work Verified",
        "description": "UAT passed, all requirements met",
        "status": "complete",
        "completed_at": "2026-01-30T15:50:00Z"
      },
      {
        "id": "archived",
        "name": "Milestone Archived",
        "description": "Moved to milestones/, marked converted in MCP",
        "status": "complete",
        "completed_at": "2026-01-30T15:57:00Z"
      }
    ]
  },
  "current_position": {
    "phase_number": 1,
    "phase_name": "login-implementation",
    "plan_number": "1.3",
    "plan_total": 3,
    "status": "complete"
  },
  "progress": {
    "phases_complete": 1,
    "phases_total": 1,
    "phases_percentage": 100,
    "plans_complete": 3,
    "plans_total": 3,
    "plans_percentage": 100,
    "tasks_complete": 13,
    "tasks_total": 13,
    "tasks_percentage": 100,
    "requirements_complete": 10,
    "requirements_total": 10,
    "requirements_percentage": 100
  },
  "phases": [
    {
      "number": 1,
      "name": "login-implementation",
      "goal": "Implement complete login flow with authentication",
      "status": "complete",
      "requirements_covered": ["AUTH-01", "AUTH-02", "AUTH-03", "AUTH-04", "AUTH-05", "ERR-01", "ERR-02", "ERR-03", "DB-01", "DB-02"],
      "plans": [
        {
          "number": "1.1",
          "name": "Database Layer",
          "status": "complete",
          "summary": "Created AcessoUsuario model and configured database connection initialization",
          "tasks": [
            {
              "id": "1.1.1",
              "name": "Create AcessoUsuario Model",
              "file": "app/models/acesso_usuario.py",
              "status": "complete",
              "description": "SQLAlchemy model for the AcessoUsuario table with all fields from legacy schema"
            },
            {
              "id": "1.1.2",
              "name": "Update Models Package Init",
              "file": "app/models/__init__.py",
              "status": "complete",
              "description": "Export AcessoUsuario model from models package"
            },
            {
              "id": "1.1.3",
              "name": "Add Database Initialization to App Startup",
              "file": "app/main.py",
              "status": "complete",
              "description": "Add startup event handler to initialize database connection"
            }
          ]
        },
        {
          "number": "1.2",
          "name": "Authentication Service",
          "status": "complete",
          "summary": "Configured SessionMiddleware and implemented authentication logic",
          "tasks": [
            {
              "id": "1.2.1",
              "name": "Add SessionMiddleware to Application",
              "file": "app/main.py",
              "status": "complete",
              "description": "Add Starlette SessionMiddleware for cookie-based sessions"
            },
            {
              "id": "1.2.2",
              "name": "Create Authentication Service",
              "file": "app/services/auth.py",
              "status": "complete",
              "description": "Authentication service with functions to validate credentials and manage sessions"
            },
            {
              "id": "1.2.3",
              "name": "Update Services Package Init",
              "file": "app/services/__init__.py",
              "status": "complete",
              "description": "Export authentication functions from services package"
            },
            {
              "id": "1.2.4",
              "name": "Verify python-multipart Dependency",
              "file": "requirements.txt",
              "status": "complete",
              "description": "Ensure python-multipart is installed for Form() data parsing"
            }
          ]
        },
        {
          "number": "1.3",
          "name": "Routes and Templates",
          "status": "complete",
          "summary": "Created login and dashboard routes with corresponding templates",
          "tasks": [
            {
              "id": "1.3.1",
              "name": "Create Auth Templates Directory",
              "file": "app/templates/auth/",
              "status": "complete",
              "description": "Create subdirectory for authentication-related templates"
            },
            {
              "id": "1.3.2",
              "name": "Create Login Template",
              "file": "app/templates/auth/login.html",
              "status": "complete",
              "description": "Login page with username and password fields matching legacy EDT_LOGIN and EDT_Senha"
            },
            {
              "id": "1.3.3",
              "name": "Create Dashboard Template",
              "file": "app/templates/dashboard.html",
              "status": "complete",
              "description": "Stub dashboard page with welcome message and logout link"
            },
            {
              "id": "1.3.4",
              "name": "Create Auth Routes",
              "file": "app/routes/auth.py",
              "status": "complete",
              "description": "Authentication routes for login, logout, and dashboard with form validation"
            },
            {
              "id": "1.3.5",
              "name": "Register Auth Router in Main App",
              "file": "app/main.py",
              "status": "complete",
              "description": "Import and register auth router with main FastAPI application"
            },
            {
              "id": "1.3.6",
              "name": "Update Routes Package Init",
              "file": "app/routes/__init__.py",
              "status": "complete",
              "description": "Export auth router from routes package"
            }
          ]
        }
      ]
    }
  ],
  "requirements": {
    "total": 10,
    "complete": 10,
    "categories": [
      {
        "id": "AUTH",
        "name": "Authentication",
        "complete": 5,
        "total": 5,
        "percentage": 100,
        "items": [
          {
            "id": "AUTH-01",
            "description": "User can view login page with username and password fields",
            "complete": true,
            "phase": 1
          },
          {
            "id": "AUTH-02",
            "description": "User can submit login form with credentials",
            "complete": true,
            "phase": 1
          },
          {
            "id": "AUTH-03",
            "description": "System validates credentials against AcessoUsuario table",
            "complete": true,
            "phase": 1
          },
          {
            "id": "AUTH-04",
            "description": "User session is created on successful login",
            "complete": true,
            "phase": 1
          },
          {
            "id": "AUTH-05",
            "description": "User is redirected to dashboard after successful login",
            "complete": true,
            "phase": 1
          }
        ]
      },
      {
        "id": "ERR",
        "name": "Error Handling",
        "complete": 3,
        "total": 3,
        "percentage": 100,
        "items": [
          {
            "id": "ERR-01",
            "description": "System displays error for empty username",
            "complete": true,
            "phase": 1
          },
          {
            "id": "ERR-02",
            "description": "System displays error for empty password",
            "complete": true,
            "phase": 1
          },
          {
            "id": "ERR-03",
            "description": "System displays error for invalid credentials",
            "complete": true,
            "phase": 1
          }
        ]
      },
      {
        "id": "DB",
        "name": "Database",
        "complete": 2,
        "total": 2,
        "percentage": 100,
        "items": [
          {
            "id": "DB-01",
            "description": "AcessoUsuario model is created with required fields",
            "complete": true,
            "phase": 1
          },
          {
            "id": "DB-02",
            "description": "Database connection is configured for SQL Server",
            "complete": true,
            "phase": 1
          }
        ]
      }
    ]
  },
  "blockers": [],
  "meta": {
    "generated_at": "2026-01-30T18:30:00Z",
    "wxcode_version": "1.2.4"
  }
}
```

## Data Sources

| Field | Source |
|-------|--------|
| `milestone.*` | Created by `/wxcode:new-milestone` |
| `milestone.mongodb_id` | MCP `create_milestone` response |
| `workflow.*` | Computed from file existence and command execution |
| `current_position.*` | `.planning/STATE.md` |
| `phases` | `.planning/ROADMAP.md` |
| `phases[].plans` | `.planning/phases/*/*.md` files |
| `phases[].plans[].tasks` | Parsed from `*-PLAN.md` (see below) |
| `phases[].plans[].summary` | From `*-SUMMARY.md` if exists |
| `requirements` | `.planning/REQUIREMENTS.md` |
| `blockers` | `.planning/STATE.md` |

## Workflow Stage Detection

How to determine each stage's status:

| Stage | Detect Complete |
|-------|-----------------|
| `created` | Milestone folder exists |
| `requirements` | REQUIREMENTS.md exists and has content |
| `roadmap` | ROADMAP.md exists and has phases defined |
| `planning` | All phases in ROADMAP have at least one PLAN.md |
| `executing` | At least one SUMMARY.md exists |
| `verified` | UAT.md exists with status "passed" |
| `archived` | `/wxcode:complete-milestone` executed (milestone.status = "completed") |

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

| Command | Workflow Stage | What to Update |
|---------|----------------|----------------|
| `/wxcode:new-milestone` | created → requirements → roadmap | Create initial dashboard with first 3 stages |
| `/wxcode:plan-phase` | planning | Add plans and tasks, update planning stage |
| `/wxcode:execute-phase` | executing | Update task/plan status, executing stage |
| `/wxcode:verify-work` | verified | Update requirement completion, verified stage |
| `/wxcode:complete-milestone` | archived | Set milestone.status = "completed", archive stage |
