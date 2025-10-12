# Tutorial 15: Makefile and Non-Working Scripts Cleanup

## Date

2025-01-12 21:55:00

## Summary

Cleaned up Tutorial 15 Makefile and removed non-working demo scripts based
on confirmed findings about `runner.run_live()` limitations.

## Files Removed

### 1. `voice_assistant/interactive.py`

**Why removed**: Attempted to use audio input through ADK Runner which doesn't
work.

**What it tried to do**:
- Record audio from microphone
- Send to `runner.run_live()` via `send_realtime()`
- This pattern is not supported by ADK Runner

**Replacement**: Use `adk web` for bidirectional audio or
`direct_live_audio.py` for direct API access.

### 2. `voice_assistant/basic_live.py`

**Why removed**: Complete duplicate of `basic_demo.py` with identical
functionality.

**Redundancy**: Both files demonstrated the same Live API pattern with
`LiveRequestQueue`.

**Replacement**: Use `basic_demo.py` (kept) or preferably `adk web`.

## Makefile Changes

### Updated Quick Start Section

**Before**:
```makefile
make setup    # Install dependencies
make demo     # Run text-based demo (API key or Vertex AI)
make basic_demo # Live API streaming demo (requires Vertex AI)
```

**After**:
```makefile
make setup    # Install dependencies
make dev      # Start ADK web interface (✅ RECOMMENDED for Live API)
make demo     # Run text-based demo (API key or Vertex AI)
```

### Enhanced `dev` Target

Added comprehensive usage instructions emphasizing that `adk web` is the
working method for Live API:

```makefile
dev:
	@echo "✅ This is the WORKING method for Live API bidirectional streaming"
	@echo ""
	@echo "📋 Prerequisites:"
	@echo "   • Vertex AI: Set GOOGLE_GENAI_USE_VERTEXAI=1"
	@echo "   • Project: Set GOOGLE_CLOUD_PROJECT=your-project"
	@echo "   • Region: Set GOOGLE_CLOUD_LOCATION=us-central1"
	@echo "   • Model: Set VOICE_ASSISTANT_LIVE_MODEL=..."
	@echo ""
	@echo "🎯 Usage:"
	@echo "   1. Open http://localhost:8000 in your browser"
	@echo "   2. Select 'voice_assistant' from the dropdown"
	@echo "   3. Click the Audio/Microphone button (🎤)"
	@echo "   4. Start typing or speaking"
```

### Removed Targets

- `interactive_demo` - Pointed to non-working audio input demo
- `live_audio_demo` - Alias to interactive_demo
- Duplicate `basic_demo` target (kept only `basic_demo_text` and
`basic_demo_audio`)

### Updated Demo Descriptions

**`basic_demo_audio`**:
- Changed: "✅ WORKS" → "requires 20-30s"
- Clarified it works but is slow

**`all_demos`**:
- Removed: "For voice interaction: make interactive_demo"
- Added: "For Live API with audio: make dev (start ADK web interface)"
- Added: "For direct audio I/O: make direct_audio_demo"

## Test Updates

### Removed Tests

**`tests/test_imports.py`**:
- Removed: `test_import_interactive()`
- Removed: `test_import_basic_live()`

**`tests/test_structure.py`**:
- Removed: `test_voice_assistant_interactive_exists()`
- Removed: `test_voice_assistant_basic_live_exists()`

### Test Results

**Before cleanup**: 45 tests, 2 failures
**After cleanup**: 41 tests, all pass ✅

```
================== 41 passed, 2 skipped, 7 warnings in 4.25s ===================
```

## Remaining Working Demos

### ✅ Fully Working

1. **`make dev`** (adk web) - **RECOMMENDED**
   - Bidirectional audio streaming
   - Full ADK agent capabilities
   - WebSocket `/run_live` endpoint
   - Browser-based interface

2. **`make demo`** - Text conversation demo
   - Works with API keys or Vertex AI
   - Simple text-based interaction
   - No Live API required

3. **`make direct_audio_demo`** - Direct API audio
   - True audio input → audio output
   - Bypasses ADK Runner limitations
   - Uses `google.genai.Client` directly

### ⚠️ Works but Slow

4. **`make basic_demo_text`** - Live API text mode
   - Text input → text output
   - Single turn demonstration
   - 20-30 second response time

5. **`make basic_demo_audio`** - Live API audio output
   - Text input → audio output
   - Single turn demonstration
   - 20-30 second response time

### 📚 Educational

6. **`make advanced_demo`** - Advanced features
   - Proactivity examples
   - Affective dialog patterns
   - Educational demonstrations

7. **`make multi_demo`** - Multi-agent coordination
   - Sequential agent workflows
   - Agent composition patterns

## Key Insights Documented

### What Works

- **ADK web** (`/run_live` WebSocket endpoint)
- **Direct genai.Client API** (bypasses ADK Runner)
- **Single-turn text demos** (basic_demo.py)

### What Doesn't Work

- **Standalone `runner.run_live()` scripts** (no WebSocket context)
- **Audio input via `send_realtime()`** (not supported in ADK Runner)
- **Interactive audio loops** (require active WebSocket connection)

## Recommendations for Users

1. **For Live API**: Use `make dev` to start ADK web interface
2. **For quick testing**: Use `make demo` for text-based demos
3. **For true audio I/O**: Use `make direct_audio_demo`
4. **Avoid**: Trying to create standalone `runner.run_live()` scripts

## Files Status

### Kept (Working)

- ✅ `voice_assistant/agent.py` - Core agent definition
- ✅ `voice_assistant/audio_utils.py` - Audio utilities
- ✅ `voice_assistant/demo.py` - Text-based demo
- ✅ `voice_assistant/basic_demo.py` - Live API demo (slow but works)
- ✅ `voice_assistant/direct_live_audio.py` - Direct API alternative
- ✅ `voice_assistant/advanced.py` - Advanced patterns
- ✅ `voice_assistant/multi_agent.py` - Multi-agent demo

### Removed (Non-Working)

- ❌ `voice_assistant/interactive.py` - Audio input doesn't work
- ❌ `voice_assistant/basic_live.py` - Duplicate functionality
- ❌ `voice_assistant/basic_demo_fixed.py` - Attempted fix that didn't work

## Next Steps

1. ✅ Cleanup complete
2. ✅ Tests passing (41/41)
3. ✅ Makefile streamlined
4. Consider: Update tutorial documentation to match Makefile changes
5. Consider: Add troubleshooting guide about WebSocket requirement

## Impact

- **Clearer user experience**: Removed confusing non-working options
- **Better guidance**: Emphasizes working solutions (adk web, direct API)
- **Reduced confusion**: No misleading demo names or targets
- **Maintainability**: Fewer files to maintain and explain
