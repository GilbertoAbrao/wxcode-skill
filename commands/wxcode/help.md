---
name: wxcode:help
description: Show available WXCODE fork management commands
---

<structured_output>
**At command start (emit before reference content):**
```
<!-- WXCODE:HEADER:{"command":"help","args":"","title":"WXCODE ▶ COMMAND REFERENCE"} -->
```
</structured_output>

<objective>
Display the complete WXCODE command reference.

**First emit the structured header, then output the reference content.**

Output ONLY the reference content below. Do NOT add:

- Project-specific analysis
- Git status or file context
- Next-step suggestions
- Any commentary beyond the reference
</objective>

<reference>
# WXCODE Command Reference

**WXCODE** is a fork management system for customizing WXCODE (Get Shit Done) while staying in sync with upstream improvements.

## Quick Start

1. `/wxcode:init` — Initialize fork management (run once)
2. `/wxcode:status` — Check for upstream updates
3. `/wxcode:sync` — Apply upstream updates with transformations

## Core Commands

### `/wxcode:init`

Initialize the WXCODE fork management system.

- Creates `.wxcode/` configuration directory
- Configures upstream Git remote
- Records initial sync state
- Optionally applies WXCODE → WXCODE transformation

**Usage:** `/wxcode:init`

Run this once when setting up your WXCODE fork.

---

### `/wxcode:sync`

Synchronize with upstream WXCODE repository.

- Fetches latest changes from upstream
- Classifies changes (deterministic, new feature, conflict)
- Applies WXCODE → WXCODE transformations automatically
- Asks for decisions on new features and conflicts
- Creates commit with all changes

**Usage:** `/wxcode:sync`

---

### `/wxcode:status`

Show current sync state and available updates.

- Compares local version with upstream
- Lists pending changes
- Shows customization and override counts
- Read-only (no changes made)

**Usage:** `/wxcode:status`

## Customization Commands

### `/wxcode:discuss`

Explore and plan new features or behavioral changes.

- Open-ended questioning to understand your needs
- Design new commands or modifications
- Creates design documents for approval
- Can implement directly or save for later

**Usage:** `/wxcode:discuss`

Use when you're not sure exactly what you want or need to explore options.

---

### `/wxcode:customize <name>`

Directly customize a specific command or agent.

- Goes straight to modifying a known target
- Focused questioning about specific changes
- Records decisions in `.wxcode/decisions/`
- Marks file as customized for future syncs

**Usage:**
- `/wxcode:customize plan-phase` — Customize the plan-phase command
- `/wxcode:customize executor` — Customize the wxcode-executor agent

Use when you know exactly what you want to modify.

## Management Commands

### `/wxcode:override <file>`

Mark a file to ignore upstream changes.

Overridden files are completely skipped during sync — you maintain them manually.

**Usage:**
- `/wxcode:override README.md` — Add file to override list
- `/wxcode:override --remove README.md` — Remove from override list
- `/wxcode:override --list` — Show all overridden files

Use for files you've completely customized (custom README, rewritten commands).

---

### `/wxcode:diff [file]`

Compare local file with upstream equivalent.

- Shows differences after applying WXCODE → WXCODE transformation
- Helps you understand what's different before syncing
- Read-only (no changes made)

**Usage:**
- `/wxcode:diff` — List all files with differences
- `/wxcode:diff plan-phase` — Compare specific command
- `/wxcode:diff commands/wxcode/help.md` — Compare by path

---

### `/wxcode:rollback`

Revert the last sync operation.

- Creates a git revert commit (preserves history)
- Restores previous sync state
- Useful when a sync introduced problems

**Usage:** `/wxcode:rollback`

---

### `/wxcode:history`

View complete sync and customization history.

- Sync timeline with versions and changes
- Customization decisions made
- Override additions/removals
- Statistics

**Usage:** `/wxcode:history`

## Development Server Commands

### `/wxcode:create-start-dev`

Generate start-dev.sh script from stack template.

- Detects project stack from configuration
- Fetches template from MongoDB via MCP
- Uses standardized ports (7xxx series)
- Sets executable permissions

**Usage:** `/wxcode:create-start-dev`

---

### `/wxcode:start-dev`

Execute start-dev.sh to start development server(s).

- Kills processes on required ports automatically
- Starts server(s) in background
- Redirects logs to `/tmp/{project_name}.log`
- Displays access URLs

**Usage:** `/wxcode:start-dev`

## Conversion Traceability Commands

### `/wxcode:trace <element|file>`

Navigate bidirectionally between legacy WinDev code and converted code.

- **Legacy → Converted:** Shows all converted files, control mappings, procedure mappings
- **Converted → Legacy:** Shows all legacy origins for a converted file
- Displays deviations from legacy behavior
- Shows conversion status and dependencies

**Usage:**
- `/wxcode:trace PAGE_Login` — Find converted code for legacy page
- `/wxcode:trace Global_ValidaCPF` — Find converted function
- `/wxcode:trace app/routes/auth.py` — Find legacy origins of file
- `/wxcode:trace PAGE_Login --json` — Output as JSON for tooling

**Output includes:**
- Converted file locations with line numbers
- Control mappings (EDT_Usuario → input[name='usuario'])
- Procedure mappings (Global_ValidaCPF → validar_cpf())
- Data binding mappings
- Documented deviations from legacy behavior

## Workflow

### Standard Workflow

```
/wxcode:init           # First time only

/wxcode:status         # Check for updates
/wxcode:sync           # Apply updates when available

/wxcode:customize X    # Modify specific commands as needed
```

### Customization Workflow

```
/wxcode:discuss        # Explore what you want to change
/wxcode:customize X    # Apply specific customizations
/wxcode:override X     # Mark files to never sync
```

### Recovery Workflow

```
/wxcode:rollback       # Undo problematic sync
/wxcode:history        # Review what happened
/wxcode:status         # Check current state
```

## Configuration Files

```
.wxcode/
├── config.md           # Identity and settings
├── transform-rules.md  # WXCODE → WXCODE transformations
├── upstream-state.md   # Sync state tracking
├── customizations.md   # Decision history
├── overrides.md        # Files to skip during sync
└── decisions/          # Per-command decision records
    ├── plan-phase.md
    └── ...
```

## Transformation Rules

During sync, these transformations are applied automatically:

| WXCODE | WXCODE |
|-----|--------|
| `wxcode:` | `wxcode:` |
| `wxcode-` | `wxcode-` |
| `WXCODE` | `WXCODE` |
| `get-shit-done` | `wxcode` |
| `Get Shit Done` | `WXCODE` |

## Sync Decision Types

When syncing, you may be asked about:

| Type | Description | Options |
|------|-------------|---------|
| **New Feature** | Upstream added something | Import, Import & customize, Skip, Never |
| **Behavioral Change** | Upstream modified customized file | Accept upstream, Keep local, Merge |
| **Conflict** | Both sides changed | Various resolution strategies |

## Tips

- Run `/wxcode:status` regularly to stay aware of upstream changes
- Use `/wxcode:diff` before sync to preview changes
- Mark heavily customized files as overrides to avoid conflicts
- Record decisions in `/wxcode:discuss` before major changes
- Use `/wxcode:history` to understand past decisions
</reference>
