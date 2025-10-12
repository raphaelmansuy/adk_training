"""
Basic Live API Example
Simple bidirectional streaming with LiveRequestQueue and audio support.
"""

import asyncio
import os
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

try:
    from voice_assistant.audio_utils import AudioPlayer, check_audio_available
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    AudioPlayer = None
    check_audio_available = None

LIVE_MODEL = os.getenv('VOICE_ASSISTANT_LIVE_MODEL')
TEXT_FALLBACK_MODEL = os.getenv('VOICE_ASSISTANT_LIVE_TEXT_MODEL', 'gemini-live-2.5-flash-preview')


def _resolve_live_model() -> str:
    """
    Return the configured Live model directly.
    Native audio models work fine with text responses via fallback in agent.py.
    """
    model = (LIVE_MODEL or TEXT_FALLBACK_MODEL).strip()
    if not model:
        raise RuntimeError(
            "VOICE_ASSISTANT_LIVE_MODEL is not set. "
            "Run 'make live_models_list' to see available models."
        )
    return model


async def basic_live_session(use_audio: bool = True):
    """
    Demonstrate basic Live API bidirectional streaming with audio.
    
    This example shows:
    - Creating a Live API agent
    - Configuring bidirectional streaming with audio
    - Using LiveRequestQueue for communication
    - Processing and playing audio responses
    
    Args:
        use_audio: If True, use audio modality and play responses. If False, use text.
    """
    
    # Check audio availability if requested
    if use_audio:
        if not AUDIO_AVAILABLE:
            print("⚠️  Audio utilities not available. Install PyAudio:")
            print("   pip install pyaudio")
            print("   See AUDIO_SETUP.md for platform-specific instructions.")
            print("\n   Falling back to text mode...")
            use_audio = False
        else:
            audio_ok, error_msg = check_audio_available()
            if not audio_ok:
                print(f"⚠️  {error_msg}")
                print("   Falling back to text mode...")
                use_audio = False
    
    # Create agent for live interaction
    model_to_use = _resolve_live_model()
    if not model_to_use:
        raise RuntimeError(
            "VOICE_ASSISTANT_LIVE_MODEL is not set. Refer to https://ai.google.dev/gemini-api/docs/live#before_you_begin_building"
        )

    agent = Agent(
        model=model_to_use,
        name='live_assistant',
        description='Basic voice assistant for Live API demonstration',
        instruction='You are a helpful voice assistant. Keep responses concise and natural for voice interaction.'
    )
    
    # Configure live streaming based on mode
    if use_audio:
        run_config = RunConfig(
            streaming_mode=StreamingMode.BIDI,
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Puck'  # Friendly, conversational voice
                    )
                )
            ),
            response_modalities=[types.Modality.AUDIO],  # Use enum for proper Pydantic validation
        )
    else:
        # Text mode fallback
        run_config = RunConfig(
            streaming_mode=StreamingMode.BIDI,
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Puck'
                    )
                )
            ),
            response_modalities=[types.Modality.TEXT],  # Use enum for proper Pydantic validation
        )
    
    # Create request queue for live communication
    queue = LiveRequestQueue()
    
    # Create app and runner with session service
    app = App(name='basic_live_app', root_agent=agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)
    
    # Create session
    user_id = 'test_user'
    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id
    )
    
    mode_str = "AUDIO" if use_audio else "TEXT"
    print("=" * 70)
    print(f"BASIC LIVE API DEMONSTRATION - {mode_str} MODE")
    print("=" * 70)
    print()
    print("This demo demonstrates bidirectional streaming with Google's Live API.")
    print(f"Configured live model: {model_to_use}")
    print(f"Response mode: {mode_str}")
    
    if use_audio:
        print("Audio output: Enabled (will play audio through speakers)")
    else:
        print("Text output: Enabled (will display text responses)")
    print()
    
    # Send a test message
    print("🎤 User: Hello, how are you today?")
    queue.send_content(
        types.Content(
            role='user',
            parts=[types.Part.from_text(text="Hello, how are you today?")]
        )
    )
    
    # Close queue to signal end of input
    queue.close()
    
    # Initialize audio player if needed
    audio_player = None
    if use_audio:
        audio_player = AudioPlayer()
        print("🔊 Agent speaking...", flush=True)
    else:
        print("🤖 Agent: ", end='', flush=True)

    # Start live session with correct parameters
    audio_chunks = []
    event_count = 0
    try:
        async for event in runner.run_live(
            live_request_queue=queue,
            user_id=user_id,
            session_id=session.id,
            run_config=run_config
        ):
            event_count += 1
            if event_count == 1:
                print("   (Receiving response...)", flush=True)
            
            if not event.server_content:
                continue
            
            for part in event.server_content.parts:
                # Handle audio response
                if use_audio and part.inline_data:
                    audio_data = part.inline_data.data
                    if audio_data:
                        audio_chunks.append(audio_data)
                        # Play audio chunks in real-time
                        audio_player.play_pcm_bytes(audio_data)
                        print(".", end='', flush=True)  # Progress indicator
                
                # Handle text response (fallback mode)
                elif not use_audio and part.text:
                    print(part.text, end='', flush=True)
        
        if use_audio and audio_chunks:
            # Save complete audio to file
            complete_audio = b''.join(audio_chunks)
            audio_player.save_to_wav(complete_audio, 'response.wav')
            print(f"\n💾 Audio saved to: response.wav ({len(complete_audio)} bytes)")
            
    except Exception as exc:
        error_message = str(exc)
        print(f"\n❌ Error during live session: {error_message}")
        if 'Publisher Model' in error_message or 'NOT_FOUND' in error_message:
            print("   👉 This project/region does not have access to the selected Live API model.")
            print("   👉 Run `make live_models_list` to see which Live models are enabled for your Vertex location.")
            print("   👉 Use `make live_models_doc` for official model ids and request access if needed.")
        elif 'invalid argument' in error_message.lower():
            print("   👉 Native audio model requires 'audio' modality, not 'text'.")
            print("   👉 Try: python -m voice_assistant.basic_demo --audio")
    finally:
        if audio_player:
            audio_player.close()
    
    print("\n")
    print("=" * 70)
    print("SESSION COMPLETE")
    print("=" * 70)


def main():
    """Main entry point."""
    import sys
    
    # Ensure environment is configured for Vertex AI (required for Live API)
    if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI'):
        print("⚠️  Live API requires Vertex AI authentication:")
        print("   Set GOOGLE_GENAI_USE_VERTEXAI=1")
        print("   Set GOOGLE_CLOUD_PROJECT=your_project_id")
        print("   Authenticate with: gcloud auth application-default login")
        return
    if not (os.getenv('GOOGLE_CLOUD_LOCATION') or os.getenv('GOOGLE_GENAI_VERTEXAI_LOCATION')):
        print("⚠️  Live API requires a region. For example:")
        print("   export GOOGLE_CLOUD_LOCATION=us-central1")
        print("   export GOOGLE_GENAI_VERTEXAI_LOCATION=us-central1")
        return
    
    # Check command line arguments
    use_audio = '--audio' in sys.argv or '-a' in sys.argv
    use_text = '--text' in sys.argv or '-t' in sys.argv
    
    # Default to audio if audio utils available, otherwise text
    if not use_text and not use_audio:
        use_audio = AUDIO_AVAILABLE
    elif use_text:
        use_audio = False
    
    asyncio.run(basic_live_session(use_audio=use_audio))


if __name__ == '__main__':
    main()
