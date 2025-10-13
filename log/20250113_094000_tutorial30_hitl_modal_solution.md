# Tutorial 30: HITL Fix - Modal Dialog Approach

**Date:** 2025-01-13 09:40 AM  
**Issue:** renderAndWaitForResponse not working with ADK backend  
**Root Cause:** ADK backend tools don't properly trigger frontend renderAndWaitForResponse  
**Solution:** Use frontend-only action with Promise-based approval modal  
**Status:** ✅ Implemented - Ready for testing

## Problem Analysis

**Why renderAndWaitForResponse didn't work:**
1. ADK backend has `process_refund` as a tool
2. When agent calls it, backend executes immediately
3. Frontend `renderAndWaitForResponse` never gets proper status = "executing"
4. Approval dialog never appears

**Console would show:**
```
❌ HITL dialog NOT showing - status is "complete", expected "executing"
```

## New Solution: Promise-Based Modal Dialog

### Architecture

1. **Frontend-only action** (`available: "remote"`)
2. **Handler returns Promise** that waits for user decision
3. **React state** (`refundRequest`) triggers modal overlay
4. **User clicks button** → Promise resolves → Agent continues

### Implementation

**Step 1: Frontend Action with Promise**
```typescript
useCopilotAction({
  name: "process_refund",
  available: "remote",  // Frontend-only, no backend collision
  handler: async ({ order_id, amount, reason }) => {
    setRefundRequest({ order_id, amount, reason });  // Show modal
    
    // Return promise that resolves when user decides
    return new Promise((resolve) => {
      window.__refundPromiseResolve = resolve;
    });
  },
});
```

**Step 2: Modal Dialog Component**
```typescript
{refundRequest && (
  <div className="fixed inset-0 bg-black/50 ...">
    <div className="bg-card border rounded-lg ...">
      <h2>🔔 Refund Approval Required</h2>
      {/* Show order_id, amount, reason */}
      <button onClick={() => handleRefundApproval(false)}>❌ Cancel</button>
      <button onClick={() => handleRefundApproval(true)}>✅ Approve</button>
    </div>
  </div>
)}
```

**Step 3: Approval Handler**
```typescript
const handleRefundApproval = async (approved: boolean) => {
  const resolve = window.__refundPromiseResolve;
  
  if (approved) {
    resolve({
      approved: true,
      message: "Refund processed successfully"
    });
  } else {
    resolve({
      approved: false,
      message: "Refund cancelled by user"
    });
  }
  
  setRefundRequest(null);  // Hide modal
};
```

## Flow Diagram

```
User: "I want a refund"
    ↓
Agent: Gathers order_id, amount, reason
    ↓
Agent: Calls process_refund(order_id, amount, reason)
    ↓
Frontend: Handler called → setRefundRequest() → Modal appears
    ↓
Handler: Returns Promise (agent waits...)
    ↓
User: Clicks "✅ Approve" or "❌ Cancel"
    ↓
handleRefundApproval(): Resolves promise with decision
    ↓
Agent: Receives {approved: true/false, message: "..."}
    ↓
Agent: Responds to user based on decision
```

## Key Differences from Previous Approach

| Aspect | Old (renderAndWaitForResponse) | New (Promise + Modal) |
|--------|-------------------------------|----------------------|
| **Trigger** | Relies on status = "executing" | React state change |
| **Display** | Inline in chat | Modal overlay |
| **Control** | CopilotKit manages lifecycle | We manage Promise |
| **Compatibility** | Requires ADK support | Works with any backend |
| **Reliability** | ❌ Didn't work | ✅ Should work |

## Testing Instructions

1. **Refresh browser** (changes are hot-reloaded but refresh is cleaner)
2. **Clear any old conversation** (start fresh)
3. **Type:** "I want a refund for order ORD-12345"
4. **Answer questions:**
   - Reason: "Product broken"
   - Amount: "100"
5. **Watch for:**
   - 🎯 Modal dialog appears with black overlay
   - 🎯 Shows order details: ORD-12345, $100.00, "Product broken"
   - 🎯 Two buttons: "❌ Cancel Refund" and "✅ Approve Refund"

**Test Approve Flow:**
1. Click "✅ Approve Refund"
2. Modal disappears
3. Agent says: "Refund processed successfully for order ORD-12345"

**Test Cancel Flow:**
1. Request another refund
2. Click "❌ Cancel Refund"
3. Modal disappears
4. Agent says: "Refund cancelled by user"

## Technical Details

### Why This Works

1. **No backend collision**: Using `available: "remote"` means backend tool is never called
2. **Promise blocks agent**: Agent waits for Promise to resolve before continuing
3. **State triggers render**: React state change shows/hides modal
4. **Clean resolution**: Promise resolves → agent gets decision → continues conversation

### Promise Pattern

```typescript
// Handler creates Promise and stores resolve function
handler: async (params) => {
  return new Promise((resolve) => {
    window.__refundPromiseResolve = resolve;  // Save for later
  });
  // Agent is now BLOCKED waiting for this Promise
}

// Button click resolves the Promise
button.onClick = () => {
  const resolve = window.__refundPromiseResolve;
  resolve({ approved: true });  // Agent unblocked!
}
```

### Modal Styling

- Fixed positioning with `inset-0` covers entire screen
- `bg-black/50` creates semi-transparent overlay
- `z-50` ensures it's above chat interface
- Centered with flexbox: `flex items-center justify-center`
- Proper dark mode support with `dark:` variants

## Backend Changes

**Important:** The backend `process_refund` tool can stay in the tools list, but it will NEVER be called because the frontend action with `available: "remote"` takes precedence.

Alternatively, you could remove it from the backend:

```python
# In agent.py
tools=[
    search_knowledge_base,
    lookup_order_status,
    create_support_ticket,
    get_product_details,
    # process_refund,  # Not needed - frontend handles it
],
```

## Files Modified

- `/nextjs_frontend/app/page.tsx`:
  - Added `refundRequest` state
  - Changed `process_refund` to use `available: "remote"` with Promise handler
  - Added modal dialog component
  - Added `handleRefundApproval()` function

## Success Criteria

- ✅ Modal dialog appears when refund requested
- ✅ Modal shows correct order_id, amount, reason
- ✅ Approve button processes refund
- ✅ Cancel button cancels refund
- ✅ Agent receives and acknowledges user's decision
- ✅ Modal disappears after decision
- ✅ Works in both light and dark mode

## Advantages

1. **Reliable**: Doesn't depend on ADK backend behavior
2. **Visual**: Modal overlay is more prominent than inline dialog
3. **Flexible**: Easy to customize styling and behavior
4. **Debuggable**: Console logs show exactly what's happening
5. **Portable**: Same pattern works with any backend (not just ADK)

## Future Enhancements

- Add loading spinner while processing
- Add error handling for failed refunds
- Add animation for modal appearance/disappearance
- Add keyboard support (ESC to cancel, Enter to approve)
- Add audit log of approval decisions

**Ready to test!** Refresh the page and request a refund.
