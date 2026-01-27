# MCP Tools Usage Guide

Reference for using the 19 MCP tools available from WXCODE Conversor.

## Tool Categories

| Category | Count | Purpose |
|----------|-------|---------|
| KB Read | 9 | Read legacy code from MongoDB |
| Neo4j Analysis | 6 | Analyze dependency graph |
| Conversion | 4 | Track conversion progress |

---

## KB Read Tools (9)

### get_element

Returns full element data including code and AST.

**When to use:** Starting analysis of any element.

```
Input: element_name (string)
Output: {
  "name": "PAGE_Login",
  "type": "page",
  "raw_content": "// WLanguage code...",
  "ast": { ... },
  "properties": { ... }
}
```

**Key fields:**
- `raw_content` - Original WLanguage source code
- `ast` - Parsed abstract syntax tree (if available)
- `properties` - Element configuration

### get_controls

Returns UI control hierarchy with events and properties.

**When to use:** Understanding UI structure of pages/windows.

```
Input: element_name (string)
Output: {
  "controls": [
    {
      "name": "EDT_Usuario",
      "type": "edit",
      "properties": {
        "databinding": "USUARIO.LOGIN",
        "plane": 1
      },
      "events": {
        "exit": "ValidaUsuario()"
      },
      "children": []
    }
  ]
}
```

**Key fields:**
- `type` - Control type (edit, button, table, cell, etc.)
- `properties.databinding` - Data binding expression
- `properties.plane` - Plane number (for stacked views)
- `events` - Event handlers with code references

### get_procedures

Returns procedures related to an element.

**When to use:** Understanding business logic.

```
Input: element_name (string)
Output: {
  "local": [
    { "name": "ValidaForm", "code": "..." }
  ],
  "called": [
    { "name": "proc:ValidaCPF", "element_id": "..." }
  ]
}
```

**Key fields:**
- `local` - Procedures defined within the element
- `called` - External procedures this element calls

### get_schema

Returns database schema for tables used by element.

**When to use:** Understanding data layer requirements.

```
Input: element_name (string)
Output: {
  "tables": [
    {
      "name": "CLIENTE",
      "fields": [
        { "name": "ID", "type": "int", "primary": true },
        { "name": "NOME", "type": "string", "size": 100 }
      ],
      "indexes": [...],
      "connections": [...]
    }
  ]
}
```

### get_dependencies

Returns dependency graph for element.

**When to use:** Understanding conversion order and impacts.

```
Input: element_name (string)
Output: {
  "depends_on": [
    { "name": "proc:ValidaCPF", "type": "procedure" },
    { "name": "TABLE:USUARIO", "type": "table" }
  ],
  "depended_by": [
    { "name": "PAGE_Dashboard", "type": "page" }
  ]
}
```

**Important:** Check if `depends_on` items are already converted before planning.

### list_elements

Lists all elements in a project.

**When to use:** Getting overview of project scope.

```
Input: project_name (string), optional: type_filter
Output: {
  "elements": [
    { "name": "PAGE_Login", "type": "page" },
    { "name": "proc:ValidaCPF", "type": "procedure" }
  ]
}
```

### search_elements

Searches elements by name or content.

**When to use:** Finding specific functionality.

```
Input: query (string), optional: project_name
Output: {
  "matches": [...]
}
```

### get_project_stats

Returns statistics about a project.

**When to use:** Understanding project scope and complexity.

```
Input: project_name (string)
Output: {
  "total_elements": 150,
  "by_type": {
    "page": 45,
    "procedure": 80,
    "class": 15,
    "table": 10
  }
}
```

### list_projects

Lists all imported projects.

**When to use:** Finding available knowledge bases.

```
Output: {
  "projects": [
    { "name": "Linkpay_ADM", "elements": 150 }
  ]
}
```

---

## Neo4j Analysis Tools (6)

### analyze_impact

Analyzes what would be affected by changing an element.

**When to use:** Understanding ripple effects of changes.

```
Input: element_name (string), optional: depth
Output: {
  "direct_impact": [...],
  "indirect_impact": [...],
  "total_affected": 15
}
```

### find_paths

Finds paths between two elements in the dependency graph.

**When to use:** Understanding how elements connect.

```
Input: from_element (string), to_element (string)
Output: {
  "paths": [
    ["PAGE_Login", "proc:ValidaLogin", "TABLE:USUARIO"]
  ]
}
```

### find_hubs

Finds elements with many connections (critical elements).

**When to use:** Identifying core components to convert carefully.

```
Input: optional: min_connections
Output: {
  "hubs": [
    { "name": "proc:ValidaCPF", "connections": 45 }
  ]
}
```

### find_dead_code

Finds elements that nothing depends on.

**When to use:** Identifying potentially unused code.

```
Output: {
  "dead_code": [...]
}
```

### detect_cycles

Finds circular dependencies.

**When to use:** Identifying complex dependency patterns.

```
Output: {
  "cycles": [
    ["proc:A", "proc:B", "proc:A"]
  ]
}
```

### get_subgraph

Gets a subgraph around an element.

**When to use:** Visualizing local dependency context.

```
Input: element_name (string), depth (int)
Output: {
  "nodes": [...],
  "edges": [...]
}
```

---

## Conversion Tools (4)

### get_next_element

Returns the next element to convert (topological order).

**When to use:** Determining what to convert next.

```
Input: project_name (string)
Output: {
  "next": "proc:ValidaCPF",
  "reason": "No unconverted dependencies",
  "pending_dependencies": []
}
```

### get_conversion_stats

Returns conversion progress statistics.

**When to use:** Tracking overall progress.

```
Input: project_name (string)
Output: {
  "total": 150,
  "converted": 45,
  "pending": 105,
  "percentage": 30
}
```

### mark_converted

Marks an element as successfully converted.

**When to use:** After completing conversion of an element.

```
Input: element_name (string), optional: commit_hash, notes
Output: {
  "success": true
}
```

### get_conversion_context

Returns current conversion state and context.

**When to use:** Loading conversion context at session start.

```
Input: project_name (string)
Output: {
  "current_element": "PAGE_Login",
  "converted": ["proc:ValidaCPF", "TABLE:USUARIO"],
  "pending": [...],
  "output_project": {
    "stack_id": "fastapi-jinja2",
    "language": "python"
  }
}
```

---

## Usage Patterns

### Starting a New Element

```
1. get_conversion_context     → Current state
2. get_element {name}         → Full element data
3. get_controls {name}        → UI structure
4. get_procedures {name}      → Business logic
5. get_schema {name}          → Data requirements
6. get_dependencies {name}    → Prerequisites
```

### Before Planning

```
1. Check depends_on from get_dependencies
2. For each dependency:
   - Is it in "converted" list? → Can import
   - Is it in "pending" list? → May need to convert first
```

### After Conversion

```
1. mark_converted {element_name}
2. Commit changes with reference to element
```

---

## Error Handling

MCP tools may return errors if:
- Element not found
- Project not imported
- Neo4j not available (for analysis tools)

Always handle gracefully and inform user if data is unavailable.
