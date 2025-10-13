# Tutorial 20: YAML Configuration - Agent Runner
# Load and run agent from YAML configuration

import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.agents import config_agent_utils

# Environment setup for ADK
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ.get('GOOGLE_CLOUD_PROJECT', 'your-project-id')
os.environ['GOOGLE_CLOUD_LOCATION'] = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')


async def main():
    """Load configuration and run agent with test queries."""

    print("🤖 Loading YAML-configured Customer Support Agent...")
    print("=" * 70)

    try:
        # Load agent from YAML configuration
        agent = config_agent_utils.from_config('root_agent.yaml')
        print(f"✅ Configuration loaded successfully: {agent.name}")
        print(f"   Tools: {len(agent.tools) if hasattr(agent, 'tools') else 0}")
        print()

    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return

    # Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="yaml_config_demo",
        agent=agent,
        session_service=session_service
    )

    # Create a session
    session_id = "demo_session"
    user_id = "demo_user"
    await session_service.create_session(
        session_id=session_id,
        user_id=user_id,
        app_name="yaml_config_demo"
    )

    # Test queries demonstrating different tool capabilities
    queries = [
        "Check the status of customer CUST-001",
        "What's the status of order ORD-001?",
        "Can you track shipment for order ORD-001?",
        "Search the knowledge base for login issues",
        "Run a diagnostic for connection problems",
        "Get billing history for customer CUST-001",
        "Process a refund of $50 for order ORD-002"
    ]

    for i, query in enumerate(queries, 1):
        print(f"Query {i}: {query}")
        print("-" * 70)

        try:
            # Create message content
            from google.genai import types
            message = types.Content(
                parts=[types.Part(text=query)],
                role="user"
            )

            # Execute the query using the ADK Runner
            response_events = []
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=message
            ):
                response_events.append(event)
                if hasattr(event, 'content') and event.content:
                    print(f"Event: {event.content}")

            print(f"Received {len(response_events)} events")
            print()

        except Exception as e:
            print(f"❌ Error running query: {e}")
            print()

        # Small delay between queries
        if i < len(queries):
            await asyncio.sleep(2)

    print("=" * 70)
    print("🎉 Demo complete! The YAML-configured agent is working.")


if __name__ == '__main__':
    asyncio.run(main())