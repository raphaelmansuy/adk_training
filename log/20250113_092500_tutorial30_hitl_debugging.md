# Tutorial 30: HITL Not Working - Investigation

**Date:** 2025-01-13 09:25 AM  
**Issue:** Human-in-the-Loop approval dialog not appearing for refunds  
**Status:** 🔧 Debugging in progress

## Problem

When user requests a refund:
1. ✅ Agent correctly asks for order ID, amount, and reason
2. ✅ Agent calls `process_refund()` with parameters
3. ❌ Frontend approval dialog does NOT appear
4. ❌ Refund is processed immediately without user confirmation
5. ✅ Agent responds with "The refund has been processed..."

**Expected Behavior:**
- Approval dialog should appear BEFORE refund is processed
- User should see Cancel and Approve buttons
- Refund should only process if user clicks Approve

## Architecture Analysis

### Current Setup

**Backend (`agent.py`):**
```python
def process_refund(order_id: str, amount: float, reason: str) -> Dict[str, Any]:
    """Process a refund for an order."""
    # Refund logic here
    return {"status": "success", "refund": {...}}

# In tools list:
tools=[..., process_refund]
```

**Frontend (`page.tsx`):**
```typescript
useCopilotAction({
  name: "process_refund",
  renderAndWaitForResponse: ({ args, respond, status }) => {
    if (status !== "executing") return <div className="hidden" />;
    // Show approval dialog with Cancel/Approve buttons
  },
});
```

### Potential Issues

#### Issue 1: Name Collision
Both backend and frontend define `process_refund`:
- Backend: As a Python tool function
- Frontend: As a CopilotAction with HITL

**Hypothesis:** Backend tool executes directly, bypassing frontend HITL dialog.

**Test:** Check if removing backend tool from tools list causes frontend to take over.

#### Issue 2: AG-UI Protocol Tool Resolution
When agent calls `process_refund`:
1. Does AG-UI protocol check frontend actions first?
2. Or does it execute backend tool directly?
3. Is there a priority/override mechanism?

**Official docs say:** Frontend actions with `renderAndWaitForResponse` should intercept backend tool calls.

#### Issue 3: Status Flow
`renderAndWaitForResponse` only shows dialog when `status === "executing"`.

**Possible statuses:**
- `"inProgress"` - Tool is being called
- `"executing"` - Waiting for user response
- `"complete"` - Tool completed

**Hypothesis:** Status might be "inProgress" instead of "executing", causing dialog to not render.

**Test:** Log status value in render function.

#### Issue 4: CopilotKit Version Compatibility
Tutorial uses CopilotKit v1.10.0 with ADK.

**Question:** Is `renderAndWaitForResponse` fully supported with ADK backend?

**Check:** CopilotKit migration docs and compatibility matrix.

## Debugging Steps

### Step 1: Add Console Logging

Update `page.tsx` to log status:

```typescript
renderAndWaitForResponse: ({ args, respond, status }) => {
  console.log("🔍 HITL Status:", status);
  console.log("🔍 HITL Args:", args);
  console.log("🔍 HITL Respond:", typeof respond);
  
  if (status !== "executing") {
    console.warn("❌ Status is not 'executing', dialog won't show");
    return <div className="hidden" />;
  }
  // ... dialog code
},
```

### Step 2: Check Backend Logs

Look for clues in backend terminal:
- Is `process_refund` being called?
- Are there any AG-UI protocol messages about frontend actions?
- Any errors or warnings?

### Step 3: Check Browser Network Tab

Filter for `POST /api/copilotkit`:
- Request payload: Does it include process_refund tool call?
- Response: Does it mention frontend action interception?
- Headers: Any AG-UI protocol headers?

### Step 4: Test Without Backend Tool

Temporarily remove `process_refund` from backend tools list:

```python
tools=[
    search_knowledge_base,
    lookup_order_status,
    create_support_ticket,
    get_product_details,
    # process_refund,  # Commented out for testing
],
```

**Expected:**
- Agent might say "I don't have a process_refund tool"
- OR AG-UI discovers frontend action and uses it
- If frontend action works, we know it's a collision issue

### Step 5: Check CopilotKit Agent Mode

Verify `CopilotKit` component configuration:

```typescript
<CopilotKit
  runtimeUrl="/api/copilotkit"
  agent="customer_support_agent"  // Must match backend agent name
>
```

Agent name must match exactly for AG-UI protocol to work.

## Possible Solutions

### Solution A: Remove Backend Tool
If frontend action should be the ONLY implementation:

```python
# Backend: Remove from tools list
tools=[..., # NO process_refund]

# Frontend: Keep as is with renderAndWaitForResponse
```

**Trade-off:** Lose backend refund logic, frontend must implement everything.

### Solution B: Use Frontend Action with Remote Handler
If backend logic should run AFTER approval:

```typescript
useCopilotAction({
  name: "process_refund",
  available: "remote",  // Frontend-only, no backend collision
  handler: async ({ order_id, amount, reason }) => {
    // Call backend API endpoint (not agent tool)
    const response = await fetch("/api/refund", {
      method: "POST",
      body: JSON.stringify({ order_id, amount, reason }),
    });
    return response.json();
  },
  renderAndWaitForResponse: ({ args, respond, status }) => {
    // Show approval dialog
    // When approved, handler executes
  },
});
```

**Trade-off:** Need separate backend API endpoint for refunds.

### Solution C: Backend Tool with Returns Schema (ADK Official Pattern)
Following official HITL docs exactly:

```python
# Backend: Define tool with TOOL_REFERENCE including returns schema
REFUND_TOOL = """{
    "type": "function",
    "function": {
        "name": "process_refund",
        "parameters": {...},
        "returns": {
            "type": "object",
            "properties": {
                "approved": {"type": "boolean"}
            }
        }
    }
}"""

# Agent instructions reference the tool
instruction=f"...TOOL_REFERENCE: {REFUND_TOOL}..."
```

**Trade-off:** More complex setup, but matches official pattern.

## Next Steps

1. **Immediate:** Add console.log debugging to see actual status value
2. **Test:** Remove backend tool temporarily to isolate issue
3. **Research:** Check CopilotKit GitHub issues for ADK HITL examples
4. **Compare:** Find working ADK HITL example and compare architecture

## Expected Files to Check

- `/Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/tutorial30/nextjs_frontend/app/page.tsx` (frontend action)
- `/Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/tutorial30/agent/agent.py` (backend tool)
- Browser DevTools Console (status logs)
- Backend terminal (AG-UI protocol logs)
- Browser Network tab (API requests)

## References

- CopilotKit ADK HITL Docs: https://docs.copilotkit.ai/adk/human-in-the-loop/agent
- AG-UI Protocol Spec: https://docs.copilotkit.ai/ag-ui-protocol
- CopilotKit GitHub Issues: Search for "renderAndWaitForResponse ADK"
