# WXCODE Structured Output Specification

**Versão:** 1.1.0
**Data:** 2026-02-04 (atualizado)
**Propósito:** Especificação completa para parsing de saídas WXCODE em interfaces de chat.

---

## 1. Formato Geral

Todas as saídas estruturadas usam comentários HTML (invisíveis em markdown renderers):

```
<!-- WXCODE:TYPE:JSON_PAYLOAD -->
```

### Regex para Parsing

```javascript
const WXCODE_PATTERN = /<!-- WXCODE:(\w+):(\{.*?\}) -->/g;
```

```python
import re
WXCODE_PATTERN = r'<!-- WXCODE:(\w+):(\{.*?\}) -->'
```

### Estrutura Geral

```typescript
interface WxcodeEvent {
  type: 'HEADER' | 'TOOL' | 'TOOL_RESULT' | 'STATUS' | 'NEXT_ACTION' | 'ERROR';
  data: HeaderData | ToolData | ToolResultData | StatusData | NextActionData | ErrorData;
}
```

---

## 2. Tipos de Eventos

### 2.1 HEADER

**Quando:** Emitido no INÍCIO de cada comando.

```
<!-- WXCODE:HEADER:{"command":"execute-phase","args":"3","title":"WXCODE ▶ EXECUTING PHASE 3"} -->
```

**Schema TypeScript:**

```typescript
interface HeaderData {
  command: string;      // Nome do comando (sem /wxcode:)
  args: string | null;  // Argumentos passados
  title: string;        // Título visual do comando
  phase?: number;       // Número da fase (se aplicável)
  plan?: string;        // ID do plano (se aplicável)
}
```

**Exemplos por Comando:**

| Comando | Exemplo HEADER |
|---------|----------------|
| `execute-phase 3` | `{"command":"execute-phase","args":"3","title":"WXCODE ▶ EXECUTING PHASE 3"}` |
| `plan-phase 2` | `{"command":"plan-phase","args":"2","title":"WXCODE ▶ PLANNING PHASE 2"}` |
| `progress` | `{"command":"progress","args":"","title":"WXCODE ▶ PROJECT PROGRESS"}` |
| `verify-work 3` | `{"command":"verify-work","args":"3","title":"WXCODE ▶ VERIFYING PHASE 3"}` |
| `new-project` | `{"command":"new-project","args":"","title":"WXCODE ▶ INITIALIZING PROJECT"}` |
| `audit-milestone` | `{"command":"audit-milestone","args":"","title":"WXCODE ▶ AUDITING MILESTONE"}` |
| `debug "login broken"` | `{"command":"debug","args":"login broken","title":"WXCODE ▶ DEBUG SESSION"}` |
| `help` | `{"command":"help","args":"","title":"WXCODE ▶ COMMAND REFERENCE"}` |

**Rendering Sugerido:**

```
┌─────────────────────────────────────────────┐
│  🟣 WXCODE ▶ EXECUTING PHASE 3              │
└─────────────────────────────────────────────┘
```

---

### 2.2 STATUS

**Quando:** Emitido quando o status de execução muda.

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing wave 1 of 2","progress":25} -->
```

**Schema TypeScript:**

```typescript
interface StatusData {
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'paused';
  message: string;        // Mensagem descritiva
  progress?: number;      // Porcentagem 0-100 (opcional)
  phase?: number;         // Fase atual (opcional)
  plan?: string;          // Plano atual (opcional)
  task?: string;          // Tarefa atual (opcional)
}
```

**Valores de Status:**

| Status | Significado | Cor Sugerida |
|--------|-------------|--------------|
| `pending` | Aguardando início | Cinza |
| `in_progress` | Em execução | Azul/Amarelo |
| `completed` | Concluído com sucesso | Verde |
| `failed` | Falhou | Vermelho |
| `paused` | Pausado (checkpoint) | Laranja |

**Sequência Típica:**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Loading context","progress":10} -->
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing wave 1 of 3","progress":33} -->
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing wave 2 of 3","progress":66} -->
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing wave 3 of 3","progress":90} -->
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Verifying phase","progress":95} -->
<!-- WXCODE:STATUS:{"status":"completed","message":"Phase 3 complete","progress":100} -->
```

**Rendering Sugerido:**

```
[████████░░░░░░░░░░░░] 33%
Executing wave 1 of 3
```

---

### 2.3 TOOL

**Quando:** Emitido ANTES de uma chamada de ferramenta.

```
<!-- WXCODE:TOOL:{"tool":"Bash","description":"Get model profile from config","command":"cat .planning/config.json"} -->
```

**Schema TypeScript:**

```typescript
interface ToolData {
  tool: string;           // Nome da ferramenta
  description: string;    // Descrição da operação
  command?: string;       // Para Bash: o comando
  file?: string;          // Para Read/Write/Edit: caminho do arquivo
  mcp_tool?: string;      // Para MCP: nome do tool
}
```

**Tools Comuns:**

| Tool | Campos Típicos |
|------|----------------|
| `Bash` | `command`: comando shell |
| `Read` | `file`: caminho do arquivo |
| `Write` | `file`: caminho do arquivo |
| `Edit` | `file`: caminho do arquivo |
| `MCP` | `mcp_tool`: nome do MCP tool |
| `Task` | `description`: descrição do subagent |
| `Glob` | `description`: padrão de busca |
| `Grep` | `description`: termo de busca |

**Rendering Sugerido:**

```
⚙️ Running: Get model profile from config
   $ cat .planning/config.json
```

---

### 2.4 TOOL_RESULT

**Quando:** Emitido DEPOIS que uma ferramenta completa.

```
<!-- WXCODE:TOOL_RESULT:{"tool":"Bash","success":true,"output":"balanced","duration_ms":45} -->
```

**Schema TypeScript:**

```typescript
interface ToolResultData {
  tool: string;           // Nome da ferramenta
  success: boolean;       // Se teve sucesso
  output?: string;        // Output truncado (max 200 chars)
  error?: string;         // Mensagem de erro (se falhou)
  duration_ms?: number;   // Tempo de execução em ms
}
```

**Rendering Sugerido (Sucesso):**

```
✓ Get model profile from config (45ms)
  → balanced
```

**Rendering Sugerido (Erro):**

```
✗ Get model profile from config (120ms)
  → Error: File not found
```

---

### 2.5 NEXT_ACTION

**Quando:** Emitido no FINAL do comando com sugestão de próximo passo.

```
<!-- WXCODE:NEXT_ACTION:{"command":"verify-work","args":"3","description":"Validate the implemented features","priority":"recommended"} -->
```

**Schema TypeScript:**

```typescript
interface NextActionData {
  command: string;        // Comando sugerido (sem /wxcode:)
  args?: string;          // Argumentos sugeridos
  description: string;    // Por que esse é o próximo passo
  priority: 'required' | 'recommended' | 'optional';
}
```

**Valores de Priority:**

| Priority | Significado | Ação Sugerida |
|----------|-------------|---------------|
| `required` | Obrigatório para continuar | Botão destacado |
| `recommended` | Recomendado | Botão normal |
| `optional` | Opcional | Link discreto |

**Mapeamento Comando → Próxima Ação:**

| Depois de... | Próxima Ação Típica |
|--------------|---------------------|
| `new-project` | `plan-phase 1` |
| `discuss-phase X` | `plan-phase X` |
| `plan-phase X` | `execute-phase X` |
| `execute-phase X` (sucesso) | `discuss-phase X+1` ou `audit-milestone` |
| `execute-phase X` (gaps) | `plan-phase X --gaps` |
| `verify-work X` (gaps) | `execute-phase X --gaps-only` |
| `audit-milestone` | `complete-milestone` |
| `complete-milestone` | `new-milestone` |

**Rendering Sugerido:**

```
┌─────────────────────────────────────────────┐
│  ▶ Next: Validate the implemented features  │
│                                             │
│  [/wxcode:verify-work 3]                    │
└─────────────────────────────────────────────┘
```

---

### 2.6 ERROR

**Quando:** Emitido quando ocorre um erro.

```
<!-- WXCODE:ERROR:{"code":"MCP_UNAVAILABLE","message":"Cannot connect to wxcode-kb MCP server","recoverable":true,"suggestion":"Check if MCP server is running"} -->
```

**Schema TypeScript:**

```typescript
interface ErrorData {
  code: string;           // Código do erro (ver tabela)
  message: string;        // Mensagem legível
  recoverable: boolean;   // Se pode continuar
  suggestion?: string;    // Como resolver
}
```

**Códigos de Erro:**

| Code | Descrição | Recoverable | Comandos |
|------|-----------|-------------|----------|
| `MCP_UNAVAILABLE` | MCP server não conectado | true | mcp-health-check, execute-phase, plan-phase |
| `FILE_NOT_FOUND` | Arquivo não existe | depends | new-project-greetings |
| `MISSING_ARGUMENT` | Argumento obrigatório faltando | true | new-project-greetings |
| `PHASE_NOT_FOUND` | Fase não existe no roadmap | false | execute-phase, plan-phase |
| `PLAN_NOT_FOUND` | Plano não encontrado | false | execute-phase |
| `NO_PROJECT` | Projeto WXCODE não encontrado | true | set-profile, settings |
| `INVALID_PROFILE` | Perfil de modelo inválido | true | set-profile |
| `NOT_INITIALIZED` | WXCODE fork não inicializado | true | status |
| `NO_SYNC_FOUND` | Nenhum sync para rollback | false | rollback |
| `GIT_DIRTY` | Mudanças não commitadas | true | execute-phase |
| `VALIDATION_FAILED` | Validação falhou | true | plan-phase |
| `AUTH_REQUIRED` | Precisa autenticação | true | - |
| `TOOL_FAILED` | Ferramenta falhou | depends | execute-phase |
| `UAT_GAPS_FOUND` | Testes falharam | true | verify-work |
| `TIMEOUT` | Operação timeout | true | execute-phase |

**Rendering Sugerido:**

```
┌─────────────────────────────────────────────┐
│  ❌ Error: MCP_UNAVAILABLE                  │
│                                             │
│  Cannot connect to wxcode-kb MCP server     │
│                                             │
│  💡 Check if MCP server is running          │
└─────────────────────────────────────────────┘
```

---

## 3. Fluxos Típicos por Comando

### 3.1 execute-phase

```
<!-- WXCODE:HEADER:{"command":"execute-phase","args":"3","title":"WXCODE ▶ EXECUTING PHASE 3"} -->

[conteúdo visual]

<!-- WXCODE:TOOL:{"tool":"Bash","description":"Get model profile"} -->
<!-- WXCODE:TOOL_RESULT:{"tool":"Bash","success":true,"output":"balanced"} -->

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing wave 1 of 2","progress":25} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Executing wave 2 of 2","progress":50} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Verifying phase","progress":80} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"completed","message":"Phase 3 complete","progress":100} -->
<!-- WXCODE:NEXT_ACTION:{"command":"discuss-phase","args":"4","description":"Gather context for next phase","priority":"recommended"} -->
```

### 3.2 plan-phase

```
<!-- WXCODE:HEADER:{"command":"plan-phase","args":"2","title":"WXCODE ▶ PLANNING PHASE 2"} -->

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Researching phase requirements","progress":25} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Creating plan","progress":50} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Verifying plan","progress":75} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"completed","message":"Plan created","progress":100} -->
<!-- WXCODE:NEXT_ACTION:{"command":"execute-phase","args":"2","description":"Execute the planned tasks","priority":"recommended"} -->
```

### 3.3 progress

```
<!-- WXCODE:HEADER:{"command":"progress","args":"","title":"WXCODE ▶ PROJECT PROGRESS"} -->
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Phase 3 of 5","progress":60,"phase":3} -->

[conteúdo visual - status report]

<!-- WXCODE:NEXT_ACTION:{"command":"execute-phase","args":"3","description":"Execute planned tasks","priority":"recommended"} -->
```

### 3.4 verify-work (com gaps)

```
<!-- WXCODE:HEADER:{"command":"verify-work","args":"3","title":"WXCODE ▶ VERIFYING PHASE 3"} -->

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Testing: Login flow","progress":33} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"in_progress","message":"Testing: Dashboard","progress":66} -->

[conteúdo visual]

<!-- WXCODE:STATUS:{"status":"completed","message":"3/4 tests passed, 1 gap found"} -->
<!-- WXCODE:ERROR:{"code":"UAT_GAPS_FOUND","message":"1 test failed: Login redirect broken","recoverable":true,"suggestion":"Run /wxcode:execute-phase with --gaps-only"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"execute-phase","args":"3 --gaps-only","description":"Execute gap fix plans","priority":"required"} -->
```

---

## 4. Parsing Completo

### JavaScript/TypeScript

```typescript
interface WxcodeEvent {
  type: string;
  data: Record<string, any>;
  raw: string;
  index: number;
}

function parseWxcodeMarkdown(markdown: string): {
  events: WxcodeEvent[];
  content: string;
} {
  const WXCODE_PATTERN = /<!-- WXCODE:(\w+):(\{.*?\}) -->/g;
  const events: WxcodeEvent[] = [];

  let match;
  while ((match = WXCODE_PATTERN.exec(markdown)) !== null) {
    try {
      events.push({
        type: match[1],
        data: JSON.parse(match[2]),
        raw: match[0],
        index: match.index,
      });
    } catch (e) {
      console.error('Failed to parse WXCODE event:', match[0]);
    }
  }

  // Remove markers from content for rendering
  const content = markdown.replace(WXCODE_PATTERN, '').trim();

  return { events, content };
}

// Uso
const { events, content } = parseWxcodeMarkdown(claudeResponse);

const header = events.find(e => e.type === 'HEADER');
const status = events.filter(e => e.type === 'STATUS');
const nextAction = events.find(e => e.type === 'NEXT_ACTION');
const errors = events.filter(e => e.type === 'ERROR');
```

### Python

```python
import re
import json
from typing import TypedDict, List, Optional
from dataclasses import dataclass

@dataclass
class WxcodeEvent:
    type: str
    data: dict
    raw: str
    index: int

def parse_wxcode_markdown(markdown: str) -> tuple[List[WxcodeEvent], str]:
    """Parse WXCODE structured output from markdown."""
    WXCODE_PATTERN = r'<!-- WXCODE:(\w+):(\{.*?\}) -->'
    events = []

    for match in re.finditer(WXCODE_PATTERN, markdown):
        try:
            events.append(WxcodeEvent(
                type=match.group(1),
                data=json.loads(match.group(2)),
                raw=match.group(0),
                index=match.start()
            ))
        except json.JSONDecodeError:
            print(f"Failed to parse: {match.group(0)}")

    # Remove markers from content
    content = re.sub(WXCODE_PATTERN, '', markdown).strip()

    return events, content

# Uso
events, content = parse_wxcode_markdown(claude_response)

header = next((e for e in events if e.type == 'HEADER'), None)
statuses = [e for e in events if e.type == 'STATUS']
next_action = next((e for e in events if e.type == 'NEXT_ACTION'), None)
errors = [e for e in events if e.type == 'ERROR']
```

---

## 5. Mapeamento Completo de Comandos

**Legenda:**
- ✓ = Implementado com múltiplos cenários
- ○ = Implementado (cenário único)
- - = Não aplicável (comando terminal)

| Comando | Title | STATUS | NEXT_ACTION | ERROR |
|---------|-------|--------|-------------|-------|
| `add-phase` | ADDING PHASE | ✓ | ✓ plan-phase | - |
| `add-todo` | ADDING TODO | ✓ | ✓ check-todos | - |
| `audit-milestone` | AUDITING MILESTONE | ✓ | ✓ complete-milestone | - |
| `check-todos` | CHECKING TODOS | ✓ | ✓ progress | - |
| `complete-milestone` | COMPLETING MILESTONE | ✓ | ✓ new-milestone | - |
| `create-start-dev` | CREATING START-DEV | ✓ | ✓ start-dev | - |
| `customize` | CUSTOMIZING WXCODE | ✓ | ✓ status | - |
| `dashboard` | GENERATING DASHBOARD | ✓ | ✓ progress | - |
| `debug` | DEBUG SESSION | ✓ | ✓ progress | - |
| `design-system` | DESIGN SYSTEM | ✓ | ✓ progress | - |
| `diff` | DIFF | ✓ completed/N differences | ✓ sync (se diferenças) | - |
| `discuss-phase` | DISCUSSING PHASE X | ✓ | ✓ plan-phase X | - |
| `discuss` | DISCUSSION | ✓ | ✓ progress | - |
| `execute-phase` | EXECUTING PHASE X | ✓ waves/verifying | ✓ discuss-phase X+1 | ✓ |
| `help` | COMMAND REFERENCE | ○ completed | - | - |
| `history` | HISTORY | ○ completed | ✓ status | - |
| `init` | INITIALIZING WXCODE | ✓ | ✓ help | - |
| `insert-phase` | INSERTING PHASE | ✓ | ✓ plan-phase | - |
| `join-discord` | JOIN DISCORD | ○ completed | - | - |
| `list-phase-assumptions` | PHASE ASSUMPTIONS | ✓ | ✓ discuss-phase | - |
| `map-codebase` | MAPPING CODEBASE | ✓ | ✓ progress | - |
| `mcp-health-check` | MCP HEALTH CHECK | ✓ connected/failed | - | ✓ MCP_UNAVAILABLE |
| `new-milestone` | NEW MILESTONE | ✓ | ✓ plan-phase 1 | - |
| `new-project` | INITIALIZING PROJECT | ✓ | ✓ plan-phase 1 | - |
| `new-project-greetings` | WELCOME | ✓ loaded/failed | ✓ new-project | ✓ MISSING_ARG, FILE_NOT_FOUND |
| `override` | OVERRIDE | ✓ usage/list/add/remove | ✓ override --list, diff | - |
| `pause-work` | PAUSING WORK | ✓ | ✓ resume-work | - |
| `plan-milestone-gaps` | PLANNING GAP CLOSURE | ✓ | ✓ execute-phase | - |
| `plan-phase` | PLANNING PHASE X | ✓ researching/creating/verifying | ✓ execute-phase X | ✓ |
| `progress` | PROJECT PROGRESS | ✓ Phase X of Y (6 rotas) | ✓ execute/plan/discuss/complete | - |
| `quick` | QUICK TASK | ✓ | ✓ progress | - |
| `remove-phase` | REMOVING PHASE | ✓ | ✓ progress | - |
| `research-phase` | RESEARCHING PHASE X | ✓ | ✓ plan-phase X | - |
| `resume-work` | RESUMING WORK | ✓ | ✓ progress | - |
| `rollback` | ROLLBACK | ✓ complete/failed/cancelled | ✓ status | ✓ NO_SYNC_FOUND |
| `set-profile` | SET PROFILE | ✓ success/error | - | ✓ INVALID_PROFILE, NO_PROJECT |
| `settings` | SETTINGS | ✓ updated/error | - | ✓ NO_PROJECT |
| `start-dev` | STARTING DEV SERVER | ✓ | ✓ progress | - |
| `status` | STATUS | ✓ up-to-date/updates/offline | ✓ sync (se updates) | ✓ NOT_INITIALIZED |
| `sync` | SYNCING WITH UPSTREAM | ✓ | ✓ status | - |
| `trace` | TRACING ELEMENT | ✓ | ✓ progress | - |
| `update` | UPDATING WXCODE | ✓ | ✓ version | - |
| `verify-work` | VERIFYING PHASE X | ✓ Testing: [item] | ✓ execute-phase --gaps | ✓ UAT_GAPS_FOUND |
| `version` | VERSION | ○ completed | - | - |

---

## 6. Considerações de UI

### Estados Visuais

1. **Header**: Sempre visível no topo da mensagem
2. **Status**: Pode atualizar progressivamente (última STATUS válida)
3. **Tools**: Pode colapsar/expandir
4. **Errors**: Sempre destacado
5. **Next Action**: Sempre visível no final

### Cores Sugeridas

```css
.wxcode-header { background: #7C3AED; color: white; }
.wxcode-status-pending { color: #6B7280; }
.wxcode-status-in_progress { color: #3B82F6; }
.wxcode-status-completed { color: #10B981; }
.wxcode-status-failed { color: #EF4444; }
.wxcode-status-paused { color: #F59E0B; }
.wxcode-error { background: #FEE2E2; border: 1px solid #EF4444; }
.wxcode-next-action { background: #EDE9FE; border: 1px solid #7C3AED; }
```

### Acessibilidade

- Todos os status devem ter aria-label
- Progress bars devem ter role="progressbar"
- Errors devem ter role="alert"
- Next actions devem ser focusáveis

---

## 7. Versionamento

Esta especificação segue semantic versioning. Mudanças:

- **MAJOR**: Mudanças breaking no formato
- **MINOR**: Novos tipos de eventos ou campos opcionais
- **PATCH**: Correções e esclarecimentos

### Histórico de Versões

**1.1.0** (2026-02-04)
- 100% dos 44 comandos com structured output completo
- Adicionados ERROR markers para 12 comandos
- Adicionados novos códigos de erro: MISSING_ARGUMENT, NO_PROJECT, INVALID_PROFILE, NOT_INITIALIZED, NO_SYNC_FOUND
- Comandos corrigidos: diff, help, history, join-discord, mcp-health-check, new-project-greetings, override, rollback, set-profile, settings, status, version
- Tabela de mapeamento atualizada com indicadores de cobertura

**1.0.0** (2026-02-04)
- Especificação inicial
- 6 tipos de eventos: HEADER, STATUS, TOOL, TOOL_RESULT, NEXT_ACTION, ERROR
- Parsers TypeScript e Python
- Guia de UI

Versão atual: **1.1.0**
