# Tutorial 15: Complete Demo Scripts Removal

## Date

2025-01-12 22:00:00

## Summary

Removed all demo scripts and associated Makefile targets per user request.
Tutorial 15 now focuses solely on the working `adk web` interface for Live API.

## Files Removed

### Demo Scripts

All demo scripts have been removed:

1. **`voice_assistant/demo.py`** - Text-based conversation demo
2. **`voice_assistant/basic_demo.py`** - Live API basic demo (text/audio)
3. **`voice_assistant/advanced.py`** - Advanced features (proactivity, affective)
4. **`voice_assistant/multi_agent.py`** - Multi-agent coordination
5. **`voice_assistant/direct_live_audio.py`** - Direct API audio demo
6. **`voice_assistant/interactive.py`** - Interactive voice (already removed)
7. **`voice_assistant/basic_live.py`** - Duplicate demo (already removed)

### Remaining Core Files

Only essential agent implementation files remain:

- ✅ `voice_assistant/__init__.py` - Package initialization
- ✅ `voice_assistant/agent.py` - Core agent and VoiceAssistant class
- ✅ `voice_assistant/audio_utils.py` - Audio utilities (AudioPlayer, AudioRecorder)

## Makefile Changes

### Removed Targets

- `demo` - Main text-based demo
- `basic_demo_text` - Live API text mode
- `basic_demo_audio` - Live API audio mode
- `direct_audio_demo` - Direct API audio
- `advanced_demo` - Advanced features
- `multi_demo` - Multi-agent demo
- `all_demos` - Run all demos
- `check_audio` - Audio device check
- `audio_deps_check` - Audio dependencies check

### Removed from .PHONY

Updated from:
```makefile
.PHONY: help setup dev test demo clean
.PHONY: basic_demo_text basic_demo_audio advanced_demo multi_demo all_demos
.PHONY: lint format validate
.PHONY: live_env_check audio_deps_check live_smoke live_models_doc live_access_help direct_audio_demo
```

To:
```makefile
.PHONY: help setup dev test clean
.PHONY: lint format validate
.PHONY: live_env_check live_smoke live_models_doc live_access_help
```

### Updated Help Output

**Before** - Had entire "DEMO COMMANDS" section with 7+ demo targets

**After** - Simplified to essential commands:
```
📋 QUICK START:
  make setup    # Install dependencies
  make dev      # Start ADK web interface (✅ RECOMMENDED for Live API)
  make test     # Run comprehensive test suite

🔧 DIAGNOSTICS & SETUP:
  make live_env_check    # Verify Vertex AI Live API configuration
  make live_models_list  # List available Live API models
  make live_smoke        # Quick Vertex Live connectivity smoke test
  make live_models_doc   # Show docs for supported Live API models
  make live_access_help  # Steps to request Gemini Live API activation

🧹 MAINTENANCE:
  make clean    # Remove cache files and artifacts
  make lint     # Check code quality
  make format   # Format code with black
  make validate # Run full validation suite
```

### Updated Setup Instructions

**Before**:
```
2. For text demo (make demo): Add GOOGLE_API_KEY to .env
3. For Live API (make basic_demo): Set GOOGLE_GENAI_USE_VERTEXAI=1
4. Run 'make demo' for basic text conversation
5. Run 'make basic_demo' for real-time streaming
6. For voice features: pip install pyaudio
```

**After**:
```
2. Configure Vertex AI credentials:
   export GOOGLE_GENAI_USE_VERTEXAI=1
   export GOOGLE_CLOUD_PROJECT=your-project
   export GOOGLE_CLOUD_LOCATION=us-central1
   export VOICE_ASSISTANT_LIVE_MODEL=gemini-2.0-flash-live-preview-04-09
3. Run 'make dev' to start ADK web interface
4. Open http://localhost:8000 and select 'voice_assistant'
```

## Test Updates

### Removed Test Functions

**`tests/test_imports.py`**:
- `test_import_demo()`
- `test_import_advanced()`
- `test_import_multi_agent()`
- `test_import_interactive()` (already removed)
- `test_import_basic_live()` (already removed)

**`tests/test_structure.py`**:
- `test_voice_assistant_demo_exists()`
- `test_voice_assistant_advanced_exists()`
- `test_voice_assistant_multi_agent_exists()`
- `test_voice_assistant_interactive_exists()` (already removed)
- `test_voice_assistant_basic_live_exists()` (already removed)

### Test Results

**Before removal**: 41 tests
**After removal**: 35 tests
**Status**: ✅ All passing (2 skipped - integration tests requiring API key)

```
================== 35 passed, 2 skipped, 7 warnings in 4.15s ===================
```

### Coverage

- `voice_assistant/__init__.py`: 100% coverage
- `voice_assistant/agent.py`: 33% coverage (unit tested, integration requires API)
- `voice_assistant/audio_utils.py`: 0% coverage (hardware dependent)

## Remaining Functionality

### Core Components

1. **VoiceAssistant Class** (`voice_assistant/agent.py`)
   - Agent definition with Live API configuration
   - Speech config and voice settings
   - RunConfig with BIDI streaming mode
   - Exports `root_agent` for ADK discovery

2. **Audio Utilities** (`voice_assistant/audio_utils.py`)
   - AudioPlayer for PCM audio playback
   - AudioRecorder for microphone input
   - Audio format conversion utilities
   - Hardware availability checks

### Usage Pattern

**Single recommended workflow**:

```bash
# 1. Setup
make setup

# 2. Configure environment
export GOOGLE_GENAI_USE_VERTEXAI=1
export GOOGLE_CLOUD_PROJECT=your-project
export GOOGLE_CLOUD_LOCATION=us-central1
export VOICE_ASSISTANT_LIVE_MODEL=gemini-2.0-flash-live-preview-04-09

# 3. Start web interface
make dev

# 4. Use in browser
# - Open http://localhost:8000
# - Select 'voice_assistant' from dropdown
# - Click Audio/Microphone button
# - Start conversation
```

## Diagnostics Still Available

The following diagnostic commands remain for troubleshooting:

- `make live_env_check` - Verify Vertex AI configuration
- `make live_models_list` - List available models in your project
- `make live_smoke` - Quick connectivity test
- `make live_models_doc` - Show supported model documentation
- `make live_access_help` - Guide for requesting API access

## Rationale

### Why Remove Demos?

1. **Confusion**: Multiple demo approaches confused users
2. **Non-working**: Most demos used `runner.run_live()` which doesn't work standalone
3. **Single truth**: ADK web is the ONLY working pattern for Live API
4. **Maintenance**: Fewer files to maintain and explain
5. **Clarity**: One clear path reduces decision paralysis

### What Users Should Use

**For Live API with Audio**:
- Use `adk web` (the ONLY working method)
- WebSocket `/run_live` endpoint
- Full ADK agent capabilities
- Browser-based interface

**For Development**:
- Import `VoiceAssistant` class directly
- Use in custom applications
- Integrate with other frameworks
- Access audio utilities as needed

## Impact

### Positive

- ✅ Clear, single path for users
- ✅ No confusing non-working demos
- ✅ Reduced maintenance burden
- ✅ Simpler codebase
- ✅ Focused on working solution

### Considerations

- ⚠️ No command-line demo scripts
- ⚠️ Requires browser for audio interaction
- ⚠️ Must use `adk web` for Live API features

### Migration Path

**For users who want standalone scripts**:

They can still:
1. Import `VoiceAssistant` class
2. Create custom scripts using the agent
3. Use `google.genai.Client` directly (bypassing ADK)

**Example**:
```python
from voice_assistant import VoiceAssistant

# Create assistant
assistant = VoiceAssistant()

# Use in custom application
# (but remember: runner.run_live() needs WebSocket context)
```

## Files Status After Cleanup

### Voice Assistant Package

```
voice_assistant/
├── __init__.py          (3 statements, 100% coverage)
├── agent.py             (149 statements, 33% coverage)
└── audio_utils.py       (138 statements, 0% coverage - hardware)
```

### Tests

```
tests/
├── test_agent.py        (Agent configuration & VoiceAssistant class)
├── test_imports.py      (Package imports & ADK dependencies)
└── test_structure.py    (Project structure validation)
```

### Configuration

```
Makefile                 (Simplified, 4 main targets)
requirements.txt         (Core dependencies)
pyproject.toml          (Package metadata)
.env.example            (Environment template)
README.md               (Documentation)
```

## Next Steps

1. ✅ Demo scripts removed
2. ✅ Makefile cleaned
3. ✅ Tests updated and passing
4. Consider: Update README to reflect changes
5. Consider: Update tutorial documentation
6. Consider: Add quickstart guide for ADK web

## Conclusion

Tutorial 15 is now streamlined to focus on the single working pattern: `adk web`.
This eliminates confusion from non-working demo scripts and provides a clear,
maintainable path for users to work with Live API.

Users can still access the core components (`VoiceAssistant`, audio utilities)
programmatically, but the tutorial emphasizes the proven working approach rather
than attempting patterns that fundamentally don't work with ADK's architecture.
