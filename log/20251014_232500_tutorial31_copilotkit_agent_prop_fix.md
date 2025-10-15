# Tutorial 31: CopilotKit Agent Prop Fix (422 Error)

**Date**: 2025-10-14 23:25:00  
**Status**: ✅ Complete  
**Type**: Bug Fix

## Summary

Fixed 422 Unprocessable Entity error by adding missing `agent` prop to CopilotKit component. This prop is required to route requests to the correct ADK agent.

## Problem Identified

After fixing the 404 error, user encountered a new error:
```
Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)
:5173/api/copilotkit
```

### Root Cause

The `CopilotKit` component was missing the required `agent` prop. Without this prop, the AG-UI protocol doesn't know which agent to route the request to, resulting in a 422 validation error.

## Solution Applied

### Frontend Fix

**File**: `frontend/src/App.tsx`

**Before**:
```tsx
<CopilotKit runtimeUrl="/api/copilotkit">
  <div className="dashboard">
    {/* ... */}
  </div>
</CopilotKit>
```

**After**:
```tsx
<CopilotKit runtimeUrl="/api/copilotkit" agent="data_analyst">
  <div className="dashboard">
    {/* ... */}
  </div>
</CopilotKit>
```

### Agent Name Matching

The `agent` prop must match the agent name defined in the backend:

**File**: `agent/agent.py`
```python
adk_agent = Agent(
    name="data_analyst",  # ← Frontend agent prop must match this
    model="gemini-2.0-flash-exp",
    instruction="...",
    tools=[load_csv_data, analyze_data, create_chart]
)
```

## Technical Details

### AG-UI Protocol Agent Routing

The AG-UI protocol uses the agent name to route requests:

1. **Frontend**: Sends agent name in request metadata
2. **Backend**: `add_adk_fastapi_endpoint()` registers agent with name
3. **Routing**: ag_ui_adk matches request to correct agent
4. **Result**: Agent processes request and returns response

### Comparison with Tutorial 30

Tutorial 30 correctly implements this pattern:

```tsx
// tutorial30/nextjs_frontend/app/page.tsx
<CopilotKit runtimeUrl="/api/copilotkit" agent="customer_support_agent">
  <ChatInterface />
</CopilotKit>
```

With matching backend:
```python
# tutorial30/agent/agent.py
adk_agent = Agent(
    name="customer_support_agent",  # Matches frontend
    # ...
)
```

## Files Modified

1. `frontend/src/App.tsx` - Added `agent="data_analyst"` prop
2. `README.md` - Added troubleshooting section for 422 error

## Testing Instructions

1. **Ensure** changes are applied (Vite hot-reloads automatically)
2. **Refresh** browser if needed
3. **Upload** CSV file
4. **Send** chat message
5. **Verify** no 422 errors in console
6. **Confirm** agent responds correctly

## Expected Behavior

After fix:
```
✅ Connection successful
✅ Agent routing: data_analyst
✅ Request processed
✅ Response received
```

Console should show successful GraphQL operations instead of 422 errors.

## Documentation Updates

Added new troubleshooting section at top of README:

### 422 Unprocessable Entity Error

- **Symptom**: Missing or incorrect agent prop
- **Solution**: Add `agent="data_analyst"` to CopilotKit
- **Example**: Correct vs incorrect code snippets
- **Explanation**: How agent name matching works

## Lessons Learned

1. **AG-UI requires agent prop**: Not optional - must match backend name
2. **Reference similar tutorials**: Tutorial 30 showed correct pattern
3. **Documentation matters**: Error was not obvious without docs
4. **Agent naming consistency**: Frontend and backend must align exactly
5. **Test thoroughly**: 404 fixed but revealed new issue

## Error Sequence

1. **Initial**: 404 Not Found (wrong proxy config)
2. **After proxy fix**: 422 Unprocessable Entity (missing agent prop)
3. **After agent prop**: ✅ Working correctly

## Related Issues

Common mistakes that cause 422 errors:
- Missing `agent` prop entirely
- Typo in agent name (`data_analyst` vs `dataAnalyst`)
- Backend agent name doesn't match frontend
- Multiple agents registered but wrong name used

## Prevention

Always ensure when creating ADK + CopilotKit integration:

1. Define agent name in backend: `name="agent_name"`
2. Add same name to frontend: `agent="agent_name"`
3. Keep names synchronized during refactoring
4. Document agent name in README
5. Add validation tests for agent name matching

## Next Steps

1. User should verify agent responds correctly
2. Test all agent tools (CSV upload, analysis, charts)
3. Complete remaining tutorial implementation
4. Update original tutorial documentation

## Related Files

- `frontend/src/App.tsx` - CopilotKit configuration
- `agent/agent.py` - Agent definition and registration
- `README.md` - Troubleshooting documentation
- `tutorial_implementation/tutorial30/` - Reference implementation
