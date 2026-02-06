# Command Scoping Architecture

**Data:** 2026-02-06
**Versao:** 1.4.31+

---

## Resumo

WXCODE usa um modelo de **comando por projeto** (project-level commands). Nenhum comando operacional e instalado globalmente. Cada projeto opta explicitamente nos comandos que precisa via **symlink** para um diretorio de armazenamento global.

---

## Principio Fundamental

> **Nenhum projeto deve ver comandos que nao sao relevantes para ele.**

| Tipo de projeto | Comandos visiveis | Comandos invisiveis |
|---|---|---|
| Output-project (conversao) | `/wxcode:*` | `/gsd:*` |
| Projeto GSD vanilla | `/gsd:*` | `/wxcode:*` |
| Projeto sem setup | Nenhum (so bootstrap) | Todos |

---

## Estrutura de Armazenamento

Apos a instalacao (`npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global`):

```
~/.claude/
├── commands/
│   └── wxcode/
│       ├── new-project.md      ← bootstrap (unico comando global)
│       ├── help.md             ← bootstrap
│       ├── version.md          ← bootstrap
│       └── update.md           ← bootstrap
│
├── get-shit-done/
│   ├── commands/               ← STORAGE (nao visivel diretamente)
│   │   ├── gsd/                ← todos comandos GSD (1+)
│   │   │   └── help.md
│   │   └── wxcode/             ← todos comandos WXCODE (46+)
│   │       ├── new-project.md
│   │       ├── plan-phase.md
│   │       ├── execute-phase.md
│   │       └── ...
│   ├── references/             ← docs de referencia
│   ├── templates/              ← templates
│   └── workflows/              ← workflows
│
├── agents/                     ← agentes (sempre globais)
│   ├── wxcode-executor.md
│   ├── wxcode-planner.md
│   └── ...
│
└── hooks/                      ← hooks (sempre globais)
```

### Por que "storage" separado?

- `~/.claude/commands/` e escaneado pelo Claude Code para descobrir skills
- `~/.claude/get-shit-done/commands/` **NAO** e escaneado (nao e `commands/` direto)
- Isso permite armazenar comandos sem torna-los visiveis globalmente

---

## Como Projetos Ganham Acesso

### Output-projects (conversao WXCODE)

O `/wxcode:new-project` cria automaticamente o symlink durante Phase 1 Setup:

```
output-project/
└── .claude/
    └── commands/
        └── wxcode → ~/.claude/get-shit-done/commands/wxcode  (symlink)
```

**Resultado:** O projeto ve todos os 46+ comandos `/wxcode:*`.

O `/wxcode:new-milestone` tambem verifica e cria o symlink se necessario (para projetos existentes).

### Projetos GSD vanilla

Para projetos que usam GSD puro (nao-wxcode), criar o symlink manualmente:

```bash
mkdir -p .claude/commands
ln -s ~/.claude/get-shit-done/commands/gsd .claude/commands/gsd
```

**Resultado:** O projeto ve todos os comandos `/gsd:*`.

### Projeto wxcode-ui

O wxcode-ui e um projeto especial — ele gerencia output-projects mas nao e um deles.
Deve ter seus proprios comandos locais conforme necessidade:

```
wxcode-ui/
└── .claude/
    └── commands/
        ├── gsd → ~/.claude/get-shit-done/commands/gsd  (se quiser GSD)
        ├── openspec/       ← comandos proprios
        └── wx-convert/     ← comandos proprios
```

**NAO** deve ter symlink para wxcode (para nao confundir com output-projects).

---

## Cenarios de Deploy

### Local (Maquina de Desenvolvimento)

```
Dev Machine
├── ~/.claude/                          ← instalacao global
│   ├── commands/wxcode/ (4 bootstrap)
│   └── get-shit-done/commands/         ← storage
│       ├── gsd/
│       └── wxcode/
│
├── ~/projetos/wxcode-ui/               ← gerencia conversoes
│   └── .claude/commands/gsd → storage  ← ve /gsd:*
│
├── ~/projetos/meu-app/                 ← projeto GSD vanilla
│   └── .claude/commands/gsd → storage  ← ve /gsd:*
│
└── ~/projetos/output-simetra/          ← output-project
    └── .claude/commands/wxcode → storage  ← ve /wxcode:*
```

**Dev machine tem tudo instalado.** Cada projeto so ve o que precisa.

### Cloud (Instancia de Producao)

```
Cloud Instance
├── ~/.claude/                          ← instalacao global
│   ├── commands/wxcode/ (4 bootstrap)
│   └── get-shit-done/commands/         ← storage
│       ├── gsd/                        ← armazenado, mas ninguem usa
│       └── wxcode/
│
└── /app/output-project/                ← unico tipo de projeto na nuvem
    └── .claude/commands/wxcode → storage  ← ve /wxcode:*
```

**Na nuvem, output-projects so vem `/wxcode:*`.** GSD existe no storage mas nenhum projeto cria symlink para ele.

### Setup da Cloud Instance

```bash
# 1. Instalar WXCODE (mesmo comando de sempre)
npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global

# 2. Resultado automatico:
#    - 4 bootstrap wxcode commands em ~/.claude/commands/wxcode/
#    - Storage completo em ~/.claude/get-shit-done/commands/
#    - GSD no storage mas NAO em ~/.claude/commands/gsd/ (nao global)
#    - Agents e hooks globais

# 3. Ao criar output-project:
#    /wxcode:new-project cria o symlink automaticamente
#    Output-project ve APENAS /wxcode:*
```

---

## Comandos Bootstrap (Globais)

Apenas estes comandos sao instalados globalmente em `~/.claude/commands/`:

| Comando | Namespace | Proposito |
|---|---|---|
| `new-project.md` | `wxcode` | Criar novo projeto (cria symlink automaticamente) |
| `help.md` | `wxcode` | Referencia de comandos |
| `version.md` | `wxcode` | Exibir versao |
| `update.md` | `wxcode` | Atualizar para ultima versao |

**GSD NAO tem comandos globais.** Para usar GSD, crie o symlink manualmente.

---

## Fluxo de Criacao de Projeto

### Output-project (via wxcode-ui ou CLI)

```
1. Usuario roda /wxcode:new-project
2. Phase 1 Setup:
   a. Verifica se .claude/commands/wxcode existe
   b. Se nao: cria symlink → ~/.claude/get-shit-done/commands/wxcode
   c. NAO cria symlink para gsd
3. Todos comandos /wxcode:* ficam disponiveis
4. Nenhum comando /gsd:* visivel
```

### Projeto GSD vanilla

```
1. Usuario cria diretorio do projeto
2. Executa manualmente:
   mkdir -p .claude/commands
   ln -s ~/.claude/get-shit-done/commands/gsd .claude/commands/gsd
3. Todos comandos /gsd:* ficam disponiveis
4. Nenhum comando /wxcode:* visivel (alem dos 4 bootstrap)
```

---

## Perguntas Frequentes

### O symlink e rastreado pelo git?

Nao. O diretorio `.claude/` geralmente esta no `.gitignore`. Cada clone/instancia precisa criar seu proprio symlink.

### E se o target do symlink nao existir (storage nao instalado)?

O `/wxcode:new-project` detecta isso e exibe:
```
⚠ WXCODE commands storage not found.
Run: npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global
```

### Os 4 bootstrap commands aparecem em todos os projetos?

Sim. Os 4 comandos wxcode bootstrap (`new-project`, `help`, `version`, `update`) sao globais e aparecem em todos os projetos. Sao inofensivos — servem apenas para administracao.

### Como remover wxcode de um projeto?

```bash
rm .claude/commands/wxcode  # remove symlink
```

### Como o OpenCode funciona?

OpenCode continua usando a estrutura global flat (sem symlinks). Todos os comandos gsd-* e wxcode-* ficam em `~/.config/opencode/command/`. A separacao por projeto nao se aplica ao OpenCode.

### Posso ter GSD e WXCODE no mesmo projeto?

Tecnicamente sim (criar ambos symlinks), mas nao e recomendado. Os comandos podem conflitar ou confundir o LLM.

---

## Referencia: Arquivos do Installer

O `bin/install.js` faz:

1. **GSD commands**: copia para storage (`get-shit-done/commands/gsd/`), NAO instala global
2. **WXCODE commands**: copia para storage (`get-shit-done/commands/wxcode/`), instala 4 bootstrap global
3. **get-shit-done/**: copia references, templates, workflows
4. **Agents**: copia para `~/.claude/agents/` (sempre global)
5. **Hooks**: copia para `~/.claude/hooks/` (sempre global)

A copia para storage roda DEPOIS da copia de `get-shit-done/` porque `copyWithPathReplacement()` faz clean install (deleta destino antes de copiar).
