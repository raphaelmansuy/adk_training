"""
Basic Streaming Demo - Tutorial 14

Demonstrates the basic streaming implementation using ADK's real streaming APIs.
"""

import asyncio
import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Environment setup
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', 'FALSE')


async def stream_response(query: str):
    """
    Stream agent response using real ADK APIs.

    Args:
        query: User query to process
    """
    # Create agent
    agent = Agent(
        model='gemini-2.0-flash',
        name='streaming_assistant',
        instruction='Provide detailed, helpful responses.'
    )

    # Configure streaming
    run_config = RunConfig(
        streaming_mode=StreamingMode.SSE
    )

    # Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(app_name="streaming_demo", agent=agent, session_service=session_service)

    # Create session
    session = await session_service.create_session(
        app_name="streaming_demo",
        user_id="demo_user"
    )

    print(f"User: {query}\n")
    print("Agent: ", end='', flush=True)

    # Run with streaming
    async for event in runner.run_async(
        user_id="demo_user",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=query)]),
        run_config=run_config
    ):
        # Print each chunk as it arrives
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end='', flush=True)

        # Check for completion
        if event.turn_complete:
            break

    print("\n")


async def main():
    """Run the basic streaming demo."""
    print("=" * 60)
    print("BASIC STREAMING DEMO - Tutorial 14")
    print("=" * 60)

    # Demo queries
    queries = [
        "Explain how neural networks work",
        "What are the benefits of streaming responses?",
        "How does Server-Sent Events work?"
    ]

    for query in queries:
        await stream_response(query)
        await asyncio.sleep(0.5)  # Brief pause between queries

    print("=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(main())