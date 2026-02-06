---
name: wxcode:sync
description: Synchronize WXCODE fork with upstream WXCODE repository
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - AskUserQuestion
---

<objective>

Synchronize your WXCODE fork with the upstream WXCODE repository.

This command:
1. Fetches latest changes from upstream
2. Classifies each change (deterministic, new feature, behavioral, conflict)
3. Applies deterministic transformations automatically
4. Conducts questioning for changes requiring decisions
5. Resolves conflicts (trivial: auto, complex: ask)
6. Updates sync state and commits changes

**After this command:** Your fork is up-to-date with upstream improvements while preserving your customizations.

</objective>

<execution_context>

@~/.claude/agents/wxcode-sync-agent.md
@.wxcode/config.md
@.wxcode/transform-rules.md
@.wxcode/upstream-state.md
@.wxcode/overrides.md

</execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"sync","args":"$ARGUMENTS","title":"WXCODE ▶ SYNCING WITH UPSTREAM"} -->
## WXCODE ▶ SYNCING WITH UPSTREAM
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"status","args":"","description":"Check sync status","priority":"recommended"} -->
```
</structured_output>



<process>

## Phase 1: Pre-flight Checks

**1.1 Check initialization:**

```bash
if [ ! -f .wxcode/upstream-state.md ]; then
  echo "NOT_INITIALIZED"
fi
```

If not initialized:

```
WXCODE not initialized.

Run /wxcode:init first to setup fork management.
```

Exit.

**1.2 Check for uncommitted changes:**

```bash
git status --porcelain
```

If uncommitted changes exist:

Use AskUserQuestion:
- header: "Uncommitted Changes"
- question: "You have uncommitted changes. How to proceed?"
- options:
  - "Stash changes" — Stash, sync, then restore
  - "Commit first" — Abort sync, commit manually
  - "Continue anyway" — Sync with uncommitted changes (risky)

**1.3 Load configuration:**

Read all `.wxcode/` configuration files.

## Phase 2: Fetch & Analyze

**Display banner:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► SYNCING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fetching upstream...
```

**2.1 Fetch upstream:**

```bash
git fetch upstream main
```

**2.2 Get version info:**

```bash
# Last synced commit
LAST_SYNC=$(grep "Upstream Commit" .wxcode/upstream-state.md | grep -o '[a-f0-9]\{7,\}' | head -1)

# Current upstream
UPSTREAM_HEAD=$(git rev-parse upstream/main)
UPSTREAM_VERSION=$(git show upstream/main:package.json | grep '"version"' | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')

# Last synced version
LAST_VERSION=$(grep "Upstream Version" .wxcode/upstream-state.md | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)
```

**2.3 Check if sync needed:**

If `LAST_SYNC` == `UPSTREAM_HEAD`:

```
Already up to date.

Upstream: v[VERSION] ([COMMIT])
Local: Synced ✓

No changes to apply.
```

Exit.

**2.4 List changes:**

```bash
# Get changed files
git diff --name-status $LAST_SYNC upstream/main
```

Display summary:

```
Upstream changes detected:

v[LAST_VERSION] → v[UPSTREAM_VERSION]
[LAST_SYNC] → [UPSTREAM_HEAD]

Files changed: [N]
- Added: [N]
- Modified: [N]
- Deleted: [N]
```

## Phase 3: Classification

**Spawn wxcode-sync-agent for analysis:**

```
Task(prompt="
<task>
Analyze upstream changes and classify each file.
</task>

<upstream_diff>
[git diff output]
</upstream_diff>

<overrides>
[content of overrides.md]
</overrides>

<customizations>
[content of customizations.md - list of customized files]
</customizations>

<instructions>
For each changed file, classify as:
1. DETERMINISTIC — No local customization, apply transform
2. NEW_FEATURE — New command/agent, needs user decision
3. BEHAVIORAL — Modified file with local customization
4. CONFLICT — Both sides changed, needs resolution
5. OVERRIDE — In override list, skip
6. DELETION — Upstream deleted, check local equivalent

Return structured classification.
</instructions>
", subagent_type="wxcode-sync-agent", description="Classify changes")
```

## Phase 4: Process Changes

**4.1 Display classification:**

```
## Change Classification

| File | Type | Action |
|------|------|--------|
| commands/gsd/new-cmd.md | NEW_FEATURE | Ask |
| agents/wxcode-planner.md | DETERMINISTIC | Auto |
| commands/gsd/plan-phase.md | BEHAVIORAL | Ask |
| README.md | OVERRIDE | Skip |
```

**4.2 Process DETERMINISTIC changes:**

For each deterministic file:

1. Get content from upstream
2. Apply path transformation (gsd/ → wxcode/, gsd- → wxcode-)
3. Apply text transformations (from transform-rules.md)
4. **Verify folder paths preserved** (CRITICAL)
5. Write to local file

```bash
# Example for a command file
git show upstream/main:commands/gsd/help.md > /tmp/upstream-file.md

# Apply transformations - NOTE: DO NOT transform 'get-shit-done' folder paths!
sed -i '' \
  -e 's/gsd:/wxcode:/g' \
  -e 's/gsd-/wxcode-/g' \
  -e 's/GSD/WXCODE/g' \
  -e 's/Get Shit Done/WXCODE/g' \
  /tmp/upstream-file.md

# Write to correct location
mv /tmp/upstream-file.md commands/wxcode/help.md
```

**CRITICAL: For bin/install.js specifically:**

The `get-shit-done/` folder keeps its original name. After transforming `bin/install.js`:

```bash
# Verify these paths still reference 'get-shit-done', NOT 'wxcode':
grep -n "path.join.*'get-shit-done'" bin/install.js

# If incorrectly transformed, fix them:
# - skillSrc/skillDest should use 'get-shit-done'
# - changelogDest/versionDest should use 'get-shit-done'
# - gsdDir (uninstall) should use 'get-shit-done'
```

**Patterns that must NEVER be transformed:**

| Pattern | Reason |
|---------|--------|
| `path.join(..., 'get-shit-done')` | Folder path - folder keeps name |
| `targetDir, 'get-shit-done'` | Installation target |
| `~/.claude/get-shit-done/` | Installed folder reference |
| GitHub URLs to upstream | Credit/attribution |

**4.3 Process NEW_FEATURE changes:**

For each new command/agent, use AskUserQuestion:

```
header: "New Command"
question: "Upstream added /wxcode:new-command (does X). Import it?"
options:
  - "Import (Recommended)" — Transform and add as /wxcode:new-command
  - "Import & customize" — Transform, add, then customize
  - "Skip for now" — Don't import, remind me next sync
  - "Never import" — Add to permanent skip list
```

Based on answer:
- Import: Apply transformation, add file
- Import & customize: Apply transformation, add file, mark for customization
- Skip: Add to deferred list in upstream-state.md
- Never: Add to permanent skip in overrides.md

**4.4 Process BEHAVIORAL changes:**

For files with local customizations:

```
header: "Upstream Change"
question: "Upstream modified /wxcode:plan-phase. You have local customizations."
options:
  - "Accept upstream" — Replace with transformed upstream (lose customizations)
  - "Keep local" — Ignore upstream changes
  - "Show diff" — See what changed before deciding
  - "Merge" — Attempt to combine both
```

If "Show diff":
- Display side-by-side comparison
- Re-ask with context

If "Merge":
- Attempt intelligent merge
- If conflict, show and ask for resolution

**4.5 Process OVERRIDE files:**

Just notify:

```
Skipped (override): README.md
```

**4.6 Process DELETIONS:**

```
header: "File Deleted"
question: "Upstream deleted commands/gsd/old-command.md. Delete local equivalent?"
options:
  - "Delete" — Remove commands/wxcode/old-command.md
  - "Keep" — Preserve local file
```

## Phase 5: Apply & Commit

**5.1 Display summary before applying:**

```
## Changes to Apply

### Automatic (Deterministic)
- commands/wxcode/help.md — updated
- agents/wxcode-planner.md — updated

### User Decisions
- commands/wxcode/new-cmd.md — import
- commands/wxcode/plan-phase.md — keep local

### Skipped
- README.md — override

Proceed? (yes/no)
```

**5.2 Apply all changes:**

Execute all file operations.

**5.3 Update state files:**

Update `.wxcode/upstream-state.md`:

```markdown
## Current State

| Property | Value |
|----------|-------|
| **Status** | Synced |
| **Last Sync** | [CURRENT_DATE] |
| **Upstream Commit** | [UPSTREAM_HEAD] |
| **Upstream Version** | [UPSTREAM_VERSION] |
| **Local Commit After Sync** | [pending] |
```

Update `.wxcode/customizations.md` with decisions made.

**5.4 Git commit:**

```bash
git add -A
git commit -m "$(cat <<'EOF'
sync: upstream WXCODE v[OLD] → v[NEW]

Changes:
- Updated: [N] files
- Added: [N] files
- Deleted: [N] files

Decisions:
- /wxcode:new-cmd — imported
- /wxcode:plan-phase — kept local

Skipped:
- README.md (override)
EOF
)"
```

Update upstream-state.md with commit hash.

## Phase 6: Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► SYNC COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Upstream:** v[OLD] → v[NEW]
**Commit:** [OLD_HASH] → [NEW_HASH]

## Summary

| Metric | Count |
|--------|-------|
| Files updated | [N] |
| New features imported | [N] |
| Decisions made | [N] |
| Skipped (override) | [N] |

## What's New

[Brief description of notable changes from upstream]

## Next Steps

- Test affected commands
- `/wxcode:status` — Verify sync state
- `/wxcode:history` — Review all changes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</process>

<success_criteria>

- [ ] Upstream fetched successfully
- [ ] All changes classified
- [ ] Deterministic changes applied with transformations
- [ ] **CRITICAL: bin/install.js folder paths verified**
  - [ ] `'get-shit-done'` folder references NOT transformed to `'wxcode'`
  - [ ] skillSrc/skillDest use `'get-shit-done'`
  - [ ] changelogDest/versionDest use `'get-shit-done'`
- [ ] User decisions collected for non-deterministic changes
- [ ] State files updated
- [ ] Git commit created
- [ ] User informed of changes

</success_criteria>

<post_sync_verification>

## MANDATORY: Verify Installer After Sync

If `bin/install.js` was updated, run this verification:

```bash
# Check for incorrectly transformed folder paths
grep -n "path.join.*'wxcode'" bin/install.js
```

**If any results:** The sync incorrectly transformed folder paths. Fix them:

```bash
# These MUST use 'get-shit-done', NOT 'wxcode':
# - skillSrc = path.join(src, 'get-shit-done')
# - skillDest = path.join(targetDir, 'get-shit-done')
# - gsdDir = path.join(targetDir, 'get-shit-done')
# - changelogDest = path.join(targetDir, 'get-shit-done', 'CHANGELOG.md')
# - versionDest = path.join(targetDir, 'get-shit-done', 'VERSION')
```

**Why:** The `get-shit-done/` folder keeps its original name. It contains
references, templates, and workflows. Only command prefixes (`gsd:` → `wxcode:`)
and agent prefixes (`gsd-` → `wxcode-`) are transformed.

</post_sync_verification>
