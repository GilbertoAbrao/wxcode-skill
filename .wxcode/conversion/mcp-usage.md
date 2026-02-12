# MCP Tools Usage Guide

Reference for using the 28 MCP tools available from WXCODE Conversor.

## Tool Categories

| Category | Count | Purpose |
|----------|-------|---------|
| Elements | 3 | Access WinDev source code |
| Controls | 2 | UI control hierarchy and bindings |
| Procedures | 2 | Global and local procedures |
| Schema | 2 | Database schema |
| Graph | 6 | Dependency analysis (Neo4j) |
| Conversion | 5 | Conversion workflow |
| Stack | 1 | Target stack conventions |
| Planes | 1 | Tabs/wizard/views detection |
| WLanguage | 3 | H* function reference |
| Comprehension | 2 | Business rules and explanations |
| Semantic Search | 2 | Natural language and vector search |
| Similarity | 1 | Find similar converted elements |
| PDF | 1 | Documentation and screenshots |

---

## Elements (3)

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

### search_code

Searches elements by code content.

**When to use:** Finding specific functionality or patterns.

```
Input: query (string), optional: project_name
Output: {
  "matches": [...]
}
```

---

## Controls (2)

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

### get_data_bindings

Returns data bindings for controls in an element.

**When to use:** Understanding form-to-database mappings.

```
Input: element_name (string)
Output: {
  "bindings": [
    { "control": "EDT_Nome", "table": "CLIENTE", "field": "NOME" }
  ]
}
```

---

## Procedures (2)

### get_procedures

Returns all procedures related to an element.

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

### get_procedure

Returns a specific procedure by name.

**When to use:** Getting details of a specific procedure.

```
Input: procedure_name (string)
Output: {
  "name": "ValidaCPF",
  "code": "...",
  "parameters": [...],
  "returns": "boolean"
}
```

---

## Schema (2)

### get_schema

Returns full database schema.

**When to use:** Understanding complete data model.

```
Output: {
  "tables": [
    {
      "name": "CLIENTE",
      "fields": [...],
      "indexes": [...],
      "connections": [...]
    }
  ]
}
```

### get_table

Returns details of a specific table.

**When to use:** Understanding specific table structure.

```
Input: table_name (string)
Output: {
  "name": "CLIENTE",
  "fields": [
    { "name": "ID", "type": "int", "primary": true },
    { "name": "NOME", "type": "string", "size": 100 }
  ],
  "indexes": [...],
  "relations": [...]
}
```

---

## Graph - Neo4j Analysis (6)

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

### get_impact

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

### get_path

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

### find_cycles

Finds circular dependencies.

**When to use:** Identifying complex dependency patterns.

```
Output: {
  "cycles": [
    ["proc:A", "proc:B", "proc:A"]
  ]
}
```

---

## Conversion (5)

### get_conversion_candidates

Returns elements ready to convert (dependencies satisfied).

**When to use:** Determining what can be converted next.

```
Input: project_name (string)
Output: {
  "candidates": [
    { "name": "proc:ValidaCPF", "reason": "No dependencies" }
  ]
}
```

### get_topological_order

Returns elements in topological order for conversion.

**When to use:** Planning conversion sequence.

```
Input: project_name (string)
Output: {
  "order": [
    "TABLE:USUARIO",
    "proc:ValidaCPF",
    "PAGE_Login"
  ]
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

### mark_project_initialized

Marks output project as initialized.

**When to use:** After `/wxcode:new-project` creates foundation.

```
Output: {
  "success": true
}
```

---

## Stack (1)

### get_stack_conventions

Returns conventions for the target stack.

**When to use:** Ensuring generated code follows stack patterns.

```
Input: stack_id (string)
Output: {
  "naming": { ... },
  "file_structure": { ... },
  "patterns": { ... }
}
```

---

## Planes (1)

### get_element_planes

Detects planes (tabs/wizard/views) in an element.

**When to use:** Understanding stacked UI patterns.

```
Input: element_name (string)
Output: {
  "has_planes": true,
  "planes": [
    { "number": 1, "controls": ["EDT_Nome", "EDT_Email"] },
    { "number": 2, "controls": ["EDT_Endereco", "EDT_Cidade"] }
  ],
  "navigation_pattern": "wizard"
}
```

---

## WLanguage (3)

### get_wlanguage_reference

Returns reference for H* functions.

**When to use:** Understanding WLanguage database functions.

```
Input: function_name (string)
Output: {
  "name": "HReadSeek",
  "description": "...",
  "parameters": [...],
  "equivalent": "query().filter_by()"
}
```

### list_wlanguage_functions

Lists all WLanguage functions used in project.

**When to use:** Getting overview of functions to convert.

```
Input: project_name (string)
Output: {
  "functions": [
    { "name": "HReadSeek", "count": 45 },
    { "name": "HAdd", "count": 32 }
  ]
}
```

### get_wlanguage_pattern

Returns conversion pattern for a WLanguage construct.

**When to use:** Getting recommended conversion approach.

```
Input: pattern_name (string)
Output: {
  "wlanguage": "HReadSeek(...)",
  "python": "session.query(...).filter_by(...)",
  "notes": "..."
}
```

---

## Comprehension (2)

### get_business_rules

Returns business rules extracted from an element's procedures.

**When to use:** Understanding critical business logic that must be preserved during conversion.

```
Input: element_name (string), optional: project_name, category, text_filter
Output: {
  "rules": [
    {
      "id": "rule_001",
      "description": "CPF must be validated before save",
      "category": "validation",
      "confidence": 0.95,
      "source_procedure": "ValidaCPF",
      "source_element": "PAGE_Login"
    }
  ]
}
```

**Key fields:**
- `category` - Rule category (validation, calculation, workflow, access_control, etc.)
- `confidence` - Extraction confidence (0-1)
- `source_procedure` - Procedure where rule was found

---

## Semantic Search (2)

### semantic_search

Natural language search across the knowledge base with project scoping.

**When to use:** Finding elements by what they DO rather than what they're named.

```
Input: query (string), optional: project_name, type_filter, search_mode (hybrid|vector|fulltext)
Output: {
  "results": [
    {
      "name": "PAGE_Login",
      "type": "page",
      "score": 0.92,
      "snippet": "Handles user authentication with CPF validation..."
    }
  ]
}
```

**Search modes:**
- `hybrid` (default) - Combines vector similarity and full-text search
- `vector` - Pure semantic similarity
- `fulltext` - Traditional text matching

### find_similar_by_embedding

Find semantically similar elements using stored vector embeddings.

**When to use:** Finding elements with similar behavior or structure regardless of naming.

```
Input: element_name (string), optional: limit, type_filter
Output: {
  "similar": [
    {
      "name": "PAGE_LoginMobile",
      "type": "page",
      "similarity": 0.89,
      "conversion_status": "converted"
    }
  ]
}
```

---

## Similarity (1)

### search_converted_similar

Finds similar elements that were already converted.

**When to use:** Learning from previous conversions.

```
Input: element_name (string)
Output: {
  "similar": [
    {
      "name": "PAGE_ClienteEdit",
      "similarity": 0.85,
      "converted_file": "routes/cliente.py"
    }
  ]
}
```

---

## PDF (1)

### get_element_pdf_slice

Returns PDF documentation and screenshots for element.

**When to use:** Getting visual reference of original UI.

```
Input: element_name (string)
Output: {
  "pdf_url": "...",
  "screenshots": [...],
  "documentation": "..."
}
```

---

## Usage Patterns

### Building a Dependency Tree (Recursive Fallback)

No single MCP tool traverses `uses` direction recursively. To build a D1→D2→D3 dependency tree, use N+1 `get_dependencies` calls:

```
Step 1: D1 = get_dependencies(ELEMENT, direction="uses", project_name=PROJECT)
        → filter to Procedure/Class only (exclude TABLE)
        → exclude local procedures (ELEMENT.ProcName pattern)

Step 2: For each D1 item (parallel):
        D2 = get_dependencies(D1_ITEM, direction="uses", project_name=PROJECT)
        → filter, deduplicate against visited set

Step 3: For each D2 item (parallel):
        D3 = get_dependencies(D2_ITEM, direction="uses", project_name=PROJECT)
        → filter, deduplicate against visited set

Step 4: For each unique procedure across all depths:
        get_procedure(proc_name, project_name=PROJECT)
        → extract signature, parameters[], return_type
```

**Optimization:** Call `get_dependencies` in parallel for each level. Max calls = D1_count + D2_count + D3_count + signature lookups. For typical elements: ~10-20 MCP calls total.

**Stop at max_depth=3** to limit calls. Most dependency chains terminate naturally at D2-D3 (leaf nodes calling only WLanguage built-ins).

**Used by:** `new-milestone` Phase 1.86 for dependency depth selection.

### Starting a New Element

```
1. get_element {name}           → Full element data
2. get_controls {name}          → UI structure
3. get_element_planes {name}    → Detect tabs/wizard
4. get_procedures {name}        → Business logic
5. get_business_rules {name}    → Extracted business rules
6. get_dependencies {name}      → Prerequisites
7. search_converted_similar     → Learn from similar
8. semantic_search {name}       → Find related elements
```

### Before Planning

```
1. Check depends_on from get_dependencies
2. For each dependency:
   - Converted? → Can import
   - Pending? → May need to convert first
3. get_wlanguage_reference for H* functions found
```

### Before Conversion

```
1. get_business_rules {element}  → Rules to preserve
2. find_similar_by_embedding     → Similar already-converted elements
3. Use rules to guide implementation
4. Document rule preservation in SUMMARY.md
```

### After Conversion

```
1. mark_converted {element_name}
2. Commit changes with reference to element
```

### Project Initialization

```
1. get_schema                   → Full database schema
2. get_conversion_stats         → Current state
3. mark_project_initialized     → After foundation created
```

---

## Error Handling

MCP tools may return errors if:
- Element not found
- Project not imported
- Neo4j not available (for analysis tools)
- PDF not available for element

Always handle gracefully and inform user if data is unavailable.
