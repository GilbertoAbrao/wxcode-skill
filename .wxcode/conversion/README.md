# WXCODE Conversion Context

This extension layer specializes WXCODE/GSD for **WinDev/WebDev code conversion projects**.

## Key Differences from Standard GSD

| Standard GSD | Conversion Mode |
|--------------|-----------------|
| Greenfield project | Converting existing code |
| Requirements from user | Requirements from legacy code |
| Design decisions fresh | Design decisions from legacy + user adjustments |
| No external data source | MongoDB via MCP is source of truth |

## Core Principles

### 1. Legacy is Source of Truth

The legacy code in MongoDB (accessible via MCP) defines:
- What fields forms should have
- What validation rules exist
- What database operations are needed
- What the UI structure looks like

### 2. Consult Before Asking

Before asking the user ANY question:
1. Check if the answer exists in legacy code
2. Check if similar element was already converted
3. Only ask about NEW decisions or ambiguous mappings

### 3. Preserve Structure

Generated code should feel **familiar** to legacy users:
- Similar naming conventions (adjusted for target stack)
- Similar file organization
- Similar logic flow

### 4. Respect Dependencies

Elements have dependencies (via Neo4j graph):
- Convert dependencies first
- Reuse already-converted code (don't recreate)
- Understand impact of changes

## Workflow Adaptations

### Before Planning or Research

```
1. MCP: get_element → Understand what we're converting
2. MCP: get_controls → Map UI elements
3. MCP: get_procedures → Understand business logic
4. MCP: get_dependencies → Know prerequisites
5. MCP: get_conversion_context → Check already converted
```

### Before Asking User Questions

```
1. Check legacy code for existing answer
2. Check similar converted elements for patterns
3. Rephrase question with legacy context:
   - DON'T: "What fields should the form have?"
   - DO: "Legacy has EDT_Usuario and EDT_Senha. Keep or rename?"
```

### During Execution

```
1. Reference legacy code for implementation details
2. Import already-converted dependencies (don't recreate)
3. Follow structure-preservation guidelines
4. Mark element as converted when done
```

## Reference Files

| File | Purpose |
|------|---------|
| [mcp-usage.md](mcp-usage.md) | How to use the 19 MCP tools |
| [planes-detection.md](planes-detection.md) | How to identify planes in WinDev code |
| [structure-preservation.md](structure-preservation.md) | Guidelines for familiar code generation |
| [injection-points.md](injection-points.md) | Where to inject conversion logic |

## MCP Tools Available

**KB Read (9):** get_element, list_elements, search_elements, get_controls, get_procedures, get_schema, get_dependencies, get_project_stats, list_projects

**Neo4j Analysis (6):** analyze_impact, find_paths, find_hubs, find_dead_code, detect_cycles, get_subgraph

**Conversion (4):** get_next_element, get_conversion_stats, mark_converted, get_conversion_context

## Extension Agents

| Agent | Purpose |
|-------|---------|
| wxcode-legacy-analyzer | Analyzes legacy code via MCP |
| wxcode-conversion-advisor | Advises on conversion decisions |

---
*This extension layer is isolated from upstream GSD merges.*
