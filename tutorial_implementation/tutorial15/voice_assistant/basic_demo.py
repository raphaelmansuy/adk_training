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
    agent = Agent(
        model='gemini-live-2.5-flash-preview',
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
        response_modalities=['text']  # Use string instead of enum to avoid pydantic warning
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
    
    print("=" * 70)
    print("BASIC LIVE API DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demo demonstrates bidirectional streaming with Google's Live API.")
    print("It sends a greeting message and displays the agent's text response.")
    print("The agent is configured with voice output (Puck voice), but only text modality is used here.")
    print("In a full implementation, this would handle real-time audio input/output.")
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
    
    print("🤖 Agent: ", end='', flush=True)
    
    # Start live session with correct parameters
    try:
        async for event in runner.run_live(
            live_request_queue=queue,
            user_id=user_id,
            session_id=session.id,
            run_config=run_config
        ):
            print(f"DEBUG: Received event: {event}")  # Debug print
            if event.content and event.content.parts:
                # Process agent responses
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end='', flush=True)
            else:
                print(f"DEBUG: Event has no content or parts: {event}")
    except Exception as e:
        print(f"\n❌ Error during live session: {e}")
    
    print("\n")
    print("=" * 70)
    print("SESSION COMPLETE")
    print("=" * 70)


def main():
    """Main entry point."""
    # Ensure environment is configured for Vertex AI (required for Live API)
    if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI'):
        print("⚠️  Live API requires Vertex AI authentication:")
        print("   Set GOOGLE_GENAI_USE_VERTEXAI=1")
        print("   Set GOOGLE_CLOUD_PROJECT=your_project_id")
        print("   Authenticate with: gcloud auth application-default login")
        return
    
    asyncio.run(basic_live_session())


if __name__ == '__main__':
    main()
