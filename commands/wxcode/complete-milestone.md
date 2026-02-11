---
type: prompt
name: wxcode:complete-milestone
description: Archive completed milestone and prepare for next version
argument-hint: <version>
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - mcp__wxcode-kb__get_conversion_stats
  - mcp__wxcode-kb__update_milestone_status
  - mcp__wxcode-kb__mark_converted
---

<objective>
Mark milestone {{version}} complete, archive to milestones/, and update ROADMAP.md and REQUIREMENTS.md.

Purpose: Create historical record of shipped version, archive milestone artifacts (roadmap + requirements), and prepare for next milestone.
Output: Milestone archived (roadmap + requirements), PROJECT.md evolved, git tagged.
</objective>

<execution_context>
**Load these files NOW (before proceeding):**

- @~/.claude/wxcode-skill/workflows/complete-milestone.md (main workflow)
- @~/.claude/wxcode-skill/templates/milestone-archive.md (archive template)
  </execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"complete-milestone","args":"$ARGUMENTS","title":"WXCODE ▶ COMPLETING MILESTONE $ARGUMENTS"} -->
## WXCODE ▶ COMPLETING MILESTONE $ARGUMENTS
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"new-milestone","args":"","description":"Start next milestone","priority":"recommended"} -->
```
</structured_output>



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

8. **Update milestone status in KB:**

   - Find the milestone ID from `.milestones/` context files or CONTEXT.md
   - Call MCP tool to mark milestone as completed:

   ```
   mcp__wxcode-kb__update_milestone_status(
       milestone_id="<milestone_id>",
       status="completed",
       confirm=True
   )
   ```

   - This updates the MongoDB record to reflect completion

   **Mark ALL elements as converted:**

   Read ELEMENT_LIST from MILESTONE.json (`"elements"` array, fallback to `["element"]`):

   ```
   For each ELEM in ELEMENT_LIST:
     mcp__wxcode-kb__mark_converted(
       element_name=ELEM,
       project_name=<project_name>,
       confirm=true,
       notes="Converted in milestone v{{version}}"
     )
   ```

   Display: `✓ Marked ${ELEMENT_COUNT} element(s) as converted`

9. **Regenerate dashboards (MANDATORY):**

   ```bash
   python3 ~/.claude/wxcode-skill/bin/generate-dashboard.py --all --project-dir .
   ```

   This updates:
   - `.planning/dashboard.json` — project dashboard
   - `.planning/dashboard_v{{version}}-*.json` — milestone dashboard with archived status

10. **Worktree merge and cleanup (if running in worktree):**

    Detect if we're in a worktree:
    ```bash
    IS_WORKTREE=$(git rev-parse --git-common-dir 2>/dev/null | grep -v "^\.git$" && echo "true" || echo "false")
    ```

    **If NOT in a worktree:** Skip to step 11.

    **If in a worktree:**

    a) **Clean planning files** (these are per-milestone, shouldn't go to main):
    ```bash
    rm -f .planning/ROADMAP.md
    rm -f .planning/REQUIREMENTS.md
    rm -f .planning/STATE.md
    rm -rf .planning/phases/
    rm -rf .planning/research/
    ```

    b) **Update MILESTONE.json status:**
    ```bash
    # Update the placeholder that was committed on main
    # (it's in .planning/milestones/${MILESTONE_FOLDER}/MILESTONE.json)
    ```
    Update status to "completed", add `completed_at` and `tag` fields.

    c) **Commit cleanup:**
    ```bash
    git add -A .planning/
    git commit -m "chore: prepare v{{version}} for merge to main"
    ```

    d) **Offer merge options:**

    Use AskUserQuestion:
    - header: "Merge"
    - question: "How should this milestone be merged to main?"
    - options:
      - "Squash merge (Recommended)" — One clean commit on main with all milestone work
      - "Regular merge" — Preserve all individual commits on main
      - "Skip" — I'll merge manually later

    **If "Squash merge":**

    Read MILESTONE.json to determine element(s):
    ```bash
    MILESTONE_JSON=$(cat .planning/milestones/*/MILESTONE.json 2>/dev/null | head -1)
    # Parse elements array and element_count
    ```

    ```bash
    MAIN_PATH=$(git rev-parse --git-common-dir | sed 's/\.git$//')
    BRANCH_NAME=$(git branch --show-current)
    git -C "${MAIN_PATH}" merge --squash ${BRANCH_NAME}

    # Commit message depends on element count:
    # Single element:  "feat: convert PAGE_Login (v1.0)"
    # Multi-element:   "feat: convert 3 elements (v1.0)"
    ```
    If single element: `git -C "${MAIN_PATH}" commit -m "feat: convert ${ELEMENT_NAME} (v{{version}})"`
    If multi-element: `git -C "${MAIN_PATH}" commit -m "feat: convert ${ELEMENT_COUNT} elements (v{{version}})"`

    **If "Regular merge":**
    ```bash
    git -C "${MAIN_PATH}" merge ${BRANCH_NAME}
    ```

    **If "Skip":** Display merge instructions for later.

    e) **Handle merge conflicts (if any):**
    - Display conflicting files
    - Instruct user to resolve in main directory
    - Offer: "Conflicts are typically in barrel/index files — add both imports"

    f) **Cleanup worktree:**

    Use AskUserQuestion:
    - header: "Cleanup"
    - question: "Remove this worktree and branch?"
    - options:
      - "Yes, clean up (Recommended)" — Remove worktree and delete branch
      - "Keep worktree" — I may need to reference this later

    **If "Yes, clean up":**
    ```bash
    WORKTREE_PATH=$(pwd)
    BRANCH_NAME=$(git branch --show-current)

    # Must leave worktree before removing
    cd "${MAIN_PATH}"
    git worktree remove "${WORKTREE_PATH}"
    git branch -d "${BRANCH_NAME}" 2>/dev/null || echo "Branch preserved (has unmerged commits)"
    ```

    Display:
    ```
    ✓ Worktree removed: ${WORKTREE_PATH}
    ✓ Branch deleted: ${BRANCH_NAME}

    Continue working in your main project directory.
    ```

11. **Offer next steps:**
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
- Milestone status updated in KB via MCP (`status="completed"`)
- Dashboard updated
- **(If worktree)** Planning files cleaned (ROADMAP, REQUIREMENTS, STATE, phases/, research/)
- **(If worktree)** MILESTONE.json updated to completed
- **(If worktree)** Merge to main offered (squash/regular/skip)
- **(If worktree)** Worktree removal offered
- User knows next steps (including need for fresh requirements)
</success_criteria>

<dashboard_update>

## Update Dashboards (Final Step)

**MANDATORY:** After state changes, regenerate dashboards using the Python script.

```bash
python3 ~/.claude/wxcode-skill/bin/generate-dashboard.py --all --project-dir .
```

This script:
- Parses all `.planning/` files deterministically
- Extracts tasks from PLAN.md XML blocks
- Generates proper nested `phases[].plans[].tasks[]` structure
- Outputs `[WXCODE:DASHBOARD_UPDATED]` notifications

**Do NOT generate dashboard JSON manually via LLM.**

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
