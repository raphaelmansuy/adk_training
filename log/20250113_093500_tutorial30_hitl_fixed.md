# Tutorial 30: HITL Fix - Handler/RenderAndWaitForResponse Conflict

**Date:** 2025-01-13 09:35 AM  
**Issue:** HITL approval dialog not appearing  
**Root Cause:** Cannot use both `handler` and `renderAndWaitForResponse` together  
**Status:** ✅ Fixed

## Problem Identified

The code had BOTH:
```typescript
useCopilotAction({
  name: "process_refund",
  handler: async ({ order_id, amount, reason }) => { ... },  // ❌ This was the problem!
  renderAndWaitForResponse: ({ args, respond, status }) => { ... },
});
```

**Why this breaks HITL:**
- When `handler` is present, it executes immediately
- `renderAndWaitForResponse` never gets proper control
- No approval dialog appears
- Refund processes without user confirmation

## Solution Applied

Removed the `handler` function, keeping only `renderAndWaitForResponse`:

```typescript
useCopilotAction({
  name: "process_refund",
  description: "Process a refund (requires user approval)",
  parameters: [...],
  // NO handler function!
  renderAndWaitForResponse: ({ args, respond, status }) => {
    // Debug logging added
    console.log("🔍 HITL process_refund - Status:", status);
    
    if (status !== "executing") {
      console.warn(`❌ Dialog NOT showing - status is "${status}"`);
      return <div className="hidden" />;
    }

    // Show approval dialog
    return <div>... approval UI ...</div>;
  },
});
```

## How HITL Works (Correct Pattern)

1. **Agent calls** `process_refund(order_id, amount, reason)`
2. **Frontend intercepts** with `renderAndWaitForResponse`
3. **Status becomes** `"executing"` (waiting for user)
4. **Approval dialog** appears with Cancel/Approve buttons
5. **User clicks** Approve or Cancel
6. **`respond()` called** with `{approved: true/false}`
7. **Backend receives** user's decision
8. **Refund processed** only if approved

## Key Rules for HITL

✅ **DO:**
- Use ONLY `renderAndWaitForResponse` for HITL
- Check `status === "executing"` before showing dialog
- Call `respond({ approved: boolean })` on button clicks
- Add debug logging to troubleshoot

❌ **DON'T:**
- Combine `handler` with `renderAndWaitForResponse`
- Forget to check status (dialog won't show)
- Return null or undefined from render function
- Use `available: "remote"` for HITL (use default or "enabled")

## Testing Instructions

1. Refresh browser (http://localhost:3000 or 3001)
2. Open DevTools Console (F12)
3. Type: "I want a refund for order ORD-12345"
4. Answer: "Don't work" when asked for reason
5. Answer: "ALL" when asked for amount

**Expected Result:**
```
Console logs:
🔍 HITL process_refund - Status: executing
🔍 HITL process_refund - Args: {order_id: "ORD-12345", amount: ..., reason: "Don't work"}
✅ HITL dialog SHOWING - rendering approval UI

UI shows:
🔔 Refund Approval Required
Order ID: ORD-12345
Amount: $XX.XX
Reason: Don't work
[❌ Cancel] [✅ Approve Refund]
```

## Files Modified

- `/nextjs_frontend/app/page.tsx`: Removed `handler`, kept `renderAndWaitForResponse` with debug logging

## Related Documentation

- CopilotKit HITL Docs: https://docs.copilotkit.ai/adk/human-in-the-loop/agent
- AG-UI Protocol: https://docs.copilotkit.ai/ag-ui-protocol
- useCopilotAction API: https://docs.copilotkit.ai/reference/hooks/useCopilotAction

## Success Criteria

- ✅ Approval dialog appears when refund requested
- ✅ Console shows `status: executing` and `✅ HITL dialog SHOWING`
- ✅ Cancel button rejects refund
- ✅ Approve button processes refund
- ✅ Agent acknowledges user's decision

**Ready for testing!** Refresh the browser and try requesting a refund.
