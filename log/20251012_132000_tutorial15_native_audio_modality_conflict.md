# Tutorial 15: Native Audio Model Modality Conflict Resolution

**Date**: 2025-01-12 13:20:00  
**Status**: Documented - Known Limitation  
**Issue**: Native audio Live API model incompatible with TEXT modality demos

## Problem Summary

The configured model `gemini-live-2.5-flash-preview-native-audio-09-2025` is a **native audio model** that only supports AUDIO response modality, but all demos are configured for TEXT modality. This causes websocket error 1007 "Request contains an invalid argument".

## Error Details

```
Connection closed: received 1007 (invalid frame payload data) Request contains an invalid argument.; 
then sent 1007 (invalid frame payload data) Request contains an invalid argument.
```

**Pydantic Warning (Secondary)**:
```
PydanticSerializationUnexpectedValue(Expected `enum` - serialized value may not be as expected 
[field_name='response_modalities', input_value='text', input_type=str])
```

## Root Cause

Native audio Live models:
- **Require**: `response_modalities=['audio']` OR `response_modalities=[types.Modality.AUDIO]`
- **Don't support**: TEXT response modality
- **Return**: Binary audio data, not text transcriptions
- **Need**: Audio playback infrastructure (PyAudio, speakers)

Current demos:
- **Use**: `response_modalities=['text']` for simpler demo execution
- **Expect**: Text responses they can print to console
- **Don't have**: Audio playback capabilities

## Why Native Audio Model Works in Playground

Vertex AI playground:
- Has built-in audio playback UI
- Handles audio responses properly
- Uses browser Web Audio API
- Shows waveforms and plays audio

Python demos:
- Console/terminal output only
- No audio playback UI
- Would need PyAudio + manual audio handling
- Can't easily "show" binary audio data

## Solutions

### Option 1: Use Text-Capable Live Model (Recommended for Demos)

Switch to half-cascade model that supports both text and audio:

```bash
# In Makefile or environment
export VOICE_ASSISTANT_LIVE_MODEL="gemini-live-2.5-flash-preview"
```

**Pros**:
- Works with existing demo code
- Returns text responses that can be printed
- No audio infrastructure needed

**Cons**:
- Model name `gemini-live-2.5-flash-preview` may not exist in Vertex us-central1
- Needs verification of available text-capable Live models in your region

### Option 2: Accept Audio-Only Operation

Keep native audio model but accept audio responses:

```python
run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name='Puck'
            )
        )
    ),
    response_modalities=['audio'],  # AUDIO not TEXT
)

# Then handle binary audio in response loop:
async for event in runner.run_live(...):
    if event.server_content:
        for part in event.server_content.parts:
            if part.inline_data:  # Binary audio data
                audio_bytes = part.inline_data.data
                # Need to play audio with PyAudio or save to file
                # Can't just print to console
```

**Pros**:
- Uses the actual native audio model you have access to
- Authentic Live API audio experience

**Cons**:
- Requires PyAudio installation and configuration
- Needs audio playback code
- Demos become platform-dependent (audio hardware)
- Can't run in CI/CD without audio device mocking

### Option 3: Conceptual Demo (Current Approach)

Keep demos educational/conceptual without actual execution:

```python
def main():
    print("=" * 70)
    print("NATIVE AUDIO LIVE API - CONCEPTUAL OVERVIEW")
    print("=" * 70)
    print()
    print("This demo shows Live API patterns but doesn't execute audio.")
    print("Full audio execution requires:")
    print("  1. Native audio model (✓ gemini-live-2.5-flash-preview-native-audio-09-2025)")
    print("  2. Audio I/O infrastructure (PyAudio + microphone/speakers)")
    print("  3. Binary audio handling code")
    print()
    print("For interactive testing, use Vertex AI playground at:")
    print("  https://console.cloud.google.com/vertex-ai/generative/language/prompt-gallery")
```

**Pros**:
- Shows patterns and concepts
- Works everywhere (no audio deps)
- Educational value preserved

**Cons**:
- Not fully executable
- Users can't experience actual audio interaction
- Less impressive as a demo

## Current State

**Working**:
- ✅ `make live_smoke` - Verifies Vertex AI text API connectivity
- ✅ `make advanced_demo` - Shows conceptual patterns
- ✅ `make demo` - Text-based conversation with fallback to text API

**Not Working** (Expected):
- ⚠️ `make basic_demo` - Native audio model rejects TEXT modality
- ⚠️ `make basic_live` - Same issue
- ⚠️ Audio-based interactive demos - Need audio infrastructure

## Recommendations

### For Learning/Tutorial Purposes

1. **Document the limitation clearly** in README and tutorial
2. **Keep conceptual demos** (current advanced_demo approach)
3. **Add note** about Vertex AI playground for actual audio testing
4. **Provide audio infrastructure setup guide** as optional advanced section

### For Production Use

1. **Verify available models** with `gcloud ai models list --region=us-central1 --filter="displayName:live"`
2. **Choose appropriate model**:
   - Text-capable for text-based UIs
   - Native audio for voice-first applications
3. **Implement proper audio handling** if using native audio:
   - PyAudio for capture/playback
   - Audio format conversion (PCM 16-bit, 16kHz mono)
   - Error handling for audio device issues

## Files Modified

- `tutorial_implementation/tutorial15/voice_assistant/basic_demo.py`
  - Fixed `_resolve_live_model()` to use configured model directly
  - Updated response_modalities to use string 'text'
  
- `tutorial_implementation/tutorial15/voice_assistant/agent.py`
  - Added comment about Pydantic serialization workaround

- `tutorial_implementation/tutorial15/voice_assistant/advanced.py`
  - Simplified to conceptual overview
  - Removed audio execution code

- `tutorial_implementation/tutorial15/scripts/smoke_test.py` (NEW)
  - Created dedicated script for Makefile smoke test
  - Uses text model to verify Vertex AI connectivity

- `tutorial_implementation/tutorial15/Makefile`
  - Fixed `live_smoke` target to call Python script instead of inline code
  - All Vertex AI environment variables configured

## Next Steps

**Option A - Stay with Native Audio Model**:
- Accept current conceptual demo approach
- Document in README that full audio requires additional setup
- Reference Vertex AI playground for interactive testing

**Option B - Find Text-Capable Live Model**:
- Contact Google Cloud support about text-capable Live models in us-central1
- Check if `gemini-2.0-flash-live-preview-04-09` is available
- Update `VOICE_ASSISTANT_LIVE_MODEL` if found

**Option C - Implement Audio Infrastructure**:
- Add PyAudio to requirements.txt
- Create audio playback utilities
- Add platform-specific setup instructions
- Make demos fully executable with audio I/O

## References

- **Vertex AI Playground**: https://console.cloud.google.com/vertex-ai/generative/language/prompt-gallery
- **ADK Live API Docs**: https://google.github.io/adk-docs/get-started/streaming/
- **PyAudio**: https://people.csail.mit.edu/hubert/pyaudio/
- **Model Documentation**: Check Vertex AI console for available Live models in your region
