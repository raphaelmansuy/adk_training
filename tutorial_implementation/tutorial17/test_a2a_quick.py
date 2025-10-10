#!/usr/bin/env python3
"""
Quick A2A Communication Test using ADK Runner

Test if the orchestrator can successfully communicate with remote agents
using the corrected agent card URLs via the ADK Runner.
"""

import asyncio
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from a2a_orchestrator.agent import root_agent

async def test_a2a_communication():
    """Test basic A2A communication with a simple query using Runner."""
    
    print("🧪 Testing A2A Communication with ADK Runner...")
    print("=" * 50)
    
    try:
        # Create session service and runner with the orchestrator agent
        session_service = InMemorySessionService()
        runner = Runner(
            app_name="a2a_test", 
            agent=root_agent, 
            session_service=session_service
        )
        
        # Create a session
        session_id = "test_session"
        user_id = "test_user"
        await session_service.create_session(
            session_id=session_id,
            user_id=user_id,
            app_name="a2a_test"
        )
        
        # Simple test query
        test_query = "Write a brief summary about AI trends"
        
        print(f"📝 Query: {test_query}")
        print("\n🤖 Orchestrator Response:")
        print("-" * 30)
        
        # Create message content
        message = types.Content(
            parts=[types.Part(text=test_query)],
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
        
        print(f"\nReceived {len(response_events)} events")
        print("\n✅ A2A Communication Test PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ A2A Communication Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_a2a_communication())
    exit(0 if success else 1)