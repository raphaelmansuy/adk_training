#!/usr/bin/env python3
"""
Demo Script for ADK Interactions Agent

This script demonstrates running the ADK agent with Interactions API
integration both through the ADK web interface and programmatically.

Usage:
    # Interactive demo
    python -m adk_interactions_agent.demo
    
    # Or run the module directly
    python demo.py
    
    # Start ADK web interface
    make dev
"""

import asyncio
import os
import sys
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def check_environment() -> bool:
    """Check if required environment variables are set."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY environment variable not set")
        print("\nTo fix this:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Google API key")
        print("  3. Run this script again")
        return False
    print("✅ GOOGLE_API_KEY is configured")
    return True


def print_demo_header():
    """Print demo header with information."""
    print("=" * 60)
    print("  ADK Interactions Agent Demo")
    print("  Demonstrating Google Interactions API + ADK Integration")
    print("=" * 60)
    print()


def print_demo_prompts():
    """Print suggested demo prompts."""
    prompts = [
        ("🌤️ Weather Query", "What's the weather like in Tokyo?"),
        ("🔢 Math Calculation", "Calculate 15% of 250 plus 100"),
        ("🔍 Knowledge Search", "Tell me about machine learning"),
        ("🔄 Multi-Tool", "What's the weather in Paris? Also calculate 20% tip on $85"),
        ("💭 Reasoning", "Compare the weather in New York and London"),
    ]
    
    print("📋 Suggested Demo Prompts:\n")
    for emoji_name, prompt in prompts:
        print(f"  {emoji_name}:")
        print(f"    \"{prompt}\"\n")


def print_adk_web_instructions():
    """Print instructions for using ADK web interface."""
    print("🌐 ADK Web Interface:\n")
    print("  To start the interactive web UI:")
    print("    make dev")
    print("    # or")
    print("    adk web")
    print()
    print("  Then open http://localhost:8000 in your browser")
    print("  Select 'adk_interactions_agent' from the dropdown")
    print()


def print_programmatic_example():
    """Print example of programmatic usage."""
    print("💻 Programmatic Usage Example:\n")
    code = '''
from adk_interactions_agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

# Create session and runner
session_service = InMemorySessionService()
session = session_service.create_session(
    app_name="demo",
    user_id="user_1"
)

runner = Runner(
    agent=root_agent,
    session_service=session_service
)

# Run a query
response = runner.run(
    session_id=session.id,
    user_message="What's the weather in Tokyo?"
)

print(response.output)
'''
    print(code)


async def run_interactive_demo():
    """Run an interactive demo if API key is available."""
    try:
        from google import genai
        from google.genai import types
        
        print("🚀 Running Interactive Demo...\n")
        
        client = genai.Client()
        
        # Demo the Interactions API directly
        print("📨 Testing Interactions API connection...")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hello! Please respond with a brief greeting.",
        )
        
        print(f"✅ Connection successful!")
        print(f"   Response: {response.text[:100]}...")
        print()
        
        return True
        
    except ImportError:
        print("⚠️ google-genai package not available for interactive demo")
        return False
    except Exception as e:
        print(f"⚠️ Interactive demo error: {e}")
        return False


def main():
    """Main demo entry point."""
    print_demo_header()
    
    # Check environment
    if not check_environment():
        print()
        sys.exit(1)
    
    print()
    
    # Print available demos
    print_demo_prompts()
    print("-" * 60)
    print()
    
    print_adk_web_instructions()
    print("-" * 60)
    print()
    
    print_programmatic_example()
    print("-" * 60)
    print()
    
    # Offer to run interactive demo
    print("🎯 Quick Test:\n")
    try:
        asyncio.run(run_interactive_demo())
    except KeyboardInterrupt:
        print("\n\nDemo cancelled.")
    
    print()
    print("=" * 60)
    print("  Demo complete! Try 'make dev' to start the web interface.")
    print("=" * 60)


if __name__ == "__main__":
    main()
