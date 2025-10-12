# Tutorial 15: Runner.run_live() Limitation Confirmed

## Date

2025-01-12 21:00:00

## Summary

Confirmed that `runner.run_live()` **does NOT work** in standalone Python scripts, even with proper concurrent queue management. It ONLY works within the ADK web server WebSocket endpoint context.

## Investigation

### Attempted Fix

Created `basic_demo_fixed.py` implementing the same concurrent pattern as ADK web server:

```python
async def forward_events():
    async for event in runner.run_live(...):
        process_event(event)

async def send_messages():
    queue.send_content(...)
    await response_received.wait()
    queue.close()

# Run concurrently
await asyncio.gather(forward_events(), send_messages())
```

### Result

**STILL HANGS** at the `async for event in runner.run_live()` loop.

## Root Cause

`runner.run_live()` is designed to work ONLY in these contexts:

1. **ADK Web Server WebSocket Handler** (`@app.websocket("/run_live")`)
   - Has active WebSocket connection
   - Frontend sends LiveRequest messages through WebSocket
   - Server forwards events back through WebSocket

2. **Direct genai.Client Connection** (bypasses ADK Runner entirely)
   - Uses `google.genai.Client.aio.live.connect()`
   - Establishes own WebSocket connection
   - Does not use `runner.run_live()` at all

### Why Standalone Scripts Fail

When running `runner.run_live()` in a standalone script:
- No WebSocket connection exists
- No client is connected to send LiveRequest messages
- Queue closes immediately after sending one message
- Loop waits indefinitely for events that never come
- Timeout occurs (or hangs forever without timeout)

## Working Solutions

### Option 1: Use ADK Web Interface (Recommended)

```bash
cd tutorial_implementation/tutorial15
export VOICE_ASSISTANT_LIVE_MODEL=gemini-2.0-flash-live-preview-04-09
adk web

# Open http://localhost:8000
# Select voice_assistant from dropdown
# Click Audio button to start voice chat
```

**Advantages**:
- ✅ Fully functional bidirectional audio
- ✅ Uses ADK agent framework (tools, state, etc.)
- ✅ Official supported pattern
- ✅ Proven to work

### Option 2: Direct Live API (Alternative)

```bash
cd tutorial_implementation/tutorial15
make direct_audio_demo
```

**Advantages**:
- ✅ Works in standalone script
- ✅ True bidirectional audio (mic input → audio output)
- ✅ Official Google API

**Disadvantages**:
- ❌ No ADK agent framework
- ❌ No tools, state management, or other ADK features
- ❌ Manual conversation handling

### Option 3: Text-based Demo (Existing basic_demo.py)

```bash
make basic_demo_text   # Text input → Text output
make basic_demo_audio  # Text input → Audio output
```

**This DOES work** because:
- Uses `queue.send_content()` for text input ✅
- Receives responses via `event.server_content` ✅
- Single turn, no continuous bidirectional streaming needed

## Key Technical Insight

The difference between **working** and **broken**:

**Working (basic_demo.py)**:
```python
queue.send_content(...)  # Send one message
queue.close()            # Close immediately

async for event in runner.run_live(...):
    # Processes this single turn successfully
    process_event(event)
```

**Broken (attempted concurrent pattern)**:
```python
queue.send_content(...)  # Send one message
# Queue stays open
# No WebSocket client sending more LiveRequest messages
# Loop waits forever for next event

async for event in runner.run_live(...):
    # Hangs - no WebSocket connection providing events
    pass
```

**Working (ADK web server)**:
```python
@app.websocket("/run_live")
async def handler(websocket):
    queue = LiveRequestQueue()
    
    # Frontend continuously sends LiveRequest via WebSocket
    async def process_messages():
        while True:
            data = await websocket.receive_text()
            queue.send(LiveRequest.model_validate_json(data))
    
    # Server forwards events back to frontend
    async def forward_events():
        async for event in runner.run_live(queue, ...):
            await websocket.send_text(event.model_dump_json())
    
    # Both run concurrently with active WebSocket
    await asyncio.gather(forward_events(), process_messages())
```

## Conclusion

**`runner.run_live()` requires an active WebSocket connection with a client sending LiveRequest messages.**

For standalone scripts:
- Use `basic_demo.py` (text input → text/audio output) ✅
- Use `direct_live_audio.py` (direct API, bypasses Runner) ✅
- Do NOT try to replicate ADK web server pattern ❌

## Files Updated

- Created `basic_demo_fixed.py` (attempted fix - confirmed doesn't work)
- This log documents the limitation

## Next Steps

1. Update tutorial documentation to clarify `runner.run_live()` limitation
2. Recommend `adk web` as primary Live API interface
3. Keep `basic_demo.py` for simple text/audio demos
4. Keep `direct_live_audio.py` for true bidirectional voice
