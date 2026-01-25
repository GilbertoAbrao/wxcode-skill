# Customization History

Records all customization decisions made during syncs and manual customizations.

## Decision Log

### 2026-01-25 - Initial Setup

- **Date:** 2026-01-25T19:57:10Z
- **Action:** Fork initialized with GSD → WXCODE transformation
- **Upstream Version:** 1.9.13
- **Transformation Applied:** Yes
- **Changes:**
  - Renamed `commands/gsd/` → `commands/wxcode/`
  - Renamed `agents/gsd-*.md` → `agents/wxcode-*.md`
  - Renamed `hooks/gsd-*.js` → `hooks/wxcode-*.js`
  - Applied text substitutions: `gsd:` → `wxcode:`, `gsd-` → `wxcode-`, `GSD` → `WXCODE`

---

## Customizations by Command

Track which commands have been customized beyond simple renaming.

| Command | Customization | Date | Decision File |
|---------|---------------|------|---------------|
| — | — | — | — |

## Customizations by Agent

Track which agents have been customized beyond simple renaming.

| Agent | Customization | Date | Decision File |
|-------|---------------|------|---------------|
| — | — | — | — |

## Local-Only Features

Features created locally that don't exist in upstream:

| Feature | Type | Created | Description |
|---------|------|---------|-------------|
| wxcode:init | command | 2026-01-25 | Initialize WXCODE fork management |
| wxcode:sync | command | 2026-01-25 | Synchronize with upstream GSD |
| wxcode:status | command | 2026-01-25 | Show sync state |
| wxcode:discuss | command | 2026-01-25 | Explore new features |
| wxcode:customize | command | 2026-01-25 | Customize specific commands |
| wxcode:override | command | 2026-01-25 | Mark files to ignore |
| wxcode:diff | command | 2026-01-25 | Compare with upstream |
| wxcode:rollback | command | 2026-01-25 | Revert last sync |
| wxcode:history | command | 2026-01-25 | View sync history |
| wxcode:help | command | 2026-01-25 | Command reference |
| wxcode-sync-agent | agent | 2026-01-25 | Sync agent for fork management |

## Sync Decisions

Decisions made during sync operations:

| Date | Upstream Change | Decision | Rationale |
|------|-----------------|----------|-----------|
| — | — | — | — |

---
*Updated by /wxcode:sync, /wxcode:customize, and /wxcode:discuss*
