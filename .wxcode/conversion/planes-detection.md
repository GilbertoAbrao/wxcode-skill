# Detecting Planes in WinDev Code

Planes are a WinDev feature for creating stacked views within a single page/window.
The WXCODE/GSD workflow must identify planes by analyzing the element's code since
there is no dedicated MCP tool for plane extraction.

## What Are Planes?

Planes are **stacked views** where only one is visible at a time:

```
┌─────────────────────────────────────┐
│            PAGE_Cadastro            │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐    │
│  │ Plane 1: Dados Pessoais     │ ◄──┼── Visible
│  │ - EDT_Nome                  │    │
│  │ - EDT_CPF                   │    │
│  │ - BTN_Proximo               │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ Plane 2: Dados Profissionais│ ◄──┼── Hidden
│  │ - EDT_Empresa               │    │
│  │ - EDT_Cargo                 │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │ Plane 3: Confirmacao        │ ◄──┼── Hidden
│  │ - STC_Resumo                │    │
│  │ - BTN_Confirmar             │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

Common use cases:
- **Wizard/Step forms** - Multi-step data entry
- **Tab-like interfaces** - Different views of same data
- **Conditional views** - Show/hide based on state

---

## How to Identify Planes

### Source 1: get_controls Response

Check the `plane` property in control metadata:

```json
{
  "controls": [
    {
      "name": "EDT_Nome",
      "properties": {
        "plane": 1
      }
    },
    {
      "name": "EDT_Empresa",
      "properties": {
        "plane": 2
      }
    }
  ]
}
```

**Analysis approach:**
1. Group controls by `plane` property
2. Identify controls without plane (visible on all)
3. Build plane structure

### Source 2: raw_content Analysis

In the element's `raw_content` (WLanguage code), look for:

#### Plane Declarations

```wlanguage
// Explicit plane variables (less common)
PLANE1 is Plane
PLANE2 is Plane
PLANE_DADOS is Plane
```

#### Plane Property Assignments

```wlanguage
// Control assigned to specific plane
EDT_Nome..Plane = 1
BTN_Proximo..Plane = 1
EDT_Empresa..Plane = 2
EDT_Cargo..Plane = 2
STC_Resumo..Plane = 3
BTN_Confirmar..Plane = 3
```

#### Plane Navigation Functions

```wlanguage
// Show specific plane
Plane(2)

// Get current plane
nCurrentPlane = Plane()

// Navigate relatively
Plane(Plane() + 1)  // Next plane
Plane(Plane() - 1)  // Previous plane

// Enable/disable planes
PlaneEnable(1, True)
PlaneEnable(2, False)

// Check plane visibility
IF PlaneVisible(3) THEN ...
```

#### Navigation Event Patterns

```wlanguage
// Typical "Next" button
PROCEDURE BTN_Proximo_Click()
  IF ValidaPlaneAtual() THEN
    Plane(Plane() + 1)
  END

// Typical "Previous" button
PROCEDURE BTN_Anterior_Click()
  Plane(Plane() - 1)

// Direct plane navigation (tab-like)
PROCEDURE TAB_DadosPessoais_Click()
  Plane(1)

PROCEDURE TAB_DadosProfissionais_Click()
  Plane(2)
```

---

## Analysis Algorithm

```
1. Call MCP: get_element {name}
2. Call MCP: get_controls {name}

3. From get_controls:
   - Group controls by plane property
   - Create plane_map = { plane_number: [controls] }

4. From raw_content:
   - Search for Plane() function calls
   - Search for ..Plane = N assignments
   - Search for PlaneEnable/PlaneVisible calls
   - Identify navigation patterns

5. Build plane structure:
   planes = [
     {
       number: 1,
       name: "Dados Pessoais" (infer from controls/context),
       controls: [...],
       navigation: { next: button_name, prev: null }
     },
     ...
   ]

6. Determine plane purpose:
   - Wizard: Sequential navigation (next/prev buttons)
   - Tabs: Direct navigation (tab buttons)
   - Conditional: Based on state/selection
```

---

## Documenting Planes

When planes are detected, document in RESEARCH.md:

```markdown
## Planes Structure

This element has **{N} planes** functioning as a **{wizard|tabs|conditional}**.

### Plane 1: {Inferred Name}
**Purpose:** {What this plane does}
**Controls:**
- EDT_Nome (edit) - Nome completo
- EDT_CPF (edit) - CPF com validacao
- BTN_Proximo (button) - Avanca para plane 2

### Plane 2: {Inferred Name}
**Purpose:** {What this plane does}
**Controls:**
- ...

### Navigation Pattern
- Type: {wizard|tabs|conditional}
- Forward: BTN_Proximo calls Plane(Plane()+1)
- Backward: BTN_Anterior calls Plane(Plane()-1)
- Validation: ValidaPlaneAtual() before advance
```

---

## Conversion Strategies

Based on target stack, planes can become:

### Strategy: Tabs (Same Page)

**Best for:** Non-sequential access, quick switching
**Target stacks:** All

```html
<!-- Jinja2/HTML example -->
<div class="tabs">
  <button onclick="showPane(1)">Dados Pessoais</button>
  <button onclick="showPane(2)">Dados Profissionais</button>
</div>
<div id="pane-1" class="pane active">...</div>
<div id="pane-2" class="pane">...</div>
```

### Strategy: Wizard (Multi-Step Form)

**Best for:** Sequential data entry, validation between steps
**Target stacks:** All

```html
<!-- Jinja2/HTML example -->
<form id="wizard">
  <div class="step" data-step="1">
    <!-- Plane 1 fields -->
    <button type="button" onclick="nextStep()">Proximo</button>
  </div>
  <div class="step hidden" data-step="2">
    <!-- Plane 2 fields -->
    <button type="button" onclick="prevStep()">Anterior</button>
    <button type="button" onclick="nextStep()">Proximo</button>
  </div>
</form>
```

### Strategy: Separate Routes

**Best for:** Complex planes, deep linking needed
**Target stacks:** MPA frameworks

```python
# FastAPI example
@router.get("/cadastro/dados-pessoais")
def step1(): ...

@router.get("/cadastro/dados-profissionais")
def step2(): ...

@router.post("/cadastro/dados-pessoais")
def submit_step1():
    # Validate and redirect to step 2
    return RedirectResponse("/cadastro/dados-profissionais")
```

### Strategy: SPA State

**Best for:** Rich interactivity, no page reloads
**Target stacks:** React, Vue, Angular

```javascript
// React example
const [currentStep, setCurrentStep] = useState(1);

return (
  <>
    {currentStep === 1 && <DadosPessoais onNext={() => setCurrentStep(2)} />}
    {currentStep === 2 && <DadosProfissionais onPrev={() => setCurrentStep(1)} />}
  </>
);
```

### Strategy: HTMX Fragments

**Best for:** Progressive enhancement, partial updates
**Target stacks:** HTMX-enabled

```html
<div id="wizard-content">
  <form hx-post="/cadastro/step1" hx-target="#wizard-content">
    <!-- Plane 1 fields -->
    <button type="submit">Proximo</button>
  </form>
</div>
```

---

## User Decision Required

When planes are detected, ask the user:

```
This element has {N} planes functioning as a {wizard|tabs}.

How should planes be converted for {stack_name}?

1. Tabs (same page, JavaScript switching)
2. Wizard (multi-step form with validation)
3. Separate routes (one URL per plane)
4. Let me decide per element

Current plane structure:
- Plane 1: {name} ({N} controls)
- Plane 2: {name} ({N} controls)
- ...
```

Document the decision in CONTEXT.md for consistency across elements.

---

## Common Patterns

### Wizard with Validation

```wlanguage
PROCEDURE BTN_Proximo_Click()
  SWITCH Plane()
    CASE 1:
      IF ValidaDadosPessoais() THEN
        Plane(2)
      END
    CASE 2:
      IF ValidaDadosProfissionais() THEN
        Plane(3)
      END
  END
```

**Conversion note:** Preserve validation logic, call before step transition.

### Tab-Style Navigation

```wlanguage
PROCEDURE TAB_Click(nTab)
  Plane(nTab)
  // Highlight active tab
  FOR i = 1 TO 3
    TAB[i]..State = (i = nTab ? Active : Normal)
  END
```

**Conversion note:** Use CSS classes for active state.

### Conditional Planes

```wlanguage
PROCEDURE RBT_TipoPessoa_Click()
  IF RBT_TipoPessoa = "PF" THEN
    Plane(1)  // Pessoa Fisica
  ELSE
    Plane(2)  // Pessoa Juridica
  END
```

**Conversion note:** May become conditional rendering based on selection.
