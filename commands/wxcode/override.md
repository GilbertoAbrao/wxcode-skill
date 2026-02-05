---
name: wxcode:override
description: Mark a file to ignore upstream changes during sync
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

<structured_output>
## Structured Output (MANDATORY)

**At command start:**
```
<!-- WXCODE:HEADER:{"command":"override","args":"$ARGUMENTS","title":"WXCODE ▶ OVERRIDE"} -->
```

**At command end (help/usage):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Usage displayed"} -->
```

**At command end (list):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"N overrides active"} -->
```

**At command end (add success):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Override added"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"override","args":"--list","description":"View all overrides","priority":"optional"} -->
```

**At command end (remove success):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Override removed"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"diff","args":"<file>","description":"Preview upstream changes","priority":"optional"} -->
```
</structured_output>

<objective>

Manage override files — files that should be completely ignored during upstream sync.

**Usage:**
- `/wxcode:override <file>` — Add file to override list
- `/wxcode:override --remove <file>` — Remove file from override list
- `/wxcode:override --list` — Show all overridden files

**Use cases:**
- Custom README.md with your own documentation
- Completely rewritten commands
- Local-only configuration files

</objective>

<process>

## Phase 1: Parse Arguments

**1.1 Determine action:**

| Argument | Action |
|----------|--------|
| `<file>` | Add to overrides |
| `--remove <file>` | Remove from overrides |
| `--list` | Show all overrides |
| (none) | Show help |

**1.2 If no arguments:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► OVERRIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Manage files that ignore upstream changes.

## Usage

Add override:
  /wxcode:override README.md
  /wxcode:override commands/wxcode/help.md

Remove override:
  /wxcode:override --remove README.md

List overrides:
  /wxcode:override --list

## What Overrides Do

When a file is overridden:
- /wxcode:sync will SKIP this file completely
- Upstream changes are ignored
- You maintain the file manually

## When to Use

- Custom documentation (README, CHANGELOG)
- Completely rewritten commands
- Local-only features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"Usage displayed"} -->
```

Exit.

## Phase 2: Handle --list

**If --list:**

```bash
cat .wxcode/overrides.md
```

Display formatted:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► OVERRIDES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Active Overrides

| File | Reason | Added |
|------|--------|-------|
[content from overrides.md]

## Commands

- /wxcode:override <file> — Add override
- /wxcode:override --remove <file> — Remove override

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"N overrides active"} -->
```

Exit.

## Phase 3: Handle Add Override

**3.1 Validate file exists:**

```bash
if [ ! -f "$FILE" ]; then
  echo "FILE_NOT_FOUND"
fi
```

If not found:

```
File not found: [FILE]

Override files must exist. Create the file first, then override it.
```

Exit.

**3.2 Check if already overridden:**

```bash
grep -q "$FILE" .wxcode/overrides.md && echo "ALREADY_OVERRIDDEN"
```

If already overridden:

```
File already overridden: [FILE]

Use /wxcode:override --list to see all overrides.
```

Exit.

**3.3 Confirm override:**

Use AskUserQuestion:
- header: "Confirm"
- question: "Override [FILE]? This file will be ignored during sync."
- options:
  - "Yes, override" — Add to override list
  - "Cancel" — Don't add

**3.4 Ask for reason:**

Ask inline:
"Why are you overriding this file? (helps future you remember)"

Wait for response.

**3.5 Add to overrides.md:**

Read current overrides.md, add new entry to the table:

```markdown
| [FILE] | [REASON] | [DATE] |
```

**3.6 Update customizations.md:**

```markdown
### [Date] - Override Added

- **File:** [FILE]
- **Reason:** [REASON]
```

**3.7 Display confirmation:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► OVERRIDE ADDED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**File:** [FILE]
**Reason:** [REASON]

This file will now be skipped during /wxcode:sync.

To remove this override later:
  /wxcode:override --remove [FILE]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"Override added"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"override","args":"--list","description":"View all overrides","priority":"optional"} -->
```

## Phase 4: Handle --remove

**4.1 Check if file is overridden:**

```bash
grep -q "$FILE" .wxcode/overrides.md || echo "NOT_OVERRIDDEN"
```

If not overridden:

```
File not in override list: [FILE]

Use /wxcode:override --list to see all overrides.
```

Exit.

**4.2 Confirm removal:**

Use AskUserQuestion:
- header: "Confirm"
- question: "Remove override for [FILE]? Next sync will update this file from upstream."
- options:
  - "Yes, remove" — Remove from override list
  - "Cancel" — Keep override

**4.3 Remove from overrides.md:**

Edit the file to remove the row containing the file path.

**4.4 Update customizations.md:**

```markdown
### [Date] - Override Removed

- **File:** [FILE]
- **Note:** File will now sync with upstream
```

**4.5 Display confirmation:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► OVERRIDE REMOVED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**File:** [FILE]

This file will now be updated during /wxcode:sync.

The next sync will apply upstream changes to this file
(with WXCODE → WXCODE transformation).

To preview what would change:
  /wxcode:diff [FILE]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<!-- WXCODE:STATUS:{"status":"completed","message":"Override removed"} -->
<!-- WXCODE:NEXT_ACTION:{"command":"diff","args":"[FILE]","description":"Preview upstream changes","priority":"optional"} -->
```

</process>

<success_criteria>

- [ ] Action determined from arguments
- [ ] File existence validated (for add)
- [ ] Override status checked
- [ ] User confirmed action
- [ ] overrides.md updated
- [ ] customizations.md updated
- [ ] User informed of result

</success_criteria>
