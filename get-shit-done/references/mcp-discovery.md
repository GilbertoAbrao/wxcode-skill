# MCP Tool Discovery for Conversion Projects

This reference explains how agents should discover and use MCP tools for WinDev/WebDev conversion projects.

## Why Dynamic Discovery?

The MCP wxcode-kb server evolves rapidly. New tools are added frequently. Instead of hardcoding tool lists, agents should:

1. **Check if conversion project** — Look for `.planning/CONVERSION.md`
2. **Verify MCP availability** — Call `mcp__wxcode-kb__health_check`
3. **Discover available tools** — Tools prefixed with `mcp__wxcode-kb__` are available

## When to Use MCP

**Use MCP when ALL of these are true:**
- `.planning/CONVERSION.md` exists (this is a conversion project)
- You need information about the legacy WinDev/WebDev code
- The information isn't already in CONTEXT.md or phase files

**Skip MCP when:**
- Not a conversion project (no CONVERSION.md)
- Working on pure target stack code (no legacy context needed)
- Information already available in existing files

## Tool Categories

MCP tools are organized by category. Discover what's available by looking at tool names:

| Prefix Pattern | Purpose |
|----------------|---------|
| `get_element*` | Retrieve WinDev source code |
| `get_controls*` | UI hierarchy and properties |
| `get_procedure*` | Procedures (global and local) |
| `get_schema*`, `get_table*` | Database schema |
| `get_dependencies*`, `get_impact*` | Dependency analysis |
| `get_conversion*`, `mark_*` | Conversion workflow |
| `search_*` | Code and similarity search |
| `list_*` | List available elements |
| `get_wlanguage*` | WLanguage reference |
| `get_element_planes*` | Tab/wizard detection |

## Common Workflows

### Before Planning an Element

```
1. get_element {name}           → Full source code
2. get_controls {name}          → UI structure
3. get_element_planes {name}    → Detect tabs/wizard
4. get_procedures {name}        → Business logic
5. get_dependencies {name}      → What it depends on
6. search_converted_similar     → Learn from similar conversions
```

### Before Executing Conversion

```
1. get_element {name}           → Current source
2. get_data_bindings {name}     → Field mappings
3. get_dependencies {name}      → Prerequisites
```

### After Completing Conversion

```
1. mark_converted {name}        → Update conversion state
```

## Integration Pattern

Agents should include this check at the start of their workflow:

```markdown
## Check Conversion Context

**If `.planning/CONVERSION.md` exists:**

This is a conversion project. Before researching/planning/executing:

1. Check what legacy context is needed
2. Use MCP tools to retrieve legacy code/structure
3. Document legacy findings in output files

**MCP tools available:** All tools prefixed with `mcp__wxcode-kb__`

Call `mcp__wxcode-kb__health_check` to verify connectivity.
```

## Key Principles

1. **CONTEXT.md is snapshot, MCP is Source of Truth** — Always prefer MCP for current data
2. **Discover, don't assume** — Tool names may change, new tools may be added
3. **Check availability first** — Use `health_check` before depending on MCP
4. **Document what you found** — Include legacy analysis in RESEARCH.md or PLAN.md
