# Tutorial 15: Working Demo Analysis & Path Forward

**Date**: October 12, 2025  
**Status**: ⚠️ Demo Timeout Issue

## Problem

`basic_demo.py` times out with "keepalive ping timeout" error after model name was corrected to `gemini-2.0-flash-live-preview-04-09`.

## Official ADK Sample vs Our Implementation

### Official Sample (`research/adk-python/contributing/samples/live_bidi_streaming_single_agent/`)

- **How it works**: Uses `adk web` interactive UI
- **No programmatic `run_live()` call in agent.py**
- **User interactions**: Through browser with audio/video button clicks
- **Documentation**: Instructs to click Audio/Video button to start stream

### Our Implementation (`tutorial15/voice_assistant/basic_demo.py`)

- **How it works**: Programmatic `runner.run_live()` call  
- **Pattern**: Direct script execution with `python -m voice_assistant.basic_demo`
- **Problem**: Times out during `run_live()` iteration

## Key Findings

### 1. Pydantic Warning is Harmless

The warning about `response_modalities` expecting enum but getting string is **expected behavior**:

```python
# ADK RunConfig internally converts enum to string
run_config = RunConfig(
    response_modalities=[types.Modality.AUDIO]  # We pass enum
)
# Internally becomes: ['AUDIO'] string list
```

This is not the root cause of timeout.

### 2. No Programmatic Live API Examples in ADK Source

- ✅ Found: ADK web UI integration (browser-based)
- ❌ Not found: Standalone Python script using `runner.run_live()`
- 📝 Documentation: Focuses on `adk web` for Live API demos

### 3. Timeout Occurs During Event Iteration

```python
async for event in runner.run_live(
    live_request_queue=queue,
    user_id=user_id,
    session_id=session.id,
    run_config=run_config
):
    # Never reaches this point - times out before first event
```

## Hypothesis

**The Live API through ADK Runner may be designed primarily for web UI integration**, not standalone script execution.

Potential issues:
1. Missing configuration for programmatic use
2. Websocket connection not completing without browser context
3. ADK Runner expecting HTTP server context (like `adk web` provides)

## Path Forward - 3 Options

### Option 1: Use ADK Web Interface (Recommended)

Follow the official sample pattern:

```bash
cd tutorial_implementation/tutorial15
adk web

# Then open browser and click Audio/Video button
```

**Pros**:
- Matches official documentation
- Guaranteed to work (official sample pattern)
- Full Live API features (audio/video UI buttons)

**Cons**:
- Not suitable for automated demos
- Requires manual browser interaction

### Option 2: Use Direct genai.Client (Already Implemented)

Use `direct_live_audio.py` which bypasses ADK Runner:

```python
# Uses google.genai.Client directly
async with client.aio.live.connect(model=model, config=config) as session:
    # Direct audio input/output
    await session.send(input=audio_blob)
```

**Pros**:
- Works programmatically in scripts
- Full control over Live API connection
- Already implemented and tested

**Cons**:
- Bypasses ADK Runner/Agent framework
- No multi-agent support
- Manual session management

### Option 3: Debug ADK Runner.run_live()

Investigate why `run_live()` times out:

```python
# Add debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check websocket connection
# Review ADK source for missing config
# Test with minimal example
```

**Pros**:
- Would enable programmatic ADK integration
- Better for multi-agent scenarios

**Cons**:
- Time-consuming investigation
- May require ADK framework changes
- Unclear if supported use case

## Recommendation

**For Tutorial 15**:

1. **Primary Demo**: Document `adk web` usage (matches official sample)
2. **Programmatic Alternative**: Use `direct_live_audio.py` for script-based demos
3. **Update Documentation**: Clarify that Live API works best with `adk web` UI

This aligns with official ADK patterns and provides both interactive and programmatic options.

## Next Steps

1. ✅ Update README to emphasize `adk web` as primary method
2. ✅ Keep `direct_live_audio.py` as working programmatic alternative
3. ✅ Add troubleshooting section explaining timeout issue
4. ⏳ Consider filing GitHub issue with ADK team about programmatic `run_live()` support
