"""
StreamingMode Configuration Demo - Tutorial 14

Demonstrates different StreamingMode configurations and their usage.
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


async def demo_streaming_modes():
    """
    Demonstrate different streaming mode configurations.
    """
    print("=" * 70)
    print("STREAMING MODE CONFIGURATION DEMO")
    print("=" * 70)

    # Create agent
    agent = Agent(
        model='gemini-2.0-flash',
        name='config_demo_agent',
        instruction='Provide brief, helpful responses for configuration testing.'
    )

    # Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(app_name="config_demo", agent=agent, session_service=session_service)

    # Create session
    session = await session_service.create_session(
        app_name="config_demo",
        user_id="demo_user"
    )

    query = "Explain the difference between SSE and blocking responses in one sentence."

    # Demo 1: SSE Streaming
    print("\n1. SSE Streaming Mode:")
    print("-" * 30)

    sse_config = RunConfig(
        streaming_mode=StreamingMode.SSE
    )

    print("User: " + query)
    print("Agent (SSE): ", end='', flush=True)

    async for event in runner.run_async(
        user_id="demo_user",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=query)]),
        run_config=sse_config
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end='', flush=True)
        if event.turn_complete:
            break

    print("\n")

    # Demo 2: No Streaming (blocking)
    print("\n2. Blocking Mode (No Streaming):")
    print("-" * 35)

    blocking_config = RunConfig(
        streaming_mode=StreamingMode.NONE
    )

    print("User: " + query)
    print("Agent (Blocking): ", end='', flush=True)

    # Collect complete response
    response_parts = []
    async for event in runner.run_async(
        user_id="demo_user",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=query)]),
        run_config=blocking_config
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_parts.append(part.text)
        if event.turn_complete:
            break

    # Print complete response at once
    complete_response = ''.join(response_parts)
    print(complete_response)

    print("\n" + "=" * 70)
    print("Available Streaming Modes:")
    print("- StreamingMode.SSE: Server-Sent Events (one-way streaming)")
    print("- StreamingMode.BIDI: Bidirectional streaming (two-way, for Live API)")
    print("- StreamingMode.NONE: No streaming (default, blocking)")
    print("=" * 70)


async def main():
    """Run the streaming mode configuration demo."""
    await demo_streaming_modes()


if __name__ == '__main__':
    asyncio.run(main())