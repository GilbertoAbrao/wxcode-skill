# Structure Preservation Guidelines

Generate code that feels **familiar** to users of the legacy system.
The converted code should be recognizable, not alien.

## Core Principle

> The user who maintained the WinDev code should feel comfortable
> maintaining the converted code. Preserve semantics, adapt syntax.

---

## Traceability Comments (MANDATORY)

Every converted file MUST include `@legacy` comments to enable bidirectional navigation between legacy and converted code.

### Why This Matters

- **Grep-friendly:** `grep -r "@legacy: PAGE_Login" .` finds all related code
- **IDE navigation:** Tools can parse and provide jump-to-legacy features
- **Git blame context:** Developers understand the original intent
- **Validation:** CI can verify all conversions are properly traced

### File-Level Header (Required)

At the top of every converted file:

```python
# @legacy-element: PAGE_Login
# @legacy-type: page
# @legacy-controls: EDT_Usuario, EDT_Senha, BTN_Entrar
# @legacy-procedures: Local_Login, Global_FazLoginUsuarioInterno
# @legacy-tables: USUARIO
```

```html
<!-- @legacy-element: PAGE_Login -->
<!-- @legacy-type: page -->
<!-- @legacy-controls: EDT_Usuario, EDT_Senha, BTN_Entrar -->
```

### Function/Method Level (Required for converted procedures)

```python
# @legacy: Global_FazLoginUsuarioInterno
# @legacy-params: sLogin, sSenha -> login: str, senha: str
async def fazer_login_usuario_interno(login: str, senha: str, db: Session) -> Usuario:
    """
    Authenticates user with login and password.

    Legacy: ServerProcedures.Global_FazLoginUsuarioInterno
    """
    ...
```

### Control Mapping in Templates (Required)

```html
<form method="post" action="/login">
    <!-- @legacy: EDT_Usuario | USUARIO.LOGIN -->
    <input type="text" name="usuario" id="usuario" required>

    <!-- @legacy: EDT_Senha -->
    <input type="password" name="senha" id="senha" required>

    <!-- @legacy: BTN_Entrar.OnClick -> POST /login -->
    <button type="submit" id="btn-entrar">Entrar</button>
</form>
```

### Inline Code References (When relevant)

```python
async def login(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    login = form.get("usuario")
    senha = form.get("senha")

    # @legacy: Global_FazLoginUsuarioInterno
    usuario = await fazer_login_usuario_interno(login, senha, db)

    if not usuario:
        # @legacy: PAGE_Login.Local_Login error handling
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # @legacy: Global_SetaTempoSessao
    request.session["user_id"] = usuario.id
    request.session["timeout"] = datetime.now() + timedelta(hours=8)

    return RedirectResponse("/dashboard", status_code=303)
```

### Model/Schema Files

```python
# @legacy-element: TABLE:USUARIO
# @legacy-type: table

class Usuario(Base):
    """
    User account for system authentication.

    Legacy: USUARIO table from BD.wda
    """
    __tablename__ = "usuario"

    # @legacy: USUARIO.ID (auto-increment)
    id: Mapped[int] = mapped_column(primary_key=True)

    # @legacy: USUARIO.LOGIN (unique, indexed)
    login: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    # @legacy: USUARIO.SENHA (was plaintext, now hashed)
    senha_hash: Mapped[str] = mapped_column(String(255))

    # @legacy: USUARIO.NOME
    nome: Mapped[str] = mapped_column(String(100))

    # @legacy: USUARIO.ATIVO
    ativo: Mapped[bool] = mapped_column(default=True)
```

### Comment Format Reference

| Tag | Usage | Example |
|-----|-------|---------|
| `@legacy-element` | File header - source element name | `PAGE_Login`, `ServerProcedures` |
| `@legacy-type` | Element type | `page`, `procedure_group`, `table`, `class` |
| `@legacy-controls` | UI controls in this file | `EDT_Usuario, BTN_Salvar` |
| `@legacy-procedures` | Procedures called/converted | `Global_ValidaCPF, Local_Salvar` |
| `@legacy-tables` | Tables accessed | `USUARIO, CLIENTE` |
| `@legacy` | Inline reference | `@legacy: Global_ValidaCPF` |
| `@legacy-params` | Parameter mapping | `sNome, nID -> nome: str, id: int` |

### Deviation Comments

When deviating from legacy behavior, document inline:

```python
# @legacy: Global_FazLoginUsuarioInterno
# @legacy-deviation: Password now hashed with bcrypt (was plaintext)
# @legacy-deviation: Returns Usuario object instead of boolean
async def fazer_login_usuario_interno(login: str, senha: str, db: Session) -> Usuario | None:
    ...
```

---

## Naming Conventions

### Element Names → File Names

| Legacy Pattern | Converted Pattern | Example |
|----------------|-------------------|---------|
| `PAGE_*` | `pages/*.py` + `templates/*.html` | `PAGE_Login` → `pages/login.py`, `templates/login.html` |
| `WIN_*` | `windows/*.py` + `templates/*.html` | `WIN_Cadastro` → `pages/cadastro.py` |
| `proc:*` | `services/*.py` | `proc:ValidaCPF` → `services/validation.py::validar_cpf()` |
| `class:*` | `domain/*.py` | `class:Cliente` → `domain/cliente.py::Cliente` |
| `TABLE:*` | `models/*.py` | `TABLE:CLIENTE` → `models/cliente.py::Cliente` |

### Procedure Names → Function Names

Preserve the semantic meaning:

| Legacy | Converted | Rule |
|--------|-----------|------|
| `ValidaCPF` | `validar_cpf()` | Portuguese verb → infinitive, snake_case |
| `CalculaDesconto` | `calcular_desconto()` | Same pattern |
| `EnviaEmail` | `enviar_email()` | Same pattern |
| `GetCliente` | `get_cliente()` | English verbs stay English |
| `IsValid` | `is_valid()` | Booleans keep prefix |

### Variable Names

WinDev uses Hungarian notation prefixes:

| Prefix | Meaning | Conversion Strategy |
|--------|---------|---------------------|
| `g` | Global | Remove or use `g_` prefix |
| `m` | Member | Remove (class context is implicit) |
| `n` | Numeric | Remove (typing handles this) |
| `s` | String | Remove (typing handles this) |
| `b` | Boolean | Keep as `is_` or `has_` prefix |
| `arr` | Array | Remove (typing handles this) |
| `st` | Structure | Remove (class handles this) |

**Examples:**

| Legacy | Option A (Modern) | Option B (Preserve Style) |
|--------|-------------------|---------------------------|
| `gnUsuarioID` | `current_user.id` | `g_usuario_id` |
| `gsUsuarioNome` | `current_user.nome` | `g_usuario_nome` |
| `mNome` | `self.nome` | `self.nome` |
| `bAtivo` | `is_ativo` | `is_ativo` |

**Decision required:** Ask user preference for global variable handling.

### Control Names → HTML Element IDs/Names

| Legacy | Converted | Example |
|--------|-----------|---------|
| `EDT_*` | `input name="*"` | `EDT_Usuario` → `<input name="usuario">` |
| `BTN_*` | `button id="btn-*"` | `BTN_Salvar` → `<button id="btn-salvar">` |
| `CHK_*` | `input type="checkbox"` | `CHK_Ativo` → `<input type="checkbox" name="ativo">` |
| `RBT_*` | `input type="radio"` | `RBT_Tipo` → `<input type="radio" name="tipo">` |
| `CMB_*` | `select` | `CMB_Estado` → `<select name="estado">` |
| `TAB_*` | `table` or tabs | Context-dependent |
| `STC_*` | `span` or `label` | Static text display |

---

## Code Organization

### Procedures → Services

Keep similar organization:

```
Legacy:                          Converted:
├── Procedures/                  ├── services/
│   ├── Validacao/              │   ├── validation.py
│   │   ├── ValidaCPF           │   │   ├── validar_cpf()
│   │   ├── ValidaCNPJ          │   │   ├── validar_cnpj()
│   │   └── ValidaEmail         │   │   └── validar_email()
│   ├── Calculo/                │   ├── calculation.py
│   │   ├── CalculaDesconto     │   │   ├── calcular_desconto()
│   │   └── CalculaJuros        │   │   └── calcular_juros()
│   └── Notificacao/            │   └── notification.py
│       └── EnviaEmail          │       └── enviar_email()
```

### Classes → Domain Models

Preserve class structure:

```wlanguage
// Legacy
class:Cliente
  mID is int
  mNome is string
  mCPF is string
  mAtivo is boolean

  PROCEDURE Valida()
  PROCEDURE Salva()
```

```python
# Converted
class Cliente:
    def __init__(self):
        self.id: int = None
        self.nome: str = None
        self.cpf: str = None
        self.ativo: bool = True

    def validar(self) -> bool:
        ...

    def salvar(self) -> None:
        ...
```

### Pages → Routes + Templates

```
Legacy:                          Converted:
├── Pages/                       ├── routes/
│   ├── PAGE_Login              │   ├── auth.py
│   ├── PAGE_Dashboard          │   │   ├── login()
│   ├── PAGE_Clientes           │   │   └── logout()
│   └── PAGE_ClienteDetalhe     │   ├── dashboard.py
│                                │   └── clientes.py
│                                │       ├── listar()
│                                │       └── detalhe()
│                                │
│                                ├── templates/
│                                │   ├── login.html
│                                │   ├── dashboard.html
│                                │   └── clientes/
│                                │       ├── lista.html
│                                │       └── detalhe.html
```

---

## Logic Preservation

### Validation Logic

Legacy validation should produce same results:

```wlanguage
// Legacy
PROCEDURE ValidaCPF(sCPF)
  IF Length(sCPF) <> 11 THEN
    RESULT False
  END
  // ... digit validation
  RESULT True
```

```python
# Converted - same logic flow
def validar_cpf(cpf: str) -> bool:
    if len(cpf) != 11:
        return False
    # ... digit validation
    return True
```

### Database Operations

Map H* functions to ORM equivalents:

| Legacy | SQLAlchemy | Description |
|--------|------------|-------------|
| `HReadFirst(TABLE)` | `db.query(Model).first()` | Read first record |
| `HReadSeek(TABLE, KEY, val)` | `db.query(Model).filter_by(key=val).first()` | Search by key |
| `HAdd(TABLE)` | `db.add(instance)` | Insert record |
| `HModify(TABLE)` | `db.commit()` | Update record |
| `HDelete(TABLE)` | `db.delete(instance)` | Delete record |
| `HExecuteQuery(QRY)` | `db.execute(text(sql))` | Execute query |

### Error Handling

```wlanguage
// Legacy
WHEN EXCEPTION IN
  HAdd(CLIENTE)
DO
  Error("Erro ao salvar: " + ExceptionInfo())
END
```

```python
# Converted
try:
    db.add(cliente)
    db.commit()
except Exception as e:
    logger.error(f"Erro ao salvar: {e}")
    raise
```

---

## UI Preservation

### Layout Structure

Preserve visual hierarchy:

```
Legacy UI (from PDF):            Converted HTML:
┌─────────────────────┐          <div class="card">
│ Dados do Cliente    │            <h2>Dados do Cliente</h2>
├─────────────────────┤            <form>
│ Nome: [___________] │              <label>Nome</label>
│ CPF:  [___________] │              <input name="nome">
│ Email:[___________] │              <label>CPF</label>
│                     │              <input name="cpf">
│ [Salvar] [Cancelar] │              <label>Email</label>
└─────────────────────┘              <input name="email">
                                     <button>Salvar</button>
                                     <button>Cancelar</button>
                                   </form>
                                 </div>
```

### Control Groupings

If legacy uses CELLs or ZONEs for grouping, preserve in HTML:

```wlanguage
// Legacy
CELL_DadosPessoais contains:
  - EDT_Nome
  - EDT_CPF

CELL_DadosProfissionais contains:
  - EDT_Empresa
  - EDT_Cargo
```

```html
<!-- Converted -->
<fieldset class="dados-pessoais">
  <legend>Dados Pessoais</legend>
  <input name="nome">
  <input name="cpf">
</fieldset>

<fieldset class="dados-profissionais">
  <legend>Dados Profissionais</legend>
  <input name="empresa">
  <input name="cargo">
</fieldset>
```

---

## When to Deviate

Deviate from legacy structure when:

### 1. Security Concerns

```wlanguage
// Legacy - SQL in UI code
sSQL = "SELECT * FROM USUARIO WHERE LOGIN='" + EDT_Usuario + "'"
```

```python
# Converted - MUST use parameterized queries
user = db.query(Usuario).filter_by(login=username).first()
```

### 2. Anti-Patterns in Target Stack

```wlanguage
// Legacy - Global state everywhere
gnUsuarioID = HRead(USUARIO, ID)
```

```python
# Converted - Use proper patterns
# Option A: Dependency injection
def get_usuario(usuario_id: int = Depends(get_current_user_id)):
    ...

# Option B: Context/session
current_user = get_current_user()
```

### 3. Performance Issues

```wlanguage
// Legacy - N+1 query pattern
FOR EACH CLIENTE
  HReadSeek(PEDIDO, CLIENTEID, CLIENTE.ID)
  // process
END
```

```python
# Converted - Use joins
clientes_com_pedidos = (
    db.query(Cliente)
    .options(joinedload(Cliente.pedidos))
    .all()
)
```

### 4. Modern Best Practices

```wlanguage
// Legacy - Inline error messages
IF NOT ValidaCPF(sCPF) THEN
  Error("CPF inválido")
END
```

```python
# Converted - Proper validation with i18n support
from pydantic import validator

class ClienteInput(BaseModel):
    cpf: str

    @validator('cpf')
    def validate_cpf(cls, v):
        if not validar_cpf(v):
            raise ValueError('CPF inválido')
        return v
```

---

## Documentation of Deviations

When deviating from legacy structure, document in SUMMARY.md:

```markdown
## Deviations from Legacy

### Security: SQL Injection Prevention
- **Legacy:** Dynamic SQL concatenation in PAGE_Login
- **Converted:** Parameterized queries via SQLAlchemy
- **Reason:** Security best practice

### Pattern: Global State Removal
- **Legacy:** gnUsuarioID global variable
- **Converted:** Dependency injection via FastAPI
- **Reason:** Testability, thread safety

### Performance: N+1 Query Fix
- **Legacy:** Loop with individual queries in PAGE_Clientes
- **Converted:** Single query with JOIN
- **Reason:** Performance (reduced from ~100 queries to 1)
```
