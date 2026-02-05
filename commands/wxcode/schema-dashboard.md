---
name: wxcode:schema-dashboard
description: Generate stack-agnostic schema dashboard JSON from current project models
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - mcp__wxcode-kb__*
---

<structured_output>
## Structured Output (MANDATORY)

**At command start:**
```
<!-- WXCODE:HEADER:{"command":"schema-dashboard","args":"$ARGUMENTS","title":"WXCODE ▶ GENERATING SCHEMA DASHBOARD"} -->
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Dashboard generated with N tables"} -->
```

**On errors:**
```
<!-- WXCODE:ERROR:{"code":"NOT_CONVERSION_PROJECT","message":"No conversion project found","recoverable":false} -->
```
</structured_output>

<objective>
Generate a stack-agnostic JSON dashboard of all database models in the current project.

This command parses ORM-specific model files (SQLAlchemy, Prisma, TypeORM, Django, Sequelize, etc.) and produces a unified JSON format that any UI can consume without understanding specific ORMs.

**Output:** `.planning/schema-dashboard.json`

**Called by:**
- `wxcode-schema-generator` after generating/validating models
- Manually via `/wxcode:schema-dashboard`
- CI/CD pipelines for documentation
</objective>

<context>
**Arguments:**
- (none) — Generate full dashboard
- `--table=TABLE_NAME` — Regenerate entry for specific table only

**Required:**
- `.planning/CONVERSION.md` (conversion project context)
- Model files in stack-appropriate location
</context>

<dashboard_schema>
## Complete Schema Dashboard Format

The output JSON must capture ALL elements of a database schema, regardless of ORM/stack:

```json
{
  "$schema": "https://wxcode.dev/schemas/dashboard-v1.json",
  "version": "1.0.0",
  "generated_at": "2026-02-05T10:30:00Z",

  "project": {
    "name": "Project Name",
    "output_project_id": "507f1f77bcf86cd799439011",
    "legacy_project": "WINDEV_PROJECT"
  },

  "stack": {
    "id": "fastapi-sqlalchemy",
    "orm": "SQLAlchemy",
    "orm_version": "2.0",
    "database_type": "postgresql",
    "models_location": "app/models/"
  },

  "coverage": {
    "legacy_tables": 50,
    "models_generated": 45,
    "models_validated": 45,
    "percentage": 90.0,
    "missing_tables": ["TABLE_X", "TABLE_Y"],
    "extra_tables": []
  },

  "connections": [
    {
      "name": "default",
      "database_type": "postgresql",
      "host": "localhost",
      "port": 5432,
      "database": "mydb",
      "schema": "public"
    }
  ],

  "enums": [
    {
      "name": "StatusPedido",
      "legacy_name": "STATUS_PEDIDO",
      "values": [
        {"name": "PENDING", "value": "P", "label": "Pendente"},
        {"name": "APPROVED", "value": "A", "label": "Aprovado"},
        {"name": "CANCELLED", "value": "C", "label": "Cancelado"}
      ],
      "model_file": "app/models/enums.py"
    }
  ],

  "tables": [
    {
      "name": "Usuario",
      "legacy_name": "USUARIO",
      "model_file": "app/models/usuario.py",
      "status": "validated",
      "description": "User accounts table",

      "columns": [
        {
          "name": "ID_USUARIO",
          "legacy_name": "ID_USUARIO",
          "type": {
            "base": "integer",
            "raw": "Integer",
            "orm_specific": "Column(Integer)",
            "size": null,
            "precision": null,
            "scale": null
          },
          "nullable": false,
          "primary_key": true,
          "auto_increment": true,
          "unique": false,
          "default": null,
          "server_default": null,
          "comment": "User unique identifier",
          "computed": null
        },
        {
          "name": "NM_USUARIO",
          "legacy_name": "NM_USUARIO",
          "type": {
            "base": "string",
            "raw": "String(100)",
            "orm_specific": "Column(String(100))",
            "size": 100,
            "precision": null,
            "scale": null
          },
          "nullable": false,
          "primary_key": false,
          "auto_increment": false,
          "unique": false,
          "default": null,
          "server_default": null,
          "comment": "User full name",
          "computed": null
        },
        {
          "name": "VL_SALDO",
          "legacy_name": "VL_SALDO",
          "type": {
            "base": "decimal",
            "raw": "Numeric(19,4)",
            "orm_specific": "Column(Numeric(19, 4))",
            "size": null,
            "precision": 19,
            "scale": 4
          },
          "nullable": false,
          "primary_key": false,
          "auto_increment": false,
          "unique": false,
          "default": "0.0000",
          "server_default": "0",
          "comment": "Account balance",
          "computed": null
        },
        {
          "name": "DT_CADASTRO",
          "legacy_name": "DT_CADASTRO",
          "type": {
            "base": "datetime",
            "raw": "DateTime",
            "orm_specific": "Column(DateTime)",
            "size": null,
            "precision": null,
            "scale": null
          },
          "nullable": false,
          "primary_key": false,
          "auto_increment": false,
          "unique": false,
          "default": null,
          "server_default": "CURRENT_TIMESTAMP",
          "comment": "Registration date",
          "computed": null
        },
        {
          "name": "DS_HASH_SENHA",
          "legacy_name": "DS_HASH_SENHA",
          "type": {
            "base": "text",
            "raw": "Text",
            "orm_specific": "Column(Text)",
            "size": null,
            "precision": null,
            "scale": null
          },
          "nullable": true,
          "primary_key": false,
          "auto_increment": false,
          "unique": false,
          "default": null,
          "server_default": null,
          "comment": "Password hash",
          "computed": null
        },
        {
          "name": "BL_ATIVO",
          "legacy_name": "BL_ATIVO",
          "type": {
            "base": "boolean",
            "raw": "Boolean",
            "orm_specific": "Column(Boolean)",
            "size": null,
            "precision": null,
            "scale": null
          },
          "nullable": false,
          "primary_key": false,
          "auto_increment": false,
          "unique": false,
          "default": true,
          "server_default": "true",
          "comment": "Active flag",
          "computed": null
        },
        {
          "name": "IM_AVATAR",
          "legacy_name": "IM_AVATAR",
          "type": {
            "base": "binary",
            "raw": "LargeBinary",
            "orm_specific": "Column(LargeBinary)",
            "size": null,
            "precision": null,
            "scale": null
          },
          "nullable": true,
          "primary_key": false,
          "auto_increment": false,
          "unique": false,
          "default": null,
          "server_default": null,
          "comment": "Avatar image",
          "computed": null
        },
        {
          "name": "ID_EMPRESA",
          "legacy_name": "ID_EMPRESA",
          "type": {
            "base": "integer",
            "raw": "Integer",
            "orm_specific": "Column(Integer, ForeignKey('EMPRESA.ID_EMPRESA'))",
            "size": null,
            "precision": null,
            "scale": null
          },
          "nullable": false,
          "primary_key": false,
          "auto_increment": false,
          "unique": false,
          "default": null,
          "server_default": null,
          "comment": "Company FK",
          "computed": null,
          "foreign_key": {
            "table": "EMPRESA",
            "column": "ID_EMPRESA"
          }
        }
      ],

      "primary_key": {
        "name": "pk_usuario",
        "columns": ["ID_USUARIO"],
        "auto_generated_name": true
      },

      "foreign_keys": [
        {
          "name": "fk_usuario_empresa",
          "columns": ["ID_EMPRESA"],
          "references_table": "EMPRESA",
          "references_columns": ["ID_EMPRESA"],
          "on_delete": "RESTRICT",
          "on_update": "CASCADE",
          "deferrable": false
        }
      ],

      "indexes": [
        {
          "name": "idx_usuario_email",
          "columns": ["DS_EMAIL"],
          "unique": true,
          "type": "btree",
          "where": null,
          "include": null
        },
        {
          "name": "idx_usuario_empresa",
          "columns": ["ID_EMPRESA"],
          "unique": false,
          "type": "btree",
          "where": null,
          "include": null
        },
        {
          "name": "idx_usuario_nome_ativo",
          "columns": ["NM_USUARIO", "BL_ATIVO"],
          "unique": false,
          "type": "btree",
          "where": "BL_ATIVO = true",
          "include": null
        }
      ],

      "unique_constraints": [
        {
          "name": "uq_usuario_cpf",
          "columns": ["NR_CPF"]
        }
      ],

      "check_constraints": [
        {
          "name": "ck_usuario_saldo_positivo",
          "expression": "VL_SALDO >= 0",
          "columns": ["VL_SALDO"]
        }
      ],

      "relationships": [
        {
          "name": "empresa",
          "type": "many-to-one",
          "target_table": "EMPRESA",
          "target_model": "Empresa",
          "local_columns": ["ID_EMPRESA"],
          "remote_columns": ["ID_EMPRESA"],
          "back_populates": "usuarios",
          "lazy": "select",
          "cascade": null
        },
        {
          "name": "pedidos",
          "type": "one-to-many",
          "target_table": "PEDIDO",
          "target_model": "Pedido",
          "local_columns": ["ID_USUARIO"],
          "remote_columns": ["ID_USUARIO"],
          "back_populates": "usuario",
          "lazy": "dynamic",
          "cascade": "all, delete-orphan"
        },
        {
          "name": "perfis",
          "type": "many-to-many",
          "target_table": "PERFIL",
          "target_model": "Perfil",
          "junction_table": "USUARIO_PERFIL",
          "local_columns": ["ID_USUARIO"],
          "remote_columns": ["ID_PERFIL"],
          "back_populates": "usuarios",
          "lazy": "select",
          "cascade": null
        }
      ],

      "triggers": [
        {
          "name": "trg_usuario_audit",
          "timing": "AFTER",
          "events": ["INSERT", "UPDATE", "DELETE"],
          "for_each": "ROW",
          "function": "fn_audit_log",
          "condition": null
        }
      ],

      "table_options": {
        "schema": "public",
        "tablespace": null,
        "comment": "System users table",
        "inherits": null,
        "partition_by": null
      }
    }
  ],

  "views": [
    {
      "name": "VW_USUARIOS_ATIVOS",
      "legacy_name": "VW_USUARIOS_ATIVOS",
      "model_file": null,
      "definition": "SELECT * FROM USUARIO WHERE BL_ATIVO = true",
      "materialized": false,
      "columns": [
        {
          "name": "ID_USUARIO",
          "type": {"base": "integer"}
        }
      ]
    }
  ],

  "sequences": [
    {
      "name": "seq_usuario_id",
      "start": 1,
      "increment": 1,
      "min_value": 1,
      "max_value": null,
      "cycle": false,
      "owned_by": "USUARIO.ID_USUARIO"
    }
  ],

  "functions": [
    {
      "name": "fn_calcula_idade",
      "legacy_name": "FN_CALCULA_IDADE",
      "parameters": [
        {"name": "p_data_nascimento", "type": "date", "mode": "IN"}
      ],
      "return_type": "integer",
      "language": "SQL",
      "volatility": "STABLE",
      "definition": "SELECT EXTRACT(YEAR FROM AGE(p_data_nascimento))::INTEGER"
    }
  ],

  "procedures": [
    {
      "name": "sp_atualiza_saldos",
      "legacy_name": "SP_ATUALIZA_SALDOS",
      "parameters": [
        {"name": "p_empresa_id", "type": "integer", "mode": "IN"},
        {"name": "p_resultado", "type": "integer", "mode": "OUT"}
      ],
      "language": "PLPGSQL"
    }
  ],

  "composite_types": [
    {
      "name": "tp_endereco",
      "legacy_name": "TP_ENDERECO",
      "attributes": [
        {"name": "logradouro", "type": "varchar(200)"},
        {"name": "numero", "type": "varchar(20)"},
        {"name": "cidade", "type": "varchar(100)"},
        {"name": "uf", "type": "char(2)"},
        {"name": "cep", "type": "char(8)"}
      ]
    }
  ],

  "domains": [
    {
      "name": "dm_cpf",
      "base_type": "char(11)",
      "nullable": false,
      "check": "VALUE ~ '^[0-9]{11}$'"
    }
  ],

  "extensions": [
    {
      "name": "uuid-ossp",
      "version": "1.1",
      "schema": "public"
    }
  ],

  "statistics": {
    "total_tables": 45,
    "total_columns": 523,
    "total_relationships": 67,
    "total_indexes": 89,
    "total_foreign_keys": 52,
    "total_enums": 8,
    "total_views": 5,
    "total_functions": 12,
    "total_procedures": 3
  }
}
```

</dashboard_schema>

<type_mappings>
## Base Type Normalization

All ORM-specific types are normalized to these base types:

| Base Type | SQLAlchemy | Prisma | TypeORM | Django | Sequelize |
|-----------|------------|--------|---------|--------|-----------|
| `integer` | Integer, BigInteger, SmallInteger | Int, BigInt | int, bigint | IntegerField, BigIntegerField | INTEGER, BIGINT |
| `string` | String(n), VARCHAR | String | varchar | CharField | STRING |
| `text` | Text | String | text | TextField | TEXT |
| `decimal` | Numeric(p,s), DECIMAL | Decimal | decimal | DecimalField | DECIMAL |
| `float` | Float, Double | Float | float, double | FloatField | FLOAT, DOUBLE |
| `boolean` | Boolean | Boolean | boolean | BooleanField | BOOLEAN |
| `date` | Date | DateTime | date | DateField | DATEONLY |
| `time` | Time | DateTime | time | TimeField | TIME |
| `datetime` | DateTime | DateTime | timestamp, datetime | DateTimeField | DATE |
| `binary` | LargeBinary, BLOB | Bytes | blob, bytea | BinaryField | BLOB |
| `uuid` | UUID | String | uuid | UUIDField | UUID |
| `json` | JSON, JSONB | Json | json, jsonb | JSONField | JSON |
| `array` | ARRAY | (type)[] | simple-array | ArrayField | ARRAY |
| `enum` | Enum | enum | enum | (choices) | ENUM |

</type_mappings>

<process>

## Step 1: Verify Project Context

```bash
test -f .planning/CONVERSION.md && echo "conversion" || echo "greenfield"
```

**If greenfield:** Error - no legacy schema to compare.

Read CONVERSION.md for:
- `output_project_id`
- `legacy_project`

## Step 2: Detect Stack and Models Location

Get stack from config or detect:

```bash
# Check for common patterns
test -f pyproject.toml && grep -q "sqlalchemy" pyproject.toml && echo "sqlalchemy"
test -f prisma/schema.prisma && echo "prisma"
test -f package.json && grep -q "typeorm" package.json && echo "typeorm"
test -f manage.py && echo "django"
test -f package.json && grep -q "sequelize" package.json && echo "sequelize"
```

Set `models_location` based on stack:
- SQLAlchemy: `app/models/`
- Prisma: `prisma/schema.prisma`
- TypeORM: `src/models/` or `src/entities/`
- Django: `**/models.py`
- Sequelize: `src/models/`

## Step 3: Parse Models by Stack

### SQLAlchemy Parser

```python
# Parse each .py file in models directory
# Look for:
# - class X(Base): → table
# - __tablename__ = "Y" → legacy_name
# - Column(...) → columns with all attributes
# - relationship(...) → relationships
# - Index(...) → indexes
# - UniqueConstraint(...) → unique constraints
# - CheckConstraint(...) → check constraints
# - ForeignKey(...) → foreign keys
```

### Prisma Parser

```prisma
# Parse schema.prisma
# Look for:
# - model X { → table
# - @@map("Y") → legacy_name
# - field @map("Y") → column legacy name
# - @relation(...) → relationships
# - @@index([...]) → indexes
# - @@unique([...]) → unique constraints
# - enum X { → enums
```

### TypeORM Parser

```typescript
# Parse each .ts file
# Look for:
# - @Entity({ name: "Y" }) → table with legacy_name
# - @Column({ name: "Y", ... }) → columns
# - @PrimaryGeneratedColumn() → auto_increment PK
# - @ManyToOne, @OneToMany, @ManyToMany → relationships
# - @Index() → indexes
# - @Unique() → unique constraints
```

### Django Parser

```python
# Parse models.py files
# Look for:
# - class X(models.Model): → table
# - class Meta: db_table = "Y" → legacy_name
# - models.Field(db_column="Y") → column legacy name
# - ForeignKey, ManyToManyField → relationships
# - class Meta: indexes, constraints → indexes/constraints
```

### Sequelize Parser

```typescript
# Parse each model file
# Look for:
# - Model.init({ ... }, { tableName: "Y" }) → table
# - field: { field: "Y" } → column legacy name
# - DataTypes.X → column types
# - Model.belongsTo, hasMany, belongsToMany → relationships
```

## Step 4: Get Legacy Schema from MCP

```
mcp__wxcode-kb__get_schema(project_name)
```

Compare parsed models against legacy:
- Identify missing tables
- Identify extra tables (not in legacy)
- Calculate coverage percentage

## Step 5: Build Dashboard JSON

Construct the full JSON object following the schema above.

Ensure all fields are populated:
- Use `null` for optional fields that don't apply
- Use empty arrays `[]` for collections with no items
- Include all parsed details

## Step 6: Write Dashboard File

Write to `.planning/schema-dashboard.json`:

```bash
# Pretty-print with 2-space indent
# Write JSON file
```

**Emit watcher notification for schema dashboard:**
```
[WXCODE:SCHEMA_DASHBOARD_UPDATED] .planning/schema-dashboard.json
```

Also generate human-readable summary in `.planning/SCHEMA-STATUS.md`:

**Emit watcher notification for status file:**
```
[WXCODE:SCHEMA_STATUS_UPDATED] .planning/SCHEMA-STATUS.md
```

```markdown
# Schema Status

**Generated:** 2026-02-05 10:30:00
**Stack:** fastapi-sqlalchemy (SQLAlchemy 2.0)

## Coverage

| Metric | Count |
|--------|-------|
| Legacy Tables | 50 |
| Models Generated | 45 |
| Coverage | 90% |

## Missing Tables

- TABLE_X
- TABLE_Y

## Model Summary

| Table | Columns | Relationships | Indexes |
|-------|---------|---------------|---------|
| USUARIO | 12 | 3 | 4 |
| PEDIDO | 15 | 5 | 6 |
...

## Validation Issues

(none)
```

## Step 7: Report Completion

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Dashboard generated with N tables"} -->

## ✓ Schema Dashboard Generated

**File:** `.planning/schema-dashboard.json`
**Summary:** `.planning/SCHEMA-STATUS.md`

**Coverage:** [N]/[M] tables ([P]%)
**Statistics:**
- Tables: [N]
- Columns: [N]
- Relationships: [N]
- Indexes: [N]
```

</process>

<success_criteria>
- [ ] Correctly detects stack and ORM
- [ ] Parses all model files for the stack
- [ ] Extracts ALL schema elements (columns, PKs, FKs, indexes, constraints, relationships)
- [ ] Normalizes types to base types
- [ ] Preserves ORM-specific type info in `raw` and `orm_specific`
- [ ] Compares against legacy schema for coverage
- [ ] Outputs valid JSON following the schema
- [ ] Emits `[WXCODE:SCHEMA_DASHBOARD_UPDATED]` notification
- [ ] Emits `[WXCODE:SCHEMA_STATUS_UPDATED]` notification
- [ ] Generates human-readable SCHEMA-STATUS.md
</success_criteria>
