---
name: wxcode:update
description: Update WXCODE to latest version with changelog display
---

<objective>
Check for WXCODE updates, install if available, and display what changed.

Provides a better update experience by showing version diff and changelog entries.

**Note:** WXCODE is installed from GitHub (GilbertoAbrao/get-shit-done#main-wxcode), not npm.
</objective>

<process>

<step name="get_installed_version">
Read installed version:

```bash
cat ~/.claude/get-shit-done/VERSION 2>/dev/null
```

**If VERSION file missing:**
```
## WXCODE Update

**Installed version:** Unknown

Your installation doesn't include version tracking.

Running fresh install...
```

Proceed to install step (treat as version 0.0.0 for comparison).
</step>

<step name="check_latest_version">
Check GitHub for latest version (with cache-busting):

```bash
curl -s "https://raw.githubusercontent.com/GilbertoAbrao/get-shit-done/main-wxcode/VERSION?t=$(date +%s)" 2>/dev/null
```

**If GitHub check fails:**
```
Couldn't check for updates (offline or GitHub unavailable).

To update manually: `npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global`
```

STOP here if GitHub unavailable.
</step>

<step name="compare_versions">
Compare installed vs latest:

**If installed == latest:**
```
## WXCODE Update

**Installed:** X.Y.Z
**Latest:** X.Y.Z

You're already on the latest version.
```

STOP here if already up to date.

**If installed > latest:**
```
## WXCODE Update

**Installed:** X.Y.Z
**Latest:** A.B.C

You're ahead of the latest release (development version?).
```

STOP here if ahead.
</step>

<step name="show_changes_and_confirm">
**If update available**, fetch and show what's new BEFORE updating:

1. Fetch changelog (same as fetch_changelog step)
2. Extract entries between installed and latest versions
3. Display preview and ask for confirmation:

```
## WXCODE Update Available

**Installed:** 1.5.10
**Latest:** 1.5.15

### What's New
────────────────────────────────────────────────────────────

## [1.5.15] - 2026-01-20

### Added
- Feature X

## [1.5.14] - 2026-01-18

### Fixed
- Bug fix Y

────────────────────────────────────────────────────────────

⚠️  **Note:** The installer performs a clean install of WXCODE folders:
- `~/.claude/commands/wxcode/` will be wiped and replaced
- `~/.claude/get-shit-done/` will be wiped and replaced
- `~/.claude/agents/wxcode-*` files will be replaced

Your custom files in other locations are preserved:
- Custom commands in `~/.claude/commands/your-stuff/` ✓
- Custom agents not prefixed with `wxcode-` ✓
- Custom hooks ✓
- Your CLAUDE.md files ✓

If you've modified any WXCODE files directly, back them up first.
```

Use AskUserQuestion:
- Question: "Proceed with update?"
- Options:
  - "Yes, update now"
  - "No, cancel"

**If user cancels:** STOP here.
</step>

<step name="run_update">
Clear npm cache to ensure fresh download, then run the update:

```bash
npm cache clean --force 2>/dev/null; rm -rf ~/.npm/_npx 2>/dev/null; npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global
```

Capture output. If install fails, show error and STOP.

Clear the update cache so statusline indicator disappears:

```bash
rm -f ~/.claude/cache/wxcode-update-check.json
```
</step>

<step name="display_result">
Format completion message (changelog was already shown in confirmation step):

```
╔═══════════════════════════════════════════════════════════╗
║  WXCODE Updated: v1.5.10 → v1.5.15                           ║
╚═══════════════════════════════════════════════════════════╝

⚠️  Restart Claude Code to pick up the new commands.

[View full changelog](https://github.com/GilbertoAbrao/get-shit-done/blob/main-wxcode/CHANGELOG-WXCODE.md)
```
</step>

</process>

<success_criteria>
- [ ] Installed version read correctly
- [ ] Latest version checked via npm
- [ ] Update skipped if already current
- [ ] Changelog fetched and displayed BEFORE update
- [ ] Clean install warning shown
- [ ] User confirmation obtained
- [ ] Update executed successfully
- [ ] Restart reminder shown
</success_criteria>
