# WXCODE Changelog

All notable changes to WXCODE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.9] - 2026-01-31

### Changed
- **`/wxcode:create-start-dev`**: Always recreate file, never skip if exists
- **`/wxcode:create-start-dev`**: Auto-invoke `/wxcode:start-dev` after creation

## [1.2.8] - 2026-01-31

### Changed
- **`/wxcode:create-start-dev`**: Clearer instructions for placeholder substitution
  - Explicit example showing template → final transformation
  - Emphasized that NO placeholders should remain in output

## [1.2.7] - 2026-01-31

### Added
- **start-dev templates in MongoDB**: All 15 stacks now have `start_dev_template` field with:
  - Standardized ports (7xxx series)
  - Auto-kill of processes on required ports
  - Log redirection to `/tmp/{project_name}.log`
  - PID file management for process control

- **`/wxcode:create-start-dev` skill**: Generate start-dev.sh from stack template
  - Detects project stack from configuration
  - Fetches template from MongoDB via MCP
  - Substitutes port placeholders
  - Sets executable permissions

- **`/wxcode:start-dev` skill**: Execute start-dev.sh
  - Verifies script exists
  - Executes and validates server startup
  - Displays access URLs and log location

### Changed
- **`/wxcode:new-project`**: Now uses `/wxcode:create-start-dev` and `/wxcode:start-dev` instead of manual script creation
- **Port standardization**: All stacks use 7xxx ports:
  - Server-Rendered: 7300-7340
  - SPA: 7380-7389 (backend/frontend pairs)
  - Fullstack: 7400-7440

## [1.2.6] - 2026-01-30

### Added
- **wxcode-planner**: Conversion context section with MCP Source of Truth
  - Detects conversion projects automatically
  - Queries MCP for legacy element details if RESEARCH.md incomplete
  - Checks dependency conversion status before planning
  - Uses stack conventions from MCP
  - Searches similar conversions for patterns

- **wxcode-plan-checker**: Dimension 7 - Conversion Coverage
  - Verifies all legacy controls have corresponding tasks
  - Verifies all legacy procedures have corresponding tasks
  - Checks dependency conversion status
  - Flags missing conversion items as blockers

- **wxcode-verifier**: Step 1.5 and Step 6.5 for conversion verification
  - Loads legacy element from MCP as Source of Truth
  - Builds conversion verification matrix
  - Verifies all controls converted
  - Verifies all procedures converted
  - Verifies data bindings preserved
  - Checks behavior equivalence
  - Adds conversion gaps to gap output

### Changed
- All three agents now use MCP wxcode-kb as Source of Truth for conversion projects
- Conversion projects get additional verification dimensions

## [1.2.5] - 2026-01-30

### Added
- Workflow stages tracking in milestone dashboard schema
- 7-stage lifecycle: created → requirements → roadmap → planning → executing → verified → archived
- `workflow.current_stage` field to identify active stage
- `workflow.stages[].completed_at` timestamps for each stage
- Stage detection logic documentation

### Dashboard Schema
- `workflow.current_stage` — identifies the active stage
- `workflow.stages[]` — array of 7 lifecycle stages with status and timestamps
- Each stage: id, name, description, status (pending/in_progress/complete), completed_at

## [1.2.4] - 2026-01-30

### Added
- Tasks included in milestone dashboard schema
- Progress tracking for plans and tasks (not just phases)
- Complete real-world example in dashboard-schema-milestone.md

### Changed
- `/wxcode:new-milestone` now accepts `--element` and `--output-project` arguments
- Version determined automatically by agent (UI doesn't pass version)
- Milestone created in MongoDB immediately after folder creation (Phase 1.6)
- Removed redundant Phase 9.5 (milestone creation moved earlier)

### Dashboard Schema
- `progress.plans_complete/total/percentage` — track plan completion
- `progress.tasks_complete/total/percentage` — track task completion
- `phases[].plans[].tasks[]` — detailed task list per plan
- Task fields: id, name, file, status, description

## [1.2.3] - 2026-01-30

### Added
- Split dashboard schemas: project-level and milestone-level
- `dashboard-schema-project.md`: Global project dashboard schema
- `dashboard-schema-milestone.md`: Per-milestone dashboard schema
- `dashboard-migration-prompt.md`: Migration guide for UI integration
- Hybrid approach for conversion progress (MCP = source of truth)

### Changed
- All dashboard-emitting commands now update TWO dashboards:
  - `.planning/dashboard.json` (project)
  - `.planning/dashboard_<milestone>.json` (milestone-specific)
- `/wxcode:new-milestone` now creates Milestone in MongoDB via MCP
- Commands updated: new-project, new-milestone, plan-phase, execute-phase, verify-work, complete-milestone
- Added `mcp__wxcode-kb__get_conversion_stats` to all dashboard-emitting commands
- Added `mcp__wxcode-kb__create_milestone` to new-milestone command

### New MCP Tool Required
- `create_milestone`: Creates Milestone in MongoDB with wxcode_version and milestone_folder_name

### Dashboard Structure
```
.planning/
├── dashboard.json                 # Project (global)
├── dashboard_v1.0-PAGE_Login.json # Milestone
└── dashboard_v1.1-PAGE_Dashboard.json
```

## [1.2.2] - 2026-01-29

### Changed
- Research agents now prioritize legacy analysis for conversion projects
- `wxcode-phase-researcher`: Complete conversion research flow with dependency analysis
- `wxcode-project-researcher`: Legacy inventory and conversion sequence output
- New output formats: LEGACY-INVENTORY.md, CONVERSION-SEQUENCE.md
- Researchers verify dependencies are converted before proceeding
- Researchers analyze output project architecture patterns

### Priority for Conversion Projects
1. Understand legacy code (source, UI, business rules)
2. Analyze dependencies (what's converted, what's blocking)
3. Check output project patterns (follow existing architecture)
4. Identify conversion challenges
5. Stack research is secondary (target stack already defined)

## [1.2.1] - 2026-01-29

### Added
- `mcp__wxcode-kb__*` wildcard to all conversion-relevant agents
- `mcp-discovery.md` reference file for dynamic MCP tool discovery
- Conversion context sections in key agents (researchers, executor)

### Changed
- Agents now discover MCP tools dynamically instead of hardcoded list
- Fixed `wxcode-legacy-analyzer` and `wxcode-conversion-advisor` MCP prefix (was `mcp__wxcode__`, now `mcp__wxcode-kb__`)

### Agents Updated
- wxcode-phase-researcher
- wxcode-project-researcher
- wxcode-planner
- wxcode-executor
- wxcode-verifier
- wxcode-roadmapper
- wxcode-plan-checker
- wxcode-debugger
- wxcode-codebase-mapper
- wxcode-integration-checker
- wxcode-legacy-analyzer
- wxcode-conversion-advisor

## [1.2.0] - 2026-01-29

### Added
- `/wxcode:dashboard` command for manual dashboard generation
- `dashboard-schema.md` reference file with exact JSON schema

### Fixed
- Dashboard JSON format now deterministic (all commands reference exact schema)
- All dashboard-generating commands updated with explicit schema reference:
  - `/wxcode:new-project`
  - `/wxcode:new-milestone`
  - `/wxcode:plan-phase`
  - `/wxcode:execute-phase`
  - `/wxcode:verify-work`
  - `/wxcode:complete-milestone`

## [1.1.9] - 2026-01-29

### Added
- Dashboard now writes JSON to `.planning/dashboard.json`
- Watcher notification: `[WXCODE:DASHBOARD_UPDATED] .planning/dashboard.json`
- Dashboard update integrated into key commands:
  - `/wxcode:new-project`
  - `/wxcode:new-milestone`
  - `/wxcode:plan-phase`
  - `/wxcode:execute-phase`
  - `/wxcode:verify-work`
  - `/wxcode:complete-milestone`

## [1.1.8] - 2026-01-29

### Added
- `/wxcode:dashboard` command that returns project progress as JSON
  - Structured data for UI rendering (accordions, progress bars)
  - Includes: project info, phases with plans, requirements by category
  - Supports conversion projects, milestones history, blockers, todos
  - Reads from `.planning/` and `.milestones/` directories

## [1.1.7] - 2026-01-29

### Fixed
- Built hooks (`hooks/dist/`) now included in repo for GitHub installs
- Statusline now correctly shows `/wxcode:update` instead of `/gsd:update`

## [1.1.6] - 2026-01-29

### Changed
- MCP check now uses `health_check` tool instead of `get_conversion_stats`
- Retry logic: 3 attempts with 10s delay between each
- Shows "✓ WXCODE MCP conectado" on successful connection

## [1.1.5] - 2026-01-29

### Fixed
- MCP availability check now calls tool directly instead of searching
- Prevents false negatives when MCP is available but deferred tools search fails

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
| 1.2.6 | 1.9.13 | 2026-01-30 | MCP Source of Truth for planning/verification agents |
| 1.2.5 | 1.9.13 | 2026-01-30 | Workflow stages in milestone dashboard |
| 1.2.4 | 1.9.13 | 2026-01-30 | Tasks in milestone dashboard |
| 1.2.3 | 1.9.13 | 2026-01-30 | Split dashboard schemas (project/milestone) |
| 1.2.2 | 1.9.13 | 2026-01-29 | Conversion-first research priority |
| 1.2.1 | 1.9.13 | 2026-01-29 | Dynamic MCP tool discovery for all agents |
| 1.2.0 | 1.9.13 | 2026-01-29 | Dashboard schema consistency |
| 1.1.9 | 1.9.13 | 2026-01-29 | Dashboard file + watcher notification |
| 1.1.8 | 1.9.13 | 2026-01-29 | Add /wxcode:dashboard JSON output |
| 1.1.7 | 1.9.13 | 2026-01-29 | Include built hooks for GitHub |
| 1.1.6 | 1.9.13 | 2026-01-29 | health_check with 3 retries |
| 1.1.5 | 1.9.13 | 2026-01-29 | Fix MCP check false negatives |
| 1.1.4 | 1.9.13 | 2026-01-29 | MCP availability check |
| 1.1.3 | 1.9.13 | 2026-01-29 | Added CLAUDE.md |
| 1.1.2 | 1.9.13 | 2026-01-29 | Cache-busting, pyproject.toml fix |
| 1.1.1 | 1.9.13 | 2026-01-29 | Installer fixes, start-dev.sh verification |
| 1.1.0 | 1.9.13 | 2026-01-29 | Conversion mode for new-project |
| 1.0.0 | 1.9.13 | 2026-01-25 | Initial fork |

---

## Attribution

WXCODE is a customized fork of [GSD (Get Shit Done)](https://github.com/glittercowboy/get-shit-done) by TÂCHES.
