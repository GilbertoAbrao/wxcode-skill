# DTCG Token Specification

This document describes the Design Token Community Group (DTCG) format used by WXCODE for design system tokens.

## Overview

DTCG is a W3C Community Group format for design tokens that provides:
- **Interoperability** between design tools and code
- **Type safety** with explicit token types
- **Hierarchical organization** for complex design systems
- **Tool compatibility** with Style Dictionary, Figma Tokens, etc.

**Reference:** https://design-tokens.github.io/community-group/format/

---

## File Location

```
project/
└── design/
    └── tokens.json    ← DTCG format file
```

---

## Schema

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/"
}
```

---

## Token Structure

Each token follows this format:

```json
{
  "token-name": {
    "$value": "<value>",
    "$type": "<type>",
    "$description": "<optional description>"
  }
}
```

### Token Types

| Type | Description | Example Value |
|------|-------------|---------------|
| `color` | CSS color value | `#635bff`, `rgb(99, 91, 255)` |
| `dimension` | Size with unit | `16px`, `1rem`, `0.5em` |
| `fontFamily` | Font stack | `Inter, sans-serif` |
| `fontWeight` | Numeric weight | `400`, `600`, `700` |
| `duration` | Time value | `200ms`, `0.3s` |
| `cubicBezier` | Easing function | `[0.4, 0, 0.2, 1]` |
| `shadow` | Box shadow | `0 4px 6px rgba(0,0,0,0.1)` |
| `number` | Unitless number | `1.5`, `0.95` |

---

## Token Categories

### 1. Colors

```json
{
  "color": {
    "brand": {
      "primary": {
        "$value": "#635bff",
        "$type": "color",
        "$description": "Main brand color, used in CTAs and key UI elements"
      },
      "secondary": {
        "$value": "#0a2540",
        "$type": "color",
        "$description": "Secondary brand color, used in headers and emphasis"
      }
    },
    "semantic": {
      "success": {
        "$value": "#22c55e",
        "$type": "color"
      },
      "warning": {
        "$value": "#f59e0b",
        "$type": "color"
      },
      "error": {
        "$value": "#ef4444",
        "$type": "color"
      },
      "info": {
        "$value": "#3b82f6",
        "$type": "color"
      }
    },
    "neutral": {
      "50": { "$value": "#f9fafb", "$type": "color" },
      "100": { "$value": "#f3f4f6", "$type": "color" },
      "200": { "$value": "#e5e7eb", "$type": "color" },
      "300": { "$value": "#d1d5db", "$type": "color" },
      "400": { "$value": "#9ca3af", "$type": "color" },
      "500": { "$value": "#6b7280", "$type": "color" },
      "600": { "$value": "#4b5563", "$type": "color" },
      "700": { "$value": "#374151", "$type": "color" },
      "800": { "$value": "#1f2937", "$type": "color" },
      "900": { "$value": "#111827", "$type": "color" },
      "950": { "$value": "#030712", "$type": "color" }
    },
    "background": {
      "primary": { "$value": "#ffffff", "$type": "color" },
      "secondary": { "$value": "#f9fafb", "$type": "color" },
      "tertiary": { "$value": "#f3f4f6", "$type": "color" }
    },
    "text": {
      "primary": { "$value": "#111827", "$type": "color" },
      "secondary": { "$value": "#4b5563", "$type": "color" },
      "tertiary": { "$value": "#9ca3af", "$type": "color" },
      "inverse": { "$value": "#ffffff", "$type": "color" }
    }
  }
}
```

### 2. Typography

```json
{
  "typography": {
    "fontFamily": {
      "display": {
        "$value": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        "$type": "fontFamily",
        "$description": "Used for headings and display text"
      },
      "body": {
        "$value": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        "$type": "fontFamily",
        "$description": "Used for body text and UI elements"
      },
      "mono": {
        "$value": "JetBrains Mono, Fira Code, Consolas, monospace",
        "$type": "fontFamily",
        "$description": "Used for code blocks and technical content"
      }
    },
    "fontSize": {
      "xs": { "$value": "0.75rem", "$type": "dimension" },
      "sm": { "$value": "0.875rem", "$type": "dimension" },
      "base": { "$value": "1rem", "$type": "dimension" },
      "lg": { "$value": "1.125rem", "$type": "dimension" },
      "xl": { "$value": "1.25rem", "$type": "dimension" },
      "2xl": { "$value": "1.5rem", "$type": "dimension" },
      "3xl": { "$value": "1.875rem", "$type": "dimension" },
      "4xl": { "$value": "2.25rem", "$type": "dimension" },
      "5xl": { "$value": "3rem", "$type": "dimension" },
      "6xl": { "$value": "3.75rem", "$type": "dimension" }
    },
    "fontWeight": {
      "normal": { "$value": "400", "$type": "fontWeight" },
      "medium": { "$value": "500", "$type": "fontWeight" },
      "semibold": { "$value": "600", "$type": "fontWeight" },
      "bold": { "$value": "700", "$type": "fontWeight" }
    },
    "lineHeight": {
      "tight": { "$value": "1.25", "$type": "number" },
      "snug": { "$value": "1.375", "$type": "number" },
      "normal": { "$value": "1.5", "$type": "number" },
      "relaxed": { "$value": "1.625", "$type": "number" },
      "loose": { "$value": "2", "$type": "number" }
    },
    "letterSpacing": {
      "tighter": { "$value": "-0.05em", "$type": "dimension" },
      "tight": { "$value": "-0.025em", "$type": "dimension" },
      "normal": { "$value": "0", "$type": "dimension" },
      "wide": { "$value": "0.025em", "$type": "dimension" },
      "wider": { "$value": "0.05em", "$type": "dimension" }
    }
  }
}
```

### 3. Spacing

```json
{
  "spacing": {
    "$description": "Spacing scale based on 4px base unit",
    "0": { "$value": "0", "$type": "dimension" },
    "px": { "$value": "1px", "$type": "dimension" },
    "0.5": { "$value": "0.125rem", "$type": "dimension" },
    "1": { "$value": "0.25rem", "$type": "dimension" },
    "1.5": { "$value": "0.375rem", "$type": "dimension" },
    "2": { "$value": "0.5rem", "$type": "dimension" },
    "2.5": { "$value": "0.625rem", "$type": "dimension" },
    "3": { "$value": "0.75rem", "$type": "dimension" },
    "3.5": { "$value": "0.875rem", "$type": "dimension" },
    "4": { "$value": "1rem", "$type": "dimension" },
    "5": { "$value": "1.25rem", "$type": "dimension" },
    "6": { "$value": "1.5rem", "$type": "dimension" },
    "7": { "$value": "1.75rem", "$type": "dimension" },
    "8": { "$value": "2rem", "$type": "dimension" },
    "9": { "$value": "2.25rem", "$type": "dimension" },
    "10": { "$value": "2.5rem", "$type": "dimension" },
    "11": { "$value": "2.75rem", "$type": "dimension" },
    "12": { "$value": "3rem", "$type": "dimension" },
    "14": { "$value": "3.5rem", "$type": "dimension" },
    "16": { "$value": "4rem", "$type": "dimension" },
    "20": { "$value": "5rem", "$type": "dimension" },
    "24": { "$value": "6rem", "$type": "dimension" },
    "28": { "$value": "7rem", "$type": "dimension" },
    "32": { "$value": "8rem", "$type": "dimension" },
    "36": { "$value": "9rem", "$type": "dimension" },
    "40": { "$value": "10rem", "$type": "dimension" },
    "44": { "$value": "11rem", "$type": "dimension" },
    "48": { "$value": "12rem", "$type": "dimension" },
    "52": { "$value": "13rem", "$type": "dimension" },
    "56": { "$value": "14rem", "$type": "dimension" },
    "60": { "$value": "15rem", "$type": "dimension" },
    "64": { "$value": "16rem", "$type": "dimension" },
    "72": { "$value": "18rem", "$type": "dimension" },
    "80": { "$value": "20rem", "$type": "dimension" },
    "96": { "$value": "24rem", "$type": "dimension" }
  }
}
```

### 4. Shadows

```json
{
  "shadow": {
    "none": {
      "$value": "none",
      "$type": "shadow"
    },
    "sm": {
      "$value": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
      "$type": "shadow"
    },
    "base": {
      "$value": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
      "$type": "shadow"
    },
    "md": {
      "$value": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
      "$type": "shadow"
    },
    "lg": {
      "$value": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
      "$type": "shadow"
    },
    "xl": {
      "$value": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
      "$type": "shadow"
    },
    "2xl": {
      "$value": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
      "$type": "shadow"
    },
    "inner": {
      "$value": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)",
      "$type": "shadow"
    }
  }
}
```

### 5. Border Radius

```json
{
  "borderRadius": {
    "none": { "$value": "0", "$type": "dimension" },
    "sm": { "$value": "0.125rem", "$type": "dimension" },
    "base": { "$value": "0.25rem", "$type": "dimension" },
    "md": { "$value": "0.375rem", "$type": "dimension" },
    "lg": { "$value": "0.5rem", "$type": "dimension" },
    "xl": { "$value": "0.75rem", "$type": "dimension" },
    "2xl": { "$value": "1rem", "$type": "dimension" },
    "3xl": { "$value": "1.5rem", "$type": "dimension" },
    "full": { "$value": "9999px", "$type": "dimension" }
  }
}
```

### 6. Border Width

```json
{
  "borderWidth": {
    "0": { "$value": "0", "$type": "dimension" },
    "1": { "$value": "1px", "$type": "dimension" },
    "2": { "$value": "2px", "$type": "dimension" },
    "4": { "$value": "4px", "$type": "dimension" },
    "8": { "$value": "8px", "$type": "dimension" }
  }
}
```

### 7. Transitions

```json
{
  "transition": {
    "duration": {
      "fast": { "$value": "150ms", "$type": "duration" },
      "normal": { "$value": "200ms", "$type": "duration" },
      "slow": { "$value": "300ms", "$type": "duration" },
      "slower": { "$value": "500ms", "$type": "duration" }
    },
    "easing": {
      "linear": { "$value": [0, 0, 1, 1], "$type": "cubicBezier" },
      "ease": { "$value": [0.25, 0.1, 0.25, 1], "$type": "cubicBezier" },
      "easeIn": { "$value": [0.4, 0, 1, 1], "$type": "cubicBezier" },
      "easeOut": { "$value": [0, 0, 0.2, 1], "$type": "cubicBezier" },
      "easeInOut": { "$value": [0.4, 0, 0.2, 1], "$type": "cubicBezier" }
    }
  }
}
```

### 8. Breakpoints (Optional)

```json
{
  "breakpoint": {
    "sm": { "$value": "640px", "$type": "dimension" },
    "md": { "$value": "768px", "$type": "dimension" },
    "lg": { "$value": "1024px", "$type": "dimension" },
    "xl": { "$value": "1280px", "$type": "dimension" },
    "2xl": { "$value": "1536px", "$type": "dimension" }
  }
}
```

### 9. Z-Index (Optional)

```json
{
  "zIndex": {
    "auto": { "$value": "auto", "$type": "number" },
    "0": { "$value": "0", "$type": "number" },
    "10": { "$value": "10", "$type": "number" },
    "20": { "$value": "20", "$type": "number" },
    "30": { "$value": "30", "$type": "number" },
    "40": { "$value": "40", "$type": "number" },
    "50": { "$value": "50", "$type": "number" },
    "modal": { "$value": "100", "$type": "number" },
    "tooltip": { "$value": "150", "$type": "number" }
  }
}
```

---

## Dark Mode

For dark mode support, add a `dark` variant:

```json
{
  "color": {
    "background": {
      "primary": {
        "$value": "#ffffff",
        "$type": "color"
      }
    }
  },
  "dark": {
    "color": {
      "background": {
        "primary": {
          "$value": "#0f172a",
          "$type": "color"
        }
      }
    }
  }
}
```

---

## Stack-Specific Translation

### Tailwind CSS

```typescript
// tailwind.config.ts
import tokens from './tokens.json';

export default {
  theme: {
    extend: {
      colors: {
        primary: tokens.color.brand.primary.$value,
        secondary: tokens.color.brand.secondary.$value,
        // ... map all colors
      },
      fontFamily: {
        display: tokens.typography.fontFamily.display.$value,
        body: tokens.typography.fontFamily.body.$value,
        mono: tokens.typography.fontFamily.mono.$value,
      },
      // ... map all tokens
    }
  }
}
```

### CSS Variables

```css
/* variables.css */
:root {
  /* Colors */
  --color-primary: #635bff;
  --color-secondary: #0a2540;
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Typography */
  --font-display: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: JetBrains Mono, Fira Code, Consolas, monospace;

  /* Font Sizes */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

  /* Border Radius */
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background-primary: #0f172a;
    --color-text-primary: #f1f5f9;
    /* ... dark overrides */
  }
}
```

### CSS-in-JS (styled-components/emotion)

```typescript
// theme.ts
export const theme = {
  colors: {
    brand: {
      primary: '#635bff',
      secondary: '#0a2540',
    },
    semantic: {
      success: '#22c55e',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    },
    // ... all colors
  },
  typography: {
    fontFamily: {
      display: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
      body: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
      mono: 'JetBrains Mono, Fira Code, Consolas, monospace',
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      // ...
    },
  },
  spacing: {
    1: '0.25rem',
    2: '0.5rem',
    4: '1rem',
    // ...
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    // ...
  },
  borderRadius: {
    sm: '0.125rem',
    md: '0.375rem',
    lg: '0.5rem',
    full: '9999px',
  },
};
```

---

## Validation

Use JSON Schema for validation:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["color", "typography", "spacing"],
  "properties": {
    "color": {
      "type": "object",
      "required": ["brand", "semantic"]
    },
    "typography": {
      "type": "object",
      "required": ["fontFamily", "fontSize"]
    },
    "spacing": {
      "type": "object"
    }
  }
}
```

---

## References

- [W3C Design Tokens Format](https://design-tokens.github.io/community-group/format/)
- [Style Dictionary](https://amzn.github.io/style-dictionary/)
- [Figma Tokens](https://www.figma.com/community/plugin/843461159747178978/Tokens-Studio-for-Figma)
- [Tailwind CSS Theme Configuration](https://tailwindcss.com/docs/theme)
