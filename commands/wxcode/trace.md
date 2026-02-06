---
name: trace
description: Navigate bidirectionally between legacy WinDev elements and converted code
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__wxcode-kb__get_element
  - mcp__wxcode-kb__get_controls
  - mcp__wxcode-kb__get_procedures
  - mcp__wxcode-kb__get_dependencies
  - mcp__wxcode-kb__list_elements
  - mcp__wxcode-kb__get_conversion_stats
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"trace","args":"$ARGUMENTS","title":"WXCODE ▶ TRACING ELEMENT"} -->
## WXCODE ▶ TRACING ELEMENT
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"progress","args":"","description":"Continue with project","priority":"recommended"} -->
```
</structured_output>

<command-name>trace</command-name>

# /wxcode:trace - Legacy ↔ Converted Navigation

Navigate between legacy WinDev/WebDev code and its converted equivalent.

## Usage

```bash
# From legacy element name
/wxcode:trace PAGE_Login
/wxcode:trace ServerProcedures
/wxcode:trace Global_ValidaCPF
/wxcode:trace TABLE:USUARIO

# From converted file path
/wxcode:trace app/routes/auth.py
/wxcode:trace app/services/validation.py

# With specific query
/wxcode:trace PAGE_Login --controls    # Show only control mappings
/wxcode:trace PAGE_Login --procedures  # Show only procedure mappings
/wxcode:trace PAGE_Login --deviations  # Show only deviations from legacy
```

## Execution Flow

<step name="parse_input">
Parse the input to determine direction:

**Legacy → Converted** (input looks like element name):
- Starts with `PAGE_`, `WIN_`, `FORM_`, `LIST_`, `DASHBOARD_`
- Starts with `TABLE:`
- Contains only alphanumeric and underscores
- Matches known procedure names

**Converted → Legacy** (input looks like file path):
- Contains `/` or `\`
- Ends with `.py`, `.html`, `.ts`, `.tsx`, `.vue`, etc.
- Exists as file in project

```bash
INPUT="$1"

if [[ "$INPUT" == *"/"* ]] || [[ "$INPUT" == *".py"* ]] || [[ "$INPUT" == *".html"* ]]; then
    DIRECTION="converted_to_legacy"
else
    DIRECTION="legacy_to_converted"
fi
```
</step>

<step name="legacy_to_converted">
**When tracing from legacy element to converted code:**

### 1. Get Element Info from MCP

```
mcp__wxcode-kb__get_element(element_name="{INPUT}")
```

If procedure name (no prefix), try:
```
mcp__wxcode-kb__get_procedure(procedure_name="{INPUT}")
```

### 2. Check Conversion Status

Parse the `conversion` field:
- `status`: pending | in_progress | converted | validated
- `target_files`: List of converted files

### 3. Find @legacy Comments in Codebase

```bash
grep -rn "@legacy-element: {ELEMENT_NAME}" . --include="*.py" --include="*.html" --include="*.ts"
grep -rn "@legacy: {ELEMENT_NAME}" . --include="*.py" --include="*.html" --include="*.ts"
```

### 4. Get Control Mappings (for pages)

If element is a page:
```
mcp__wxcode-kb__get_controls(element_name="{ELEMENT_NAME}")
```

Then search for each control:
```bash
grep -rn "@legacy: EDT_Usuario" . --include="*.html"
```

### 5. Get Procedure Mappings

```
mcp__wxcode-kb__get_procedures(element_name="{ELEMENT_NAME}")
```

For each procedure, search:
```bash
grep -rn "@legacy: {PROCEDURE_NAME}" . --include="*.py"
```

### 6. Display Results

Format output as:

```
┌─────────────────────────────────────────────────────────────────────┐
│ LEGACY: {ELEMENT_NAME}                                              │
│ TYPE: {type} | LAYER: {layer}                                       │
│ STATUS: {conversion_status}                                         │
├─────────────────────────────────────────────────────────────────────┤
│ CONVERTED FILES:                                                    │
│   Route:    {file}:{line_start}-{line_end}                         │
│   Template: {file}                                                  │
│   Service:  {file}:{line}                                          │
│   Tests:    {file}                                                  │
├─────────────────────────────────────────────────────────────────────┤
│ CONTROL MAPPINGS:                                                   │
│   {LEGACY_CONTROL} → {converted_selector} ({file}:{line})          │
├─────────────────────────────────────────────────────────────────────┤
│ PROCEDURE MAPPINGS:                                                 │
│   {LEGACY_PROC} → {converted_func}() ({file}:{line})               │
├─────────────────────────────────────────────────────────────────────┤
│ TABLE BINDINGS:                                                     │
│   {TABLE.FIELD} → {model.attribute}                                │
├─────────────────────────────────────────────────────────────────────┤
│ DEVIATIONS:                                                         │
│   • {deviation_description}                                         │
├─────────────────────────────────────────────────────────────────────┤
│ DEPENDENCIES:                                                       │
│   Uses: {dep1}, {dep2}, ...                                        │
│   Used by: {dep1}, {dep2}, ...                                     │
└─────────────────────────────────────────────────────────────────────┘
```
</step>

<step name="converted_to_legacy">
**When tracing from converted file to legacy elements:**

### 1. Read File and Extract @legacy Comments

```bash
grep -n "@legacy" "{FILE_PATH}"
```

Parse comment types:
- `@legacy-element:` → Main legacy source
- `@legacy:` → Inline legacy references
- `@legacy-deviation:` → Behavior changes

### 2. Get Unique Legacy Elements

Collect all unique element/procedure names from comments.

### 3. Query MCP for Each Element

For each legacy reference found:
```
mcp__wxcode-kb__get_element(element_name="{ELEMENT}")
```

### 4. Display Results

```
┌─────────────────────────────────────────────────────────────────────┐
│ FILE: {FILE_PATH}                                                   │
│ SIZE: {lines} lines                                                 │
├─────────────────────────────────────────────────────────────────────┤
│ LEGACY ORIGINS:                                                     │
│   Primary: {element_name} ({type})                                  │
│   Lines {start}-{end}: {element}.{procedure}                        │
│   Lines {start}-{end}: {element}.{control}.{event}                  │
├─────────────────────────────────────────────────────────────────────┤
│ LEGACY PROCEDURES USED:                                             │
│   {converted_func}() ← {LEGACY_PROCEDURE} (line {N})               │
├─────────────────────────────────────────────────────────────────────┤
│ LEGACY CONTROLS MAPPED:                                             │
│   {selector} ← {LEGACY_CONTROL} (line {N})                         │
├─────────────────────────────────────────────────────────────────────┤
│ DEVIATIONS FROM LEGACY:                                             │
│   Line {N}: {deviation_description}                                 │
└─────────────────────────────────────────────────────────────────────┘
```
</step>

<step name="not_found_handling">
**When element is not converted yet:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ LEGACY: {ELEMENT_NAME}                                              │
│ STATUS: ⚠ NOT CONVERTED                                             │
├─────────────────────────────────────────────────────────────────────┤
│ ELEMENT INFO:                                                       │
│   Type: {type}                                                      │
│   Layer: {layer}                                                    │
│   File: {source_file}                                               │
├─────────────────────────────────────────────────────────────────────┤
│ DEPENDENCIES (must convert first):                                  │
│   ✓ {converted_dep} (converted)                                    │
│   ✗ {pending_dep} (pending)                                        │
├─────────────────────────────────────────────────────────────────────┤
│ SIMILAR CONVERTED:                                                  │
│   {similar_element} (85% similar) → {converted_files}              │
├─────────────────────────────────────────────────────────────────────┤
│ SUGGESTED ACTION:                                                   │
│   Run: /wxcode:plan-phase to include this element                  │
└─────────────────────────────────────────────────────────────────────┘
```
</step>

<step name="no_legacy_comments">
**When file has no @legacy comments:**

```
┌─────────────────────────────────────────────────────────────────────┐
│ FILE: {FILE_PATH}                                                   │
│ STATUS: ⚠ NO LEGACY TRACEABILITY                                    │
├─────────────────────────────────────────────────────────────────────┤
│ This file has no @legacy comments.                                  │
│                                                                     │
│ If this is converted code, add traceability:                        │
│                                                                     │
│   # @legacy-element: {SUGGESTED_ELEMENT}                           │
│   # @legacy-type: {type}                                           │
│                                                                     │
│ See: ~/.claude/wxcode-skill/.wxcode/conversion/                   │
│      structure-preservation.md#traceability-comments               │
└─────────────────────────────────────────────────────────────────────┘
```
</step>

## Examples

### Example 1: Trace a Page

```
> /wxcode:trace PAGE_Login

┌─────────────────────────────────────────────────────────────────────┐
│ LEGACY: PAGE_Login                                                  │
│ TYPE: page | LAYER: ui                                              │
│ STATUS: ✓ Converted (2026-02-01)                                   │
├─────────────────────────────────────────────────────────────────────┤
│ CONVERTED FILES:                                                    │
│   Route:    app/routes/auth.py:45-89                               │
│   Template: app/templates/login.html                               │
│   Tests:    tests/test_auth.py:12-67                               │
├─────────────────────────────────────────────────────────────────────┤
│ CONTROL MAPPINGS:                                                   │
│   EDT_Usuario  → input[name='usuario']     (login.html:15)         │
│   EDT_Senha    → input[name='senha']       (login.html:18)         │
│   BTN_Entrar   → button#btn-entrar         (login.html:21)         │
├─────────────────────────────────────────────────────────────────────┤
│ PROCEDURE MAPPINGS:                                                 │
│   Local_Login                   → login()            (auth.py:45)  │
│   Global_FazLoginUsuarioInterno → fazer_login_interno() (auth.py:52)│
│   Global_SetaTempoSessao        → (inline session)   (auth.py:78)  │
├─────────────────────────────────────────────────────────────────────┤
│ TABLE BINDINGS:                                                     │
│   USUARIO.LOGIN → Usuario.login                                    │
│   USUARIO.SENHA → Usuario.senha_hash (⚠ changed to hash)          │
├─────────────────────────────────────────────────────────────────────┤
│ DEVIATIONS:                                                         │
│   • Password now hashed with bcrypt (was plaintext)                │
│   • Session-based auth instead of global variables                 │
│   • Added CSRF protection                                          │
├─────────────────────────────────────────────────────────────────────┤
│ DEPENDENCIES:                                                       │
│   Uses: Global_FazLoginUsuarioInterno ✓, Global_SetaTempoSessao ✓  │
│   Used by: (entry point - no dependents)                           │
└─────────────────────────────────────────────────────────────────────┘
```

### Example 2: Trace a Procedure

```
> /wxcode:trace Global_ValidaCPF

┌─────────────────────────────────────────────────────────────────────┐
│ LEGACY: Global_ValidaCPF                                            │
│ TYPE: procedure | GROUP: Server_ValidacaoCPFCNPJ                    │
│ STATUS: ✓ Converted                                                 │
├─────────────────────────────────────────────────────────────────────┤
│ CONVERTED LOCATION:                                                 │
│   Function: validar_cpf()                                          │
│   File:     app/services/validation.py:12-45                       │
│   Tests:    tests/test_validation.py:8-34                          │
├─────────────────────────────────────────────────────────────────────┤
│ SIGNATURE MAPPING:                                                  │
│   Legacy:    Global_ValidaCPF(sCPF is string): boolean             │
│   Converted: validar_cpf(cpf: str) -> bool                         │
├─────────────────────────────────────────────────────────────────────┤
│ USED BY (23 elements):                                              │
│   PAGE_CadastroCliente, PAGE_CadastroFornecedor, FORM_Comprador,   │
│   PAGE_Checkout, API_ValidarDocumento, ...                         │
└─────────────────────────────────────────────────────────────────────┘
```

### Example 3: Trace from Converted File

```
> /wxcode:trace app/routes/auth.py

┌─────────────────────────────────────────────────────────────────────┐
│ FILE: app/routes/auth.py                                            │
│ SIZE: 156 lines | LEGACY REFS: 8                                    │
├─────────────────────────────────────────────────────────────────────┤
│ LEGACY ORIGINS:                                                     │
│   Primary: PAGE_Login (page)                                        │
│   Lines 45-89:  PAGE_Login.BTN_Entrar.OnClick                      │
│   Lines 92-110: PAGE_Login.OnLoad (session validation)             │
│   Lines 115-140: PAGE_SessaoExpirada redirect logic                │
├─────────────────────────────────────────────────────────────────────┤
│ LEGACY PROCEDURES:                                                  │
│   fazer_login_interno() ← Global_FazLoginUsuarioInterno (line 52)  │
│   validar_sessao()      ← Global_ValidaSessao (line 95)            │
├─────────────────────────────────────────────────────────────────────┤
│ DEVIATIONS DOCUMENTED:                                              │
│   Line 55: Password hashing (was plaintext)                        │
│   Line 78: Session storage (was global variable)                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Output Formats

### Default: Box Format
Human-readable box format shown in examples above.

### JSON Format (for tooling)
```bash
/wxcode:trace PAGE_Login --json
```

```json
{
  "element": "PAGE_Login",
  "type": "page",
  "status": "converted",
  "files": {
    "route": {"path": "app/routes/auth.py", "lines": [45, 89]},
    "template": {"path": "app/templates/login.html"},
    "tests": {"path": "tests/test_auth.py", "lines": [12, 67]}
  },
  "controls": [
    {"legacy": "EDT_Usuario", "converted": "input[name='usuario']", "file": "login.html", "line": 15}
  ],
  "procedures": [
    {"legacy": "Global_FazLoginUsuarioInterno", "converted": "fazer_login_interno", "file": "auth.py", "line": 52}
  ],
  "deviations": [
    {"description": "Password now hashed with bcrypt", "reason": "security"}
  ]
}
```

## Success Criteria

- [ ] Correctly identifies direction (legacy→converted or converted→legacy)
- [ ] Shows all converted files for legacy element
- [ ] Shows all legacy origins for converted file
- [ ] Displays control mappings with file:line references
- [ ] Displays procedure mappings with file:line references
- [ ] Lists deviations from legacy behavior
- [ ] Handles not-found gracefully with helpful suggestions
- [ ] Works without MCP (falls back to grep-only mode)
