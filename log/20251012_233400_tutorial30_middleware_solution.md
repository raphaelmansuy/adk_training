# Tutorial 30: Middleware Solution for CopilotKit Message ID Issue

**Date**: 2025-10-12  
**Time**: 23:34 UTC  
**Solution**: Custom FastAPI middleware to inject message IDs  
**Status**: 🔧 Implementation Ready

## Research Findings

### AG-UI Protocol Requirements (Source Code Analysis)

From `research/ag-ui/python-sdk/ag_ui/core/types.py`:

```python
class BaseMessage(ConfiguredBaseModel):
    """A base message, modelled after OpenAI messages."""
    id: str              # ← REQUIRED
    role: str
    content: Optional[str] = None
    name: Optional[str] = None

class UserMessage(BaseMessage):
    """A user message."""
    role: Literal["user"] = "user"
    content: str
    # Inherits required `id` field from BaseMessage
```

**Conclusion**: AG-UI protocol REQUIRES all messages to have an `id` field.

### CopilotKit Behavior

**All Versions Tested** (1.10.6, 1.9.3):
- Send messages with: `{role: "user", content: "..."}`  
- Do NOT send: `id` field
- This is consistent across versions

**Root Cause**: CopilotKit follows OpenAI message format (no IDs), but AG-UI extends it to require IDs for message tracking.

### Package Versions

```
ag-ui-adk: 0.3.1 (latest) ✅
ag-ui: (bundled with ag-ui-adk)
CopilotKit: 1.9.3 (tested), 1.10.6 (tested)
google-adk: 1.16.0
```

## Middleware Solution

### Approach

Intercept POST requests to `/api/copilotkit` and inject message IDs before FastAPI validation.

### Implementation

**File**: `tutorial_implementation/tutorial30/agent/agent.py`

Add this middleware before the `add_adk_fastapi_endpoint` call:

```python
import json
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class MessageIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject message IDs for CopilotKit compatibility.
    
    CopilotKit sends messages without IDs, but AG-UI protocol requires them.
    This middleware adds UUIDs to any messages missing the 'id' field.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Only process POST requests to /api/copilotkit
        if request.method == "POST" and request.url.path == "/api/copilotkit":
            # Read the request body
            body = await request.body()
            
            try:
                # Parse JSON
                data = json.loads(body)
                
                # Inject IDs into messages if missing
                if "messages" in data and isinstance(data["messages"], list):
                    for msg in data["messages"]:
                        if isinstance(msg, dict) and "id" not in msg:
                            # Generate unique ID
                            msg["id"] = f"msg-{uuid.uuid4()}"
                    
                    # Create new request with modified body
                    modified_body = json.dumps(data).encode()
                    
                    # Replace the request body
                    async def receive():
                        return {"type": "http.request", "body": modified_body}
                    
                    request._receive = receive
            
            except (json.JSONDecodeError, Exception) as e:
                # If parsing fails, pass through original request
                pass
        
        # Continue with the request
        response = await call_next(request)
        return response

# Add middleware to FastAPI app
app.add_middleware(MessageIDMiddleware)
```

### Integration Point

Insert the middleware BEFORE this line in `agent.py`:

```python
# Add ADK endpoint for CopilotKit
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")
```

Should become:

```python
# Add middleware to inject message IDs for CopilotKit compatibility
app.add_middleware(MessageIDMiddleware)

# Add ADK endpoint for CopilotKit
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")
```

## Expected Results

### Before Middleware
```
POST /api/copilotkit
Request: {"messages": [{"role": "user", "content": "Hello"}], ...}
Response: 422 Unprocessable Entity
Error: Field 'id' required in messages[0]
```

### After Middleware
```
POST /api/copilotkit
Original Request: {"messages": [{"role": "user", "content": "Hello"}], ...}
Modified Request: {"messages": [{"id": "msg-abc123", "role": "user", "content": "Hello"}], ...}
Response: 200 OK (SSE stream)
```

## Testing Plan

### Step 1: Implement Middleware
1. Stop current servers (Ctrl+C)
2. Edit `agent/agent.py`
3. Add `MessageIDMiddleware` class
4. Add `app.add_middleware(MessageIDMiddleware)`

### Step 2: Restart and Test
```bash
cd tutorial_implementation/tutorial30
make dev
```

### Step 3: Verify in Browser
1. Open http://localhost:3000
2. Open DevTools → Console and Network tabs
3. Send message: "What is your refund policy?"
4. Check Network tab:
   - Should see 200 OK (not 422)
   - Should see streaming response
   - "[Network] Unknown error" should disappear

### Step 4: Backend Logs
Watch for:
```
INFO: POST /api/copilotkit
INFO: Streaming response started
Tool called: search_knowledge_base
```

## Advantages of This Solution

✅ **No Version Pinning**: Works with any CopilotKit version  
✅ **Protocol Compliant**: Maintains AG-UI protocol requirements  
✅ **Transparent**: CopilotKit doesn't need to know about IDs  
✅ **Production Ready**: Can be used in deployed applications  
✅ **Maintainable**: Clear, documented middleware pattern  

## Alternative Solutions Comparison

| Solution | Pros | Cons | Status |
|----------|------|------|--------|
| **Downgrade CopilotKit** | Simple | Doesn't work (all versions lack IDs) | ❌ Failed |
| **Wait for ag-ui-adk update** | Official fix | Unknown timeline | 🟡 Waiting |
| **Middleware (This)** | Works now, any version | Requires code change | ✅ Recommended |
| **Fork ag-ui-adk** | Full control | Maintenance burden | ⚠️ Last resort |

## Implementation Files

### Before
```
tutorial30/
└── agent/
    └── agent.py (227 lines)
```

### After
```
tutorial30/
└── agent/
    └── agent.py (258 lines) ← +31 lines for middleware
```

## Next Steps

1. ✅ Research complete - identified root cause
2. 🔧 Implement middleware in agent.py
3. 🧪 Test with CopilotKit
4. 📝 Update documentation if successful
5. 🎉 Tutorial 30 working end-to-end

---

**Status**: Ready to implement middleware solution  
**Expected Resolution Time**: 5-10 minutes
