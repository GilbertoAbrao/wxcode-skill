# WXCODE

**WXCODE** is a customized fork of [GSD (Get Shit Done)](https://github.com/glittercowboy/get-shit-done) specialized for **WinDev/WebDev code conversion projects**.

Based on GSD v1.9.13 | [Upstream Repository](https://github.com/glittercowboy/get-shit-done)

---

## Table of Contents

- [Installation](#installation)
- [Branch Structure](#branch-structure)
- [What Changed from GSD](#what-changed-from-gsd)
- [Conversion Extension Layer](#conversion-extension-layer)
- [MCP Integration](#mcp-integration)
- [Extension Agents](#extension-agents)
- [Planes Detection](#planes-detection)
- [Structure Preservation](#structure-preservation)
- [Fork Management](#fork-management)
- [File Structure](#file-structure)
- [Version History](#version-history)

---

## Installation

**From GitHub (recommended):**
```bash
npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global
```

**From local clone:**
```bash
git clone https://github.com/GilbertoAbrao/get-shit-done.git
cd get-shit-done
git checkout main-wxcode
node bin/install.js --claude --global
```

Verify with `/wxcode:help` inside Claude Code.

### Updating

```bash
npx github:GilbertoAbrao/get-shit-done#main-wxcode@latest --claude --global
```

Or use `/wxcode:update` inside Claude Code.

---

## Branch Structure

| Branch | Tracks | Purpose |
|--------|--------|---------|
| `main` | `upstream/main` | Mirror of original GSD repository |
| `main-wxcode` | `origin/main-wxcode` | WXCODE customizations (work here) |

**Syncing workflow:**
```bash
git checkout main && git pull          # Update from upstream
git checkout main-wxcode && git merge main  # Merge to wxcode
```

Or use `/wxcode:sync` for automated sync with transformations.

---

## What Changed from GSD

### Basic Transformations

| GSD | WXCODE |
|-----|--------|
| Commands `gsd:*` | Commands `wxcode:*` |
| Agents `gsd-*` | Agents `wxcode-*` |
| Hooks `gsd-*` | Hooks `wxcode-*` |
| Display name "GSD" | Display name "WXCODE" |

### Fork Management (New Commands)

| Command | Description |
|---------|-------------|
| `/wxcode:init` | Initialize fork management |
| `/wxcode:sync` | Synchronize with upstream GSD |
| `/wxcode:status` | Show current sync state |
| `/wxcode:diff` | Compare local vs upstream |
| `/wxcode:history` | View sync and customization history |
| `/wxcode:customize` | Customize a specific command |
| `/wxcode:discuss` | Explore new features |
| `/wxcode:override` | Mark files to ignore during sync |
| `/wxcode:rollback` | Revert last sync |

### Conversion Extension Layer (New)

WXCODE extends GSD with specialized support for WinDev/WebDev code conversion.
See [Conversion Extension Layer](#conversion-extension-layer) for details.

---

## Conversion Extension Layer

WXCODE is specialized for converting legacy WinDev/WebDev applications to modern stacks.
This extension layer teaches the GSD workflow how to:

1. **Consult legacy code** before planning or asking questions
2. **Use MCP tools** to access the source code in MongoDB
3. **Detect planes** (stacked views) in WinDev pages
4. **Preserve structure** familiar to legacy users
5. **Avoid redundant questions** when answers exist in legacy

### Core Principle

> The MongoDB (via MCP Server) is the **source of truth** for legacy code.
> Always consult it before planning, researching, or asking the user.

### When is Conversion Mode Active?

Conversion-aware behavior is triggered when:
- `.planning/CONVERSION.md` exists in the project
- MCP tools are available
- User mentions "convert", "WinDev", "WebDev", "legacy"

### Workflow Adaptations

| Standard GSD | Conversion Mode |
|--------------|-----------------|
| Greenfield project | Converting existing code |
| Requirements from user | Requirements from legacy + user adjustments |
| Design decisions fresh | Design decisions from legacy context |
| Ask all questions | Only ask NEW decisions (check legacy first) |

### Configuration Files

Located in `.wxcode/conversion/`:

| File | Purpose |
|------|---------|
| `README.md` | Overview of conversion context |
| `mcp-usage.md` | Guide for using the 19 MCP tools |
| `planes-detection.md` | How to identify planes in WinDev code |
| `structure-preservation.md` | Guidelines for familiar code generation |
| `injection-points.md` | Where to inject conversion logic in commands |
| `templates/CONVERSION.md` | Template for project conversion context |

---

## MCP Integration

WXCODE workflows use **19 MCP tools** from the WXCODE Conversor to access legacy code.

### KB Read Tools (9)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `get_element` | Full element data (code, AST) | Starting any element analysis |
| `get_controls` | UI control hierarchy | Understanding page/window structure |
| `get_procedures` | Related procedures | Understanding business logic |
| `get_schema` | Database schema | Understanding data requirements |
| `get_dependencies` | Dependency graph | Understanding conversion order |
| `list_elements` | List all elements | Getting project overview |
| `search_elements` | Search by name/content | Finding specific functionality |
| `get_project_stats` | Project statistics | Understanding scope |
| `list_projects` | List projects | Finding available KBs |

### Neo4j Analysis Tools (6)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `analyze_impact` | What's affected by changes | Understanding ripple effects |
| `find_paths` | Paths between elements | Understanding connections |
| `find_hubs` | Critical elements | Identifying core components |
| `find_dead_code` | Unused elements | Cleanup candidates |
| `detect_cycles` | Circular dependencies | Handling complex patterns |
| `get_subgraph` | Local dependency context | Visualizing relationships |

### Conversion Tools (4)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `get_next_element` | Next element to convert | Determining conversion order |
| `get_conversion_stats` | Conversion progress | Tracking overall progress |
| `mark_converted` | Mark as converted | After successful conversion |
| `get_conversion_context` | Current conversion state | Loading context |

### Usage Pattern

```
Before planning any element:
1. get_element {name}         → Full code
2. get_controls {name}        → UI structure
3. get_procedures {name}      → Business logic
4. get_dependencies {name}    → Prerequisites
5. get_conversion_context     → What's already converted
```

See `.wxcode/conversion/mcp-usage.md` for complete documentation.

---

## Extension Agents

WXCODE adds specialized agents for conversion workflows.

### wxcode-legacy-analyzer

**Purpose:** Analyzes legacy WinDev code via MCP and produces structured documentation.

**Capabilities:**
- Retrieves element data via MCP tools
- Identifies planes in pages/windows
- Maps UI control hierarchy
- Documents business logic from procedures
- Analyzes database operations
- Categorizes dependencies (converted vs pending)

**Output:** Writes to `{phase}-LEGACY.md` or RESEARCH.md "Legacy Analysis" section.

**MCP Tools Used:**
- `get_element`, `get_controls`, `get_procedures`
- `get_schema`, `get_dependencies`, `analyze_impact`
- `get_conversion_context`

### wxcode-conversion-advisor

**Purpose:** Advises on conversion decisions and reformulates questions with legacy context.

**Capabilities:**
- Checks if answer exists in legacy (don't ask redundant questions)
- Reframes generic questions with legacy context
- Suggests defaults based on patterns
- Ensures consistency with previous decisions

**Example:**
```
Generic question: "What fields should the form have?"
Legacy shows: EDT_Usuario, EDT_Senha, CHK_Lembrar

Reframed: "Legacy has Usuario, Senha, and 'Lembrar' checkbox.
          Keep these or modify?"
```

---

## Planes Detection

WinDev pages/windows can have **planes** (stacked views where only one is visible).

### What Are Planes?

```
┌─────────────────────────────┐
│        PAGE_Cadastro        │
├─────────────────────────────┤
│ Plane 1: Dados Pessoais  ◄──┼── Visible
│ Plane 2: Documentos      ◄──┼── Hidden
│ Plane 3: Confirmacao     ◄──┼── Hidden
└─────────────────────────────┘
```

Common uses: Wizard steps, tab-like interfaces, conditional views.

### How to Detect

Since there's no MCP tool for planes, analyze the code:

**In `get_controls` response:**
```json
{ "name": "EDT_Nome", "properties": { "plane": 1 } }
```

**In `raw_content` (WLanguage):**
```wlanguage
Plane(2)                    // Show plane 2
EDT_Nome..Plane = 1         // Assign control to plane
PlaneEnable(1, True)        // Enable/disable plane
```

**Navigation patterns:**
```wlanguage
BTN_Proximo..Click:
  Plane(Plane() + 1)        // Next plane (wizard)

TAB_Dados..Click:
  Plane(1)                  // Direct navigation (tabs)
```

### Conversion Strategies

| Pattern | Strategy | Target |
|---------|----------|--------|
| Wizard (sequential) | Multi-step form | All stacks |
| Tabs (direct access) | Tab component | All stacks |
| Conditional | State-based rendering | SPA stacks |
| Complex | Separate routes | MPA stacks |

See `.wxcode/conversion/planes-detection.md` for complete documentation.

---

## Structure Preservation

Generate code that feels **familiar** to legacy users.

### Naming Conventions

| Legacy | Converted | Rule |
|--------|-----------|------|
| `PAGE_Login` | `login.py`, `login.html` | Keep semantic name |
| `proc:ValidaCPF` | `validar_cpf()` | Portuguese verb → infinitive |
| `EDT_Usuario` | `username` or `usuario` | Ask user preference |
| `gnUsuarioID` | `usuario_id` | Remove Hungarian prefix |
| `class:Cliente` | `Cliente` | Keep class name |

### Code Organization

```
Legacy:                      Converted:
├── Procedures/              ├── services/
│   └── ValidaCPF           │   └── validation.py::validar_cpf()
├── Classes/                 ├── domain/
│   └── Cliente             │   └── cliente.py::Cliente
└── Pages/                   ├── routes/
    └── PAGE_Login          │   └── auth.py::login()
                             └── templates/
                                 └── login.html
```

### When to Deviate

- **Security:** SQL injection → parameterized queries
- **Performance:** N+1 queries → JOINs
- **Anti-patterns:** Global state → proper patterns

Document deviations in SUMMARY.md.

See `.wxcode/conversion/structure-preservation.md` for complete documentation.

---

## Fork Management

### Configuration Files (`.wxcode/`)

| File | Purpose |
|------|---------|
| `config.md` | WXCODE identity and settings |
| `transform-rules.md` | GSD → WXCODE transformation rules |
| `upstream-state.md` | Sync state tracking |
| `customizations.md` | Decision history |
| `overrides.md` | Files to skip during sync |
| `decisions/` | Per-command customization records |

### Sync Commands

| Command | Description |
|---------|-------------|
| `/wxcode:sync` | Synchronize with upstream GSD |
| `/wxcode:status` | Show current sync state |
| `/wxcode:diff` | Compare local vs upstream |
| `/wxcode:rollback` | Revert last sync |
| `/wxcode:history` | View sync history |

### Customization Commands

| Command | Description |
|---------|-------------|
| `/wxcode:customize <cmd>` | Customize specific command |
| `/wxcode:discuss` | Explore new features |
| `/wxcode:override <file>` | Mark file to ignore in sync |

---

## File Structure

```
get-shit-done/
├── commands/
│   └── wxcode/                    # GSD commands (renamed)
│       ├── new-project.md
│       ├── plan-phase.md
│       ├── execute-phase.md
│       └── ...
│
├── agents/
│   ├── wxcode-*.md                # GSD agents (renamed)
│   ├── wxcode-legacy-analyzer.md  # NEW: Conversion extension
│   └── wxcode-conversion-advisor.md # NEW: Conversion extension
│
├── .wxcode/
│   ├── config.md                  # Fork identity
│   ├── transform-rules.md         # Transformation rules
│   ├── upstream-state.md          # Sync state
│   ├── customizations.md          # Decision history
│   ├── overrides.md               # Ignored files
│   ├── decisions/                 # Per-command decisions
│   │
│   └── conversion/                # NEW: Conversion extension
│       ├── README.md              # Overview
│       ├── mcp-usage.md           # MCP tools guide
│       ├── planes-detection.md    # Planes identification
│       ├── structure-preservation.md # Code structure guidelines
│       ├── injection-points.md    # Command injection points
│       └── templates/
│           └── CONVERSION.md      # Project template
│
├── get-shit-done/                 # Reference documentation
├── hooks/                         # Git hooks
├── bin/                           # Installer
│
├── README.md                      # Original GSD README
├── README-WXCODE.md               # This file
├── CHANGELOG.md                   # GSD changelog
└── CHANGELOG-WXCODE.md            # WXCODE changelog
```

### Project Structure (When Using Conversion)

```
your-project/
└── .planning/
    ├── PROJECT.md                 # Standard GSD
    ├── REQUIREMENTS.md            # Standard GSD
    ├── ROADMAP.md                 # Standard GSD
    ├── STATE.md                   # Standard GSD
    ├── config.json                # Standard GSD
    │
    ├── CONVERSION.md              # NEW: Conversion context
    │
    ├── phases/
    │   └── 01-page-login/
    │       ├── 01-RESEARCH.md     # Includes "Legacy Analysis"
    │       ├── 01-CONTEXT.md      # Includes conversion decisions
    │       ├── 01-01-PLAN.md      # Includes conversion_context
    │       └── 01-01-SUMMARY.md
    │
    └── conversion/                # NEW: Conversion-specific
        ├── state.md               # Local conversion state
        └── decisions.md           # Mapping decisions
```

---

## Injection Points

How standard GSD commands are extended for conversion:

### `/wxcode:discuss-phase`

**Before asking questions:**
1. Load element via MCP (`get_element`, `get_controls`)
2. Check if answer exists in legacy
3. Reframe questions with context

### `/wxcode:research-phase`

**Added phase before stack research:**
1. Spawn `wxcode-legacy-analyzer`
2. Document legacy analysis in RESEARCH.md
3. Continue with standard research

### `/wxcode:plan-phase`

**Plans include conversion context:**
```xml
<conversion_context>
  <legacy_element>PAGE_Login</legacy_element>
  <dependencies_converted>proc:ValidaCPF</dependencies_converted>
  <structure_approach>preserve</structure_approach>
</conversion_context>
```

### `/wxcode:execute-phase`

**Post-execution:**
```
MCP: mark_converted {element_name}
```

See `.wxcode/conversion/injection-points.md` for complete documentation.

---

## Version History

See [CHANGELOG-WXCODE.md](CHANGELOG-WXCODE.md) for full version history.

### Current Version

- **WXCODE:** 1.0.0
- **Based on GSD:** 1.9.13
- **Upstream Commit:** 3d2a960

---

## License

MIT License - Same as upstream GSD.

---

## Links

- [GSD Upstream Repository](https://github.com/glittercowboy/get-shit-done)
- [WXCODE Conversor](../wxk/wxcode) (separate project)
- [GSD Discord](https://discord.gg/5JJgD5svVS)
