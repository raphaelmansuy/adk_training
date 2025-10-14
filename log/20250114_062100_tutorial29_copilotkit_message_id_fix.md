# Tutorial 29: CopilotKit Message ID Fix

**Date**: 2025-01-14 06:21:00  
**Issue**: 422 Unprocessable Entity errors from `/api/copilotkit` endpoint  
**Root Cause**: CopilotKit sends messages without IDs, but AG-UI protocol requires them

## Problem

The Tutorial 29 backend was returning 422 errors when receiving requests from the CopilotKit frontend:

```
INFO:     127.0.0.1:64171 - "POST /api/copilotkit HTTP/1.1" 422 Unprocessable Entity
```

## Solution

Added `MessageIDMiddleware` from Tutorial 30 to inject UUIDs into messages that lack the required `id` field.

### Changes Made

1. **Added imports** (`agent/agent.py`):
   - `import json`
   - `import uuid`
   - `from starlette.middleware.base import BaseHTTPMiddleware`
   - `from starlette.requests import Request`

2. **Added MessageIDMiddleware class**:
   - Intercepts POST requests to `/api/copilotkit`
   - Parses request body JSON
   - Injects `msg-{uuid}` IDs into messages missing the `id` field
   - Reconstructs request with modified body

3. **Registered middleware**:
   - Added `app.add_middleware(MessageIDMiddleware)` before the CopilotKit endpoint

## Technical Details

- **CopilotKit Behavior**: Sends messages in format `{role, content}` without `id`
- **AG-UI Requirement**: Messages must have unique `id` field
- **Middleware Solution**: Transparently adds IDs without changing client code

## Testing

After fix:
- Backend accepts CopilotKit requests without 422 errors
- Frontend chat interface connects successfully
- Message streaming works correctly

## Lessons Learned

1. **Protocol Compatibility**: Different UI frameworks have different message formats
2. **Middleware Pattern**: Middleware is ideal for protocol adaptation without changing core code
3. **Reference Implementation**: Tutorial 30 provided working example to follow
4. **AG-UI Protocol**: Requires message IDs for proper state management

## Files Modified

- `/tutorial_implementation/tutorial29/agent/agent.py` - Added MessageIDMiddleware

## Status

✅ Complete - Tutorial 29 backend now compatible with CopilotKit frontend
