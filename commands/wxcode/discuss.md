---
name: wxcode:discuss
description: Explore and plan new features or behavioral changes through guided questioning
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - AskUserQuestion
---

<objective>

Exploratory command for discussing and planning:
- New features that don't exist in upstream
- Behavioral changes to existing commands
- New specialized agents
- Architecture modifications

This command conducts deep questioning to understand what you want, then designs a solution for your approval.

**After this command:** You'll have a clear design ready to implement with `/wxcode:customize`.

</objective>

<execution_context>

@~/.claude/agents/wxcode-sync-agent.md
@.wxcode/config.md
@.wxcode/customizations.md

</execution_context>

<process>

## Phase 1: Entry Point

**Display banner:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DISCUSS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Initial question:**

Use AskUserQuestion:
- header: "Topic"
- question: "What would you like to explore?"
- options:
  - "Create new command" — Add a command that doesn't exist in WXCODE
  - "Modify existing behavior" — Change how a command or agent works
  - "Create new agent" — Add a specialized agent
  - "Explore ideas" — Not sure yet, let's discuss

## Phase 2: Deep Questioning

### If "Create new command":

**2a.1 Understanding the need:**

Ask inline (freeform):
"What problem should this command solve? Describe the situation where you'd use it."

Wait for response.

**2a.2 Follow-up questions:**

Based on their response, ask targeted questions:

```
header: "Workflow"
question: "How would you typically use this command?"
options:
  - "Standalone" — Run independently, not part of a larger flow
  - "Before something" — Preparation step for another command
  - "After something" — Follow-up to another command
  - "Replace something" — Alternative to an existing command
```

```
header: "Frequency"
question: "How often would you use this command?"
options:
  - "Every session" — Part of daily workflow
  - "Per phase" — Once per phase/milestone
  - "Occasionally" — When specific situations arise
  - "Rarely" — Edge cases only
```

```
header: "Complexity"
question: "How complex is the work this command does?"
options:
  - "Simple" — Few steps, quick execution
  - "Medium" — Multiple steps, some decisions
  - "Complex" — Many steps, needs its own agent
```

**2a.3 Probe deeper:**

Ask about:
- What inputs does it need?
- What outputs should it produce?
- What files should it create/modify?
- Does it need user interaction (checkpoints)?
- Should it spawn agents?

### If "Modify existing behavior":

**2b.1 Identify target:**

```
header: "Target"
question: "What do you want to modify?"
options:
  - "A command" — /wxcode:something
  - "An agent" — wxcode-something
  - "A workflow" — How commands work together
  - "Output format" — What gets displayed or created
```

**2b.2 Understand current state:**

If command:
```bash
# List available commands
ls commands/wxcode/*.md | xargs -I {} basename {} .md
```

Ask which specific command.

Read the command file to understand current behavior.

**2b.3 Understand desired change:**

Ask inline:
"What should be different? Describe the behavior you want."

Wait for response.

**2b.4 Clarify the gap:**

```
header: "Change Type"
question: "What kind of change is this?"
options:
  - "Add feature" — Keep current behavior, add something new
  - "Change behavior" — Replace how something works
  - "Remove feature" — Stop doing something
  - "Restructure" — Same outcome, different approach
```

**2b.5 Impact assessment:**

Ask about:
- Does this affect other commands?
- Should this change sync with upstream?
- Is this WXCODE-specific or should it be proposed to WXCODE?

### If "Create new agent":

**2c.1 Understanding the role:**

Ask inline:
"What specialized task should this agent handle? What makes it different from existing agents?"

Wait for response.

**2c.2 Agent characteristics:**

```
header: "Spawning"
question: "Which commands would spawn this agent?"
options:
  - "New command" — Create a new command for it
  - "Existing command" — Add to an existing command
  - "Multiple commands" — Used by several commands
  - "Manual only" — Spawned directly by user
```

```
header: "Autonomy"
question: "How autonomous should this agent be?"
options:
  - "Fully autonomous" — Does everything without asking
  - "Checkpoints" — Stops for verification at key points
  - "Interactive" — Frequent user interaction
```

**2c.3 Probe deeper:**

Ask about:
- What tools does it need?
- What context does it require?
- What does it produce?
- How does it handle errors?

### If "Explore ideas":

**2d.1 Open exploration:**

Ask inline:
"Tell me what you're thinking about. What's on your mind regarding WXCODE?"

Wait for response.

**2d.2 Guided discovery:**

Based on their response, identify themes and ask clarifying questions.

Continue until a concrete direction emerges, then route to appropriate branch above.

## Phase 3: Design Synthesis

**3.1 Summarize understanding:**

Present what you understood:

```
## Understanding

Based on our discussion:

**What you want:** [summary]
**Problem it solves:** [problem]
**How it works:** [workflow]
**Key features:**
- [feature 1]
- [feature 2]
```

**3.2 Present design:**

```
## Proposed Design

### [Name]

**Type:** [command | agent | modification]

**Purpose:** [one-liner]

**Workflow:**
1. [step 1]
2. [step 2]
3. [step 3]

**Files involved:**
- `commands/wxcode/[name].md` — Command specification
- `agents/wxcode-[name].md` — Agent (if needed)

**Integration:**
- Relates to: [other commands]
- Spawns: [agents]
- Creates: [files]

**Example usage:**
```
/wxcode:[name] [args]
```
```

**3.3 Confirm design:**

Use AskUserQuestion:
- header: "Design"
- question: "Does this design capture what you want?"
- options:
  - "Yes, implement it" — Proceed to create the files
  - "Adjust something" — Let me clarify
  - "Start over" — This isn't what I meant
  - "Save for later" — Record design, implement later

## Phase 4: Implementation Decision

**If "Yes, implement it":**

```
Ready to implement.

Options:
1. Implement now — I'll create the files
2. Use /wxcode:customize — Step-by-step implementation
```

If implement now:
- Create command file (if new command)
- Create agent file (if needed)
- Update any related files
- Record in customizations.md
- Create decision file in .wxcode/decisions/

**If "Adjust something":**

Ask what needs adjustment, refine design, return to 3.3.

**If "Start over":**

Return to Phase 1.

**If "Save for later":**

Record design in `.wxcode/decisions/[name].md` as a draft.

```
Design saved to .wxcode/decisions/[name].md

Implement later with:
  /wxcode:customize [name]
```

## Phase 5: Record & Close

**5.1 Update customizations.md:**

```markdown
### [Date] - Discussion: [Name]

- **Type:** [command | agent | modification]
- **Status:** [implemented | saved for later]
- **Description:** [brief]
- **Decision file:** .wxcode/decisions/[name].md
```

**5.2 Display completion:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DISCUSSION COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Topic:** [Name]
**Outcome:** [Implemented | Saved for later | Design recorded]

[If implemented:]
Files created:
- commands/wxcode/[name].md
- agents/wxcode-[name].md (if applicable)

Test with: /wxcode:[name]

[If saved:]
Design saved to: .wxcode/decisions/[name].md
Implement with: /wxcode:customize [name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</process>

<success_criteria>

- [ ] User intent captured through questioning
- [ ] Design synthesized from discussion
- [ ] User approved or adjusted design
- [ ] Implementation completed OR design saved
- [ ] Decision recorded in .wxcode/
- [ ] User knows next steps

</success_criteria>
