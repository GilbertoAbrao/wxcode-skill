---
name: wxcode:new-milestone
description: Start a new milestone cycle — update PROJECT.md and route to requirements
argument-hint: "--element=PAGE_Login --output-project=xxx (for conversion projects)"
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
  - mcp__wxcode-kb__*
---

<objective>
Start a new milestone through unified flow: questioning → research (optional) → requirements → roadmap.

This is the brownfield equivalent of new-project. The project exists, PROJECT.md has history. This command gathers "what's next", updates PROJECT.md, then continues through the full requirements → roadmap cycle.

**Creates/Updates:**
- `.planning/PROJECT.md` — updated with new milestone goals
- `.planning/research/` — domain research (optional, focuses on NEW features)
- `.planning/REQUIREMENTS.md` — scoped requirements for this milestone
- `.planning/ROADMAP.md` — phase structure (continues numbering)
- `.planning/STATE.md` — reset for new milestone

**After this command:** Run `/wxcode:plan-phase [N]` to start execution.
</objective>

<execution_context>
@~/.claude/wxcode-skill/references/questioning.md
@~/.claude/wxcode-skill/references/ui-brand.md
@~/.claude/wxcode-skill/templates/project.md
@~/.claude/wxcode-skill/templates/requirements.md
</execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"new-milestone","args":"$ARGUMENTS","title":"WXCODE ▶ NEW MILESTONE"} -->
## WXCODE ▶ NEW MILESTONE
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"plan-phase","args":"1","description":"Plan the first phase","priority":"recommended"} -->
```
</structured_output>



<context>
**Arguments parsing:**

For **conversion projects** (UI-triggered):
- `--element=PAGE_Login`: Element name to convert (required)
- `--output-project=xxx`: MongoDB OutputProject ID (required)

Example: `/wxcode:new-milestone --element=PAGE_Login --output-project=507f1f77bcf86cd799439011`

For **greenfield projects** (CLI):
- Milestone name as positional argument (optional - will prompt if not provided)

Example: `/wxcode:new-milestone v1.1 Notifications`

**Version is determined automatically by the agent** — never passed by UI.

**Load project context:**
@.planning/PROJECT.md
@.planning/STATE.md
@.planning/MILESTONES.md
@.planning/config.json

**Load milestone context (if exists, from /wxcode:discuss-milestone):**
@.planning/MILESTONE-CONTEXT.md
</context>

<process>

## Phase 1: Load Context

**Step 0: Ensure WXCODE commands are available in this project:**

```bash
WXCODE_STORAGE="$HOME/.claude/wxcode-skill/commands/wxcode"
WXCODE_LOCAL=".claude/commands/wxcode"

if [ -L "$WXCODE_LOCAL" ]; then
    echo "WXCODE commands linked ✓"
elif [ -d "$WXCODE_LOCAL" ]; then
    echo "WXCODE commands (local) ✓"
elif [ -d "$WXCODE_STORAGE" ]; then
    mkdir -p .claude/commands
    ln -s "$WXCODE_STORAGE" "$WXCODE_LOCAL"
    echo "WXCODE commands linked ✓"
else
    echo "⚠ WXCODE commands storage not found. Run: npx github:GilbertoAbrao/get-shit-done#main --claude --global"
fi
```

**Step 1: Load project files:**

- Read PROJECT.md (existing project, Validated requirements, decisions)
- Read MILESTONES.md (what shipped previously)
- Read STATE.md (pending todos, blockers)
- Check for MILESTONE-CONTEXT.md (from /wxcode:discuss-milestone)
- Check for CONVERSION.md (conversion project indicator)

## Phase 1.5: MCP Availability Check (Conversion Projects Only)

**If `.planning/CONVERSION.md` exists:**

This is a **Conversion Project** — MCP wxcode-kb is required.

**Attempt 1:** Call `mcp__wxcode-kb__health_check`

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 2**

**Attempt 2:** Call `mcp__wxcode-kb__health_check`

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 3**

**Attempt 3:** Call `mcp__wxcode-kb__health_check`

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails after 3 attempts:**

```
╔══════════════════════════════════════════════════════════════╗
║  ERROR: MCP wxcode-kb not available                          ║
╚══════════════════════════════════════════════════════════════╝

This is a conversion project (CONVERSION.md exists).
Conversion projects require the wxcode-kb MCP server.
Tried 3 times with 10s delay between attempts.

**To fix:**
1. Ensure wxcode-kb MCP server is running
2. Verify MCP is configured in Claude Code settings
3. Restart Claude Code if recently configured

**Cannot proceed without MCP.**
```

**STOP only after all 3 attempts fail.**

**If MCP available or not a conversion project:** Continue below.

## Phase 1.6: Parse Arguments and Create Milestone (Conversion Projects)

**Skip this phase if NOT a conversion project** (no CONVERSION.md).

### Step 1: Validate required arguments

Parse from $ARGUMENTS:
```
--element=PAGE_Login     → ELEMENT_NAME
--output-project=xxx     → OUTPUT_PROJECT_ID
```

**If missing `--element` or `--output-project`:**
```
╔══════════════════════════════════════════════════════════════╗
║  ERROR: Missing required arguments                            ║
╚══════════════════════════════════════════════════════════════╝

Conversion projects require:
  --element=<element_name>
  --output-project=<output_project_id>

Example:
  /wxcode:new-milestone --element=PAGE_Login --output-project=507f1f77...
```
**STOP.**

### Step 2: Determine version automatically

Scan existing milestone dashboards to find highest version:
```bash
ls -1 .planning/dashboard_v*.json 2>/dev/null | sort -V | tail -1
```

**Version logic:**
- No existing milestones → `v1.0`
- Highest is `v1.0` → `v1.1`
- Highest is `v1.5` → `v1.6`
- Highest is `v1.9` → `v2.0`

Store:
```
WXCODE_VERSION="v1.0"  # determined automatically
MILESTONE_FOLDER_NAME="${WXCODE_VERSION}-${ELEMENT_NAME}"
# Example: "v1.0-PAGE_Login"
```

### Step 3: Create milestone folder

```bash
mkdir -p .planning/milestones/${MILESTONE_FOLDER_NAME}
```

Display:
```
✓ Milestone folder: .planning/milestones/${MILESTONE_FOLDER_NAME}
```

### Step 4: Create Milestone in MongoDB (CRITICAL - DO NOT SKIP)

**╔══════════════════════════════════════════════════════════════╗**
**║  MANDATORY: Call MCP tool IMMEDIATELY after creating folder  ║**
**╚══════════════════════════════════════════════════════════════╝**

**This is a BLOCKING requirement. DO NOT proceed to Phase 2 without completing this step.**

Call the MCP tool NOW:

```
mcp__wxcode-kb__create_milestone(
    output_project_id=OUTPUT_PROJECT_ID,
    element_name=ELEMENT_NAME,
    wxcode_version=WXCODE_VERSION,
    milestone_folder_name=MILESTONE_FOLDER_NAME,
    confirm=true
)
```

**After MCP call succeeds**, store the returned ID:
```
MONGODB_MILESTONE_ID=[returned milestone_id]
```

Display confirmation:
```
✓ Milestone created in MongoDB: ${MONGODB_MILESTONE_ID}
✓ Version: ${WXCODE_VERSION}
✓ Element: ${ELEMENT_NAME}
```

**If MCP call fails:**
- Remove the created folder: `rm -rf .planning/milestones/${MILESTONE_FOLDER_NAME}`
- Display error and **STOP**

**CHECKPOINT: Verify MCP was called before continuing.**

### Step 5: Store for later phases

These values are used in later phases:
- `ELEMENT_NAME` — for context gathering
- `OUTPUT_PROJECT_ID` — for MCP calls
- `WXCODE_VERSION` — for dashboard and STATE.md
- `MILESTONE_FOLDER_NAME` — for dashboard filename
- `MONGODB_MILESTONE_ID` — for dashboard content

---

## Phase 1.7: Verify Milestone Creation (Conversion Projects Only)

**GATE CHECK before Phase 2:**

For conversion projects, verify:
1. ✓ Milestone folder exists: `.planning/milestones/${MILESTONE_FOLDER_NAME}`
2. ✓ `MONGODB_MILESTONE_ID` is set (from MCP call in Step 4)

**If `MONGODB_MILESTONE_ID` is NOT set:**
```
╔══════════════════════════════════════════════════════════════╗
║  ERROR: MCP create_milestone was not called                   ║
╚══════════════════════════════════════════════════════════════╝

Go back to Phase 1.6 Step 4 and call:
  mcp__wxcode-kb__create_milestone(...)

Cannot continue without MongoDB milestone record.
```
**STOP and go back to Step 4.**

---

## Phase 1.8: Ensure Database Models (Conversion Projects Only)

**Purpose:** The new application accesses the EXISTING legacy database. Before converting an element, ensure all required table models exist.

**Step 1: Get element's table dependencies**

```
mcp__wxcode-kb__get_dependencies(element_name, direction="uses")
```

Filter for TABLE dependencies:
```python
table_deps = [dep for dep in dependencies if dep.type == "TABLE"]
```

**Step 2: Check which models already exist**

Based on stack conventions:
- **Python/SQLAlchemy:** Check `app/models/*.py` for `__tablename__ = "TABLE_NAME"`
- **Prisma:** Check `prisma/schema.prisma` for `@@map("TABLE_NAME")`
- **TypeORM:** Check `src/models/*.ts` for `@Entity({ name: "TABLE_NAME" })`

```bash
# Example for SQLAlchemy
grep -r "__tablename__" app/models/ 2>/dev/null | grep -oE '"[A-Z_]+"' | tr -d '"' | sort -u
```

**Step 3: Generate missing models**

If tables are missing models:

```
◆ Element ${ELEMENT_NAME} needs tables: [TABLE_A, TABLE_B, ...]
  Missing models: [TABLE_A]
  Generating...
```

Spawn schema generator:

```
Task(wxcode-schema-generator):
  prompt: |
    Generate database models for specific tables.

    Output Project ID: ${OUTPUT_PROJECT_ID}
    Tables needed: [TABLE_A, TABLE_B, ...]

    Use capability: generate_specific_models

    Requirements:
    - Preserve EXACT legacy table/column names
    - Only generate models that don't exist yet
    - Update index/barrel file with new exports

    Validate generated models against MCP schema.
  subagent_type: wxcode-schema-generator
```

**Step 4: Confirm models ready**

```
✓ Database models ready for ${ELEMENT_NAME}
  - Existing: [N] tables
  - Generated: [M] tables
```

**If no table dependencies:** Skip to Phase 2.

---

## Phase 2: Gather Milestone Goals

**If MILESTONE-CONTEXT.md exists:**
- Use features and scope from discuss-milestone
- Present summary for confirmation

**If no context file:**
- Present what shipped in last milestone
- Ask: "What do you want to build next?"
- Use AskUserQuestion to explore features
- Probe for priorities, constraints, scope

## Phase 3: Determine Milestone Version

- Parse last version from MILESTONES.md
- Suggest next version (v1.0 → v1.1, or v2.0 for major)
- Confirm with user

## Phase 4: Update PROJECT.md

Add/update these sections:

```markdown
## Current Milestone: v[X.Y] [Name]

**Goal:** [One sentence describing milestone focus]

**Target features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]
```

Update Active requirements section with new goals.

Update "Last updated" footer.

## Phase 5: Update STATE.md

```markdown
## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: [today] — Milestone v[X.Y] started
```

Keep Accumulated Context section (decisions, blockers) from previous milestone.

## Phase 6: Cleanup and Commit

Delete MILESTONE-CONTEXT.md if exists (consumed).

Check planning config:
```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

If `COMMIT_PLANNING_DOCS=false`: Skip git operations

If `COMMIT_PLANNING_DOCS=true` (default):
```bash
git add .planning/PROJECT.md .planning/STATE.md
git commit -m "docs: start milestone v[X.Y] [Name]"
```

## Phase 6.5: Resolve Model Profile

Read model profile for agent spawning:

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent | quality | balanced | budget |
|-------|---------|----------|--------|
| wxcode-project-researcher | opus | sonnet | haiku |
| wxcode-research-synthesizer | sonnet | sonnet | haiku |
| wxcode-roadmapper | opus | sonnet | sonnet |

Store resolved models for use in Task calls below.

## Phase 7: Research Decision

Use AskUserQuestion:
- header: "Research"
- question: "Research the domain ecosystem for new features before defining requirements?"
- options:
  - "Research first (Recommended)" — Discover patterns, expected features, architecture for NEW capabilities
  - "Skip research" — I know what I need, go straight to requirements

**If "Research first":**

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► RESEARCHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Researching [new features] ecosystem...
```

Create research directory:
```bash
mkdir -p .planning/research
```

Display spawning indicator:
```
◆ Spawning 4 researchers in parallel...
  → Stack research (for new features)
  → Features research
  → Architecture research (integration)
  → Pitfalls research
```

Spawn 4 parallel wxcode-project-researcher agents with milestone-aware context:

```
Task(prompt="
<research_type>
Project Research — Stack dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Existing validated capabilities (DO NOT re-research):
[List from PROJECT.md Validated requirements]

Focus ONLY on what's needed for the NEW features.
</milestone_context>

<question>
What stack additions/changes are needed for [new features]?
</question>

<project_context>
[PROJECT.md summary - current state, new milestone goals]
</project_context>

<downstream_consumer>
Your STACK.md feeds into roadmap creation. Be prescriptive:
- Specific libraries with versions for NEW capabilities
- Integration points with existing stack
- What NOT to add and why
</downstream_consumer>

<quality_gate>
- [ ] Versions are current (verify with Context7/official docs, not training data)
- [ ] Rationale explains WHY, not just WHAT
- [ ] Integration with existing stack considered
</quality_gate>

<output>
Write to: .planning/research/STACK.md
Use template: ~/.claude/wxcode-skill/templates/research-project/STACK.md
</output>
", subagent_type="wxcode-project-researcher", model="{researcher_model}", description="Stack research")

Task(prompt="
<research_type>
Project Research — Features dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Existing features (already built):
[List from PROJECT.md Validated requirements]

Focus on how [new features] typically work, expected behavior.
</milestone_context>

<question>
How do [target features] typically work? What's expected behavior?
</question>

<project_context>
[PROJECT.md summary - new milestone goals]
</project_context>

<downstream_consumer>
Your FEATURES.md feeds into requirements definition. Categorize clearly:
- Table stakes (must have for these features)
- Differentiators (competitive advantage)
- Anti-features (things to deliberately NOT build)
</downstream_consumer>

<quality_gate>
- [ ] Categories are clear (table stakes vs differentiators vs anti-features)
- [ ] Complexity noted for each feature
- [ ] Dependencies on existing features identified
</quality_gate>

<output>
Write to: .planning/research/FEATURES.md
Use template: ~/.claude/wxcode-skill/templates/research-project/FEATURES.md
</output>
", subagent_type="wxcode-project-researcher", model="{researcher_model}", description="Features research")

Task(prompt="
<research_type>
Project Research — Architecture dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Existing architecture:
[Summary from PROJECT.md or codebase map]

Focus on how [new features] integrate with existing architecture.
</milestone_context>

<question>
How do [target features] integrate with existing [domain] architecture?
</question>

<project_context>
[PROJECT.md summary - current architecture, new features]
</project_context>

<downstream_consumer>
Your ARCHITECTURE.md informs phase structure in roadmap. Include:
- Integration points with existing components
- New components needed
- Data flow changes
- Suggested build order
</downstream_consumer>

<quality_gate>
- [ ] Integration points clearly identified
- [ ] New vs modified components explicit
- [ ] Build order considers existing dependencies
</quality_gate>

<output>
Write to: .planning/research/ARCHITECTURE.md
Use template: ~/.claude/wxcode-skill/templates/research-project/ARCHITECTURE.md
</output>
", subagent_type="wxcode-project-researcher", model="{researcher_model}", description="Architecture research")

Task(prompt="
<research_type>
Project Research — Pitfalls dimension for [new features].
</research_type>

<milestone_context>
SUBSEQUENT MILESTONE — Adding [target features] to existing app.

Focus on common mistakes when ADDING these features to an existing system.
</milestone_context>

<question>
What are common mistakes when adding [target features] to [domain]?
</question>

<project_context>
[PROJECT.md summary - current state, new features]
</project_context>

<downstream_consumer>
Your PITFALLS.md prevents mistakes in roadmap/planning. For each pitfall:
- Warning signs (how to detect early)
- Prevention strategy (how to avoid)
- Which phase should address it
</downstream_consumer>

<quality_gate>
- [ ] Pitfalls are specific to adding these features (not generic)
- [ ] Integration pitfalls with existing system covered
- [ ] Prevention strategies are actionable
</quality_gate>

<output>
Write to: .planning/research/PITFALLS.md
Use template: ~/.claude/wxcode-skill/templates/research-project/PITFALLS.md
</output>
", subagent_type="wxcode-project-researcher", model="{researcher_model}", description="Pitfalls research")
```

After all 4 agents complete, spawn synthesizer to create SUMMARY.md:

```
Task(prompt="
<task>
Synthesize research outputs into SUMMARY.md.
</task>

<research_files>
Read these files:
- .planning/research/STACK.md
- .planning/research/FEATURES.md
- .planning/research/ARCHITECTURE.md
- .planning/research/PITFALLS.md
</research_files>

<output>
Write to: .planning/research/SUMMARY.md
Use template: ~/.claude/wxcode-skill/templates/research-project/SUMMARY.md
Commit after writing.
</output>
", subagent_type="wxcode-research-synthesizer", model="{synthesizer_model}", description="Synthesize research")
```

Display research complete banner and key findings:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► RESEARCH COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Key Findings

**Stack additions:** [from SUMMARY.md]
**New feature table stakes:** [from SUMMARY.md]
**Watch Out For:** [from SUMMARY.md]

Files: `.planning/research/`
```

**If "Skip research":** Continue to Phase 8.

## Phase 8: Define Requirements

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DEFINING REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Load context:**

Read PROJECT.md and extract:
- Core value (the ONE thing that must work)
- Current milestone goals
- Validated requirements (what already exists)

**If research exists:** Read research/FEATURES.md and extract feature categories.

**Present features by category:**

```
Here are the features for [new capabilities]:

## [Category 1]
**Table stakes:**
- Feature A
- Feature B

**Differentiators:**
- Feature C
- Feature D

**Research notes:** [any relevant notes]

---

## [Next Category]
...
```

**If no research:** Gather requirements through conversation instead.

Ask: "What are the main things users need to be able to do with [new features]?"

For each capability mentioned:
- Ask clarifying questions to make it specific
- Probe for related capabilities
- Group into categories

**Scope each category:**

For each category, use AskUserQuestion:

- header: "[Category name]"
- question: "Which [category] features are in this milestone?"
- multiSelect: true
- options:
  - "[Feature 1]" — [brief description]
  - "[Feature 2]" — [brief description]
  - "[Feature 3]" — [brief description]
  - "None for this milestone" — Defer entire category

Track responses:
- Selected features → this milestone's requirements
- Unselected table stakes → future milestone
- Unselected differentiators → out of scope

**Identify gaps:**

Use AskUserQuestion:
- header: "Additions"
- question: "Any requirements research missed? (Features specific to your vision)"
- options:
  - "No, research covered it" — Proceed
  - "Yes, let me add some" — Capture additions

**Generate REQUIREMENTS.md:**

Create `.planning/REQUIREMENTS.md` with:
- v1 Requirements for THIS milestone grouped by category (checkboxes, REQ-IDs)
- Future Requirements (deferred to later milestones)
- Out of Scope (explicit exclusions with reasoning)
- Traceability section (empty, filled by roadmap)

**REQ-ID format:** `[CATEGORY]-[NUMBER]` (AUTH-01, NOTIF-02)

Continue numbering from existing requirements if applicable.

**Requirement quality criteria:**

Good requirements are:
- **Specific and testable:** "User can reset password via email link" (not "Handle password reset")
- **User-centric:** "User can X" (not "System does Y")
- **Atomic:** One capability per requirement (not "User can login and manage profile")
- **Independent:** Minimal dependencies on other requirements

**Present full requirements list:**

Show every requirement (not counts) for user confirmation:

```
## Milestone v[X.Y] Requirements

### [Category 1]
- [ ] **CAT1-01**: User can do X
- [ ] **CAT1-02**: User can do Y

### [Category 2]
- [ ] **CAT2-01**: User can do Z

[... full list ...]

---

Does this capture what you're building? (yes / adjust)
```

If "adjust": Return to scoping.

**Commit requirements:**

Check planning config (same pattern as Phase 6).

If committing:
```bash
git add .planning/REQUIREMENTS.md
git commit -m "$(cat <<'EOF'
docs: define milestone v[X.Y] requirements

[X] requirements across [N] categories
EOF
)"
```

## Phase 9: Create Roadmap

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► CREATING ROADMAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning roadmapper...
```

**Determine starting phase number:**

Read MILESTONES.md to find the last phase number from previous milestone.
New phases continue from there (e.g., if v1.0 ended at phase 5, v1.1 starts at phase 6).

Spawn wxcode-roadmapper agent with context:

```
Task(prompt="
<planning_context>

**Project:**
@.planning/PROJECT.md

**Requirements:**
@.planning/REQUIREMENTS.md

**Research (if exists):**
@.planning/research/SUMMARY.md

**Config:**
@.planning/config.json

**Previous milestone (for phase numbering):**
@.planning/MILESTONES.md

</planning_context>

<instructions>
Create roadmap for milestone v[X.Y]:
1. Start phase numbering from [N] (continues from previous milestone)
2. Derive phases from THIS MILESTONE's requirements (don't include validated/existing)
3. Map every requirement to exactly one phase
4. Derive 2-5 success criteria per phase (observable user behaviors)
5. Validate 100% coverage of new requirements
6. Write files immediately (ROADMAP.md, STATE.md, update REQUIREMENTS.md traceability)
7. Return ROADMAP CREATED with summary

Write files first, then return. This ensures artifacts persist even if context is lost.
</instructions>
", subagent_type="wxcode-roadmapper", model="{roadmapper_model}", description="Create roadmap")
```

**Handle roadmapper return:**

**If `## ROADMAP BLOCKED`:**
- Present blocker information
- Work with user to resolve
- Re-spawn when resolved

**If `## ROADMAP CREATED`:**

Read the created ROADMAP.md and present it nicely inline:

```
---

## Proposed Roadmap

**[N] phases** | **[X] requirements mapped** | All milestone requirements covered ✓

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| [N] | [Name] | [Goal] | [REQ-IDs] | [count] |
| [N+1] | [Name] | [Goal] | [REQ-IDs] | [count] |
...

### Phase Details

**Phase [N]: [Name]**
Goal: [goal]
Requirements: [REQ-IDs]
Success criteria:
1. [criterion]
2. [criterion]

[... continue for all phases ...]

---
```

**CRITICAL: Ask for approval before committing:**

Use AskUserQuestion:
- header: "Roadmap"
- question: "Does this roadmap structure work for you?"
- options:
  - "Approve" — Commit and continue
  - "Adjust phases" — Tell me what to change
  - "Review full file" — Show raw ROADMAP.md

**If "Approve":** Continue to commit.

**If "Adjust phases":**
- Get user's adjustment notes
- Re-spawn roadmapper with revision context:
  ```
  Task(prompt="
  <revision>
  User feedback on roadmap:
  [user's notes]

  Current ROADMAP.md: @.planning/ROADMAP.md

  Update the roadmap based on feedback. Edit files in place.
  Return ROADMAP REVISED with changes made.
  </revision>
  ", subagent_type="wxcode-roadmapper", model="{roadmapper_model}", description="Revise roadmap")
  ```
- Present revised roadmap
- Loop until user approves

**If "Review full file":** Display raw `cat .planning/ROADMAP.md`, then re-ask.

**Commit roadmap (after approval):**

Check planning config (same pattern as Phase 6).

If committing:
```bash
git add .planning/ROADMAP.md .planning/STATE.md .planning/REQUIREMENTS.md
git commit -m "$(cat <<'EOF'
docs: create milestone v[X.Y] roadmap ([N] phases)

Phases:
[N]. [phase-name]: [requirements covered]
[N+1]. [phase-name]: [requirements covered]
...

All milestone requirements mapped to phases.
EOF
)"
```

## Phase 10: Regenerate Dashboards

**MANDATORY:** After milestone initialization, regenerate all dashboards.

Invoke `/wxcode:dashboard --all` to:
- Update project dashboard: `.planning/dashboard.json`
- Create milestone dashboard: `.planning/dashboard_<milestone>.json`
- Regenerate schema dashboard (conversion projects): `.planning/schema-dashboard.json`

This ensures the UI reflects the new milestone state.

## Phase 11: Done

Present completion with next steps:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► MILESTONE INITIALIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Milestone v[X.Y]: [Name]**

| Artifact       | Location                    |
|----------------|-----------------------------|
| Project        | `.planning/PROJECT.md`      |
| Research       | `.planning/research/`       |
| Requirements   | `.planning/REQUIREMENTS.md` |
| Roadmap        | `.planning/ROADMAP.md`      |

**[N] phases** | **[X] requirements** | Ready to build ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Phase [N]: [Phase Name]** — [Goal from ROADMAP.md]

`/wxcode:discuss-phase [N]` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/wxcode:plan-phase [N]` — skip discussion, plan directly

───────────────────────────────────────────────────────────────
```

</process>

<success_criteria>
- [ ] **(Conversion projects)** Arguments parsed: --element and --output-project
- [ ] **(Conversion projects)** Version determined automatically (v1.0, v1.1, etc.)
- [ ] **(Conversion projects)** Milestone folder created: `.planning/milestones/<folder>`
- [ ] **(Conversion projects - CRITICAL)** `mcp__wxcode-kb__create_milestone` called with confirm=true
- [ ] **(Conversion projects - CRITICAL)** MONGODB_MILESTONE_ID stored from MCP response
- [ ] PROJECT.md updated with Current Milestone section
- [ ] STATE.md reset for new milestone
- [ ] MILESTONE-CONTEXT.md consumed and deleted (if existed)
- [ ] Research completed (if selected) — 4 parallel agents spawned, milestone-aware
- [ ] Requirements gathered (from research or conversation)
- [ ] User scoped each category
- [ ] REQUIREMENTS.md created with REQ-IDs
- [ ] wxcode-roadmapper spawned with phase numbering context
- [ ] Roadmap files written immediately (not draft)
- [ ] User feedback incorporated (if any)
- [ ] ROADMAP.md created with phases continuing from previous milestone
- [ ] All commits made (if planning docs committed)
- [ ] User knows next step is `/wxcode:discuss-phase [N]`

**Atomic commits:** Each phase commits its artifacts immediately. If context is lost, artifacts persist.

- [ ] `/wxcode:dashboard --all` invoked (Phase 10)
- [ ] Project dashboard updated: `.planning/dashboard.json`
- [ ] Milestone dashboard created: `.planning/dashboard_<milestone>.json`
- [ ] (Conversion projects) Schema dashboard regenerated
</success_criteria>

