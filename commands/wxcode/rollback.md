---
name: wxcode:rollback
description: Revert the last sync operation
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
---

<structured_output>
## Structured Output (MANDATORY)

**At command start:**
```
<!-- WXCODE:HEADER:{"command":"rollback","args":"$ARGUMENTS","title":"WXCODE ▶ ROLLBACK"} -->
```

**At command end (success):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Rollback complete"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"status","args":"","description":"Verify current state","priority":"recommended"} -->
```

**At command end (no sync found):**
```
<!-- WXCODE:STATUS:{"status":"failed","message":"No sync to rollback"} -->
<!-- WXCODE:ERROR:{"code":"NO_SYNC_FOUND","message":"No sync commit found to rollback","recoverable":false} -->
```

**At command end (cancelled):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Rollback cancelled"} -->
```
</structured_output>

<objective>

Revert the last `/wxcode:sync` operation.

This command:
1. Identifies the commit created by the last sync
2. Reverts all changes from that commit
3. Updates the sync state to previous version

**Use when:** A sync introduced problems and you need to undo it.

**Warning:** This uses git revert, which creates a new commit. It doesn't rewrite history.

</objective>

<process>

## Phase 1: Gather Information

**1.1 Check sync history:**

```bash
cat .wxcode/upstream-state.md
```

Parse:
- Current sync commit
- Previous sync commit (from history table)
- Version info

**1.2 Find the sync commit:**

```bash
# Get the local commit created by last sync
LAST_SYNC_COMMIT=$(grep "Local Commit After Sync" .wxcode/upstream-state.md | grep -o '[a-f0-9]\{7,\}' | head -1)

# Get commit message to confirm it's a sync
COMMIT_MSG=$(git log -1 --format="%s" $LAST_SYNC_COMMIT 2>/dev/null)
```

**1.3 Validate:**

If no sync commit found:

```
No sync commit found to rollback.

The sync state doesn't record a local commit.
This might mean:
- No sync has been performed yet
- The last sync wasn't committed

Use /wxcode:status to check current state.

<!-- WXCODE:STATUS:{"status":"failed","message":"No sync to rollback"} -->
<!-- WXCODE:ERROR:{"code":"NO_SYNC_FOUND","message":"No sync commit found to rollback","recoverable":false} -->
```

Exit.

If commit is not a sync commit:

```
Warning: The recorded commit doesn't appear to be a sync commit.

Commit: [LAST_SYNC_COMMIT]
Message: [COMMIT_MSG]

This might indicate the sync state is out of sync with git history.

Proceed anyway? (This will revert the recorded commit)
```

## Phase 2: Show Rollback Preview

**2.1 Display what will be reverted:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► ROLLBACK PREVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Commit to Revert

**Hash:** [LAST_SYNC_COMMIT]
**Message:** [COMMIT_MSG]
**Date:** [COMMIT_DATE]

## Changes That Will Be Undone

```bash
git diff --stat [LAST_SYNC_COMMIT]^..[LAST_SYNC_COMMIT]
```

| File | Changes |
|------|---------|
[list files and change summary]

## State After Rollback

| Property | Current | After Rollback |
|----------|---------|----------------|
| Upstream Version | v[CURRENT] | v[PREVIOUS] |
| Upstream Commit | [CURRENT] | [PREVIOUS] |
| Last Sync | [CURRENT_DATE] | [PREVIOUS_DATE] |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**2.2 Confirm rollback:**

Use AskUserQuestion:
- header: "Rollback"
- question: "Revert this sync? This will create a new revert commit."
- options:
  - "Yes, rollback" — Revert the sync commit
  - "Show details" — Display full diff first
  - "Cancel" — Don't rollback

**If "Show details":**

```bash
git show $LAST_SYNC_COMMIT
```

Then re-ask.

## Phase 3: Execute Rollback

**3.1 Perform git revert:**

```bash
git revert --no-edit $LAST_SYNC_COMMIT
```

**3.2 Get the revert commit hash:**

```bash
REVERT_COMMIT=$(git rev-parse HEAD)
```

## Phase 4: Update State

**4.1 Update upstream-state.md:**

Restore previous sync state from history, or mark as "rolled back":

```markdown
## Current State

| Property | Value |
|----------|-------|
| **Status** | Rolled back |
| **Last Sync** | [PREVIOUS_DATE] |
| **Upstream Commit** | [PREVIOUS_COMMIT] |
| **Upstream Version** | [PREVIOUS_VERSION] |
| **Local Commit After Sync** | [REVERT_COMMIT] |

## Rollback Record

| Date | Reverted Commit | Revert Commit | Reason |
|------|-----------------|---------------|--------|
| [NOW] | [LAST_SYNC_COMMIT] | [REVERT_COMMIT] | User requested rollback |
```

**4.2 Update customizations.md:**

```markdown
### [Date] - Rollback

- **Reverted:** Sync to v[VERSION]
- **Commit reverted:** [LAST_SYNC_COMMIT]
- **Revert commit:** [REVERT_COMMIT]
- **Current state:** Matching upstream v[PREVIOUS_VERSION]
```

## Phase 5: Complete

**5.1 Display result:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► ROLLBACK COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Reverted:** [LAST_SYNC_COMMIT]
**Revert commit:** [REVERT_COMMIT]

## Current State

| Property | Value |
|----------|-------|
| Upstream Version | v[PREVIOUS_VERSION] |
| Upstream Commit | [PREVIOUS_COMMIT] |
| Status | Rolled back |

## What Happened

A new commit was created that undoes the changes from the last sync.
Your git history is preserved (no force push needed).

## Next Steps

- `/wxcode:status` — Verify current state
- `/wxcode:sync` — Re-sync when ready (will show same updates)
- `/wxcode:history` — Review full sync history

## Note

The rolled-back changes still exist in upstream.
Running /wxcode:sync again will offer the same changes.

If you want to permanently skip certain changes:
- `/wxcode:override <file>` — Ignore specific files
- Choose "Skip" or "Never import" during sync

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"Rollback complete"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"status","args":"","description":"Verify current state","priority":"recommended"} -->
```

</process>

<success_criteria>

- [ ] Sync commit identified
- [ ] Preview shown to user
- [ ] User confirmed rollback
- [ ] Git revert executed successfully
- [ ] upstream-state.md updated
- [ ] customizations.md updated
- [ ] User informed of result and next steps

</success_criteria>
