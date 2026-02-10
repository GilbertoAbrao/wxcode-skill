# WXCODE

**WXCODE** is an AI-powered toolkit for **WinDev/WebDev code conversion projects**, built for Claude Code, OpenCode, and Gemini.

**Current Version:** 2.2.3

---

## Table of Contents

- [Installation](#installation)
- [How It Works](#how-it-works)
- [Supported Target Stacks](#supported-target-stacks)
- [MCP Integration](#mcp-integration)
- [Extension Agents](#extension-agents)
- [Planes Detection](#planes-detection)
- [Structure Preservation](#structure-preservation)
- [Commands](#commands)
- [File Structure](#file-structure)
- [Version History](#version-history)

---

## Installation

**From GitHub (recommended):**
```bash
npx github:GilbertoAbrao/wxcode-skill#main --claude --global
```

**From local clone:**
```bash
git clone https://github.com/GilbertoAbrao/wxcode-skill.git
cd wxcode-skill
node bin/install.js --claude --global
```

Verify with `/wxcode:help` inside Claude Code.

### Updating

```bash
npm cache clean --force && rm -rf ~/.npm/_npx && npx github:GilbertoAbrao/wxcode-skill#main --claude --global
```

Or use `/wxcode:update` inside Claude Code (handles cache automatically).

---

## How It Works

WXCODE converts legacy WinDev/WebDev applications to modern stacks through a structured workflow:

### 1. Initialize Project

```
/wxcode:new-project /path/to/CONTEXT.md
```

Creates the **complete project foundation**:
- Directory structure (per target stack)
- Configuration files (pyproject.toml, package.json, etc.)
- Application entry point and `start-dev.sh`
- Database models (all at once or on-demand)
- Design system tokens (DTCG format)
- Planning documents and `.planning/CONVERSION.md`

### 2. Convert Elements via Milestones

```
/wxcode:new-milestone --element=PAGE_Login --output-project=<id>
```

Each milestone converts one WinDev/WebDev element:
1. Queries Knowledge Base for source code (MCP is Source of Truth)
2. Plans conversion phases with research and verification
3. Converts to target stack
4. Integrates with existing foundation

### 3. Plan, Execute, Verify

```
/wxcode:plan-phase 1       # Research + plan + verify
/wxcode:execute-phase 1    # Execute with parallel agents
/wxcode:verify-work 1      # Confirm conversion works
```

Each phase uses fresh context windows. Parallel execution where possible. Atomic git commits per task.

### Core Principle

> **CONTEXT.md is a snapshot. MCP is the Source of Truth.**
> Always consult MCP for current data, use CONTEXT.md for initial context only.

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

## MCP Integration

WXCODE workflows use **29 MCP tools** to access legacy code stored in MongoDB/Neo4j.

| Category | Tools | Description |
|----------|-------|-------------|
| **Elements** | `get_element`, `list_elements`, `search_code` | Access WinDev source code |
| **Controls** | `get_controls`, `get_data_bindings` | UI hierarchy and bindings |
| **Procedures** | `get_procedures`, `get_procedure` | Global and local procedures |
| **Schema** | `get_schema`, `get_table` | Database schema |
| **Graph** | `get_dependencies`, `get_impact`, `get_path`, `find_hubs`, `find_dead_code`, `find_cycles` | Dependency analysis (Neo4j) |
| **Conversion** | `get_conversion_candidates`, `get_topological_order`, `get_conversion_stats`, `mark_converted`, `mark_project_initialized` | Conversion workflow |
| **Comprehension** | `get_business_rules` | Business rules and explanations |
| **Semantic Search** | `semantic_search`, `find_similar_by_embedding` | Natural language and vector search |
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

### wxcode-schema-generator

**Purpose:** Generates ORM models from legacy schema via MCP.

**Capabilities:**
- Preserves exact table/column names for transparent legacy database access
- Supports SQLAlchemy, Prisma, TypeORM, Django, Sequelize
- Validates generated models against legacy schema

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

## Commands

### Core Workflow

| Command | What it does |
|---------|--------------|
| `/wxcode:new-project` | Initialize project: questioning, research, requirements, roadmap |
| `/wxcode:new-milestone` | Start element conversion: context, phases, roadmap |
| `/wxcode:plan-phase [N]` | Research + plan + verify for a phase |
| `/wxcode:execute-phase [N]` | Execute plans in parallel waves |
| `/wxcode:verify-work [N]` | Validate converted features |
| `/wxcode:complete-milestone` | Archive milestone, tag release |

### Navigation

| Command | What it does |
|---------|--------------|
| `/wxcode:progress` | Where am I? What's next? |
| `/wxcode:help` | Show all commands |
| `/wxcode:version` | Display current version |
| `/wxcode:update` | Update WXCODE with changelog preview |

### Phase Management

| Command | What it does |
|---------|--------------|
| `/wxcode:discuss-phase [N]` | Gather context before planning |
| `/wxcode:add-phase` | Append phase to roadmap |
| `/wxcode:insert-phase [N]` | Insert urgent work between phases |
| `/wxcode:remove-phase [N]` | Remove future phase, renumber |

### Utilities

| Command | What it does |
|---------|--------------|
| `/wxcode:settings` | Configure workflow toggles and model profile |
| `/wxcode:dashboard` | Generate project dashboard JSON |
| `/wxcode:design-system` | Create or update design tokens |
| `/wxcode:validate-schema` | Validate models against legacy schema |
| `/wxcode:trace` | Navigate between legacy and converted code |
| `/wxcode:debug` | Systematic debugging with persistent state |

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
│   └── conversion/                # Conversion extension
│       ├── context-md-spec.md
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
├── README.md                      # This file
├── CLAUDE.md                      # Development context
├── CHANGELOG-WXCODE.md            # WXCODE changelog
├── package.json                   # Version
└── VERSION                        # Version
```

---

## Version History

See [CHANGELOG-WXCODE.md](CHANGELOG-WXCODE.md) for full version history.

---

## License

MIT License.

---

## Links

- [WXCODE Repository](https://github.com/GilbertoAbrao/wxcode-skill)
- [Discord](https://discord.gg/5JJgD5svVS)
