# Injection Points

How standard GSD commands and agents should be extended for conversion context.

## Mechanism

Commands and agents should:
1. Check if `.planning/CONVERSION.md` exists (indicates conversion project)
2. If yes, load conversion context and apply extended behavior
3. Reference `.wxcode/conversion/` knowledge files

---

## Command: new-project

### Standard Behavior
Creates PROJECT.md, REQUIREMENTS.md, ROADMAP.md via questioning.

### Conversion Extension

**Detection:** User mentions "convert", "WinDev", "legacy", or MCP tools are available.

**Additional questioning:**
```
Is this a conversion project from WinDev/WebDev legacy code?

If yes:
1. What is the source project name in MongoDB?
2. What is the Output Project / target stack?
3. What elements are in scope for this milestone?
```

**Additional outputs:**
- Create `.planning/CONVERSION.md` with project context
- REQUIREMENTS.md should list elements to convert as requirements
- ROADMAP.md phases should group elements logically

---

## Command: discuss-phase

### Standard Behavior
Asks user about implementation decisions for a phase.

### Conversion Extension

**Before ANY question:**

```
1. Check .planning/CONVERSION.md for current element
2. Call MCP tools to get legacy context:
   - get_element {current_element}
   - get_controls {current_element}
   - get_procedures {current_element}
3. Analyze legacy code for existing answers
4. Only ask about NEW decisions
```

**Question reframing:**

| Standard Question | Conversion Question |
|-------------------|---------------------|
| "What fields should the form have?" | "Legacy has EDT_Usuario and EDT_Senha. Keep names or use stack conventions?" |
| "What validation rules?" | "Legacy validates CPF in proc:ValidaCPF. Preserve logic or modernize?" |
| "What layout?" | "Legacy has 3 planes (wizard). Convert as tabs, wizard, or routes?" |

**Output to CONTEXT.md:**
```markdown
## Legacy Context

Element: PAGE_Login
Controls: EDT_Usuario, EDT_Senha, BTN_Entrar, BTN_Recuperar
Planes: 2 (Login, Recuperar Senha)
Dependencies: proc:ValidaLogin, TABLE:USUARIO

## Decisions

### Naming: Keep legacy style
- EDT_Usuario → username (user preference)
- EDT_Senha → password (user preference)

### Planes: Convert as modal
- Plane 1 (Login) → Main form
- Plane 2 (Recuperar) → Modal dialog

### Validation: Preserve logic
- Use existing validar_cpf() from services/validation.py
```

---

## Command: research-phase

### Standard Behavior
Researches target stack ecosystem.

### Conversion Extension

**Add legacy research phase BEFORE stack research:**

```
## Phase 0: Legacy Analysis

1. Get element from STATE.md or CONVERSION.md
2. Call MCP tools:
   - get_element → Full code and AST
   - get_controls → UI structure
   - get_procedures → Business logic
   - get_schema → Database requirements
   - get_dependencies → Prerequisites
   - analyze_impact → What depends on this

3. Analyze code for:
   - Planes (see planes-detection.md)
   - WLanguage functions used
   - Database operations
   - External dependencies

4. Check conversion state:
   - get_conversion_context → What's already converted
   - Dependencies converted? → Can import
   - Dependencies pending? → May need first
```

**Output to RESEARCH.md:**
```markdown
## Legacy Analysis

### Element: {name}
- Type: {page|window|procedure|class}
- Lines of code: {count}
- Complexity: {low|medium|high}

### UI Structure
{from get_controls}

### Planes
{if detected - see planes-detection.md}

### Business Logic
{from procedures - key functions and their purpose}

### Database Operations
{tables accessed, CRUD operations}

### Dependencies
- Already converted: {list} → Import these
- Pending: {list} → May need first
- Circular: {list} → Handle carefully

### WLanguage Functions
{significant functions found - note for conversion}

---

## Target Stack Research

{standard research continues here}
```

---

## Command: new-milestone (Phase 1.86)

### Standard Behavior
N/A (conversion-only phase).

### Conversion Extension

**Dependency tree analysis with depth selection:**

1. Build dependency tree recursively using `get_dependencies(direction="uses")` at D1→D2→D3
2. Get signatures for all unique procedures via `get_procedure`
3. Display tree with depth levels and conversion status
4. User selects implementation depth (D0/D1/D2/D3)
5. Generate IMPLEMENT_LIST (convert) and STUB_LIST (generate stubs)
6. Write to MILESTONE-CONTEXT.md "Dependency Strategy" section

**Downstream consumers:**
- **Roadmapper:** Includes IMPLEMENT_LIST procedures as tasks, STUB_LIST as single stub-generation task
- **Planner:** Treats stubs as valid imports, doesn't block on STUB_LIST items
- **Executor:** Generates stub files with `WXCODE:STUB` marker and `raise NotImplementedError`
- **Audit:** Counts stubs via `grep -r "WXCODE:STUB"`, reports as deferred (not failure)

---

## Command: plan-phase

### Standard Behavior
Creates PLAN.md with tasks.

### Conversion Extension

**Plans must include conversion context:**

```xml
<plan>
  <conversion_context>
    <legacy_element>PAGE_Login</legacy_element>
    <legacy_type>page</legacy_type>
    <target_stack>fastapi-jinja2</target_stack>
    <dependencies_converted>
      <item>proc:ValidaCPF → services/validation.py</item>
      <item>TABLE:USUARIO → models/usuario.py</item>
    </dependencies_converted>
    <dependencies_pending>
      <!-- None, or list what needs conversion first -->
    </dependencies_pending>
    <structure_approach>preserve</structure_approach>
    <planes_strategy>modal</planes_strategy>
  </conversion_context>

  <tasks>
    <task type="auto">
      <name>Create login route</name>
      <files>routes/auth.py</files>
      <action>
        Convert PAGE_Login to FastAPI route.
        - Import validar_cpf from services.validation
        - Use Usuario model from models.usuario
        - Preserve validation logic from legacy
      </action>
      <legacy_reference>
        See RESEARCH.md "Legacy Analysis" for original code
      </legacy_reference>
    </task>
    ...
  </tasks>
</plan>
```

**Task considerations:**
1. Import already-converted dependencies (don't recreate)
2. Reference legacy code in action descriptions
3. Note structure preservation decisions
4. Include planes handling if applicable

---

## Command: execute-phase

### Standard Behavior
Executes plans, spawns executors.

### Conversion Extension

**Executor context includes:**
- Legacy analysis from RESEARCH.md
- Conversion decisions from CONTEXT.md
- MCP tools for runtime queries

**Executor behavior:**
```
1. Read PLAN.md including conversion_context
2. For each task:
   a. Check legacy reference if provided
   b. Import converted dependencies (don't recreate)
   c. Follow structure-preservation.md guidelines
   d. Generate code that matches legacy semantics
3. After all tasks:
   a. Mark element as converted: MCP mark_converted
```

**Post-execution:**
```
MCP: mark_converted {element_name}
```

Update `.planning/CONVERSION.md` state.

---

## Command: verify-work

### Standard Behavior
User acceptance testing.

### Conversion Extension

**Include legacy comparison:**
```
## Verification: PAGE_Login

### Functionality Check
Based on legacy code, this element should:
- [ ] Accept username and password
- [ ] Validate credentials against USUARIO table
- [ ] Show error for invalid login
- [ ] Redirect to dashboard on success
- [ ] Have password recovery option (Plane 2 → Modal)

### Legacy Behavior Preserved
- [ ] Validation logic matches proc:ValidaLogin
- [ ] Error messages similar to legacy
- [ ] Field names/IDs preserve semantics
```

---

## Agent: wxcode-phase-researcher

### Standard Behavior
Researches ecosystem for phase implementation.

### Conversion Extension

**Spawn legacy analyzer first:**
```
Before standard research:

1. Spawn wxcode-legacy-analyzer agent
2. Wait for legacy analysis
3. Include output in RESEARCH.md
4. Continue with stack research
```

**Context includes:**
```
@.wxcode/conversion/mcp-usage.md
@.wxcode/conversion/planes-detection.md
@.planning/CONVERSION.md
```

---

## Agent: wxcode-planner

### Standard Behavior
Creates plans for phase.

### Conversion Extension

**Additional context:**
```
@.wxcode/conversion/structure-preservation.md
@.planning/CONVERSION.md
```

**Planning rules:**
1. Check dependencies via MCP before planning
2. Import converted elements, don't recreate
3. Include conversion_context in plan XML
4. Reference legacy code for implementation details

---

## Agent: wxcode-executor

### Standard Behavior
Executes tasks from plans.

### Conversion Extension

**Additional context:**
```
@.wxcode/conversion/structure-preservation.md
```

**Execution rules:**
1. Read legacy analysis from RESEARCH.md
2. Follow structure preservation guidelines
3. Import from already-converted modules
4. Preserve semantics while adapting syntax
5. Document deviations in SUMMARY.md

**Post-execution:**
```
If all tasks successful:
  MCP: mark_converted {element_name}
```

---

## File: .planning/CONVERSION.md

Created when conversion project is detected.

**Template:**
```markdown
# Conversion Project Context

## Source Project
- **Name**: {project_name from MongoDB}
- **Type**: WinDev/WebDev
- **MCP Available**: Yes

## Target Stack
- **Stack ID**: {from Output Project}
- **Language**: {language}
- **Framework**: {framework}
- **ORM**: {orm}
- **Template Engine**: {template_engine}

## Current State
- **Total Elements**: {count}
- **Converted**: {count}
- **Pending**: {count}
- **Current Element**: {name}

## Decisions (Project-Wide)

### Naming Convention
- [ ] Preserve legacy names
- [x] Use target stack conventions
- [ ] Hybrid (ask per element)

### Structure Preservation
- [x] Maintain similar organization
- [ ] Full modernization

### Global Variables
- [ ] Keep g_ prefix
- [x] Convert to proper patterns (session, DI)

### Planes Default Strategy
- [ ] Tabs
- [x] Wizard
- [ ] Routes
- [ ] Ask per element

## Notes
{project-specific notes and decisions}
```

---

## Detection Logic

Commands should detect conversion context by:

```python
def is_conversion_project():
    # Check 1: CONVERSION.md exists
    if exists(".planning/CONVERSION.md"):
        return True

    # Check 2: MCP tools available
    if mcp_tools_available():
        return True

    # Check 3: User mentioned conversion keywords
    if user_mentioned(["convert", "WinDev", "WebDev", "legacy", "migration"]):
        return True

    return False
```

When detected, load:
- `.planning/CONVERSION.md` (if exists)
- `.wxcode/conversion/*.md` (knowledge files)
