# Tutorial 31: CopilotKit Endpoint Fix - Successfully Resolved 422 Errors

## Date
2025-01-14

## Summary
Fixed persistent 422 Unprocessable Entity errors in Tutorial 31's /api/copilotkit endpoint by replacing strict Pydantic validation with flexible JSON parsing and correcting ADK agent invocation pattern.

## Root Causes Identified

### 1. Pydantic Validation Too Strict
**Problem**: `CopilotKitRequest(BaseModel)` was rejecting actual CopilotKit requests before handler code executed.

**Solution**: Changed endpoint signature from `request: CopilotKitRequest` to `request: FastAPIRequest`, manually parse JSON with `await request.json()`.

### 2. Incorrect Agent Invocation
**Problem**: Attempted to call `adk_agent.run()` which doesn't exist on `Agent` objects (error: `'LlmAgent' object has no attribute 'run'`).

**Solution**: Used proper ADK pattern with `InMemoryRunner`:
```python
from google.adk.runners import InMemoryRunner
from google.genai import types

runner = InMemoryRunner(agent=adk_agent, app_name='data_analyst')
session = await runner.session_service.create_session(...)
message = types.Content(role='user', parts=[types.Part(text=prompt)])

async for event in runner.run_async(user_id, session_id, new_message=message):
    # Process event.content.parts[].text
```

## Changes Made

### agent/agent.py
1. **Removed**:
   - `from pydantic import BaseModel`
   - `class CopilotKitMessage(BaseModel)`
   - `class CopilotKitRequest(BaseModel)`
   - `import asyncio` (unused)

2. **Added**:
   - `from fastapi import Request as FastAPIRequest` (top-level import)
   - Dynamic JSON parsing in endpoint handler
   - Proper `InMemoryRunner` + `types.Content` pattern

3. **Endpoint Signature**: 
   - Before: `async def copilotkit_endpoint(request: CopilotKitRequest)`
   - After: `async def copilotkit_endpoint(request: FastAPIRequest)`

## Testing Results

**curl Test**:
```bash
curl -X POST http://localhost:8000/api/copilotkit \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello, can you help me analyze data?"}]}'
```

**Response**:
```json
{
  "role": "assistant",
  "content": "Yes, I can. First, I need you to load the data. Please provide the file name and the CSV content.\n",
  "id": "msg-3358460b-4cc0-4457-a9ea-f57a9913a459"
}
```

✅ **Success**: Agent responds correctly with contextually appropriate message.

## Architecture Pattern

Successfully implemented **Python-only solution** without ag_ui_adk:

```
Frontend (Vite + React + CopilotKit)
  ↓ HTTP POST /api/copilotkit
  ↓ Vite proxy (localhost:5173 → localhost:8000)
Backend (FastAPI)
  ↓ Parse flexible JSON
  ↓ InMemoryRunner.run_async()
Google ADK Agent (gemini-2.0-flash-exp)
  ↓ Execute tools (load_csv_data, analyze_data, create_chart)
Response ← Event stream → CopilotKit
```

## Key Learnings

1. **Flexible JSON Parsing**: For external integrations, accept raw `Request` objects instead of strict Pydantic models to inspect actual payload formats first.

2. **ADK Invocation Pattern**: ADK agents don't have `.run()` method. Always use:
   - `InMemoryRunner(agent, app_name)`
   - `runner.session_service.create_session()`
   - `runner.run_async(user_id, session_id, new_message=types.Content(...))`

3. **Debugging Strategy**: Remove validation layers to see actual data structure before enforcing schemas.

4. **Vite vs Next.js**: Vite lacks API routes, so Python backend must handle protocol translation directly (unlike Next.js which uses API routes + CopilotRuntime + HttpAgent).

## Next Steps

- ✅ Backend endpoint working
- 🔄 Test with frontend browser
- ⏳ CSV upload functionality
- ⏳ End-to-end data analysis workflow
- ⏳ Update tutorial documentation

## Status
✅ **RESOLVED** - Endpoint accepts requests and agent responds correctly.
