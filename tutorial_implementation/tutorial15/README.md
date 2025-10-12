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

### Interactive Voice Mode (Requires Microphone)

```bash
python -m voice_assistant.interactive
```

## Testing

Run all tests:
```bash
make test
```

## Project Structure

```
tutorial15/
├── voice_assistant/
│   ├── __init__.py           # Package initialization
│   ├── agent.py              # VoiceAssistant class (exports root_agent)
│   ├── basic_live.py         # Simple Live API example
│   ├── demo.py               # Text-based demo
│   ├── interactive.py        # Microphone-based interaction
│   ├── advanced.py           # Advanced features examples
│   └── multi_agent.py        # Multi-agent voice sessions
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

**Half-Cascade Audio (Recommended for text+audio)**: `gemini-live-2.5-flash-preview`
**Native Audio (Audio-only)**: `gemini-2.5-flash-native-audio-preview-09-2025`

## Important Notes

- Only ONE response modality per session (TEXT or AUDIO, not both)
- Use `send_content()` for text, `send_realtime()` for audio/video
- Always close the queue with `close()` when done
- Keep voice responses concise (max_output_tokens=150-200)

## Resources

- [Tutorial Documentation](../../docs/tutorial/15_live_api_audio.md)
- [Live API Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini-live)
- [Official Sample](https://github.com/google/adk-python/tree/main/contributing/samples/live_bidi_streaming_single_agent/)
