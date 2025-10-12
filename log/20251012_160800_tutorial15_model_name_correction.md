# Tutorial 15: Model Name Corrected to Official Vertex AI Live API Model

**Date**: October 12, 2025  
**Issue**: Incorrect model name causing 404 errors  
**Status**: ✅ Fixed

## Problem

The Makefile was using an incorrect model name that doesn't exist in Vertex AI:
- ❌ `gemini-2.5-flash-native-audio-preview-09-2025` (doesn't exist)
- ❌ `gemini-2.5-flash-preview-09-2025` (exists but not for Live API)
- ❌ `gemini-2.0-flash-001` (exists but not for Live API)

## Solution

Based on the official ADK sample code at:
`research/adk-python/contributing/samples/live_bidi_streaming_single_agent/agent.py`

The correct model for Vertex AI Live API is:
✅ **`gemini-2.0-flash-live-preview-04-09`**

## Changes Made

### 1. Makefile
```makefile
# Before
export VOICE_ASSISTANT_LIVE_MODEL ?= gemini-live-2.5-flash-preview-native-audio-09-2025

# After
export VOICE_ASSISTANT_LIVE_MODEL ?= gemini-2.0-flash-live-preview-04-09
```

### 2. direct_live_audio.py
```python
# Before
model = os.getenv('VOICE_ASSISTANT_LIVE_MODEL', 'gemini-2.5-flash-native-audio-preview-09-2025')

# After
model = os.getenv('VOICE_ASSISTANT_LIVE_MODEL', 'gemini-2.0-flash-live-preview-04-09')
```

## Verification

```bash
$ export VOICE_ASSISTANT_LIVE_MODEL=gemini-2.0-flash-live-preview-04-09
$ make live_env_check

🩺 Verifying Vertex Live environment...
   • Live model: gemini-2.0-flash-live-preview-04-09
   ✅ Live model is discoverable in this project/region.
   ✅ Vertex Live prerequisites detected.
```

## Available Vertex AI Models (us-central1)

From the API query:
- `gemini-2.0-flash-001`
- `gemini-2.0-flash-lite-001`
- `gemini-2.5-flash`
- `gemini-2.5-flash-lite`
- `gemini-2.5-flash-preview-09-2025`

**But for Live API specifically**: Use `gemini-2.0-flash-live-preview-04-09`

## Official ADK Sample Reference

From `research/adk-python/contributing/samples/live_bidi_streaming_single_agent/agent.py`:

```python
root_agent = Agent(
    # model='gemini-2.0-flash-live-preview-04-09',  # for Vertex project
    model='gemini-2.0-flash-live-001',  # for AI studio key
    ...
)
```

## Remaining Issues

Pydantic warnings about response_modalities - need to use enum values instead of strings.

## Status

✅ **Model Name Fixed**  
✅ **Environment Check Passes**  
⚠️  **Minor Pydantic warnings** (non-blocking)  
🎯 **Ready for Demo Testing**
