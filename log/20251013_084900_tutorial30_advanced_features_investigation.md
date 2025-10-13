# Tutorial 30: Advanced Features Not Working - Investigation

**Date**: January 13, 2025 08:49 AM  
**Tutorial**: Tutorial 30 - CopilotKit AG-UI Integration  
**Status**: 🔄 In Progress - Requires Architecture Change  
**Issue**: Advanced features (Generative UI, HITL) not being used by agent

---

## 🎯 Problem

User reported "Advanced feature are not used!" after testing the agent. When asking "Show me product PROD-001", the agent returns text-only output instead of rendering a ProductCard component.

---

## 🔍 Root Cause Analysis

### The Issue
1. **Backend has tools**: `get_product_details()`, `process_refund()`
2. **Frontend has actions**: `render_product_card`, `process_refund` (via useCopilotAction)
3. **Gap**: Backend tools are being called, but they don't trigger frontend actions
4. **Result**: Agent returns text data instead of rendering React components

### Why It's Not Working
- AG-UI protocol connects backend ADK agent to CopilotKit frontend
- Backend tools return JSON data
- Frontend actions registered with `useCopilotAction` are NOT automatically exposed to backend
- The frontend actions need to be explicitly available as "remote" tools OR
- We need to use new CopilotKit hooks (`useRenderToolCall`, `useHumanInTheLoop`)

---

## 🔧 Attempted Solutions

### Attempt 1: Rename Backend Tool
- Changed `create_product_card` → `get_product_details`
- Updated agent instruction
- ❌ Still didn't work - backend tool called, frontend action not triggered

### Attempt 2: Use New CopilotKit Hooks
- Tried `useRenderToolCall` to intercept backend tool calls
- Tried `useHumanInTheLoop` for refund approval
- ❌ TypeScript errors, missing types, zod dependency issues

### Attempt 3: Install Missing Dependencies
- Installed `zod` package
- ✅ Package installed successfully
- ⚠️ Still have TypeScript signature mismatches

---

## 📚 Key Learnings

### CopilotKit Hook Deprecation (v1.10+)
According to documentation:
- `useCopilotAction` → Being deprecated
- New hooks:
  - `useFrontendTool` - For frontend-only tools with handlers
  - `useHumanInTheLoop` - For user approval workflows
  - `useRenderToolCall` - For rendering backend tool calls

### AG-UI Protocol Behavior
- Backend tools are executed on backend
- Frontend actions are executed on frontend  
- They don't automatically connect unless explicitly configured
- Need proper tool discovery and calling mechanism

---

## 🎯 Correct Solution (Not Yet Implemented)

### Option 1: Use `useRenderToolCall` (Recommended)
```typescript
useRenderToolCall({
  name: "get_product_details",  // Backend tool name
  render: ({ result }) => {
    if (result?.product) {
      return <ProductCard {...result.product} />;
    }
    return null;
  },
});
```

### Option 2: Make Frontend Actions Available as Remote Tools
```typescript
useCopilotAction({
  name: "render_product_card",
  available: "remote",  // Makes it callable by backend
  parameters: [...],
  handler: ({ product }) => <ProductCard {...product} />,
});
```

Then backend agent needs to know to call `render_product_card` after fetching data.

### Option 3: Simpler - Just Use Backend Tools Without Frontend Actions
- Remove frontend actions entirely
- Backend returns data
- Frontend intercepts and renders based on data structure
- Use response parsing in CopilotChat component

---

## 🚧 Current State

### Backend (`agent/agent.py`)
```python
# ✅ Working tool
def get_product_details(product_id: str) -> Dict[str, Any]:
    # Returns product data
    return {
        "status": "success",
        "report": "Here are the details...",
        "product": {
            "name": "Widget Pro",
            "price": 99.99,
            ...
        }
    }

# ❌ Not in tools list anymore
# process_refund removed from agent tools
```

### Frontend (`app/page.tsx`)
```typescript
// ❌ Broken - using deprecated/new hooks incorrectly
useRenderToolCall({...})  // TypeScript errors
useHumanInTheLoop({...})  // Missing types
```

---

## 📋 Next Steps

1. **Install correct CopilotKit version** with new hooks
2. **Fix TypeScript types** for new hooks
3. **Implement `useRenderToolCall`** for get_product_details
4. **Implement `useHumanInTheLoop`** for process_refund
5. **Test with actual agent** to verify rendering
6. **Add process_refund back to backend** if using HITL hook

---

## 🔄 Alternative Approach (Simpler)

If new hooks continue to have issues, revert to:
1. Keep backend tools simple (data retrieval only)
2. Use old `useCopilotAction` with proper `available` and `render` config
3. Ensure agent instruction tells LLM to call frontend actions
4. May require custom message parsing in frontend

---

**Status**: Investigation complete, implementation in progress  
**Blocker**: TypeScript compatibility with new CopilotKit hooks  
**Risk**: HIGH - Core features completely broken  
**Priority**: CRITICAL - Must fix before tutorial can be used
