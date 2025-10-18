#!/usr/bin/env python
"""
CLI runner for the Data Visualization Agent

This demonstrates how to use the agent with code execution.
"""

import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from data_viz_agent import root_agent


# Load environment variables
load_dotenv()


async def main():
    """Main entry point for the CLI."""

    # Verify API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not set in .env file")
        print("Please copy .env.example to .env and add your API key")
        return

    # Initialize session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="data_viz_app",
        user_id="cli_user"
    )

    runner = Runner(
        agent=root_agent,
        app_name="data_viz_app",
        session_service=session_service
    )

    print("🎨 Data Visualization Agent with Code Execution")
    print("=" * 50)
    print("Type 'quit' to exit\n")

    # Interactive loop
    while True:
        try:
            user_input = input("\n📊 You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not user_input:
                continue

            print("\n⏳ Agent is thinking...")

            # Create message and run agent
            message = types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )

            # Process streaming response
            response_text = ""
            code_executed = False

            async for event in runner.run_async(
                user_id="cli_user",
                session_id=session.id,
                new_message=message
            ):
                # Check for code execution events
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.executable_code:
                            code_executed = True
                            print(f"\n📝 Code Generated:\n```python\n{part.executable_code.code}\n```")

                        elif part.code_execution_result:
                            print("✅ Code Execution Result:")
                            print(f"   Outcome: {part.code_execution_result.outcome}")
                            if part.code_execution_result.output:
                                print(f"   Output: {part.code_execution_result.output}")

                        elif part.text and not part.text.isspace():
                            response_text += part.text

                # Print final response
                if event.is_final_response() and response_text:
                    print(f"\n🤖 Agent: {response_text}")

            if code_executed and not response_text:
                print("\n✅ Visualization generated successfully!")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
