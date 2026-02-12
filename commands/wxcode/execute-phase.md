---
name: wxcode:execute-phase
description: Execute all plans in a phase with wave-based parallelization
argument-hint: "<phase-number> [--gaps-only]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - TodoWrite
  - AskUserQuestion
---

<objective>
Execute all plans in a phase using wave-based parallel execution.

Orchestrator stays lean: discover plans, analyze dependencies, group into waves, spawn subagents, collect results. Each subagent loads the full execute-plan context and handles its own plan.

Context budget: ~15% orchestrator, 100% fresh per subagent.
</objective>

<execution_context>
@~/.claude/wxcode-skill/references/ui-brand.md
@~/.claude/wxcode-skill/references/structured-output.md
@~/.claude/wxcode-skill/workflows/execute-phase.md
</execution_context>

<context>
Phase: $ARGUMENTS

**Flags:**
- `--gaps-only` — Execute only gap closure plans (plans with `gap_closure: true` in frontmatter). Use after verify-work creates fix plans.

@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<structured_output>
## Structured Output (MANDATORY)

Emit structured markers alongside human-readable output. Reference: structured-output.md

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"execute-phase","args":"$ARGUMENTS","title":"WXCODE ▶ EXECUTING PHASE $ARGUMENTS"} -->
## WXCODE ▶ EXECUTING PHASE $ARGUMENTS
```

**Before each significant tool call:**
```
<!-- WXCODE:TOOL:{"tool":"Bash","description":"Get model profile from config"} -->
```

**After tool completes:**
```
<!-- WXCODE:TOOL_RESULT:{"tool":"Bash","success":true,"output":"balanced"} -->
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing wave 1 of 2","progress":25} -->
```

**At command end (in offer_next):**
```
<!-- WXCODE:NEXT_ACTION:{"command":"discuss-phase","args":"4","description":"Gather context for next phase","priority":"recommended"} -->
```

**On errors:**
```
<!-- WXCODE:ERROR:{"code":"PHASE_NOT_FOUND","message":"Phase 99 does not exist in roadmap","recoverable":false} -->
```
</structured_output>

<output_rules>
**NEVER use `<sub>` tags or backtick-wrapped slash commands in user-facing output.**
- WRONG: `<sub>/clear first → fresh context window</sub>`
- WRONG: `` `/wxcode:verify-work 1` ``
- RIGHT: `*Run clear first for fresh context window*`
- RIGHT: `Run: wxcode:verify-work 1`

Slash commands in output get parsed as command invocations. Always use plain text.
</output_rules>

<process>
0. **Emit header and resolve Model Profile**

   Emit the structured header immediately followed by the visual banner (no blank line):
   ```
   <!-- WXCODE:HEADER:{"command":"execute-phase","args":"$ARGUMENTS","title":"WXCODE ▶ EXECUTING PHASE $ARGUMENTS"} -->
   ## WXCODE ▶ EXECUTING PHASE $ARGUMENTS
   ```

   Then resolve model:

   Read model profile for agent spawning:
   ```bash
   MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
   ```

   Default to "balanced" if not set.

   **Model lookup table:**

   | Agent | quality | balanced | budget |
   |-------|---------|----------|--------|
   | wxcode-executor | opus | sonnet | sonnet |
   | wxcode-verifier | sonnet | sonnet | haiku |
   | wxcode-rules-verifier | sonnet | sonnet | haiku |

   Store resolved models for use in Task calls below.

1. **Validate phase exists**
   - Find phase directory matching argument
   - Count PLAN.md files
   - Error if no plans found

1.5. **Check database model requirements (Conversion Projects)**

   **Skip if:** `.planning/CONVERSION.md` does not exist (greenfield project).

   **For conversion projects:**

   Check if this phase involves database models by examining the phase name and plan contents:

   ```bash
   PHASE_NAME=$(basename .planning/phases/*-${PHASE_NUMBER}-*)
   IS_DB_PHASE=$(echo "$PHASE_NAME" | grep -iE "database|model|schema" && echo "yes" || echo "no")
   ```

   **If IS_DB_PHASE="yes" OR plans reference table operations:**

   Get tables needed for this phase from PLAN.md files:
   ```bash
   grep -h "table\|TABLE\|model" .planning/phases/*-${PHASE_NUMBER}-*/*-PLAN.md 2>/dev/null
   ```

   **If tables are referenced and models might be missing:**

   Spawn schema generator to validate/generate:

   ```
   Task(wxcode-schema-generator):
     prompt: |
       Validate and generate any missing database models for phase execution.

       Output Project ID: [from .planning/CONVERSION.md]
       Phase: ${PHASE_NUMBER}

       Use capability: validate_models first, then generate_specific_models if needed.

       Steps:
       1. Check which table models already exist
       2. Identify tables referenced in phase plans
       3. Generate any missing models (preserving exact legacy names)
       4. Return summary of models ready

     subagent_type: wxcode-schema-generator
   ```

   Display result:
   ```
   ✓ Database models verified for phase ${PHASE_NUMBER}
     [N] models exist, [M] generated
   ```

   **If validation fails:** Stop and report - cannot execute phase without required models.

2. **Discover plans**
   - List all *-PLAN.md files in phase directory
   - Check which have *-SUMMARY.md (already complete)
   - If `--gaps-only`: filter to only plans with `gap_closure: true`
   - Build list of incomplete plans

3. **Group by wave**
   - Read `wave` from each plan's frontmatter
   - Group plans by wave number
   - Report wave structure to user

4. **Execute waves**
   For each wave in order:
   - Spawn `wxcode-executor` for each plan in wave (parallel Task calls)
   - Wait for completion (Task blocks)
   - Verify SUMMARYs created
   - Regenerate dashboard (progress tracking between waves):
     ```bash
     python3 ~/.claude/wxcode-skill/bin/generate-dashboard.py --all --project-dir .
     ```
   - Proceed to next wave

5. **Aggregate results**
   - Collect summaries from all plans
   - Report phase completion status

6. **Commit any orchestrator corrections**
   Check for uncommitted changes before verification:
   ```bash
   git status --porcelain
   ```

   **If changes exist:** Orchestrator made corrections between executor completions. Stage and commit them individually:
   ```bash
   # Stage each modified file individually (never use git add -u, git add ., or git add -A)
   git status --porcelain | grep '^ M' | cut -c4- | while read file; do
     git add "$file"
   done
   git commit -m "fix({phase}): orchestrator corrections"
   ```

   **If clean:** Continue to verification.

7. **Verify phase goal**
   Check config: `WORKFLOW_VERIFIER=$(cat .planning/config.json 2>/dev/null | grep -o '"verifier"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")`

   **If `workflow.verifier` is `false`:** Skip to step 8 (treat as passed).

   **Otherwise:**
   - Spawn `wxcode-verifier` subagent with phase directory and goal
   - Verifier checks must_haves against actual codebase (not SUMMARY claims)
   - Creates VERIFICATION.md with detailed report
   - Route by status:
     - `passed` → continue to step 8
     - `human_needed` → present items, get approval or feedback
     - `gaps_found` → present gaps, offer `/wxcode:plan-phase {X} --gaps`

7.5. **Verify business rules (Conversion Projects Only)**
   Check if this is a conversion project AND rules tracking is initialized:
   ```bash
   CONVERSION_EXISTS=$([ -f .planning/CONVERSION.md ] && echo "yes" || echo "no")
   RULES_SUMMARY_EXISTS=$([ -f .planning/rules-summary.json ] && echo "yes" || echo "no")
   ```

   Also check config toggle:
   ```bash
   WORKFLOW_RULES_VERIFIER=$(cat .planning/config.json 2>/dev/null | grep -o '"rules_verifier"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
   ```

   **If `CONVERSION_EXISTS=yes` AND `WORKFLOW_RULES_VERIFIER` is not `false`:**

   Get milestone ID from MILESTONE.json:
   ```bash
   MILESTONE_DIR=$(ls -d .planning/milestones/v*/ 2>/dev/null | tail -1)
   MILESTONE_ID=$(cat "${MILESTONE_DIR}/MILESTONE.json" 2>/dev/null | grep -o '"mongodb_id"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"')
   ```

   **If MILESTONE_ID exists (rules tracking was initialized in Phase 1.87):**

   Spawn `wxcode-rules-verifier` subagent:

   ```
   Task(
     prompt="Verify business rules for Phase ${PHASE_NUMBER} of milestone ${MILESTONE_ID}.

   Phase directory: ${PHASE_DIR}
   Milestone ID: ${MILESTONE_ID}
   Phase number: ${PHASE_NUMBER}

   1. Call get_milestone_rules(milestone_id=${MILESTONE_ID}, status='pending', include_rule_details=true)
   2. For each pending rule: search converted code for evidence (Grep/Read)
   3. Determine status: implemented/adapted/missing/not_applicable
   4. Call batch_update_rule_verifications with results (confirm=true)
   5. Write rules-summary.json cache
   6. Generate RULES-CHECK.md report in phase directory",
     subagent_type="wxcode-rules-verifier",
     model="{verifier_model}"
   )
   ```

   Display result:
   ```
   ✓ Business rules check complete
     Rules: {implemented + adapted} / {total checked} verified
     Missing: {missing_count}
     Report: .planning/phases/{phase_dir}/{phase}-RULES-CHECK.md
   ```

   **This check is ADVISORY** — missing rules do NOT block phase completion. They are reported for awareness and tracked in MongoDB for the milestone audit.

   **If MILESTONE_ID is empty or rules tracking not initialized:** Skip silently.

8. **Update roadmap and state**
   - Update ROADMAP.md, STATE.md

9. **Update requirements**
   Mark phase requirements as Complete:
   - Read ROADMAP.md, find this phase's `Requirements:` line (e.g., "AUTH-01, AUTH-02")
   - Read REQUIREMENTS.md traceability table
   - For each REQ-ID in this phase: change Status from "Pending" to "Complete"
   - Write updated REQUIREMENTS.md
   - Skip if: REQUIREMENTS.md doesn't exist, or phase has no Requirements line

10. **Commit phase completion**
    Check `COMMIT_PLANNING_DOCS` from config.json (default: true).
    If false: Skip git operations for .planning/ files.
    If true: Bundle all phase metadata updates in one commit:
    - Stage: `git add .planning/ROADMAP.md .planning/STATE.md`
    - Stage REQUIREMENTS.md if updated: `git add .planning/REQUIREMENTS.md`
    - Commit: `docs({phase}): complete {phase-name} phase`

10.5. **Update dashboards**
    Regenerate dashboards to reflect completed phase:
    ```bash
    python3 ~/.claude/wxcode-skill/bin/generate-dashboard.py --all --project-dir .
    ```

11. **Offer next steps**
    - Route to next action (see `<offer_next>`)
</process>

<offer_next>
Output this markdown directly (not as a code block). Route based on status.

**IMPORTANT:** Always emit structured markers BEFORE the visual output.

| Status | Route |
|--------|-------|
| `gaps_found` | Route C (gap closure) |
| `human_needed` | Present checklist, then re-route based on approval |
| `passed` + more phases | Route A (next phase) |
| `passed` + last phase | Route B (milestone complete) |

---

**Route A: Phase verified, more phases remain**

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Phase {Z} complete","progress":100,"phase":{Z}} -->
<!-- WXCODE:NEXT_ACTION:{"command":"discuss-phase","args":"{Z+1}","description":"Gather context for next phase","priority":"recommended"} -->
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► PHASE {Z} COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

{Y} plans executed
Goal verified ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

/wxcode:discuss-phase {Z+1} — gather context and clarify approach

*Run clear first for fresh context window*

───────────────────────────────────────────────────────────────

**Also available:**
- /wxcode:plan-phase {Z+1} — skip discussion, plan directly
- /wxcode:verify-work {Z} — manual acceptance testing before continuing

───────────────────────────────────────────────────────────────

---

**Route B: Phase verified, milestone complete**

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Milestone complete","progress":100} -->
<!-- WXCODE:NEXT_ACTION:{"command":"audit-milestone","args":"","description":"Verify requirements and cross-phase integration","priority":"recommended"} -->
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► MILESTONE COMPLETE 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**v1.0**

{N} phases completed
All phase goals verified ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Audit milestone** — verify requirements, cross-phase integration, E2E flows

/wxcode:audit-milestone

*Run clear first for fresh context window*

───────────────────────────────────────────────────────────────

**Also available:**
- /wxcode:verify-work — manual acceptance testing
- /wxcode:complete-milestone — skip audit, archive directly

───────────────────────────────────────────────────────────────

---

**Route C: Gaps found — need additional planning**

```
<!-- WXCODE:STATUS:{"status":"failed","message":"Phase {Z} has gaps","progress":75,"phase":{Z}} -->
<!-- WXCODE:NEXT_ACTION:{"command":"plan-phase","args":"{Z} --gaps","description":"Create plans to close the gaps","priority":"required"} -->
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► PHASE {Z} GAPS FOUND ⚠
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Phase {Z}: {Name}**

Score: {N}/{M} must-haves verified
Report: .planning/phases/{phase_dir}/{phase}-VERIFICATION.md

### What's Missing

{Extract gap summaries from VERIFICATION.md}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Plan gap closure** — create additional plans to complete the phase

/wxcode:plan-phase {Z} --gaps

*Run clear first for fresh context window*

───────────────────────────────────────────────────────────────

**Also available:**
- cat .planning/phases/{phase_dir}/{phase}-VERIFICATION.md — see full report
- /wxcode:verify-work {Z} — manual testing before planning

───────────────────────────────────────────────────────────────

---

After user runs /wxcode:plan-phase {Z} --gaps:
1. Planner reads VERIFICATION.md gaps
2. Creates plans 04, 05, etc. to close gaps
3. User runs /wxcode:execute-phase {Z} again
4. Execute-phase runs incomplete plans (04, 05...)
5. Verifier runs again → loop until passed
</offer_next>

<wave_execution>
**Parallel spawning:**

Before spawning, read file contents. The `@` syntax does not work across Task() boundaries.

```bash
# Read each plan and STATE.md
PLAN_01_CONTENT=$(cat "{plan_01_path}")
PLAN_02_CONTENT=$(cat "{plan_02_path}")
PLAN_03_CONTENT=$(cat "{plan_03_path}")
STATE_CONTENT=$(cat .planning/STATE.md)

# For conversion projects: read MILESTONE-CONTEXT.md (has dependency signatures for stub generation)
MILESTONE_CONTEXT=""
if [ -f .planning/CONVERSION.md ]; then
  MILESTONE_DIR=$(ls -d .milestones/v*/ 2>/dev/null | tail -1)
  if [ -n "$MILESTONE_DIR" ]; then
    MILESTONE_CONTEXT=$(cat "${MILESTONE_DIR}/MILESTONE-CONTEXT.md" 2>/dev/null)
  fi
fi
```

Spawn all plans in a wave with a single message containing multiple Task calls, with inlined content:

```
# For conversion projects, append milestone context to each prompt:
# "\n\nMilestone context:\n{milestone_context}"

Task(prompt="Execute plan at {plan_01_path}\n\nPlan:\n{plan_01_content}\n\nProject state:\n{state_content}\n\nMilestone context:\n{milestone_context}", subagent_type="wxcode-executor", model="{executor_model}")
Task(prompt="Execute plan at {plan_02_path}\n\nPlan:\n{plan_02_content}\n\nProject state:\n{state_content}\n\nMilestone context:\n{milestone_context}", subagent_type="wxcode-executor", model="{executor_model}")
Task(prompt="Execute plan at {plan_03_path}\n\nPlan:\n{plan_03_content}\n\nProject state:\n{state_content}\n\nMilestone context:\n{milestone_context}", subagent_type="wxcode-executor", model="{executor_model}")
```

All three run in parallel. Task tool blocks until all complete.

**No polling.** No background agents. No TaskOutput loops.
</wave_execution>

<checkpoint_handling>
Plans with `autonomous: false` have checkpoints. The execute-phase.md workflow handles the full checkpoint flow:
- Subagent pauses at checkpoint, returns structured state
- Orchestrator presents to user, collects response
- Spawns fresh continuation agent (not resume)

See `@~/.claude/wxcode/workflows/execute-phase.md` step `checkpoint_handling` for complete details.
</checkpoint_handling>

<deviation_rules>
During execution, handle discoveries automatically:

1. **Auto-fix bugs** - Fix immediately, document in Summary
2. **Auto-add critical** - Security/correctness gaps, add and document
3. **Auto-fix blockers** - Can't proceed without fix, do it and document
4. **Ask about architectural** - Major structural changes, stop and ask user

Only rule 4 requires user intervention.
</deviation_rules>

<commit_rules>
**Per-Task Commits:**

After each task completes:
1. Stage only files modified by that task
2. Commit with format: `{type}({phase}-{plan}): {task-name}`
3. Types: feat, fix, test, refactor, perf, chore
4. Record commit hash for SUMMARY.md

**Plan Metadata Commit:**

After all tasks in a plan complete:
1. Stage plan artifacts only: PLAN.md, SUMMARY.md
2. Commit with format: `docs({phase}-{plan}): complete [plan-name] plan`
3. NO code files (already committed per-task)

**Phase Completion Commit:**

After all plans in phase complete (step 7):
1. Stage: ROADMAP.md, STATE.md, REQUIREMENTS.md (if updated), VERIFICATION.md
2. Commit with format: `docs({phase}): complete {phase-name} phase`
3. Bundles all phase-level state updates in one commit

**NEVER use:**
- `git add .`
- `git add -A`
- `git add src/` or any broad directory

**Always stage files individually.**
</commit_rules>

<success_criteria>
- [ ] All incomplete plans in phase executed
- [ ] Each plan has SUMMARY.md
- [ ] Phase goal verified (must_haves checked against codebase)
- [ ] VERIFICATION.md created in phase directory
- [ ] (Conversion projects) Business rules verified (advisory) — RULES-CHECK.md created
- [ ] (Conversion projects) rules-summary.json cache updated
- [ ] STATE.md reflects phase completion
- [ ] ROADMAP.md updated
- [ ] REQUIREMENTS.md updated (phase requirements marked Complete)
- [ ] User informed of next steps
</success_criteria>
