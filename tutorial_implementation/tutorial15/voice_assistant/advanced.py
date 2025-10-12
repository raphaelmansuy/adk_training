"""
Advanced Live API Features
Examples of proactivity, affective dialog, and video streaming.
"""

import asyncio
import os
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def proactivity_example():
    """
    Demonstrate proactive agent behavior.
    Agent can initiate conversation without user input.
    """
    
    print("=" * 70)
    print("PROACTIVITY EXAMPLE")
    print("=" * 70)
    print()
    print("This example demonstrates an agent that can initiate conversation.")
    print()
    
    # Create proactive agent
    agent = Agent(
        model='gemini-live-2.5-flash-preview',
        name='proactive_assistant',
        instruction="""
You are a proactive assistant that can initiate helpful suggestions.
When appropriate, offer relevant tips or information without being asked.
        """.strip()
    )
    
    # Configure with proactivity
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        
        # Enable proactive responses (requires v1alpha API)
        proactivity=types.ProactivityConfig(
            proactive_audio=True
        ),
        
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Puck'
                )
            )
        ),
        
        response_modalities=['text']
    )
    
    # Create session
    queue = LiveRequestQueue()
    app = App(name='proactive_app', root_agent=agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)
    
    user_id = 'proactive_user'
    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id
    )
    
    # Send initial message
    print("🎤 User: I'm working on a presentation.")
    queue.send_content(
        types.Content(
            role='user',
            parts=[types.Part.from_text(text="I'm working on a presentation.")]
        )
    )
    queue.close()
    
    print("🤖 Agent: ", end='', flush=True)
    
    async for event in runner.run_live(
        live_request_queue=queue,
        user_id=user_id,
        session_id=session.id,
        run_config=run_config
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end='', flush=True)
    
    print("\n")
    print("=" * 70)


async def affective_dialog_example():
    """
    Demonstrate emotion detection in voice.
    Agent adapts responses based on detected emotions.
    """
    
    print("=" * 70)
    print("AFFECTIVE DIALOG EXAMPLE")
    print("=" * 70)
    print()
    print("This example demonstrates emotion-aware responses.")
    print()
    
    # Create emotion-aware agent
    agent = Agent(
        model='gemini-live-2.5-flash-preview',
        name='empathetic_assistant',
        instruction="""
You are an empathetic assistant that responds appropriately to user emotions.
Adjust your tone and response based on the emotional context:
- Happy: Be enthusiastic and encouraging
- Sad: Be supportive and understanding
- Angry: Be calm and helpful
- Neutral: Be professional and informative
        """.strip()
    )
    
    # Configure with affective dialog
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        
        # Enable emotion detection
        enable_affective_dialog=True,
        
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Kore'  # Warm, empathetic voice
                )
            )
        ),
        
        response_modalities=['text']
    )
    
    # Create session
    queue = LiveRequestQueue()
    app = App(name='affective_app', root_agent=agent)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)
    
    user_id = 'affective_user'
    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id
    )
    
    # Test with different emotional contexts
    test_messages = [
        ("I just got promoted at work!", "Happy"),
        ("I'm having a really tough day...", "Sad"),
        ("What's the weather forecast?", "Neutral")
    ]
    
    for message, emotion in test_messages:
        queue = LiveRequestQueue()
        
        print(f"🎤 User ({emotion}): {message}")
        queue.send_content(
            types.Content(
                role='user',
                parts=[types.Part.from_text(text=message)]
            )
        )
        queue.close()
        
        print("🤖 Agent: ", end='', flush=True)
        
        async for event in runner.run_live(
            live_request_queue=queue,
            user_id=user_id,
            session_id=session.id,
            run_config=run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end='', flush=True)
        
        print("\n")
        await asyncio.sleep(0.5)
    
    print("=" * 70)


async def video_streaming_example():
    """
    Demonstrate video streaming (conceptual).
    Note: This requires actual video capture hardware.
    """
    
    print("=" * 70)
    print("VIDEO STREAMING EXAMPLE (CONCEPTUAL)")
    print("=" * 70)
    print()
    print("This shows the pattern for video streaming.")
    print("Actual implementation requires OpenCV and camera.")
    print()
    
    # Create vision agent
    agent = Agent(
        model='gemini-live-2.5-flash-preview',
        name='vision_assistant',
        instruction="""
You analyze video streams in real-time.
Describe what you see and identify objects, gestures, or actions.
        """.strip()
    )
    
    # Configure for video
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        response_modalities=['text']
    )
    
    print("Sample code for video streaming:")
    print()
    print("```python")
    print("import cv2")
    print()
    print("# Capture video")
    print("cap = cv2.VideoCapture(0)")
    print("queue = LiveRequestQueue()")
    print()
    print("while True:")
    print("    ret, frame = cap.read()")
    print("    if not ret:")
    print("        break")
    print()
    print("    # Convert frame to bytes")
    print("    _, buffer = cv2.imencode('.jpg', frame)")
    print("    frame_bytes = buffer.tobytes()")
    print()
    print("    # Send frame to agent")
    print("    queue.send_realtime(")
    print("        blob=types.Blob(")
    print("            data=frame_bytes,")
    print("            mime_type='image/jpeg'")
    print("        )")
    print("    )")
    print()
    print("    await asyncio.sleep(0.1)  # ~10 FPS")
    print()
    print("queue.close()")
    print("```")
    print()
    print("=" * 70)


async def main():
    """Run all advanced examples."""
    
    # Check environment
    if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI') and not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  Please configure environment variables:")
        print("   Set GOOGLE_GENAI_USE_VERTEXAI=1 and GOOGLE_CLOUD_PROJECT")
        print("   OR set GOOGLE_API_KEY")
        return
    
    # Run examples
    await proactivity_example()
    print()
    
    await affective_dialog_example()
    print()
    
    await video_streaming_example()


if __name__ == '__main__':
    asyncio.run(main())
