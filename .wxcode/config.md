# WXCODE Configuration

## Identity

| Property | Value |
|----------|-------|
| **Name** | WXCODE |
| **Command Prefix** | `wxcode:` |
| **Agent Prefix** | `wxcode-` |
| **Display Name** | WXCODE |
| **Base Project** | GSD (Get Shit Done) |

## Upstream

| Property | Value |
|----------|-------|
| **Repository** | https://github.com/glittercowboy/get-shit-done |
| **Branch** | main |
| **Remote Name** | upstream |

## Sync Behavior

| Setting | Value | Description |
|---------|-------|-------------|
| `auto_apply_deterministic` | true | Automatically apply rename/replace transformations |
| `conflict_mode` | hybrid | Auto-resolve trivial conflicts, ask for complex ones |
| `track_upstream_version` | true | Record upstream version after each sync |
| `preserve_local_overrides` | true | Don't touch files marked as overrides |

## Transformation Rules Reference

See `transform-rules.md` for the complete list of deterministic transformations applied during sync.

## Files

| File | Purpose |
|------|---------|
| `config.md` | This file - general configuration |
| `transform-rules.md` | Deterministic transformation rules |
| `upstream-state.md` | State of last sync with upstream |
| `customizations.md` | History of decisions made during syncs |
| `overrides.md` | Files that should ignore upstream changes |
| `decisions/` | Individual decision records per feature |

---
*Configuration for WXCODE fork management*
