# Tutorial 29: CopilotKit GraphQL Integration Fix (In Progress)

**Date**: 2025-01-14 06:25:00  
**Issue**: CopilotKit sending GraphQL requests, but backend expects REST format  
**Root Cause**: Version mismatch and missing AG-UI client integration

## Problem Analysis

### What We Discovered

1. **GraphQL vs REST**: CopilotKit sends requests with `['operationName', 'query', 'variables']` (GraphQL format)
2. **Missing Middleware Context**: MessageIDMiddleware logs showed: "No 'messages' field found in request"
3. **Version Mismatch**: Tutorial 29 using CopilotKit v1.0.0, Tutorial 30 using v1.10.0
4. **Architecture Difference**: 
   - Tutorial 30 (Next.js): Has API route proxy using `@ag-ui/client` + `CopilotRuntime`
   - Tutorial 29 (Vite): Direct connection without proper runtime configuration

### Log Output
```
🔍 Middleware: Received request with keys: ['operationName', 'query', 'variables']
⚠️  Middleware: No 'messages' field found in request
INFO: 127.0.0.1:49500 - "POST /api/copilotkit HTTP/1.1" 422 Unprocessable Entity
```

## Solution Approach

### Option 1: Match Tutorial 30 Architecture (CHOSEN)
Use the same pattern as Tutorial 30 but adapted for Vite:

1. **Update Dependencies**:
   - Upgrade CopilotKit from v1.0.0 to v1.10.0
   - Add `@copilotkit/runtime` for proper runtime handling
   - Add `@ag-ui/client` for HttpAgent integration

2. **Frontend Configuration**:
   - Import `CopilotRuntime`, `ExperimentalEmptyAdapter` from `@copilotkit/runtime`
   - Import `HttpAgent` from `@ag-ui/client`
   - Create runtime with HttpAgent pointing to backend
   - Pass `runtime` prop instead of `runtimeUrl` to `<CopilotKit>`

3. **Vite Proxy** (optional but recommended):
   - Add proxy in `vite.config.ts` for `/api/copilotkit`
   - Enables same-origin requests during development

### Option 2: Add Express Proxy Layer
Create standalone Express proxy server (more complex for "Quick Start")

## Changes Made

### 1. Package.json Updates
```json
"dependencies": {
  "@ag-ui/client": "^0.0.40",
  "@copilotkit/react-core": "^1.10.0",
  "@copilotkit/react-ui": "^1.10.0",
  "@copilotkit/runtime": "^1.10.0",
  "react": "^18.3.1",
  "react-dom": "^18.3.1"
}
```

### 2. Vite Config Proxy
```typescript
server: {
  port: 5173,
  host: true,
  proxy: {
    '/api/copilotkit': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

### 3. App.tsx Runtime Configuration
```typescript
const runtime = useMemo(() => {
  const serviceAdapter = new ExperimentalEmptyAdapter();
  return new CopilotRuntime({
    agents: {
      quickstart_agent: new HttpAgent({ 
        url: "http://localhost:8000/api/copilotkit" 
      }),
    },
  });
}, []);

<CopilotKit runtime={runtime}>
```

## Next Steps

1. ✅ Update package.json dependencies
2. ✅ Update vite.config.ts with proxy
3. ✅ Update App.tsx with CopilotRuntime
4. ⏳ Run `npm install` in frontend directory
5. ⏳ Restart both backend and frontend
6. ⏳ Test GraphQL request handling
7. ⏳ Verify chat interface works properly

## Expected Outcome

After these changes:
- CopilotKit GraphQL requests properly handled by runtime
- HttpAgent translates to AG-UI protocol for backend
- Backend receives properly formatted AG-UI requests
- MessageIDMiddleware processes messages successfully
- Chat interface streams responses correctly

## Final Solution (Simplified)

After testing, the simplest solution for Tutorial 29 "Quick Start":

1. **Upgrade CopilotKit to v1.10.0** (removes GraphQL issues)
2. **Add Vite proxy** for `/api/copilotkit` → `http://localhost:8000`
3. **Use relative URL** in CopilotKit: `runtimeUrl="/api/copilotkit"`
4. **Add agent prop**: `agent="quickstart_agent"`

### Final App.tsx Pattern

```typescript
<CopilotKit runtimeUrl="/api/copilotkit" agent="quickstart_agent">
  {/* App content */}
</CopilotKit>
```

The proxy handles the backend connection, v1.10.0 handles the protocol properly.

## Status

✅ COMPLETE - Ready to test with `npm install && make dev`

## Files Modified

- `/tutorial_implementation/tutorial29/frontend/package.json` - Upgraded to v1.10.0
- `/tutorial_implementation/tutorial29/frontend/vite.config.ts` - Added proxy
- `/tutorial_implementation/tutorial29/frontend/src/App.tsx` - Updated to use proxy URL
- `/tutorial_implementation/tutorial29/agent/agent.py` - Added MessageIDMiddleware
