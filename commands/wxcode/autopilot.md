---
name: wxcode:autopilot
description: Autonomous conversion loop — plan, execute, verify all phases without interaction
argument-hint: "[--resume]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - mcp__wxcode-kb__*
---

<objective>
Autonomous orchestrator for conversion milestones. Loops through all phases: plan, execute, verify. Then audits and completes the milestone. Zero user interaction.

**Requires:** AUTOPILOT-STATE.md created by `/wxcode:new-milestone --autopilot`.
**Resume:** `/wxcode:autopilot --resume` continues from saved state.
</objective>

<execution_context>
@~/.claude/wxcode-skill/references/ui-brand.md
@~/.claude/wxcode-skill/references/structured-output.md
</execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"autopilot","args":"$ARGUMENTS","title":"WXCODE ▶ AUTOPILOT"} -->
## WXCODE ▶ AUTOPILOT
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"new-milestone","args":"","description":"Start next milestone","priority":"recommended"} -->
```

**On errors:**
```
<!-- WXCODE:ERROR:{"code":"AUTOPILOT_STOPPED","message":"[reason]","recoverable":true} -->
```
</structured_output>

<output_rules>
**NEVER use `<sub>` tags or backtick-wrapped slash commands in user-facing output.**
- WRONG: `<sub>/clear first</sub>`
- WRONG: `` `/wxcode:plan-phase 1` ``
- RIGHT: `*Run clear first for fresh context window*`
- RIGHT: `Run: wxcode:plan-phase 1`
</output_rules>

<context>
Arguments: $ARGUMENTS
- `--resume` — Continue from saved AUTOPILOT-STATE.md

@.planning/AUTOPILOT-STATE.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/config.json
@.planning/MILESTONE-CONTEXT.md
</context>

<process>

## Phase 0: Load State

Read `.planning/AUTOPILOT-STATE.md`.

**If file does not exist:**
```
<!-- WXCODE:ERROR:{"code":"NO_STATE_FILE","message":"AUTOPILOT-STATE.md not found. Run new-milestone --autopilot first.","recoverable":false} -->

## ERROR: No autopilot state

AUTOPILOT-STATE.md not found. This file is created by:
  wxcode:new-milestone --autopilot --elements=A,B,C --output-project=xxx

Cannot proceed without state file.
```
**STOP.**

Parse from state file frontmatter:
- `status` — current status
- `current_phase` — last completed phase (0 = none)
- `total_phases` — from roadmap
- `retry_count` — current retry count
- `max_retries` — from config (default 3)
- `elements` — element list
- `output_project` — output project ID
- `milestone_id` — MongoDB milestone ID
- `milestone_folder` — folder name
- `version` — milestone version
- `project_name` — project name for MCP calls

**Resume logic (based on `status` field):**

| Status pattern | Resume behavior |
|---|---|
| `milestone_initialized` | Fresh start — begin Phase 2 loop from phase 1 |
| `phase_{N}_planned` | Phase {N} was planned — resume from Step 2b (execute) for phase {N} |
| `phase_{N}_executed` | Phase {N} was executed — resume from Step 2c (verify) for phase {N} |
| `phase_{N}_verified` | Phase {N} complete — resume from Step 2a (plan) for phase {N+1} |
| `audited` | All phases done, audit passed — resume from Phase 4 (complete) |
| `stopped_{step}` | Error occurred — display saved error from `error_reason`, then resume from the failed step. The `error_phase` and `error_step` fields tell exactly where to continue |
| `completed` | Display "Milestone already completed" and STOP |

**If `--resume` and status contains `stopped`:**
```
Autopilot was stopped at Phase {error_phase}, step: {error_step}
Reason: {error_reason}

Resuming from that point...
```
Clear error fields (`error_phase`, `error_step`, `error_reason` → null) and reset `retry_count` to 0 before continuing.

## Phase 1: Resolve Model Profile

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Read autopilot config overrides:
```bash
AUTOPILOT_MAX_RETRIES=$(cat .planning/config.json 2>/dev/null | grep -o '"max_retries_per_phase"[[:space:]]*:[[:space:]]*[0-9]*' | grep -o '[0-9]*$' || echo "3")
AUTOPILOT_SKIP_RESEARCH=$(cat .planning/config.json 2>/dev/null | grep -o '"skip_research"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
AUTOPILOT_AUTO_PUSH_TAG=$(cat .planning/config.json 2>/dev/null | grep -o '"auto_push_tag"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
```

**Model lookup table:**

| Agent | quality | balanced | budget |
|-------|---------|----------|--------|
| wxcode-planner | opus | sonnet | sonnet |
| wxcode-plan-checker | sonnet | sonnet | haiku |
| wxcode-executor | opus | sonnet | sonnet |
| wxcode-verifier | sonnet | sonnet | haiku |
| wxcode-rules-verifier | sonnet | sonnet | haiku |
| wxcode-integration-checker | sonnet | sonnet | haiku |

## Phase 2: Main Loop

Read ROADMAP.md to get total phases and phase details.

**For each phase from (current_phase + 1) to total_phases:**

Calculate progress: `base_progress = ((phase - 1) / total_phases) * 100`

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Phase {N} of {total}: starting","progress":{base_progress}} -->
```

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AUTOPILOT ► PHASE {N} of {total}: {phase_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 2a: PLAN PHASE

Extract phase details from ROADMAP.md (goal, requirements, success criteria).
Read MILESTONE-CONTEXT.md for dependency strategy (IMPLEMENT_LIST, STUB_LIST).

Spawn wxcode-planner agent:
```
Task(
  prompt: "
    <planning_context>
    Phase: {N} — {phase_name}
    Goal: {phase_goal}
    Requirements: {phase_requirements}
    Success criteria: {phase_success_criteria}

    ROADMAP: [inline ROADMAP.md phase section]
    REQUIREMENTS: [inline relevant requirements]
    MILESTONE-CONTEXT: [inline if exists]

    Config: @.planning/config.json
    </planning_context>

    <instructions>
    Create execution plan for phase {N}.
    - Skip research (--skip-research) — MCP is the source of truth for conversion
    - Force autonomous=true on ALL plans (no checkpoints, no user interaction)
    - Write PLAN.md files immediately
    - Return PLAN CREATED with summary
    </instructions>
  ",
  subagent_type: "wxcode-planner",
  model: "{planner_model}",
  description: "Plan phase {N}"
)
```

**If plan_check enabled in config:**

Spawn wxcode-plan-checker:
```
Task(
  prompt: "Verify plan for phase {N}. Read all PLAN.md files in .planning/phases/{NN}-*/",
  subagent_type: "wxcode-plan-checker",
  model: "{checker_model}",
  description: "Check phase {N} plan"
)
```

**If checker finds issues:**
- Re-spawn planner with revision context (max AUTOPILOT_MAX_RETRIES times)
- If still failing after max retries: **STOP** (see Stop Protocol below)

Update state:
```
Write AUTOPILOT-STATE.md: status = phase_{N}_planned, current_phase = {N}
Update progress table: Phase {N} Plan = done
```

### Step 2b: EXECUTE PHASE

Discover PLAN.md files in phase directory:
```bash
ls .planning/phases/{NN}-*/??-??-PLAN.md 2>/dev/null
```

Group plans by wave (from frontmatter `wave` field, default wave 1).

**For each wave (sequential):**
  Spawn wxcode-executor agents for each plan in the wave (parallel via Task):
  ```
  Task(
    prompt: "
      Execute plan: {plan_path}
      Phase: {N}
      autonomous=true — NO checkpoints, NO user interaction.
      Complete the full plan and write SUMMARY.md.

      MILESTONE-CONTEXT: [inline if exists — for stub signatures]
    ",
    subagent_type: "wxcode-executor",
    model: "{executor_model}",
    description: "Execute {plan_name}"
  )
  ```

Collect SUMMARY.md from each executor. Verify all plans have SUMMARY.md.

**If any executor failed (no SUMMARY.md):**
- Retry failed plan once
- If still failing: **STOP**

Update state:
```
Write AUTOPILOT-STATE.md: status = phase_{N}_executed
Update progress table: Phase {N} Execute = done
```

### Step 2c: VERIFY PHASE

Check if verifier is enabled:
```bash
VERIFIER_ENABLED=$(cat .planning/config.json 2>/dev/null | grep -o '"verifier"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
```

**If verifier enabled:**

Spawn wxcode-verifier:
```
Task(
  prompt: "
    Verify phase {N} goal achievement.
    Phase goal: {phase_goal}
    Success criteria: {phase_success_criteria}
    Read all SUMMARY.md files in .planning/phases/{NN}-*/
    Write VERIFICATION.md report.
  ",
  subagent_type: "wxcode-verifier",
  model: "{verifier_model}",
  description: "Verify phase {N}"
)
```

Read VERIFICATION.md status:
- **passed** — Mark phase complete, continue to next phase
- **gaps_found** (retry < max):
  - Spawn planner with `--gaps` context from VERIFICATION.md
  - Re-execute gap plans
  - Re-verify (1 gap-closure cycle per phase)
- **gaps_found** (retry >= max) — **STOP**
- **human_needed** — **STOP** (needs manual intervention)

**If conversion project:** Spawn wxcode-rules-verifier (advisory, non-blocking):
```
Task(
  prompt: "
    Verify business rules for phase {N}.
    Read SUMMARY.md files. Check against MCP business rules.
    Write RULES-CHECK.md report. Advisory only.
  ",
  subagent_type: "wxcode-rules-verifier",
  model: "{rules_verifier_model}",
  description: "Rules check phase {N}"
)
```

**If verifier disabled:** Skip verification, mark phase as verified.

Update state:
```
Write AUTOPILOT-STATE.md: status = phase_{N}_verified
Update progress table: Phase {N} Verify = done, Status = complete
```

### Step 2d: DASHBOARD

Regenerate dashboard between phases:
```bash
python3 ~/.claude/wxcode-skill/bin/generate-dashboard.py --all 2>/dev/null || true
```

**End of loop — continue to next phase.**

## Phase 3: AUDIT MILESTONE

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Auditing milestone","progress":90} -->
```

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AUTOPILOT ► AUDITING MILESTONE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Read all VERIFICATION.md files across phases.

Spawn wxcode-integration-checker:
```
Task(
  prompt: "
    Verify cross-phase integration for milestone {version}.
    Check E2E flows, phase connections, requirements coverage.
    Read ROADMAP.md, REQUIREMENTS.md, all VERIFICATION.md and SUMMARY.md files.
    Write integration report.
  ",
  subagent_type: "wxcode-integration-checker",
  model: "{checker_model}",
  description: "Integration check"
)
```

For conversion projects, check business rules coverage via MCP:
```
mcp__wxcode-kb__get_rules_verification_summary(milestone_id=MILESTONE_ID)
```

Evaluate audit result:
- **passed** or **tech_debt** — Continue (auto-accept tech debt in autopilot)
- **gaps_found** (critical blocker) — **STOP**

Write audit report to `.planning/{version}-MILESTONE-AUDIT.md`.

Update state:
```
Write AUTOPILOT-STATE.md: status = audited
```

## Phase 4: COMPLETE MILESTONE

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Completing milestone","progress":95} -->
```

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AUTOPILOT ► COMPLETING MILESTONE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4a: Archive artifacts

```bash
MILESTONE_FOLDER=".planning/milestones/${milestone_folder}"
cp .planning/ROADMAP.md "${MILESTONE_FOLDER}/${version}-ROADMAP.md"
cp .planning/REQUIREMENTS.md "${MILESTONE_FOLDER}/${version}-REQUIREMENTS.md"
rm .planning/ROADMAP.md .planning/REQUIREMENTS.md
```

### Step 4b: Update PROJECT.md

Read PROJECT.md. Update "Validated Requirements" with completed requirements. Update "Last updated" footer.

### Step 4c: Git tag and commit

```bash
git add -A
git commit -m "$(cat <<'EOF'
chore: complete milestone {version}

Autopilot conversion: {element_list}
Phases: {total_phases}
EOF
)"
git tag -a {version} -m "Milestone {version}: {element_list}"
```

**If auto_push_tag enabled:**
```bash
git push origin main && git push origin {version}
```

### Step 4d: MCP updates (conversion projects)

```
mcp__wxcode-kb__update_milestone_status(milestone_id=MILESTONE_ID, status="completed")
```

For each element in element list:
```
mcp__wxcode-kb__mark_converted(element_name=ELEM, project_name=PROJECT_NAME)
```

### Step 4e: Dashboard

```bash
python3 ~/.claude/wxcode-skill/bin/generate-dashboard.py --all 2>/dev/null || true
```

Update state:
```
Write AUTOPILOT-STATE.md: status = completed
```

## Phase 5: DONE

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Milestone complete","progress":100} -->
```

Display completion summary:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ▶ AUTOPILOT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Milestone {version} completed autonomously.

| Metric | Value |
|--------|-------|
| Elements | {element_list} |
| Phases | {total_phases} |
| Plans executed | {plan_count} |
| Verifications | {verify_count} passed |
| Business rules | {rules_coverage}% coverage |

All artifacts archived to .planning/milestones/{milestone_folder}/
```

```
<!-- WXCODE:NEXT_ACTION:{"command":"new-milestone","args":"","description":"Start next milestone","priority":"recommended"} -->
```

</process>

<stop_protocol>
## Stop & Notify Protocol

When autopilot encounters an irrecoverable error, it MUST:

1. Update AUTOPILOT-STATE.md with:
   - `status: stopped_{step}` (e.g., `stopped_plan_phase_2`)
   - `error_phase: {N}`
   - `error_step: {step}`
   - `error_reason: {reason}`
   - `updated_at: {timestamp}`
2. Emit structured error output
3. Emit NEXT_ACTION for resume (so UI can render "Resume" button)
4. Display human-readable error
5. STOP execution

```
<!-- WXCODE:ERROR:{"code":"AUTOPILOT_STOPPED","phase":{N},"step":"{step}","recoverable":true} -->

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AUTOPILOT ► STOPPED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase:** {N} of {total}
**Step:** {step description}
**Reason:** {detailed explanation}
**Retries:** {X} of {max}

### State Saved

AUTOPILOT-STATE.md updated. To resume after fixing:

Run: wxcode:autopilot --resume
```

```
<!-- WXCODE:NEXT_ACTION:{"command":"autopilot","args":"--resume","description":"Resume autopilot from phase {N}","priority":"required"} -->
```

**Stop triggers:**
- Plan checker fails after max retries
- Executor fails after 1 retry
- Verifier returns `human_needed`
- Verifier gaps after max retries
- Audit finds critical blockers
- MCP call fails for critical operation
</stop_protocol>

<success_criteria>
- [ ] State file loaded and parsed correctly
- [ ] Model profile resolved from config
- [ ] All phases planned (PLAN.md files exist)
- [ ] All phases executed (SUMMARY.md files exist)
- [ ] All phases verified (VERIFICATION.md files exist, if verifier enabled)
- [ ] Business rules checked (advisory, if conversion project)
- [ ] Integration audit passed
- [ ] Artifacts archived to milestones folder
- [ ] PROJECT.md updated with validated requirements
- [ ] Git commit and tag created
- [ ] MCP milestone status updated (conversion projects)
- [ ] MCP elements marked as converted (conversion projects)
- [ ] Dashboard regenerated
- [ ] AUTOPILOT-STATE.md shows status=completed
- [ ] Stop protocol followed on any irrecoverable error
</success_criteria>
