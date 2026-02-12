# MCP Specification: Business Rules Verification

## Purpose

Track and verify that business rules extracted from legacy WinDev/WebDev code are preserved in the converted modern codebase. Introduces two new MongoDB collections (`milestone_procedures`, `rule_verifications`) and 6 new MCP tools for lifecycle management.

**Problem solved:** Today, business rules are extracted and stored in `business_rules` collection, but there's no mechanism to track whether each rule was actually implemented during conversion. The verifier agent checks goal achievement (user-facing), but not implementation fidelity (logic preservation). This feature closes that gap.

**Consumers:**
- `new-milestone` Phase 1.86 (populates procedures + creates initial rule verifications)
- `execute-phase` Step 7.5 (per-phase rules check, advisory)
- `audit-milestone` (comprehensive rules audit, blocking)
- `wxcode-rules-verifier` agent (performs the actual verification)
- Dashboard generator (displays rules verification progress)

---

## Data Model

### Collection 1: `milestone_procedures`

Persists the IMPLEMENT_LIST / STUB_LIST from the dependency tree selection. Links a milestone to the specific procedures being converted.

```python
class ProcedureStrategy(str, Enum):
    IMPLEMENT = "implement"
    STUB = "stub"
    ALREADY_CONVERTED = "already_converted"

class MilestoneProcedure(Document):
    """Tracks which procedures a milestone converts and their strategy."""

    milestone_id: PydanticObjectId = Field(..., description="Reference to milestones collection")
    output_project_id: PydanticObjectId = Field(..., description="Reference to output_projects collection")

    # Procedure identification
    procedure_name: str = Field(..., description="Procedure name (e.g., 'VerificarUsuarioSenha')")
    element_name: str = Field(..., description="Parent element (e.g., 'PaginaInicial_New1')")
    procedure_id: Optional[PydanticObjectId] = Field(None, description="Reference to procedures collection")
    element_id: Optional[PydanticObjectId] = Field(None, description="Reference to elements collection")

    # Dependency metadata
    depth: int = Field(..., description="Depth level: 0=element/local, 1=D1 direct, 2=D2, etc.")
    strategy: ProcedureStrategy = Field(..., description="implement, stub, or already_converted")
    is_control_event: bool = Field(default=False, description="True if this is a control event handler (e.g., BTN_Logout.event_851984)")

    # Conversion tracking
    stub_file: Optional[str] = Field(None, description="Path to generated stub file (if strategy=stub)")
    converted_in_phase: Optional[int] = Field(None, description="Phase number where this was converted")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "milestone_procedures"
        indexes = [
            "milestone_id",
            "output_project_id",
            [("milestone_id", 1), ("strategy", 1)],
            [("milestone_id", 1), ("element_name", 1)],
            [("milestone_id", 1), ("depth", 1)],
        ]
```

### Collection 2: `rule_verifications`

Tracks the verification status of each business rule within a milestone. One document per rule per milestone.

```python
class RuleVerificationStatus(str, Enum):
    PENDING = "pending"               # Not yet checked
    IMPLEMENTED = "implemented"       # Rule preserved as-is in converted code
    ADAPTED = "adapted"               # Logic preserved but implementation differs (e.g., HReadSeek -> ORM)
    MISSING = "missing"               # Rule not found in converted code
    DEFERRED = "deferred"             # Procedure is in STUB_LIST — rule check deferred
    NOT_APPLICABLE = "not_applicable" # Rule doesn't apply in modern stack (e.g., cursor management)

class RuleVerification(Document):
    """Tracks verification status of a business rule within a milestone."""

    milestone_id: PydanticObjectId = Field(..., description="Reference to milestones collection")
    output_project_id: PydanticObjectId = Field(..., description="Reference to output_projects collection")
    rule_id: PydanticObjectId = Field(..., description="Reference to business_rules collection")

    # Denormalized from business_rules (for fast queries without joins)
    rule_name: str = Field(..., description="Business rule name")
    procedure_name: str = Field(..., description="Source procedure or control event name")
    element_name: str = Field(..., description="Source element name")
    category: str = Field(..., description="Rule category: validation, workflow, permission, etc.")

    # Verification state
    status: RuleVerificationStatus = Field(default=RuleVerificationStatus.PENDING)
    verified_at: Optional[datetime] = Field(None, description="When verification was performed")
    verified_in_phase: Optional[int] = Field(None, description="Phase where rule was verified")

    # Evidence (populated by wxcode-rules-verifier agent)
    evidence_file: Optional[str] = Field(None, description="File path where rule is implemented")
    evidence_line: Optional[int] = Field(None, description="Line number in the file")
    evidence_snippet: Optional[str] = Field(None, description="Code snippet (max 200 chars)")
    notes: Optional[str] = Field(None, description="Agent notes (e.g., 'Adapted: uses bcrypt instead of MD5')")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "rule_verifications"
        indexes = [
            "milestone_id",
            "output_project_id",
            "rule_id",
            "status",
            [("milestone_id", 1), ("status", 1)],
            [("milestone_id", 1), ("element_name", 1)],
            [("milestone_id", 1), ("procedure_name", 1)],
            [("milestone_id", 1), ("category", 1)],
            [("milestone_id", 1), ("status", 1), ("category", 1)],
        ]
```

---

## MCP Tools

### Tool 1: `populate_milestone_rules`

**Purpose:** Creates `milestone_procedures` and `rule_verifications` records for a milestone. Called once during `new-milestone` Phase 1.86 after the user selects dependency depth.

**File:** `mcp/tools/conversion.py` (alongside existing milestone tools)

```python
@mcp.tool
async def populate_milestone_rules(
    ctx: Context,
    milestone_id: str,
    implement_list: list[dict],
    stub_list: list[dict],
    confirm: bool = False,
) -> dict[str, Any]:
    """Populate milestone procedures and business rule verifications.

    Creates milestone_procedures records from IMPLEMENT_LIST and STUB_LIST,
    then creates rule_verifications for ALL business rules associated with
    the milestone's elements and procedures.

    Business rules are sourced from two pools:
    1. Rules where source_element_name IN milestone.element_names
       (covers control events + local procedures of the element)
    2. Rules where source_procedure_name IN implement_list procedure names
       (covers D1+ dependency procedures from other elements)

    Rules from STUB_LIST procedures get status "deferred".
    All others get status "pending".

    Args:
        milestone_id: ID of the milestone
        implement_list: List of procedures to implement. Each dict:
            {"procedure_name": str, "element_name": str, "depth": int,
             "procedure_id": str|None, "element_id": str|None,
             "is_control_event": bool}
        stub_list: List of procedures to stub. Same dict structure.
        confirm: Set to True to execute (default: False for preview)

    Returns:
        Preview (confirm=False) or execution result (confirm=True) with counts
    """
```

**Logic:**

```
1. Validate milestone_id exists
2. Get milestone.element_names and milestone.output_project_id

3. If not confirm: PREVIEW MODE
   a. Count business_rules where source_element_name IN element_names
   b. Count business_rules where source_procedure_name IN implement_list names
   c. Deduplicate by rule_id
   d. Count stub_list rules (will be "deferred")
   e. Return preview with counts

4. If confirm: EXECUTE MODE
   a. Create MilestoneProcedure for each item in implement_list (strategy="implement")
   b. Create MilestoneProcedure for each item in stub_list (strategy="stub")

   c. Query business_rules — Pool 1:
      WHERE source_element_name IN milestone.element_names
      (this captures control events like "BTN_Logout.event_851984"
       AND local procedures like "Local_RecuperarEmail")

   d. Query business_rules — Pool 2:
      WHERE source_procedure_name IN [p.procedure_name for p in implement_list]
      AND source_element_name NOT IN milestone.element_names
      (this captures D1+ procedures from OTHER elements,
       avoiding duplicates with Pool 1)

   e. Union Pool 1 + Pool 2, deduplicate by rule _id

   f. For each rule:
      - Check if rule.source_procedure_name is in stub_list
        → status = "deferred"
      - Otherwise
        → status = "pending"
      - Create RuleVerification document

   g. Return counts:
      {
        "procedures_created": N,
        "rules_created": M,
        "rules_by_status": {"pending": X, "deferred": Y},
        "rules_by_category": {"validation": A, "workflow": B, ...}
      }
```

**Edge cases:**
- Procedure in implement_list has no business rules → MilestoneProcedure created, no RuleVerification
- Rule already exists for this milestone (idempotency) → Skip duplicates, don't error. Use `rule_id + milestone_id` as uniqueness key.
- Control event procedure (e.g., `BtnLocacoes.event_851984`) → `is_control_event=True`, depth=0

---

### Tool 2: `get_milestone_rules`

**Purpose:** Returns business rule verifications for a milestone, with filtering and aggregation. Primary tool for the `wxcode-rules-verifier` agent.

```python
@mcp.tool
async def get_milestone_rules(
    ctx: Context,
    milestone_id: str,
    status: str | None = None,
    category: str | None = None,
    element_name: str | None = None,
    procedure_name: str | None = None,
    phase: int | None = None,
    include_rule_details: bool = True,
    limit: int = 200,
) -> dict[str, Any]:
    """Get business rule verifications for a milestone.

    Returns rule verifications with optional filtering. When include_rule_details
    is True, enriches each verification with the full business rule data
    (description, conditions, actions) from the business_rules collection.

    Args:
        milestone_id: ID of the milestone
        status: Filter by verification status (pending, implemented, adapted, missing, deferred, not_applicable)
        category: Filter by rule category (validation, workflow, permission, data_integrity, notification, calculation)
        element_name: Filter by source element
        procedure_name: Filter by source procedure or control event
        phase: Filter by verified_in_phase (rules verified in a specific phase)
        include_rule_details: Enrich with full rule data from business_rules (default: True)
        limit: Max results (default: 200)

    Returns:
        List of rule verifications with optional enrichment
    """
```

**Return structure:**

```json
{
  "error": false,
  "milestone_id": "698d074e19c150e4de9f7b8f",
  "total": 69,
  "filtered": 45,
  "rules": [
    {
      "verification_id": "...",
      "rule_id": "698a8f06f9936aefd5687fcf",
      "rule_name": "usuario_deve_estar_ativo",
      "procedure_name": "Local_RecuperarEmail",
      "element_name": "PaginaInicial_New1",
      "category": "validation",
      "status": "pending",
      "verified_at": null,
      "verified_in_phase": null,
      "evidence_file": null,
      "evidence_line": null,
      "evidence_snippet": null,
      "notes": null,
      "rule_details": {
        "description": "Somente usuarios com status ativo (BitAtivo = 1) podem iniciar o processo de recuperacao de senha",
        "confidence": 0.95,
        "conditions": ["Usuario existe na tabela ClienteUsuario", "Campo BitAtivo do usuario = 1"],
        "actions": ["Prosseguir com validacao de email"]
      }
    }
  ]
}
```

**Logic:**
```
1. Build query filter from parameters (milestone_id + optional status/category/element/procedure/phase)
2. Query rule_verifications with filter, sort by element_name, procedure_name
3. If include_rule_details: batch-fetch business_rules by rule_id ($in query)
4. Merge rule details into verifications
5. Return
```

---

### Tool 3: `update_rule_verification`

**Purpose:** Updates the verification status of a single business rule. Called by the `wxcode-rules-verifier` agent for each rule it checks.

```python
@mcp.tool
async def update_rule_verification(
    ctx: Context,
    verification_id: str,
    status: str,
    evidence_file: str | None = None,
    evidence_line: int | None = None,
    evidence_snippet: str | None = None,
    notes: str | None = None,
    verified_in_phase: int | None = None,
    confirm: bool = False,
) -> dict[str, Any]:
    """Update verification status of a business rule.

    This is a write operation requiring confirm=True.

    Args:
        verification_id: ID of the rule_verification document
        status: New status (implemented, adapted, missing, not_applicable)
        evidence_file: File where rule is implemented (e.g., "app/services/auth_service.py")
        evidence_line: Line number in the file
        evidence_snippet: Code snippet showing the implementation (max 200 chars)
        notes: Agent notes explaining the verdict
        verified_in_phase: Phase number where this was verified
        confirm: Set to True to execute (default: False for preview)

    Returns:
        Preview (confirm=False) or execution result (confirm=True)
    """
```

**Validation:**
- `status` must be one of: `implemented`, `adapted`, `missing`, `not_applicable`
- Cannot update a `deferred` rule to anything other than `deferred` or `pending` (deferred rules are checked when the stub is eventually converted)
- `evidence_file` required when status is `implemented` or `adapted`
- `evidence_snippet` truncated to 200 chars

---

### Tool 4: `batch_update_rule_verifications`

**Purpose:** Bulk update multiple rule verifications in one call. Used by the agent to submit all results at once instead of N individual calls.

```python
@mcp.tool
async def batch_update_rule_verifications(
    ctx: Context,
    milestone_id: str,
    updates: list[dict],
    confirm: bool = False,
) -> dict[str, Any]:
    """Batch update multiple rule verifications.

    More efficient than calling update_rule_verification N times.
    All updates are applied atomically.

    Args:
        milestone_id: ID of the milestone (for validation)
        updates: List of update dicts, each containing:
            {"verification_id": str, "status": str,
             "evidence_file": str|None, "evidence_line": int|None,
             "evidence_snippet": str|None, "notes": str|None,
             "verified_in_phase": int|None}
        confirm: Set to True to execute (default: False for preview)

    Returns:
        Preview with summary or execution result with per-item status
    """
```

**Logic:**
```
1. Validate all verification_ids belong to the given milestone_id
2. Preview: return count by status transition (e.g., "pending -> implemented: 12")
3. Execute: bulk_write with UpdateOne operations
4. Return summary: {"updated": N, "by_status": {"implemented": X, "adapted": Y, ...}}
```

---

### Tool 5: `get_rules_verification_summary`

**Purpose:** Aggregation dashboard for rules verification progress. Used by dashboard generator and `audit-milestone`.

```python
@mcp.tool
async def get_rules_verification_summary(
    ctx: Context,
    milestone_id: str,
) -> dict[str, Any]:
    """Get aggregated rules verification progress for a milestone.

    Returns counts grouped by status, category, element, and procedure.
    Designed for dashboard display and audit checks.

    Args:
        milestone_id: ID of the milestone

    Returns:
        Aggregated verification statistics
    """
```

**Return structure:**

```json
{
  "error": false,
  "milestone_id": "698d074e19c150e4de9f7b8f",
  "total_rules": 69,
  "by_status": {
    "pending": 30,
    "implemented": 25,
    "adapted": 8,
    "missing": 2,
    "deferred": 4,
    "not_applicable": 0
  },
  "by_category": {
    "validation": {"total": 12, "implemented": 8, "adapted": 2, "missing": 1, "deferred": 1, "pending": 0, "not_applicable": 0},
    "workflow": {"total": 18, "implemented": 10, "adapted": 3, "missing": 0, "deferred": 2, "pending": 3, "not_applicable": 0},
    "permission": {"total": 15, "implemented": 5, "adapted": 2, "missing": 1, "deferred": 1, "pending": 6, "not_applicable": 0},
    "data_integrity": {"total": 10, "implemented": 2, "adapted": 1, "missing": 0, "deferred": 0, "pending": 7, "not_applicable": 0},
    "notification": {"total": 8, "implemented": 0, "adapted": 0, "missing": 0, "deferred": 0, "pending": 8, "not_applicable": 0},
    "calculation": {"total": 6, "implemented": 0, "adapted": 0, "missing": 0, "deferred": 0, "pending": 6, "not_applicable": 0}
  },
  "by_element": {
    "PaginaInicial_New1": {"total": 49, "implemented": 20, "pending": 22, "deferred": 3, "missing": 2, "adapted": 2, "not_applicable": 0},
    "Table_Dashboard": {"total": 20, "implemented": 5, "pending": 8, "deferred": 1, "missing": 0, "adapted": 6, "not_applicable": 0}
  },
  "by_procedure": [
    {"procedure": "VerificarUsuarioSenha", "element": "PaginaInicial_New1", "total": 20, "implemented": 12, "pending": 5, "missing": 1, "adapted": 2, "deferred": 0},
    {"procedure": "MenuPrincipal.event_851980", "element": "Table_Dashboard", "total": 13, "implemented": 3, "pending": 6, "missing": 0, "adapted": 4, "deferred": 0}
  ],
  "coverage_percentage": 48,
  "implementation_rate": 72
}
```

**Computed fields:**
- `coverage_percentage` = `(total - pending - deferred) / total * 100` (how many rules have been checked)
- `implementation_rate` = `(implemented + adapted) / (implemented + adapted + missing) * 100` (of checked rules, how many passed)

**Implementation:** Use MongoDB aggregation pipeline:

```python
pipeline = [
    {"$match": {"milestone_id": milestone_oid}},
    {"$facet": {
        "by_status": [
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ],
        "by_category": [
            {"$group": {
                "_id": {"category": "$category", "status": "$status"},
                "count": {"$sum": 1}
            }}
        ],
        "by_element": [
            {"$group": {
                "_id": {"element": "$element_name", "status": "$status"},
                "count": {"$sum": 1}
            }}
        ],
        "by_procedure": [
            {"$group": {
                "_id": {"procedure": "$procedure_name", "element": "$element_name", "status": "$status"},
                "count": {"$sum": 1}
            }}
        ],
        "total": [
            {"$count": "count"}
        ]
    }}
]
```

---

### Tool 6: `get_milestone_procedures`

**Purpose:** Returns the procedures being converted in a milestone (IMPLEMENT_LIST + STUB_LIST) with their strategy and conversion status.

```python
@mcp.tool
async def get_milestone_procedures(
    ctx: Context,
    milestone_id: str,
    strategy: str | None = None,
    depth: int | None = None,
) -> dict[str, Any]:
    """Get procedures associated with a milestone.

    Returns the IMPLEMENT_LIST and STUB_LIST persisted during milestone creation.

    Args:
        milestone_id: ID of the milestone
        strategy: Filter by strategy (implement, stub, already_converted)
        depth: Filter by depth level (0=element, 1=D1, 2=D2, etc.)

    Returns:
        List of milestone procedures with strategy and metadata
    """
```

**Return structure:**

```json
{
  "error": false,
  "milestone_id": "698d074e19c150e4de9f7b8f",
  "total": 12,
  "by_strategy": {"implement": 8, "stub": 3, "already_converted": 1},
  "procedures": [
    {
      "id": "...",
      "procedure_name": "VerificarUsuarioSenha",
      "element_name": "PaginaInicial_New1",
      "depth": 0,
      "strategy": "implement",
      "is_control_event": false,
      "converted_in_phase": 2,
      "stub_file": null
    },
    {
      "id": "...",
      "procedure_name": "BTN_Logout.event_851984",
      "element_name": "Table_Dashboard",
      "depth": 0,
      "strategy": "implement",
      "is_control_event": true,
      "converted_in_phase": null,
      "stub_file": null
    },
    {
      "id": "...",
      "procedure_name": "REST_ConfigurarAutenticacao",
      "element_name": "REST_Utils",
      "depth": 2,
      "strategy": "stub",
      "is_control_event": false,
      "converted_in_phase": null,
      "stub_file": "app/services/rest_utils.py"
    }
  ]
}
```

---

## Integration Points in WXCODE Skill

### 1. `new-milestone.md` — Phase 1.86

After the user selects dependency depth and IMPLEMENT_LIST/STUB_LIST are determined:

```
# After AskUserQuestion for depth selection:

# Build implement_list and stub_list dicts
# (already done for MILESTONE-CONTEXT.md)

# Persist to MongoDB
mcp__wxcode-kb__populate_milestone_rules(
    milestone_id=MILESTONE_MONGODB_ID,
    implement_list=[
        {"procedure_name": "VerificarUsuarioSenha", "element_name": "PaginaInicial_New1",
         "depth": 0, "is_control_event": false},
        {"procedure_name": "BTN_Logout.event_851984", "element_name": "Table_Dashboard",
         "depth": 0, "is_control_event": true},
        ...
    ],
    stub_list=[
        {"procedure_name": "REST_ConfigurarAutenticacao", "element_name": "REST_Utils",
         "depth": 2, "is_control_event": false},
        ...
    ],
    confirm=true
)
```

**Important:** Control events must be included in `implement_list` with `is_control_event=true`. They are part of the element being converted (depth=0), not from the dependency tree.

To build the control events list, use:
```
# Get all procedures for each element (includes control events)
mcp__wxcode-kb__get_procedures(element_name=ELEM)
# Filter: those with "event_" in name are control events
```

### 2. `execute-phase.md` — Step 7.5 (after verify-phase)

```
# Only for conversion projects
if CONVERSION.md exists:
    # Spawn wxcode-rules-verifier agent
    Task(wxcode-rules-verifier):
        prompt: |
            Verify business rules for Phase {N} of milestone {MILESTONE_ID}.

            1. Call get_milestone_rules(milestone_id, status="pending", phase=null)
               to get all pending rules
            2. For each rule with conditions/actions:
               - Search converted code for evidence (Grep/Read)
               - Determine status: implemented/adapted/missing/not_applicable
            3. Call batch_update_rule_verifications with results
            4. Generate RULES-CHECK.md report

        subagent_type: wxcode-rules-verifier
```

### 3. `audit-milestone.md`

```
# Get comprehensive summary
summary = mcp__wxcode-kb__get_rules_verification_summary(milestone_id)

# Report:
# - coverage_percentage: how many rules checked
# - implementation_rate: of checked rules, how many passed
# - missing rules must be acknowledged
```

### 4. Dashboard generator (`generate-dashboard.py`)

Add to milestone dashboard JSON:

```json
{
  "business_rules": {
    "total": 69,
    "by_status": {
      "implemented": 25,
      "adapted": 8,
      "missing": 2,
      "deferred": 4,
      "pending": 30,
      "not_applicable": 0
    },
    "coverage_percentage": 48,
    "implementation_rate": 72
  }
}
```

**Note:** The dashboard generator cannot call MCP directly. It would need either:
- A local cache file (e.g., `.planning/rules-summary.json`) written by the rules-verifier agent
- Or a CLI wrapper that calls the MCP tool and outputs JSON

---

## Population Logic Detail

The most complex part is `populate_milestone_rules`. Here's the detailed algorithm:

```python
async def _populate_rules(milestone, implement_list, stub_list):
    """Core population logic."""

    element_names = milestone.element_names  # ["PaginaInicial_New1", "Table_Dashboard"]
    implement_proc_names = {p["procedure_name"] for p in implement_list}
    stub_proc_names = {p["procedure_name"] for p in stub_list}

    # --- Step 1: Create MilestoneProcedure records ---

    for item in implement_list:
        await MilestoneProcedure(
            milestone_id=milestone.id,
            output_project_id=milestone.output_project_id,
            procedure_name=item["procedure_name"],
            element_name=item["element_name"],
            procedure_id=item.get("procedure_id"),
            element_id=item.get("element_id"),
            depth=item["depth"],
            strategy=ProcedureStrategy.IMPLEMENT,
            is_control_event=item.get("is_control_event", False),
        ).insert()

    for item in stub_list:
        await MilestoneProcedure(
            milestone_id=milestone.id,
            output_project_id=milestone.output_project_id,
            procedure_name=item["procedure_name"],
            element_name=item["element_name"],
            depth=item["depth"],
            strategy=ProcedureStrategy.STUB,
            is_control_event=item.get("is_control_event", False),
        ).insert()

    # --- Step 2: Query business rules from TWO pools ---

    # Pool 1: Rules from milestone elements (control events + local procedures)
    pool1 = await BusinessRule.find(
        {"source_element_name": {"$in": element_names}}
    ).to_list()

    # Pool 2: Rules from IMPLEMENT_LIST procedures in OTHER elements
    pool2_proc_names = implement_proc_names - {
        p["procedure_name"] for p in implement_list
        if p["element_name"] in element_names
    }
    pool2 = []
    if pool2_proc_names:
        pool2 = await BusinessRule.find(
            {"source_procedure_name": {"$in": list(pool2_proc_names)}}
        ).to_list()

    # --- Step 3: Union + deduplicate ---

    all_rules = {}
    for rule in pool1 + pool2:
        all_rules[rule.id] = rule  # Dedup by _id

    # --- Step 4: Create RuleVerification records ---

    for rule in all_rules.values():
        # Determine initial status
        if rule.source_procedure_name in stub_proc_names:
            status = RuleVerificationStatus.DEFERRED
        else:
            status = RuleVerificationStatus.PENDING

        await RuleVerification(
            milestone_id=milestone.id,
            output_project_id=milestone.output_project_id,
            rule_id=rule.id,
            rule_name=rule.name,
            procedure_name=rule.source_procedure_name,
            element_name=rule.source_element_name,
            category=rule.category,
            status=status,
        ).insert()
```

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Procedure has 0 business rules | MilestoneProcedure created, no RuleVerification for that procedure |
| Control event `BtnLocacoes.event_851984` | Captured via Pool 1 (source_element_name match). is_control_event=true |
| Same rule referenced by both Pool 1 and Pool 2 | Deduplicated by rule _id — only one RuleVerification created |
| Rule's procedure in STUB_LIST | RuleVerification.status = "deferred" |
| populate called twice for same milestone | Idempotent: check existing records, skip duplicates. Use upsert or pre-check. |
| Milestone has no business rules at all | Return success with counts=0 |
| Rule with confidence < 0.5 | Still created as RuleVerification (agent can mark as not_applicable if irrelevant) |
| D1+ procedure from another element has control event rules | Those rules are NOT included (Pool 2 filters by procedure_name, not element_name of the dependency) |

---

## Registration Checklist

### Models

1. Create `models/milestone_procedure.py` with `MilestoneProcedure` + `ProcedureStrategy`
2. Create `models/rule_verification.py` with `RuleVerification` + `RuleVerificationStatus`
3. Register both in `models/__init__.py` exports
4. Register both in `database.py` init_beanie document_models list

### Tools

5. Add tools to `mcp/tools/conversion.py` (alongside existing milestone tools):
   - `populate_milestone_rules`
   - `get_milestone_rules`
   - `update_rule_verification`
   - `batch_update_rule_verifications`
   - `get_rules_verification_summary`
   - `get_milestone_procedures`
6. No new tools file needed — these belong in conversion.py with the other milestone tools

### System

7. Update `mcp/tools/system.py` list_tools() to add "rules_verification" category
8. Update tool count in documentation

---

## Test Cases

### 1. Populate rules for milestone with elements + D1 dependencies

```
Input:
  milestone has element_names: ["PaginaInicial_New1", "Table_Dashboard"]
  implement_list: [
    {proc: "VerificarUsuarioSenha", elem: "PaginaInicial_New1", depth: 0},
    {proc: "BTN_Logout.event_851984", elem: "Table_Dashboard", depth: 0, is_control_event: true},
    {proc: "Documento_TemplatePreenchido", elem: "Comunicacao_APIDocs", depth: 1},
  ]
  stub_list: [
    {proc: "REST_ConfigurarAutenticacao", elem: "REST_Utils", depth: 2},
  ]

Expected:
  milestone_procedures: 4 records (3 implement + 1 stub)
  rule_verifications: 69+ records (all rules for elements + D1 procedures)
  Rules for "REST_ConfigurarAutenticacao" → status: "deferred"
  Rules for control events → status: "pending"
```

### 2. Get rules filtered by phase

```
Input: get_milestone_rules(milestone_id, phase=2)
Expected: Only rules where verified_in_phase=2
```

### 3. Batch update after verification

```
Input: batch_update_rule_verifications(milestone_id, [
  {verification_id: "A", status: "implemented", evidence_file: "app/services/auth.py", evidence_line: 45},
  {verification_id: "B", status: "adapted", notes: "Uses bcrypt instead of MD5"},
  {verification_id: "C", status: "missing"},
])
Expected: 3 records updated, summary returned
```

### 4. Summary aggregation

```
Input: get_rules_verification_summary(milestone_id)
Expected: Aggregated counts by status, category, element, procedure
  coverage_percentage and implementation_rate computed correctly
```

### 5. Idempotent population

```
Input: populate_milestone_rules called twice with same data
Expected: Second call returns success with 0 new records (all already exist)
```

---

## Performance Considerations

- `populate_milestone_rules`: One-time operation per milestone. ~69 inserts for typical element. Use `insert_many` for bulk.
- `get_milestone_rules`: Indexed queries on milestone_id + filters. Should be < 50ms for 200 rules.
- `batch_update_rule_verifications`: Use `bulk_write` with UpdateOne operations. Single round-trip.
- `get_rules_verification_summary`: Single aggregation pipeline with $facet. Should be < 100ms.
