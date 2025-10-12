# Tutorial 15: Live API and Audio - Real-Time Voice Interactions

This implementation demonstrates real-time bidirectional streaming with Gemini's Live API, including voice conversations, audio processing, and advanced features like proactivity and affective dialog.

## Features

- ✅ Bidirectional streaming with `StreamingMode.BIDI`
- ✅ LiveRequestQueue for real-time communication
- ✅ Audio input/output with speech recognition
- ✅ Multiple voice configurations (Puck, Charon, Kore, etc.)
- ✅ Text-based demo mode (no microphone required)
- ✅ Interactive voice mode (requires microphone)
- ✅ Advanced features: proactivity, affective dialog, video streaming
- ✅ Multi-agent voice sessions

## Prerequisites

- Python 3.10+
- Google Cloud project with Vertex AI API enabled
- (Optional) Microphone for interactive voice mode

## Setup

```bash
make setup
```

Configure environment:
```bash
cp .env.example .env
# Edit .env with your Google Cloud credentials
```

## Usage

### Text-Based Demo (No Microphone Required)

```bash
make demo
```

### ADK Web Interface

```bash
make dev
```

Open http://localhost:8000 and select "voice_assistant" from the dropdown.

### Live API Demos

**Text Input + Audio Output** (Recommended - Works with ADK Runner):
```bash
make basic_demo_text    # Text responses
make basic_demo_audio   # Audio responses (plays through speakers)
```

**True Audio Input** (Direct Live API - Bypasses ADK):
```bash
make direct_audio_demo  # Microphone → Agent → Speakers
```

⚠️ **Important Audio Limitation**: The ADK `Runner.run_live()` API currently only supports **text input with audio output**. For true bidirectional audio (microphone input), you must use:
- `make direct_audio_demo` - Direct `genai.Client` API (bypasses ADK agents/tools)
- `make dev` - ADK Web UI with audio button (WebSocket connection)

See [Audio Input Limitation](#audio-input-limitation) below for details.

## Audio Input Limitation

**What Works ✅**:
- Text input → Audio output (via ADK Runner)
- Text input → Text output (via ADK Runner)
- ADK Web UI audio streaming (WebSocket)

**What Doesn't Work ❌**:
- Audio input via `LiveRequestQueue.send_realtime()` + `Runner.run_live()`
- Programmatic microphone input through ADK framework

**Why This Matters**:
ADK Runner doesn't support audio input blobs via `send_realtime()`. For true voice-to-voice interaction, you have two options:

1. **Direct Live API** (`make direct_audio_demo`):
   - Uses `google.genai.Client` directly
   - True bidirectional audio support
   - ❌ No ADK agent features (tools, state management)
   - ✅ Official Google API, proven to work

2. **ADK Web UI** (`make dev`):
   - Full audio support via browser
   - ✅ ADK agent features (tools, state)
   - ❌ Not programmatic, manual interaction

See `log/20251012_152300_tutorial15_audio_input_critical_discovery.md` for detailed analysis.

## Testing

Run all tests:
```bash
make test
```

## Project Structure

```
tutorial15/
├── voice_assistant/
│   ├── __init__.py              # Package initialization
│   ├── agent.py                 # VoiceAssistant class (exports root_agent)
│   ├── audio_utils.py           # Audio recording/playback utilities
│   ├── basic_demo.py            # ✅ Text→Audio demo (WORKS)
│   ├── direct_live_audio.py     # ✅ Audio→Audio demo (Direct API)
│   ├── demo.py                  # Text-based demo
│   ├── advanced.py              # Advanced features examples
│   └── multi_agent.py           # Multi-agent voice sessions
├── tests/
│   ├── test_agent.py         # Agent configuration tests
│   ├── test_imports.py       # Import validation
│   └── test_structure.py     # Project structure tests
├── Makefile
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Available Voices

- **Puck**: Friendly, conversational
- **Charon**: Deep, authoritative
- **Kore**: Warm, professional
- **Fenrir**: Energetic, dynamic
- **Aoede**: Calm, soothing

## Live API Models

**Native Audio (Default)**: `gemini-live-2.5-flash-preview-native-audio`
**Half-Cascade Audio (Text+Audio blend)**: `gemini-live-2.5-flash-preview`
**Additional Native Audio SKUs**: `gemini-2.5-flash-native-audio-preview-09-2025`

## Important Notes

- Only ONE response modality per session (TEXT or AUDIO, not both)
- Use `send_content()` for text, `send_realtime()` for audio/video
- Always close the queue with `close()` when done
- Keep voice responses concise (max_output_tokens=150-200)

## Resources

- [Tutorial Documentation](../../docs/tutorial/15_live_api_audio.md)
- [Live API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini-live)
- [Official Sample](https://github.com/google/adk-python/tree/main/contributing/samples/live_bidi_streaming_single_agent/)
