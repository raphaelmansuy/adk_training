"""
Advanced Streaming Patterns Demo - Tutorial 14

Demonstrates all 4 advanced streaming patterns:
1. Response Aggregation
2. Streaming with Progress Indicators
3. Streaming to Multiple Outputs
4. Streaming with Timeout
"""

import asyncio
import os
import sys
from typing import List, Callable
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Environment setup
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', 'FALSE')


class AdvancedStreamingDemo:
    """Demo class for advanced streaming patterns."""

    def __init__(self):
        """Initialize demo with agent and runner."""
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='advanced_streaming_demo',
            instruction='Provide detailed responses for streaming pattern demonstrations.'
        )

        self.session_service = InMemorySessionService()
        self.runner = Runner(app_name="advanced_demo", agent=self.agent, session_service=self.session_service)
        self.run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    async def create_session(self):
        """Create a session for the demo."""
        return await self.session_service.create_session(
            app_name="advanced_demo",
            user_id="demo_user"
        )

    async def pattern_1_response_aggregation(self, query: str) -> tuple[str, List[str]]:
        """
        Pattern 1: Response Aggregation
        Collect the complete response while streaming.

        Args:
            query: User query

        Returns:
            Tuple of (complete_text, chunks_list)
        """
        session = await self.create_session()
        chunks = []

        print("Pattern 1 - Response Aggregation")
        print(f"Query: {query}")
        print("Streaming: ", end='', flush=True)

        async for event in self.runner.run_async(
            user_id="demo_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)]),
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunk = part.text
                        chunks.append(chunk)
                        print(chunk, end='', flush=True)

            if event.turn_complete:
                break

        complete_text = ''.join(chunks)
        print(f"\n\nTotal chunks: {len(chunks)}")
        print(f"Total length: {len(complete_text)} characters")
        return complete_text, chunks

    async def pattern_2_progress_indicators(self, query: str):
        """
        Pattern 2: Streaming with Progress Indicators
        Show progress during streaming.

        Args:
            query: User query
        """
        session = await self.create_session()

        print("\nPattern 2 - Progress Indicators")
        print(f"Query: {query}")
        print("Agent: ", end='', flush=True)

        chunk_count = 0

        async for event in self.runner.run_async(
            user_id="demo_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)]),
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunk = part.text
                        print(chunk, end='', flush=True)

                        chunk_count += 1

                        # Show progress indicator every 5 chunks
                        if chunk_count % 5 == 0:
                            sys.stderr.write('.')
                            sys.stderr.flush()

            if event.turn_complete:
                break

        print()  # New line

    async def pattern_3_multiple_outputs(self, query: str, outputs: List[Callable[[str], None]]):
        """
        Pattern 3: Streaming to Multiple Outputs
        Send streaming response to multiple destinations.

        Args:
            query: User query
            outputs: List of output functions
        """
        session = await self.create_session()

        print("\nPattern 3 - Multiple Outputs")
        print(f"Query: {query}")
        print(f"Sending to {len(outputs)} outputs simultaneously...")

        async for event in self.runner.run_async(
            user_id="demo_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)]),
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunk = part.text
                        # Send to all outputs
                        for output_fn in outputs:
                            output_fn(chunk)

            if event.turn_complete:
                break

        print("\nCompleted streaming to multiple outputs.")

    async def pattern_4_timeout_protection(self, query: str, timeout_seconds: float = 10.0):
        """
        Pattern 4: Streaming with Timeout
        Add timeout protection for streaming.

        Args:
            query: User query
            timeout_seconds: Timeout in seconds
        """
        session = await self.create_session()

        print("\nPattern 4 - Timeout Protection")
        print(f"Query: {query}")
        print(f"Timeout: {timeout_seconds} seconds")
        print("Agent: ", end='', flush=True)

        try:
            async with asyncio.timeout(timeout_seconds):
                async for event in self.runner.run_async(
                    user_id="demo_user",
                    session_id=session.id,
                    new_message=types.Content(role="user", parts=[types.Part(text=query)]),
                    run_config=self.run_config
                ):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                chunk = part.text
                                print(chunk, end='', flush=True)

                    if event.turn_complete:
                        break

        except asyncio.TimeoutError:
            print(f"\n\n[Timeout: Response took longer than {timeout_seconds} seconds]")

        print()


# Output handler functions for Pattern 3
def console_output(chunk: str):
    """Output to console."""
    print(chunk, end='', flush=True)

def file_output(chunk: str):
    """Output to file."""
    with open('streaming_output.txt', 'a', encoding='utf-8') as f:
        f.write(chunk)

def counter_output(chunk: str):
    """Count characters (demonstrates multiple handlers)."""
    if not hasattr(counter_output, 'count'):
        counter_output.count = 0
    counter_output.count += len(chunk)
    # Print count every 50 characters
    if counter_output.count % 50 == 0:
        print(f"[{counter_output.count} chars]", end='', flush=True)


async def main():
    """Run all advanced streaming pattern demos."""
    print("=" * 80)
    print("ADVANCED STREAMING PATTERNS DEMO - Tutorial 14")
    print("=" * 80)

    demo = AdvancedStreamingDemo()

    # Pattern 1: Response Aggregation
    complete, chunks = await demo.pattern_1_response_aggregation(
        "Explain machine learning briefly"
    )

    # Pattern 2: Progress Indicators
    await demo.pattern_2_progress_indicators(
        "Write a short paragraph about artificial intelligence"
    )

    # Pattern 3: Multiple Outputs
    # Clear the output file first
    with open('streaming_output.txt', 'w', encoding='utf-8') as f:
        f.write("Streaming Output Log:\n")

    await demo.pattern_3_multiple_outputs(
        "What are the benefits of renewable energy?",
        outputs=[console_output, file_output, counter_output]
    )

    # Show file contents
    print("\nFile output contents:")
    try:
        with open('streaming_output.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:200] + "..." if len(content) > 200 else content)
    except FileNotFoundError:
        print("No file output found.")

    # Pattern 4: Timeout Protection
    await demo.pattern_4_timeout_protection(
        "Explain the theory of relativity in detail",
        timeout_seconds=5.0  # Short timeout for demo
    )

    print("=" * 80)
    print("All advanced streaming patterns demonstrated!")
    print("=" * 80)


if __name__ == '__main__':
    asyncio.run(main())