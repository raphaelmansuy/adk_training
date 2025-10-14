#!/usr/bin/env python3
"""
Tutorial 28 Demo: Multi-LLM Agent Examples
Shows how to use different LLMs via LiteLLM with sample queries
"""

import asyncio
import os
import sys
from typing import Dict, Any

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.adk.runners import Runner
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import InMemorySessionService
from google.genai import types

from multi_llm_agent.agent import root_agent, gpt4o_agent, claude_agent, ollama_agent


async def run_query(agent, query: str, description: str) -> Dict[str, Any]:
    """Run a query with a specific agent and return the result."""
    print(f"\n🤖 {description}")
    print(f"💬 Query: {query}")
    print("-" * 50)

    try:
        # Create runner and session service
        session_service = InMemorySessionService()
        runner = Runner(app_name="multi_llm_demo", agent=agent, session_service=session_service)

        # Create a session for this conversation
        session = await session_service.create_session(
            app_name="multi_llm_demo",
            user_id="demo_user"
        )

        # Configure for non-streaming (complete response)
        run_config = RunConfig(
            streaming_mode=StreamingMode.NONE,
            max_llm_calls=50
        )

        # Collect all response parts
        response_parts = []

        # Run the agent with the query
        async for event in runner.run_async(
            user_id="demo_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)]),
            run_config=run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_parts.append(part.text)

            if event.turn_complete:
                break

        result = ''.join(response_parts)
        print(f"📝 Response: {result}")
        return {"success": True, "result": result, "description": description}

    except Exception as e:
        error_msg = f"❌ Error with {description}: {str(e)}"
        print(error_msg)
        return {"success": False, "error": str(e), "description": description}


async def demo_basic_math():
    """Demo basic mathematical calculations with different LLMs."""
    print("\n" + "="*60)
    print("🧮 DEMO 1: Mathematical Calculations")
    print("="*60)

    query = "What is the square of 15? Please use the calculate_square tool."

    # Test with different agents
    agents = [
        (root_agent, "OpenAI GPT-4o-mini (Default)"),
        (gpt4o_agent, "OpenAI GPT-4o-mini (Alternative)"),
        (claude_agent, "Claude 3.7 Sonnet"),
        (ollama_agent, "Ollama Granite 4 (Local)"),
    ]

    results = []
    for agent, desc in agents:
        result = await run_query(agent, query, desc)
        results.append(result)

    return results


async def demo_weather_info():
    """Demo weather information retrieval."""
    print("\n" + "="*60)
    print("🌤️  DEMO 2: Weather Information")
    print("="*60)

    query = "What's the current weather like in San Francisco? Use the get_weather tool."

    agents = [
        (root_agent, "OpenAI GPT-4o-mini"),
        (claude_agent, "Claude 3.7 Sonnet"),
        (ollama_agent, "Ollama Granite 4 (Local)"),
    ]

    results = []
    for agent, desc in agents:
        result = await run_query(agent, query, desc)
        results.append(result)

    return results


async def demo_sentiment_analysis():
    """Demo sentiment analysis of text."""
    print("\n" + "="*60)
    print("😊 DEMO 3: Sentiment Analysis")
    print("="*60)

    query = "Analyze the sentiment of this text: 'I absolutely love this new AI technology! It's incredibly innovative and has transformed how I work.'"

    agents = [
        (root_agent, "OpenAI GPT-4o-mini"),
        (gpt4o_agent, "OpenAI GPT-4o-mini"),
        (claude_agent, "Claude 3.7 Sonnet"),
        (ollama_agent, "Ollama Granite 4 (Local)"),
    ]

    results = []
    for agent, desc in agents:
        result = await run_query(agent, query, desc)
        results.append(result)

    return results


async def demo_comparison():
    """Demo comparing responses from different LLMs."""
    print("\n" + "="*60)
    print("⚖️  DEMO 4: LLM Comparison")
    print("="*60)

    query = "Explain quantum computing in simple terms that a 10-year-old could understand."

    print(f"🎯 Query: {query}")
    print("\n" + "-"*60)

    agents = [
        (root_agent, "OpenAI GPT-4o-mini"),
        (claude_agent, "Claude 3.7 Sonnet"),
        (ollama_agent, "Ollama Granite 4 (Local)"),
    ]

    responses = {}
    for agent, desc in agents:
        try:
            # Create runner and session service
            session_service = InMemorySessionService()
            runner = Runner(app_name="multi_llm_demo", agent=agent, session_service=session_service)

            # Create a session
            session = await session_service.create_session(
                app_name="multi_llm_demo",
                user_id="demo_user"
            )

            # Configure for non-streaming
            run_config = RunConfig(
                streaming_mode=StreamingMode.NONE,
                max_llm_calls=50
            )

            # Collect response
            response_parts = []
            async for event in runner.run_async(
                user_id="demo_user",
                session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part(text=query)]),
                run_config=run_config
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_parts.append(part.text)

                if event.turn_complete:
                    break

            result = ''.join(response_parts)
            responses[desc] = result
            print(f"\n🤖 {desc}:")
            print(f"   {result}")
        except Exception as e:
            print(f"\n❌ {desc}: Error - {str(e)}")

    return responses


async def main():
    """Main demo function."""
    print("🚀 Tutorial 28: Multi-LLM Agent Demo")
    print("Using LiteLLM to access OpenAI, Claude, and other LLMs")
    print("="*60)

    # Check for required API keys
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    has_ollama = True  # Assume Ollama is available locally

    print("🔑 API Key Status:")
    print(f"   OpenAI: {'✅' if has_openai else '❌'} (Required for GPT models)")
    print(f"   Anthropic: {'✅' if has_anthropic else '❌'} (Required for Claude)")
    print(f"   Ollama: {'✅' if has_ollama else '❌'} (Local Granite 4 model)")
    print()

    if not has_openai and not has_anthropic and not has_ollama:
        print("⚠️  Warning: No API keys or local models detected. Demo may fail.")
        print("   Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or ensure Ollama is running.")
        print()

    # Run demos
    try:
        await demo_basic_math()
        await demo_weather_info()
        await demo_sentiment_analysis()
        await demo_comparison()

        print("\n" + "="*60)
        print("✅ Demo completed!")
        print("="*60)
        print("💡 Key Takeaways:")
        print("   • LiteLLM makes it easy to switch between LLM providers")
        print("   • Each LLM has different strengths (cost, speed, reasoning)")
        print("   • Tools work consistently across different models")
        print("   • Local models like Ollama (Granite 4) provide privacy and offline capability")

    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)