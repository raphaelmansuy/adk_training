# Tutorial 15: Critical Discovery - Audio Input Not Supported via ADK Runner

**Date**: October 12, 2025  
**Issue**: `audio_demo.py` hangs when sending audio input via `send_realtime()`  
**Status**: Root cause identified

## Problem Summary

Interactive audio demo (`make audio_demo`) successfully:
- ✅ Records audio from microphone (5 seconds, ~160KB PCM data)
- ✅ Sends audio via `queue.send_realtime(blob=Blob(data=audio_data, mime_type='audio/pcm'))`
- ✅ Calls `queue.close()` properly
- ❌ **Hangs waiting for response** - `runner.run_live()` yields NO events

## Official Documentation Research

### Google Gen AI SDK (Direct Client API)

**Source**: https://ai.google.dev/gemini-api/docs/live

Official example uses **direct `genai.Client` API**:

```python
from google import genai
from google.genai import types

client = genai.Client()
model = "gemini-2.5-flash-native-audio-preview-09-2025"

async with client.aio.live.connect(model=model, config=config) as session:
    # Load and convert audio
    y, sr = librosa.load("sample.wav", sr=16000)
    sf.write(buffer, y, sr, format='RAW', subtype='PCM_16')
    audio_bytes = buffer.read()
    
    # Send audio - NOTE: session.send_realtime_input()
    await session.send_realtime_input(
        audio=types.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
    )
    
    # Receive response
    async for response in session.receive():
        if response.data is not None:
            wf.writeframes(response.data)
```

**Key Differences**:
1. Uses `client.aio.live.connect()` - WebSocket connection
2. Uses `session.send_realtime_input()` - NOT `queue.send_realtime()`
3. Uses `session.receive()` - NOT `runner.run_live()`
4. Direct connection to Live API - bypasses ADK agent framework

### ADK Official Sample

**Source**: `research/adk-python/contributing/samples/live_bidi_streaming_single_agent/`

The official ADK sample:
- ✅ Defines agent with tools (`roll_die`, `check_prime`)
- ✅ Uses `gemini-2.0-flash-live-001` or `gemini-2.0-flash-live-preview-04-09`
- ✅ Intended for **ADK Web UI** interaction (audio/video buttons)
- ❌ **No manual Python code for audio input** shown

**Usage**: Run `adk web`, click Audio/Video button in UI to stream

## Root Cause Analysis

### ADK `Runner.run_live()` Limitations

Current implementation in `audio_demo.py`:
```python
queue = LiveRequestQueue()
queue.send_realtime(blob=types.Blob(data=audio_data, mime_type='audio/pcm'))
queue.close()

# This hangs - no events yielded
async for event in runner.run_live(
    live_request_queue=queue,
    user_id=user_id,
    session_id=session.id,
    run_config=run_config
):
    # Never reaches here
    pass
```

**Hypothesis**: `LiveRequestQueue.send_realtime()` + `Runner.run_live()` combination:
1. May not support audio input blobs in current ADK version
2. May require WebSocket Live API connection (like Web UI uses)
3. May only work with text input via `send_content()`

### Working Pattern (Text Input → Audio Output)

`basic_demo.py` successfully uses:
```python
queue = LiveRequestQueue()

# Send TEXT input
queue.send_content(types.Content(
    role='user',
    parts=[types.Part.from_text(text="Hello")]
))
queue.close()

# Receive AUDIO output
async for event in runner.run_live(...):
    if event.server_content:
        for part in event.server_content.parts:
            if part.inline_data:  # Audio chunks received!
                audio_data = part.inline_data.data
                player.play_pcm_bytes(audio_data)
```

**This works perfectly** - proven by `make basic_demo_audio`

## Conclusions

### What Works ✅
1. **Text input + Audio output** via ADK `Runner.run_live()`
2. **Audio recording** from microphone via PyAudio
3. **Audio playback** through speakers via PyAudio
4. **Direct Live API** with `genai.Client` (bypasses ADK agents)

### What Doesn't Work ❌
1. **Audio input** via `LiveRequestQueue.send_realtime()` + `Runner.run_live()`
2. Full bidirectional voice (microphone → agent → speakers) via ADK Runner

### Why This Matters

The ADK framework appears designed for:
- **Text-to-audio**: Traditional chat with voice responses
- **Web UI streaming**: ADK Web UI handles audio/video via WebSockets

But NOT for:
- **Programmatic audio input**: Python scripts sending recorded audio
- **Voice-to-voice**: Microphone input → voice output workflow

## Recommendations

### Option 1: Use Direct Live API (RECOMMENDED)
Bypass ADK agents and use `google.genai.Client` directly:

```python
from google import genai

client = genai.Client()

async with client.aio.live.connect(model=model, config=config) as session:
    # Send audio
    await session.send_realtime_input(audio=Blob(...))
    
    # Receive audio
    async for response in session.receive():
        play_audio(response.data)
```

**Pros**: Official API, proven to work, full audio support  
**Cons**: No ADK agent framework (tools, state management, etc.)

### Option 2: Keep Text Input (CURRENT)
Use what works - text input with audio output:

```python
queue.send_content(types.Content(
    role='user',
    parts=[types.Part.from_text(text="User message")]
))

# Receive audio response
async for event in runner.run_live(...):
    # Play audio chunks
```

**Pros**: Works with ADK agents, tools, state  
**Cons**: No microphone input, text-only interaction

### Option 3: ADK Web UI
Use `adk web` with audio/video buttons in browser:

```bash
adk web
# Open browser, click Audio button, speak
```

**Pros**: Full audio support, ADK agent features  
**Cons**: Not programmatic, requires manual browser interaction

## Next Steps

1. **Document limitation** in Tutorial 15
2. **Update audio_demo.py** to use text input
3. **Add note** about ADK Web UI for full audio
4. **Create separate example** using direct `genai.Client` for audio input
5. **Update MIME type** to `audio/pcm;rate=16000` (with semicolon)

## Files Affected

- `tutorial_implementation/tutorial15/voice_assistant/audio_demo.py` - Needs revision
- `docs/tutorial/15_live_api_audio.md` - Add limitation note
- `tutorial_implementation/tutorial15/README.md` - Clarify audio input limitations

## References

- Official Live API docs: https://ai.google.dev/gemini-api/docs/live
- ADK sample: `research/adk-python/contributing/samples/live_bidi_streaming_single_agent/`
- Working demo: `tutorial_implementation/tutorial15/voice_assistant/basic_demo.py`
