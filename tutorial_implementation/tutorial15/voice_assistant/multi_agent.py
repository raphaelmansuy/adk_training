"""
Multi-Agent Live Sessions
Demonstrates coordinating multiple agents in voice conversation.
"""

import asyncio
import os
from google.adk.agents import Agent, LiveRequestQueue
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def multi_agent_voice_example():
    """
    Demonstrate multi-agent coordination in live conversation.
    """
    
    print("=" * 70)
    print("MULTI-AGENT VOICE CONVERSATION")
    print("=" * 70)
    print()
    print("Orchestrator coordinates between specialized agents:")
    print("- Greeter: Handles initial contact")
    print("- Expert: Provides detailed answers")
    print()
    print("=" * 70)
    print()
    
    # Create specialized agents
    greeter = Agent(
        model='gemini-live-2.5-flash-preview',
        name='greeter',
        description='Friendly greeting specialist',
        instruction='Greet users warmly and ask how you can help. Be brief and welcoming.'
    )
    
    expert = Agent(
        model='gemini-live-2.5-flash-preview',
        name='expert',
        description='Technical expert',
        instruction='Provide detailed, accurate expert answers to technical questions.'
    )
    
    # Orchestrator agent coordinates the others
    orchestrator = Agent(
        model='gemini-live-2.5-flash-preview',
        name='orchestrator',
        description='Multi-agent coordinator',
        instruction="""
You coordinate between multiple specialized agents:

- Use 'greeter' agent for initial user contact and welcomes
- Use 'expert' agent for detailed technical questions
- Ensure smooth conversation flow between agents
- Make it feel like a natural conversation

When a user first arrives, route to greeter.
When they ask technical questions, route to expert.
        """.strip(),
        sub_agents=[greeter, expert]
    )
    
    # Configure live streaming
    run_config = RunConfig(
        streaming_mode=StreamingMode.BIDI,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Puck'
                )
            )
        ),
        response_modalities=['text']
    )
    
    # Create app and runner
    app = App(name='multi_agent_voice', root_agent=orchestrator)
    session_service = InMemorySessionService()
    runner = Runner(app=app, session_service=session_service)
    
    # Create session
    user_id = 'multi_agent_user'
    session = await runner.session_service.create_session(
        app_name=app.name,
        user_id=user_id
    )
    
    # Conversation flow
    messages = [
        "Hello! I'm new here.",
        "Can you explain quantum computing?",
        "That's helpful, thank you!"
    ]
    
    for message in messages:
        queue = LiveRequestQueue()
        
        print(f"🎤 User: {message}")
        
        # Send message
        queue.send_content(
            types.Content(
                role='user',
                parts=[types.Part.from_text(text=message)]
            )
        )
        queue.close()
        
        print("🤖 System: ", end='', flush=True)
        
        # Get response
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
    print("MULTI-AGENT SESSION COMPLETE")
    print("=" * 70)


async def main():
    """Main entry point."""
    
    # Check environment
    if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI') and not os.getenv('GOOGLE_API_KEY'):
        print("⚠️  Please configure environment variables:")
        print("   Set GOOGLE_GENAI_USE_VERTEXAI=1 and GOOGLE_CLOUD_PROJECT")
        print("   OR set GOOGLE_API_KEY")
        return
    
    await multi_agent_voice_example()


if __name__ == '__main__':
    asyncio.run(main())
