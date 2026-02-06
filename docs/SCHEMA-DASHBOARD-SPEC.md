# Schema Dashboard JSON Specification

**Version:** 1.0.0
**Date:** 2026-02-05
**Purpose:** Stack-agnostic representation of database models for UI consumption.

---

## 1. Overview

The Schema Dashboard is a JSON file (`.planning/schema-dashboard.json`) that provides a unified view of all database models in a conversion project, regardless of the underlying ORM (SQLAlchemy, Prisma, TypeORM, Django, Sequelize).

### 1.1 Design Goals

1. **Stack-Agnostic:** UI doesn't need to understand specific ORMs
2. **Complete:** Captures ALL database schema elements
3. **Normalized:** Types mapped to common base types
4. **Traceable:** Links models back to legacy schema
5. **Actionable:** Includes coverage and validation status

### 1.2 File Locations

| File | Format | Purpose |
|------|--------|---------|
| `.planning/schema-dashboard.json` | JSON | Machine-readable, UI consumption |
| `.planning/SCHEMA-STATUS.md` | Markdown | Human-readable summary |

---

## 2. Root Schema

```json
{
  "$schema": "https://wxcode.dev/schemas/dashboard-v1.json",
  "version": "1.0.0",
  "generated_at": "2026-02-05T10:30:00Z",
  "project": { ... },
  "stack": { ... },
  "coverage": { ... },
  "connections": [ ... ],
  "enums": [ ... ],
  "tables": [ ... ],
  "views": [ ... ],
  "sequences": [ ... ],
  "functions": [ ... ],
  "procedures": [ ... ],
  "composite_types": [ ... ],
  "domains": [ ... ],
  "extensions": [ ... ],
  "statistics": { ... }
}
```

### 2.1 Root Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | No | JSON Schema URL for validation |
| `version` | string | Yes | Spec version (semver) |
| `generated_at` | string | Yes | ISO 8601 timestamp |
| `project` | object | Yes | Project identification |
| `stack` | object | Yes | Technology stack info |
| `coverage` | object | Yes | Schema coverage metrics |
| `connections` | array | Yes | Database connections |
| `enums` | array | Yes | Enum types |
| `tables` | array | Yes | Table definitions |
| `views` | array | Yes | View definitions |
| `sequences` | array | Yes | Sequence definitions |
| `functions` | array | Yes | Function definitions |
| `procedures` | array | Yes | Stored procedure definitions |
| `composite_types` | array | Yes | Custom composite types |
| `domains` | array | Yes | Domain types |
| `extensions` | array | Yes | Database extensions |
| `statistics` | object | Yes | Aggregate statistics |

---

## 3. Project Object

Identifies the project context.

```json
{
  "project": {
    "name": "Limpax ADM",
    "output_project_id": "507f1f77bcf86cd799439011",
    "legacy_project": "LIMPAX_ADM"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable project name |
| `output_project_id` | string | Yes | MongoDB ObjectId from WXCODE KB |
| `legacy_project` | string | Yes | Legacy WinDev/WebDev project name |

---

## 4. Stack Object

Describes the technology stack.

```json
{
  "stack": {
    "id": "fastapi-sqlalchemy",
    "orm": "SQLAlchemy",
    "orm_version": "2.0",
    "database_type": "postgresql",
    "models_location": "app/models/"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Stack identifier from WXCODE |
| `orm` | string | Yes | ORM name |
| `orm_version` | string | No | ORM version if detectable |
| `database_type` | string | Yes | Database type (postgresql, mysql, sqlserver, sqlite) |
| `models_location` | string | Yes | Path to model files |

### 4.1 Supported Stacks

| Stack ID | ORM | Models Location |
|----------|-----|-----------------|
| `fastapi-sqlalchemy` | SQLAlchemy | `app/models/` |
| `fastapi-react` | SQLAlchemy | `backend/app/models/` |
| `django-templates` | Django ORM | `*/models.py` |
| `nextjs-app-router` | Prisma | `prisma/schema.prisma` |
| `nextjs-pages` | Prisma | `prisma/schema.prisma` |
| `nuxt3` | Prisma | `prisma/schema.prisma` |
| `nestjs-react` | TypeORM | `src/entities/` |
| `nestjs-vue` | TypeORM | `src/entities/` |
| `sveltekit` | Prisma | `prisma/schema.prisma` |
| `remix` | Prisma | `prisma/schema.prisma` |
| `laravel-blade` | Eloquent | `app/Models/` |
| `laravel-react` | Eloquent | `app/Models/` |
| `rails-erb` | ActiveRecord | `app/models/` |

---

## 5. Coverage Object

Schema coverage metrics.

```json
{
  "coverage": {
    "legacy_tables": 50,
    "models_generated": 45,
    "models_validated": 45,
    "percentage": 90.0,
    "missing_tables": ["TABLE_X", "TABLE_Y"],
    "extra_tables": ["LOCAL_CACHE"]
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `legacy_tables` | integer | Yes | Total tables in legacy schema |
| `models_generated` | integer | Yes | Models created in new project |
| `models_validated` | integer | Yes | Models passing validation |
| `percentage` | number | Yes | Coverage percentage (0-100) |
| `missing_tables` | array | Yes | Legacy tables without models |
| `extra_tables` | array | Yes | Models without legacy tables |

---

## 6. Connections Array

Database connection configurations.

```json
{
  "connections": [
    {
      "name": "default",
      "database_type": "postgresql",
      "host": "localhost",
      "port": 5432,
      "database": "limpax_db",
      "schema": "public",
      "user": "app_user"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Connection identifier |
| `database_type` | string | Yes | Database type |
| `host` | string | Yes | Database host |
| `port` | integer | Yes | Database port |
| `database` | string | Yes | Database name |
| `schema` | string | No | Default schema (PostgreSQL) |
| `user` | string | No | Database user (no password!) |

---

## 7. Enums Array

Enumeration type definitions.

```json
{
  "enums": [
    {
      "name": "StatusPedido",
      "legacy_name": "STATUS_PEDIDO",
      "model_file": "app/models/enums.py",
      "values": [
        {"name": "PENDING", "value": "P", "label": "Pendente"},
        {"name": "APPROVED", "value": "A", "label": "Aprovado"},
        {"name": "CANCELLED", "value": "C", "label": "Cancelado"}
      ]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Model enum name |
| `legacy_name` | string | Yes | Legacy enum/table name |
| `model_file` | string | No | File where enum is defined |
| `values` | array | Yes | Enum value definitions |
| `values[].name` | string | Yes | Code-friendly name |
| `values[].value` | string | Yes | Database value |
| `values[].label` | string | No | Human-readable label |

---

## 8. Tables Array

Table/entity definitions - the core of the dashboard.

```json
{
  "tables": [
    {
      "name": "Usuario",
      "legacy_name": "USUARIO",
      "model_file": "app/models/usuario.py",
      "status": "validated",
      "description": "System users table",
      "columns": [ ... ],
      "primary_key": { ... },
      "foreign_keys": [ ... ],
      "indexes": [ ... ],
      "unique_constraints": [ ... ],
      "check_constraints": [ ... ],
      "relationships": [ ... ],
      "triggers": [ ... ],
      "table_options": { ... }
    }
  ]
}
```

### 8.1 Table Root Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Model class name |
| `legacy_name` | string | Yes | Exact legacy table name |
| `model_file` | string | Yes | Path to model file |
| `status` | string | Yes | Status: `generated`, `validated`, `error` |
| `description` | string | No | Table description/comment |
| `columns` | array | Yes | Column definitions |
| `primary_key` | object | Yes | Primary key definition |
| `foreign_keys` | array | Yes | Foreign key constraints |
| `indexes` | array | Yes | Index definitions |
| `unique_constraints` | array | Yes | Unique constraints |
| `check_constraints` | array | Yes | Check constraints |
| `relationships` | array | Yes | ORM relationships |
| `triggers` | array | Yes | Trigger definitions |
| `table_options` | object | Yes | Table-level options |

### 8.2 Column Object

```json
{
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
      "computed": null,
      "foreign_key": null
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Column name in model |
| `legacy_name` | string | Yes | Exact legacy column name |
| `type` | object | Yes | Type information (see 8.2.1) |
| `nullable` | boolean | Yes | Allows NULL values |
| `primary_key` | boolean | Yes | Part of primary key |
| `auto_increment` | boolean | Yes | Auto-incrementing |
| `unique` | boolean | Yes | Has unique constraint |
| `default` | any | No | Application default value |
| `server_default` | string | No | Database default expression |
| `comment` | string | No | Column comment |
| `computed` | object | No | Computed column definition |
| `foreign_key` | object | No | FK reference if applicable |

#### 8.2.1 Type Object

```json
{
  "type": {
    "base": "decimal",
    "raw": "Numeric(19,4)",
    "orm_specific": "Column(Numeric(19, 4))",
    "size": null,
    "precision": 19,
    "scale": 4
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `base` | string | Yes | Normalized base type (see 8.2.2) |
| `raw` | string | Yes | ORM type as written |
| `orm_specific` | string | Yes | Full ORM declaration |
| `size` | integer | No | For string types: max length |
| `precision` | integer | No | For decimal types: total digits |
| `scale` | integer | No | For decimal types: decimal places |

#### 8.2.2 Base Types

All ORM-specific types are normalized to these base types:

| Base Type | Description | Examples |
|-----------|-------------|----------|
| `integer` | Whole numbers | int, bigint, smallint, tinyint |
| `string` | Variable-length text | varchar, char, nvarchar |
| `text` | Unlimited text | text, longtext, clob |
| `decimal` | Exact numeric | decimal, numeric, money |
| `float` | Approximate numeric | float, double, real |
| `boolean` | True/false | boolean, bit, tinyint(1) |
| `date` | Date only | date |
| `time` | Time only | time |
| `datetime` | Date and time | datetime, timestamp |
| `binary` | Binary data | blob, bytea, varbinary |
| `uuid` | UUID/GUID | uuid, uniqueidentifier |
| `json` | JSON data | json, jsonb |
| `array` | Array types | array, simple-array |
| `enum` | Enumeration | enum |

#### 8.2.3 Computed Column

```json
{
  "computed": {
    "expression": "CONCAT(first_name, ' ', last_name)",
    "stored": true,
    "type": {"base": "string"}
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `expression` | string | Yes | SQL expression |
| `stored` | boolean | Yes | Persisted or virtual |
| `type` | object | Yes | Result type |

#### 8.2.4 Foreign Key Reference (in column)

```json
{
  "foreign_key": {
    "table": "EMPRESA",
    "column": "ID_EMPRESA"
  }
}
```

### 8.3 Primary Key Object

```json
{
  "primary_key": {
    "name": "pk_usuario",
    "columns": ["ID_USUARIO"],
    "auto_generated_name": true
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Constraint name |
| `columns` | array | Yes | Column names in PK |
| `auto_generated_name` | boolean | Yes | Name auto-generated by DB |

### 8.4 Foreign Keys Array

```json
{
  "foreign_keys": [
    {
      "name": "fk_usuario_empresa",
      "columns": ["ID_EMPRESA"],
      "references_table": "EMPRESA",
      "references_columns": ["ID_EMPRESA"],
      "on_delete": "RESTRICT",
      "on_update": "CASCADE",
      "deferrable": false,
      "initially_deferred": false
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Constraint name |
| `columns` | array | Yes | Local column(s) |
| `references_table` | string | Yes | Referenced table |
| `references_columns` | array | Yes | Referenced column(s) |
| `on_delete` | string | Yes | Delete action |
| `on_update` | string | Yes | Update action |
| `deferrable` | boolean | No | Can be deferred |
| `initially_deferred` | boolean | No | Deferred by default |

#### 8.4.1 Referential Actions

| Action | Description |
|--------|-------------|
| `NO ACTION` | Reject if references exist (default) |
| `RESTRICT` | Reject if references exist (immediate) |
| `CASCADE` | Delete/update referenced rows |
| `SET NULL` | Set FK columns to NULL |
| `SET DEFAULT` | Set FK columns to default |

### 8.5 Indexes Array

```json
{
  "indexes": [
    {
      "name": "idx_usuario_email",
      "columns": ["DS_EMAIL"],
      "unique": true,
      "type": "btree",
      "where": null,
      "include": null,
      "using": null
    },
    {
      "name": "idx_usuario_nome_ativo",
      "columns": ["NM_USUARIO", "BL_ATIVO"],
      "unique": false,
      "type": "btree",
      "where": "BL_ATIVO = true",
      "include": ["DS_EMAIL"],
      "using": null
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Index name |
| `columns` | array | Yes | Indexed columns |
| `unique` | boolean | Yes | Unique index |
| `type` | string | No | Index type (btree, hash, gin, gist) |
| `where` | string | No | Partial index condition |
| `include` | array | No | Included columns (covering index) |
| `using` | string | No | Index method |

### 8.6 Unique Constraints Array

```json
{
  "unique_constraints": [
    {
      "name": "uq_usuario_cpf",
      "columns": ["NR_CPF"]
    },
    {
      "name": "uq_usuario_email_empresa",
      "columns": ["DS_EMAIL", "ID_EMPRESA"]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Constraint name |
| `columns` | array | Yes | Columns in constraint |

### 8.7 Check Constraints Array

```json
{
  "check_constraints": [
    {
      "name": "ck_usuario_saldo_positivo",
      "expression": "VL_SALDO >= 0",
      "columns": ["VL_SALDO"]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | Constraint name |
| `expression` | string | Yes | Check expression |
| `columns` | array | No | Columns involved |

### 8.8 Relationships Array

ORM relationship definitions.

```json
{
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
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Relationship property name |
| `type` | string | Yes | Relationship type |
| `target_table` | string | Yes | Related legacy table |
| `target_model` | string | Yes | Related model class |
| `local_columns` | array | Yes | Columns on this side |
| `remote_columns` | array | Yes | Columns on related side |
| `junction_table` | string | No | For many-to-many: join table |
| `back_populates` | string | No | Inverse relationship name |
| `lazy` | string | No | Loading strategy |
| `cascade` | string | No | Cascade options |

#### 8.8.1 Relationship Types

| Type | Description |
|------|-------------|
| `one-to-one` | Single related record |
| `many-to-one` | FK on this table |
| `one-to-many` | FK on related table |
| `many-to-many` | Through junction table |

#### 8.8.2 Lazy Loading Options

| Option | Description |
|--------|-------------|
| `select` | Load on first access (default) |
| `joined` | Load via JOIN |
| `subquery` | Load via subquery |
| `dynamic` | Return query instead of list |
| `raise` | Raise error if accessed |
| `noload` | Never load |

### 8.9 Triggers Array

```json
{
  "triggers": [
    {
      "name": "trg_usuario_audit",
      "timing": "AFTER",
      "events": ["INSERT", "UPDATE", "DELETE"],
      "for_each": "ROW",
      "function": "fn_audit_log",
      "condition": null
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Trigger name |
| `timing` | string | Yes | BEFORE, AFTER, INSTEAD OF |
| `events` | array | Yes | INSERT, UPDATE, DELETE, TRUNCATE |
| `for_each` | string | Yes | ROW or STATEMENT |
| `function` | string | Yes | Trigger function name |
| `condition` | string | No | WHEN condition |

### 8.10 Table Options Object

```json
{
  "table_options": {
    "schema": "public",
    "tablespace": null,
    "comment": "System users table",
    "inherits": null,
    "partition_by": null,
    "managed": true
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema` | string | No | Database schema |
| `tablespace` | string | No | Tablespace name |
| `comment` | string | No | Table comment |
| `inherits` | string | No | Parent table (PostgreSQL) |
| `partition_by` | object | No | Partitioning config |
| `managed` | boolean | No | ORM manages table (Django) |

---

## 9. Views Array

```json
{
  "views": [
    {
      "name": "VwUsuariosAtivos",
      "legacy_name": "VW_USUARIOS_ATIVOS",
      "model_file": null,
      "materialized": false,
      "definition": "SELECT * FROM USUARIO WHERE BL_ATIVO = true",
      "columns": [
        {"name": "ID_USUARIO", "type": {"base": "integer"}},
        {"name": "NM_USUARIO", "type": {"base": "string"}}
      ],
      "dependencies": ["USUARIO"]
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | View name in model |
| `legacy_name` | string | Yes | Legacy view name |
| `model_file` | string | No | Path if mapped to model |
| `materialized` | boolean | Yes | Materialized view |
| `definition` | string | No | SQL definition |
| `columns` | array | Yes | View columns |
| `dependencies` | array | No | Tables/views used |

---

## 10. Sequences Array

```json
{
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
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Sequence name |
| `start` | integer | Yes | Starting value |
| `increment` | integer | Yes | Increment by |
| `min_value` | integer | No | Minimum value |
| `max_value` | integer | No | Maximum value |
| `cycle` | boolean | Yes | Cycle when exhausted |
| `owned_by` | string | No | Owner column |

---

## 11. Functions Array

```json
{
  "functions": [
    {
      "name": "fn_calcula_idade",
      "legacy_name": "FN_CALCULA_IDADE",
      "parameters": [
        {"name": "p_data_nascimento", "type": "date", "mode": "IN", "default": null}
      ],
      "return_type": "integer",
      "return_set": false,
      "language": "SQL",
      "volatility": "STABLE",
      "definition": "SELECT EXTRACT(YEAR FROM AGE(p_data_nascimento))::INTEGER"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Function name |
| `legacy_name` | string | Yes | Legacy function name |
| `parameters` | array | Yes | Input parameters |
| `return_type` | string | Yes | Return type |
| `return_set` | boolean | Yes | Returns set of rows |
| `language` | string | Yes | Language (SQL, PLPGSQL, etc.) |
| `volatility` | string | No | IMMUTABLE, STABLE, VOLATILE |
| `definition` | string | No | Function body |

### 11.1 Parameter Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Parameter name |
| `type` | string | Yes | Parameter type |
| `mode` | string | Yes | IN, OUT, INOUT, VARIADIC |
| `default` | any | No | Default value |

---

## 12. Procedures Array

```json
{
  "procedures": [
    {
      "name": "sp_atualiza_saldos",
      "legacy_name": "SP_ATUALIZA_SALDOS",
      "parameters": [
        {"name": "p_empresa_id", "type": "integer", "mode": "IN"},
        {"name": "p_resultado", "type": "integer", "mode": "OUT"}
      ],
      "language": "PLPGSQL",
      "definition": null
    }
  ]
}
```

Same structure as functions, but no return type.

---

## 13. Composite Types Array

```json
{
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
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Type name |
| `legacy_name` | string | Yes | Legacy type name |
| `attributes` | array | Yes | Type attributes |

---

## 14. Domains Array

```json
{
  "domains": [
    {
      "name": "dm_cpf",
      "base_type": "char(11)",
      "nullable": false,
      "default": null,
      "check": "VALUE ~ '^[0-9]{11}$'"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Domain name |
| `base_type` | string | Yes | Underlying type |
| `nullable` | boolean | Yes | Allows NULL |
| `default` | any | No | Default value |
| `check` | string | No | Check constraint |

---

## 15. Extensions Array

```json
{
  "extensions": [
    {
      "name": "uuid-ossp",
      "version": "1.1",
      "schema": "public"
    },
    {
      "name": "postgis",
      "version": "3.1",
      "schema": "public"
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Extension name |
| `version` | string | No | Extension version |
| `schema` | string | No | Install schema |

---

## 16. Statistics Object

Aggregate metrics for quick summary.

```json
{
  "statistics": {
    "total_tables": 45,
    "total_columns": 523,
    "total_relationships": 67,
    "total_indexes": 89,
    "total_foreign_keys": 52,
    "total_enums": 8,
    "total_views": 5,
    "total_functions": 12,
    "total_procedures": 3,
    "total_sequences": 15,
    "total_triggers": 7
  }
}
```

---

## 17. Type Mapping Reference

### 17.1 SQLAlchemy to Base

| SQLAlchemy | Base Type |
|------------|-----------|
| Integer | integer |
| BigInteger | integer |
| SmallInteger | integer |
| String(n) | string |
| Text | text |
| Numeric(p,s) | decimal |
| Float | float |
| Boolean | boolean |
| Date | date |
| Time | time |
| DateTime | datetime |
| LargeBinary | binary |
| UUID | uuid |
| JSON | json |
| ARRAY | array |
| Enum | enum |

### 17.2 Prisma to Base

| Prisma | Base Type |
|--------|-----------|
| Int | integer |
| BigInt | integer |
| String | string |
| Decimal | decimal |
| Float | float |
| Boolean | boolean |
| DateTime | datetime |
| Bytes | binary |
| Json | json |

### 17.3 TypeORM to Base

| TypeORM | Base Type |
|---------|-----------|
| int, bigint | integer |
| varchar | string |
| text | text |
| decimal | decimal |
| float, double | float |
| boolean | boolean |
| date | date |
| time | time |
| timestamp, datetime | datetime |
| bytea, blob | binary |
| uuid | uuid |
| json, jsonb | json |

### 17.4 Django to Base

| Django | Base Type |
|--------|-----------|
| IntegerField, BigIntegerField | integer |
| CharField | string |
| TextField | text |
| DecimalField | decimal |
| FloatField | float |
| BooleanField | boolean |
| DateField | date |
| TimeField | time |
| DateTimeField | datetime |
| BinaryField | binary |
| UUIDField | uuid |
| JSONField | json |

---

## 18. Example: Complete Dashboard

See `.planning/schema-dashboard.json` in any conversion project for a real example.

---

## 19. Versioning

This spec follows semantic versioning:

- **MAJOR:** Breaking changes to structure
- **MINOR:** New fields (backward compatible)
- **PATCH:** Clarifications and fixes

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-05 | Initial specification |

---

## 20. UI Integration

### 20.1 Reading the Dashboard

```typescript
// Example: TypeScript UI code
interface SchemaDashboard {
  version: string;
  generated_at: string;
  coverage: Coverage;
  tables: Table[];
  // ... other fields
}

async function loadSchema(): Promise<SchemaDashboard> {
  const content = await fs.readFile('.planning/schema-dashboard.json', 'utf-8');
  return JSON.parse(content);
}
```

### 20.2 Displaying Coverage

```typescript
function renderCoverage(coverage: Coverage) {
  return {
    percentage: coverage.percentage,
    status: coverage.percentage === 100 ? 'complete' : 'incomplete',
    missing: coverage.missing_tables.length,
  };
}
```

### 20.3 Rendering Table Details

The UI can render any table uniformly using the `base` type for icons/colors and `orm_specific` for technical details.

### 20.4 Watcher Notifications

WXCODE commands emit notifications when files are updated, allowing UI to react in real-time.

#### Schema Dashboard Notifications

```
[WXCODE:SCHEMA_DASHBOARD_UPDATED] .planning/schema-dashboard.json
[WXCODE:SCHEMA_STATUS_UPDATED] .planning/SCHEMA-STATUS.md
```

#### Design System Notifications

```
[WXCODE:DESIGN_TOKENS_UPDATED] design/tokens.json
[WXCODE:DESIGN_VARIABLES_UPDATED] design/variables.css
```

**UI Integration:**

```typescript
// Watch for WXCODE updates
function watchWxcodeUpdates(output: string) {
  // Schema updates
  const dashboardMatch = output.match(/\[WXCODE:SCHEMA_DASHBOARD_UPDATED\] (.+)/);
  if (dashboardMatch) {
    reloadSchemaDashboard(dashboardMatch[1]);
  }

  const statusMatch = output.match(/\[WXCODE:SCHEMA_STATUS_UPDATED\] (.+)/);
  if (statusMatch) {
    reloadSchemaStatus(statusMatch[1]);
  }

  // Design system updates
  const tokensMatch = output.match(/\[WXCODE:DESIGN_TOKENS_UPDATED\] (.+)/);
  if (tokensMatch) {
    reloadDesignTokens(tokensMatch[1]);
  }

  const variablesMatch = output.match(/\[WXCODE:DESIGN_VARIABLES_UPDATED\] (.+)/);
  if (variablesMatch) {
    reloadDesignVariables(variablesMatch[1]);
  }
}
```

**Notification Events:**

| Notification | File | Trigger |
|--------------|------|---------|
| `SCHEMA_DASHBOARD_UPDATED` | `.planning/schema-dashboard.json` | Dashboard regenerated |
| `SCHEMA_STATUS_UPDATED` | `.planning/SCHEMA-STATUS.md` | Status summary regenerated |
| `DESIGN_TOKENS_UPDATED` | `design/tokens.json` | Design tokens generated/updated |
| `DESIGN_VARIABLES_UPDATED` | `design/variables.css` | CSS variables generated/updated |

**Emitted by:**

| Command/Agent | Notifications |
|---------------|---------------|
| `/wxcode:schema-dashboard` | `SCHEMA_DASHBOARD_UPDATED`, `SCHEMA_STATUS_UPDATED` |
| `/wxcode:dashboard --all` | All schema notifications (via schema-dashboard) |
| `/wxcode:design-system` | `DESIGN_TOKENS_UPDATED`, `DESIGN_VARIABLES_UPDATED` |
| `wxcode-schema-generator` | Schema notifications (after generate/validate) |

---

## 21. Related Commands

| Command | Description |
|---------|-------------|
| `/wxcode:schema-dashboard` | Regenerate the dashboard |
| `/wxcode:validate-schema` | Validate models against legacy |
| `/wxcode:validate-schema --fix` | Generate missing models |
