---
name: wxcode:version
description: Display WXCODE version
allowed-tools:
  - Read
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"version","args":"$ARGUMENTS","title":"WXCODE ▶ VERSION"} -->
## WXCODE ▶ VERSION
```

**At command end:**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"v{VERSION}"} -->
```
</structured_output>

<objective>
Display the current WXCODE version.
</objective>

<process>

Read and display version:

```bash
cat ~/.claude/wxcode-skill/VERSION
```

Output format:

```
WXCODE v{VERSION}

<!-- WXCODE:STATUS:{"status":"completed","message":"v{VERSION}"} -->
```

</process>
