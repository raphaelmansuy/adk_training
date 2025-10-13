# Tutorial 30: HITL Debugging - Testing Instructions

**Date:** 2025-01-13 09:30 AM  
**Status:** 🧪 Ready for testing with debug logs  
**Changes Applied:** Added console logging to diagnose HITL status

## Changes Made

### 1. Frontend Debug Logging (`app/page.tsx`)

Added comprehensive logging to `renderAndWaitForResponse`:

```typescript
renderAndWaitForResponse: ({ args, respond, status }) => {
  // Debug logging
  console.log("🔍 HITL process_refund - Status:", status);
  console.log("🔍 HITL process_refund - Args:", args);
  console.log("🔍 HITL process_refund - Respond function:", typeof respond);
  
  if (status !== "executing") {
    console.warn(`❌ HITL dialog NOT showing - status is "${status}", expected "executing"`);
    return <div className="hidden" />;
  }

  console.log("✅ HITL dialog SHOWING - rendering approval UI");
  // ... dialog code
}
```

### 2. Backend Tool Configuration (`agent.py`)

Confirmed `process_refund` is in backend tools list:

```python
tools=[
    search_knowledge_base,
    lookup_order_status,
    create_support_ticket,
    get_product_details,
    process_refund,  # Backend tool that frontend will intercept with HITL
],
```

## Testing Steps

### Test 1: Trigger HITL Flow

1. **Open browser** at http://localhost:3000 or http://localhost:3001
2. **Open DevTools Console** (F12 → Console tab)
3. **Clear console** to see only new messages
4. **Type in chat:** "I want a refund for order ORD-12345"
5. **Agent will ask:** "What is the reason for the refund? Also, how much of a refund are you requesting?"
6. **Respond:** "Don't work" (or similar reason)
7. **Watch console for logs:**

**Expected Console Output (if HITL working):**
```
🔍 HITL process_refund - Status: executing
🔍 HITL process_refund - Args: {order_id: "ORD-12345", amount: ..., reason: "Don't work"}
🔍 HITL process_refund - Respond function: function
✅ HITL dialog SHOWING - rendering approval UI
```

**Expected Console Output (if HITL NOT working):**
```
🔍 HITL process_refund - Status: complete (or inProgress)
🔍 HITL process_refund - Args: {order_id: "ORD-12345", ...}
🔍 HITL process_refund - Respond function: function (or undefined)
❌ HITL dialog NOT showing - status is "complete", expected "executing"
```

### Test 2: Check Network Activity

1. **Open DevTools Network tab**
2. **Filter:** `copilotkit`
3. **Trigger refund flow** (steps from Test 1)
4. **Find:** `POST /api/copilotkit` requests
5. **Inspect payload:**
   - Look for `"name": "process_refund"` in tool_calls
   - Check if there's a `"status"` field
   - Look for any `"wait_for_response"` or similar flags

### Test 3: Check Backend Logs

Watch the backend terminal for:
- `process_refund` function calls
- AG-UI protocol messages
- Any mentions of frontend actions
- Errors or warnings

## Diagnostic Questions

Based on console logs, answer these:

### Q1: What status value appears in the console?
- [ ] "executing" (expected for HITL)
- [ ] "complete" (tool already finished)
- [ ] "inProgress" (tool is running)
- [ ] Other: ______________

### Q2: Is the respond function available?
- [ ] Yes, typeof is "function"
- [ ] No, typeof is "undefined"

### Q3: When does the log appear?
- [ ] Before refund is processed (good - can intercept)
- [ ] After refund is processed (bad - too late)
- [ ] Never (bad - action not being called)

### Q4: What does the agent say?
- [ ] "Please confirm the refund" (waiting for approval)
- [ ] "The refund has been processed" (already done)
- [ ] Something else: ______________

## Possible Outcomes

### Outcome A: Status is "complete"
**Meaning:** Backend tool executes immediately, frontend action never gets control.

**Root cause:** AG-UI protocol is NOT intercepting backend tool for HITL.

**Solutions:**
1. Remove backend tool, use frontend-only action with `available: "remote"`
2. Use official ADK HITL pattern with TOOL_REFERENCE and returns schema
3. Check CopilotKit version compatibility

### Outcome B: Status is "executing" but dialog doesn't show
**Meaning:** renderAndWaitForResponse is called but React not rendering.

**Root cause:** Rendering issue, possibly with hidden class or conditional logic.

**Solutions:**
1. Remove `className="hidden"` from status check
2. Add `render` function separately (not just renderAndWaitForResponse)
3. Check React DevTools to see if component exists in DOM

### Outcome C: Logs never appear
**Meaning:** Frontend action not being registered or called.

**Root cause:** Action not discovered by AG-UI protocol.

**Solutions:**
1. Check agent name matches: `agent="customer_support_agent"`
2. Verify CopilotKit runtimeUrl: `/api/copilotkit`
3. Check browser console for CopilotKit errors
4. Verify AG-UI middleware is working

## Next Steps Based on Results

**If status !== "executing":**
→ Follow "Solution A: Remove Backend Tool" from debugging doc
→ Make process_refund frontend-only with `available: "remote"`

**If status === "executing" but no dialog:**
→ Check React component rendering
→ Try simpler dialog without conditional hidden class

**If logs never appear:**
→ Check CopilotKit setup and agent connection
→ Verify AG-UI protocol is discovering frontend actions

## Files to Share

If asking for help, share:
1. Console logs (screenshots or text)
2. Network tab request/response for process_refund
3. Backend terminal logs during refund attempt
4. React DevTools component tree (if dialog should exist but doesn't render)

## Testing Completed?

- [ ] Test 1: Console logs captured
- [ ] Test 2: Network activity inspected
- [ ] Test 3: Backend logs reviewed
- [ ] Diagnostic questions answered
- [ ] Outcome identified (A, B, or C)
- [ ] Next steps determined

---

**Report findings in this format:**

```
STATUS: [executing|complete|inProgress|other]
RESPOND: [function|undefined]
TIMING: [before|after|never]
AGENT_SAYS: [brief quote]
CONCLUSION: [Outcome A|B|C]
RECOMMENDED_FIX: [solution number from debugging doc]
```
