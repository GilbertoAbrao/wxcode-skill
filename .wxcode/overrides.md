# Override Files

Files listed here are completely managed locally and will NOT be updated from upstream during sync.

## Active Overrides

| File | Reason | Added |
|------|--------|-------|
| `commands/wxcode/update.md` | Points to GilbertoAbrao/get-shit-done#main-wxcode instead of upstream | 2026-01-27 |
| `bin/install.js` (banner section) | WXCODE ASCII art logo instead of GSD | 2026-02-04 |

## How Overrides Work

When a file is marked as an override:

1. **During sync:** The file is skipped entirely
2. **Upstream changes:** You'll be notified but changes won't be applied
3. **Responsibility:** You maintain this file manually

## Adding an Override

Use `/wxcode:override <file-path>` to add a file to this list.

Example:
```
/wxcode:override commands/wxcode/help.md
```

This is useful when:
- You've completely rewritten a command
- You have local-only documentation
- You maintain a custom workflow

## Removing an Override

Use `/wxcode:override --remove <file-path>` to remove a file from this list.

After removal, the next sync will update the file from upstream.

## Recommended Overrides

Consider overriding these files if you customize them heavily:

| File | Why Override |
|------|--------------|
| `README.md` | Custom documentation for your fork |
| `commands/wxcode/help.md` | Custom help content |
| `CHANGELOG.md` | Your own changelog |

---
*Managed by /wxcode:override command*
