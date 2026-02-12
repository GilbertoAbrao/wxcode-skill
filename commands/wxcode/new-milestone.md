---
name: wxcode:new-milestone
description: Start a new milestone cycle — update PROJECT.md and route to requirements
argument-hint: "--element=PAGE_Login --output-project=xxx OR --elements=A,B,C --output-project=xxx"
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
- `.planning/ROADMAP.md` — phase structure (starts from phase 1, local to milestone)
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

<output_rules>
**NEVER use `<sub>` tags or backtick-wrapped slash commands in user-facing output.**
- WRONG: `<sub>/clear first → fresh context window</sub>`
- WRONG: `` `/wxcode:plan-phase 1` ``
- RIGHT: `*Run clear first for fresh context window*`
- RIGHT: `Run: wxcode:plan-phase 1`

Slash commands in output get parsed as command invocations. Always use plain text.
</output_rules>


<context>
**Arguments parsing:**

For **conversion projects** (UI-triggered):
- `--element=PAGE_Login`: Single element to convert (backward compat)
- `--elements=PAGE_Login,PAGE_Dashboard`: Comma-separated list of elements (multi-element milestone)
- `--output-project=xxx`: MongoDB OutputProject ID (required)
- `--name=auth-pages`: Custom milestone display name (optional, for multi-element)

**Rules:** Use `--element` OR `--elements`, not both. If neither provided, error.

Example (single): `/wxcode:new-milestone --element=PAGE_Login --output-project=507f1f77...`
Example (multi): `/wxcode:new-milestone --elements=PAGE_Login,PAGE_Dashboard --name=auth-pages --output-project=507f1f77...`

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
--element=PAGE_Login             → single element (backward compat)
--elements=PAGE_Login,PAGE_Dash  → comma-separated list
--output-project=xxx             → OUTPUT_PROJECT_ID
--name=auth-pages                → MILESTONE_DISPLAY_NAME (optional)
```

**Derive:**
```
If --elements: ELEMENT_LIST = split by comma; ELEMENT_NAME = first; IS_MULTI = true
If --element:  ELEMENT_LIST = [value]; ELEMENT_NAME = value; IS_MULTI = false
If both: ERROR — use --element OR --elements, not both
If neither: ERROR (see below)
```

**ELEMENT_COUNT** = length of ELEMENT_LIST.

**If missing element arg or `--output-project`:**
```
╔══════════════════════════════════════════════════════════════╗
║  ERROR: Missing required arguments                            ║
╚══════════════════════════════════════════════════════════════╝

Conversion projects require:
  --element=<element_name>  OR  --elements=<A,B,C>
  --output-project=<output_project_id>

Example (single):
  /wxcode:new-milestone --element=PAGE_Login --output-project=507f1f77...

Example (multi):
  /wxcode:new-milestone --elements=PAGE_Login,PAGE_Dashboard --output-project=507f1f77...
```
**STOP.**

### Step 2: Determine version automatically

Scan existing milestone dashboards AND placeholder files to find highest version:
```bash
# Check dashboards (completed or active milestones)
ls -1 .planning/dashboard_v*.json 2>/dev/null | sort -V | tail -1

# Also check MILESTONE.json placeholders (reserved versions from parallel worktrees)
ls -1 .planning/milestones/v*/MILESTONE.json 2>/dev/null
```

Parse the highest version from BOTH sources. Placeholder files reserve versions for in-progress milestones that may be running in parallel worktrees.

**Version logic:**
- No existing milestones or placeholders → `v1.0`
- Highest is `v1.0` → `v1.1`
- Highest is `v1.5` → `v1.6`
- Highest is `v1.9` → `v2.0`

Store:
```
WXCODE_VERSION="v1.0"  # determined automatically

# Folder naming:
If IS_MULTI and MILESTONE_DISPLAY_NAME:
  MILESTONE_FOLDER_NAME="${WXCODE_VERSION}-${MILESTONE_DISPLAY_NAME}"
  # Example: "v1.0-auth-pages"
Elif IS_MULTI:
  REMAINING = ELEMENT_COUNT - 1
  MILESTONE_FOLDER_NAME="${WXCODE_VERSION}-${ELEMENT_NAME}+${REMAINING}more"
  # Example: "v1.0-PAGE_Login+2more"
Else:
  MILESTONE_FOLDER_NAME="${WXCODE_VERSION}-${ELEMENT_NAME}"
  # Example: "v1.0-PAGE_Login"
```

### Step 3: Create milestone folder and placeholder

```bash
mkdir -p .planning/milestones/${MILESTONE_FOLDER_NAME}
```

Create MILESTONE.json placeholder to **reserve this version** (prevents collision with parallel milestones):

```bash
cat > .planning/milestones/${MILESTONE_FOLDER_NAME}/MILESTONE.json << EOF
{
  "version": "${WXCODE_VERSION}",
  "element": "${ELEMENT_NAME}",
  "elements": ${JSON_ARRAY_OF_ELEMENT_LIST},
  "display_name": ${MILESTONE_DISPLAY_NAME or null},
  "status": "in_progress",
  "branch": "milestone/${MILESTONE_FOLDER_NAME}",
  "worktree": "../$(basename $PWD)-${MILESTONE_FOLDER_NAME}",
  "created_at": "$(date +%Y-%m-%d)"
}
EOF
```

**Notes:**
- `"element"` is always the primary (first) element — backward compatible
- `"elements"` is always an array (even for single: `["PAGE_Login"]`)
- `"display_name"` is null if not provided via `--name`

Display:
```
✓ Milestone folder: .planning/milestones/${MILESTONE_FOLDER_NAME}
✓ Placeholder: MILESTONE.json (version reserved)
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

**After MCP call succeeds**, store the returned values:
```
MONGODB_MILESTONE_ID=[returned milestone_id]
```

**Extract PROJECT_NAME from MILESTONE-CONTEXT.md:**
Read the generated MILESTONE-CONTEXT.md and extract the project name (e.g., `Linkpay_Comissao_1c7aac45`). Store as `PROJECT_NAME`. This is **required** for all subsequent MCP calls to avoid element disambiguation errors.

**If IS_MULTI:** For each additional element (all except primary), enrich the MILESTONE-CONTEXT.md with a lightweight summary. Do NOT generate full JSONs — detailed data is fetched on-demand via MCP during execution.

For each additional element:
1. Call `mcp__wxcode-kb__get_element(element_name=ELEM, project_name=PROJECT_NAME)` — get type, layer, stats
2. Call `mcp__wxcode-kb__get_dependencies(element_name=ELEM, project_name=PROJECT_NAME, direction="uses")` — get table deps

Append to MILESTONE-CONTEXT.md:
```markdown
## Additional Element: ${ELEM}
- **Type:** ${type} | **Layer:** ${layer}
- **Controls:** ${control_count} (${controls_with_code} with code)
- **Procedures:** ${procedure_count}
- **Table dependencies:** ${table_list}
```

Display confirmation:
```
✓ Milestone created in MongoDB: ${MONGODB_MILESTONE_ID}
✓ Version: ${WXCODE_VERSION}
✓ Elements: ${ELEMENT_LIST} (${ELEMENT_COUNT} total)
```

**If MCP call fails:**
- Remove the created folder: `rm -rf .planning/milestones/${MILESTONE_FOLDER_NAME}`
- Display error and **STOP**

**CHECKPOINT: Verify MCP was called before continuing.**

### Step 5: Store for later phases

These values are used in later phases:
- `ELEMENT_NAME` — for context gathering
- `OUTPUT_PROJECT_ID` — for MCP calls
- `PROJECT_NAME` — for MCP element disambiguation (CRITICAL: pass to ALL MCP calls)
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

## Phase 1.75: Create Worktree (Optional — Multi-Dev)

**Check config for worktree mode:**

```bash
WORKTREE_MODE=$(cat .planning/config.json 2>/dev/null | grep -o '"worktree"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
```

**If `worktree` is `false` (default):** Skip to Phase 1.8.

**If `worktree` is `true`:**

This enables parallel milestone development. Each milestone gets its own branch and worktree so multiple developers can work simultaneously.

### Step 1: Commit placeholder on main

The placeholder MILESTONE.json was created in Phase 1.6 Step 3. Commit it on main to **reserve the version atomically**:

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")

if [ "$COMMIT_PLANNING_DOCS" = "true" ]; then
  git add .planning/milestones/${MILESTONE_FOLDER_NAME}/MILESTONE.json
  git commit -m "docs: reserve milestone ${WXCODE_VERSION}-${ELEMENT_NAME}"
  git push origin main 2>/dev/null || echo "⚠ Push failed — manual push needed before another dev starts a milestone"
fi
```

Display:
```
✓ Version ${WXCODE_VERSION} reserved on main
```

### Step 2: Create branch and worktree

```bash
BRANCH_NAME="milestone/${WXCODE_VERSION}-${ELEMENT_NAME}"
WORKTREE_PATH="../$(basename $PWD)-${WXCODE_VERSION}-${ELEMENT_NAME}"

git branch ${BRANCH_NAME}
git worktree add ${WORKTREE_PATH} ${BRANCH_NAME}
```

Display:
```
✓ Branch: ${BRANCH_NAME}
✓ Worktree: ${WORKTREE_PATH}
```

### Step 3: Instruct developer

```
╔══════════════════════════════════════════════════════════════╗
║  WORKTREE CREATED — Open in a new IDE window                 ║
╚══════════════════════════════════════════════════════════════╝

Open the worktree directory in your IDE:
  ${WORKTREE_PATH}

Then run in the new session:
  /wxcode:progress

The remaining steps (requirements, roadmap, planning) happen
in the worktree, not here on main.
```

**STOP HERE** — remaining phases execute in the worktree's session.

The user opens the worktree in their IDE. A fresh Claude Code session in that worktree picks up from `.planning/` state and continues the workflow (Phase 2+).

---

## Phase 1.8: Ensure Database Models (Conversion Projects Only)

**Purpose:** The new application accesses the EXISTING legacy database. Before converting an element, ensure all required table models exist.

**Step 1: Get table dependencies for ALL elements**

For each element in ELEMENT_LIST:
```
mcp__wxcode-kb__get_dependencies(element_name=ELEM, project_name=PROJECT_NAME, direction="uses")
```

Filter for TABLE dependencies and **union + deduplicate** across all elements:
```python
all_table_deps = set()
for elem in ELEMENT_LIST:
    deps = get_dependencies(elem, direction="uses")
    all_table_deps |= {dep for dep in deps if dep.type == "TABLE"}
table_deps = sorted(all_table_deps)
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
◆ Elements need tables: [TABLE_A, TABLE_B, ...] (combined from ${ELEMENT_COUNT} elements)
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
✓ Database models ready for ${ELEMENT_COUNT} element(s)
  - Existing: [N] tables
  - Generated: [M] tables
```

**If no table dependencies:** Skip to Phase 2.

---

## Phase 1.85: Load Comprehension Data (Conversion Projects Only)

**Skip if not a conversion project** (no `.planning/CONVERSION.md`).

### Step 1: Get business rules for ALL elements

For each element in ELEMENT_LIST:
```
mcp__wxcode-kb__get_business_rules(element_name=ELEM, project_name=PROJECT_NAME)
```

Aggregate all rules, deduplicating by rule ID.

### Step 2: Get screenshots and planes for ALL elements

For each element in ELEMENT_LIST:
```
mcp__wxcode-kb__get_element_screenshot(element_name=ELEM, project_name=PROJECT_NAME)
mcp__wxcode-kb__get_element_planes(element_name=ELEM, project_name=PROJECT_NAME)
```

If screenshots exist, **read the image files** to visually understand the UI. This informs the roadmapper about layout, visual patterns, and component choices.

Store screenshot paths for inclusion in MILESTONE-CONTEXT.md or roadmapper prompt.

### Step 3: Get similar elements for ALL elements

For each element in ELEMENT_LIST:
```
mcp__wxcode-kb__semantic_search(query=ELEM, project_name=PROJECT_NAME, search_mode="hybrid")
```

Deduplicate similar elements across queries.

### Step 4: Display context

If comprehension data found:
```
✓ Comprehension data loaded for ${ELEMENT_COUNT} element(s)
  - {N} business rules found
  - {M} similar elements ({K} already converted)
  - {P} screenshots loaded
```

If no data: Skip gracefully:
```
ℹ No comprehension data found (run `wxcode comprehend` first)
```

Business rules, screenshots, and similar elements inform research and roadmap phases.

---

## Phase 1.86: Dependency Tree Analysis (Conversion Projects Only)

**Skip if not a conversion project** (no `.planning/CONVERSION.md`).

**Purpose:** Show the user the full dependency tree for each element and let them choose how deep to implement in this milestone. Dependencies beyond the selected depth get auto-generated stubs with matching signatures.

### Step 1: Build dependency tree for ALL elements

For each element in ELEMENT_LIST, build a dependency tree using recursive `get_dependencies` calls:

```
# Level D1: Direct dependencies
D1 = mcp__wxcode-kb__get_dependencies(element_name=ELEM, project_name=PROJECT_NAME, direction="uses")
     → filter to Procedure and Class only (exclude TABLE — handled in Phase 1.8)
     → exclude local procedures (names containing "ELEM." prefix — these are part of the element)

# Level D2: Dependencies of D1
For each D1 item (parallel where possible):
  D2 = mcp__wxcode-kb__get_dependencies(element_name=D1_ITEM.name, project_name=PROJECT_NAME, direction="uses")
       → filter Procedure/Class, exclude TABLE, exclude already-seen nodes

# Level D3: Dependencies of D2
For each D2 item (parallel where possible):
  D3 = mcp__wxcode-kb__get_dependencies(element_name=D2_ITEM.name, project_name=PROJECT_NAME, direction="uses")
       → filter Procedure/Class, exclude TABLE, exclude already-seen nodes

# Stop at D3 by default (max_depth=3) to limit MCP calls
```

**Deduplication:** Track visited nodes across all depths. If a procedure appears at D1 and D2, keep the shallowest depth.

### Step 2: Get signatures for all unique procedures

For each unique procedure in the tree:
```
mcp__wxcode-kb__get_procedure(procedure_name=PROC_NAME, project_name=PROJECT_NAME)
→ extract: signature, parameters[], return_type
```

Also check conversion status from the element's `conversion_status` field.

### Step 3: Display tree with depth levels

Present a visual tree to the user. Example:

```
Dependency Tree — PaginaInicial_New1

D1 (Direct — 5 procedures):
  ✓ Documento_TemplatePreenchido(sSlug, sContent): (str, str)     [pending]
  ✓ Documento_ConsultarAceite(sSlug): (str, str)                  [pending]
  ✓ Documento_RegistrarAceite(sSlug, sContent): (str, str)        [pending]
  ✓ Thread_GravaLogProcessamento(sMsg): void                      [pending]
  ● SQLServerConectar(): boolean                                   [converted]

D2 (Dependencies of D1 — 2 procedures):
  ✓ REST_ConfigurarAutenticacao(sToken): void                     [pending]
  ✓ Global_PegaTokenAPI(): string                                 [pending]

D3 (Dependencies of D2 — 1 procedure):
  ✓ Config_LerParametro(sChave): string                           [pending]

Local procedures (included in element conversion):
  • PaginaInicial_New1.VerificarUsuarioSenha
  • PaginaInicial_New1.Local_ConfiguraMenu
  • PaginaInicial_New1.Local_RecuperarEmail

Legend: ✓ = pending, ● = already converted

Summary:
  D1: 5 total (1 converted, 4 pending)
  D2: 2 total (0 converted, 2 pending)
  D3: 1 total (0 converted, 1 pending)
```

**If no procedure dependencies found:** Skip this phase entirely (element only calls local procedures or WLanguage built-ins).

**If ALL dependencies already converted:** Display tree with all `●` markers and skip depth selection — no stubs needed.

### Step 4: User selects depth

Use AskUserQuestion:

```
header: "Dep depth"
question: "Até qual nível de dependências deseja implementar neste milestone?"
options:
  - label: "D0 — Apenas o elemento"
    description: "Stubs para todas as dependências pendentes"
  - label: "D1 — Dependências diretas (Recommended)"
    description: "${D1_pending_count} procedures + stubs para D2+"
  - label: "D2 — Até segundo nível"
    description: "${D1_pending_count + D2_pending_count} procedures + stubs para D3+"
  - label: "D3 — Todas as dependências"
    description: "${total_pending_count} procedures, sem stubs"
```

**Adjust options dynamically:** Only show depth levels that have pending procedures. If D3 is empty, max option is D2. If D2 is empty, max option is D1. If D1 is empty, skip this phase.

### Step 5: Store selection and generate dependency manifest

Based on user selection:

```
DEPENDENCY_DEPTH = [selected depth: D0, D1, D2, or D3]
IMPLEMENT_LIST = [procedures at or below selected depth that are NOT already converted]
STUB_LIST = [procedures beyond selected depth that are NOT already converted]
```

**Already-converted procedures** go into neither list — they're imported as-is.

Append to MILESTONE-CONTEXT.md:

```markdown
## Dependency Strategy

**Depth:** D${N} (${depth_description})
**Implement:** ${IMPLEMENT_LIST.length} procedures
**Stub:** ${STUB_LIST.length} procedures (D${N+1}+)
**Already converted:** ${converted_count} procedures (import as-is)

### To Implement
| Procedure | Signature | Element | Depth |
|-----------|-----------|---------|-------|
| Documento_TemplatePreenchido | (sSlug, sContent) → (str,str) | Comunicacao_APIDocs | D1 |
| ... | ... | ... | ... |

### Stubs (Deferred Dependencies)
| Procedure | Signature | Element | Depth | Called By |
|-----------|-----------|---------|-------|----------|
| REST_ConfigurarAutenticacao | (sToken) → void | REST_Utils | D2 | Documento_TemplatePreenchido |
| ... | ... | ... | ... | ... |

### Already Converted (Import)
| Procedure | Element |
|-----------|---------|
| SQLServerConectar | ConexaoBD |
| ... | ... |
```

Display confirmation:
```
✓ Dependency strategy defined
  - Depth: D${N}
  - Implement: ${IMPLEMENT_LIST.length} procedures
  - Stub: ${STUB_LIST.length} procedures (deferred)
  - Import: ${converted_count} procedures (already converted)
```

### Step 6: Persist business rules to MongoDB

**Do this IMMEDIATELY after Step 5** — same phase, no gap.

Build implement_list and stub_list dicts from Step 5 output:

```python
# For each procedure in IMPLEMENT_LIST:
implement_list = [
    {
        "procedure_name": "VerificarUsuarioSenha",
        "element_name": "PaginaInicial_New1",
        "depth": 0,
        "is_control_event": False
    },
    {
        "procedure_name": "BTN_Login.event_851980",
        "element_name": "PaginaInicial_New1",
        "depth": 0,
        "is_control_event": True  # events contain "event_" in name
    },
    {
        "procedure_name": "Documento_TemplatePreenchido",
        "element_name": "Comunicacao_APIDocs",
        "depth": 1,
        "is_control_event": False
    }
]

# For each procedure in STUB_LIST:
stub_list = [
    {
        "procedure_name": "REST_ConfigurarAutenticacao",
        "element_name": "REST_Utils",
        "depth": 2,
        "is_control_event": False
    }
]
```

**Include control events:** Get all procedures for each element:
```
mcp__wxcode-kb__get_procedures(element_name=ELEM, project_name=PROJECT_NAME)
```
Filter: those with `event_` in the name are control events. Add them to implement_list with `is_control_event=true` and `depth=0`.

Call MCP to persist:
```
mcp__wxcode-kb__populate_milestone_rules(
    milestone_id=MONGODB_MILESTONE_ID,
    implement_list=implement_list,
    stub_list=stub_list,
    confirm=true
)
```

Display result:
```
✓ Business rules tracking initialized
  - Procedures tracked: ${procedures_created}
  - Business rules: ${rules_created} (${pending} pending, ${deferred} deferred)
```

**If MCP call fails:** Log warning and continue — rules tracking is advisory, not blocking.

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
- Also check `.planning/milestones/v*/MILESTONE.json` for reserved versions (parallel worktrees)
- Suggest next version (v1.0 → v1.1, or v2.0 for major)
- Confirm with user

### Phase 3.5: Create Placeholder and Worktree (If Enabled)

**Check config for worktree mode:**

```bash
WORKTREE_MODE=$(cat .planning/config.json 2>/dev/null | grep -o '"worktree"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
```

**If `worktree` is `false` (default):** Skip to Phase 4.

**If `worktree` is `true`:**

Create milestone placeholder to reserve version:

```bash
MILESTONE_FOLDER_NAME="v${VERSION}-${MILESTONE_NAME_SLUG}"
mkdir -p .planning/milestones/${MILESTONE_FOLDER_NAME}

cat > .planning/milestones/${MILESTONE_FOLDER_NAME}/MILESTONE.json << EOF
{
  "version": "v${VERSION}",
  "name": "${MILESTONE_NAME}",
  "status": "in_progress",
  "branch": "milestone/v${VERSION}-${MILESTONE_NAME_SLUG}",
  "worktree": "../$(basename $PWD)-v${VERSION}-${MILESTONE_NAME_SLUG}",
  "created_at": "$(date +%Y-%m-%d)"
}
EOF
```

Commit on main and create worktree (same as Phase 1.75):

```bash
git add .planning/milestones/${MILESTONE_FOLDER_NAME}/MILESTONE.json
git commit -m "docs: reserve milestone v${VERSION}-${MILESTONE_NAME_SLUG}"
git push origin main 2>/dev/null || echo "⚠ Push failed"

BRANCH_NAME="milestone/v${VERSION}-${MILESTONE_NAME_SLUG}"
WORKTREE_PATH="../$(basename $PWD)-v${VERSION}-${MILESTONE_NAME_SLUG}"
git branch ${BRANCH_NAME}
git worktree add ${WORKTREE_PATH} ${BRANCH_NAME}
```

Display same worktree instructions as Phase 1.75 Step 3.

**STOP HERE if worktree created** — remaining phases execute in the worktree.

## Phase 4: Update PROJECT.md

Update these sections (stable info only — no volatile milestone state):

- Update Active requirements section with new goals
- Update "Last updated" footer
- Do NOT add "Current Milestone" section here — that goes in STATE.md (avoids merge conflicts in worktree scenarios)

## Phase 5: Update STATE.md

Add current milestone info and reset position:

```markdown
## Current Milestone

**Milestone:** v[X.Y] [Name]
**Goal:** [One sentence describing milestone focus]
**Target features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: [today] — Milestone v[X.Y] started
```

Keep Accumulated Context section (decisions, blockers) from previous milestone.

**Why STATE.md:** Each worktree has its own STATE.md, so there's zero conflict when milestones run in parallel. PROJECT.md stays stable with just validated requirements and decisions.

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

**Phase numbering is LOCAL to each milestone — always starts at 1.**

This enables parallel milestone development via git worktrees. Each milestone's phases are numbered independently (01, 02, 03...) regardless of previous milestones.

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

</planning_context>

<instructions>
Create roadmap for milestone v[X.Y]:
1. Start phase numbering from 1 (phases are LOCAL to each milestone)
2. Derive phases from THIS MILESTONE's requirements (don't include validated/existing)
3. Map every requirement to exactly one phase
4. Derive 2-5 success criteria per phase (observable user behaviors)
5. Validate 100% coverage of new requirements
6. Write files immediately (ROADMAP.md, STATE.md, update REQUIREMENTS.md traceability)
7. Return ROADMAP CREATED with summary

**Multi-element milestone:** This milestone converts ${ELEMENT_COUNT} element(s): ${ELEMENT_LIST}
- If elements share tables/procedures: organize phases cross-element
  (Phase 1 = shared models, Phase 2 = shared routes, Phase 3 = per-element templates)
- If elements are independent: organize per-element
  (Phase 1 = Element A complete, Phase 2 = Element B complete)
- The agent fetches detailed element data on-demand via MCP during planning.

**Dependency strategy (if Phase 1.86 was executed):**
- IMPLEMENT_LIST: Procedures to convert in this milestone (include as tasks)
- STUB_LIST: Procedures to generate stubs for (single task: "Generate dependency stubs")
- Already-converted procedures: Import as-is (don't recreate)
- Read MILESTONE-CONTEXT.md "Dependency Strategy" section for full lists

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

Run: wxcode:discuss-phase [N] — gather context and clarify approach

*Run clear first for fresh context window*

---

**Also available:**
- wxcode:plan-phase [N] — skip discussion, plan directly

───────────────────────────────────────────────────────────────
```

</process>

<success_criteria>
- [ ] **(Conversion projects)** Arguments parsed: --element/--elements and --output-project
- [ ] **(Conversion projects)** ELEMENT_LIST derived correctly (single or multi)
- [ ] **(Conversion projects)** Version determined automatically (v1.0, v1.1, etc.)
- [ ] **(Conversion projects)** Milestone folder named correctly (single: `v1.0-PAGE_Login`, multi: `v1.0-PAGE_Login+2more` or `v1.0-auth-pages`)
- [ ] **(Conversion projects)** MILESTONE.json has both `"element"` (primary) and `"elements"` (array) fields
- [ ] **(If worktree enabled)** Placeholder committed on main
- [ ] **(If worktree enabled)** Branch and worktree created
- [ ] **(If worktree enabled)** User instructed to open worktree in new IDE window
- [ ] **(Conversion projects - CRITICAL)** `mcp__wxcode-kb__create_milestone` called with confirm=true
- [ ] **(Conversion projects - CRITICAL)** MONGODB_MILESTONE_ID stored from MCP response
- [ ] **(Multi-element)** Additional elements enriched in MILESTONE-CONTEXT.md (lightweight summary)
- [ ] **(Conversion projects)** Table dependencies collected from ALL elements (union + deduplicate)
- [ ] **(Conversion projects)** Comprehension data loaded for ALL elements (if available)
- [ ] **(Conversion projects)** Dependency tree built recursively (D1→D2→D3) with signatures
- [ ] **(Conversion projects)** User selected dependency depth (D0/D1/D2/D3) via AskUserQuestion
- [ ] **(Conversion projects)** MILESTONE-CONTEXT.md updated with Dependency Strategy (IMPLEMENT_LIST + STUB_LIST)
- [ ] **(Conversion projects)** `mcp__wxcode-kb__populate_milestone_rules` called with IMPLEMENT_LIST + STUB_LIST (Phase 1.86 Step 6)
- [ ] **(Conversion projects)** Business rules tracking initialized in MongoDB (procedures + rule verifications)
- [ ] **(Multi-element)** Roadmapper instructed on cross-element vs per-element phase organization
- [ ] PROJECT.md updated (stable info only, no volatile milestone state)
- [ ] STATE.md updated with Current Milestone section and reset position
- [ ] MILESTONE-CONTEXT.md consumed and deleted (if existed)
- [ ] Research completed (if selected) — 4 parallel agents spawned, milestone-aware
- [ ] Requirements gathered (from research or conversation)
- [ ] User scoped each category
- [ ] REQUIREMENTS.md created with REQ-IDs
- [ ] wxcode-roadmapper spawned with phase numbering context
- [ ] Roadmap files written immediately (not draft)
- [ ] User feedback incorporated (if any)
- [ ] ROADMAP.md created with phases starting from 1 (local to milestone)
- [ ] All commits made (if planning docs committed)
- [ ] User knows next step is `/wxcode:discuss-phase [N]`

**Atomic commits:** Each phase commits its artifacts immediately. If context is lost, artifacts persist.

- [ ] `/wxcode:dashboard --all` invoked (Phase 10)
- [ ] Project dashboard updated: `.planning/dashboard.json`
- [ ] Milestone dashboard created: `.planning/dashboard_<milestone>.json`
- [ ] (Conversion projects) Schema dashboard regenerated
</success_criteria>

