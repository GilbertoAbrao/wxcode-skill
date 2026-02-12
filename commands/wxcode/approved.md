---
name: wxcode:approved
description: Approve checkpoint and continue execution
user-invocable: true
---

<structured_output>
## Structured Output (MANDATORY)

**At command start (emit together with visual banner, no blank line):**
```
<!-- WXCODE:HEADER:{"command":"approved","args":"","title":"WXCODE ► CHECKPOINT APPROVED"} -->
## WXCODE ► CHECKPOINT APPROVED
```

**At command end:**
```
<!-- WXCODE:STATUS:{"status":"completed","message":"Checkpoint approved, continuing execution"} -->
```
</structured_output>

<objective>
Signal checkpoint approval during execute-phase. This command is invoked by the UI when the user clicks the "approved" action button rendered from a WXCODE:NEXT_ACTION tag.
</objective>

<process>

The user has approved the current checkpoint. Continue the execution flow:

1. If inside an active `/wxcode:execute-phase` with a pending checkpoint:
   - Treat this as the user typing "approved"
   - Spawn the continuation agent for the paused plan
   - Resume wave-based execution

2. If inside an active verification (`human_needed` status):
   - Treat this as the user approving the human verification checklist
   - Continue to update_roadmap step

3. If no active checkpoint or verification exists:
   - Output: "No active checkpoint to approve."

</process>
