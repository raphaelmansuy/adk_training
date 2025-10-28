#!/usr/bin/env python3
"""Test script for simplified commerce agent."""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from commerce_agent.agent import root_agent  # Updated import path


async def test_agent():
    """Test the simplified agent with a sample query."""
    
    print("\n" + "="*60)
    print("Testing Simplified Commerce Agent")
    print("="*60 + "\n")
    
    # Use in-memory session service for testing
    session_service = InMemorySessionService()
    runner = Runner(
        session_service=session_service,
        app_name="commerce_agent",
        agent=root_agent
    )
    
    # Test 1: Simple product search
    print("Test 1: Simple Search")
    print("-" * 40)
    result = await runner.run_async(
        "I want to buy trail running shoes under 100 euros"
    )
    
    print("\n🤖 Agent Response:")
    print(result.content.parts[0].text)
    print("\n" + "="*60 + "\n")
    
    # Test 2: With preferences
    print("Test 2: Save Preferences")
    print("-" * 40)
    result2 = await runner.run_async(
        "I'm a beginner runner, budget is 100 euros max, interested in trail running",
        session_id="test_session_123"
    )
    
    print("\n🤖 Agent Response:")
    print(result2.content.parts[0].text)
    print("\n" + "="*60 + "\n")
    
    # Test 3: Search using saved preferences
    print("Test 3: Search with Saved Preferences")
    print("-" * 40)
    result3 = await runner.run_async(
        "Show me some shoes based on my preferences",
        session_id="test_session_123"
    )
    
    print("\n🤖 Agent Response:")
    print(result3.content.parts[0].text)
    
    print("\n" + "="*60)
    print("✅ Test Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("Set it with: export GOOGLE_API_KEY=your_key")
        sys.exit(1)
    
    asyncio.run(test_agent())
