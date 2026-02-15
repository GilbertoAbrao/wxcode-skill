---
mode: autopilot
status: milestone_initialized
current_phase: 0
total_phases: {TOTAL_PHASES}
retry_count: 0
max_retries: 3
elements: [{ELEMENT_LIST}]
output_project: "{OUTPUT_PROJECT_ID}"
milestone_id: "{MONGODB_MILESTONE_ID}"
milestone_folder: "{MILESTONE_FOLDER_NAME}"
version: "{WXCODE_VERSION}"
project_name: "{PROJECT_NAME}"
created_at: "{TIMESTAMP}"
updated_at: "{TIMESTAMP}"
error_phase: null
error_step: null
error_reason: null
---

# Autopilot Progress

| Phase | Plan | Execute | Verify | Status |
|-------|------|---------|--------|--------|
{PHASE_ROWS}

## Log

- {TIMESTAMP} — Autopilot initialized by new-milestone
