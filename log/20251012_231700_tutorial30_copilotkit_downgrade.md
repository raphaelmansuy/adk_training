# Tutorial 30: CopilotKit Downgrade to Fix Network Error

**Date**: 2025-10-12  
**Time**: 23:16 UTC  
**Action**: Downgraded CopilotKit from 1.10.6 to 1.9.3  
**Status**: 🟡 Testing required

## What Was Done

### Problem
"[Network] Unknown error occurred" caused by CopilotKit 1.10.6 not sending required `id` field in messages.

### Solution
Downgraded to CopilotKit 1.9.3 (last stable version before 1.10.x series).

### Commands Executed

```bash
cd tutorial_implementation/tutorial30/nextjs_frontend
npm install @copilotkit/react-core@1.9.3 @copilotkit/react-ui@1.9.3
```

### Version Change

**Before:**
```
@copilotkit/react-core: 1.10.6
@copilotkit/react-ui: 1.10.6
```

**After:**
```
@copilotkit/react-core: 1.9.3
@copilotkit/react-ui: 1.9.3
```

## Testing Instructions

### Step 1: Ensure Both Servers Are Running

**Backend:**
```bash
# Terminal 1
cd tutorial_implementation/tutorial30
source agent/.env
python -m agent.agent
```

Should show:
```
============================================================
🤖 Customer Support Agent API
============================================================
🌐 Server: http://0.0.0.0:8000
📚 Docs: http://0.0.0.0:8000/docs
💬 CopilotKit: http://0.0.0.0:8000/api/copilotkit
============================================================
```

**Frontend:**
```bash
# Terminal 2
cd tutorial_implementation/tutorial30/nextjs_frontend
npm run dev
```

Should show:
```
▲ Next.js 15.5.4
- Local:        http://localhost:3000
✓ Ready in 1422ms
```

### Step 2: Test the Chat Interface

1. **Open Browser**
   - Navigate to http://localhost:3000
   - Open DevTools (F12)
   - Go to Console tab

2. **Check for Errors**
   - **OLD BEHAVIOR**: "[Network] Unknown error occurred" banner
   - **EXPECTED NEW BEHAVIOR**: No network error banner

3. **Send Test Messages**

Try these prompts:

**Knowledge Base Test:**
```
What is your refund policy?
```

Expected: Agent responds with refund policy details from knowledge base

**Order Lookup Test:**
```
Check order status for ORD-12345
```

Expected: Agent responds with order details (shipped, tracking number, etc.)

**Ticket Creation Test:**
```
My product stopped working after 2 months
```

Expected: Agent creates support ticket and provides ticket number

### Step 3: Monitor Network Tab

1. Open DevTools → Network tab
2. Filter by "copilotkit"
3. Send a message
4. Check responses:
   - **Initial 422 errors**: Still expected (handshake)
   - **After first message**: Should see 200 OK
   - **Streaming responses**: Should see SSE events

### Step 4: Verify Tools Are Called

Check backend terminal logs for:
```
Tool called: search_knowledge_base
Tool called: lookup_order_status
Tool called: create_support_ticket
```

## Expected Results

### ✅ Success Indicators

1. **No "[Network] Unknown error" banner**
2. **Chat accepts user input**
3. **Agent responds to messages**
4. **Tools are executed (visible in backend logs)**
5. **Responses stream in real-time**
6. **Network tab shows 200 OK after initial 422s**

### ❌ Failure Indicators

1. **Still seeing "[Network] Unknown error"**
   - Check browser console for validation errors
   - Verify CopilotKit version: `npm list @copilotkit/react-core`
   - May need to try even older version (1.8.x or 1.7.x)

2. **Different error messages**
   - Document the new error
   - Check backend logs for details
   - May indicate different compatibility issue

## If This Works ✅

### Update package.json

Pin the working version to prevent future upgrades:

```json
{
  "dependencies": {
    "@copilotkit/react-core": "1.9.3",
    "@copilotkit/react-ui": "1.9.3",
    ...
  }
}
```

### Update Documentation

1. **README.md**: Remove critical warning about network error
2. **TROUBLESHOOTING_422.md**: Update with working version info
3. **Implementation log**: Add note about version requirements

### Create Version Compatibility Note

```markdown
## Known Compatible Versions

✅ **Working Configuration:**
- CopilotKit: 1.9.3
- ag_ui_adk: 0.1.0
- Next.js: 15.5.4
- Python: 3.12
- google-adk: 1.16.0

❌ **Known Incompatible:**
- CopilotKit: 1.10.6+ (missing message ID field)
```

## If This Doesn't Work ❌

### Try Older Versions

**Option A: CopilotKit 1.8.x**
```bash
npm install @copilotkit/react-core@1.8.9 @copilotkit/react-ui@1.8.9
npm run dev
```

**Option B: CopilotKit 1.7.x**
```bash
npm install @copilotkit/react-core@1.7.1 @copilotkit/react-ui@1.7.1
npm run dev
```

**Option C: CopilotKit 1.5.x**
```bash
npm install @copilotkit/react-core@1.5.9 @copilotkit/react-ui@1.5.9
npm run dev
```

### Document Findings

Create a version compatibility matrix:

| CopilotKit | ag_ui_adk | Status | Notes |
|------------|-----------|--------|-------|
| 1.10.6 | 0.1.0 | ❌ | Missing message ID field |
| 1.9.3 | 0.1.0 | 🟡 | Testing... |
| 1.8.9 | 0.1.0 | 🟡 | Not tested |
| 1.7.1 | 0.1.0 | 🟡 | Not tested |

### Alternative Solution: Middleware

If no version works, we can implement a FastAPI middleware to inject message IDs:

```python
@app.middleware("http")
async def add_message_ids(request: Request, call_next):
    if request.url.path == "/api/copilotkit" and request.method == "POST":
        body = await request.body()
        data = json.loads(body)
        
        # Inject IDs if missing
        if "messages" in data:
            for i, msg in enumerate(data["messages"]):
                if "id" not in msg:
                    msg["id"] = f"msg-{uuid.uuid4()}"
        
        # Create new request with modified body
        # ... (implementation details)
    
    return await call_next(request)
```

## Rollback Instructions

If you need to go back to 1.10.6:

```bash
cd tutorial_implementation/tutorial30/nextjs_frontend
npm install @copilotkit/react-core@1.10.6 @copilotkit/react-ui@1.10.6
npm run dev
```

## Next Steps

1. **Test the chat interface** (see Step 2 above)
2. **Document results** in this file
3. **Update main documentation** if successful
4. **Share findings** with community

## Testing Results

**Date Tested**: _________  
**Tester**: _________  
**Result**: ⬜ Success ⬜ Failure ⬜ Partial

**Notes:**
```
[Your testing notes here]
```

**Network Error Banner**: ⬜ Gone ⬜ Still present  
**Chat Functionality**: ⬜ Working ⬜ Not working  
**Tools Executed**: ⬜ Yes ⬜ No  
**Recommended**: ⬜ Use this version ⬜ Try older version ⬜ Implement middleware

---

**Status**: 🟡 Awaiting test results
