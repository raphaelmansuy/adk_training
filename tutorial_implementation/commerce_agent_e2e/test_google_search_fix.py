#!/usr/bin/env python3
"""
Test script to verify Google Search tool integration with commerce agent.

This script tests that the search_agent properly uses the google_search tool
to find products on Decathlon Hong Kong.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from commerce_agent import root_agent


# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    print("⚠️  .env file not found. Using environment variables.")


async def test_google_search_integration():
    """Test the Google Search tool integration with commerce agent."""
    
    print("=" * 70)
    print("🔍 Testing Google Search Tool Integration")
    print("=" * 70)
    print()
    
    # Check authentication
    api_key = os.getenv("GOOGLE_API_KEY")
    use_vertex_ai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() == "true"
    
    if api_key:
        print("✅ Using Gemini API (GOOGLE_API_KEY)")
    elif use_vertex_ai:
        print("✅ Using Vertex AI")
    else:
        print("❌ No authentication configured!")
        print("   Please set either GOOGLE_API_KEY or Vertex AI credentials")
        return
    
    print()
    
    # Setup session and runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="commerce_agent_test",
        session_service=session_service
    )
    
    app_name = "commerce_agent_test"
    user_id = "test_user"
    session_id = "test_session_001"
    
    # Create session
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Test queries
    test_queries = [
        "I want running shoes",
        "Find cycling equipment under 200 EUR",
        "Show me hiking boots from Decathlon",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─' * 70}")
        print(f"TEST {i}: {query}")
        print(f"{'─' * 70}")
        
        content = types.Content(
            role='user',
            parts=[types.Part(text=query)]
        )
        
        try:
            response_text = "No response received."
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text = part.text
                    
                    print("\n✅ Agent Response:")
                    print(f"{response_text}")
                    
                    # Check if response contains product information
                    if "decathlon" in response_text.lower():
                        print("\n✓ Response mentions Decathlon")
                    if "price" in response_text.lower() or "€" in response_text:
                        print("✓ Response includes pricing information")
                    if "http" in response_text.lower() or "url" in response_text.lower():
                        print("✓ Response includes product links")
                    
            print()
            
        except Exception as e:
            print(f"❌ Error during query: {e}")
            import traceback
            traceback.print_exc()
    
    print()
    print("=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)
    print()
    print("Summary:")
    print("- If you see product recommendations with Decathlon links")
    print("- And pricing information in EUR/HKD")
    print("- The Google Search tool is working correctly!")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(test_google_search_integration())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
