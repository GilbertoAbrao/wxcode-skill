---
name: wxcode:audit-milestone
description: Audit milestone completion against original intent before archiving
argument-hint: "[version]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
  - Write
  - mcp__wxcode-kb__get_business_rules
---

<objective>
Verify milestone achieved its definition of done. Check requirements coverage, cross-phase integration, and end-to-end flows.

**This command IS the orchestrator.** Reads existing VERIFICATION.md files (phases already verified during execute-phase), aggregates tech debt and deferred gaps, then spawns integration checker for cross-phase wiring.
</objective>

<execution_context>
<!-- Spawns wxcode-integration-checker agent which has all audit expertise baked in -->
</execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"audit-milestone","args":"$ARGUMENTS","title":"WXCODE ▶ AUDITING MILESTONE"} -->
## WXCODE ▶ AUDITING MILESTONE
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"complete-milestone","args":"","description":"Archive the milestone","priority":"recommended"} -->
```
</structured_output>



<context>
Version: $ARGUMENTS (optional — defaults to current milestone)

**Original Intent:**
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md

**Planned Work:**
@.planning/ROADMAP.md
@.planning/config.json (if exists)

**Completed Work:**
Glob: .planning/phases/*/*-SUMMARY.md
Glob: .planning/phases/*/*-VERIFICATION.md
</context>

<process>

## 0. Resolve Model Profile

Read model profile for agent spawning:

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent | quality | balanced | budget |
|-------|---------|----------|--------|
| wxcode-integration-checker | sonnet | sonnet | haiku |

Store resolved model for use in Task call below.

## 1. Determine Milestone Scope

```bash
# Get phases in milestone
ls -d .planning/phases/*/ | sort -V
```

- Parse version from arguments or detect current from ROADMAP.md
- Identify all phase directories in scope
- Extract milestone definition of done from ROADMAP.md
- Extract requirements mapped to this milestone from REQUIREMENTS.md

## 2. Read All Phase Verifications

For each phase directory, read the VERIFICATION.md:

```bash
cat .planning/phases/01-*/*-VERIFICATION.md
cat .planning/phases/02-*/*-VERIFICATION.md
# etc.
```

From each VERIFICATION.md, extract:
- **Status:** passed | gaps_found
- **Critical gaps:** (if any — these are blockers)
- **Non-critical gaps:** tech debt, deferred items, warnings
- **Anti-patterns found:** TODOs, stubs, placeholders
- **Requirements coverage:** which requirements satisfied/blocked

If a phase is missing VERIFICATION.md, flag it as "unverified phase" — this is a blocker.

## 2.5 Verify Business Rule Coverage (Conversion Projects Only)

If `.planning/CONVERSION.md` exists:

**Determine element list:** Read MILESTONE.json from `.planning/milestones/*/MILESTONE.json` (find the active milestone folder). Use the `"elements"` array. Fallback to `["element"]` if `"elements"` is missing (backward compat with older milestones).

For each element in ELEMENT_LIST:
1. Call `mcp__wxcode-kb__get_business_rules(element_name=ELEM)`
2. Check if each rule appears in SUMMARY.md conversion notes
3. Flag rules with no coverage as "potentially lost"

Track:
- preserved_rules: N (mentioned in SUMMARYs)
- missing_rules: [list] (not found in SUMMARYs)
- coverage_pct: N%

## 2.7 Count Dependency Stubs (Conversion Projects Only)

If `.planning/CONVERSION.md` exists:

**Count stubs in the codebase:**

```bash
grep -r "WXCODE:STUB" --include="*.py" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx" -l . 2>/dev/null
```

**For each stub file found:**
1. Extract the legacy procedure name from the TODO comment
2. Extract the depth level (D2, D3, etc.)
3. Extract the legacy element name

**Track:**
- `stub_count`: Total number of stub files
- `stub_list`: [{procedure, depth, legacy_element, file_path}]

**Stubs are NOT failures.** They are intentional deferrals from the dependency depth selection in Phase 1.86 of `new-milestone`. Report them as "deferred dependencies" in the audit, not as gaps or tech debt.

## 3. Spawn Integration Checker

With phase context collected:

```
Task(
  prompt="Check cross-phase integration and E2E flows.

Phases: {phase_dirs}
Phase exports: {from SUMMARYs}
API routes: {routes created}

Verify cross-phase wiring and E2E user flows.",
  subagent_type="wxcode-integration-checker",
  model="{integration_checker_model}"
)
```

## 4. Collect Results

Combine:
- Phase-level gaps and tech debt (from step 2)
- Integration checker's report (wiring gaps, broken flows)

## 5. Check Requirements Coverage

For each requirement in REQUIREMENTS.md mapped to this milestone:
- Find owning phase
- Check phase verification status
- Determine: satisfied | partial | unsatisfied

## 6. Aggregate into v{version}-MILESTONE-AUDIT.md

Create `.planning/v{version}-v{version}-MILESTONE-AUDIT.md` with:

```yaml
---
milestone: {version}
audited: {timestamp}
status: passed | gaps_found | tech_debt
scores:
  requirements: N/M
  phases: N/M
  integration: N/M
  flows: N/M
gaps:  # Critical blockers
  requirements: [...]
  integration: [...]
  flows: [...]
tech_debt:  # Non-critical, deferred
  - phase: 01-auth
    items:
      - "TODO: add rate limiting"
      - "Warning: no password strength validation"
  - phase: 03-dashboard
    items:
      - "Deferred: mobile responsive layout"
business_rules:  # Conversion projects only
  total: N
  preserved: N
  missing: [...]
  coverage: N%
dependency_stubs:  # Conversion projects only
  count: N
  stubs:
    - procedure: "REST_ConfigurarAutenticacao"
      depth: "D2"
      legacy_element: "REST_Utils"
      file: "services/rest_utils.py"
  note: "Intentional deferrals from dependency depth selection"
---
```

Plus full markdown report with tables for requirements, phases, integration, tech debt.

**Status values:**
- `passed` — all requirements met, no critical gaps, minimal tech debt
- `gaps_found` — critical blockers exist
- `tech_debt` — no blockers but accumulated deferred items need review

## 7. Present Results

Route by status (see `<offer_next>`).

</process>

<offer_next>
Output this markdown directly (not as a code block). Route based on status:

---

**If passed:**

## ✓ Milestone {version} — Audit Passed

**Score:** {N}/{M} requirements satisfied
**Report:** .planning/v{version}-MILESTONE-AUDIT.md

All requirements covered. Cross-phase integration verified. E2E flows complete.

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Complete milestone** — archive and tag

/wxcode:complete-milestone {version}

*Run clear first for fresh context window*

───────────────────────────────────────────────────────────────

---

**If gaps_found:**

## ⚠ Milestone {version} — Gaps Found

**Score:** {N}/{M} requirements satisfied
**Report:** .planning/v{version}-MILESTONE-AUDIT.md

### Unsatisfied Requirements

{For each unsatisfied requirement:}
- **{REQ-ID}: {description}** (Phase {X})
  - {reason}

### Cross-Phase Issues

{For each integration gap:}
- **{from} → {to}:** {issue}

### Broken Flows

{For each flow gap:}
- **{flow name}:** breaks at {step}

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Plan gap closure** — create phases to complete milestone

/wxcode:plan-milestone-gaps

*Run clear first for fresh context window*

───────────────────────────────────────────────────────────────

**Also available:**
- cat .planning/v{version}-MILESTONE-AUDIT.md — see full report
- /wxcode:complete-milestone {version} — proceed anyway (accept tech debt)

───────────────────────────────────────────────────────────────

---

**If tech_debt (no blockers but accumulated debt):**

## ⚡ Milestone {version} — Tech Debt Review

**Score:** {N}/{M} requirements satisfied
**Report:** .planning/v{version}-MILESTONE-AUDIT.md

All requirements met. No critical blockers. Accumulated tech debt needs review.

### Tech Debt by Phase

{For each phase with debt:}
**Phase {X}: {name}**
- {item 1}
- {item 2}

### Total: {N} items across {M} phases

───────────────────────────────────────────────────────────────

## ▶ Options

**A. Complete milestone** — accept debt, track in backlog

/wxcode:complete-milestone {version}

**B. Plan cleanup phase** — address debt before completing

/wxcode:plan-milestone-gaps

*Run clear first for fresh context window*

───────────────────────────────────────────────────────────────
</offer_next>

<success_criteria>
- [ ] Milestone scope identified
- [ ] All phase VERIFICATION.md files read
- [ ] Tech debt and deferred gaps aggregated
- [ ] Integration checker spawned for cross-phase wiring
- [ ] v{version}-MILESTONE-AUDIT.md created
- [ ] (Conversion projects) Business rule coverage checked
- [ ] (Conversion projects) Dependency stubs counted (WXCODE:STUB grep) and reported as deferred (not failure)
- [ ] Results presented with actionable next steps
</success_criteria>
