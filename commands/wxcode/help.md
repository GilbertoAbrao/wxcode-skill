---
name: wxcode:help
description: Show available WXCODE commands
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"help","args":"","title":"WXCODE ▶ COMMAND REFERENCE"} -->
## WXCODE ▶ COMMAND REFERENCE
```

**At command end (emit after reference content):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Help displayed"} -->
```
</structured_output>

<objective>
Display the complete WXCODE command reference.

**Emit the structured header immediately followed by the visual banner (no blank line), then output the reference content.**

Output ONLY the reference content below. Do NOT add:

- Project-specific analysis
- Git status or file context
- Next-step suggestions
- Any commentary beyond the reference
</objective>

<reference>
# WXCODE Command Reference

**WXCODE** is an AI-powered WinDev/WebDev conversion toolkit for Claude Code.

## Project Setup

### `/wxcode:new-project`
Initialize a new project with deep context gathering and PROJECT.md.

### `/wxcode:new-milestone`
Create a new milestone for converting a specific WinDev element.

### `/wxcode:version`
Display the current WXCODE version.

### `/wxcode:update`
Update WXCODE to the latest version.

---

## Planning & Research

### `/wxcode:plan-phase`
Plan a project phase with research, task breakdown, and verification.

### `/wxcode:research-phase`
Deep research for a specific phase before planning.

### `/wxcode:discuss-phase`
Discuss and explore a phase's approach before planning.

### `/wxcode:discuss`
Open-ended exploration and planning for features or changes.

### `/wxcode:map-codebase`
Analyze and map the current codebase structure.

### `/wxcode:list-phase-assumptions`
List assumptions made during phase planning.

---

## Execution & Progress

### `/wxcode:execute-phase`
Execute a planned phase with atomic commits and state management.

### `/wxcode:progress`
Show project progress and phase status.

### `/wxcode:dashboard`
Generate project dashboard with metrics and status.

### `/wxcode:quick`
Quick task execution without full phase workflow.

---

## Phase Management

### `/wxcode:add-phase`
Add a new phase to the project roadmap.

### `/wxcode:insert-phase`
Insert a phase at a specific position in the roadmap.

### `/wxcode:remove-phase`
Remove a phase from the project roadmap.

---

## Verification & Quality

### `/wxcode:verify-work`
Verify completed work meets acceptance criteria.

### `/wxcode:audit-milestone`
Audit a milestone for completeness and quality.

### `/wxcode:check-todos`
Check and manage TODO items in the codebase.

### `/wxcode:add-todo`
Add a TODO item to track.

---

## Milestone Management

### `/wxcode:complete-milestone`
Complete and archive a milestone.

### `/wxcode:plan-milestone-gaps`
Identify gaps in milestone planning.

---

## Development Server

### `/wxcode:create-start-dev`
Generate start-dev.sh script from stack template.

### `/wxcode:start-dev`
Execute start-dev.sh to start development server(s).

---

## Conversion Tools

### `/wxcode:trace <element|file>`
Navigate between legacy WinDev code and converted code.

### `/wxcode:validate-schema`
Validate database schema models against legacy.

### `/wxcode:schema-dashboard`
Show schema conversion progress dashboard.

### `/wxcode:mcp-health-check`
Check MCP server health and connectivity.

---

## Design & Customization

### `/wxcode:design-system`
Manage the project's design system.

### `/wxcode:customize <name>`
Customize a specific command or agent.

### `/wxcode:set-profile`
Set user profile preferences.

### `/wxcode:settings`
Manage WXCODE settings.

---

## Session Management

### `/wxcode:pause-work`
Save current work state for later resumption.

### `/wxcode:resume-work`
Resume previously paused work.

### `/wxcode:debug`
Debug issues with scientific method approach.

---

## Community

### `/wxcode:join-discord`
Join the WXCODE community Discord.

---

## Configuration Files

```
.wxcode/
├── config.md           # Identity and settings
├── customizations.md   # Decision history
├── overrides.md        # Files with special handling
└── decisions/          # Per-command decision records
```

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Help displayed"} -->
```
</reference>
