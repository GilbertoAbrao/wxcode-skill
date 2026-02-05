---
name: wxcode:diff
description: Compare local WXCODE file with upstream WXCODE equivalent
allowed-tools:
  - Read
  - Bash
---

<structured_output>
## Structured Output (MANDATORY)

**At command start:**
```
<!-- WXCODE:HEADER:{"command":"diff","args":"$ARGUMENTS","title":"WXCODE ▶ DIFF"} -->
```

**At command end (no differences):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"No differences found"} -->
```

**At command end (differences exist):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"N differences found"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"sync","args":"","description":"Apply upstream changes","priority":"optional"} -->
```

**At command end (list mode):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"N files with differences"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"diff","args":"<file>","description":"View specific file diff","priority":"optional"} -->
```
</structured_output>

<objective>

Show the difference between your local WXCODE file and the upstream WXCODE version.

**Usage:**
- `/wxcode:diff <file>` — Compare specific file
- `/wxcode:diff <command>` — Compare command (e.g., `plan-phase`)
- `/wxcode:diff` — List files with differences

**This is a read-only command** — shows differences but makes no changes.

</objective>

<process>

## Phase 1: Parse Arguments

**1.1 If no arguments — list all differences:**

```bash
# Get last synced commit
LAST_SYNC=$(grep "Upstream Commit" .wxcode/upstream-state.md | grep -o '[a-f0-9]\{7,\}' | head -1)

# Fetch upstream for comparison
git fetch upstream main 2>/dev/null

# List all changed files
git diff --name-only $LAST_SYNC upstream/main
```

Display:

```
<!-- WXCODE:STATUS:{"status":"completed","message":"N files with differences"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"diff","args":"<file>","description":"View specific file diff","priority":"optional"} -->
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DIFF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files with differences from upstream:

## Commands
- [list of changed commands]

## Agents
- [list of changed agents]

## Other
- [list of other changed files]

To see specific differences:
  /wxcode:diff <file>
  /wxcode:diff plan-phase

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Exit.

**1.2 Resolve file path:**

If argument is a command name (no path):
- Check `commands/wxcode/<name>.md`

If argument is an agent name:
- Check `agents/wxcode-<name>.md`

If argument is a full path:
- Use as-is

```bash
# Resolve target
if [ -f "commands/wxcode/${ARG}.md" ]; then
  LOCAL_FILE="commands/wxcode/${ARG}.md"
  UPSTREAM_FILE="commands/gsd/${ARG}.md"
elif [ -f "agents/wxcode-${ARG}.md" ]; then
  LOCAL_FILE="agents/wxcode-${ARG}.md"
  UPSTREAM_FILE="agents/wxcode-${ARG}.md"
elif [ -f "$ARG" ]; then
  LOCAL_FILE="$ARG"
  # Map to upstream equivalent
  UPSTREAM_FILE=$(echo "$ARG" | sed 's/wxcode/gsd/g')
else
  echo "NOT_FOUND"
fi
```

If not found:

```
File not found: [ARG]

Specify a command name or full file path:
  /wxcode:diff plan-phase
  /wxcode:diff commands/wxcode/help.md
```

Exit.

## Phase 2: Get Upstream Content

**2.1 Fetch upstream file:**

```bash
# Get upstream content
UPSTREAM_CONTENT=$(git show upstream/main:$UPSTREAM_FILE 2>/dev/null)

if [ -z "$UPSTREAM_CONTENT" ]; then
  echo "NO_UPSTREAM"
fi
```

If no upstream file:

```
No upstream equivalent for: [LOCAL_FILE]

This file is local-only (doesn't exist in WXCODE).
```

Exit.

**2.2 Create transformed upstream for comparison:**

```bash
# Apply transformations to upstream content
TRANSFORMED=$(echo "$UPSTREAM_CONTENT" | sed \
  -e 's/wxcode:/wxcode:/g' \
  -e 's/wxcode-/wxcode-/g' \
  -e 's/WXCODE/WXCODE/g' \
  -e 's/get-shit-done/wxcode/g' \
  -e 's/Get Shit Done/WXCODE/g')
```

## Phase 3: Generate Diff

**3.1 Compare local vs transformed upstream:**

```bash
# Write transformed to temp file
echo "$TRANSFORMED" > /tmp/upstream-transformed.md

# Generate diff
diff -u /tmp/upstream-transformed.md "$LOCAL_FILE" > /tmp/diff-output.txt
DIFF_LINES=$(wc -l < /tmp/diff-output.txt)
```

## Phase 4: Display Diff

**4.1 If no differences:**

```
<!-- WXCODE:STATUS:{"status":"completed","message":"No differences found"} -->
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DIFF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**File:** [LOCAL_FILE]
**Upstream:** [UPSTREAM_FILE]

✓ No differences

Your file matches upstream (after transformation).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**4.2 If differences exist:**

```
<!-- WXCODE:STATUS:{"status":"completed","message":"N differences found"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"sync","args":"","description":"Apply upstream changes","priority":"optional"} -->
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DIFF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Local:** [LOCAL_FILE]
**Upstream:** [UPSTREAM_FILE] (transformed)

## Summary

- Lines added: [N]
- Lines removed: [N]
- Lines changed: [N]

## Differences

```diff
[diff output with syntax highlighting hints]
--- upstream (transformed)
+++ local

[actual diff content]
```

## Legend

- Lines starting with `-` exist in upstream but not locally
- Lines starting with `+` exist locally but not in upstream
- Lines starting with ` ` are unchanged context

## Actions

- `/wxcode:sync` — Apply upstream changes
- `/wxcode:customize [name]` — Modify local version
- `/wxcode:override [file]` — Permanently ignore upstream

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**4.3 Additional context for customized files:**

If the file is in customizations.md:

```
## Customization Context

This file has local customizations:

[list customization history from .wxcode/decisions/<name>.md]

The differences above may be intentional customizations.
```

</process>

<output>

Read-only diff display. No files modified.

</output>

<success_criteria>

- [ ] File path resolved correctly
- [ ] Upstream content fetched
- [ ] Transformation applied for fair comparison
- [ ] Diff generated and displayed
- [ ] Context provided (customization status)
- [ ] Next actions suggested

</success_criteria>
