---
name: wxcode:status
description: Show current WXCODE sync state and available updates
allowed-tools:
  - Read
  - Bash
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"status","args":"$ARGUMENTS","title":"WXCODE ▶ STATUS"} -->
## WXCODE ▶ STATUS
```

**At command end (up-to-date):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Up to date with upstream"} -->
```

**At command end (updates available):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"N updates available"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"sync","args":"","description":"Apply upstream updates","priority":"recommended"} -->
```

**At command end (not initialized):**
```
<!-- WXCODE:STATUS:{"status":"failed","message":"WXCODE not initialized"} -->
<!-- WXCODE:ERROR:{"code":"NOT_INITIALIZED","message":"WXCODE fork not initialized","recoverable":true,"suggestion":"Run /wxcode:init"} -->
```

**At command end (fetch failed):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Offline - showing cached state"} -->
```
</structured_output>

<objective>

Display the current state of your WXCODE fork:
- Local vs upstream version comparison
- Pending changes from upstream
- Deferred decisions
- Override status

**This is a read-only command** — it shows information but makes no changes.

</objective>

<process>

## Phase 1: Check Initialization

```bash
if [ ! -f .wxcode/upstream-state.md ]; then
  echo "NOT_INITIALIZED"
fi
```

If not initialized:

```
WXCODE not initialized.

Run /wxcode:init to setup fork management.

<!-- WXCODE:STATUS:{"status":"failed","message":"WXCODE not initialized"} -->
<!-- WXCODE:ERROR:{"code":"NOT_INITIALIZED","message":"WXCODE fork not initialized","recoverable":true,"suggestion":"Run /wxcode:init"} -->
```

Exit.

## Phase 2: Load State

**2.1 Read configuration:**

```bash
cat .wxcode/upstream-state.md
cat .wxcode/customizations.md
cat .wxcode/overrides.md
```

**2.2 Fetch upstream (non-blocking):**

```bash
git fetch upstream main 2>/dev/null || echo "FETCH_FAILED"
```

**2.3 Get version info:**

```bash
# Local state
LAST_SYNC=$(grep "Last Sync" .wxcode/upstream-state.md | sed 's/.*| //' | tr -d ' ')
LAST_COMMIT=$(grep "Upstream Commit" .wxcode/upstream-state.md | grep -o '[a-f0-9]\{7,\}' | head -1)
LAST_VERSION=$(grep "Upstream Version" .wxcode/upstream-state.md | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)

# Upstream state
UPSTREAM_COMMIT=$(git rev-parse upstream/main 2>/dev/null)
UPSTREAM_VERSION=$(git show upstream/main:package.json 2>/dev/null | grep '"version"' | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')

# Comparison
if [ "$LAST_COMMIT" = "${UPSTREAM_COMMIT:0:7}" ]; then
  SYNC_STATUS="up-to-date"
else
  SYNC_STATUS="updates-available"
fi
```

## Phase 3: Count Changes

**If updates available:**

```bash
# Count changed files
CHANGES=$(git diff --name-only $LAST_COMMIT upstream/main 2>/dev/null | wc -l | tr -d ' ')

# Categorize
ADDED=$(git diff --name-status $LAST_COMMIT upstream/main 2>/dev/null | grep '^A' | wc -l | tr -d ' ')
MODIFIED=$(git diff --name-status $LAST_COMMIT upstream/main 2>/dev/null | grep '^M' | wc -l | tr -d ' ')
DELETED=$(git diff --name-status $LAST_COMMIT upstream/main 2>/dev/null | grep '^D' | wc -l | tr -d ' ')

# New commands
NEW_COMMANDS=$(git diff --name-status $LAST_COMMIT upstream/main 2>/dev/null | grep '^A.*commands/gsd/' | wc -l | tr -d ' ')
```

## Phase 4: Display Status

**If up-to-date:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Up to date with upstream

## Current State

| Property | Value |
|----------|-------|
| Local Version | v[LAST_VERSION] |
| Upstream Version | v[UPSTREAM_VERSION] |
| Last Sync | [LAST_SYNC] |
| Upstream Commit | [LAST_COMMIT] |

## Customizations

- Commands customized: [N]
- Agents customized: [N]
- Files overridden: [N]

## Commands

- /wxcode:sync — Already up to date
- /wxcode:customize <cmd> — Customize a command
- /wxcode:discuss — Plan new features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"Up to date with upstream"} -->
```

**If updates available:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Updates available from upstream

## Version Comparison

| | Local | Upstream |
|---|-------|----------|
| Version | v[LAST_VERSION] | v[UPSTREAM_VERSION] |
| Commit | [LAST_COMMIT] | [UPSTREAM_COMMIT] |

## Pending Changes

| Type | Count |
|------|-------|
| Added | [ADDED] |
| Modified | [MODIFIED] |
| Deleted | [DELETED] |
| **Total** | **[CHANGES]** |

[If NEW_COMMANDS > 0:]
**New commands available:** [NEW_COMMANDS]

## Last Sync

[LAST_SYNC]

## Customizations

| Type | Count |
|------|-------|
| Commands customized | [N] |
| Agents customized | [N] |
| Files overridden | [N] |

## Deferred Decisions

[List any deferred items from upstream-state.md]

## Next Steps

→ `/wxcode:sync` — Apply upstream updates
→ `/wxcode:diff` — Preview specific changes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"N updates available"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"sync","args":"","description":"Apply upstream updates","priority":"recommended"} -->
```

**If fetch failed:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠ Could not fetch upstream (offline?)

## Last Known State

| Property | Value |
|----------|-------|
| Local Version | v[LAST_VERSION] |
| Last Sync | [LAST_SYNC] |
| Upstream Commit | [LAST_COMMIT] |

## Customizations

- Commands customized: [N]
- Agents customized: [N]
- Files overridden: [N]

Retry when online: /wxcode:status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"Offline - showing cached state"} -->
```

</process>

<output>

Read-only status display. No files modified.

</output>

<success_criteria>

- [ ] Configuration loaded
- [ ] Upstream fetch attempted
- [ ] Version comparison displayed
- [ ] Pending changes counted (if any)
- [ ] Customization status shown
- [ ] Clear next steps provided

</success_criteria>
