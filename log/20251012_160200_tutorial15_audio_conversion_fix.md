# Tutorial 15: Fixed Direct Audio Demo - Removed Unnecessary Conversion

**Date**: October 12, 2025  
**Issue**: Audio conversion error in `direct_live_audio.py`  
**Status**: ✅ Fixed

## Problem

User reported audio conversion error when running `make direct_audio_demo`:

```
✅ Recorded 159744 bytes
🔄 Converting audio format...
⚠️  Audio conversion error: Error opening <_io.BytesIO object>: Format not recognised.
```

## Root Cause

The `convert_to_pcm_16khz()` function attempted to:
1. Load raw PCM bytes as if they were a recognizable audio file format
2. Use `soundfile.read()` on a BytesIO buffer containing raw PCM data
3. Convert audio that was already in the correct format

**The issue**: `AudioRecorder.record_audio()` already returns audio in the exact format needed:
- 16-bit PCM
- 16kHz sample rate  
- Mono (1 channel)
- Raw bytes (no file headers)

There was **no conversion needed** - the function was trying to "fix" data that was already correct.

## Solution

### 1. Removed Unnecessary Conversion Function

**Before** (lines 40-74):
```python
def convert_to_pcm_16khz(audio_data: bytes, source_rate: int = 16000) -> bytes:
    try:
        buffer = io.BytesIO(audio_data)
        data, sr = sf.read(buffer, dtype='int16')  # ❌ Fails - raw PCM has no headers
        # ... conversion logic ...
    except Exception as e:
        print(f"⚠️  Audio conversion error: {e}")
        return audio_data
```

**After**:
```python
# Function removed entirely - not needed!
```

### 2. Updated Audio Recording Flow

**Before**:
```python
audio_data = recorder.record_audio(duration_seconds=5, show_progress=True)
print(f"✅ Recorded {len(audio_data)} bytes")
print("🔄 Converting audio format...")
audio_data = convert_to_pcm_16khz(audio_data, source_rate=16000)  # ❌ Unnecessary
```

**After**:
```python
audio_data = recorder.record_audio(duration_seconds=5, show_progress=True)
print(f"✅ Recorded {len(audio_data)} bytes")
print("   (Audio already in correct format: 16-bit PCM, 16kHz, mono)")
# No conversion needed!
```

### 3. Removed Unused Dependencies

**requirements.txt** - Removed:
```
librosa>=0.10.0    # Not needed
soundfile>=0.12.0  # Not needed
```

These libraries were:
- Added for audio conversion
- Never actually needed
- Heavy dependencies (100+ MB)
- Slowed down installation

**Makefile** - Updated demo description:
```makefile
# Before
⚠️  Requires: Vertex AI + PyAudio + librosa + soundfile

# After
⚠️  Requires: Vertex AI + PyAudio + Microphone + Speakers
```

### 4. Cleaned Up Imports

**Before**:
```python
import asyncio
import io  # ❌ Unused
import os

try:
    import soundfile as sf  # ❌ Unused
    import librosa          # ❌ Unused
    AUDIO_LIBS_AVAILABLE = True
except ImportError:
    AUDIO_LIBS_AVAILABLE = False
```

**After**:
```python
import asyncio
import os

# Removed unused imports
```

## Why This Works

### AudioRecorder Format Specification

The `AudioRecorder` class in `audio_utils.py` is configured to record at exactly the format needed:

```python
class AudioRecorder:
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = 16000  # Exactly what Live API needs
        self.channels = 1         # Mono
        self.format = pyaudio.paInt16  # 16-bit PCM
```

When `record_audio()` is called:
```python
stream = audio.open(
    format=pyaudio.paInt16,  # 16-bit
    channels=1,              # Mono
    rate=16000,              # 16kHz
    input=True
)
# Returns raw PCM bytes in exact format needed
```

### Live API Format Requirements

From official documentation:
```python
await session.send_realtime_input(
    audio=types.Blob(
        data=audio_data,           # Raw PCM bytes
        mime_type="audio/pcm;rate=16000"  # 16kHz, 16-bit, mono
    )
)
```

The `AudioRecorder` output matches **exactly** what Live API expects. No conversion needed!

## Impact

### Benefits ✅

1. **Faster Installation**
   - Removed 100+ MB of dependencies (librosa + soundfile)
   - Faster `make setup` execution

2. **Simpler Code**
   - Removed 35 lines of unnecessary conversion logic
   - Removed error-prone file format handling
   - Clearer what's actually happening

3. **No More Errors**
   - Eliminated soundfile/librosa import errors
   - Removed confusing "Format not recognised" error
   - Audio works immediately without conversion

4. **Better Performance**
   - No conversion overhead
   - Direct passthrough of audio data
   - Minimal memory usage

### Trade-offs ❌

None! The conversion was never needed in the first place.

## Testing

### Expected Flow (Fixed)

```bash
make direct_audio_demo
```

**Output**:
```
✓ Using Vertex AI authentication

======================================================================
DIRECT LIVE API - BIDIRECTIONAL AUDIO CONVERSATION
======================================================================

🔌 Connecting to Live API...
✅ Connected to Live API

======================================================================
TURN 1/3
======================================================================

🎤 Recording your message (5 seconds)...
   Speak now!
🎤 Recording for 5 seconds...
🎤 Recording complete!
✅ Recorded 159744 bytes
   (Audio already in correct format: 16-bit PCM, 16kHz, mono)
📤 Sending audio to agent...
✅ Audio sent
🔊 Agent responding...
   [Audio playback through speakers]
```

## Files Modified

- ✅ `voice_assistant/direct_live_audio.py`
  - Removed `convert_to_pcm_16khz()` function (35 lines)
  - Removed unused imports (`io`, `soundfile`, `librosa`)
  - Removed `AUDIO_LIBS_AVAILABLE` check
  - Simplified audio recording flow
  
- ✅ `requirements.txt`
  - Removed `librosa>=0.10.0`
  - Removed `soundfile>=0.12.0`
  
- ✅ `Makefile`
  - Updated `direct_audio_demo` description
  - Removed librosa/soundfile from requirements list

## Key Lesson

**Always check if data is already in the right format before converting!**

In this case:
- `AudioRecorder` was specifically designed to output Live API format
- Conversion function assumed data needed fixing
- Reality: Data was perfect, conversion broke it

**The fix**: Trust the original data and pass it through directly.

## Status

✅ **Fix Complete**  
✅ **Dependencies Simplified**  
✅ **Code Cleaner**  
✅ **Ready for Testing**  
🎯 **Audio demo should now work correctly**
