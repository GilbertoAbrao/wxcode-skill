# Transformation Rules

Rules applied deterministically during `/wxcode:sync` operations.

## Directory Renames

| Original | Transformed |
|----------|-------------|
| `commands/gsd/` | `commands/wxcode/` |

## File Renames

| Pattern | Transformation |
|---------|----------------|
| `agents/gsd-*.md` | `agents/wxcode-*.md` |
| `hooks/gsd-*.js` | `hooks/wxcode-*.js` |
| `hooks/dist/gsd-*.js` | `hooks/dist/wxcode-*.js` |

## Text Substitutions

Applied in order (order matters to avoid double-replacements):

| Order | Pattern | Replacement | Scope |
|-------|---------|-------------|-------|
| 1 | `gsd:` | `wxcode:` | Command prefixes |
| 2 | `gsd-` | `wxcode-` | Agent/file prefixes |
| 3 | `GSD` | `WXCODE` | Display names, titles, banners |
| 4 | `get-shit-done` | `wxcode` | Project references |
| 5 | `Get Shit Done` | `WXCODE` | Human-readable titles |

## Exclusions (Do Not Transform)

These patterns are preserved as-is:

| Pattern | Reason |
|---------|--------|
| GitHub URLs containing `get-shit-done` | Preserve upstream references |
| `glittercowboy/get-shit-done` | Credit to original project |
| Comments mentioning "forked from GSD" | Attribution |
| `upstream` remote references | Git configuration |
| `path.join(..., 'get-shit-done')` | Folder path in installer - folder keeps original name |
| `targetDir, 'get-shit-done'` | Installation target folder |
| `'get-shit-done/` followed by path | Reference folder paths |

## File Type Scope

Transformations apply to:
- `*.md` - Markdown files
- `*.js` - JavaScript files
- `*.json` - JSON configuration
- `*.ts` - TypeScript files (if any)

Transformations do NOT apply to:
- `.git/` - Git internals
- `node_modules/` - Dependencies
- Binary files
- `.wxcode/` - This configuration directory

## Validation

After transformation, verify:
- [ ] No remaining `gsd:` command references (except in exclusions)
- [ ] No remaining `gsd-` agent references (except in exclusions)
- [ ] All banners show `WXCODE` instead of `GSD`
- [ ] Directory structure matches expected layout

---
*Rules are applied by wxcode-sync-agent during /wxcode:sync*
