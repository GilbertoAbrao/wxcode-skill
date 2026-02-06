---
name: wxcode:init
description: Initialize WXCODE fork - setup .wxcode/ configuration, configure upstream, apply initial transformation
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"init","args":"$ARGUMENTS","title":"WXCODE ▶ INITIALIZING WXCODE"} -->
## WXCODE ▶ INITIALIZING WXCODE
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"help","args":"","description":"See available commands","priority":"recommended"} -->
```
</structured_output>

<objective>

Initialize the WXCODE fork management system.

This command:
1. Creates `.wxcode/` directory structure (if not exists)
2. Configures the upstream Git remote
3. Records the current upstream state
4. Applies the initial WXCODE → WXCODE transformation (if not already done)

**Run this once** when setting up a new WXCODE fork.

</objective>

<process>

## Phase 1: Pre-flight Checks

**1.1 Check if already initialized:**

```bash
if [ -f .wxcode/upstream-state.md ]; then
  LAST_SYNC=$(grep "Last Sync" .wxcode/upstream-state.md | grep -v "—")
  if [ -n "$LAST_SYNC" ]; then
    echo "ALREADY_INITIALIZED"
  fi
fi
```

If already initialized, display status and offer options:

```
WXCODE is already initialized.

Last sync: [date]
Upstream version: [version]

Options:
- Run /wxcode:status to see current state
- Run /wxcode:sync to sync with upstream
```

Exit if already initialized (unless user wants to reinitialize).

**1.2 Check Git repository:**

```bash
git rev-parse --git-dir 2>/dev/null || echo "NOT_A_GIT_REPO"
```

If not a git repo, abort:

```
Error: Not a git repository.

WXCODE fork management requires git. Initialize a repository first:
  git init
```

## Phase 2: Directory Setup

**2.1 Create .wxcode/ structure:**

```bash
mkdir -p .wxcode/decisions
```

**2.2 Verify configuration files exist:**

Check for:
- `.wxcode/config.md`
- `.wxcode/transform-rules.md`
- `.wxcode/upstream-state.md`
- `.wxcode/customizations.md`
- `.wxcode/overrides.md`

If any are missing, create them with default content.

## Phase 3: Upstream Configuration

**3.1 Configure upstream remote:**

```bash
# Check if upstream exists
UPSTREAM_URL=$(git remote get-url upstream 2>/dev/null)

if [ -z "$UPSTREAM_URL" ]; then
  git remote add upstream https://github.com/glittercowboy/get-shit-done.git
  echo "Added upstream remote"
else
  echo "Upstream remote exists: $UPSTREAM_URL"
fi
```

**3.2 Fetch upstream:**

```bash
git fetch upstream main
```

**3.3 Record initial state:**

```bash
# Get upstream info
UPSTREAM_COMMIT=$(git rev-parse upstream/main)
UPSTREAM_VERSION=$(git show upstream/main:package.json 2>/dev/null | grep '"version"' | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
CURRENT_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
```

Update `.wxcode/upstream-state.md`:

```markdown
## Current State

| Property | Value |
|----------|-------|
| **Status** | Initialized |
| **Last Sync** | [CURRENT_DATE] |
| **Upstream Commit** | [UPSTREAM_COMMIT] |
| **Upstream Version** | [UPSTREAM_VERSION] |
| **Local Commit After Sync** | — |

## Sync History

| Date | Upstream Version | Upstream Commit | Changes | Local Commit |
|------|------------------|-----------------|---------|--------------|
| [CURRENT_DATE] | [UPSTREAM_VERSION] | [UPSTREAM_COMMIT] | Initial setup | — |
```

## Phase 4: Initial Transformation Check

**4.1 Check if transformation is needed:**

```bash
# Check for WXCODE artifacts that should be WXCODE
WXCODE_COMMANDS=$(ls commands/gsd/*.md 2>/dev/null | wc -l)
WXCODE_AGENTS=$(ls agents/wxcode-*.md 2>/dev/null | wc -l)
WXCODE_COMMANDS=$(ls commands/wxcode/*.md 2>/dev/null | wc -l)
```

**4.2 Offer initial transformation:**

If WXCODE artifacts exist but WXCODE doesn't:

Use AskUserQuestion:
- header: "Transform"
- question: "Apply initial WXCODE → WXCODE transformation now?"
- options:
  - "Yes, transform now (Recommended)" — Apply all transformations
  - "No, just initialize" — Setup complete, transform later with /wxcode:sync

**4.3 If transformation selected:**

Display progress:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► TRANSFORMING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Applying WXCODE → WXCODE transformation...
```

Execute transformation:

```bash
# 1. Rename directories
if [ -d commands/gsd ] && [ ! -d commands/wxcode ]; then
  mv commands/gsd commands/wxcode
fi

# 2. Rename agent files
for f in agents/wxcode-*.md; do
  [ -f "$f" ] && mv "$f" "${f/wxcode-/wxcode-}"
done

# 3. Rename hook files
for f in hooks/wxcode-*.js; do
  [ -f "$f" ] && mv "$f" "${f/wxcode-/wxcode-}"
done
for f in hooks/dist/wxcode-*.js; do
  [ -f "$f" ] && mv "$f" "${f/wxcode-/wxcode-}"
done

# 4. Apply text substitutions to all relevant files
find . -type f \( -name "*.md" -o -name "*.js" -o -name "*.json" \) \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  -not -path "./.wxcode/*" \
  -exec sed -i '' \
    -e 's/wxcode:/wxcode:/g' \
    -e 's/wxcode-/wxcode-/g' \
    -e 's/WXCODE/WXCODE/g' \
    -e 's/get-shit-done/wxcode/g' \
    -e 's/Get Shit Done/WXCODE/g' {} \;
```

## Phase 5: Finalization

**5.1 Record in customizations.md:**

```markdown
### Initial Setup

- **Date:** [CURRENT_DATE]
- **Action:** Fork initialized
- **Upstream Version:** [UPSTREAM_VERSION]
- **Transformation Applied:** [Yes/No]
```

**5.2 Git commit (optional):**

Use AskUserQuestion:
- header: "Commit"
- question: "Create git commit for initialization?"
- options:
  - "Yes, commit changes" — Create commit with all changes
  - "No, I'll commit later" — Leave changes staged

If yes:

```bash
git add -A
git commit -m "chore: initialize WXCODE fork

- Setup .wxcode/ configuration
- Configure upstream remote (WXCODE)
- Record initial upstream state: v[VERSION]
[- Apply WXCODE → WXCODE transformation]"
```

**5.3 Display completion:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► INITIALIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Upstream:** WXCODE v[VERSION]
**Commit:** [COMMIT_HASH]
**Transformed:** [Yes/No]

## Configuration

| File | Status |
|------|--------|
| .wxcode/config.md | ✓ |
| .wxcode/transform-rules.md | ✓ |
| .wxcode/upstream-state.md | ✓ |
| .wxcode/customizations.md | ✓ |
| .wxcode/overrides.md | ✓ |

## Next Steps

- `/wxcode:status` — Check current sync state
- `/wxcode:sync` — Sync with upstream when updates available
- `/wxcode:customize <command>` — Customize a specific command
- `/wxcode:discuss` — Plan new features or changes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</process>

<success_criteria>

- [ ] .wxcode/ directory exists with all config files
- [ ] Upstream remote configured
- [ ] Upstream fetched successfully
- [ ] upstream-state.md records current state
- [ ] Initial transformation applied (if selected)
- [ ] customizations.md records initialization
- [ ] User knows next steps

</success_criteria>
