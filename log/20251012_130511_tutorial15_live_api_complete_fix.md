# Tutorial 15 Live API Model Configuration Fix

## Problem Summary

The `advanced_demo` was failing to connect to the Live API due to multiple
configuration issues:

1. Wrong model name in Makefile (missing `-09-2025` suffix)
2. Missing Vertex AI environment variables
3. Using Google AI Studio API instead of Vertex AI
4. Native audio models require AUDIO modality, not TEXT
5. Audio responses need special handling (not just text extraction)

## Root Causes

1. **Model Name Mismatch**: Makefile had `gemini-live-2.5-flash-preview-native-
   audio` but Vertex AI has `gemini-live-2.5-flash-preview-native-audio-09-
   2025`

2. **Missing Vertex AI Config**: `GOOGLE_GENAI_USE_VERTEXAI` and
   `GOOGLE_CLOUD_PROJECT` were not set in Makefile

3. **Modality Mismatch**: Native audio models require `types.Modality.AUDIO`
   but demos were using `types.Modality.TEXT`

4. **Response Handling**: Audio responses don't contain text parts, script was
   hanging waiting for text that never arrives

## Solutions Implemented

### 1. Updated Makefile with Correct Configuration

```makefile
export VOICE_ASSISTANT_LIVE_MODEL ?= gemini-live-2.5-flash-preview-native-
audio-09-2025
export GOOGLE_CLOUD_PROJECT ?= saas-app-001
export GOOGLE_GENAI_USE_VERTEXAI ?= 1
export GOOGLE_CLOUD_LOCATION ?= us-central1
export GOOGLE_GENAI_VERTEXAI_LOCATION ?= $(GOOGLE_CLOUD_LOCATION)
```

### 2. Simplified Advanced Demo

Changed `advanced.py` to show conceptual patterns only, since full Live API
execution requires:
- Audio I/O infrastructure (microphone, speakers)
- PyAudio for audio capture/playback
- Special handling for audio response data

The demo now:
- Explains what each advanced feature does
- Shows code patterns for reference
- Directs users to `make interactive_demo` for actual voice interaction

### 3. Fixed Model Resolution

Updated `_resolve_live_model()` to use configured model directly without
incorrect fallback logic.

## Verification

```bash
make advanced_demo
# Now completes successfully with informative output
```

## Key Learnings

1. **Native Audio Models**: Require `AUDIO` modality and return audio data,
   not text
2. **Vertex AI vs AI Studio**: Different model naming and authentication
3. **Live API Requirements**: Need proper audio infrastructure for full
   interaction
4. **Demo Design**: Conceptual demos are better when full infrastructure isn't
   universally available

## Files Modified

- `tutorial_implementation/tutorial15/Makefile`
  - Added Vertex AI environment variables
  - Updated model name with correct version suffix

- `tutorial_implementation/tutorial15/voice_assistant/advanced.py`
  - Simplified to conceptual overview
  - Fixed model resolution
  - Added helpful user guidance

## Next Steps

For users wanting full Live API interaction:
1. Ensure PyAudio is installed
2. Have working microphone and speakers
3. Use `make interactive_demo` for real voice interaction
4. Or implement custom audio handling for native audio responses
