---
type: prompt
name: wxcode:complete-milestone
description: Archive completed milestone and prepare for next version
argument-hint: <version>
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__wxcode-kb__get_conversion_stats
---

<objective>
Mark milestone {{version}} complete, archive to milestones/, and update ROADMAP.md and REQUIREMENTS.md.

Purpose: Create historical record of shipped version, archive milestone artifacts (roadmap + requirements), and prepare for next milestone.
Output: Milestone archived (roadmap + requirements), PROJECT.md evolved, git tagged.
</objective>

<execution_context>
**Load these files NOW (before proceeding):**

- @~/.claude/get-shit-done/workflows/complete-milestone.md (main workflow)
- @~/.claude/get-shit-done/templates/milestone-archive.md (archive template)
  </execution_context>

<context>
**Project files:**
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `.planning/STATE.md`
- `.planning/PROJECT.md`

**User input:**

- Version: {{version}} (e.g., "1.0", "1.1", "2.0")
  </context>

<process>

**Follow complete-milestone.md workflow:**

0. **Check for audit:**

   - Look for `.planning/v{{version}}-MILESTONE-AUDIT.md`
   - If missing or stale: recommend `/wxcode:audit-milestone` first
   - If audit status is `gaps_found`: recommend `/wxcode:plan-milestone-gaps` first
   - If audit status is `passed`: proceed to step 1

   ```markdown
   ## Pre-flight Check

   {If no v{{version}}-MILESTONE-AUDIT.md:}
   ⚠ No milestone audit found. Run `/wxcode:audit-milestone` first to verify
   requirements coverage, cross-phase integration, and E2E flows.

   {If audit has gaps:}
   ⚠ Milestone audit found gaps. Run `/wxcode:plan-milestone-gaps` to create
   phases that close the gaps, or proceed anyway to accept as tech debt.

   {If audit passed:}
   ✓ Milestone audit passed. Proceeding with completion.
   ```

1. **Verify readiness:**

   - Check all phases in milestone have completed plans (SUMMARY.md exists)
   - Present milestone scope and stats
   - Wait for confirmation

2. **Gather stats:**

   - Count phases, plans, tasks
   - Calculate git range, file changes, LOC
   - Extract timeline from git log
   - Present summary, confirm

3. **Extract accomplishments:**

   - Read all phase SUMMARY.md files in milestone range
   - Extract 4-6 key accomplishments
   - Present for approval

4. **Archive milestone:**

   - Create `.planning/milestones/v{{version}}-ROADMAP.md`
   - Extract full phase details from ROADMAP.md
   - Fill milestone-archive.md template
   - Update ROADMAP.md to one-line summary with link

5. **Archive requirements:**

   - Create `.planning/milestones/v{{version}}-REQUIREMENTS.md`
   - Mark all v1 requirements as complete (checkboxes checked)
   - Note requirement outcomes (validated, adjusted, dropped)
   - Delete `.planning/REQUIREMENTS.md` (fresh one created for next milestone)

6. **Update PROJECT.md:**

   - Add "Current State" section with shipped version
   - Add "Next Milestone Goals" section
   - Archive previous content in `<details>` (if v1.1+)

7. **Commit and tag:**

   - Stage: MILESTONES.md, PROJECT.md, ROADMAP.md, STATE.md, archive files
   - Commit: `chore: archive v{{version}} milestone`
   - Tag: `git tag -a v{{version}} -m "[milestone summary]"`
   - Ask about pushing tag

8. **Offer next steps:**
   - `/wxcode:new-milestone` — start next milestone (questioning → research → requirements → roadmap)

</process>

<success_criteria>

- Milestone archived to `.planning/milestones/v{{version}}-ROADMAP.md`
- Requirements archived to `.planning/milestones/v{{version}}-REQUIREMENTS.md`
- `.planning/REQUIREMENTS.md` deleted (fresh for next milestone)
- ROADMAP.md collapsed to one-line entry
- PROJECT.md updated with current state
- Git tag v{{version}} created
- Commit successful
- Dashboard updated
- User knows next steps (including need for fresh requirements)
</success_criteria>

<dashboard_update>

## Update Dashboards (Final Step)

After milestone completion, update TWO dashboards:
1. **Project dashboard** (global) — `.planning/dashboard.json`
2. **Milestone dashboard** — `.planning/dashboard_<milestone>.json`

**References:**
- Project dashboard: `~/.claude/get-shit-done/references/dashboard-schema-project.md`
- Milestone dashboard: `~/.claude/get-shit-done/references/dashboard-schema-milestone.md`

### Step 1: Determine milestone folder name

Read from STATE.md or CONVERSION.md:
```
MILESTONE_FOLDER_NAME="v[X.Y]-[element_name]"
```

### Step 2: Gather conversion data (if conversion project)

**Use HYBRID approach:**
```
mcp__wxcode-kb__get_conversion_stats(project_name=PROJECT_NAME)
```

Use MCP response for `conversion.elements_converted` and `conversion.elements_total`.
Use CONVERSION.md for `conversion.stack`.

### Step 3: Update project dashboard

1. Read current `.planning/dashboard.json`
2. Update milestone status to "completed" in `milestones[]`
3. Update `milestones[].completed_at` with current timestamp
4. Update `progress.milestones_complete`
5. Update `conversion.*` with hybrid data
6. Set `current_milestone` to null (no active milestone)
7. Write to `.planning/dashboard.json`
8. Output: `[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json`

### Step 4: Update milestone dashboard

1. Read `.planning/dashboard_${MILESTONE_FOLDER_NAME}.json`
2. Set `milestone.status` to "completed"
3. Set `milestone.completed_at` to current timestamp
4. Ensure all phases show "complete" status
5. Update `progress` to 100%
6. Write to `.planning/dashboard_${MILESTONE_FOLDER_NAME}.json`
7. Output: `[WXCODE:DASHBOARD_UPDATED] .planning/dashboard_<milestone>.json`

### Step 5: Update workflow stages

Complete the `workflow` section:

1. Set `workflow.stages[6]` (archived) to `"status": "complete"`, `"completed_at": "<now>"`
2. Update `workflow.current_stage` to `"archived"`
3. Ensure all previous stages are marked complete

```json
"workflow": {
  "current_stage": "archived",
  "stages": [
    { "id": "created", "status": "complete", "completed_at": "..." },
    { "id": "requirements", "status": "complete", "completed_at": "..." },
    { "id": "roadmap", "status": "complete", "completed_at": "..." },
    { "id": "planning", "status": "complete", "completed_at": "..." },
    { "id": "executing", "status": "complete", "completed_at": "..." },
    { "id": "verified", "status": "complete", "completed_at": "..." },
    { "id": "archived", "status": "complete", "completed_at": "<now>" }
  ]
}
```

**IMPORTANT:** Use the EXACT schemas from the reference files. Do NOT invent a different format.

</dashboard_update>

<critical_rules>

- **Load workflow first:** Read complete-milestone.md before executing
- **Verify completion:** All phases must have SUMMARY.md files
- **User confirmation:** Wait for approval at verification gates
- **Archive before deleting:** Always create archive files before updating/deleting originals
- **One-line summary:** Collapsed milestone in ROADMAP.md should be single line with link
- **Context efficiency:** Archive keeps ROADMAP.md and REQUIREMENTS.md constant size per milestone
- **Fresh requirements:** Next milestone starts with `/wxcode:new-milestone` which includes requirements definition
  </critical_rules>
