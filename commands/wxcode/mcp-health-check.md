---
name: wxcode:mcp-health-check
description: Test wxcode-kb MCP server connectivity and health
allowed-tools:
  - mcp__wxcode-kb__health_check
---

<objective>
Test the wxcode-kb MCP server connectivity and display health status.

Use this command to verify the MCP server is running and accessible before starting conversion work.
</objective>

<process>

## Step 1: Call Health Check

Call the MCP health check tool:

```
mcp__wxcode-kb__health_check()
```

## Step 2: Display Result

**If success:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE MCP ► HEALTH CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ MCP wxcode-kb connected

| Service | Status |
|---------|--------|
| MongoDB | [status from response] |
| Neo4j   | [status from response] |

[Any additional info from health_check response]
```

**If fails:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE MCP ► HEALTH CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✗ MCP wxcode-kb not available

**To fix:**
1. Ensure wxcode-kb MCP server is running
2. Verify MCP is configured in Claude Code settings
3. Restart Claude Code if recently configured
```

</process>

<success_criteria>
- [ ] health_check tool called
- [ ] Status displayed clearly (success or failure)
- [ ] Service details shown if available
</success_criteria>
