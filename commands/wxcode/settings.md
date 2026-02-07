---
name: wxcode:settings
description: Configure WXCODE workflow toggles and model profile
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"settings","args":"$ARGUMENTS","title":"WXCODE ▶ SETTINGS"} -->
## WXCODE ▶ SETTINGS
```

**At command end (success):**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Settings updated"} -->
```

**At command end (no project):**
```
<!-- WXCODE:STATUS:{"status":"failed","message":"No project found"} -->
<!-- WXCODE:ERROR:{"code":"NO_PROJECT","message":"No WXCODE project found","recoverable":true,"suggestion":"Run /wxcode:new-project first"} -->
```
</structured_output>

<objective>
Allow users to toggle workflow agents on/off and select model profile via interactive settings.

Updates `.planning/config.json` with workflow preferences and model profile selection.
</objective>

<process>

## 0. Check for Quick Command

If argument is `language <code>` (e.g., `language pt-BR`):

**Supported codes:** `en`, `pt-BR`, `es`

1. Read current config
2. Update `output_language` field only
3. Display confirmation and exit

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► LANGUAGE UPDATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Output language set to: {language name}

All future command outputs will be in {language name}.
```

**If invalid language code:** Show error with valid options.

**If no arguments or other arguments:** Continue to full settings flow below.

---

## 1. Validate Environment

```bash
ls .planning/config.json 2>/dev/null
```

**If not found:** Error - run `/wxcode:new-project` first.

## 2. Read Current Config

```bash
cat .planning/config.json
```

Parse current values (default to `true` if not present):
- `workflow.research` — spawn researcher during plan-phase
- `workflow.plan_check` — spawn plan checker during plan-phase
- `workflow.verifier` — spawn verifier during execute-phase
- `model_profile` — which model each agent uses (default: `balanced`)
- `output_language` — language for human-readable output (default: `"en"`)
- `git.branching_strategy` — branching approach (default: `"none"`)
- `worktree` — enable git worktree per milestone for multi-dev (default: `false`)

## 3. Present Settings

Use AskUserQuestion with current values shown:

```
AskUserQuestion([
  {
    question: "Which model profile for agents?",
    header: "Model",
    multiSelect: false,
    options: [
      { label: "Quality", description: "Opus everywhere except verification (highest cost)" },
      { label: "Balanced (Recommended)", description: "Opus for planning, Sonnet for execution/verification" },
      { label: "Budget", description: "Sonnet for writing, Haiku for research/verification (lowest cost)" }
    ]
  },
  {
    question: "Which language for WXCODE outputs?",
    header: "Language",
    multiSelect: false,
    options: [
      { label: "Português (pt-BR)", description: "Mensagens e status em português brasileiro" },
      { label: "English (en)", description: "Messages and status in English" },
      { label: "Español (es)", description: "Mensajes y estados en español" }
    ]
  },
  {
    question: "Spawn Plan Researcher? (researches domain before planning)",
    header: "Research",
    multiSelect: false,
    options: [
      { label: "Yes", description: "Research phase goals before planning" },
      { label: "No", description: "Skip research, plan directly" }
    ]
  },
  {
    question: "Spawn Plan Checker? (verifies plans before execution)",
    header: "Plan Check",
    multiSelect: false,
    options: [
      { label: "Yes", description: "Verify plans meet phase goals" },
      { label: "No", description: "Skip plan verification" }
    ]
  },
  {
    question: "Spawn Execution Verifier? (verifies phase completion)",
    header: "Verifier",
    multiSelect: false,
    options: [
      { label: "Yes", description: "Verify must-haves after execution" },
      { label: "No", description: "Skip post-execution verification" }
    ]
  },
  {
    question: "Git branching strategy?",
    header: "Branching",
    multiSelect: false,
    options: [
      { label: "None (Recommended)", description: "Commit directly to current branch" },
      { label: "Per Phase", description: "Create branch for each phase (gsd/phase-{N}-{name})" },
      { label: "Per Milestone", description: "Create branch for entire milestone (gsd/{version}-{name})" }
    ]
  },
  {
    question: "Enable git worktree per milestone? (for parallel multi-dev)",
    header: "Worktree",
    multiSelect: false,
    options: [
      { label: "No (Recommended)", description: "Single working directory, one milestone at a time" },
      { label: "Yes", description: "Each milestone gets branch + worktree for parallel development" }
    ]
  }
])
```

**Pre-select based on current config values.**

## 4. Update Config

Merge new settings into existing config.json:

**Language mapping:**
- "Português (pt-BR)" → `"pt-BR"`
- "English (en)" → `"en"`
- "Español (es)" → `"es"`

```json
{
  ...existing_config,
  "model_profile": "quality" | "balanced" | "budget",
  "output_language": "en" | "pt-BR" | "es",
  "workflow": {
    "research": true/false,
    "plan_check": true/false,
    "verifier": true/false
  },
  "git": {
    "branching_strategy": "none" | "phase" | "milestone"
  },
  "worktree": true/false
}
```

Write updated config to `.planning/config.json`.

## 5. Confirm Changes

Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► SETTINGS UPDATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Setting              | Value |
|----------------------|-------|
| Model Profile        | {quality/balanced/budget} |
| Output Language      | {en/pt-BR/es} |
| Plan Researcher      | {On/Off} |
| Plan Checker         | {On/Off} |
| Execution Verifier   | {On/Off} |
| Git Branching        | {None/Per Phase/Per Milestone} |

These settings apply to future /wxcode:plan-phase and /wxcode:execute-phase runs.

Quick commands:
- /wxcode:set-profile <profile> — switch model profile
- /wxcode:settings language pt-BR — change output language
- /wxcode:plan-phase --research — force research
- /wxcode:plan-phase --skip-research — skip research
- /wxcode:plan-phase --skip-verify — skip plan check

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Settings updated"} -->
```

</process>

<success_criteria>
- [ ] Current config read
- [ ] User presented with 7 settings (profile + language + 3 workflow toggles + git branching + worktree)
- [ ] Config updated with model_profile, output_language, workflow, git, and worktree sections
- [ ] Changes confirmed to user
</success_criteria>
