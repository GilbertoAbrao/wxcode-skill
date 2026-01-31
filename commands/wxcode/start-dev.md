---
name: wxcode:start-dev
description: Execute start-dev.sh to start development server(s)
allowed-tools:
  - Read
  - Bash
---

<objective>

Execute the project's `start-dev.sh` script to start development server(s).

If the script doesn't exist, guides the user to create it first.

</objective>

<process>

## Phase 1: Check Script Exists

```bash
if [ -f "start-dev.sh" ]; then
  echo "SCRIPT_EXISTS"
else
  echo "SCRIPT_MISSING"
fi
```

**If script missing:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► START-DEV
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✗ start-dev.sh not found

Run /wxcode:create-start-dev to generate the script first.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Exit.

## Phase 2: Extract Configuration

Read the script to extract port info for display:

```bash
# Get project name
PROJECT_NAME=$(basename "$(pwd)")

# Extract ports from script
PORT_BACKEND=$(grep -E "^PORT_BACKEND=|^PORT=" start-dev.sh | head -1 | grep -o '[0-9]\+')
PORT_FRONTEND=$(grep "^PORT_FRONTEND=" start-dev.sh | grep -o '[0-9]\+')

# Check for existing processes
BACKEND_PID=$(cat /tmp/${PROJECT_NAME}-backend.pid 2>/dev/null || cat /tmp/${PROJECT_NAME}.pid 2>/dev/null)
```

## Phase 3: Execute Script

```bash
./start-dev.sh
```

Wait briefly for startup:

```bash
sleep 2
```

## Phase 4: Verify Server Started

**4.1 Check process is running:**

```bash
PROJECT_NAME=$(basename "$(pwd)")

# Check PID file exists and process is running
if [ -f "/tmp/${PROJECT_NAME}.pid" ]; then
  PID=$(cat /tmp/${PROJECT_NAME}.pid)
  if ps -p $PID > /dev/null 2>&1; then
    echo "SERVER_RUNNING"
  else
    echo "SERVER_FAILED"
  fi
elif [ -f "/tmp/${PROJECT_NAME}-backend.pid" ]; then
  PID=$(cat /tmp/${PROJECT_NAME}-backend.pid)
  if ps -p $PID > /dev/null 2>&1; then
    echo "SERVER_RUNNING"
  else
    echo "SERVER_FAILED"
  fi
else
  echo "NO_PID_FILE"
fi
```

**4.2 Check HTTP response (optional):**

```bash
# Quick health check
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT_BACKEND/ 2>/dev/null || echo "000")
```

## Phase 5: Display Result

**If server started successfully:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► START-DEV
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Development server started

## Server Info

| Property | Value |
|----------|-------|
| Project | [PROJECT_NAME] |
| PID | [PID] |
| Log File | /tmp/[PROJECT_NAME].log |

## Access URLs

[For single-server:]
→ http://localhost:[PORT_BACKEND]

[For SPA:]
→ http://localhost:[PORT_FRONTEND] (frontend)
→ http://localhost:[PORT_BACKEND] (API)

## Commands

tail -f /tmp/[PROJECT_NAME].log    # Watch logs
kill $(cat /tmp/[PROJECT_NAME].pid) # Stop server

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If server failed:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WXCODE ► START-DEV
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✗ Server failed to start

## Debug

Check the log file for errors:

cat /tmp/[PROJECT_NAME].log

## Common Issues

- Missing dependencies (run pip install or npm install)
- Port already in use (script should auto-kill, but check manually)
- Missing __init__.py files (Python packages)
- Wrong module paths in entry point

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</process>

<output>

Executes start-dev.sh and displays server status with access URLs.

</output>

<success_criteria>

- [ ] Script existence verified
- [ ] Script executed successfully
- [ ] Server process running
- [ ] Access URLs displayed
- [ ] Log file location shown

</success_criteria>
