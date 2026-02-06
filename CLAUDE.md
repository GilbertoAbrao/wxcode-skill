# CLAUDE.md - WXCODE Development Context

This file contains everything needed to work on the WXCODE project effectively.

## Project Overview

**WXCODE** is an AI-powered WinDev/WebDev conversion toolkit for Claude Code, OpenCode, and Gemini.

- **Repository:** GilbertoAbrao/get-shit-done
- **Branch:** `main` (always work here)
- **Installs to:** `~/.claude/commands/wxcode/` (all commands), `~/.claude/wxcode-skill/` (references)
- **Coexists with GSD:** installer does NOT touch GSD files (`get-shit-done/`, `commands/gsd/`)

---

## Architecture

WXCODE extends standard project workflows with specialized support for WinDev/WebDev code conversion.

### Core Principle

> **CONTEXT.md is a snapshot. MCP is the Source of Truth.**
> Always consult MCP for current data, use CONTEXT.md for initial context only.

### Conversion Mode

When `/wxcode:new-project` receives a CONTEXT.md argument, it switches to conversion mode:
1. Reads CONTEXT.md (snapshot) + consults MCP (Source of Truth)
2. Creates project foundation with all files
3. Generates database models
4. Creates `.planning/CONVERSION.md` (activates conversion mode for other commands)

---

## Version Management (CRITICAL)

### When to Bump Version

**ALWAYS bump version when making ANY change that will be released.**

Files to update (ALL 4 of them):
1. `package.json` → `"version": "X.Y.Z"`
2. `VERSION` → `X.Y.Z`
3. `CHANGELOG-WXCODE.md` → Add new version section
4. `README.md` → Update "Current Version" line

**Note:** Changelog is `CHANGELOG-WXCODE.md` (not `CHANGELOG.md` — that was deleted with the GSD upstream).

### Version Format

```
MAJOR.MINOR.PATCH
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

### Commit and Push Workflow

```bash
# 1. Make changes
# 2. Update version in ALL files
# 3. Commit
git add -A && git commit -m "feat/fix/chore: description"

# 4. Push
git push origin main
```

---

## Installation & Update Flow

### How Installation Works

1. User runs: `npx github:GilbertoAbrao/get-shit-done#main --claude --global`
2. npm downloads package from GitHub
3. `bin/install.js` runs
4. Copies files to `~/.claude/`:
   - `commands/wxcode/` <- all 39+ commands (global)
   - `wxcode-skill/` <- references, templates, workflows
   - `agents/wxcode-*.md` <- agents
   - `hooks/` <- bundled hooks
   - `wxcode-skill/CHANGELOG-WXCODE.md` <- changelog
   - `wxcode-skill/VERSION` <- version file

**Important:** The installer ONLY manages WXCODE files. It does NOT touch GSD files
(`~/.claude/get-shit-done/`, `~/.claude/commands/gsd/`). Both products coexist independently.

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
wxcode/
├── commands/
│   └── wxcode/                 # ALL commands here (39+)
│       ├── new-project.md
│       ├── plan-phase.md
│       ├── execute-phase.md
│       └── ...
│
├── agents/
│   ├── wxcode-*.md             # Standard agents
│   ├── wxcode-legacy-analyzer.md    # Conversion agent
│   └── wxcode-conversion-advisor.md # Conversion agent
│
├── .wxcode/
│   ├── config.md               # WXCODE identity
│   └── conversion/             # Conversion-specific docs
│       ├── context-md-spec.md  # CONTEXT.md format spec
│       ├── mcp-usage.md        # 25 MCP tools guide
│       └── ...
│
├── wxcode-skill/               # Reference documentation
│   ├── references/
│   ├── templates/
│   └── workflows/
│
├── bin/
│   └── install.js              # Installer script
│
├── package.json                # Version here!
├── VERSION                     # Version here too!
├── CHANGELOG-WXCODE.md         # And here!
├── README.md                   # And here!
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
ls ~/.claude/wxcode-skill/commands/wxcode/ | wc -l
```

### After Push

```bash
# Clear cache and reinstall from GitHub
npm cache clean --force && rm -rf ~/.npm/_npx
npx github:GilbertoAbrao/get-shit-done#main --claude --global
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
# Edit: package.json, VERSION, CHANGELOG-WXCODE.md, README.md
git add -A && git commit -m "feat/fix/chore: description"
git push origin main
```

### Force Update
```bash
npm cache clean --force && rm -rf ~/.npm/_npx
npx github:GilbertoAbrao/get-shit-done#main --claude --global
```

### Check Installed Version
```bash
cat ~/.claude/wxcode-skill/VERSION
```
