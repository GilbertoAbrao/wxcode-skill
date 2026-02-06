---
name: wxcode:history
description: View sync history and customization decisions
allowed-tools:
  - Read
  - Bash
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"history","args":"$ARGUMENTS","title":"WXCODE ▶ HISTORY"} -->
## WXCODE ▶ HISTORY
```

**At command end:**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"History displayed"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"status","args":"","description":"Check current sync state","priority":"optional"} -->
```
</structured_output>

<objective>

Display the complete history of:
- Sync operations with upstream
- Customization decisions made
- Overrides added/removed
- Rollbacks performed

**This is a read-only command** — shows history but makes no changes.

</objective>

<process>

## Phase 1: Load History Data

**1.1 Read state files:**

```bash
cat .wxcode/upstream-state.md
cat .wxcode/customizations.md
cat .wxcode/overrides.md
```

**1.2 Get git history for sync commits:**

```bash
# Find sync commits
git log --oneline --grep="sync:" --grep="wxcode" --all-match -- . 2>/dev/null | head -20
```

## Phase 2: Display History

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► HISTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Current State

| Property | Value |
|----------|-------|
| Upstream Version | v[VERSION] |
| Last Sync | [DATE] |
| Total Syncs | [N] |
| Customizations | [N] |
| Overrides | [N] |

## Sync History

[From upstream-state.md sync history table]

| Date | Version | Changes | Commit |
|------|---------|---------|--------|
| [DATE] | v[X] → v[Y] | [N] files | [HASH] |
| [DATE] | v[W] → v[X] | [N] files | [HASH] |
| ... | ... | ... | ... |

## Customization Timeline

[From customizations.md, in reverse chronological order]

### [Most Recent Date]

**[Action]:** [Description]
- Target: [file/command]
- Details: [brief]

### [Previous Date]

**[Action]:** [Description]
- Target: [file/command]
- Details: [brief]

[... continue for all entries ...]

## Active Overrides

[From overrides.md]

| File | Reason | Since |
|------|--------|-------|
| [FILE] | [REASON] | [DATE] |
| ... | ... | ... |

## Decision Files

[List of files in .wxcode/decisions/]

| Command/Agent | Last Updated |
|---------------|--------------|
| [NAME] | [DATE] |
| ... | ... |

View details: `cat .wxcode/decisions/<name>.md`

## Rollbacks

[If any rollbacks recorded in upstream-state.md]

| Date | Reverted Version | Reason |
|------|------------------|--------|
| [DATE] | v[VERSION] | [REASON] |

## Statistics

| Metric | Value |
|--------|-------|
| First sync | [DATE] |
| Total syncs | [N] |
| Total customizations | [N] |
| Files customized | [N] |
| Files overridden | [N] |
| Rollbacks | [N] |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Commands

- /wxcode:status — Current state summary
- /wxcode:diff <file> — Compare specific file with upstream
- /wxcode:sync — Sync with upstream

```
<!-- WXCODE:STATUS:{"status":"completed","message":"History displayed"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"status","args":"","description":"Check current sync state","priority":"optional"} -->
```

</process>

<output>

Read-only history display. No files modified.

</output>

<success_criteria>

- [ ] Sync history loaded and displayed
- [ ] Customization timeline shown
- [ ] Override list displayed
- [ ] Decision files listed
- [ ] Statistics calculated
- [ ] Clear, chronological presentation

</success_criteria>
