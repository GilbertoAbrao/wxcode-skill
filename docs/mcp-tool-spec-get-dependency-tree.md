# MCP Tool Specification: `get_dependency_tree`

## Purpose

Server-side recursive dependency traversal that replaces N+1 client-side `get_dependencies` calls with a single deterministic Neo4j query. Returns the full dependency tree for an element with depth levels, procedure signatures, and conversion status.

**Problem solved:** Today, building a D1→D2→D3 dependency tree requires ~10-20 sequential MCP calls (one `get_dependencies` per node + one `get_procedure` per unique procedure). This is non-deterministic and token-expensive. A single server-side traversal with variable-length path matching is O(1) from the client perspective.

**Consumer:** `new-milestone` Phase 1.86 (dependency depth selection). The user sees the tree, picks a depth, and the command generates IMPLEMENT_LIST (procedures to convert) and STUB_LIST (procedures to stub).

---

## Tool Registration

```python
@server.tool()
async def get_dependency_tree(
    element_name: str,
    project_name: str,
    max_depth: int = 3,
    dep_types: list[str] | None = None,
    include_signatures: bool = True,
    include_conversion_status: bool = True,
    exclude_local: bool = True,
) -> dict:
    """Get full dependency tree for an element with depth levels.

    Traverses the CALLS relationship graph from the source element,
    returning all dependencies organized by depth level (D1, D2, D3...).

    Uses a single Neo4j variable-length path query for efficiency.
    Enriches each node with procedure signatures from MongoDB.

    Use this to understand the full dependency chain before conversion,
    allowing depth-based implementation vs stub decisions.

    Args:
        element_name: Starting element (e.g., "PaginaInicial_New1")
        project_name: Project scope (required, avoids disambiguation)
        max_depth: Maximum traversal depth (default: 3, max: 5)
        dep_types: Filter node types (default: ["Procedure", "Class"])
        include_signatures: Include procedure signatures from MongoDB (default: True)
        include_conversion_status: Include conversion status (default: True)
        exclude_local: Exclude local procedures (Element.ProcName pattern) (default: True)

    Returns:
        Dependency tree organized by depth with signatures and status
    """
```

---

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `element_name` | `str` | Yes | — | Starting element name (e.g., `"PaginaInicial_New1"`, `"PAGE_Login"`) |
| `project_name` | `str` | Yes | — | Project name for scoping (e.g., `"Linkpay_Comissao_1c7aac45"`) |
| `max_depth` | `int` | No | `3` | Max traversal depth (1-5). Clamp to 5. |
| `dep_types` | `list[str]` | No | `None` | Filter dependency types. `None` = `["Procedure", "Class"]`. Valid: `"Procedure"`, `"Class"`, `"Element"`. Never includes `"Table"` (tables are handled separately). |
| `include_signatures` | `bool` | No | `True` | Enrich with signatures from MongoDB `procedures` collection |
| `include_conversion_status` | `bool` | No | `True` | Enrich with conversion status from MongoDB `elements` collection |
| `exclude_local` | `bool` | No | `True` | Exclude local procedures whose name starts with `{element_name}.` |

---

## Return Structure

```json
{
  "element": "PaginaInicial_New1",
  "project": "Linkpay_Comissao_1c7aac45",
  "total_dependencies": 8,
  "max_depth_reached": 3,
  "tree": {
    "D1": [
      {
        "name": "Documento_TemplatePreenchido",
        "type": "Procedure",
        "parent_element": "Comunicacao_APIDocs",
        "signature": "PROCEDURE Documento_TemplatePreenchido(sSlug is ANSI string, sContent is ANSI string): (string, string)",
        "parameters": [
          {"name": "sSlug", "type": "ANSI string", "default": null},
          {"name": "sContent", "type": "ANSI string", "default": null}
        ],
        "return_type": "(string, string)",
        "conversion_status": "pending",
        "called_by": "PaginaInicial_New1",
        "sub_dep_count": 2
      },
      {
        "name": "Documento_ConsultarAceite",
        "type": "Procedure",
        "parent_element": "Comunicacao_APIDocs",
        "signature": "PROCEDURE Documento_ConsultarAceite(sSlug is ANSI string): (string, string)",
        "parameters": [
          {"name": "sSlug", "type": "ANSI string", "default": null}
        ],
        "return_type": "(string, string)",
        "conversion_status": "pending",
        "called_by": "PaginaInicial_New1",
        "sub_dep_count": 0
      },
      {
        "name": "SQLServerConectar",
        "type": "Procedure",
        "parent_element": "ConexaoBD",
        "signature": "PROCEDURE SQLServerConectar(): boolean",
        "parameters": [],
        "return_type": "boolean",
        "conversion_status": "converted",
        "called_by": "PaginaInicial_New1",
        "sub_dep_count": 0
      }
    ],
    "D2": [
      {
        "name": "REST_ConfigurarAutenticacao",
        "type": "Procedure",
        "parent_element": "REST_Utils",
        "signature": "PROCEDURE REST_ConfigurarAutenticacao(sToken is ANSI string)",
        "parameters": [
          {"name": "sToken", "type": "ANSI string", "default": null}
        ],
        "return_type": "void",
        "conversion_status": "pending",
        "called_by": "Documento_TemplatePreenchido",
        "sub_dep_count": 1
      },
      {
        "name": "Global_PegaTokenAPI",
        "type": "Procedure",
        "parent_element": "GlobalUtils",
        "signature": "PROCEDURE Global_PegaTokenAPI(): string",
        "parameters": [],
        "return_type": "string",
        "conversion_status": "pending",
        "called_by": "Documento_TemplatePreenchido",
        "sub_dep_count": 0
      }
    ],
    "D3": [
      {
        "name": "Config_LerParametro",
        "type": "Procedure",
        "parent_element": "ConfigUtils",
        "signature": "PROCEDURE Config_LerParametro(sChave is ANSI string): string",
        "parameters": [
          {"name": "sChave", "type": "ANSI string", "default": null}
        ],
        "return_type": "string",
        "conversion_status": "pending",
        "called_by": "REST_ConfigurarAutenticacao",
        "sub_dep_count": 0
      }
    ]
  },
  "local_procedures": [
    "PaginaInicial_New1.VerificarUsuarioSenha",
    "PaginaInicial_New1.Local_ConfiguraMenu",
    "PaginaInicial_New1.Local_RecuperarEmail"
  ],
  "summary": {
    "D1": {"total": 5, "converted": 1, "pending": 4},
    "D2": {"total": 2, "converted": 0, "pending": 2},
    "D3": {"total": 1, "converted": 0, "pending": 1}
  }
}
```

### Field Descriptions

**Top-level:**

| Field | Type | Description |
|-------|------|-------------|
| `element` | `str` | Source element name |
| `project` | `str` | Project name |
| `total_dependencies` | `int` | Total unique dependencies across all depths |
| `max_depth_reached` | `int` | Deepest level that has entries (may be < `max_depth` if tree terminates early) |
| `tree` | `dict[str, list]` | Dependencies grouped by depth: `"D1"`, `"D2"`, `"D3"`, etc. |
| `local_procedures` | `list[str]` | Local procedures excluded from tree (part of the element itself) |
| `summary` | `dict[str, dict]` | Per-depth counts: `total`, `converted`, `pending` |

**Per dependency node (items in `tree.D*`):**

| Field | Type | When | Description |
|-------|------|------|-------------|
| `name` | `str` | Always | Procedure/Class name |
| `type` | `str` | Always | Node type: `"Procedure"` or `"Class"` |
| `parent_element` | `str` | Always | Element that contains this procedure |
| `signature` | `str` | `include_signatures=True` | Full WLanguage signature string |
| `parameters` | `list[dict]` | `include_signatures=True` | Parameter list with name, type, default |
| `return_type` | `str` | `include_signatures=True` | Return type (`"void"` if none) |
| `conversion_status` | `str` | `include_conversion_status=True` | `"pending"`, `"converted"`, `"in_progress"`, `"validated"` |
| `called_by` | `str` | Always | Name of the node at depth-1 that calls this (parent in the tree) |
| `sub_dep_count` | `int` | Always | Number of children this node has (0 = leaf) |

---

## Implementation

### Phase 1: Neo4j Query

Core logic — single variable-length path match:

```cypher
// Find all dependencies up to max_depth via CALLS edges
MATCH path = (source {name: $element_name, project: $project_name})
             -[:CALLS*1..$max_depth]->(dep)
WHERE (dep:Procedure OR dep:Class)
WITH dep,
     min(length(path)) AS depth,
     // Get the node at depth-1 that calls this dependency
     [rel IN relationships(path) | startNode(rel).name][-1] AS called_by,
     // Count outgoing CALLS from this dep (sub-dependencies)
     size([(dep)-[:CALLS]->(child) WHERE child:Procedure OR child:Class | child]) AS sub_dep_count
RETURN
    dep.name AS name,
    labels(dep)[0] AS type,
    depth,
    called_by,
    sub_dep_count
ORDER BY depth, dep.name
```

**Notes on the query:**

1. **Variable-length path `*1..$max_depth`**: Neo4j handles this server-side — no client-side recursion needed. The `$max_depth` parameter is injected (parameterized, not string-interpolated).

2. **`min(length(path))`**: A node reachable at both D1 and D3 should appear at D1 only (shallowest depth wins).

3. **`called_by`**: The last `startNode` in the relationship chain is the direct caller. For D1 nodes this is the source element itself.

4. **`sub_dep_count`**: Counts immediate children so the client can show "has N sub-dependencies" without another query.

5. **Local procedure exclusion** (`exclude_local=True`): Add a WHERE clause:
   ```cypher
   AND NOT dep.name STARTS WITH ($element_name + ".")
   ```

6. **Type filtering** (`dep_types`): Replace `(dep:Procedure OR dep:Class)` with dynamic label check based on `dep_types` parameter.

### Phase 1.5: Collect Local Procedures

Separate query for local procedures (excluded from tree but returned for reference):

```cypher
MATCH (source {name: $element_name, project: $project_name})-[:CALLS]->(local)
WHERE local:Procedure
  AND local.name STARTS WITH ($element_name + ".")
RETURN local.name AS name
ORDER BY local.name
```

### Phase 2: Parent Element Resolution

For each unique dependency, find the parent element:

```cypher
MATCH (element)-[:CONTAINS]->(dep {name: $dep_name, project: $project_name})
WHERE element:Element
RETURN element.name AS parent_element
LIMIT 1
```

**Optimization:** Batch all dependency names into a single query:

```cypher
UNWIND $dep_names AS dep_name
MATCH (element)-[:CONTAINS]->(dep {name: dep_name, project: $project_name})
WHERE element:Element
RETURN dep.name AS name, element.name AS parent_element
```

### Phase 3: MongoDB Enrichment (signatures)

If `include_signatures=True`:

For each unique procedure in the tree, query MongoDB `procedures` collection:

```python
# Batch query all procedures at once
procedures = db.procedures.find(
    {
        "name": {"$in": list(unique_proc_names)},
        "project_name": project_name,
    },
    {
        "name": 1,
        "signature": 1,
        "parameters": 1,
        "return_type": 1,
    }
)
```

Map results back to tree nodes by `name`.

**If a procedure is not found in MongoDB** (e.g., it's a Neo4j-only node): Set `signature`, `parameters`, `return_type` to `null`.

### Phase 4: MongoDB Enrichment (conversion status)

If `include_conversion_status=True`:

```python
# Check element conversion_status for each parent_element
elements = db.elements.find(
    {
        "name": {"$in": list(unique_parent_elements)},
        "project_name": project_name,
    },
    {
        "name": 1,
        "conversion_status": 1,
    }
)
```

**Fallback:** If not found, default to `"pending"`.

**Alternative:** If procedures themselves have a `conversion_status` field in Neo4j properties, use that directly from Phase 1 query results.

### Phase 5: Assembly

```python
def assemble_tree(neo4j_results, local_procs, parent_map, signatures, statuses):
    tree = {}
    summary = {}

    for row in neo4j_results:
        depth_key = f"D{row['depth']}"
        if depth_key not in tree:
            tree[depth_key] = []
            summary[depth_key] = {"total": 0, "converted": 0, "pending": 0}

        node = {
            "name": row["name"],
            "type": row["type"],
            "parent_element": parent_map.get(row["name"], "unknown"),
            "called_by": row["called_by"],
            "sub_dep_count": row["sub_dep_count"],
        }

        # Signature enrichment
        if include_signatures:
            sig = signatures.get(row["name"], {})
            node["signature"] = sig.get("signature")
            node["parameters"] = sig.get("parameters", [])
            node["return_type"] = sig.get("return_type", "void")

        # Conversion status enrichment
        if include_conversion_status:
            status = statuses.get(row["name"], "pending")
            node["conversion_status"] = status

        tree[depth_key].append(node)

        # Summary
        summary[depth_key]["total"] += 1
        if node.get("conversion_status") == "converted":
            summary[depth_key]["converted"] += 1
        else:
            summary[depth_key]["pending"] += 1

    max_depth_reached = max(
        (int(k[1:]) for k in tree.keys()),
        default=0
    )

    return {
        "element": element_name,
        "project": project_name,
        "total_dependencies": sum(s["total"] for s in summary.values()),
        "max_depth_reached": max_depth_reached,
        "tree": tree,
        "local_procedures": local_procs,
        "summary": summary,
    }
```

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Element has no procedure dependencies | Return empty tree: `{"tree": {}, "total_dependencies": 0, "summary": {}}` |
| Element not found | Return error: `{"error": "Element not found", "element": "...", "project": "..."}` |
| Circular dependency (A→B→A) | Neo4j `*1..N` path matching handles cycles — a node appears at its shallowest depth only |
| Procedure in MongoDB but not Neo4j | Can't happen — tree is built from Neo4j, MongoDB only enriches |
| Procedure in Neo4j but not MongoDB | `signature`, `parameters`, `return_type` = `null` |
| `max_depth` > actual tree depth | `max_depth_reached` reflects actual depth; empty `D*` levels are omitted |
| All dependencies already converted | Return normally — client checks `summary.D*.pending == 0` to skip depth selection |
| Local procedure also called globally | If `exclude_local=True`, local procs (matching `element_name.` prefix) are excluded from tree and listed separately. A global procedure with the same logic but different name appears normally. |

---

## Performance

| Scenario | Expected Performance |
|----------|---------------------|
| Typical element (5-15 deps, depth 2-3) | < 200ms |
| Hub element (50+ deps, depth 3) | < 500ms |
| max_depth=5 on large graph | < 1s |

The Neo4j variable-length path query is the bottleneck. MongoDB batch lookups add ~50ms.

**Optimization tips:**
- Use `$in` for batch MongoDB queries (one query per collection, not per node)
- Cache parent element resolution if `CONTAINS` relationships are stable
- Consider adding a Neo4j index on `(name, project)` if not already present

---

## Relationship to Existing Tools

| Existing Tool | What It Does | Gap `get_dependency_tree` Fills |
|---------------|-------------|--------------------------------|
| `get_dependencies` | D1 only, both directions | No recursion, no signatures |
| `get_impact` | Recursive `used_by` (reverse) | Wrong direction — traverses who uses this, not what this uses |
| `get_procedure` | Single procedure details | One-at-a-time, no tree context |
| `get_topological_order` | Full project ordering | All elements, not scoped to one element's tree |

`get_dependency_tree` = `get_dependencies(direction="uses")` applied recursively + `get_procedure` signatures batched + conversion status — all in one call.

---

## Test Cases

### 1. Element with no dependencies
```
Input: element_name="SimplePage", project_name="TestProject", max_depth=3
Expected: total_dependencies=0, tree={}, summary={}
```

### 2. Element with D1-only dependencies
```
Input: element_name="PAGE_Login", project_name="TestProject", max_depth=3
Expected: tree has "D1" only, no "D2"/"D3", max_depth_reached=1
```

### 3. Element with deep chain
```
Input: element_name="PAGE_Complex", max_depth=2
Expected: tree has "D1" and "D2" only (D3 deps exist but max_depth=2 stops them)
```

### 4. Circular dependency handling
```
Graph: A→B→C→A (cycle)
Input: element_name="A", max_depth=5
Expected: B at D1, C at D2, A NOT in tree (it's the source, not a dep)
```

### 5. Shared dependency (diamond)
```
Graph: A→B, A→C, B→D, C→D (D reachable via two paths)
Input: element_name="A", max_depth=3
Expected: D appears at D2 only (shallowest), called_by is one of B or C
```

### 6. Local procedures excluded
```
Graph: A→A.LocalProc, A→GlobalProc
Input: element_name="A", exclude_local=True
Expected: tree has GlobalProc only, local_procedures has ["A.LocalProc"]
```

### 7. include_signatures=False
```
Input: include_signatures=False
Expected: nodes have name, type, parent_element, called_by, sub_dep_count, conversion_status
         nodes do NOT have signature, parameters, return_type
```
