---
name: wxcode:version
description: Display WXCODE version
allowed-tools:
  - Read
---

<structured_output>
**At command start:**
```
<!-- WXCODE:HEADER:{"command":"version","args":"$ARGUMENTS","title":"WXCODE ▶ VERSION"} -->
```
</structured_output>

<objective>
Display the current WXCODE version.
</objective>

<process>

Read and display version:

```bash
cat ~/.claude/get-shit-done/VERSION
```

Output format:

```
WXCODE v{VERSION}
```

</process>
