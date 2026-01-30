---
name: wxcode:dashboard
description: Generate project progress JSON and notify watchers
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

<objective>

Generate a comprehensive JSON snapshot of project progress for external UI rendering.

**Output:**
1. Writes JSON to `.planning/dashboard.json`
2. Emits watcher notification: `[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json`

**Use case:** IDE integrations, dashboards, progress visualization, file watchers

</objective>

<execution_context>
@~/.claude/get-shit-done/references/dashboard-schema.md
</execution_context>

<output_schema>

```json
{
  "project": {
    "name": "string",
    "core_value": "string",
    "current_milestone": "string",
    "description": "string"
  },
  "current_position": {
    "milestone": "string",
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
    "phases_percentage": "number",
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
      "requirements_covered": ["string"],
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
        "id": "string",
        "name": "string",
        "complete": "number",
        "total": "number",
        "percentage": "number",
        "items": [
          {
            "id": "string",
            "description": "string",
            "complete": "boolean",
            "phase": "number | null"
          }
        ]
      }
    ]
  },
  "blockers": ["string"],
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
      "completed_at": "string",
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

</output_schema>

<process>

## Step 1: Check Project Exists

```bash
[ -f .planning/PROJECT.md ] || echo '{"error": "No project found. Run /wxcode:new-project first."}' && exit 0
```

If no project, output error JSON and STOP.

## Step 2: Read All Source Files

Read these files (skip if not exist):

1. `.planning/PROJECT.md` → project info, core value
2. `.planning/STATE.md` → current position, blockers, todos
3. `.planning/ROADMAP.md` → phases list with status
4. `.planning/REQUIREMENTS.md` → requirements with checkboxes
5. `.planning/config.json` → workflow preferences
6. `.planning/CONVERSION.md` → conversion project info (if exists)
7. `.milestones/*.md` → completed milestones history

## Step 3: Read Phase Details

For each phase in ROADMAP.md:

```bash
ls .planning/phases/
```

For each phase folder (e.g., `01-project-setup/`):
- Read all `*-PLAN.md` files for plan details
- Read all `*-SUMMARY.md` files for completion summaries
- Count tasks from PLAN.md task lists

## Step 4: Parse and Build JSON

### From PROJECT.md:
- Extract project name (first H1)
- Extract "Core Value" section
- Extract "What This Is" section for description

### From STATE.md:
- Extract "Current Position" section
- Parse phase number, plan number, status
- Extract "Blockers" section
- Extract "Pending Todos" section

### From ROADMAP.md:
- Parse phase table or list
- For each phase: number, name, goal, status
- Count complete vs total phases

### From REQUIREMENTS.md:
- Parse v1 Requirements sections
- For each category (AUTH, PROF, etc.):
  - Count checked `[x]` vs unchecked `[ ]`
  - Extract requirement IDs and descriptions
- Parse Traceability table for phase mapping

### From Phase Folders:
- For each PLAN.md:
  - Extract plan name/objective
  - Count task checkboxes (complete/total)
- For each SUMMARY.md:
  - Extract summary text

### From .milestones/:
- List all milestone files
- Parse version, name, completion date
- Count phases per milestone

### From CONVERSION.md (if exists):
- Set is_conversion_project = true
- Extract stack target
- Extract conversion stats if available

## Step 5: Write JSON and Notify

1. **Write JSON to file:**
   - Use Write tool to save to `.planning/dashboard.json`
   - Ensure valid JSON (proper escaping, no trailing commas)

2. **Emit watcher notification:**
   - Output exactly this line (for terminal watchers):
   ```
   [WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json
   ```

**IMPORTANT:**
- The notification line must be exactly as shown above
- No extra formatting or explanation around it
- This allows external processes to detect dashboard updates

</process>

<example_output>

{
  "project": {
    "name": "CommunityApp",
    "core_value": "Users can share and discuss content with people who share their interests",
    "current_milestone": "v1.0 MVP",
    "description": "A community platform for sharing and discussing content"
  },
  "current_position": {
    "milestone": "v1.0",
    "phase_number": 3,
    "phase_name": "User Authentication",
    "phase_total": 5,
    "plan_number": 2,
    "plan_total": 3,
    "status": "in_progress"
  },
  "progress": {
    "phases_complete": 2,
    "phases_total": 5,
    "phases_percentage": 40,
    "requirements_complete": 6,
    "requirements_total": 20,
    "requirements_percentage": 30
  },
  "phases": [
    {
      "number": 1,
      "name": "Project Setup",
      "goal": "Initialize project structure and core dependencies",
      "status": "complete",
      "requirements_covered": ["AUTH-01", "AUTH-02"],
      "plans": [
        {
          "number": 1,
          "name": "Initialize project structure",
          "status": "complete",
          "tasks_complete": 5,
          "tasks_total": 5,
          "summary": "Created project structure with FastAPI, configured database connection"
        }
      ]
    },
    {
      "number": 2,
      "name": "Database Models",
      "goal": "Create SQLAlchemy models for all entities",
      "status": "complete",
      "requirements_covered": ["AUTH-03", "AUTH-04", "PROF-01", "PROF-02"],
      "plans": [
        {
          "number": 1,
          "name": "User and Profile models",
          "status": "complete",
          "tasks_complete": 4,
          "tasks_total": 4,
          "summary": "Created User, Profile, and Session models"
        },
        {
          "number": 2,
          "name": "Content models",
          "status": "complete",
          "tasks_complete": 3,
          "tasks_total": 3,
          "summary": "Created Post, Comment, and Like models"
        }
      ]
    },
    {
      "number": 3,
      "name": "User Authentication",
      "goal": "Implement signup, login, and session management",
      "status": "in_progress",
      "requirements_covered": [],
      "plans": [
        {
          "number": 1,
          "name": "Signup endpoint",
          "status": "complete",
          "tasks_complete": 4,
          "tasks_total": 4,
          "summary": "Implemented /auth/signup with email verification"
        },
        {
          "number": 2,
          "name": "Login endpoint",
          "status": "in_progress",
          "tasks_complete": 2,
          "tasks_total": 5,
          "summary": null
        },
        {
          "number": 3,
          "name": "Session management",
          "status": "pending",
          "tasks_complete": 0,
          "tasks_total": 4,
          "summary": null
        }
      ]
    },
    {
      "number": 4,
      "name": "Dashboard UI",
      "goal": "Create user dashboard with profile and feed",
      "status": "pending",
      "requirements_covered": [],
      "plans": []
    },
    {
      "number": 5,
      "name": "API Integration",
      "goal": "Connect frontend to backend APIs",
      "status": "pending",
      "requirements_covered": [],
      "plans": []
    }
  ],
  "requirements": {
    "total": 20,
    "complete": 6,
    "categories": [
      {
        "id": "AUTH",
        "name": "Authentication",
        "complete": 4,
        "total": 4,
        "percentage": 100,
        "items": [
          {"id": "AUTH-01", "description": "User can sign up with email and password", "complete": true, "phase": 1},
          {"id": "AUTH-02", "description": "User receives email verification after signup", "complete": true, "phase": 1},
          {"id": "AUTH-03", "description": "User can reset password via email link", "complete": true, "phase": 2},
          {"id": "AUTH-04", "description": "User session persists across browser refresh", "complete": true, "phase": 2}
        ]
      },
      {
        "id": "PROF",
        "name": "Profiles",
        "complete": 2,
        "total": 4,
        "percentage": 50,
        "items": [
          {"id": "PROF-01", "description": "User can create profile with display name", "complete": true, "phase": 2},
          {"id": "PROF-02", "description": "User can upload avatar image", "complete": true, "phase": 2},
          {"id": "PROF-03", "description": "User can write bio", "complete": false, "phase": null},
          {"id": "PROF-04", "description": "User can view other users' profiles", "complete": false, "phase": null}
        ]
      },
      {
        "id": "CONT",
        "name": "Content",
        "complete": 0,
        "total": 5,
        "percentage": 0,
        "items": [
          {"id": "CONT-01", "description": "User can create text post", "complete": false, "phase": null},
          {"id": "CONT-02", "description": "User can upload image with post", "complete": false, "phase": null},
          {"id": "CONT-03", "description": "User can edit own posts", "complete": false, "phase": null},
          {"id": "CONT-04", "description": "User can delete own posts", "complete": false, "phase": null},
          {"id": "CONT-05", "description": "User can view feed of posts", "complete": false, "phase": null}
        ]
      }
    ]
  },
  "blockers": [
    "Waiting for SMTP credentials for email verification"
  ],
  "todos": [
    {"id": "1", "subject": "Add rate limiting to auth endpoints", "status": "pending", "priority": null},
    {"id": "2", "subject": "Write API documentation", "status": "pending", "priority": null}
  ],
  "milestones_history": [],
  "conversion": {
    "is_conversion_project": false,
    "elements_converted": null,
    "elements_total": null,
    "stack": null
  },
  "meta": {
    "generated_at": "2026-01-29T14:30:00Z",
    "wxcode_version": "1.1.7"
  }
}

</example_output>

<success_criteria>
- [ ] JSON is valid (parseable)
- [ ] Written to `.planning/dashboard.json`
- [ ] Notification emitted: `[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json`
- [ ] All existing files parsed correctly
- [ ] Missing files handled gracefully (null values)
- [ ] Phase details include all plans
- [ ] Requirements grouped by category
- [ ] Blockers and todos included
- [ ] Conversion project info included (if applicable)
</success_criteria>

<integration>

## Triggering Dashboard Updates

Other commands should trigger dashboard update after significant state changes.

**Add this step to commands that modify project state:**

```
## Final Step: Update Dashboard

After completing all other steps, update the project dashboard:

1. Generate dashboard JSON (follow /wxcode:dashboard process)
2. Write to `.planning/dashboard.json`
3. Output: `[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json`
```

**Commands that should trigger dashboard update:**
- `/wxcode:new-project` (after completion)
- `/wxcode:new-milestone` (after completion)
- `/wxcode:plan-phase` (after PLAN.md created)
- `/wxcode:execute-phase` (after each plan completes)
- `/wxcode:verify-work` (after verification)
- `/wxcode:complete-milestone` (after archiving)

</integration>
