---
name: wxcode:customize
description: Customize a specific WXCODE command or agent with targeted questioning
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - AskUserQuestion
---

<objective>

Directly customize a specific command or agent.

Unlike `/wxcode:discuss` (exploratory), this command goes straight to modifying a known target.

**Usage:** `/wxcode:customize <name>`

Examples:
- `/wxcode:customize plan-phase` — Customize the plan-phase command
- `/wxcode:customize executor` — Customize the wxcode-executor agent

</objective>

<execution_context>

@~/.claude/agents/wxcode-sync-agent.md
@.wxcode/config.md
@.wxcode/customizations.md

</execution_context>

<process>

## Phase 1: Identify Target

**1.1 Parse argument:**

Extract `<name>` from command invocation.

If no argument provided:

```bash
# List available commands
echo "=== Commands ==="
ls commands/wxcode/*.md 2>/dev/null | xargs -I {} basename {} .md

echo "=== Agents ==="
ls agents/wxcode-*.md 2>/dev/null | sed 's/.*wxcode-//' | sed 's/.md//'
```

Use AskUserQuestion:
- header: "Target"
- question: "What do you want to customize?"
- options: [dynamically generated from list above]

**1.2 Resolve target file:**

```bash
# Check if it's a command
if [ -f "commands/wxcode/${NAME}.md" ]; then
  TARGET_FILE="commands/wxcode/${NAME}.md"
  TARGET_TYPE="command"
# Check if it's an agent
elif [ -f "agents/wxcode-${NAME}.md" ]; then
  TARGET_FILE="agents/wxcode-${NAME}.md"
  TARGET_TYPE="agent"
# Check with wxcode- prefix
elif [ -f "agents/wxcode-${NAME#wxcode-}.md" ]; then
  TARGET_FILE="agents/wxcode-${NAME#wxcode-}.md"
  TARGET_TYPE="agent"
else
  echo "NOT_FOUND"
fi
```

If not found:

```
Target not found: [NAME]

Did you mean:
- [similar matches]

Or use /wxcode:discuss to create something new.
```

Exit.

## Phase 2: Load Context

**2.1 Read target file:**

```bash
cat "$TARGET_FILE"
```

**2.2 Check for existing customizations:**

```bash
DECISION_FILE=".wxcode/decisions/${NAME}.md"
if [ -f "$DECISION_FILE" ]; then
  cat "$DECISION_FILE"
fi
```

**2.3 Check customization history:**

```bash
grep -A5 "$NAME" .wxcode/customizations.md
```

**2.4 Display context:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► CUSTOMIZE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Target:** [TARGET_TYPE] /wxcode:[NAME]
**File:** [TARGET_FILE]

[If previously customized:]
**Previous customizations:**
- [date]: [change description]

## Current Behavior

[Brief summary of what the command/agent currently does]
```

## Phase 3: Customization Questioning

**3.1 What to change:**

Use AskUserQuestion:
- header: "Change"
- question: "What would you like to customize?"
- options:
  - "Add feature" — Add new capability
  - "Modify behavior" — Change how something works
  - "Remove feature" — Stop doing something
  - "Change output" — Modify what gets created/displayed
  - "Adjust flow" — Change the order or structure

**3.2 Based on selection, conduct focused questioning:**

### If "Add feature":

Ask inline:
"What feature do you want to add? Describe what it should do."

Wait for response.

Follow up:
```
header: "Integration"
question: "Where should this feature fit in the workflow?"
options:
  - "New phase" — Add as a new phase/step
  - "Extend existing" — Add to an existing phase
  - "Optional flag" — Enabled via argument
  - "Always active" — Part of default behavior
```

### If "Modify behavior":

Ask inline:
"What behavior do you want to change? Describe current vs desired."

Wait for response.

Follow up:
```
header: "Scope"
question: "How significant is this change?"
options:
  - "Minor tweak" — Small adjustment
  - "Significant change" — Notable difference
  - "Complete overhaul" — Rewrite the logic
```

### If "Remove feature":

```
header: "Remove"
question: "What do you want to remove?"
options: [dynamically list features/phases from target]
```

Ask:
"Why remove this? (Helps ensure we don't break dependencies)"

### If "Change output":

```
header: "Output"
question: "What output do you want to change?"
options:
  - "Console display" — What's shown to user
  - "Files created" — What files get generated
  - "Return value" — What's passed to other commands
  - "Logging" — Debug/status information
```

### If "Adjust flow":

Ask inline:
"Describe the flow change you want. What should happen in what order?"

## Phase 4: Design Change

**4.1 Analyze impact:**

Based on questioning, identify:
- Which sections of the file need changes
- Dependencies that might be affected
- Other files that might need updates

**4.2 Present change plan:**

```
## Proposed Changes

**Target:** [TARGET_FILE]

### Changes

1. **[Section]:** [What changes]
   - Before: [current behavior]
   - After: [new behavior]

2. **[Section]:** [What changes]
   ...

### Impact

- Affects: [other commands/agents if any]
- Dependencies: [none | list]
- Risk: [low | medium | high]

### Preview

[Show the specific code/text that will change]
```

**4.3 Confirm changes:**

Use AskUserQuestion:
- header: "Confirm"
- question: "Apply these changes?"
- options:
  - "Apply" — Make the changes
  - "Modify" — Adjust the plan
  - "Preview more" — Show more context
  - "Cancel" — Don't make changes

## Phase 5: Apply Changes

**5.1 Make edits:**

Use the Edit tool to modify the target file.

For each change:
1. Locate the section
2. Apply the edit
3. Verify the edit was applied correctly

**5.2 Update related files (if needed):**

If the change affects other files, update them too.

**5.3 Create/update decision file:**

Write to `.wxcode/decisions/${NAME}.md`:

```markdown
# Customization: [NAME]

## Overview

- **Type:** [command | agent]
- **File:** [TARGET_FILE]
- **Last Updated:** [date]

## Customization History

### [Date] - [Brief description]

**Change:** [What was changed]
**Reason:** [Why it was changed]
**Impact:** [What's affected]

**Before:**
```
[relevant code/text before]
```

**After:**
```
[relevant code/text after]
```

---

[Previous customizations if any]
```

**5.4 Update customizations.md:**

Add entry to the log:

```markdown
### [Date] - Customize: /wxcode:[NAME]

- **Type:** [add feature | modify | remove | change output | adjust flow]
- **Change:** [brief description]
- **Decision file:** .wxcode/decisions/[NAME].md
```

## Phase 6: Verify & Close

**6.1 Verification:**

```
## Verification

The following was changed:

| File | Change |
|------|--------|
| [TARGET_FILE] | [description] |
| [other files] | [description] |

Test the customization:
  /wxcode:[NAME] [test scenario]
```

**6.2 Display completion:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► CUSTOMIZATION COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Target:** /wxcode:[NAME]
**Change:** [brief description]

## Files Modified

- [TARGET_FILE]
- .wxcode/decisions/[NAME].md
- .wxcode/customizations.md

## Testing

Test with: /wxcode:[NAME] [suggested args]

## Note on Upstream Sync

This file is now marked as customized. Future `/wxcode:sync` operations will:
- Notify you of upstream changes to this file
- Ask how to handle conflicts
- Never auto-overwrite your customizations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</process>

<success_criteria>

- [ ] Target identified and loaded
- [ ] User intent captured through questioning
- [ ] Change plan created and approved
- [ ] Edits applied to target file
- [ ] Decision file created/updated
- [ ] customizations.md updated
- [ ] User knows how to test

</success_criteria>
