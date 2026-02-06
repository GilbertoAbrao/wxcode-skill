---
name: wxcode:validate-schema
description: Validate database models against legacy schema via MCP
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Task
  - mcp__wxcode-kb__*
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"validate-schema","args":"$ARGUMENTS","title":"WXCODE ▶ VALIDATING SCHEMA"} -->
## WXCODE ▶ VALIDATING SCHEMA
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end (valid):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Schema valid - N models match legacy"} -->
```

**At command end (issues found):**
```
<!-- WXCODE:STATUS:{"status":"failed","message":"Schema issues found","issues":N} -->
<!-- WXCODE:NEXT_ACTION:{"command":"validate-schema","args":"--fix","description":"Generate missing models","priority":"recommended"} -->
```
</structured_output>

<objective>
Validate that database models in the current project match the legacy schema from MCP.

This ensures the new application can access the legacy database transparently without schema drift.

**Use cases:**
- Before milestone completion: verify all needed models exist
- After manual model changes: check for drift
- Debugging data issues: confirm model matches legacy
- CI/CD: automated schema validation
</objective>

<context>
**Arguments:**
- `--fix` — Generate missing models automatically
- `--table=TABLE_NAME` — Validate specific table only
- (no args) — Validate all models

**Required files:**
@.planning/CONVERSION.md (contains output_project_id)

**If not a conversion project:** Error - this command is only for conversion projects.
</context>

<process>

## Step 1: Verify Conversion Project

```bash
test -f .planning/CONVERSION.md && echo "conversion" || echo "greenfield"
```

**If greenfield:**
```
<!-- WXCODE:ERROR:{"code":"NOT_CONVERSION_PROJECT","message":"This command is only for conversion projects","recoverable":false} -->

This command validates models against legacy schema.
For greenfield projects, there is no legacy schema to validate against.
```
**STOP.**

## Step 2: Load Project Context

Read `.planning/CONVERSION.md` to get:
- `output_project_id` — MongoDB OutputProject ID
- `project_name` — Legacy project name in KB

Get stack conventions:
```
mcp__wxcode-kb__get_stack_conventions(output_project_id)
```

Determine models location:
- **Python/SQLAlchemy:** `app/models/`
- **Prisma:** `prisma/schema.prisma`
- **TypeORM:** `src/models/` or `src/entities/`
- **Django:** `*/models.py`
- **Sequelize:** `src/models/`

## Step 3: Spawn Schema Generator for Validation

```
Task(wxcode-schema-generator):
  prompt: |
    Validate existing database models against legacy schema.

    Output Project ID: ${OUTPUT_PROJECT_ID}

    Use capability: validate_models

    Check:
    1. Table coverage - every legacy table should have a model
    2. Table name mapping - models must map to exact legacy names
    3. Column coverage - every legacy column should exist in model
    4. Column name mapping - columns must map to exact legacy names
    5. Type compatibility - ORM types must match legacy types

    Return detailed validation report.
  subagent_type: wxcode-schema-generator
```

## Step 4: Display Results

**If all valid:**

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Schema valid - N models match legacy"} -->

## ✓ Schema Validation Passed

**Models:** [N] validated
**Tables in Legacy:** [N]
**Coverage:** 100%

All models correctly map to legacy database schema.
```

**If issues found:**

```
<!-- WXCODE:STATUS:{"status":"failed","message":"Schema issues found","issues":N} -->

## ⚠ Schema Validation Issues

**Models:** [N] checked
**Issues:** [M] found

### Missing Models

| Legacy Table | Status |
|--------------|--------|
| TABLE_A | ❌ No model |
| TABLE_B | ❌ No model |

### Mapping Issues

| Model | Issue | Expected | Found |
|-------|-------|----------|-------|
| Usuario | Table name | USUARIO | usuarios |
| Pedido | Missing column | VL_DESCONTO | - |

### Recommendations

1. Run `/wxcode:validate-schema --fix` to generate missing models
2. Or manually fix mapping issues in existing models
```

## Step 5: Handle --fix Flag

**If `--fix` argument provided AND issues found:**

```
◆ Generating missing models...
```

```
Task(wxcode-schema-generator):
  prompt: |
    Generate models for tables that are missing.

    Output Project ID: ${OUTPUT_PROJECT_ID}
    Missing tables: [from validation report]

    Use capability: generate_specific_models

    Requirements:
    - Preserve EXACT legacy table/column names
    - Add to existing models directory
    - Update exports/barrel file
  subagent_type: wxcode-schema-generator
```

After generation:
```
✓ Generated [N] missing models

Run `/wxcode:validate-schema` again to verify.
```

## Step 6: Handle --table Flag

**If `--table=TABLE_NAME` argument provided:**

Validate only that specific table:

```
Task(wxcode-schema-generator):
  prompt: |
    Validate the model for a specific table.

    Output Project ID: ${OUTPUT_PROJECT_ID}
    Table: ${TABLE_NAME}

    Check if model exists and correctly maps to legacy table.
    If model doesn't exist, report as missing.
    If model exists, verify all columns and types match.
  subagent_type: wxcode-schema-generator
```

</process>

<success_criteria>
- [ ] Correctly identifies conversion vs greenfield projects
- [ ] Spawns schema generator with correct capability
- [ ] Reports all missing models clearly
- [ ] Reports mapping issues with specific details
- [ ] `--fix` generates missing models
- [ ] `--table` validates single table
- [ ] Structured output emitted correctly
</success_criteria>
