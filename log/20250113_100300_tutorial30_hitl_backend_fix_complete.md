# Tutorial 30: HITL Backend Fix - Complete Solution

**Date:** 2025-01-13 10:03 AM  
**Issue:** Modal dialog not appearing because backend tool was intercepting refund requests  
**Root Cause:** Backend had `process_refund` in tools list, executing immediately before frontend could show dialog  
**Solution:** Removed `process_refund` from backend tools, making it frontend-only  
**Status:** ✅ Complete - Ready for testing

## Problem Discovery

**Console Evidence:**
```
HITL render - Status: complete Args: {reason: "Broken", amount: 100, order_id: 'ORD-12345'}
HITL render - Status: complete Args: {reason: "Broken", amount: 100, order_id: 'ORD-12345'}
... (repeated many times)
```

**What This Means:**
- The `render` function was being called repeatedly
- Status was immediately "complete" (never "executing" or "inProgress")
- The `handler` function was NEVER called (no "🔍 HITL handler called with:" logs)
- This means the backend tool processed the refund before frontend could intercept

## Root Cause Analysis

### The Flow When It Was Broken:

```
User: "I want a refund for ORD-12345"
    ↓
Agent: Gathers order_id, amount, reason
    ↓
Agent: Sees process_refund() in tools list
    ↓
Backend: Executes process_refund() immediately ❌
    ↓
Frontend: Receives completed action (status="complete")
    ↓
Frontend: render() called but handler() never invoked
    ↓
Result: No approval dialog, refund already processed
```

### Why Backend Tool Had Priority:

1. Agent sees `process_refund` as a backend tool (in agent.py tools list)
2. AG-UI protocol routes tool calls to backend first
3. Backend executes and returns result
4. Frontend action with `available: "remote"` is bypassed
5. Frontend only gets notified AFTER execution (status="complete")

## The Fix

### File: `/tutorial_implementation/tutorial30/agent/agent.py`

**Before (lines 344-350):**
```python
tools=[
    search_knowledge_base,
    lookup_order_status,
    create_support_ticket,
    get_product_details,
    process_refund,  # ❌ Backend tool - executes immediately
],
```

**After (lines 344-351):**
```python
tools=[
    search_knowledge_base,
    lookup_order_status,
    create_support_ticket,
    get_product_details,
    # Note: process_refund is ONLY available as a frontend action (not backend tool)
    # This ensures the HITL approval dialog is shown before processing
],
```

### Why This Works:

1. **No Backend Tool**: Agent can't execute `process_refund` on backend
2. **Frontend Discovery**: CopilotKit sends frontend actions to backend via `tools` array in API request
3. **Frontend Execution**: When agent calls `process_refund()`, frontend handler is invoked
4. **Approval Flow**: Handler sets state → Modal shows → User decides → Promise resolves → Agent continues

## The Correct Flow (After Fix)

```
User: "I want a refund for ORD-12345"
    ↓
Agent: Gathers order_id, amount, reason
    ↓
Agent: Calls process_refund(order_id, amount, reason)
    ↓
Frontend: Handler invoked ✅
    ↓
Frontend: setRefundRequest({order_id, amount, reason})
    ↓
Frontend: Modal dialog appears 🎯
    ↓
Frontend: Returns unresolved Promise (agent waits...)
    ↓
User: Clicks "✅ Approve" or "❌ Cancel"
    ↓
Frontend: Resolves Promise with decision
    ↓
Agent: Receives {approved: true/false, message: "..."}
    ↓
Agent: Responds to user based on decision
```

## Frontend Implementation Details

### Modal Dialog Component (`page.tsx` lines 183-233)

**Key Features:**
- Fixed positioning with backdrop: `fixed inset-0 bg-black/50`
- Z-index 50 ensures it's above chat interface
- Shows order details: order_id, amount (formatted), reason
- Two prominent buttons: Cancel (red) and Approve (green)
- Conditional rendering: `{refundRequest && (...)}`

### Handler Function (`page.tsx` lines 109-119)

```typescript
handler: async ({ order_id, amount, reason }) => {
  console.log("🔍 HITL handler called with:", { order_id, amount, reason });
  
  // Store the refund request to show in the dialog
  setRefundRequest({ order_id, amount, reason });
  
  // Return a promise that resolves when user approves/cancels
  return new Promise((resolve) => {
    (window as any).__refundPromiseResolve = resolve;
  });
}
```

**Critical Points:**
- Handler sets state to trigger modal rendering
- Returns Promise immediately (blocks agent)
- Promise resolver stored in window global for button access
- Console log confirms handler invocation

### Approval Handler (`page.tsx` lines 145-174)

```typescript
const handleRefundApproval = async (approved: boolean) => {
  console.log("🔍 User decision:", approved ? "APPROVED" : "CANCELLED");
  
  const resolve = (window as any).__refundPromiseResolve;
  if (resolve && refundRequest) {
    if (approved) {
      // Could call backend API here for actual processing
      resolve({
        approved: true,
        message: `Refund processed successfully for order ${refundRequest.order_id}`
      });
    } else {
      resolve({
        approved: false,
        message: "Refund cancelled by user"
      });
    }
  }
  
  setRefundRequest(null);  // Hide modal
  delete (window as any).__refundPromiseResolve;  // Cleanup
};
```

**Flow:**
1. User clicks button
2. Function logs decision
3. Retrieves Promise resolver from window
4. Resolves with approved/cancelled message
5. Clears state (hides modal)
6. Cleans up global resolver

## Testing Instructions

### 1. Clear Browser State
- Open http://localhost:3001
- Open DevTools Console (F12 → Console tab)
- Clear any previous conversation (refresh if needed)

### 2. Request a Refund
Type in chat:
```
I want a refund for order ORD-12345
```

### 3. Provide Details
Agent will ask for:
- **Reason**: Type "Product broken"
- **Amount**: Type "100"

### 4. Watch for Modal Dialog

**Expected Behavior:**
```
✅ Console logs:
   🔍 HITL handler called with: {order_id: "ORD-12345", amount: 100, reason: "Product broken"}

✅ Visual:
   - Screen darkens with semi-transparent overlay
   - Modal dialog appears center-screen
   - Shows: Order ID: ORD-12345
   - Shows: Amount: $100.00
   - Shows: Reason: Product broken
   - Two buttons: "❌ Cancel" and "✅ Approve Refund"
```

### 5. Test Approve Flow

Click "✅ Approve Refund" button

**Expected:**
```
✅ Console logs:
   🔍 User decision: APPROVED

✅ Visual:
   - Modal disappears
   - Agent responds: "Refund processed successfully for order ORD-12345"
```

### 6. Test Cancel Flow

Request another refund, then click "❌ Cancel"

**Expected:**
```
✅ Console logs:
   🔍 User decision: CANCELLED

✅ Visual:
   - Modal disappears
   - Agent responds: "Refund cancelled by user"
```

## Troubleshooting

### If Handler Not Called

**Symptom:** No "🔍 HITL handler called with:" in console

**Diagnosis:**
```bash
# Check if backend still has process_refund in tools
cd tutorial_implementation/tutorial30/agent
grep "process_refund" agent.py

# Should NOT appear in tools list (around line 349)
```

**Fix:** Restart backend server
```bash
# Kill backend
pkill -f "python agent.py"

# Start backend
cd tutorial_implementation/tutorial30
make dev-backend
```

### If Modal Doesn't Appear

**Symptom:** Handler called but no modal visible

**Diagnosis:**
```javascript
// In browser console, check state
console.log("refundRequest state:", 
  document.querySelector('[class*="fixed inset-0"]'))

// Should show the modal element when refund requested
```

**Fix:** Check for CSS/z-index conflicts

### If Buttons Don't Work

**Symptom:** Modal shows but clicking buttons does nothing

**Diagnosis:**
```javascript
// In browser console, check if resolver exists
console.log("Resolver exists:", typeof window.__refundPromiseResolve)

// Should be "function" when waiting for approval
```

**Fix:** Check handleRefundApproval is correctly wired to buttons

## Success Criteria

- ✅ Modal dialog appears when refund requested
- ✅ Modal shows correct order_id, amount, reason
- ✅ Approve button processes refund with success message
- ✅ Cancel button cancels refund with cancellation message
- ✅ Modal disappears after decision
- ✅ Agent receives and acknowledges user's decision
- ✅ Console logs show handler invocation and user decision
- ✅ Works in both light and dark mode

## Architecture Benefits

### 1. Clear Separation of Concerns
- **Backend**: Business logic, data access, tool implementations
- **Frontend**: User interaction, approval workflows, UI components

### 2. Security
- Sensitive actions require explicit user approval
- No automatic execution of critical operations
- Audit trail via console logs

### 3. User Experience
- Visual feedback with modal overlay
- Clear presentation of action details
- Explicit approval/cancel buttons
- Responsive design

### 4. Maintainability
- Frontend-only actions easy to identify (`available: "remote"`)
- Backend doesn't need HITL logic
- Promise-based async pattern is standard JavaScript

## Key Learnings

1. **Tool Priority**: Backend tools take precedence over frontend actions
2. **Frontend-Only Actions**: Use `available: "remote"` AND remove from backend tools
3. **Promise Pattern**: Unresolved Promise effectively blocks agent execution
4. **State Management**: React state triggers modal rendering
5. **Cleanup**: Always clean up global state (Promise resolver)

## Files Modified

- `/agent/agent.py`: Removed `process_refund` from tools list (line 349)
- Backend restarted to apply changes

## Files Already Correct

- `/nextjs_frontend/app/page.tsx`: 
  - Modal dialog component (lines 183-233)
  - Handler with Promise (lines 109-119)
  - Approval handler (lines 145-174)

## Next Steps

1. **Test the implementation** following instructions above
2. **Verify all three features work**:
   - Generative UI: "Show me product PROD-001"
   - HITL: "I want a refund for ORD-12345"
   - Shared State: "What's my account status?"
3. **Document final results** based on testing outcomes

**Ready to test!** Follow the testing instructions above and verify the modal dialog appears properly.
