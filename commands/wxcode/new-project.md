---
name: wxcode:new-project
description: Initialize a new project with deep context gathering and PROJECT.md
allowed-tools:
  - Read
  - Bash
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - WebFetch
  - mcp__wxcode-kb__*
  - mcp__playwright__*
---

<objective>

Initialize a new project through unified flow: questioning → research (optional) → requirements → roadmap.

This is the most leveraged moment in any project. Deep questioning here means better plans, better execution, better outcomes. One command takes you from idea to ready-for-planning.

**Two Modes:**

1. **Greenfield Mode** (default): Deep questioning → research → requirements → roadmap
2. **Conversion Mode** (when CONTEXT.md passed): Create foundation for WinDev/WebDev conversion

**Creates (Greenfield):**
- `.planning/PROJECT.md` — project context
- `.planning/config.json` — workflow preferences
- `.planning/research/` — domain research (optional)
- `.planning/REQUIREMENTS.md` — scoped requirements
- `.planning/ROADMAP.md` — phase structure
- `.planning/STATE.md` — project memory

**Creates (Conversion):**
- All of the above, plus:
- `.planning/CONVERSION.md` — conversion-specific context
- Project foundation (structure, config files, entry point)
- `start-dev.sh` — development server script
- Database models (all or on-demand)

**After this command:** Run `/wxcode:new-milestone` to convert first element (conversion) or `/wxcode:plan-phase 1` (greenfield).

</objective>

<execution_context>

@~/.claude/wxcode-skill/references/questioning.md
@~/.claude/wxcode-skill/references/ui-brand.md
@~/.claude/wxcode-skill/references/structured-output.md
@~/.claude/wxcode-skill/templates/project.md
@~/.claude/wxcode-skill/templates/requirements.md
@~/.claude/wxcode-skill/.wxcode/conversion/injection-points.md
@~/.claude/wxcode-skill/.wxcode/conversion/mcp-usage.md
@~/.claude/wxcode-skill/.wxcode/conversion/structure-preservation.md

</execution_context>

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"new-project","args":"$ARGUMENTS","title":"WXCODE ▶ INITIALIZING PROJECT"} -->
## WXCODE ▶ INITIALIZING PROJECT
```

**On status changes:**
```
<!-- WXCODE:STATUS:{"status":"in_progress","message":"[current step]","progress":[0-100]} -->
```

**At command end:**
```
<!-- WXCODE:NEXT_ACTION:{"command":"plan-phase","args":"1","description":"Plan the first phase","priority":"recommended"} -->
```
</structured_output>



<process>

## Phase 1: Setup

**MANDATORY FIRST STEP — Execute these checks before ANY user interaction:**

1. **Abort if project exists:**
   ```bash
   [ -f .planning/PROJECT.md ] && echo "ERROR: Project already initialized. Use /wxcode:progress" && exit 1
   ```

2. **Initialize git repo in THIS directory** (required even if inside a parent repo):
   ```bash
   if [ -d .git ] || [ -f .git ]; then
       echo "Git repo exists in current directory"
   else
       git init
       echo "Initialized new git repo"
   fi
   ```

3. **Ensure WXCODE commands are available in this project:**

   WXCODE commands are project-level (not global). This step creates a symlink
   so all `/wxcode:*` commands become available in this project.

   ```bash
   WXCODE_STORAGE="$HOME/.claude/wxcode-skill/commands/wxcode"
   WXCODE_LOCAL=".claude/commands/wxcode"

   if [ -L "$WXCODE_LOCAL" ]; then
       echo "WXCODE commands linked ✓"
   elif [ -d "$WXCODE_LOCAL" ]; then
       echo "WXCODE commands (local) ✓"
   elif [ -d "$WXCODE_STORAGE" ]; then
       mkdir -p .claude/commands
       ln -s "$WXCODE_STORAGE" "$WXCODE_LOCAL"
       echo "WXCODE commands linked ✓"
   else
       echo "⚠ WXCODE commands storage not found. Run: npx github:GilbertoAbrao/get-shit-done#main-wxcode --claude --global"
   fi
   ```

   **You MUST execute this bash block using the Bash tool before proceeding.**

4. **Detect existing code (brownfield detection):**
   ```bash
   CODE_FILES=$(find . -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.swift" -o -name "*.java" 2>/dev/null | grep -v node_modules | grep -v .git | head -20)
   HAS_PACKAGE=$([ -f package.json ] || [ -f requirements.txt ] || [ -f Cargo.toml ] || [ -f go.mod ] || [ -f Package.swift ] && echo "yes")
   HAS_CODEBASE_MAP=$([ -d .planning/codebase ] && echo "yes")
   ```

   **You MUST run all bash commands above using the Bash tool before proceeding.**

## Phase 1.5: Conversion Mode Detection

**Check if CONTEXT.md was passed as argument:**

```bash
CONTEXT_PATH="$ARGUMENTS"
```

**If CONTEXT.md path provided:**

This is a **Conversion Project**.

### MCP Availability Check (MANDATORY)

**Before proceeding, verify MCP wxcode-kb is available.**

**IMPORTANT: Use ONLY the `health_check` tool. Do NOT use `get_conversion_stats` or any other tool.**

**Initial delay:** Wait 5 seconds before first attempt (MCP servers may still be initializing).

```bash
sleep 5
```

**Attempt 1:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 2**

**Attempt 2:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 3**

**Attempt 3:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 4**

**Attempt 4:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 5**

**Attempt 5:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 6**

**Attempt 6:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 7**

**Attempt 7:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 8**

**Attempt 8:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 9**

**Attempt 9:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails:** Wait 10 seconds, then **Attempt 10**

**Attempt 10:** Call the tool exactly as shown:
```
mcp__wxcode-kb__health_check()
```

**If success:** Display and continue:
```
✓ WXCODE MCP conectado
```

**If fails after 10 attempts:**

```
╔══════════════════════════════════════════════════════════════╗
║  ERROR: MCP wxcode-kb not available                          ║
╚══════════════════════════════════════════════════════════════╝

Conversion Mode requires the wxcode-kb MCP server.
Tried 10 times with 10s delay between attempts (total ~100s).

**To fix:**
1. Run `/wxcode:mcp-health-check` to test connectivity manually
2. Ensure wxcode-kb MCP server is running
3. Verify MCP is configured in Claude Code settings
4. Restart Claude Code if recently configured
5. Try running `/wxcode:new-project` again after MCP is confirmed working

**Cannot proceed without MCP.**
```

**STOP only after all 10 attempts fail.**

---

The CONTEXT.md contains:
- Project name and target stack
- File structure and naming conventions
- Type mappings for database conversion
- Database schema from WinDev/WebDev

**IMPORTANT:** CONTEXT.md is a **snapshot**. The MCP (wxcode-kb) is the **Source of Truth**.
Always consult MCP for current data when needed.

**→ Skip to [Phase C1: Conversion Mode](#phase-c1-conversion-mode-setup)**

**If no CONTEXT.md provided:**

Continue with standard greenfield flow (Phase 2 below).

---

# CONVERSION MODE FLOW

## Phase C1: Conversion Mode Setup

**Display banner:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► INITIALIZING CONVERSION PROJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Read CONTEXT.md and extract:**

```
- Project name (from "Name:" field)
- Stack ID (from "Stack:" field, e.g., "fastapi-jinja2")
- Language (from "Language:" field)
- Framework (from "Framework:" field)
- File structure (from "File Structure" section)
- Naming conventions (from "Naming Conventions" section)
- Type mappings (from "Type Mappings" section)
- Database schema (all tables with columns, types, indexes)
```

**Consult MCP for current stats (SoT):**

```
mcp__wxcode-kb__get_project_stats()
```

Display:
```
Project: [Project Name]
Stack: [Stack ID]
Tables: [N] tables in schema
Elements: [N] total (from MCP)
```

**Initialize git and planning:**

```bash
if [ -d .git ] || [ -f .git ]; then
    echo "Git repo exists"
else
    git init
fi
mkdir -p .planning
```

## Phase C2: Create Project Foundation

Based on the **Stack ID** from CONTEXT.md, create:

### Directory Structure

Use the **File Structure** section from CONTEXT.md exactly.

Example for `fastapi-jinja2`:
```bash
mkdir -p app/models app/schemas app/routes app/services app/templates app/static app/config app/utils
```

Example for `nextjs-app-router`:
```bash
mkdir -p src/app src/components src/lib prisma public
```

### Development Database Setup

**First, get stack conventions (including ORM) via MCP:**

```
mcp__wxcode-kb__get_stack_conventions:
  stack_id: "<STACK_ID>"
```

This returns the stack's `orm`, `language`, `file_structure`, `naming_conventions`, etc.

**Create database directory:**

```bash
mkdir -p dados
```

**Register connection in OutputProject via MCP:**

```
mcp__wxcode-kb__add_connection_outputproject:
  output_project_id: "<OUTPUT_PROJECT_ID>"
  connection_name: "dev"
  connection_type: "sqlite"
  connection_string: "sqlite:///dados/dev.db"
  is_default: true
  confirm: true
```

**Create ORM-specific configuration based on stack's `orm` field:**

---

**If `orm: sqlalchemy` (Python stacks):**

```env
# .env
DATABASE_URL=sqlite:///dados/dev.db
SECRET_KEY=dev-secret-change-in-production
DEBUG=true
```

```python
# app/config/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dados/dev.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

**If `orm: prisma` (Node.js fullstack stacks):**

```env
# .env
DATABASE_URL="file:./dados/dev.db"
```

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

// Models will be added during schema conversion
```

Run `npx prisma generate` after adding models.

---

**If `orm: typeorm` (NestJS stacks):**

```env
# .env
DATABASE_URL=sqlite:./dados/dev.db
```

```typescript
// src/config/database.config.ts
import { TypeOrmModuleOptions } from '@nestjs/typeorm';

export const databaseConfig: TypeOrmModuleOptions = {
  type: 'sqlite',
  database: './dados/dev.db',
  entities: [__dirname + '/../**/*.entity{.ts,.js}'],
  synchronize: true, // Only in dev
};
```

---

**If `orm: django-orm` (Django stacks):**

```python
# settings.py (add to DATABASES)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'dados' / 'dev.db',
    }
}
```

---

**If `orm: eloquent` (Laravel stacks):**

```env
# .env
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/dados/dev.db
```

```php
// config/database.php (sqlite connection already exists, just use .env)
```

---

**If `orm: active-record` (Rails stacks):**

```yaml
# config/database.yml
development:
  adapter: sqlite3
  database: dados/dev.db
  pool: 5
  timeout: 5000
```

### Configuration Files

**For Python stacks (fastapi-*, django-*):**

Create `pyproject.toml` with framework dependencies and **package discovery**:
```toml
[project]
name = "{project_name}"
version = "0.1.0"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn[standard]>=0.22.0",
    "sqlalchemy>=2.0.0",
    "python-dotenv>=1.0.0",
    "jinja2>=3.1.0",  # if using templates
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*", "config*"]  # Include all project packages
```

Create `.env.example` with DATABASE_URL, SECRET_KEY placeholders.

**For Node.js stacks (nextjs-*, nuxt3, sveltekit, remix, nestjs-*):**

Create `package.json` with framework dependencies.
Create `.env.example` with DATABASE_URL placeholder.
Create `tsconfig.json` if TypeScript.

**For Ruby stacks (rails-erb):**

Create `Gemfile` with Rails dependencies.

**For PHP stacks (laravel-*):**

Create `composer.json` with Laravel dependencies.

### Application Entry Point

Create the main entry point based on the stack's ORM. The database config was created in the previous step.

**If `orm: sqlalchemy` (fastapi-jinja2, fastapi-htmx, fastapi-react, fastapi-vue):**

```python
# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config.database import engine, Base

app = FastAPI(title="[Project Name]")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

**If `orm: prisma` (nextjs-app-router, nextjs-pages, nuxt3, sveltekit, remix):**

```typescript
// src/lib/db.ts (or lib/prisma.ts)
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient }

export const prisma = globalForPrisma.prisma || new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

```tsx
// src/app/page.tsx (Next.js) or equivalent
export default function Home() {
  return <main><h1>[Project Name]</h1><p>Conversion in progress...</p></main>;
}
```

---

**If `orm: typeorm` (nestjs-react, nestjs-vue):**

```typescript
// src/app.module.ts
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { databaseConfig } from './config/database.config';

@Module({
  imports: [TypeOrmModule.forRoot(databaseConfig)],
})
export class AppModule {}
```

---

**If `orm: django-orm` (django-templates):**

```python
# Standard Django manage.py - database configured in settings.py
# Run: python manage.py migrate
```

---

**If `orm: eloquent` (laravel-blade, laravel-react):**

```php
// Standard Laravel - database configured in config/database.php
// Run: php artisan migrate
```

---

**If `orm: active-record` (rails-erb):**

```ruby
# Standard Rails - database configured in config/database.yml
# Run: rails db:migrate
```

### start-dev.sh

**Use the dedicated skill to create start-dev.sh from the stack template:**

```
/wxcode:create-start-dev
```

This skill will:
1. Detect the project's stack from configuration
2. Fetch the appropriate template from MongoDB (via MCP)
3. Generate `start-dev.sh` with correct ports (7xxx series)
4. Set executable permissions

### Verify Development Server

**IMPORTANT:** Test that the project runs before proceeding.

**Use the dedicated skill to start the development server:**

```
/wxcode:start-dev
```

This skill will:
1. Execute start-dev.sh
2. Verify server is running
3. Display access URLs and log location

**If test fails:**
- Check logs: `cat /tmp/{project_name}.log`
- Fix configuration issues (missing dependencies, wrong paths)
- Re-run `/wxcode:start-dev`

**Common fixes:**
- Missing `__init__.py` files in Python packages
- Missing dependencies in requirements.txt/package.json
- Wrong module paths in entry point
- **Multiple top-level packages error (setuptools):** Add to pyproject.toml:
  ```toml
  [tool.setuptools.packages.find]
  where = ["."]
  include = ["app*", "config*"]
  ```

**Only proceed to next phase when server starts and responds.**

## Phase C2.5: Design System Collection

**Display banner:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DESIGN SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Purpose:** Establish design tokens as the Single Source of Truth for all UI generation.
These tokens will be automatically used by the `frontend-design` skill during execution.

**Reference files:**
- Spec: `~/.claude/wxcode-skill/.wxcode/conversion/dtcg-spec.md`
- Flow: `~/.claude/wxcode-skill/.wxcode/conversion/design-system-flow.md`
- Template: `~/.claude/wxcode-skill/templates/design-tokens.json`

### Step 1: Choose Collection Method

Use AskUserQuestion:

```
questions: [
  {
    header: "Design Source",
    question: "How should I capture your design preferences?",
    multiSelect: false,
    options: [
      { label: "Reference URL", description: "Extract colors, typography from an existing website" },
      { label: "Screenshots", description: "Analyze design mockups or reference images" },
      { label: "Questionnaire", description: "Answer questions about brand, style preferences" },
      { label: "Use defaults", description: "Start with WXCODE default tokens (can customize later)" }
    ]
  }
]
```

### Step 2A: URL Extraction

**If "Reference URL" selected:**

Ask inline: "What URL should I analyze for design patterns?"

**Fetch and analyze:**

```
WebFetch:
  url: [user's URL]
  prompt: "Extract design tokens from this page:
    1. Colors: primary brand color, secondary colors, text colors, background colors, semantic colors (success, warning, error, info)
    2. Typography: font families (headings, body, mono), font sizes used, font weights, line heights
    3. Spacing: padding/margin patterns, gap sizes
    4. Border radius: button rounding, card rounding, input rounding
    5. Shadows: elevation levels used
    Return as structured JSON matching DTCG format."
```

**If WebFetch fails (403, timeout, JavaScript-rendered):**

Display:
```
WebFetch couldn't access this URL. Trying MCP Playwright...
```

Use MCP Playwright as fallback:
```
mcp__playwright__navigate: url=[user's URL]
mcp__playwright__screenshot: (capture page)
```

Then analyze screenshot using same extraction logic.

**Confidence check:**

After extraction, categorize confidence:
- **High (>80%):** Token clearly visible/extracted
- **Medium (50-80%):** Inferred from patterns
- **Low (<50%):** Best guess, needs validation

Present extraction results:
```
## Extracted Design Tokens

**From:** [URL]

### Colors (High confidence)
- Primary: #3b82f6 ← extracted from buttons, links
- Secondary: #1e293b ← extracted from headers
- Background: #ffffff ← page background
- Text: #111827 ← body text

### Typography (Medium confidence)
- Display: Inter ← detected via font-family
- Body: Inter ← same
- Sizes: 14px base, scale inferred

### Spacing (Low confidence)
- Base unit: 4px (inferred from patterns)

---
Accept these tokens? (yes / adjust / try different URL)
```

If "adjust" → allow inline edits.
If "try different URL" → return to Step 2A.

### Step 2B: Screenshot Analysis

**If "Screenshots" selected:**

Ask inline: "Please provide the path(s) to your design mockups or screenshots."

**Read and analyze images:**

For each image path:
```
Read: [image_path]
```

Analyze visually for:
- Dominant colors and color palette
- Typography styles (approximate sizes, weights)
- Spacing patterns
- Border radius usage
- Shadow/elevation levels
- Overall aesthetic (modern, minimal, bold, etc.)

Present findings same as URL extraction (with confidence levels).

### Step 2C: Questionnaire

**If "Questionnaire" selected:**

**Round 1 — Brand personality:**

```
questions: [
  {
    header: "Style",
    question: "What visual style best describes your brand?",
    multiSelect: false,
    options: [
      { label: "Modern & Minimal", description: "Clean lines, lots of whitespace, subtle colors" },
      { label: "Bold & Vibrant", description: "Strong colors, high contrast, energetic" },
      { label: "Professional & Corporate", description: "Trustworthy, structured, conventional" },
      { label: "Playful & Friendly", description: "Rounded shapes, warm colors, approachable" }
    ]
  },
  {
    header: "Primary Color",
    question: "What's your primary brand color?",
    multiSelect: false,
    options: [
      { label: "Blue", description: "Trust, stability (#3b82f6)" },
      { label: "Green", description: "Growth, nature (#22c55e)" },
      { label: "Purple", description: "Creative, premium (#8b5cf6)" },
      { label: "Custom", description: "I'll provide a hex code" }
    ]
  }
]
```

If "Custom" selected, ask for hex code inline.

**Round 2 — Typography:**

```
questions: [
  {
    header: "Typography",
    question: "What typography style do you prefer?",
    multiSelect: false,
    options: [
      { label: "Modern Sans-Serif", description: "Inter, system fonts — clean, readable" },
      { label: "Classic Serif", description: "Georgia, Merriweather — traditional, editorial" },
      { label: "Technical Mono", description: "JetBrains Mono emphasis — developer-focused" },
      { label: "Custom fonts", description: "I'll specify font names" }
    ]
  }
]
```

**Round 3 — Shapes:**

```
questions: [
  {
    header: "Corners",
    question: "How rounded should UI elements be?",
    multiSelect: false,
    options: [
      { label: "Sharp", description: "0-2px radius — crisp, technical" },
      { label: "Subtle", description: "4-6px radius — balanced (most common)" },
      { label: "Rounded", description: "8-12px radius — friendly, modern" },
      { label: "Pill", description: "Fully rounded — playful, soft" }
    ]
  }
]
```

Generate tokens from questionnaire responses using style presets.

### Step 2D: Use Defaults

**If "Use defaults" selected:**

Copy template directly:
```bash
mkdir -p design
cp ~/.claude/wxcode-skill/templates/design-tokens.json design/tokens.json
```

Display:
```
Created design/tokens.json with WXCODE default tokens.
You can customize these anytime by editing the file.
```

Skip to Step 4.

### Step 3: Generate Design Tokens

**Create design directory and tokens file:**

```bash
mkdir -p design
```

Write `design/tokens.json` using DTCG format from spec:

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "$description": "[Project Name] Design System",
  "color": {
    "brand": {
      "primary": {
        "$value": "[extracted/selected color]",
        "$type": "color",
        "$description": "Main brand color"
      }
      // ... all color tokens
    }
    // ... semantic, neutral, background, text, border
  },
  "typography": {
    // ... fontFamily, fontSize, fontWeight, lineHeight
  },
  "spacing": {
    // ... spacing scale
  },
  "shadow": {
    // ... shadow definitions
  },
  "borderRadius": {
    // ... radius scale
  },
  "transition": {
    // ... duration and easing
  },
  "breakpoint": {
    // ... responsive breakpoints
  },
  "zIndex": {
    // ... layer stack
  }
}
```

### Step 4: Generate Stack-Specific Config (if applicable)

Based on stack, generate additional config:

**For Tailwind-based stacks (nextjs-*, nuxt3, sveltekit, remix):**

Generate `tailwind.config.js` theme extension that references tokens:

```javascript
// tailwind.config.js (partial - theme section)
import tokens from './design/tokens.json';

const theme = {
  extend: {
    colors: {
      primary: tokens.color.brand.primary.$value,
      secondary: tokens.color.brand.secondary.$value,
      // ... map all colors
    },
    fontFamily: {
      display: [tokens.typography.fontFamily.display.$value],
      body: [tokens.typography.fontFamily.body.$value],
      mono: [tokens.typography.fontFamily.mono.$value],
    },
    // ... other mappings
  }
};
```

**For CSS-variable stacks (fastapi-jinja2, fastapi-htmx, django-*, rails-*, laravel-blade):**

Generate `app/static/css/tokens.css` (or equivalent path):

```css
:root {
  /* Brand Colors */
  --color-primary: #3b82f6;
  --color-secondary: #1e293b;

  /* Typography */
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  /* ... */
}
```

### Step 5: Display Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DESIGN SYSTEM READY ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| File | Purpose |
|------|---------|
| design/tokens.json | DTCG tokens (Source of Truth) |
| [stack-specific file] | Framework integration |

**Primary:** [color swatch] [hex]
**Typography:** [font names]
**Style:** [extracted/selected style]

These tokens will be used automatically when generating UI components.
```

**Continue to next phase.**

## Phase C3: Schema Decision

Use AskUserQuestion:

```
questions: [
  {
    header: "Schema",
    question: "Convert database schema now or on-demand as each milestone needs it?",
    multiSelect: false,
    options: [
      { label: "Convert all now (Recommended)", description: "Generate all [N] models upfront — consistent foundation" },
      { label: "On-demand", description: "Generate models as each element is converted — gradual approach" }
    ]
  }
]
```

## Phase C4: Generate Database Models

**CRITICAL:** Models must preserve **exact** legacy table/column names for transparent database access. The new application accesses the EXISTING legacy database.

**If "Convert all now":**

Display progress:
```
◆ Generating [N] database models...
```

Spawn the schema generator agent:

```
Task(wxcode-schema-generator):
  prompt: |
    Generate all database models for this conversion project.

    Output Project ID: [output_project_id from CONTEXT.md]

    Use capability: generate_all_models

    Requirements:
    - Preserve EXACT legacy table names (use __tablename__, @@map, db_table, etc.)
    - Preserve EXACT legacy column names (use Column name=, @map, db_column, field=, etc.)
    - Include all constraints, indexes, and relationships
    - Create base/config files as needed by the stack
    - Create index/barrel file exporting all models

    After generation, validate models against MCP schema to confirm no drift.
  subagent_type: wxcode-schema-generator
```

Wait for agent completion and display summary:
```
✓ Generated [N] models
  - Tables: [list first 5]...
  - Validation: [✓ All match | ⚠ See report]
```

**If "On-demand":**

Create only base infrastructure (no agent needed):

**Python/SQLAlchemy:**
- Create `app/models/base.py` with Base class and engine setup
- Create `app/models/__init__.py` (empty, will be populated per milestone)
- Add comment: "Models generated on-demand via wxcode-schema-generator"

**TypeScript/Prisma:**
- Create `prisma/schema.prisma` with datasource only (no models yet)
- Add comment: "Models added per milestone via wxcode-schema-generator"

**TypeScript/TypeORM:**
- Create `src/config/database.ts` with connection setup
- Create `src/models/index.ts` (empty barrel file)
- Add comment: "Models generated on-demand via wxcode-schema-generator"

Note in PROJECT.md:
```markdown
## Schema Status

Models generated per milestone as needed.
Use `/wxcode:validate-schema` to check coverage.
```

## Phase C5: Workflow Preferences

Use the same workflow preferences as greenfield mode (Phase 5 below), but with conversion-appropriate defaults:

**Suggested defaults for conversion:**
- Mode: YOLO (conversion is well-defined)
- Depth: Standard
- Parallelization: Yes
- Commit docs: Yes
- Research: No (legacy is the source)
- Plan Check: Yes
- Verifier: Yes
- Model Profile: Balanced

Create `.planning/config.json` with selected settings.

## Phase C6: Create Planning Documents

**Create .planning/PROJECT.md:**

```markdown
# [Project Name]

## What This Is

Conversion of WinDev/WebDev application to [Stack Target].

## Source

- **Type:** WinDev/WebDev (via MCP: wxcode-kb)
- **Elements:** [N] total

## Target Stack

- **Stack ID:** [stack-id]
- **Language:** [language]
- **Framework:** [framework]
- **ORM:** [orm]

## Conversion Strategy

Element-by-element conversion via milestones. Each milestone:
1. Queries Knowledge Base for source code
2. Converts to target stack
3. Integrates with existing foundation

## Schema Status

[✓ All [N] models generated | Models generated per milestone as needed]

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Stack: [Stack ID] | Defined in CONTEXT.md | — Set |
| Schema: [all/on-demand] | User preference | — Set |

---
*Initialized: [date]*
```

**Create .planning/CONVERSION.md:**

Use template from `.wxcode/conversion/templates/CONVERSION.md`, populated with:
- Source project info from MCP
- Target stack from CONTEXT.md
- Initial state (0 converted)
- Project-wide decisions (defaults, can adjust later)

**Create .planning/ROADMAP.md:**

```markdown
# Conversion Roadmap

## Strategy

Elements are converted via milestones. Each milestone:
1. Receives element context
2. Queries Knowledge Base for source code (MCP is SoT)
3. Converts to [Stack Target]
4. Integrates with existing foundation

## Milestones

| # | Element | Status |
|---|---------|--------|
| — | Foundation | ✓ Complete |
| 1 | (pending) | — |

---
*Initialized: [date]*
```

**Create .planning/STATE.md:**

```markdown
# Project State

## Current Position

- **Mode:** Conversion
- **Phase:** Foundation complete
- **Next:** First element conversion

## Foundation Status

- [x] Project structure created
- [x] Configuration files created
- [x] Entry point created
- [x] start-dev.sh created
- [x] Development server verified ✓
- [x] [Schema status]
- [x] Planning documents created
- [x] CONVERSION.md created

---
*Last updated: [date]*
```

## Phase C7: Commit Foundation

```bash
git add -A
git commit -m "$(cat <<'EOF'
feat: initialize conversion project foundation

Stack: [Stack ID]
Schema: [N] models [generated/pending]

Ready for element conversion via milestones.
EOF
)"
```

## Phase C8: Mark Project Initialized

**Call MCP to mark project as initialized:**

```
mcp__wxcode-kb__mark_project_initialized()
```

## Phase C9: Conversion Complete

**Display completion (NO next step suggestion):**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► FOUNDATION READY ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**[Project Name]**

| Component | Status |
|-----------|--------|
| Structure | ✓ Created |
| Config | ✓ Created |
| Entry point | ✓ Ready to run |
| start-dev.sh | ✓ Verified working |
| Models | ✓ [N] generated / Pending |
| Planning | ✓ Initialized |
| CONVERSION.md | ✓ Created |

───────────────────────────────────────────────────────────────

## Run the Project

/wxcode:start-dev

───────────────────────────────────────────────────────────────
```

**IMPORTANT:** Do NOT suggest next steps. IDE tooling will handle navigation.

**→ End command (conversion mode)**

---

# GREENFIELD MODE FLOW

## Phase 2: Brownfield Offer

**If existing code detected and .planning/codebase/ doesn't exist:**

Check the results from setup step:
- If `CODE_FILES` is non-empty OR `HAS_PACKAGE` is "yes"
- AND `HAS_CODEBASE_MAP` is NOT "yes"

Use AskUserQuestion:
- header: "Existing Code"
- question: "I detected existing code in this directory. Would you like to map the codebase first?"
- options:
  - "Map codebase first" — Run /wxcode:map-codebase to understand existing architecture (Recommended)
  - "Skip mapping" — Proceed with project initialization

**If "Map codebase first":**
```
Run `/wxcode:map-codebase` first, then return to `/wxcode:new-project`
```
Exit command.

**If "Skip mapping":** Continue to Phase 3.

**If no existing code detected OR codebase already mapped:** Continue to Phase 3.

## Phase 3: Deep Questioning

**Display stage banner:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► QUESTIONING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Open the conversation:**

Ask inline (freeform, NOT AskUserQuestion):

"What do you want to build?"

Wait for their response. This gives you the context needed to ask intelligent follow-up questions.

**Follow the thread:**

Based on what they said, ask follow-up questions that dig into their response. Use AskUserQuestion with options that probe what they mentioned — interpretations, clarifications, concrete examples.

Keep following threads. Each answer opens new threads to explore. Ask about:
- What excited them
- What problem sparked this
- What they mean by vague terms
- What it would actually look like
- What's already decided

Consult `questioning.md` for techniques:
- Challenge vagueness
- Make abstract concrete
- Surface assumptions
- Find edges
- Reveal motivation

**Check context (background, not out loud):**

As you go, mentally check the context checklist from `questioning.md`. If gaps remain, weave questions naturally. Don't suddenly switch to checklist mode.

**Decision gate:**

When you could write a clear PROJECT.md, use AskUserQuestion:

- header: "Ready?"
- question: "I think I understand what you're after. Ready to create PROJECT.md?"
- options:
  - "Create PROJECT.md" — Let's move forward
  - "Keep exploring" — I want to share more / ask me more

If "Keep exploring" — ask what they want to add, or identify gaps and probe naturally.

Loop until "Create PROJECT.md" selected.

## Phase 4: Write PROJECT.md

Synthesize all context into `.planning/PROJECT.md` using the template from `templates/project.md`.

**For greenfield projects:**

Initialize requirements as hypotheses:

```markdown
## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

### Out of Scope

- [Exclusion 1] — [why]
- [Exclusion 2] — [why]
```

All Active requirements are hypotheses until shipped and validated.

**For brownfield projects (codebase map exists):**

Infer Validated requirements from existing code:

1. Read `.planning/codebase/ARCHITECTURE.md` and `STACK.md`
2. Identify what the codebase already does
3. These become the initial Validated set

```markdown
## Requirements

### Validated

- ✓ [Existing capability 1] — existing
- ✓ [Existing capability 2] — existing
- ✓ [Existing capability 3] — existing

### Active

- [ ] [New requirement 1]
- [ ] [New requirement 2]

### Out of Scope

- [Exclusion 1] — [why]
```

**Key Decisions:**

Initialize with any decisions made during questioning:

```markdown
## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| [Choice from questioning] | [Why] | — Pending |
```

**Last updated footer:**

```markdown
---
*Last updated: [date] after initialization*
```

Do not compress. Capture everything gathered.

**Commit PROJECT.md:**

```bash
mkdir -p .planning
git add .planning/PROJECT.md
git commit -m "$(cat <<'EOF'
docs: initialize project

[One-liner from PROJECT.md What This Is section]
EOF
)"
```

## Phase 5: Workflow Preferences

**Round 1 — Core workflow settings (4 questions):**

```
questions: [
  {
    header: "Mode",
    question: "How do you want to work?",
    multiSelect: false,
    options: [
      { label: "YOLO (Recommended)", description: "Auto-approve, just execute" },
      { label: "Interactive", description: "Confirm at each step" }
    ]
  },
  {
    header: "Depth",
    question: "How thorough should planning be?",
    multiSelect: false,
    options: [
      { label: "Quick", description: "Ship fast (3-5 phases, 1-3 plans each)" },
      { label: "Standard", description: "Balanced scope and speed (5-8 phases, 3-5 plans each)" },
      { label: "Comprehensive", description: "Thorough coverage (8-12 phases, 5-10 plans each)" }
    ]
  },
  {
    header: "Execution",
    question: "Run plans in parallel?",
    multiSelect: false,
    options: [
      { label: "Parallel (Recommended)", description: "Independent plans run simultaneously" },
      { label: "Sequential", description: "One plan at a time" }
    ]
  },
  {
    header: "Git Tracking",
    question: "Commit planning docs to git?",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Planning docs tracked in version control" },
      { label: "No", description: "Keep .planning/ local-only (add to .gitignore)" }
    ]
  }
]
```

**Round 1.5 — Output language:**

```
questions: [
  {
    header: "Language",
    question: "Which language for WXCODE outputs?",
    multiSelect: false,
    options: [
      { label: "Português (pt-BR) (Recommended)", description: "Mensagens e status em português brasileiro" },
      { label: "English (en)", description: "Messages and status in English" },
      { label: "Español (es)", description: "Mensajes y estados en español" }
    ]
  }
]
```

Save the selection to config.json as `output_language`:
- "Português (pt-BR)" → `"pt-BR"`
- "English (en)" → `"en"`
- "Español (es)" → `"es"`

**Round 2 — Workflow agents:**

These spawn additional agents during planning/execution. They add tokens and time but improve quality.

| Agent | When it runs | What it does |
|-------|--------------|--------------|
| **Researcher** | Before planning each phase | Investigates domain, finds patterns, surfaces gotchas |
| **Plan Checker** | After plan is created | Verifies plan actually achieves the phase goal |
| **Verifier** | After phase execution | Confirms must-haves were delivered |

All recommended for important projects. Skip for quick experiments.

```
questions: [
  {
    header: "Research",
    question: "Research before planning each phase? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Investigate domain, find patterns, surface gotchas" },
      { label: "No", description: "Plan directly from requirements" }
    ]
  },
  {
    header: "Plan Check",
    question: "Verify plans will achieve their goals? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Catch gaps before execution starts" },
      { label: "No", description: "Execute plans without verification" }
    ]
  },
  {
    header: "Verifier",
    question: "Verify work satisfies requirements after each phase? (adds tokens/time)",
    multiSelect: false,
    options: [
      { label: "Yes (Recommended)", description: "Confirm deliverables match phase goals" },
      { label: "No", description: "Trust execution, skip verification" }
    ]
  },
  {
    header: "Model Profile",
    question: "Which AI models for planning agents?",
    multiSelect: false,
    options: [
      { label: "Balanced (Recommended)", description: "Sonnet for most agents — good quality/cost ratio" },
      { label: "Quality", description: "Opus for research/roadmap — higher cost, deeper analysis" },
      { label: "Budget", description: "Haiku where possible — fastest, lowest cost" }
    ]
  }
]
```

Create `.planning/config.json` with all settings:

```json
{
  "mode": "yolo|interactive",
  "depth": "quick|standard|comprehensive",
  "parallelization": true|false,
  "commit_docs": true|false,
  "output_language": "en|pt-BR|es",
  "model_profile": "quality|balanced|budget",
  "workflow": {
    "research": true|false,
    "plan_check": true|false,
    "verifier": true|false
  }
}
```

**If commit_docs = No:**
- Set `commit_docs: false` in config.json
- Add `.planning/` to `.gitignore` (create if needed)

**If commit_docs = Yes:**
- No additional gitignore entries needed

**Commit config.json:**

```bash
git add .planning/config.json
git commit -m "$(cat <<'EOF'
chore: add project config

Mode: [chosen mode]
Depth: [chosen depth]
Parallelization: [enabled/disabled]
Workflow agents: research=[on/off], plan_check=[on/off], verifier=[on/off]
EOF
)"
```

**Note:** Run `/wxcode:settings` anytime to update these preferences.

## Phase 5.5: Resolve Model Profile

Read model profile for agent spawning:

```bash
MODEL_PROFILE=$(cat .planning/config.json 2>/dev/null | grep -o '"model_profile"[[:space:]]*:[[:space:]]*"[^"]*"' | grep -o '"[^"]*"$' | tr -d '"' || echo "balanced")
```

Default to "balanced" if not set.

**Model lookup table:**

| Agent | quality | balanced | budget |
|-------|---------|----------|--------|
| wxcode-project-researcher | opus | sonnet | haiku |
| wxcode-research-synthesizer | sonnet | sonnet | haiku |
| wxcode-roadmapper | opus | sonnet | sonnet |

Store resolved models for use in Task calls below.

## Phase 5.6: Design System Collection

**Display banner:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DESIGN SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Purpose:** Establish design tokens as the Single Source of Truth for all UI generation.
These tokens will be automatically used by the `frontend-design` skill during execution.

**Reference files:**
- Spec: `~/.claude/wxcode-skill/.wxcode/conversion/dtcg-spec.md`
- Flow: `~/.claude/wxcode-skill/.wxcode/conversion/design-system-flow.md`
- Template: `~/.claude/wxcode-skill/templates/design-tokens.json`

### Step 1: Choose Collection Method

Use AskUserQuestion:

```
questions: [
  {
    header: "Design Source",
    question: "How should I capture your design preferences?",
    multiSelect: false,
    options: [
      { label: "Reference URL", description: "Extract colors, typography from an existing website" },
      { label: "Screenshots", description: "Analyze design mockups or reference images" },
      { label: "Questionnaire", description: "Answer questions about brand, style preferences" },
      { label: "Use defaults", description: "Start with WXCODE default tokens (can customize later)" }
    ]
  }
]
```

### Step 2A: URL Extraction

**If "Reference URL" selected:**

Ask inline: "What URL should I analyze for design patterns?"

**Fetch and analyze:**

```
WebFetch:
  url: [user's URL]
  prompt: "Extract design tokens from this page:
    1. Colors: primary brand color, secondary colors, text colors, background colors, semantic colors (success, warning, error, info)
    2. Typography: font families (headings, body, mono), font sizes used, font weights, line heights
    3. Spacing: padding/margin patterns, gap sizes
    4. Border radius: button rounding, card rounding, input rounding
    5. Shadows: elevation levels used
    Return as structured JSON matching DTCG format."
```

**If WebFetch fails (403, timeout, JavaScript-rendered):**

Display:
```
WebFetch couldn't access this URL. Trying MCP Playwright...
```

Use MCP Playwright as fallback:
```
mcp__playwright__navigate: url=[user's URL]
mcp__playwright__screenshot: (capture page)
```

Then analyze screenshot using same extraction logic.

**Confidence check:**

After extraction, categorize confidence:
- **High (>80%):** Token clearly visible/extracted
- **Medium (50-80%):** Inferred from patterns
- **Low (<50%):** Best guess, needs validation

Present extraction results:
```
## Extracted Design Tokens

**From:** [URL]

### Colors (High confidence)
- Primary: #3b82f6 ← extracted from buttons, links
- Secondary: #1e293b ← extracted from headers
- Background: #ffffff ← page background
- Text: #111827 ← body text

### Typography (Medium confidence)
- Display: Inter ← detected via font-family
- Body: Inter ← same
- Sizes: 14px base, scale inferred

### Spacing (Low confidence)
- Base unit: 4px (inferred from patterns)

---
Accept these tokens? (yes / adjust / try different URL)
```

If "adjust" → allow inline edits.
If "try different URL" → return to Step 2A.

### Step 2B: Screenshot Analysis

**If "Screenshots" selected:**

Ask inline: "Please provide the path(s) to your design mockups or screenshots."

**Read and analyze images:**

For each image path:
```
Read: [image_path]
```

Analyze visually for:
- Dominant colors and color palette
- Typography styles (approximate sizes, weights)
- Spacing patterns
- Border radius usage
- Shadow/elevation levels
- Overall aesthetic (modern, minimal, bold, etc.)

Present findings same as URL extraction (with confidence levels).

### Step 2C: Questionnaire

**If "Questionnaire" selected:**

**Round 1 — Brand personality:**

```
questions: [
  {
    header: "Style",
    question: "What visual style best describes your brand?",
    multiSelect: false,
    options: [
      { label: "Modern & Minimal", description: "Clean lines, lots of whitespace, subtle colors" },
      { label: "Bold & Vibrant", description: "Strong colors, high contrast, energetic" },
      { label: "Professional & Corporate", description: "Trustworthy, structured, conventional" },
      { label: "Playful & Friendly", description: "Rounded shapes, warm colors, approachable" }
    ]
  },
  {
    header: "Primary Color",
    question: "What's your primary brand color?",
    multiSelect: false,
    options: [
      { label: "Blue", description: "Trust, stability (#3b82f6)" },
      { label: "Green", description: "Growth, nature (#22c55e)" },
      { label: "Purple", description: "Creative, premium (#8b5cf6)" },
      { label: "Custom", description: "I'll provide a hex code" }
    ]
  }
]
```

If "Custom" selected, ask for hex code inline.

**Round 2 — Typography:**

```
questions: [
  {
    header: "Typography",
    question: "What typography style do you prefer?",
    multiSelect: false,
    options: [
      { label: "Modern Sans-Serif", description: "Inter, system fonts — clean, readable" },
      { label: "Classic Serif", description: "Georgia, Merriweather — traditional, editorial" },
      { label: "Technical Mono", description: "JetBrains Mono emphasis — developer-focused" },
      { label: "Custom fonts", description: "I'll specify font names" }
    ]
  }
]
```

**Round 3 — Shapes:**

```
questions: [
  {
    header: "Corners",
    question: "How rounded should UI elements be?",
    multiSelect: false,
    options: [
      { label: "Sharp", description: "0-2px radius — crisp, technical" },
      { label: "Subtle", description: "4-6px radius — balanced (most common)" },
      { label: "Rounded", description: "8-12px radius — friendly, modern" },
      { label: "Pill", description: "Fully rounded — playful, soft" }
    ]
  }
]
```

Generate tokens from questionnaire responses using style presets.

### Step 2D: Use Defaults

**If "Use defaults" selected:**

Copy template directly:
```bash
mkdir -p design
cp ~/.claude/wxcode-skill/templates/design-tokens.json design/tokens.json
```

Display:
```
Created design/tokens.json with WXCODE default tokens.
You can customize these anytime by editing the file.
```

Skip to Step 4.

### Step 3: Generate Design Tokens

**Create design directory and tokens file:**

```bash
mkdir -p design
```

Write `design/tokens.json` using DTCG format from spec:

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "$description": "[Project Name] Design System",
  "color": {
    "brand": {
      "primary": {
        "$value": "[extracted/selected color]",
        "$type": "color",
        "$description": "Main brand color"
      }
      // ... all color tokens
    }
    // ... semantic, neutral, background, text, border
  },
  "typography": {
    // ... fontFamily, fontSize, fontWeight, lineHeight
  },
  "spacing": {
    // ... spacing scale
  },
  "shadow": {
    // ... shadow definitions
  },
  "borderRadius": {
    // ... radius scale
  },
  "transition": {
    // ... duration and easing
  },
  "breakpoint": {
    // ... responsive breakpoints
  },
  "zIndex": {
    // ... layer stack
  }
}
```

### Step 4: Generate Stack-Specific Config (if applicable)

**Note:** Stack may not be determined yet in greenfield flow. If stack is known (from PROJECT.md or questioning), generate config. Otherwise, defer to execution phase.

**For Tailwind-based stacks:**

Generate `tailwind.config.js` theme extension that references tokens.

**For CSS-variable stacks:**

Generate `static/css/tokens.css` (or equivalent path):

```css
:root {
  /* Brand Colors */
  --color-primary: #3b82f6;
  --color-secondary: #1e293b;

  /* Typography */
  --font-display: Inter, system-ui, sans-serif;
  --font-body: Inter, system-ui, sans-serif;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  /* ... */
}
```

### Step 5: Display Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DESIGN SYSTEM READY ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| File | Purpose |
|------|---------|
| design/tokens.json | DTCG tokens (Source of Truth) |

**Primary:** [color swatch] [hex]
**Typography:** [font names]
**Style:** [extracted/selected style]

These tokens will be used automatically when generating UI components.
```

**Continue to next phase.**

## Phase 6: Research Decision

Use AskUserQuestion:
- header: "Research"
- question: "Research the domain ecosystem before defining requirements?"
- options:
  - "Research first (Recommended)" — Discover standard stacks, expected features, architecture patterns
  - "Skip research" — I know this domain well, go straight to requirements

**If "Research first":**

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► RESEARCHING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Researching [domain] ecosystem...
```

Create research directory:
```bash
mkdir -p .planning/research
```

**Determine milestone context:**

Check if this is greenfield or subsequent milestone:
- If no "Validated" requirements in PROJECT.md → Greenfield (building from scratch)
- If "Validated" requirements exist → Subsequent milestone (adding to existing app)

Display spawning indicator:
```
◆ Spawning 4 researchers in parallel...
  → Stack research
  → Features research
  → Architecture research
  → Pitfalls research
```

Spawn 4 parallel wxcode-project-researcher agents with rich context:

```
Task(prompt="First, read ~/.claude/agents/wxcode-project-researcher.md for your role and instructions.

<research_type>
Project Research — Stack dimension for [domain].
</research_type>

<milestone_context>
[greenfield OR subsequent]

Greenfield: Research the standard stack for building [domain] from scratch.
Subsequent: Research what's needed to add [target features] to an existing [domain] app. Don't re-research the existing system.
</milestone_context>

<question>
What's the standard 2025 stack for [domain]?
</question>

<project_context>
[PROJECT.md summary - core value, constraints, what they're building]
</project_context>

<downstream_consumer>
Your STACK.md feeds into roadmap creation. Be prescriptive:
- Specific libraries with versions
- Clear rationale for each choice
- What NOT to use and why
</downstream_consumer>

<quality_gate>
- [ ] Versions are current (verify with Context7/official docs, not training data)
- [ ] Rationale explains WHY, not just WHAT
- [ ] Confidence levels assigned to each recommendation
</quality_gate>

<output>
Write to: .planning/research/STACK.md
Use template: ~/.claude/wxcode-skill/templates/research-project/STACK.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Stack research")

Task(prompt="First, read ~/.claude/agents/wxcode-project-researcher.md for your role and instructions.

<research_type>
Project Research — Features dimension for [domain].
</research_type>

<milestone_context>
[greenfield OR subsequent]

Greenfield: What features do [domain] products have? What's table stakes vs differentiating?
Subsequent: How do [target features] typically work? What's expected behavior?
</milestone_context>

<question>
What features do [domain] products have? What's table stakes vs differentiating?
</question>

<project_context>
[PROJECT.md summary]
</project_context>

<downstream_consumer>
Your FEATURES.md feeds into requirements definition. Categorize clearly:
- Table stakes (must have or users leave)
- Differentiators (competitive advantage)
- Anti-features (things to deliberately NOT build)
</downstream_consumer>

<quality_gate>
- [ ] Categories are clear (table stakes vs differentiators vs anti-features)
- [ ] Complexity noted for each feature
- [ ] Dependencies between features identified
</quality_gate>

<output>
Write to: .planning/research/FEATURES.md
Use template: ~/.claude/wxcode-skill/templates/research-project/FEATURES.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Features research")

Task(prompt="First, read ~/.claude/agents/wxcode-project-researcher.md for your role and instructions.

<research_type>
Project Research — Architecture dimension for [domain].
</research_type>

<milestone_context>
[greenfield OR subsequent]

Greenfield: How are [domain] systems typically structured? What are major components?
Subsequent: How do [target features] integrate with existing [domain] architecture?
</milestone_context>

<question>
How are [domain] systems typically structured? What are major components?
</question>

<project_context>
[PROJECT.md summary]
</project_context>

<downstream_consumer>
Your ARCHITECTURE.md informs phase structure in roadmap. Include:
- Component boundaries (what talks to what)
- Data flow (how information moves)
- Suggested build order (dependencies between components)
</downstream_consumer>

<quality_gate>
- [ ] Components clearly defined with boundaries
- [ ] Data flow direction explicit
- [ ] Build order implications noted
</quality_gate>

<output>
Write to: .planning/research/ARCHITECTURE.md
Use template: ~/.claude/wxcode-skill/templates/research-project/ARCHITECTURE.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Architecture research")

Task(prompt="First, read ~/.claude/agents/wxcode-project-researcher.md for your role and instructions.

<research_type>
Project Research — Pitfalls dimension for [domain].
</research_type>

<milestone_context>
[greenfield OR subsequent]

Greenfield: What do [domain] projects commonly get wrong? Critical mistakes?
Subsequent: What are common mistakes when adding [target features] to [domain]?
</milestone_context>

<question>
What do [domain] projects commonly get wrong? Critical mistakes?
</question>

<project_context>
[PROJECT.md summary]
</project_context>

<downstream_consumer>
Your PITFALLS.md prevents mistakes in roadmap/planning. For each pitfall:
- Warning signs (how to detect early)
- Prevention strategy (how to avoid)
- Which phase should address it
</downstream_consumer>

<quality_gate>
- [ ] Pitfalls are specific to this domain (not generic advice)
- [ ] Prevention strategies are actionable
- [ ] Phase mapping included where relevant
</quality_gate>

<output>
Write to: .planning/research/PITFALLS.md
Use template: ~/.claude/wxcode-skill/templates/research-project/PITFALLS.md
</output>
", subagent_type="general-purpose", model="{researcher_model}", description="Pitfalls research")
```

After all 4 agents complete, spawn synthesizer to create SUMMARY.md:

```
Task(prompt="
<task>
Synthesize research outputs into SUMMARY.md.
</task>

<research_files>
Read these files:
- .planning/research/STACK.md
- .planning/research/FEATURES.md
- .planning/research/ARCHITECTURE.md
- .planning/research/PITFALLS.md
</research_files>

<output>
Write to: .planning/research/SUMMARY.md
Use template: ~/.claude/wxcode-skill/templates/research-project/SUMMARY.md
Commit after writing.
</output>
", subagent_type="wxcode-research-synthesizer", model="{synthesizer_model}", description="Synthesize research")
```

Display research complete banner and key findings:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► RESEARCH COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Key Findings

**Stack:** [from SUMMARY.md]
**Table Stakes:** [from SUMMARY.md]
**Watch Out For:** [from SUMMARY.md]

Files: `.planning/research/`
```

**If "Skip research":** Continue to Phase 7.

## Phase 7: Define Requirements

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► DEFINING REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Load context:**

Read PROJECT.md and extract:
- Core value (the ONE thing that must work)
- Stated constraints (budget, timeline, tech limitations)
- Any explicit scope boundaries

**If research exists:** Read research/FEATURES.md and extract feature categories.

**Present features by category:**

```
Here are the features for [domain]:

## Authentication
**Table stakes:**
- Sign up with email/password
- Email verification
- Password reset
- Session management

**Differentiators:**
- Magic link login
- OAuth (Google, GitHub)
- 2FA

**Research notes:** [any relevant notes]

---

## [Next Category]
...
```

**If no research:** Gather requirements through conversation instead.

Ask: "What are the main things users need to be able to do?"

For each capability mentioned:
- Ask clarifying questions to make it specific
- Probe for related capabilities
- Group into categories

**Scope each category:**

For each category, use AskUserQuestion:

- header: "[Category name]"
- question: "Which [category] features are in v1?"
- multiSelect: true
- options:
  - "[Feature 1]" — [brief description]
  - "[Feature 2]" — [brief description]
  - "[Feature 3]" — [brief description]
  - "None for v1" — Defer entire category

Track responses:
- Selected features → v1 requirements
- Unselected table stakes → v2 (users expect these)
- Unselected differentiators → out of scope

**Identify gaps:**

Use AskUserQuestion:
- header: "Additions"
- question: "Any requirements research missed? (Features specific to your vision)"
- options:
  - "No, research covered it" — Proceed
  - "Yes, let me add some" — Capture additions

**Validate core value:**

Cross-check requirements against Core Value from PROJECT.md. If gaps detected, surface them.

**Generate REQUIREMENTS.md:**

Create `.planning/REQUIREMENTS.md` with:
- v1 Requirements grouped by category (checkboxes, REQ-IDs)
- v2 Requirements (deferred)
- Out of Scope (explicit exclusions with reasoning)
- Traceability section (empty, filled by roadmap)

**REQ-ID format:** `[CATEGORY]-[NUMBER]` (AUTH-01, CONTENT-02)

**Requirement quality criteria:**

Good requirements are:
- **Specific and testable:** "User can reset password via email link" (not "Handle password reset")
- **User-centric:** "User can X" (not "System does Y")
- **Atomic:** One capability per requirement (not "User can login and manage profile")
- **Independent:** Minimal dependencies on other requirements

Reject vague requirements. Push for specificity:
- "Handle authentication" → "User can log in with email/password and stay logged in across sessions"
- "Support sharing" → "User can share post via link that opens in recipient's browser"

**Present full requirements list:**

Show every requirement (not counts) for user confirmation:

```
## v1 Requirements

### Authentication
- [ ] **AUTH-01**: User can create account with email/password
- [ ] **AUTH-02**: User can log in and stay logged in across sessions
- [ ] **AUTH-03**: User can log out from any page

### Content
- [ ] **CONT-01**: User can create posts with text
- [ ] **CONT-02**: User can edit their own posts

[... full list ...]

---

Does this capture what you're building? (yes / adjust)
```

If "adjust": Return to scoping.

**Commit requirements:**

```bash
git add .planning/REQUIREMENTS.md
git commit -m "$(cat <<'EOF'
docs: define v1 requirements

[X] requirements across [N] categories
[Y] requirements deferred to v2
EOF
)"
```

## Phase 8: Create Roadmap

Display stage banner:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► CREATING ROADMAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ Spawning roadmapper...
```

Spawn wxcode-roadmapper agent with context:

```
Task(prompt="
<planning_context>

**Project:**
@.planning/PROJECT.md

**Requirements:**
@.planning/REQUIREMENTS.md

**Research (if exists):**
@.planning/research/SUMMARY.md

**Config:**
@.planning/config.json

</planning_context>

<instructions>
Create roadmap:
1. Derive phases from requirements (don't impose structure)
2. Map every v1 requirement to exactly one phase
3. Derive 2-5 success criteria per phase (observable user behaviors)
4. Validate 100% coverage
5. Write files immediately (ROADMAP.md, STATE.md, update REQUIREMENTS.md traceability)
6. Return ROADMAP CREATED with summary

Write files first, then return. This ensures artifacts persist even if context is lost.
</instructions>
", subagent_type="wxcode-roadmapper", model="{roadmapper_model}", description="Create roadmap")
```

**Handle roadmapper return:**

**If `## ROADMAP BLOCKED`:**
- Present blocker information
- Work with user to resolve
- Re-spawn when resolved

**If `## ROADMAP CREATED`:**

Read the created ROADMAP.md and present it nicely inline:

```
---

## Proposed Roadmap

**[N] phases** | **[X] requirements mapped** | All v1 requirements covered ✓

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | [Name] | [Goal] | [REQ-IDs] | [count] |
| 2 | [Name] | [Goal] | [REQ-IDs] | [count] |
| 3 | [Name] | [Goal] | [REQ-IDs] | [count] |
...

### Phase Details

**Phase 1: [Name]**
Goal: [goal]
Requirements: [REQ-IDs]
Success criteria:
1. [criterion]
2. [criterion]
3. [criterion]

**Phase 2: [Name]**
Goal: [goal]
Requirements: [REQ-IDs]
Success criteria:
1. [criterion]
2. [criterion]

[... continue for all phases ...]

---
```

**CRITICAL: Ask for approval before committing:**

Use AskUserQuestion:
- header: "Roadmap"
- question: "Does this roadmap structure work for you?"
- options:
  - "Approve" — Commit and continue
  - "Adjust phases" — Tell me what to change
  - "Review full file" — Show raw ROADMAP.md

**If "Approve":** Continue to commit.

**If "Adjust phases":**
- Get user's adjustment notes
- Re-spawn roadmapper with revision context:
  ```
  Task(prompt="
  <revision>
  User feedback on roadmap:
  [user's notes]

  Current ROADMAP.md: @.planning/ROADMAP.md

  Update the roadmap based on feedback. Edit files in place.
  Return ROADMAP REVISED with changes made.
  </revision>
  ", subagent_type="wxcode-roadmapper", model="{roadmapper_model}", description="Revise roadmap")
  ```
- Present revised roadmap
- Loop until user approves

**If "Review full file":** Display raw `cat .planning/ROADMAP.md`, then re-ask.

**Commit roadmap (after approval):**

```bash
git add .planning/ROADMAP.md .planning/STATE.md .planning/REQUIREMENTS.md
git commit -m "$(cat <<'EOF'
docs: create roadmap ([N] phases)

Phases:
1. [phase-name]: [requirements covered]
2. [phase-name]: [requirements covered]
...

All v1 requirements mapped to phases.
EOF
)"
```

## Phase 10: Done

Present completion with next steps:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► PROJECT INITIALIZED ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**[Project Name]**

| Artifact       | Location                    |
|----------------|-----------------------------|
| Project        | `.planning/PROJECT.md`      |
| Config         | `.planning/config.json`     |
| Research       | `.planning/research/`       |
| Requirements   | `.planning/REQUIREMENTS.md` |
| Roadmap        | `.planning/ROADMAP.md`      |

**[N] phases** | **[X] requirements** | Ready to build ✓

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Phase 1: [Phase Name]** — [Goal from ROADMAP.md]

/wxcode:discuss-phase 1 — gather context and clarify approach

<sub>/clear first → fresh context window</sub>

---

**Also available:**
- /wxcode:plan-phase 1 — skip discussion, plan directly

───────────────────────────────────────────────────────────────
```

</process>

<output>

**Greenfield Mode:**
- `.planning/PROJECT.md`
- `.planning/config.json`
- `.planning/research/` (if research selected)
  - `STACK.md`
  - `FEATURES.md`
  - `ARCHITECTURE.md`
  - `PITFALLS.md`
  - `SUMMARY.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `design/tokens.json` — DTCG design tokens (Source of Truth)
- Stack-specific config (if stack known)

**Conversion Mode (additional):**
- `.planning/CONVERSION.md`
- Project directory structure (per stack)
- Configuration files (pyproject.toml, package.json, etc.)
- Application entry point
- `start-dev.sh`
- Database models (if "convert all now" selected)
- `design/tokens.json` — DTCG design tokens (Source of Truth)
- Stack-specific design config (tailwind.config.js or tokens.css)

</output>

<success_criteria>

**Greenfield Mode:**
- [ ] .planning/ directory created
- [ ] Git repo initialized
- [ ] Brownfield detection completed
- [ ] Deep questioning completed (threads followed, not rushed)
- [ ] PROJECT.md captures full context → **committed**
- [ ] config.json has workflow mode, depth, parallelization → **committed**
- [ ] **Design system collected** (URL, screenshot, questionnaire, or defaults)
- [ ] **design/tokens.json created** with DTCG format
- [ ] Research completed (if selected) — 4 parallel agents spawned → **committed**
- [ ] Requirements gathered (from research or conversation)
- [ ] User scoped each category (v1/v2/out of scope)
- [ ] REQUIREMENTS.md created with REQ-IDs → **committed**
- [ ] wxcode-roadmapper spawned with context
- [ ] Roadmap files written immediately (not draft)
- [ ] User feedback incorporated (if any)
- [ ] ROADMAP.md created with phases, requirement mappings, success criteria
- [ ] STATE.md initialized
- [ ] REQUIREMENTS.md traceability updated
- [ ] User knows next step is `/wxcode:discuss-phase 1`

**Conversion Mode:**
- [ ] CONTEXT.md loaded and parsed
- [ ] MCP consulted for current stats (SoT)
- [ ] Stack target identified
- [ ] Project structure created (per CONTEXT.md file structure)
- [ ] Configuration files created (per stack)
- [ ] Entry point created (project can run)
- [ ] start-dev.sh created and executable
- [ ] **Development server tested and working** (verified via curl)
- [ ] **Design system collected** (URL, screenshot, questionnaire, or defaults)
- [ ] **design/tokens.json created** with DTCG format
- [ ] **Stack-specific design config generated** (tailwind.config.js or tokens.css)
- [ ] Schema decision made (all now / on-demand)
- [ ] Models generated (if "all now" selected)
- [ ] config.json created with workflow preferences → **committed**
- [ ] .planning/PROJECT.md created → **committed**
- [ ] .planning/CONVERSION.md created → **committed**
- [ ] .planning/ROADMAP.md created → **committed**
- [ ] .planning/STATE.md created → **committed**
- [ ] Foundation committed to git
- [ ] MCP mark_project_initialized called
- [ ] NO next step suggested (IDE handles navigation)

**Atomic commits:** Each phase commits its artifacts immediately. If context is lost, artifacts persist.

**Dashboard:** After project initialization completes, update dashboard (see below).

</success_criteria>

<dashboard_update>

## Update Dashboards (Final Step)

**MANDATORY:** After project initialization, regenerate dashboards:

```
/wxcode:dashboard --all
```

This generates all dashboard JSON files and emits `[WXCODE:DASHBOARD_UPDATED]` notifications.

</dashboard_update>
