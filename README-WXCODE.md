# WXCODE

**WXCODE** is an AI-powered toolkit for **WinDev/WebDev code conversion projects**, built for Claude Code, OpenCode, and Gemini.

---

## Table of Contents

- [Installation](#installation)
- [Conversion Extension Layer](#conversion-extension-layer)
- [MCP Integration](#mcp-integration)
- [Extension Agents](#extension-agents)
- [Planes Detection](#planes-detection)
- [Structure Preservation](#structure-preservation)
- [File Structure](#file-structure)
- [Version History](#version-history)

---

## Installation

**From GitHub (recommended):**
```bash
npx github:GilbertoAbrao/get-shit-done#main --claude --global
```

**From local clone:**
```bash
git clone https://github.com/GilbertoAbrao/get-shit-done.git
cd get-shit-done
git checkout main
node bin/install.js --claude --global
```

Verify with `/wxcode:help` inside Claude Code.

### Updating

```bash
npm cache clean --force && rm -rf ~/.npm/_npx && npx github:GilbertoAbrao/get-shit-done#main --claude --global
```

Or use `/wxcode:update` inside Claude Code (handles cache automatically).

---

## Conversion Extension Layer

WXCODE is specialized for converting legacy WinDev/WebDev applications to modern stacks.

1. **Consult legacy code** before planning or asking questions
2. **Use MCP tools** to access the source code in MongoDB
3. **Detect planes** (stacked views) in WinDev pages
4. **Preserve structure** familiar to legacy users
5. **Avoid redundant questions** when answers exist in legacy

### Core Principle

> The MongoDB (via MCP Server) is the **source of truth** for legacy code.
> Always consult it before planning, researching, or asking the user.

### Starting a Conversion Project

Use `/wxcode:new-project` with a CONTEXT.md file:

```bash
/wxcode:new-project /path/to/CONTEXT.md
```

This creates the **complete project foundation**:
- Directory structure (per target stack)
- Configuration files (pyproject.toml, package.json, etc.)
- Application entry point
- `start-dev.sh` script
- Database models (all at once or on-demand)
- All planning documents
- `.planning/CONVERSION.md` (activates conversion mode)

**CONTEXT.md** is a snapshot. **MCP is the Source of Truth** — always consulted for current data.

### When is Conversion Mode Active?

Conversion-aware behavior is triggered when:
- **CONTEXT.md passed to `/wxcode:new-project`** (initializes conversion project)
- `.planning/CONVERSION.md` exists in the project
- MCP tools are available
- User mentions "convert", "WinDev", "WebDev", "legacy"

### Configuration Files

Located in `.wxcode/conversion/`:

| File | Purpose |
|------|---------|
| `README.md` | Overview of conversion context |
| `context-md-spec.md` | Specification for CONTEXT.md format |
| `mcp-usage.md` | Guide for using the 25 MCP tools |
| `planes-detection.md` | How to identify planes in WinDev code |
| `structure-preservation.md` | Guidelines for familiar code generation |
| `injection-points.md` | Where to inject conversion logic in commands |
| `templates/CONVERSION.md` | Template for project conversion context |

---

## MCP Integration

WXCODE workflows use **25 MCP tools** to access legacy code.

| Category | Tools | Description |
|----------|-------|-------------|
| **Elements** | `get_element`, `list_elements`, `search_code` | Access WinDev source code |
| **Controls** | `get_controls`, `get_data_bindings` | UI hierarchy and bindings |
| **Procedures** | `get_procedures`, `get_procedure` | Global and local procedures |
| **Schema** | `get_schema`, `get_table` | Database schema |
| **Graph** | `get_dependencies`, `get_impact`, `get_path`, `find_hubs`, `find_dead_code`, `find_cycles` | Dependency analysis (Neo4j) |
| **Conversion** | `get_conversion_candidates`, `get_topological_order`, `get_conversion_stats`, `mark_converted`, `mark_project_initialized` | Conversion workflow |
| **Stack** | `get_stack_conventions` | Target stack conventions |
| **Planes** | `get_element_planes` | Tabs/wizard/views detection |
| **WLanguage** | `get_wlanguage_reference`, `list_wlanguage_functions`, `get_wlanguage_pattern` | H* function reference |
| **Similarity** | `search_converted_similar` | Find similar converted elements |
| **PDF** | `get_element_pdf_slice` | Documentation and screenshots |

### Usage Pattern

```
Before planning any element:
1. get_element {name}           -> Full code
2. get_controls {name}          -> UI structure
3. get_element_planes {name}    -> Detect tabs/wizard
4. get_procedures {name}        -> Business logic
5. get_dependencies {name}      -> Prerequisites
6. search_converted_similar     -> Learn from similar
```

See `.wxcode/conversion/mcp-usage.md` for complete documentation.

---

## Extension Agents

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

### wxcode-conversion-advisor

**Purpose:** Advises on conversion decisions and reformulates questions with legacy context.

**Capabilities:**
- Checks if answer exists in legacy (don't ask redundant questions)
- Reframes generic questions with legacy context
- Suggests defaults based on patterns
- Ensures consistency with previous decisions

---

## Planes Detection

WinDev pages/windows can have **planes** (stacked views where only one is visible).

### What Are Planes?

```
+---------------------------------+
|        PAGE_Cadastro            |
+---------------------------------+
| Plane 1: Dados Pessoais  <------ Visible
| Plane 2: Documentos      <------ Hidden
| Plane 3: Confirmacao     <------ Hidden
+---------------------------------+
```

Common uses: Wizard steps, tab-like interfaces, conditional views.

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
| `proc:ValidaCPF` | `validar_cpf()` | Portuguese verb -> infinitive |
| `EDT_Usuario` | `username` or `usuario` | Ask user preference |
| `gnUsuarioID` | `usuario_id` | Remove Hungarian prefix |
| `class:Cliente` | `Cliente` | Keep class name |

See `.wxcode/conversion/structure-preservation.md` for complete documentation.

---

## File Structure

```
wxcode/
├── commands/
│   └── wxcode/                    # WXCODE commands (39+)
│       ├── new-project.md
│       ├── plan-phase.md
│       ├── execute-phase.md
│       └── ...
│
├── agents/
│   ├── wxcode-*.md                # WXCODE agents
│   ├── wxcode-legacy-analyzer.md  # Conversion extension
│   └── wxcode-conversion-advisor.md # Conversion extension
│
├── .wxcode/
│   ├── config.md                  # WXCODE identity
│   ├── customizations.md          # Decision history
│   ├── overrides.md               # Files with special handling
│   ├── decisions/                 # Per-command decisions
│   │
│   └── conversion/                # Conversion extension
│       ├── README.md
│       ├── mcp-usage.md
│       ├── planes-detection.md
│       ├── structure-preservation.md
│       ├── injection-points.md
│       └── templates/
│           └── CONVERSION.md
│
├── wxcode-skill/                  # Reference documentation
│   ├── references/
│   ├── templates/
│   └── workflows/
│
├── hooks/                         # Hooks
├── bin/                           # Installer
│
├── README.md                      # Original upstream README
├── README-WXCODE.md               # This file
├── CHANGELOG.md                   # Upstream changelog
└── CHANGELOG-WXCODE.md            # WXCODE changelog
```

---

## Supported Target Stacks

15 stacks organized by rendering type:

### Server-Rendered
- `fastapi-jinja2`, `fastapi-htmx`
- `django-templates`
- `rails-erb`
- `laravel-blade`

### SPA (Backend + Frontend)
- `fastapi-react`, `fastapi-vue`
- `nestjs-react`, `nestjs-vue`
- `laravel-react`

### Fullstack (Single Node)
- `nextjs-app-router`, `nextjs-pages`
- `nuxt3`, `sveltekit`, `remix`

---

## Version History

See [CHANGELOG-WXCODE.md](CHANGELOG-WXCODE.md) for full version history.

### Current Version

- **WXCODE:** 2.0.1

---

## License

MIT License.

---

## Links

- [WXCODE Repository](https://github.com/GilbertoAbrao/get-shit-done)
- [Discord](https://discord.gg/5JJgD5svVS)
