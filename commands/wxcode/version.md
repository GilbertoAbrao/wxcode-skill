---
name: wxcode:version
description: Display current WXCODE version and upstream info
allowed-tools:
  - Read
  - Bash
---

<objective>
Display the current WXCODE version, upstream GSD version, and installation path.
</objective>

<process>

## Read Version Info

```bash
VERSION=$(cat ~/.claude/get-shit-done/VERSION 2>/dev/null || echo "unknown")
```

## Display Version

Output this directly (not as code block):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE v${VERSION}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on GSD (Get Shit Done) v1.9.13
Upstream: github.com/glittercowboy/get-shit-done

Installation: ~/.claude/

Commands:   ~/.claude/commands/wxcode/
Agents:     ~/.claude/agents/wxcode-*.md
Reference:  ~/.claude/get-shit-done/
Bin:        ~/.claude/get-shit-done/bin/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/wxcode:update — check for updates
/wxcode:help   — show all commands
```

</process>
