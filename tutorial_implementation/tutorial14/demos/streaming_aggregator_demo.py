"""
StreamingResponseAggregator Demo - Tutorial 14

Demonstrates response aggregation using ADK streaming APIs.
Note: ADK may not have StreamingResponseAggregator class, so we implement manual aggregation.
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


class ManualStreamingAggregator:
    """
    Manual implementation of streaming response aggregation.
    Since StreamingResponseAggregator may not be available in current ADK.
    """

    def __init__(self):
        """Initialize aggregator."""
        self.chunks = []
        self.complete_text = ""

    def add_event(self, event):
        """
        Add a streaming event to the aggregation.

        Args:
            event: Streaming event from runner.run_async()
        """
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    self.chunks.append(part.text)
                    self.complete_text += part.text

    def get_response(self):
        """
        Get the complete aggregated response.

        Returns:
            Dict with aggregated response data
        """
        return {
            'content': {
                'parts': [{'text': self.complete_text}]
            },
            'chunks': self.chunks,
            'total_chunks': len(self.chunks),
            'total_length': len(self.complete_text)
        }


async def stream_with_manual_aggregator(query: str, agent: Agent):
    """
    Use manual aggregation for cleaner streaming code.

    Args:
        query: User query
        agent: Agent to use

    Returns:
        Complete response dict
    """
    # Create runner and session
    session_service = InMemorySessionService()
    runner = Runner(app_name="aggregator_demo", agent=agent, session_service=session_service)

    session = await session_service.create_session(
        app_name="aggregator_demo",
        user_id="demo_user"
    )

    run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    # Create manual aggregator
    aggregator = ManualStreamingAggregator()

    print(f"Query: {query}")
    print("Streaming with aggregation: ", end='', flush=True)

    async for event in runner.run_async(
        user_id="demo_user",
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=query)]),
        run_config=run_config
    ):
        # Aggregator handles chunk collection
        aggregator.add_event(event)

        # Display chunk
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end='', flush=True)

        if event.turn_complete:
            break

    # Get complete response
    complete_response = aggregator.get_response()

    print("\n\nAggregation Results:")
    print(f"- Total chunks: {complete_response['total_chunks']}")
    print(f"- Total length: {complete_response['total_length']} characters")

    return complete_response


async def demo_aggregation_patterns():
    """
    Demonstrate different aggregation approaches.
    """
    print("=" * 70)
    print("STREAMING RESPONSE AGGREGATION DEMO")
    print("=" * 70)

    # Create agent
    agent = Agent(
        model='gemini-2.0-flash',
        name='aggregator_demo_agent',
        instruction='Provide detailed responses for aggregation testing.'
    )

    # Demo queries
    queries = [
        "Explain blockchain technology",
        "What are microservices?",
        "How does machine learning work?"
    ]

    for query in queries:
        print(f"\n{'='*50}")
        response = await stream_with_manual_aggregator(query, agent)
        print(f"{'='*50}")

        # Show chunk analysis
        chunks = response['chunks']
        if len(chunks) > 0:
            avg_chunk_size = sum(len(chunk) for chunk in chunks) / len(chunks)
            print(f"Average chunk size: {avg_chunk_size:.1f} chars")
            print(f"Largest chunk: {max(len(chunk) for chunk in chunks)} chars")
            print(f"Smallest chunk: {min(len(chunk) for chunk in chunks)} chars")

        await asyncio.sleep(0.5)  # Brief pause

    print("\n" + "=" * 70)
    print("Aggregation demo completed!")
    print("This demonstrates how to collect streaming chunks into complete responses.")
    print("=" * 70)


async def main():
    """Run the aggregation demo."""
    await demo_aggregation_patterns()


if __name__ == '__main__':
    asyncio.run(main())