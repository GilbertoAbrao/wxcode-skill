# CLAUDE.md - WXCODE Development Context

This file contains everything needed to work on the WXCODE project effectively.

## Project Overview

**WXCODE** is a customized fork of [GSD (Get Shit Done)](https://github.com/glittercowboy/get-shit-done) specialized for **WinDev/WebDev code conversion projects**.

- **Repository:** GilbertoAbrao/get-shit-done
- **Branch:** `main-wxcode` (always work here)
- **Based on:** GSD v1.9.13
- **Installs to:** `~/.claude/` (commands, agents, hooks)

---

## Extension Architecture

WXCODE uses an **Extension Pattern** — it extends existing GSD commands rather than creating new ones.

### How Extensions Work

1. **Inject conditional logic** into existing commands
2. **Detect mode** via arguments or context files
3. **Branch to specialized flow** when conditions met
4. **Return to standard flow** for common operations

### Example: `/wxcode:new-project` Extension

```
Standard Flow (Greenfield):
  Phase 1 → Phase 2 → Phase 3 → ...

Extended Flow (Conversion Mode):
  Phase 1 → Phase 1.5 (detect CONTEXT.md) → Phase C1 → C2 → C3 → ...
                ↓
         If no CONTEXT.md, continue standard flow
```

### Injection Points

When extending a command:

1. **Add detection phase** early in the flow
2. **Branch to specialized phases** (prefix with C for conversion)
3. **Rejoin standard flow** where appropriate
4. **Update success_criteria** to include new checks

### Key Principle

> **CONTEXT.md is a snapshot. MCP is the Source of Truth.**
> Always consult MCP for current data, use CONTEXT.md for initial context only.

---

## Version Management (CRITICAL)

### When to Bump Version

**ALWAYS bump version when making ANY change that will be released.**

Files to update (ALL of them):
1. `package.json` → `"version": "X.Y.Z"`
2. `VERSION` → `X.Y.Z`
3. `CHANGELOG-WXCODE.md` → Add new version section
4. `README-WXCODE.md` → Update "Current Version"

### Version Format

```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, small improvements
  │     └──────── New features, non-breaking changes
  └────────────── Breaking changes (rarely used)
```

### Changelog Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Modification description
```

Also update the **Upstream Sync History** table at the bottom.

### Commit and Push Workflow

```bash
# 1. Make changes
# 2. Update version in ALL files
# 3. Commit
git add -A && git commit -m "feat/fix/chore: description"

# 4. Push
git push origin main-wxcode
```

---

## Installation & Update Flow

### How Installation Works

1. User runs: `npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global`
2. npm downloads package from GitHub
3. `bin/install.js` runs
4. Copies files to `~/.claude/`:
   - `commands/wxcode/` ← from `commands/wxcode/`
   - `get-shit-done/` ← reference docs
   - `agents/wxcode-*.md` ← agents
   - `hooks/` ← bundled hooks

### Cache Issues

npm/npx caches GitHub packages aggressively. To force fresh download:

```bash
npm cache clean --force && rm -rf ~/.npm/_npx && npx github:...
```

The `/wxcode:update` command includes cache-busting for VERSION check:
```bash
curl -s "...VERSION?t=$(date +%s)"  # timestamp prevents cache
```

---

## File Structure

```
get-shit-done/
├── commands/
│   └── wxcode/                 # ALL commands here (not gsd/)
│       ├── new-project.md      # Extended with Conversion Mode
│       ├── plan-phase.md
│       ├── execute-phase.md
│       ├── update.md           # Handles version checking
│       └── ...
│
├── agents/
│   ├── wxcode-*.md             # Standard agents (renamed from gsd-)
│   ├── wxcode-legacy-analyzer.md    # NEW: Conversion extension
│   └── wxcode-conversion-advisor.md # NEW: Conversion extension
│
├── .wxcode/
│   ├── config.md               # Fork identity
│   ├── transform-rules.md      # GSD → WXCODE transformations
│   └── conversion/             # Conversion-specific docs
│       ├── context-md-spec.md  # CONTEXT.md format spec
│       ├── mcp-usage.md        # 25 MCP tools guide
│       └── ...
│
├── bin/
│   └── install.js              # Installer script
│
├── package.json                # Version here!
├── VERSION                     # Version here too!
├── CHANGELOG-WXCODE.md         # And here!
├── README-WXCODE.md            # And here!
└── CLAUDE.md                   # This file
```

---

## MCP Integration

WXCODE uses **25 MCP tools** to access legacy WinDev/WebDev code.

### Tool Categories

| Category | Tools |
|----------|-------|
| Elements | `get_element`, `list_elements`, `search_code` |
| Controls | `get_controls`, `get_data_bindings` |
| Procedures | `get_procedures`, `get_procedure` |
| Schema | `get_schema`, `get_table` |
| Graph | `get_dependencies`, `get_impact`, `get_path`, `find_hubs`, `find_dead_code`, `find_cycles` |
| Conversion | `get_conversion_candidates`, `get_topological_order`, `get_conversion_stats`, `mark_converted`, `mark_project_initialized` |
| Stack | `get_stack_conventions` |
| Planes | `get_element_planes` |
| WLanguage | `get_wlanguage_reference`, `list_wlanguage_functions`, `get_wlanguage_pattern` |
| Similarity | `search_converted_similar` |
| PDF | `get_element_pdf_slice` |

### MCP Tool Prefix

All MCP tools are prefixed with `mcp__wxcode_kb__` in Claude Code.

---

## Supported Target Stacks

15 stacks organized by rendering type:

### Server-Rendered
- `fastapi-jinja2`, `fastapi-htmx`
- `django-templates`
- `rails-erb`
- `laravel-blade`

### SPA (Backend + Frontend)
- `fastapi-react`, `fastapi-vue`
- `nestjs-react`, `nestjs-vue`
- `laravel-react`

### Fullstack (Single Node)
- `nextjs-app-router`, `nextjs-pages`
- `nuxt3`, `sveltekit`, `remix`

---

## Common Issues & Fixes

### 1. npm cache serving old version

```bash
npm cache clean --force && rm -rf ~/.npm/_npx
```

### 2. Multiple top-level packages (Python)

Add to `pyproject.toml`:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["app*", "config*"]
```

### 3. start-dev.sh fails

The `/wxcode:new-project` command verifies the server starts. Common fixes:
- Missing `__init__.py` in Python packages
- Missing dependencies in requirements.txt
- Port already in use

### 4. GitHub raw content cache

VERSION file cached for ~5 minutes. Use cache-busting:
```bash
curl -s "...VERSION?t=$(date +%s)"
```

---

## Testing Changes

### Local Testing

```bash
# Install from local clone
node bin/install.js --claude --global

# Verify
grep "your-change" ~/.claude/commands/wxcode/your-file.md
```

### After Push

```bash
# Clear cache and reinstall from GitHub
npm cache clean --force && rm -rf ~/.npm/_npx
npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global
```

---

## Conversion Mode Checklist

When extending commands for conversion mode:

- [ ] Add `mcp__wxcode_kb__*` to `allowed-tools` in frontmatter
- [ ] Add detection phase (check for CONTEXT.md or `.planning/CONVERSION.md`)
- [ ] Use MCP as Source of Truth (not just CONTEXT.md)
- [ ] Verify generated code works (test start-dev.sh)
- [ ] Update success_criteria
- [ ] Don't suggest "Next Up" (IDE handles navigation)

---

## Quick Reference

### Bump Version
```bash
# Edit: package.json, VERSION, CHANGELOG-WXCODE.md, README-WXCODE.md
git add -A && git commit -m "chore: bump version to X.Y.Z"
git push origin main-wxcode
```

### Force Update
```bash
npm cache clean --force && rm -rf ~/.npm/_npx
npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global
```

### Check Installed Version
```bash
cat ~/.claude/get-shit-done/VERSION
grep "Conversion Mode" ~/.claude/commands/wxcode/new-project.md
```
