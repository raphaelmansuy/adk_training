"""
Interactive Demo for Interactions API

This script demonstrates the key features of the Interactions API.
Run with: python -m interactions_basic_agent.demo
"""

import os
import sys


def check_api_key():
    """Check if API key is configured."""
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not set!")
        print("")
        print("Set your API key:")
        print("  export GOOGLE_API_KEY='your-key-here'")
        print("")
        print("Get a key at: https://aistudio.google.com/apikey")
        sys.exit(1)


def run_basic_demo():
    """Run basic interaction demo."""
    from . import create_basic_interaction
    
    print("=" * 60)
    print("1️⃣  BASIC INTERACTION")
    print("=" * 60)
    print("")
    print("Sending: 'Tell me a short programming joke.'")
    print("")
    
    try:
        result = create_basic_interaction(
            "Tell me a short programming joke."
        )
        print(f"📝 Response: {result['text']}")
        print(f"🆔 Interaction ID: {result['id'][:20]}...")
        print("")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("")


def run_stateful_demo():
    """Run stateful conversation demo."""
    from . import create_stateful_conversation
    
    print("=" * 60)
    print("2️⃣  STATEFUL CONVERSATION (Server-Side State)")
    print("=" * 60)
    print("")
    print("This demo shows how the API remembers context across turns.")
    print("")
    
    messages = [
        "My favorite programming language is Python.",
        "What is my favorite programming language?",
    ]
    
    try:
        results = create_stateful_conversation(messages)
        
        for i, (msg, result) in enumerate(zip(messages, results), 1):
            print(f"👤 Turn {i}: {msg}")
            print(f"🤖 Model: {result['text']}")
            if result['previous_id']:
                print(f"   (linked to previous: {result['previous_id'][:20]}...)")
            print("")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("")


def run_streaming_demo():
    """Run streaming demo."""
    from . import create_streaming_interaction
    
    print("=" * 60)
    print("3️⃣  STREAMING RESPONSE")
    print("=" * 60)
    print("")
    print("Sending: 'Count from 1 to 5 slowly.'")
    print("")
    print("🤖 Response (streaming): ", end="", flush=True)
    
    try:
        for chunk in create_streaming_interaction(
            "Count from 1 to 5, with a brief pause description between each number."
        ):
            print(chunk, end="", flush=True)
        print("")
        print("")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("")


def run_function_calling_demo():
    """Run function calling demo."""
    from . import create_function_calling_interaction, get_weather_tool
    from .tools import execute_tool
    
    print("=" * 60)
    print("4️⃣  FUNCTION CALLING")
    print("=" * 60)
    print("")
    print("Sending: 'What's the weather in Tokyo?'")
    print("Tool: get_weather")
    print("")
    
    try:
        result = create_function_calling_interaction(
            "What's the weather in Tokyo?",
            tools=[get_weather_tool()],
            tool_executor=execute_tool
        )
        
        if result["tool_calls"]:
            print("🔧 Tool Calls:")
            for call in result["tool_calls"]:
                print(f"   - {call['name']}({call['arguments']})")
            print("")
        
        if result["tool_results"]:
            print("📊 Tool Results:")
            for res in result["tool_results"]:
                print(f"   - {res}")
            print("")
        
        print(f"🤖 Final Response: {result['text']}")
        print("")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("")


def main():
    """Run all demos."""
    print("")
    print("🚀 Interactions API Demo")
    print("========================")
    print("")
    print("This demo showcases the key features of Google's Interactions API.")
    print("")
    
    # Check for API key
    check_api_key()
    
    # Run demos
    run_basic_demo()
    run_stateful_demo()
    run_streaming_demo()
    run_function_calling_demo()
    
    print("=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)
    print("")
    print("Learn more:")
    print("- Interactions API Docs: https://ai.google.dev/gemini-api/docs/interactions")
    print("- Deep Research Agent: https://ai.google.dev/gemini-api/docs/deep-research")
    print("")


if __name__ == "__main__":
    main()
