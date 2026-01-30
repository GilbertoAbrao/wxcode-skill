# Dashboard Workflow Stages — Migration Guide

## Overview

O dashboard de milestone agora inclui uma seção `workflow` que rastreia as 7 etapas do ciclo de vida de um milestone. Isso permite que a UI exiba um stepper/timeline mostrando em qual etapa o milestone está.

## Nova Seção: `workflow`

```json
{
  "workflow": {
    "current_stage": "executing",
    "stages": [
      {
        "id": "created",
        "name": "Milestone Created",
        "description": "Folder created, MongoDB record, initial research",
        "status": "complete",
        "completed_at": "2026-01-30T13:43:00Z"
      },
      {
        "id": "requirements",
        "name": "Requirements Defined",
        "description": "REQUIREMENTS.md generated with acceptance criteria",
        "status": "complete",
        "completed_at": "2026-01-30T13:45:00Z"
      },
      {
        "id": "roadmap",
        "name": "Roadmap Created",
        "description": "ROADMAP.md with phase breakdown",
        "status": "complete",
        "completed_at": "2026-01-30T13:50:00Z"
      },
      {
        "id": "planning",
        "name": "All Phases Planned",
        "description": "PLAN.md exists for all phases",
        "status": "complete",
        "completed_at": "2026-01-30T14:30:00Z"
      },
      {
        "id": "executing",
        "name": "Execution In Progress",
        "description": "Plans being executed, code being written",
        "status": "in_progress",
        "completed_at": null
      },
      {
        "id": "verified",
        "name": "Work Verified",
        "description": "UAT passed, all requirements met",
        "status": "pending",
        "completed_at": null
      },
      {
        "id": "archived",
        "name": "Milestone Archived",
        "description": "Moved to milestones/, marked converted in MCP",
        "status": "pending",
        "completed_at": null
      }
    ]
  }
}
```

## Campos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `workflow.current_stage` | string | ID da etapa ativa (onde o trabalho está acontecendo) |
| `workflow.stages` | array | Lista fixa de 7 etapas em ordem |
| `stages[].id` | string | Identificador único da etapa |
| `stages[].name` | string | Nome amigável para exibição |
| `stages[].description` | string | Descrição do que acontece nesta etapa |
| `stages[].status` | enum | `pending` \| `in_progress` \| `complete` |
| `stages[].completed_at` | string \| null | Timestamp ISO8601 quando foi concluída |

## Status das Etapas

```
pending      → Etapa ainda não iniciada (cinza/inativo)
in_progress  → Etapa atual, trabalho em andamento (azul/pulsando)
complete     → Etapa concluída (verde/check)
```

## Visualização Sugerida

### Opção 1: Stepper Horizontal

```
[✓]────[✓]────[✓]────[✓]────[●]────[ ]────[ ]
 │      │      │      │      │      │      │
Created Reqs  Road  Plan   Exec  Verify Archive
                            ↑
                        current
```

### Opção 2: Timeline Vertical

```
✓ Milestone Created          30 Jan 13:43
│
✓ Requirements Defined       30 Jan 13:45
│
✓ Roadmap Created            30 Jan 13:50
│
✓ All Phases Planned         30 Jan 14:30
│
● Execution In Progress      ← atual
│
○ Work Verified
│
○ Milestone Archived
```

### Opção 3: Compact Pills

```
[✓ Created] [✓ Reqs] [✓ Roadmap] [✓ Planning] [● Executing] [○ Verified] [○ Archived]
```

## Lógica de Renderização

```typescript
interface WorkflowStage {
  id: string;
  name: string;
  description: string;
  status: 'pending' | 'in_progress' | 'complete';
  completed_at: string | null;
}

interface Workflow {
  current_stage: string;
  stages: WorkflowStage[];
}

// Exemplo de renderização
function renderStage(stage: WorkflowStage, isCurrent: boolean) {
  const icon = {
    'complete': '✓',
    'in_progress': '●',
    'pending': '○'
  }[stage.status];

  const color = {
    'complete': 'green',
    'in_progress': 'blue',
    'pending': 'gray'
  }[stage.status];

  return {
    icon,
    color,
    name: stage.name,
    timestamp: stage.completed_at ? formatDate(stage.completed_at) : null,
    isCurrent
  };
}
```

## Ordem das Etapas (Fixa)

A ordem é sempre a mesma:

1. **created** — Milestone criado (pasta + MongoDB)
2. **requirements** — Requisitos definidos (REQUIREMENTS.md)
3. **roadmap** — Roadmap criado (ROADMAP.md com fases)
4. **planning** — Todas as fases planejadas (PLANs existem)
5. **executing** — Execução em progresso (código sendo escrito)
6. **verified** — Trabalho verificado (UAT passou)
7. **archived** — Milestone arquivado (movido para milestones/)

## Quando Cada Etapa é Completada

| Etapa | Comando que Completa |
|-------|---------------------|
| created | `/wxcode:new-milestone` cria pasta |
| requirements | `/wxcode:new-milestone` gera REQUIREMENTS.md |
| roadmap | `/wxcode:new-milestone` gera ROADMAP.md |
| planning | `/wxcode:plan-phase` (quando todas as fases têm PLAN) |
| executing | `/wxcode:execute-phase` (quando todos os PLANs têm SUMMARY) |
| verified | `/wxcode:verify-work` passa UAT |
| archived | `/wxcode:complete-milestone` finaliza |

## Exemplo Completo

### Milestone em Progresso (Executando)

```json
{
  "milestone": {
    "folder_name": "v1.0-PAGE_Login",
    "status": "in_progress"
  },
  "workflow": {
    "current_stage": "executing",
    "stages": [
      { "id": "created", "status": "complete", "completed_at": "2026-01-30T13:43:00Z" },
      { "id": "requirements", "status": "complete", "completed_at": "2026-01-30T13:45:00Z" },
      { "id": "roadmap", "status": "complete", "completed_at": "2026-01-30T13:50:00Z" },
      { "id": "planning", "status": "complete", "completed_at": "2026-01-30T14:30:00Z" },
      { "id": "executing", "status": "in_progress", "completed_at": null },
      { "id": "verified", "status": "pending", "completed_at": null },
      { "id": "archived", "status": "pending", "completed_at": null }
    ]
  }
}
```

### Milestone Completo (Arquivado)

```json
{
  "milestone": {
    "folder_name": "v1.0-PAGE_Login",
    "status": "completed"
  },
  "workflow": {
    "current_stage": "archived",
    "stages": [
      { "id": "created", "status": "complete", "completed_at": "2026-01-30T13:43:00Z" },
      { "id": "requirements", "status": "complete", "completed_at": "2026-01-30T13:45:00Z" },
      { "id": "roadmap", "status": "complete", "completed_at": "2026-01-30T13:50:00Z" },
      { "id": "planning", "status": "complete", "completed_at": "2026-01-30T14:30:00Z" },
      { "id": "executing", "status": "complete", "completed_at": "2026-01-30T15:45:00Z" },
      { "id": "verified", "status": "complete", "completed_at": "2026-01-30T15:50:00Z" },
      { "id": "archived", "status": "complete", "completed_at": "2026-01-30T15:57:00Z" }
    ]
  }
}
```

## Breaking Changes

Nenhum. A seção `workflow` é nova e aditiva. O resto do schema permanece inalterado.

## Versão

Esta mudança foi introduzida na **WXCODE v1.2.5**.
