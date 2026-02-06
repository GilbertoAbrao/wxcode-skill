# Command Scoping Architecture

**Data:** 2026-02-06
**Versao:** 2.0.0+

---

## Resumo

WXCODE usa um modelo de **comando por projeto** (project-level commands). Nenhum comando operacional e instalado globalmente. Cada projeto opta explicitamente nos comandos que precisa via **symlink** para um diretorio de armazenamento global.

---

## Principio Fundamental

> **Nenhum projeto deve ver comandos que nao sao relevantes para ele.**

| Tipo de projeto | Comandos visiveis | Comandos invisiveis |
|---|---|---|
| Output-project (conversao) | `/wxcode:*` | — |
| Projeto sem setup | Nenhum (so bootstrap) | Todos |

---

## Estrutura de Armazenamento

Apos a instalacao (`npx github:GilbertoAbrao/get-shit-done#main --claude --global`):

```
~/.claude/
├── commands/
│   └── wxcode/
│       ├── new-project.md      ← bootstrap (unico comando global)
│       ├── help.md             ← bootstrap
│       ├── version.md          ← bootstrap
│       └── update.md           ← bootstrap
│
├── wxcode-skill/
│   ├── commands/               ← STORAGE (nao visivel diretamente)
│   │   └── wxcode/             ← todos comandos WXCODE (39+)
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
- `~/.claude/wxcode-skill/commands/` **NAO** e escaneado (nao e `commands/` direto)
- Isso permite armazenar comandos sem torna-los visiveis globalmente

---

## Como Projetos Ganham Acesso

### Output-projects (conversao WXCODE)

O `/wxcode:new-project` cria automaticamente o symlink durante Phase 1 Setup:

```
output-project/
└── .claude/
    └── commands/
        └── wxcode → ~/.claude/wxcode-skill/commands/wxcode  (symlink)
```

**Resultado:** O projeto ve todos os 39+ comandos `/wxcode:*`.

O `/wxcode:new-milestone` tambem verifica e cria o symlink se necessario (para projetos existentes).

---

## Cenarios de Deploy

### Local (Maquina de Desenvolvimento)

```
Dev Machine
├── ~/.claude/                          ← instalacao global
│   ├── commands/wxcode/ (4 bootstrap)
│   └── wxcode-skill/commands/          ← storage
│       └── wxcode/
│
├── ~/projetos/output-simetra/          ← output-project
│   └── .claude/commands/wxcode → storage  ← ve /wxcode:*
│
└── ~/projetos/outro-output/            ← outro output-project
    └── .claude/commands/wxcode → storage  ← ve /wxcode:*
```

### Cloud (Instancia de Producao)

```
Cloud Instance
├── ~/.claude/                          ← instalacao global
│   ├── commands/wxcode/ (4 bootstrap)
│   └── wxcode-skill/commands/          ← storage
│       └── wxcode/
│
└── /app/output-project/                ← unico tipo de projeto na nuvem
    └── .claude/commands/wxcode → storage  ← ve /wxcode:*
```

### Setup da Cloud Instance

```bash
# 1. Instalar WXCODE (mesmo comando de sempre)
npx github:GilbertoAbrao/get-shit-done#main --claude --global

# 2. Resultado automatico:
#    - 4 bootstrap wxcode commands em ~/.claude/commands/wxcode/
#    - Storage completo em ~/.claude/wxcode-skill/commands/
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

---

## Fluxo de Criacao de Projeto

### Output-project (via wxcode-ui ou CLI)

```
1. Usuario roda /wxcode:new-project
2. Phase 1 Setup:
   a. Verifica se .claude/commands/wxcode existe
   b. Se nao: cria symlink → ~/.claude/wxcode-skill/commands/wxcode
3. Todos comandos /wxcode:* ficam disponiveis
```

---

## Perguntas Frequentes

### O symlink e rastreado pelo git?

Nao. O diretorio `.claude/` geralmente esta no `.gitignore`. Cada clone/instancia precisa criar seu proprio symlink.

### E se o target do symlink nao existir (storage nao instalado)?

O `/wxcode:new-project` detecta isso e exibe:
```
⚠ WXCODE commands storage not found.
Run: npx github:GilbertoAbrao/get-shit-done#main --claude --global
```

### Os 4 bootstrap commands aparecem em todos os projetos?

Sim. Os 4 comandos wxcode bootstrap (`new-project`, `help`, `version`, `update`) sao globais e aparecem em todos os projetos. Sao inofensivos — servem apenas para administracao.

### Como remover wxcode de um projeto?

```bash
rm .claude/commands/wxcode  # remove symlink
```

### Como o OpenCode funciona?

OpenCode continua usando a estrutura global flat (sem symlinks). Todos os comandos wxcode-* ficam em `~/.config/opencode/command/`. A separacao por projeto nao se aplica ao OpenCode.

---

## Referencia: Arquivos do Installer

O `bin/install.js` faz:

1. **WXCODE commands**: copia para storage (`wxcode-skill/commands/wxcode/`), instala 4 bootstrap global
2. **wxcode-skill/**: copia references, templates, workflows
3. **Agents**: copia para `~/.claude/agents/` (sempre global)
4. **Hooks**: copia para `~/.claude/hooks/` (sempre global)

A copia para storage roda DEPOIS da copia de `wxcode-skill/` porque `copyWithPathReplacement()` faz clean install (deleta destino antes de copiar).
