# WXCODE Changelog

All notable changes to WXCODE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.33] - 2026-02-06

### Added
- **Restored 27 GSD commands from upstream `main` branch**
  - `commands/gsd/` now contains all original GSD commands (was only `help.md`)
  - Enables non-WXCODE projects (e.g., guest-portal) to use `/gsd:*` commands via symlink
  - Commands are exact upstream copies with `gsd:` namespace
  - No changes to installer — it already copies `commands/gsd/` to storage
  - Commands restored: add-phase, add-todo, audit-milestone, check-todos, complete-milestone, debug, discuss-phase, execute-phase, help, insert-phase, join-discord, list-phase-assumptions, map-codebase, new-milestone, new-project, pause-work, plan-milestone-gaps, plan-phase, progress, quick, remove-phase, research-phase, resume-work, set-profile, settings, update, verify-work

## [1.4.32] - 2026-02-06

### Fixed
- **HEADER + visual banner now emitted together** (no blank line between them)
  - Fixes streaming issue where HEADER comment could arrive in separate chunk from visual title
  - All 46 commands updated: `## TITLE` immediately follows HEADER comment
  - Updated structured output specs (v1.2.0) with new pattern and best practice
  - Pattern: `<!-- WXCODE:HEADER:... -->\n## WXCODE ▶ TITLE` (no blank line)

## [1.4.31] - 2026-02-06

### Changed
- **ALL commands are now project-level (GSD + WXCODE)**
  - Neither `/gsd:*` nor `/wxcode:*` commands are globally visible
  - Only 4 wxcode bootstrap commands stay global (`new-project`, `help`, `version`, `update`)
  - Installer stores commands in `~/.claude/get-shit-done/commands/{gsd,wxcode}/`
  - Projects create symlinks to access the commands they need
  - `/wxcode:new-project` creates wxcode symlink automatically
  - `/wxcode:new-milestone` ensures wxcode symlink exists
  - Old global GSD commands cleaned up automatically on update
  - See `docs/command-scoping.md` for full architecture

### Added
- **`docs/command-scoping.md`** — complete documentation of command scoping architecture
  - Local vs cloud deployment scenarios
  - How symlinks work for each project type
  - Setup instructions for GSD, WXCODE, and wxcode-ui projects
  - FAQ section

## [1.4.30] - 2026-02-06

### Changed
- **WXCODE commands are now project-level, not global** (superseded by 1.4.31)

### Fixed
- **`/wxcode:new-project` dashboard section** no longer references non-existent Python script

## [1.4.29] - 2026-02-05

### Fixed
- **`/wxcode:dashboard` now emits structured output correctly**
  - Added Step 0: HEADER emission at start
  - Added STATUS markers throughout process (5% → 15% → 30% → 45% → 60% → 80% → 100%)
  - Added NEXT_ACTION at completion
  - Removed references to non-existent Python script
  - Proper step numbering (0-7)
  - Updated troubleshooting section

## [1.4.28] - 2026-02-05

### Fixed
- **`/wxcode:new-milestone` now calls `/wxcode:dashboard --all` at completion**
  - Added Phase 10 for dashboard regeneration
  - Removed reference to non-existent Python script
  - Updates project dashboard, milestone dashboard, and schema dashboard
  - Ensures UI reflects new milestone state

## [1.4.27] - 2026-02-05

### Added
- **`/wxcode:design-system` watcher notifications**
  - Emits `[WXCODE:DESIGN_TOKENS_UPDATED] design/tokens.json` on completion
  - Emits `[WXCODE:DESIGN_VARIABLES_UPDATED] design/variables.css` on completion
  - UI can listen for these to refresh design panel
  - Documented in SCHEMA-DASHBOARD-SPEC.md section 20.4

## [1.4.26] - 2026-02-05

### Fixed
- **`/wxcode:design-system` now emits structured output markers**
  - Added HEADER at command start
  - Added STATUS markers throughout process (Steps 3-7)
  - Added ERROR marker for missing tokens.json on --regenerate
  - Added NEXT_ACTION at completion
  - Compliant with STRUCTURED-OUTPUT-SPEC.md

## [1.4.25] - 2026-02-05

### Changed
- **`wxcode-executor` screenshot handling: graceful fallback**
  - Added note: screenshot may not exist or may return invalid image
  - If screenshot unavailable/invalid, ignore and proceed with conversion
  - Use control hierarchy, planes analysis, and code structure instead
  - Do not block execution waiting for valid screenshot

## [1.4.24] - 2026-02-05

### Changed
- **`wxcode-executor` frontend-design directive now fetches legacy screenshots**
  - For conversion projects, uses `get_element_pdf_slice` MCP tool to get legacy page screenshot
  - Screenshot provides visual reference of original control layout
  - Added warning about WinDev/WebDev planes: screenshot shows only one plane
  - Instructs to check `get_element_planes` for multi-plane pages (tabs, wizards, etc.)
  - Planes analysis passed to frontend-design skill for modern equivalent suggestions

## [1.4.23] - 2026-02-05

### Added
- **Watcher notifications for schema dashboard**
  - `[WXCODE:SCHEMA_DASHBOARD_UPDATED] .planning/schema-dashboard.json`
  - `[WXCODE:SCHEMA_STATUS_UPDATED] .planning/SCHEMA-STATUS.md`
  - UI can listen for these to refresh datamodel panel
  - Documented in SCHEMA-DASHBOARD-SPEC.md section 20.4

## [1.4.22] - 2026-02-05

### Changed
- **`/wxcode:dashboard --all` now regenerates schema dashboard**
  - For conversion projects, invokes `/wxcode:schema-dashboard`
  - Generates `.planning/schema-dashboard.json` for UI datamodel panel
  - Generates `.planning/SCHEMA-STATUS.md` for human review
  - Added to success criteria and summary output

## [1.4.21] - 2026-02-05

### Added
- **New command: `/wxcode:schema-dashboard`**
  - Generates stack-agnostic JSON dashboard of all database models
  - Output: `.planning/schema-dashboard.json` (for UI consumption)
  - Output: `.planning/SCHEMA-STATUS.md` (human-readable summary)
  - Comprehensive schema format covering ALL database elements:
    - Tables with full column details (type, size, precision, scale, nullable, default, computed)
    - Primary keys, foreign keys, indexes, unique constraints, check constraints
    - Relationships (one-to-one, one-to-many, many-to-many) with all metadata
    - Enums, views, sequences, functions, procedures, triggers
    - Composite types, domains, extensions
    - Type normalization from any ORM to base types
  - Parsers for: SQLAlchemy, Prisma, TypeORM, Django, Sequelize
  - Coverage comparison against legacy schema from MCP

### Changed
- **`wxcode-schema-generator` now triggers dashboard update**
  - After generate_all_models: updates dashboard
  - After generate_specific_models: updates dashboard
  - After validate_models: updates dashboard
  - Ensures UI always has current schema information

## [1.4.20] - 2026-02-05

### Added
- **New command: `/wxcode:validate-schema`**
  - Validates database models against legacy schema via MCP
  - Reports missing models and mapping issues
  - `--fix` flag to auto-generate missing models
  - `--table=NAME` flag to validate specific table
  - Only works for conversion projects

### Changed
- **`/wxcode:new-milestone` Phase 1.8: Ensure Database Models**
  - Gets element's table dependencies via MCP
  - Checks which models already exist
  - Spawns wxcode-schema-generator for missing models
  - Ensures all required tables have models before milestone work begins

- **`/wxcode:execute-phase` Step 1.5: Check database model requirements**
  - For conversion projects, validates models before phase execution
  - Detects database-related phases by name pattern
  - Spawns wxcode-schema-generator to validate/generate missing models
  - Blocks execution if required models cannot be generated

## [1.4.19] - 2026-02-05

### Changed
- **`/wxcode:new-project` Phase C4 now uses `wxcode-schema-generator` agent**
  - Replaced inline schema conversion logic with agent call
  - Ensures exact legacy table/column name preservation
  - Added validation step after generation
  - "On-demand" mode now creates proper base infrastructure with comments

## [1.4.18] - 2026-02-05

### Added
- **New agent: `wxcode-schema-generator`**
  - Generates ORM models from legacy schema via MCP
  - Preserves exact table/column names for transparent legacy database access
  - Supports SQLAlchemy, Prisma, TypeORM, Django, Sequelize
  - Capabilities: generate_all_models, generate_specific_models, validate_models, get_missing_tables
  - Called by: new-project (Phase C4), new-milestone, execute-phase
  - Ensures new application can access legacy data without schema drift

## [1.4.17] - 2026-02-05

### Fixed
- **`/wxcode:progress` suggesting milestone completion with incomplete phases**
  - Bug: When reaching the last phase number, Route D (milestone complete) was triggered even if other phases weren't executed
  - Fix: Now verifies ALL phases have `summaries >= plans` before suggesting `/wxcode:complete-milestone`
  - Added explicit loop to check completion status of each phase directory
  - Route C now handles "at last phase but incomplete phases exist" by finding the next incomplete phase

## [1.4.16] - 2026-02-04

### Added
- **Output Language Internationalization**
  - Commands now check `.planning/config.json` for `output_language` setting
  - Supported languages: `en` (English), `pt-BR` (Portuguese), `es` (Spanish)
  - Human-readable outputs localized; command names and technical terms stay in English
  - Added language preference question in `/wxcode:new-project` workflow (Phase 5, Round 1.5)
  - Added language setting in `/wxcode:settings` command (6 settings now: profile, language, 3 workflow toggles, branching)
  - Added quick command: `/wxcode:settings language pt-BR`
  - Updated `structured-output.md` with "Output Language" section and best practice #7

## [1.4.15] - 2026-02-05

### Fixed
- **install.js not copying commands/wxcode/ directory**
  - Added copy logic for `commands/wxcode/` in Claude Code & Gemini installs
  - Added copy logic for `commands/wxcode/` in OpenCode flat structure
  - Added uninstall cleanup for `commands/wxcode/` directory
  - This fixes `/wxcode:update` not updating wxcode commands

## [1.4.14] - 2026-02-04

### Fixed
- **100% Structured Output Coverage**
  - Fixed 12 commands missing inline STATUS/NEXT_ACTION markers
  - All 44 WXCODE commands now emit parseable structured output
  - Commands fixed: diff, help, history, join-discord, mcp-health-check, new-project-greetings, override, rollback, set-profile, settings, status, version
  - Added ERROR markers for failure scenarios
  - Terminal commands (help, version, etc.) correctly emit STATUS without NEXT_ACTION

## [1.4.13] - 2026-02-04

### Added
- **Structured Output for UI Parsing**
  - All 44 WXCODE commands now emit structured markers (`<!-- WXCODE:TYPE:JSON -->`)
  - Enables chat UIs to parse and render: headers, status/progress, tool calls, errors, next actions
  - Created `get-shit-done/references/structured-output.md` specification
  - Created `docs/STRUCTURED-OUTPUT-SPEC.md` with complete parsing guide (TypeScript/Python examples)
  - Format uses HTML comments (invisible in markdown rendering)

### Event Types
- `HEADER` — Command title and context
- `STATUS` — Progress updates with percentage
- `TOOL` — Tool call notifications
- `TOOL_RESULT` — Tool completion results
- `NEXT_ACTION` — Suggested next command with priority
- `ERROR` — Error details with recovery suggestions

## [1.4.12] - 2026-02-04

### Added
- **`/wxcode:complete-milestone` MCP integration**
  - Added `mcp__wxcode-kb__update_milestone_status` to allowed-tools
  - New step 8 to update milestone status in KB after commit/tag
  - Marks milestone as `completed` in MongoDB via MCP tool

## [1.4.11] - 2026-02-04

### Changed
- **WXCODE ASCII art banner**
  - Replaced GSD ASCII logo with WXCODE logo in installer
  - Added `bin/install.js` banner section to overrides.md
  - Future syncs will preserve WXCODE branding

## [1.4.10] - 2026-02-04

### Changed
- **`/wxcode:sync` folder path protection**
  - Added explicit verification step for bin/install.js after transformation
  - Added post_sync_verification section with mandatory folder path checks
  - Updated success_criteria to include folder path verification
- **`wxcode-sync-agent` transformation rules**
  - Updated transformation function to explicitly exclude `'get-shit-done'` folder paths
  - Added CRITICAL: Folder Path Exclusions table with patterns that must NOT be transformed
  - Added verification commands after transformation

## [1.4.9] - 2026-02-03

### Fixed
- **Installer broken after GSD sync**
  - Sync incorrectly transformed `'get-shit-done'` folder paths to `'wxcode'`
  - The `get-shit-done/` folder (references/templates) keeps its original name
  - Fixed paths in install.js: skillSrc, skillDest, changelogDest, versionDest
  - Added exclusions to transform-rules.md for folder paths

## [1.4.8] - 2026-02-03

### Fixed
- **Dashboard generation for archived milestones**
  - Archived milestones now correctly show all workflow stages as "complete"
  - Requirements progress shows 100% for archived milestones (not 0%)
  - Script now finds archived files with version prefix (e.g., `v1.0-REQUIREMENTS.md`)
  - Fixed file path detection for nested milestone structures
- **`/wxcode:complete-milestone` not regenerating dashboards**
  - Added explicit step 8 to process to run `generate-dashboard.py`
  - Dashboard regeneration is now part of the workflow, not just a footnote

## [1.4.7] - 2026-02-03

### Fixed
- **`/wxcode:verify-work` not suggesting audit-milestone after last phase**
  - Workflow was always suggesting "plan-phase next" without checking if milestone complete
  - Now detects if current phase is last phase and routes to `/wxcode:audit-milestone`
  - Consistent with Route B in verify-work.md command

### Changed
- **Synced with upstream GSD v1.11.1**
  - Git branching strategy configuration (none/phase/milestone)
  - Squash merge option at milestone completion
  - Context compliance verification in plan checker
  - CONTEXT.md flow fix to downstream agents
  - Native Gemini CLI support

## [1.4.6] - 2026-02-02

### Added
- **`/wxcode:version`** — Display current WXCODE version and installation paths

## [1.4.5] - 2026-02-02

### Fixed
- **`/wxcode:new-milestone` not calling MCP create_milestone**
  - Added emphatic CRITICAL markers and visual box around MCP call requirement
  - Added Phase 1.7 gate check to verify MCP was called before Phase 2
  - Added checkpoint verification to prevent skipping the MCP tool call
  - Updated success criteria with explicit CRITICAL tags

## [1.4.4] - 2026-02-02

### Fixed
- **Python dashboard script not installed**
  - Installer now copies `bin/` folder to `~/.claude/get-shit-done/bin/`
  - `generate-dashboard.py` now available after installation
  - Fixes "No such file or directory" error for dashboard commands

## [1.4.3] - 2026-02-02

### Changed
- **All commands now use Python script for dashboard updates**
  - Replaced LLM-based dashboard generation in 9 commands
  - Commands affected: add-phase, complete-milestone, execute-phase, insert-phase, new-milestone, new-project, plan-phase, remove-phase, verify-work
  - All now call `python3 ~/.claude/get-shit-done/bin/generate-dashboard.py --all`
  - Ensures consistent, deterministic dashboard JSON with tasks

## [1.4.2] - 2026-02-02

### Changed
- **`/wxcode:design-system` now uses MCP Playwright exclusively**
  - Replaces WebFetch with `mcp__playwright__navigate` + `mcp__playwright__screenshot`
  - Better support for JS-rendered sites and SPAs
  - No CSP blocking issues
- Added "Enter my own URL" as first option in URL selection

## [1.4.1] - 2026-02-02

### Added
- **`/wxcode:design-system` standalone command**
  - Interactive mode to choose method (URL, screenshots, questionnaire)
  - `--url <url>` — Extract design tokens from live website
  - `--screenshots` — Analyze design mockups/images
  - `--questionnaire` — 12 structured questions
  - `--regenerate` — Rebuild stack files from existing tokens.json
  - Generates DTCG tokens, CSS variables, Tailwind config, and README

## [1.4.0] - 2026-02-02

### Added
- **Deterministic Python dashboard generator** (`bin/generate-dashboard.py`)
  - Replaces LLM-based JSON generation with deterministic script
  - Parses `.planning/` files and extracts tasks from XML `<task>` blocks
  - Generates proper nested `phases[].plans[].tasks[]` structure
  - Handles both nested and flat milestone structures
  - Falls back to root `phases/` when milestone folder is empty marker
  - Outputs `[WXCODE:DASHBOARD_UPDATED]` notifications

### Changed
- `/wxcode:dashboard` now calls Python script instead of generating JSON via LLM

## [1.3.9] - 2026-02-02

### Fixed
- **`--all` flag not forcing regeneration**
  - Added explicit instruction that `--all` means REGENERATE from source files
  - Prevents "already updated" skip behavior
- **PLAN.md file naming pattern incorrect**
  - Fixed: `01-01-PLAN.md` (actual) not `1.1-PLAN.md` (documented)
- **Milestone dashboard missing nested plans/tasks structure**
  - Added critical requirement for nested `phases[].plans[].tasks[]` structure
  - Prevents simplified structure without task details

## [1.3.8] - 2026-02-02

### Fixed
- **Milestone dashboard not detecting phases in flat structure**
  - Now supports both nested (`.planning/v1.0-PAGE_Login/phases/`) and flat (`.planning/phases/`) structures
  - Auto-detects which structure exists and uses correct paths
  - Fixes ROADMAP.md, REQUIREMENTS.md, and phases directory location

## [1.3.7] - 2026-02-02

### Fixed
- **Milestone dashboard shows 0/0 for plans and tasks**
  - Fixed PLAN.md path discovery: files are in `${MILESTONE_FOLDER}/phases/01-*/`
  - Fixed task parsing format: uses XML (`<task>`) not Markdown
  - Added explicit progress calculation from populated phases array
- **Workflow stage shows "Planning" when executing**
  - Fixed workflow stage detection: "executing" now shows `in_progress` when some (but not all) phases have SUMMARY.md
  - `current_stage` now finds first stage with `in_progress` status

## [1.3.6] - 2026-02-02

### Fixed
- **CRITICAL: Never infer table structure in conversion projects**
  - Added explicit rule to `wxcode-planner`: Must query `mcp__wxcode-kb__get_table` for missing tables
  - Added explicit rule to `wxcode-phase-researcher`: Must resolve table schema from MCP, not infer
  - CONTEXT.md is snapshot only, MCP is Source of Truth for database schema

## [1.3.5] - 2026-02-02

### Added
- `/wxcode:new-project-greetings` command for MCP warm-up before conversion
  - Displays project context from CONTEXT.md
  - Gives MCP servers time to connect in background
  - Suggests `/wxcode:new-project` as next step

## [1.3.4] - 2026-02-02

### Changed
- MCP availability check: 10 attempts (was 5) for ~100s total wait

## [1.3.3] - 2026-02-02

### Changed
- MCP availability check improved: 5s initial delay + 5 attempts (was 3) for ~50s total wait
- Error message now suggests `/wxcode:mcp-health-check` for manual testing

## [1.3.2] - 2026-02-02

### Added
- `/wxcode:mcp-health-check` command to test wxcode-kb MCP server connectivity

## [1.3.1] - 2026-02-02

### Fixed
- MCP availability check now explicitly uses `health_check` tool instead of potentially using `get_conversion_stats`

## [1.3.0] - 2026-02-02

### Added
- **DTCG Design System Integration**: Design tokens as Single Source of Truth for UI generation
  - New phase in `/wxcode:new-project` for design system collection (both Greenfield and Conversion modes)
  - 3 collection methods: URL extraction, Screenshots analysis, Questionnaire
  - Generates `design/tokens.json` in DTCG (Design Token Community Group) W3C format
  - WebFetch for URL extraction with MCP Playwright fallback for JavaScript-rendered pages
  - Stack-specific config generation (Tailwind theme or CSS variables)

- **Design tokens documentation**:
  - `.wxcode/conversion/dtcg-spec.md` — Complete DTCG token specification
  - `.wxcode/conversion/design-system-flow.md` — Design system collection flow documentation
  - `get-shit-done/templates/design-tokens.json` — Ready-to-use default tokens template

- **wxcode-executor design system integration**:
  - Automatic design token loading for UI tasks
  - Mandatory `frontend-design` skill usage for visual components
  - Quality checks for token usage before commits
  - Design system usage documentation in SUMMARY.md

### Changed
- `/wxcode:new-project` now includes design system collection phase (C2.5 for conversion, 5.6 for greenfield)
- Added `WebFetch` and `mcp__playwright__*` to allowed-tools in new-project command

## [1.2.16] - 2026-02-02

### Added
- **`/wxcode:trace` command**: Bidirectional navigation between legacy and converted code
  - Trace from legacy element: `/wxcode:trace PAGE_Login` shows converted files, control mappings, procedure mappings
  - Trace from converted file: `/wxcode:trace app/routes/auth.py` shows legacy origins
  - Displays deviations from legacy behavior
  - Shows dependencies and conversion status
  - Supports `--json` output for tooling integration

- **Mandatory `@legacy` traceability comments**: Updated `structure-preservation.md` with required comment format
  - File-level headers: `@legacy-element`, `@legacy-type`, `@legacy-controls`, `@legacy-procedures`, `@legacy-tables`
  - Function-level: `@legacy: {PROCEDURE_NAME}` with optional `@legacy-params` mapping
  - Inline references: `@legacy: {ELEMENT}` for specific code sections
  - Deviation documentation: `@legacy-deviation: {description}`
  - Enables grep-based navigation: `grep -r "@legacy: PAGE_Login" .`

## [1.2.15] - 2026-01-31

### Added
- **MCP health_check precondition**: Added to all commands that use wxcode-kb MCP
  - `/wxcode:create-start-dev` - Phase 0 health check
  - `/wxcode:execute-phase` - Step 0 health check
  - `/wxcode:plan-phase` - Step 0 health check
  - `/wxcode:verify-work` - Step 0 health check
  - `/wxcode:new-project` - already had (unchanged)
  - `/wxcode:new-milestone` - already had (unchanged)
  - `/wxcode:complete-milestone` - excluded (doesn't need MCP)

### Changed
- **Wildcard MCP patterns**: All commands now use `mcp__wxcode-kb__*` instead of specific tool names

## [1.2.14] - 2026-01-31

### Changed
- **All data access via wxcode-kb MCP**: Removed direct `mcp__mongodb__*` access
  - `/wxcode:new-project` now uses `get_stack_conventions(stack_id=...)`
  - `/wxcode:create-start-dev` now uses `get_stack_conventions(stack_id=...)`
  - Single source of truth: wxcode-kb MCP server

## [1.2.13] - 2026-01-31

### Fixed
- **MCP tools in skills**: Use wildcard patterns `mcp__wxcode-kb__*` and `mcp__mongodb__*`
  instead of specific tool names to ensure MCP access in skills

## [1.2.12] - 2026-01-31

### Changed
- **Installer branding**: Shows WXCODE ASCII art instead of GSD during installation
- Updated banner text to "WinDev/WebDev code conversion system"

## [1.2.11] - 2026-01-31

### Changed
- **`/wxcode:new-project`**: Adaptive database config based on stack ORM
  - Fetches ORM from `stacks` collection via MCP
  - Generates ORM-specific database configuration:
    - `sqlalchemy` → Python SQLAlchemy config
    - `prisma` → Prisma schema.prisma
    - `typeorm` → TypeORM config for NestJS
    - `django-orm` → Django settings.py
    - `eloquent` → Laravel .env config
    - `active-record` → Rails database.yml
  - Added `mcp__mongodb__find` to allowed-tools

## [1.2.10] - 2026-01-31

### Added
- **`/wxcode:new-project`**: Development database setup in Phase C2
  - Creates `dados/dev.db` SQLite database
  - Registers connection via MCP `add_connection_outputproject`
  - Creates `.env` with DATABASE_URL pointing to SQLite
  - Added `mcp__wxcode-kb__add_connection_outputproject` to allowed-tools

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
| 1.3.0 | 1.9.13 | 2026-02-02 | DTCG Design System Integration |
| 1.2.16 | 1.9.13 | 2026-02-02 | `/wxcode:trace` and `@legacy` comments |
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
