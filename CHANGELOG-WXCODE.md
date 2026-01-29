# WXCODE Changelog

All notable changes to WXCODE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.4] - 2026-01-29

### Added
- MCP availability check in `/wxcode:new-project` (conversion mode)
- MCP availability check in `/wxcode:new-milestone` (conversion projects)
- Commands now abort with clear error if wxcode-kb MCP is not available

## [1.1.3] - 2026-01-29

### Added
- `CLAUDE.md` with complete development context for AI assistants
  - Extension architecture documentation
  - Version management requirements
  - MCP integration details
  - Common issues and fixes

## [1.1.2] - 2026-01-29

### Fixed
- `/wxcode:update` now uses cache-busting to bypass GitHub raw content cache
- `/wxcode:new-project` generates proper `pyproject.toml` with package discovery for Python stacks
- Added "Multiple top-level packages" fix to common fixes list

## [1.1.1] - 2026-01-29

### Fixed
- Install script now copies from `commands/wxcode/` instead of `commands/gsd/`
- `/wxcode:update` now clears npm cache before updating to ensure fresh download

### Added
- `/wxcode:new-project` now verifies `start-dev.sh` works before proceeding (tests server, fixes issues if needed)

### Changed
- Updated README-WXCODE.md with correct update command (includes cache clearing)

## [1.1.0] - 2026-01-29

### Added

#### Conversion Mode for `/wxcode:new-project`
- Pass CONTEXT.md as argument to activate conversion mode
- Creates complete project foundation (structure, config, entry point, start-dev.sh)
- Single question: convert schema now or on-demand
- Supports all 15 target stacks from WXCODE Conversor
- Creates `.planning/CONVERSION.md` to activate conversion mode for other commands
- Calls MCP `mark_project_initialized` on completion

#### Documentation
- `.wxcode/conversion/context-md-spec.md` — Specification for CONTEXT.md format
- `.wxcode/conversion/mcp-usage.md` — Updated to 25 MCP tools (was 19)
- `docs/CONTEXT.md` — CONTEXT.md specification for conversion projects

### Changed
- MCP tools documentation updated from 19 to 25 tools
- Reorganized MCP tools by category (Elements, Controls, Procedures, Schema, Graph, Conversion, Stack, Planes, WLanguage, Similarity, PDF)

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
| 1.1.4 | 1.9.13 | 2026-01-29 | MCP availability check |
| 1.1.3 | 1.9.13 | 2026-01-29 | Added CLAUDE.md |
| 1.1.2 | 1.9.13 | 2026-01-29 | Cache-busting, pyproject.toml fix |
| 1.1.1 | 1.9.13 | 2026-01-29 | Installer fixes, start-dev.sh verification |
| 1.1.0 | 1.9.13 | 2026-01-29 | Conversion mode for new-project |
| 1.0.0 | 1.9.13 | 2026-01-25 | Initial fork |

---

## Attribution

WXCODE is a customized fork of [GSD (Get Shit Done)](https://github.com/glittercowboy/get-shit-done) by TÂCHES.
