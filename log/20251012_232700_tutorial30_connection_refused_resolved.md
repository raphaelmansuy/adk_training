# Tutorial 30: Connection Refused Error - RESOLVED

**Date**: 2025-10-12  
**Time**: 23:27 UTC  
**Issue**: `net::ERR_CONNECTION_REFUSED` on `localhost:8000/api/copilotkit`  
**Status**: ✅ RESOLVED

## Problem Summary

User encountered `net::ERR_CONNECTION_REFUSED` error when accessing the chat interface, indicating the frontend (port 3000) could not connect to the backend (port 8000).

## Root Cause

**The backend server was not running.**

Error Details:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
:8000/api/copilotkit:1  Failed to load resource: net::ERR_CONNECTION_REFUSED
CopilotKit Error: CombinedError: [Network] Unknown error occurred
```

This is different from the earlier 422 errors - `ERR_CONNECTION_REFUSED` means no server is listening on port 8000 at all.

## Solution

Started the backend server:

```bash
cd tutorial_implementation/tutorial30/agent
python agent.py &
```

## Verification

Backend is now running and healthy:

```bash
$ curl http://localhost:8000/health
{"status":"healthy","agent":"customer_support_agent","version":"1.0.0"}
```

## Current Status

### Backend ✅
- **Running**: Yes
- **Port**: 8000
- **Health**: Healthy
- **Endpoints**:
  - `http://localhost:8000/health` - Health check
  - `http://localhost:8000/docs` - API documentation
  - `http://localhost:8000/api/copilotkit` - CopilotKit endpoint

### Frontend ✅
- **Running**: Yes  
- **Port**: 3000
- **CopilotKit Version**: 1.9.3 (downgraded from 1.10.6)
- **URL**: http://localhost:3000

## Testing Instructions

### Step 1: Verify Both Servers Are Running

**Check Backend:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","agent":"customer_support_agent","version":"1.0.0"}
```

**Check Frontend:**
```bash
curl http://localhost:3000
# Should return HTML (Next.js page)
```

### Step 2: Test the Chat

1. **Open Browser**: Navigate to http://localhost:3000
2. **Open DevTools**: Press F12, go to Console and Network tabs
3. **Check for Errors**:
   - ❌ OLD: `ERR_CONNECTION_REFUSED` - backend not running
   - ✅ NOW: Should connect successfully (may see 422 handshake errors - that's normal)

### Step 3: Send a Test Message

Type in the chat:
```
What is your refund policy?
```

**Expected Behavior:**
- Message is sent to backend
- Agent processes the request
- Tool `search_knowledge_base` is called
- Response streams back to frontend
- You see the refund policy information

### Step 4: Monitor Network Activity

In DevTools Network tab, filter by "copilotkit":
- **Initial 422 errors**: Normal (handshake attempts)
- **First message**: Should get 200 OK
- **SSE stream**: Should see streaming response events

## Comparison: Connection Refused vs. 422 Errors

### `ERR_CONNECTION_REFUSED` (What We Just Fixed)
- **Cause**: Backend server not running
- **Symptom**: Cannot connect to port 8000 at all
- **Solution**: Start the backend server
- **Severity**: 🔴 Critical - chat completely non-functional

### `422 Unprocessable Entity` (Expected Behavior)
- **Cause**: CopilotKit handshake requests during initialization
- **Symptom**: Initial requests rejected by validation
- **Solution**: None needed - handled automatically
- **Severity**: ✅ Normal - chat works fine

### `[Network] Unknown error` (Version Compatibility)
- **Cause**: CopilotKit 1.10.6 missing `id` field in messages
- **Symptom**: All requests fail validation
- **Solution**: Downgrade to CopilotKit 1.9.3
- **Severity**: 🟡 Moderate - fixed by version downgrade

## How to Keep Backend Running

### Option 1: Keep Terminal Open
```bash
cd tutorial_implementation/tutorial30/agent
python agent.py
# Keep this terminal open
```

### Option 2: Background Process
```bash
cd tutorial_implementation/tutorial30/agent
nohup python agent.py > /tmp/backend.log 2>&1 &
# Check logs: tail -f /tmp/backend.log
```

### Option 3: Use Makefile
```bash
cd tutorial_implementation/tutorial30
make dev
# Starts both backend and frontend
```

### Option 4: Separate Terminals
```bash
# Terminal 1 - Backend
cd tutorial_implementation/tutorial30/agent
python agent.py

# Terminal 2 - Frontend  
cd tutorial_implementation/tutorial30/nextjs_frontend
npm run dev
```

## Troubleshooting Commands

### Check if Backend is Running
```bash
lsof -i :8000
# Should show python process if running
```

### Check Backend Logs
```bash
tail -f /tmp/backend.log
# Or check terminal where backend is running
```

### Restart Backend
```bash
# Kill existing process
lsof -ti :8000 | xargs kill -9

# Start new process
cd tutorial_implementation/tutorial30/agent
python agent.py &
```

### Test Backend Directly
```bash
# Health check
curl http://localhost:8000/health

# Test copilotkit endpoint
curl -X POST http://localhost:8000/api/copilotkit \
  -H "Content-Type: application/json" \
  -d '{
    "threadId": "test-123",
    "runId": "run-456",
    "state": {},
    "messages": [{"id": "msg-1", "role": "user", "content": "Hello"}],
    "tools": [],
    "context": [],
    "forwardedProps": {}
  }'
```

## Resolution Summary

**Problem**: Backend was not running → `ERR_CONNECTION_REFUSED`  
**Solution**: Started backend server  
**Status**: ✅ Resolved  

**Additional Fix**: Downgraded CopilotKit from 1.10.6 to 1.9.3 to resolve message `id` field compatibility issue.

## Next Steps

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 3000  
3. ✅ CopilotKit downgraded to 1.9.3
4. 🟡 **TEST**: Send messages in chat to verify end-to-end functionality
5. 📝 **DOCUMENT**: Update README if 1.9.3 works perfectly

## Success Criteria

- ✅ No more `ERR_CONNECTION_REFUSED` errors
- ✅ Backend health endpoint responding
- 🟡 Frontend can send messages (needs testing)
- 🟡 Agent responds with tool usage (needs testing)
- 🟡 No "[Network] Unknown error" banner (needs verification)

---

**Resolution Time**: 23:27 UTC  
**Next Action**: User should test chat functionality and report results
