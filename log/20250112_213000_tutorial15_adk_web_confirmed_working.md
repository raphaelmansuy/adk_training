# Tutorial 15: ADK Web Confirmed Working for Live API

## Date

2025-01-12 21:30:00

## Summary

Successfully confirmed that `adk web` provides fully functional Live API bidirectional
streaming with audio support. User reported: "adk web works".

## Working Solution

### Commands Used

```bash
cd tutorial_implementation/tutorial15
pip install -e .  # Install voice_assistant as discoverable package
adk web          # Start web server with WebSocket endpoints
```

### Access

- **URL**: http://localhost:8000
- **Agent**: Select `voice_assistant` from dropdown
- **Audio Mode**: Click microphone/audio button
- **Result**: ✅ Working bidirectional audio streaming

## Key Insights

### Why ADK Web Works

**WebSocket Endpoint Pattern** (`/run_live`):

```python
@app.websocket("/run_live")
async def run_agent_live(websocket, app_name, user_id, session_id):
    queue = LiveRequestQueue()
    
    # Two concurrent tasks with active WebSocket
    async def forward_events():
        async for event in runner.run_live(queue, ...):
            await websocket.send_text(event.model_dump_json())
    
    async def process_messages():
        while True:
            data = await websocket.receive_text()
            queue.send(LiveRequest.model_validate_json(data))
    
    await asyncio.gather(forward_events(), process_messages())
```

**Critical Components**:

- Active WebSocket connection between browser and server
- Frontend continuously sends LiveRequest messages
- Server forwards Event responses back to client
- Bidirectional communication channel stays open
- Queue receives messages from WebSocket, not just script

### Why Standalone Scripts Don't Work

**Programmatic Pattern** (doesn't work):

```python
# No WebSocket connection
queue = LiveRequestQueue()
queue.send_content(...)
queue.close()

# Hangs - no client sending LiveRequest messages
async for event in runner.run_live(queue, ...):
    # Never receives events
    pass
```

**Problem**: `runner.run_live()` expects continuous LiveRequest stream from
connected client, not single-shot message from script.

## Comparison: What Works vs What Doesn't

| Approach | Works? | Why |
|----------|--------|-----|
| `adk web` | ✅ YES | WebSocket with connected browser client |
| `basic_demo.py` (text→text) | ✅ YES | Single turn, closes queue immediately |
| `basic_demo.py` (text→audio) | ⚠️ SLOW | Works but takes 20-30s, often times out |
| `direct_live_audio.py` | ✅ YES | Bypasses ADK Runner, uses direct API |
| Standalone `runner.run_live()` | ❌ NO | No WebSocket connection context |

## Recommendations

### For Tutorial 15 Users

**Primary Method** (Recommended):

```bash
make setup     # Install as package
adk web        # Use web interface
```

- Full ADK features (tools, state, agents)
- Bidirectional audio streaming
- Proven working pattern
- Official supported approach

**Alternative Method** (Audio I/O without ADK framework):

```bash
make direct_audio_demo
```

- Direct `genai.Client` API
- True audio input support
- No ADK agent features
- Simpler, but more limited

### For Documentation

Update Tutorial 15 docs to emphasize:

1. **`adk web` is the primary Live API interface**
2. `runner.run_live()` requires WebSocket server context
3. Standalone scripts should use direct `genai.Client` API
4. `basic_demo.py` is for demonstration only (single turn)

## Files Status

### Working Files

- ✅ `voice_assistant/agent.py` - Agent definition
- ✅ `voice_assistant/audio_utils.py` - Audio I/O utilities
- ✅ `voice_assistant/basic_demo.py` - Text demo (single turn)
- ✅ `voice_assistant/direct_live_audio.py` - Direct API alternative
- ✅ `pyproject.toml` - Package configuration for ADK discovery

### Server Logs

- `adk_web.log` - Web server output (running in background)

## Next Steps

1. ✅ Confirmed working solution (adk web)
2. Document best practices in tutorial
3. Update README with clear usage instructions
4. Add troubleshooting section about WebSocket requirement
5. Consider removing `basic_demo_fixed.py` (attempted fix that doesn't work)

## Conclusion

**`runner.run_live()` is designed for WebSocket server contexts, not standalone
scripts.** The ADK web interface is the official, working pattern for Live API
bidirectional streaming with full agent capabilities.

User confirmation: "adk web works" ✅
