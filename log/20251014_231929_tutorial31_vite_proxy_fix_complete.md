# Tutorial 31: Vite Proxy Configuration Fix

**Date**: 2025-10-14 23:19:29  
**Status**: ✅ Complete  
**Type**: Bug Fix + Enhancement

## Summary

Fixed 404 error on `/api/copilotkit` endpoint caused by incorrect Vite proxy configuration. Added comprehensive troubleshooting documentation.

## Problem Identified

User reported browser error:
```
Failed to load resource: the server responded with a status of 404 (Not Found)
:5173/api/copilotkit
```

### Root Cause

Vite proxy configuration was incorrectly rewriting the path:
- Frontend: `http://localhost:5173/api/copilotkit`
- Vite proxy rewrote to: `http://localhost:8000/copilotkit` (removed `/api`)
- Backend expected: `http://localhost:8000/api/copilotkit`
- Result: **404 Not Found**

## Solution Applied

### 1. Fixed Vite Proxy Configuration

**File**: `frontend/vite.config.ts`

**Before**:
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, ''),  // ❌ Removed /api prefix
  }
}
```

**After**:
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    // ✅ No rewrite - keeps /api prefix intact
  }
}
```

### 2. Added Comprehensive Troubleshooting

Enhanced `README.md` with detailed troubleshooting section covering:

- **404 Error on `/api/copilotkit`**: Backend not running, proxy mismatch, port conflicts
- **CORS Errors**: Development vs production configuration
- **Charts Not Rendering**: Chart.js registration, data format issues
- **File Upload Issues**: Size limits, CSV format, encoding
- **Agent Not Responding**: API key, backend logs, direct testing
- **Vite Build Errors**: Dependencies, Node version, TypeScript
- **Common Mistakes**: venv activation, working directory, env variables

## Technical Details

### Correct Architecture Flow

```
Browser Request: GET /api/copilotkit
       ↓
Vite Proxy: localhost:5173/api/copilotkit
       ↓
Forwards to: localhost:8000/api/copilotkit (no rewrite)
       ↓
Backend: FastAPI receives at /api/copilotkit
       ↓
ADK Agent: Processes request via ag_ui_adk
```

### Comparison with Next.js (Tutorial 30)

**Next.js Pattern**:
- API Route: `app/api/copilotkit/route.ts`
- Forwards to: `http://localhost:8000/api/copilotkit`
- Uses HttpAgent from `@ag-ui/client`

**Vite Pattern**:
- Proxy Config: `vite.config.ts`
- Forwards to: `http://localhost:8000/api/copilotkit`
- Direct connection (no middleware layer)

Both patterns keep the `/api/copilotkit` path intact on the backend!

## Files Modified

1. `frontend/vite.config.ts` - Removed incorrect path rewrite
2. `README.md` - Added comprehensive troubleshooting section (250+ lines)

## Testing Instructions

1. **Stop** frontend dev server (Ctrl+C)
2. **Restart** frontend: `cd frontend && npm run dev`
3. **Open** browser: `http://localhost:5173`
4. **Upload** CSV file
5. **Verify** no 404 errors in console
6. **Test** chat functionality

## Verification

Expected console output:
```
[Vite Proxy] POST /api/copilotkit → /api/copilotkit
✅ Connected to backend
✅ Agent responding
```

## Documentation Updates

- Added 6 major troubleshooting categories
- Included code examples for each issue
- Provided step-by-step solutions
- Added common mistakes section
- Included debugging commands

## Lessons Learned

1. **Vite proxy defaults are safe**: Don't rewrite paths unless absolutely necessary
2. **Backend path consistency**: Always match frontend proxy with backend endpoint
3. **Reference similar tutorials**: Tutorial 30 (Next.js) showed correct pattern
4. **Comprehensive troubleshooting**: Prevents repeated user questions
5. **Log proxy requests**: Debug logging helps identify routing issues

## Related Files

- `agent/agent.py` - Backend endpoint at `/api/copilotkit`
- `frontend/src/App.tsx` - CopilotKit runtimeUrl configuration
- `tutorial_implementation/tutorial30/` - Reference Next.js implementation

## Next Steps

1. User should restart frontend dev server
2. Test CSV upload and analysis features
3. Verify all agent tools work correctly
4. Complete remaining tutorial implementation tasks
