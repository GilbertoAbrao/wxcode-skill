---
name: wxcode:progress
description: Check project progress, show context, and route to next action (execute or plan)
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - SlashCommand
---

<execution_context>
@~/.claude/get-shit-done/references/structured-output.md
</execution_context>

<structured_output>
## Structured Output (MANDATORY)

Emit structured markers alongside human-readable output.

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"progress","args":"","title":"WXCODE ▶ PROJECT PROGRESS"} -->
## WXCODE ▶ PROJECT PROGRESS
```

**With status report (emit after loading context):**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Phase 3 of 5","progress":60,"phase":3} -->
```

**At command end (based on route):**
```
<!-- WXCODE:NEXT_ACTION:{"command":"execute-phase","args":"3","description":"Execute planned tasks","priority":"recommended"} -->
```
or
```
<!-- WXCODE:NEXT_ACTION:{"command":"plan-phase","args":"3","description":"Create execution plan","priority":"recommended"} -->
```
or
```
<!-- WXCODE:NEXT_ACTION:{"command":"complete-milestone","args":"","description":"Archive milestone","priority":"recommended"} -->
```
</structured_output>

<objective>
Check project progress, summarize recent work and what's ahead, then intelligently route to the next action - either executing an existing plan or creating the next one.

Provides situational awareness before continuing work.
</objective>


<process>

<step name="header">
**Emit structured header:**

```
<!-- WXCODE:HEADER:{"command":"progress","args":"","title":"WXCODE ▶ PROJECT PROGRESS"} -->
## WXCODE ▶ PROJECT PROGRESS
```
</step>

<step name="verify">
**Verify planning structure exists:**

Use Bash (not Glob) to check—Glob respects .gitignore but .planning/ is often gitignored:

```bash
test -d .planning && echo "exists" || echo "missing"
```

If no `.planning/` directory:

```
No planning structure found.

Run /wxcode:new-project to start a new project.
```

Exit.

If missing STATE.md: suggest `/wxcode:new-project`.

**If ROADMAP.md missing but PROJECT.md exists:**

This means a milestone was completed and archived. Go to **Route F** (between milestones).

If missing both ROADMAP.md and PROJECT.md: suggest `/wxcode:new-project`.
</step>

<step name="load">
**Load full project context:**

- Read `.planning/STATE.md` for living memory (position, decisions, issues)
- Read `.planning/ROADMAP.md` for phase structure and objectives
- Read `.planning/PROJECT.md` for current state (What This Is, Core Value, Requirements)
- Read `.planning/config.json` for settings (model_profile, workflow toggles)
  </step>

<step name="recent">
**Gather recent work context:**

- Find the 2-3 most recent SUMMARY.md files
- Extract from each: what was accomplished, key decisions, any issues logged
- This shows "what we've been working on"
  </step>

<step name="position">
**Parse current position:**

- From STATE.md: current phase, plan number, status
- Calculate: total plans, completed plans, remaining plans
- Note any blockers or concerns
- Check for CONTEXT.md: For phases without PLAN.md files, check if `{phase}-CONTEXT.md` exists in phase directory
- Count pending todos: `ls .planning/todos/pending/*.md 2>/dev/null | wc -l`
- Check for active debug sessions: `ls .planning/debug/*.md 2>/dev/null | grep -v resolved | wc -l`
  </step>

<step name="report">
**Present rich status report:**

```
# [Project Name]

**Progress:** [████████░░] 8/10 plans complete
**Profile:** [quality/balanced/budget]

## Recent Work
- [Phase X, Plan Y]: [what was accomplished - 1 line]
- [Phase X, Plan Z]: [what was accomplished - 1 line]

## Current Position
Phase [N] of [total]: [phase-name]
Plan [M] of [phase-total]: [status]
CONTEXT: [✓ if CONTEXT.md exists | - if not]

## Key Decisions Made
- [decision 1 from STATE.md]
- [decision 2]

## Blockers/Concerns
- [any blockers or concerns from STATE.md]

## Pending Todos
- [count] pending — /wxcode:check-todos to review

## Active Debug Sessions
- [count] active — /wxcode:debug to continue
(Only show this section if count > 0)

## What's Next
[Next phase/plan objective from ROADMAP]
```

</step>

<step name="route">
**Determine next action based on verified counts.**

**Step 1: Count plans, summaries, and issues in current phase**

List files in the current phase directory:

```bash
ls -1 .planning/phases/[current-phase-dir]/*-PLAN.md 2>/dev/null | wc -l
ls -1 .planning/phases/[current-phase-dir]/*-SUMMARY.md 2>/dev/null | wc -l
ls -1 .planning/phases/[current-phase-dir]/*-UAT.md 2>/dev/null | wc -l
```

State: "This phase has {X} plans, {Y} summaries."

**Step 1.5: Check for unaddressed UAT gaps**

Check for UAT.md files with status "diagnosed" (has gaps needing fixes).

```bash
# Check for diagnosed UAT with gaps
grep -l "status: diagnosed" .planning/phases/[current-phase-dir]/*-UAT.md 2>/dev/null
```

Track:
- `uat_with_gaps`: UAT.md files with status "diagnosed" (gaps need fixing)

**Step 2: Route based on counts**

| Condition | Meaning | Action |
|-----------|---------|--------|
| uat_with_gaps > 0 | UAT gaps need fix plans | Go to **Route E** |
| summaries < plans | Unexecuted plans exist | Go to **Route A** |
| summaries = plans AND plans > 0 | Phase complete | Go to Step 3 |
| plans = 0 | Phase not yet planned | Go to **Route B** |

---

**Route A: Unexecuted plan exists**

Find the first PLAN.md without matching SUMMARY.md.
Read its `<objective>` section.

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Phase {N} ready to execute","progress":{calculated},"phase":{N}} -->
<!-- WXCODE:NEXT_ACTION:{"command":"execute-phase","args":"{phase}","description":"Execute planned tasks","priority":"recommended"} -->
```

---

## ▶ Next Up

**{phase}-{plan}: [Plan Name]** — [objective summary from PLAN.md]

`/wxcode:execute-phase {phase}`

<sub>`/clear` first → fresh context window</sub>

---

---

**Route B: Phase needs planning**

Check if `{phase}-CONTEXT.md` exists in phase directory.

**If CONTEXT.md exists:**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Phase {N} ready to plan","progress":{calculated},"phase":{N}} -->
<!-- WXCODE:NEXT_ACTION:{"command":"plan-phase","args":"{phase}","description":"Create execution plan","priority":"recommended"} -->
```

---

## ▶ Next Up

**Phase {N}: {Name}** — {Goal from ROADMAP.md}
<sub>✓ Context gathered, ready to plan</sub>

`/wxcode:plan-phase {phase-number}`

<sub>`/clear` first → fresh context window</sub>

---

**If CONTEXT.md does NOT exist:**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Phase {N} needs context","progress":{calculated},"phase":{N}} -->
<!-- WXCODE:NEXT_ACTION:{"command":"discuss-phase","args":"{phase}","description":"Gather context before planning","priority":"recommended"} -->
```

---

## ▶ Next Up

**Phase {N}: {Name}** — {Goal from ROADMAP.md}

`/wxcode:discuss-phase {phase}` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/wxcode:plan-phase {phase}` — skip discussion, plan directly
- `/wxcode:list-phase-assumptions {phase}` — see Claude's assumptions

---

---

**Route E: UAT gaps need fix plans**

UAT.md exists with gaps (diagnosed issues). User needs to plan fixes.

```
<!-- WXCODE:STATUS:{"status":"failed","message":"Phase {N} has UAT gaps","progress":{calculated},"phase":{N}} -->
<!-- WXCODE:NEXT_ACTION:{"command":"plan-phase","args":"{phase} --gaps","description":"Plan fixes for UAT gaps","priority":"required"} -->
```

---

## ⚠ UAT Gaps Found

**{phase}-UAT.md** has {N} gaps requiring fixes.

`/wxcode:plan-phase {phase} --gaps`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/wxcode:execute-phase {phase}` — execute phase plans
- `/wxcode:verify-work {phase}` — run more UAT testing

---

---

**Step 3: Check milestone status (only when current phase complete)**

Read ROADMAP.md and identify:
1. Current phase number
2. All phase numbers in the current milestone section
3. The highest phase number

**Verify ALL phases are complete before suggesting milestone completion:**

```bash
# For EACH phase directory in .planning/phases/
# Count PLAN.md files and SUMMARY.md files
# A phase is complete when summaries >= plans AND plans > 0
for dir in .planning/phases/*/; do
  plans=$(ls -1 "$dir"*-PLAN.md 2>/dev/null | wc -l)
  summaries=$(ls -1 "$dir"*-SUMMARY.md 2>/dev/null | wc -l)
  echo "$dir: plans=$plans summaries=$summaries"
done
```

State: "Current phase is {X}. Milestone has {N} phases (highest: {Y}). Phases complete: {completed}/{total}."

**Route based on milestone status:**

| Condition | Meaning | Action |
|-----------|---------|--------|
| current phase < highest phase | More phases remain | Go to **Route C** |
| current phase = highest phase BUT incomplete phases exist | Last phase reached but not all done | Go to **Route C** (next incomplete phase) |
| ALL phases complete (summaries >= plans for each) | Milestone truly complete | Go to **Route D** |

---

**Route C: Phase complete, more phases remain (or incomplete phases exist)**

Find the **next incomplete phase** — either the next sequential phase, or if at the last phase, find the first incomplete phase.

Read ROADMAP.md to get that phase's name and goal.

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Phase {Z} complete","progress":{calculated},"phase":{Z}} -->
<!-- WXCODE:NEXT_ACTION:{"command":"discuss-phase","args":"{Z+1}","description":"Gather context for next phase","priority":"recommended"} -->
```

---

## ✓ Phase {Z} Complete

## ▶ Next Up

**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

`/wxcode:discuss-phase {Z+1}` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/wxcode:plan-phase {Z+1}` — skip discussion, plan directly
- `/wxcode:verify-work {Z}` — user acceptance test before continuing

---

---

**Route D: Milestone complete**

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Milestone complete","progress":100} -->
<!-- WXCODE:NEXT_ACTION:{"command":"complete-milestone","args":"","description":"Archive milestone","priority":"recommended"} -->
```

---

## 🎉 Milestone Complete

All {N} phases finished!

## ▶ Next Up

**Complete Milestone** — archive and prepare for next

`/wxcode:complete-milestone`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/wxcode:verify-work` — user acceptance test before completing milestone

---

---

**Route F: Between milestones (ROADMAP.md missing, PROJECT.md exists)**

A milestone was completed and archived. Ready to start the next milestone cycle.

Read MILESTONES.md to find the last completed milestone version.

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Between milestones","progress":100} -->
<!-- WXCODE:NEXT_ACTION:{"command":"new-milestone","args":"","description":"Start next milestone cycle","priority":"recommended"} -->
```

---

## ✓ Milestone v{X.Y} Complete

Ready to plan the next milestone.

## ▶ Next Up

**Start Next Milestone** — questioning → research → requirements → roadmap

`/wxcode:new-milestone`

<sub>`/clear` first → fresh context window</sub>

---

</step>

<step name="edge_cases">
**Handle edge cases:**

- Phase complete but next phase not planned → offer `/wxcode:plan-phase [next]`
- All work complete → offer milestone completion
- Blockers present → highlight before offering to continue
- Handoff file exists → mention it, offer `/wxcode:resume-work`
  </step>

</process>

<success_criteria>

- [ ] Rich context provided (recent work, decisions, issues)
- [ ] Current position clear with visual progress
- [ ] What's next clearly explained
- [ ] Smart routing: /wxcode:execute-phase if plans exist, /wxcode:plan-phase if not
- [ ] User confirms before any action
- [ ] Seamless handoff to appropriate gsd command
      </success_criteria>
