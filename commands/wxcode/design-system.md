---
name: wxcode:design-system
description: Generate or regenerate design tokens from URL, screenshots, or questionnaire
argument-hint: [--url <url> | --screenshots | --questionnaire | --regenerate]
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
  - mcp__wxcode-kb__*
  - mcp__playwright__*
---

<objective>

Generate or regenerate design system tokens for the project.

**Usage:**
- `/wxcode:design-system` — Interactive mode (choose method)
- `/wxcode:design-system --url <url>` — Extract from URL directly
- `/wxcode:design-system --screenshots` — Analyze provided screenshots
- `/wxcode:design-system --questionnaire` — Manual questionnaire (12 questions)
- `/wxcode:design-system --regenerate` — Regenerate stack files from existing tokens.json

**Output Files:**
```
design/
├── tokens.json           # DTCG format (Source of Truth)
├── tailwind.config.ts    # If Tailwind stack
├── variables.css         # CSS custom properties
└── README.md             # Human-readable docs
```

**Use cases:**
- Initial design system setup (if skipped during new-project)
- Update design based on new references
- Regenerate stack-specific files after tokens.json edit
- Switch visual style mid-project

</objective>

<execution_context>
@~/.claude/get-shit-done/.wxcode/conversion/design-system-flow.md
@~/.claude/get-shit-done/.wxcode/conversion/dtcg-spec.md
@~/.claude/get-shit-done/templates/design-tokens.json
</execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start:**
```
<!-- WXCODE:HEADER:{"command":"design-system","args":"$ARGUMENTS","title":"WXCODE ▶ DESIGN SYSTEM"} -->
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"progress","args":"","description":"Continue with project","priority":"recommended"} -->
```
</structured_output>



<process>

## Step 0: Emit Header

**First, emit the structured header:**

```
<!-- WXCODE:HEADER:{"command":"design-system","args":"$ARGUMENTS","title":"WXCODE ▶ DESIGN SYSTEM"} -->
```

## Step 1: Parse Arguments

```bash
MODE=""
URL=""

if [[ "$ARGUMENTS" == *"--url"* ]]; then
  MODE="url"
  URL=$(echo "$ARGUMENTS" | sed 's/.*--url[[:space:]]*\([^[:space:]]*\).*/\1/')
elif [[ "$ARGUMENTS" == *"--screenshots"* ]]; then
  MODE="screenshots"
elif [[ "$ARGUMENTS" == *"--questionnaire"* ]]; then
  MODE="questionnaire"
elif [[ "$ARGUMENTS" == *"--regenerate"* ]]; then
  MODE="regenerate"
fi
```

## Step 2: Check Existing Design System

```bash
if [ -f design/tokens.json ]; then
  echo "Existing design system found"
  EXISTING=true
else
  EXISTING=false
fi
```

If `--regenerate` and no tokens.json exists, error:
```
<!-- WXCODE:ERROR:{"code":"NO_TOKENS_FILE","message":"No design/tokens.json found","recoverable":true} -->

ERROR: No design/tokens.json found.
Use /wxcode:design-system without --regenerate to create one.
```
**STOP.**

## Step 3: Method Selection (if no mode specified)

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Selecting design source method","progress":10} -->
```

If MODE is empty, present options:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DESIGN SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

How would you like to define your design system?
```

Use AskUserQuestion:

```yaml
questions:
  - header: "Source"
    question: "How should I capture your design preferences?"
    options:
      - label: "Reference URL (Recommended)"
        description: "Extract colors, fonts, spacing from a live website"
      - label: "Screenshots"
        description: "Analyze design mockups or reference images"
      - label: "Questionnaire"
        description: "Answer 12 questions about your preferences"
```

---

## Step 4a: URL Extraction

**If MODE=url:**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Extracting design from URL","progress":30} -->
```

1. **Get URL** (if not provided in arguments):

   Use AskUserQuestion with presets AND custom option:

   ```yaml
   questions:
     - header: "URL"
       question: "What URL should I analyze for design patterns?"
       options:
         - label: "Enter my own URL"
           description: "I have a specific website to use as reference"
         - label: "https://stripe.com"
           description: "Modern fintech design with clean UI"
         - label: "https://vercel.com"
           description: "Developer-focused with dark/light themes"
         - label: "https://linear.app"
           description: "Minimal, productivity-focused design"
   ```

   **IMPORTANT:** "Enter my own URL" must be the FIRST option.
   When user selects "Other" or "Enter my own URL", ask inline for the URL.

2. **Navigate and capture with MCP Playwright:**

   ```
   mcp__playwright__navigate: url=<provided-url>
   ```

   Wait for page to fully load (JS-rendered content included).

   ```
   mcp__playwright__screenshot: (capture full page)
   ```

3. **Analyze the screenshot:**

   Use the captured screenshot to extract design tokens:
   - Dominant colors from logo, buttons, backgrounds
   - Typography characteristics (font style, sizes)
   - Spacing patterns
   - Shadow and border styles

   **Extraction prompt for screenshot analysis:**
   ```
   Analyze this webpage screenshot and extract design tokens:

   COLORS:
   - Primary brand color (from logo, main buttons)
   - Secondary color (supporting elements)
   - Background colors (main, card, input)
   - Text colors (primary, secondary, muted)
   - Semantic colors if visible (success green, error red, warning yellow)

   TYPOGRAPHY:
   - Font family style (serif, sans-serif, modern, classic)
   - Apparent size scale (compact, normal, spacious)
   - Weight usage (light, regular, bold patterns)

   SPACING:
   - Density (compact, comfortable, spacious)
   - Apparent base unit (4px or 8px system)

   VISUAL STYLE:
   - Shadow intensity (none, subtle, pronounced)
   - Border radius style (sharp, soft, rounded, pill)
   - Overall aesthetic (minimal, corporate, playful, technical)

   Return structured analysis with confidence levels.
   ```

4. **Present extracted values** for confirmation

   Show the user what was detected and ask for confirmation/adjustments.
   (See design-system-flow.md for detailed preview format)

5. **Allow adjustments** before generating

   User can modify any extracted values before final generation.

---

## Step 4b: Screenshot Analysis

**If MODE=screenshots:**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Analyzing screenshots","progress":30} -->
```

1. **Request images:**
   ```
   Please provide the path(s) to your design mockups or screenshots.

   Tips for best results:
   • Include variety (home, form, list views)
   • Higher resolution = better color analysis
   • 1-5 images recommended
   ```

2. **Read each image** using Read tool

3. **Analyze visually:**
   - Dominant colors
   - Typography characteristics
   - Layout patterns
   - Shadow/border styles

4. **Ask confirmation questions** (colors are approximate):
   - "Which is the PRIMARY brand color?"
   - "Which font family should I use?"
   - "Spacing base: 4px or 8px?"
   - "Shadow style: subtle, pronounced, or flat?"
   - "Border radius: soft, rounded, or minimal?"

---

## Step 4c: Manual Questionnaire

**If MODE=questionnaire:**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Collecting design preferences","progress":30} -->
```

Run through 12 structured questions:

### Colors (Q1-Q2)
1. Primary brand color (hex or preset)
2. Secondary color + semantic colors (success, warning, error, info)

### Typography (Q3-Q4)
3. Main font family (Inter, Roboto, Open Sans, Poppins, etc.)
4. Code font (JetBrains Mono, Fira Code, etc.)

### Typography Scale (Q5-Q6)
5. Size scale (Tailwind, Material Design, or custom)
6. Font weights to include (400, 500, 600, 700)

### Spacing (Q7-Q8)
7. Base unit (4px or 8px)
8. Scale multipliers

### Shadows (Q9-Q10)
9. Shadow style (subtle, pronounced, flat)
10. Number of shadow levels (sm, md, lg, xl)

### Borders (Q11)
11. Border radius scale (soft, rounded, minimal, custom)

### Dark Mode (Q12)
12. Include dark mode? (auto-generate, manual later, none)

---

## Step 4d: Regenerate Stack Files

**If MODE=regenerate:**

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Regenerating stack files","progress":50} -->
```

1. Read existing `design/tokens.json`
2. Detect stack from `.planning/CONVERSION.md` or `package.json`
3. Regenerate stack-specific files only

---

## Step 5: Generate DTCG Tokens

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Generating DTCG tokens","progress":60} -->
```

Create `design/tokens.json` following DTCG spec:

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "$description": "[Project Name] Design System",

  "color": {
    "primary": {
      "$value": "#635bff",
      "$type": "color",
      "$description": "Main brand color"
    },
    "secondary": { ... },
    "success": { ... },
    "warning": { ... },
    "error": { ... },
    "info": { ... },
    "background": { ... },
    "foreground": { ... }
  },

  "typography": {
    "fontFamily": {
      "sans": { "$value": "Inter, system-ui, sans-serif", "$type": "fontFamily" },
      "mono": { "$value": "JetBrains Mono, monospace", "$type": "fontFamily" }
    },
    "fontSize": {
      "xs": { "$value": "0.75rem", "$type": "dimension" },
      "sm": { "$value": "0.875rem", "$type": "dimension" },
      "base": { "$value": "1rem", "$type": "dimension" },
      "lg": { "$value": "1.125rem", "$type": "dimension" },
      "xl": { "$value": "1.25rem", "$type": "dimension" },
      "2xl": { "$value": "1.5rem", "$type": "dimension" },
      "3xl": { "$value": "1.875rem", "$type": "dimension" },
      "4xl": { "$value": "2.25rem", "$type": "dimension" }
    },
    "fontWeight": { ... },
    "lineHeight": { ... }
  },

  "spacing": {
    "1": { "$value": "0.25rem", "$type": "dimension" },
    "2": { "$value": "0.5rem", "$type": "dimension" },
    "3": { "$value": "0.75rem", "$type": "dimension" },
    "4": { "$value": "1rem", "$type": "dimension" },
    ...
  },

  "shadow": {
    "sm": { "$value": "0 1px 2px rgba(0,0,0,0.05)", "$type": "shadow" },
    "md": { "$value": "0 4px 6px rgba(0,0,0,0.07)", "$type": "shadow" },
    "lg": { "$value": "0 10px 15px rgba(0,0,0,0.1)", "$type": "shadow" },
    "xl": { "$value": "0 20px 25px rgba(0,0,0,0.15)", "$type": "shadow" }
  },

  "borderRadius": {
    "sm": { "$value": "0.25rem", "$type": "dimension" },
    "md": { "$value": "0.5rem", "$type": "dimension" },
    "lg": { "$value": "0.75rem", "$type": "dimension" },
    "xl": { "$value": "1rem", "$type": "dimension" },
    "full": { "$value": "9999px", "$type": "dimension" }
  }
}
```

## Step 6: Generate Stack-Specific Files

```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"Generating stack-specific files","progress":80} -->
```

### Detect Stack

```bash
# From CONVERSION.md
STACK=$(grep -i "stack:" .planning/CONVERSION.md | head -1 | awk '{print $2}')

# Or from package.json
if [ -z "$STACK" ]; then
  if grep -q "tailwindcss" package.json 2>/dev/null; then
    STACK="tailwind"
  fi
fi
```

### Generate Based on Stack

**Tailwind (`design/tailwind.config.ts`):**
```typescript
import type { Config } from 'tailwindcss'
import tokens from './tokens.json'

export default {
  theme: {
    extend: {
      colors: {
        primary: tokens.color.primary.$value,
        secondary: tokens.color.secondary.$value,
        // ... map all colors
      },
      fontFamily: {
        sans: tokens.typography.fontFamily.sans.$value.split(', '),
        mono: tokens.typography.fontFamily.mono.$value.split(', '),
      },
      // ... map all tokens
    },
  },
} satisfies Config
```

**CSS Variables (`design/variables.css`):**
```css
:root {
  /* Colors */
  --color-primary: #635bff;
  --color-secondary: #0a2540;
  /* ... */

  /* Typography */
  --font-sans: Inter, system-ui, sans-serif;
  --font-mono: JetBrains Mono, monospace;
  /* ... */

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  /* ... */
}
```

**README (`design/README.md`):**
```markdown
# Design System

Generated by WXCODE on [date].

## Colors
| Token | Value | Usage |
|-------|-------|-------|
| primary | #635bff | Main brand color |
| ... | ... | ... |

## Typography
...

## Usage
Import `tokens.json` or use `variables.css` in your application.
```

## Step 7: Completion

```
<!-- WXCODE:STATUS:{"status":"completed","message":"Design system generated","progress":100} -->
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DESIGN SYSTEM GENERATED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| File | Description |
|------|-------------|
| design/tokens.json | DTCG tokens (Source of Truth) |
| design/variables.css | CSS custom properties |
| design/tailwind.config.ts | Tailwind theme extension |
| design/README.md | Human-readable documentation |

Token Summary:
• 12 colors (4 brand + 4 semantic + 4 neutral)
• 9 font sizes
• 4 font weights
• 12 spacing values
• 4 shadows
• 5 border-radius values

These tokens will be used automatically by the frontend-design skill.
```

```
<!-- WXCODE:NEXT_ACTION:{"command":"progress","args":"","description":"Continue with project","priority":"recommended"} -->
```

</process>

<success_criteria>

- [ ] Method selected (URL, screenshots, questionnaire, or regenerate)
- [ ] Design tokens extracted/defined
- [ ] User confirmed values (for URL/screenshots)
- [ ] `design/tokens.json` created in DTCG format
- [ ] Stack-specific files generated
- [ ] `design/README.md` created
- [ ] Completion summary displayed

</success_criteria>

<integration>

## Using Design Tokens in Execution

During `/wxcode:execute-phase`, when UI tasks are detected:

1. Check for `design/tokens.json`
2. Include tokens as context for `frontend-design` skill
3. Skill uses tokens as Source of Truth for all visual decisions

## Updating Design System

To update after initial creation:
```
/wxcode:design-system --url https://new-reference.com
```

To regenerate stack files after manual tokens.json edit:
```
/wxcode:design-system --regenerate
```

</integration>
