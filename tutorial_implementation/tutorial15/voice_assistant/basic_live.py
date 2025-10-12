"""
Basic Live API Example
Simple bidirectional streaming with LiveRequestQueue.
"""

import asyncio
import os
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

LIVE_MODEL = os.getenv('VOICE_ASSISTANT_LIVE_MODEL')
TEXT_FALLBACK_MODEL = os.getenv('VOICE_ASSISTANT_LIVE_TEXT_MODEL', 'gemini-live-2.5-flash-preview')


def _resolve_live_model() -> str:
    model = (LIVE_MODEL or TEXT_FALLBACK_MODEL).strip()
    if not model:
        return TEXT_FALLBACK_MODEL
    if 'native-audio' in model or 'native_audio' in model:
        fallback = TEXT_FALLBACK_MODEL
        print("ℹ️  Native-audio Live model detected; using text-capable fallback "
              f"'{fallback}' for scripted demo.")
        return fallback
    return model


async def basic_live_session():
    """
    Demonstrate basic Live API bidirectional streaming.
    
    This example shows:
    - Creating a Live API agent
    - Configuring bidirectional streaming
    - Using LiveRequestQueue for communication
    - Processing real-time responses
    """
    
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
        instruction='You are a helpful voice assistant. Respond naturally to user queries.'
    )
    
    # Configure live streaming
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Puck'  # Friendly, conversational voice
                )
            )
        ),
        response_modalities=[types.Modality.TEXT],
    )
    
    # Create request queue for live communication
    queue = LiveRequestQueue()
    
    # Create app and runner
    app = App(name='basic_live_app', root_agent=agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)
    
    # Create session
    user_id = 'test_user'
    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id
    )
    
    print("=" * 70)
    print("BASIC LIVE API DEMONSTRATION")
    print("=" * 70)
    print()
    print(f"Configured live model: {model_to_use}")
    
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
    
    print("🤖 Agent: ", end='', flush=True)
    
    # Start live session with correct parameters
    async for event in runner.run_live(
        live_request_queue=queue,
        user_id=user_id,
        session_id=session.id,
        run_config=run_config
    ):
        if event.content and event.content.parts:
            # Process agent responses
            for part in event.content.parts:
                if part.text:
                    print(part.text, end='', flush=True)
    
    print("\n")
    print("=" * 70)
    print("SESSION COMPLETE")
    print("=" * 70)


def main():
    """Main entry point."""
    # Ensure environment is configured
    if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI') and not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  Please configure environment variables:")
        print("   Set GOOGLE_GENAI_USE_VERTEXAI=1 and GOOGLE_CLOUD_PROJECT")
        print("   OR set GOOGLE_API_KEY")
        return
    
    asyncio.run(basic_live_session())


if __name__ == '__main__':
    main()
