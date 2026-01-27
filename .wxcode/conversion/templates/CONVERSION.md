# Conversion Project Context

This file identifies this as a **conversion project** from WinDev/WebDev legacy code.
Its presence triggers conversion-aware behavior in WXCODE/GSD commands.

---

## Source Project

| Property | Value |
|----------|-------|
| **Project Name** | `{PROJECT_NAME}` |
| **Source Type** | WinDev / WebDev / WinDev Mobile |
| **MongoDB Collection** | elements |
| **MCP Available** | Yes |

## Target Stack

| Property | Value |
|----------|-------|
| **Output Project ID** | `{OUTPUT_PROJECT_ID}` |
| **Stack ID** | `{STACK_ID}` |
| **Language** | `{LANGUAGE}` |
| **Framework** | `{FRAMEWORK}` |
| **Template Engine** | `{TEMPLATE_ENGINE}` |
| **ORM** | `{ORM}` |

## Conversion Scope

### Elements in Scope

| Type | Count | Examples |
|------|-------|----------|
| Pages | {N} | PAGE_Login, PAGE_Dashboard |
| Windows | {N} | WIN_Cadastro |
| Procedures | {N} | proc:ValidaCPF |
| Classes | {N} | class:Cliente |
| Tables | {N} | TABLE:CLIENTE |

### Out of Scope

- {List elements explicitly excluded}

---

## Conversion State

| Metric | Value |
|--------|-------|
| **Total Elements** | {N} |
| **Converted** | {N} |
| **Pending** | {N} |
| **Current Element** | `{ELEMENT_NAME}` |
| **Progress** | {N}% |

### Recently Converted

| Element | Date | Phase | Commit |
|---------|------|-------|--------|
| proc:ValidaCPF | YYYY-MM-DD | 01 | abc123 |
| TABLE:USUARIO | YYYY-MM-DD | 01 | def456 |

---

## Project-Wide Decisions

These decisions apply to ALL elements unless overridden.

### Naming Convention

- [x] Use target stack conventions (snake_case for Python)
- [ ] Preserve legacy names (adapted to valid identifiers)
- [ ] Hybrid (ask per element)

**Details:**
- Variables: `gnUsuarioID` → `usuario_id` or `current_user.id`
- Functions: `ValidaCPF` → `validar_cpf()`
- Classes: `class:Cliente` → `Cliente`
- Files: `PAGE_Login` → `login.py`, `login.html`

### Structure Preservation

- [x] Maintain similar organization to legacy
- [ ] Full modernization (ignore legacy structure)

**Details:**
- Keep similar file groupings
- Preserve module/package boundaries
- Similar function/method organization

### Global Variables Handling

- [ ] Keep g_ prefix style
- [x] Convert to proper patterns

**Pattern:**
- Session-scoped: `gnUsuarioID` → `session['usuario_id']`
- Request-scoped: Use dependency injection
- Constants: Move to config

### Planes Default Strategy

When element has planes, default approach:

- [ ] Tabs (all content loaded, CSS switching)
- [x] Wizard (multi-step form component)
- [ ] Separate routes (one URL per plane)
- [ ] Ask per element

**Can be overridden per element in phase CONTEXT.md**

### Validation Logic

- [x] Preserve exact legacy logic
- [ ] Use modern libraries (but verify equivalence)

**Details:**
- CPF/CNPJ: Preserve digit validation algorithm
- Email: Can use library
- Custom rules: Preserve exactly

### Error Messages

- [x] Keep Portuguese messages
- [ ] Translate to English
- [ ] Use i18n keys

### Database Operations

- [x] Map H* functions to ORM equivalents
- [ ] Use raw SQL where complex

**Mapping:**
- HReadSeek → `query().filter_by()`
- HAdd → `db.add()`
- HModify → `db.commit()`
- HDelete → `db.delete()`

---

## Conversion Order

Based on dependency analysis:

### Layer 1: Schema (No Dependencies)
- [ ] TABLE:USUARIO
- [ ] TABLE:CLIENTE
- [ ] TABLE:PRODUTO

### Layer 2: Domain (Depends on Schema)
- [ ] class:Usuario
- [ ] class:Cliente

### Layer 3: Services (Depends on Domain)
- [ ] proc:ValidaCPF
- [ ] proc:ValidaLogin
- [ ] proc:CalculaDesconto

### Layer 4: UI (Depends on Services)
- [ ] PAGE_Login
- [ ] PAGE_Dashboard
- [ ] PAGE_Clientes

---

## Notes

### Known Issues
- {List any known issues or concerns}

### Special Handling Required
- {Elements that need special attention}

### External Dependencies
- {Third-party integrations, APIs, etc.}

---

## References

- **MCP Tools:** See `.wxcode/conversion/mcp-usage.md`
- **Planes Detection:** See `.wxcode/conversion/planes-detection.md`
- **Structure Guidelines:** See `.wxcode/conversion/structure-preservation.md`
- **Injection Points:** See `.wxcode/conversion/injection-points.md`

---

*This file is created by `/wxcode:new-project` when conversion context is detected.*
*Update `Current Element` and `Recently Converted` as work progresses.*
