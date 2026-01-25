# WXCODE Changelog

All notable changes to WXCODE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-25

### Added

#### Fork Management System
- `/wxcode:init` — Initialize WXCODE fork management
- `/wxcode:sync` — Synchronize with upstream GSD
- `/wxcode:status` — Show current sync state
- `/wxcode:discuss` — Explore new features or changes
- `/wxcode:customize` — Customize specific commands
- `/wxcode:override` — Mark files to ignore during sync
- `/wxcode:diff` — Compare local vs upstream
- `/wxcode:rollback` — Revert last sync
- `/wxcode:history` — View sync and customization history
- `/wxcode:help` — Command reference for fork management

#### Configuration
- `.wxcode/config.md` — Identity and settings
- `.wxcode/transform-rules.md` — GSD → WXCODE transformation rules
- `.wxcode/upstream-state.md` — Sync state tracking
- `.wxcode/customizations.md` — Decision history
- `.wxcode/overrides.md` — Files to skip during sync
- `.wxcode/decisions/` — Per-command decision records

#### Agent
- `wxcode-sync-agent` — Intelligent sync agent for fork management

### Changed

- All commands renamed from `gsd:*` to `wxcode:*`
- All agents renamed from `gsd-*` to `wxcode-*`
- All hooks renamed from `gsd-*` to `wxcode-*`
- Display names changed from "GSD" to "WXCODE"

### Based On

- **GSD v1.9.13** (commit `3d2a960`)
- [GSD Repository](https://github.com/glittercowboy/get-shit-done)

---

## Upstream Sync History

| WXCODE Version | GSD Version | Sync Date | Notes |
|----------------|-------------|-----------|-------|
| 1.0.0 | 1.9.13 | 2026-01-25 | Initial fork |

---

## Attribution

WXCODE is a customized fork of [GSD (Get Shit Done)](https://github.com/glittercowboy/get-shit-done) by TÂCHES.
