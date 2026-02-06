# Command Scoping Architecture

**Data:** 2026-02-06
**Versao:** 2.0.3+

---

## Resumo

Todos os comandos WXCODE sao instalados **globalmente** em `~/.claude/commands/wxcode/`. Qualquer projeto ve todos os 39+ comandos `/wxcode:*` automaticamente.

---

## Estrutura Apos Instalacao

```
~/.claude/
├── commands/
│   └── wxcode/                    ← todos os comandos WXCODE (39+)
│       ├── new-project.md
│       ├── plan-phase.md
│       ├── execute-phase.md
│       ├── help.md
│       ├── version.md
│       ├── update.md
│       └── ...
│
├── wxcode-skill/                  ← referencias, templates, workflows
│   ├── references/
│   ├── templates/
│   ├── workflows/
│   ├── CHANGELOG-WXCODE.md
│   └── VERSION
│
├── agents/                        ← agentes (globais)
│   ├── wxcode-executor.md
│   ├── wxcode-planner.md
│   └── ...
│
└── hooks/                         ← hooks (globais)
```

---

## Coexistencia com GSD

WXCODE e GSD sao produtos independentes. O installer WXCODE nao toca arquivos GSD:

```
~/.claude/
├── commands/
│   ├── wxcode/          ← WXCODE (39+ commands)
│   └── gsd/             ← GSD (28 commands) — intocado
│
├── wxcode-skill/        ← WXCODE skill dir
├── get-shit-done/       ← GSD skill dir — intocado
```

---

## OpenCode

OpenCode usa estrutura flat em `~/.config/opencode/command/`:
- Comandos sao copiados como `wxcode-*.md` (prefixo flat)
- Todos os comandos sao globais (mesmo comportamento)

---

## Referencia: Arquivos do Installer

O `bin/install.js` faz:

1. **WXCODE commands**: copia todos para `~/.claude/commands/wxcode/` (global)
2. **wxcode-skill/**: copia references, templates, workflows
3. **Agents**: copia para `~/.claude/agents/` (global)
4. **Hooks**: copia para `~/.claude/hooks/` (global)
5. **CHANGELOG-WXCODE.md**: copia para `~/.claude/wxcode-skill/`
6. **VERSION**: escreve em `~/.claude/wxcode-skill/`
