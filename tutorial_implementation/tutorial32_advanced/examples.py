#!/usr/bin/env python
"""
Examples of using the Data Visualization Agent

This script demonstrates common visualization tasks.
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


# Example prompts to try
EXAMPLES = [
    "Create a bar chart showing quarterly revenue: Q1=$100k, Q2=$150k, Q3=$180k, Q4=$200k",
    "Generate a line plot of temperature changes over 12 months",
    "Make a scatter plot with 50 random points",
    "Create a pie chart showing market share: Company A=35%, B=25%, C=20%, D=20%",
    "Generate a sine wave from 0 to 4π",
    "Show a histogram of 1000 normally distributed values",
]


async def run_example(example: str, runner: Runner, session_id: str):
    """Run a single example."""
    print(f"\n{'='*60}")
    print(f"📊 Request: {example}")
    print(f"{'='*60}")

    try:
        message = types.Content(
            role="user",
            parts=[types.Part(text=example)]
        )

        response_text = ""
        code_shown = False

        async for event in runner.run_async(
            user_id="examples_user",
            session_id=session_id,
            new_message=message
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.executable_code and not code_shown:
                        print(f"\n📝 Generated Code:\n```python\n{part.executable_code.code}\n```")
                        code_shown = True

                    elif part.code_execution_result:
                        status = part.code_execution_result.outcome
                        output = part.code_execution_result.output or ""
                        print(f"\n✅ Execution: {status}")
                        if output:
                            print(f"   Output: {output}")

                    elif part.text and not part.text.isspace():
                        response_text += part.text

            if event.is_final_response():
                if response_text:
                    print(f"\n🤖 Explanation: {response_text}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


async def main():
    """Run all examples."""

    # Verify API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not set")
        return

    # Setup session and runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="examples_app",
        user_id="examples_user"
    )

    runner = Runner(
        agent=root_agent,
        app_name="examples_app",
        session_service=session_service
    )

    print("\n🎨 Data Visualization Agent - Examples")
    print("=" * 60)

    # Run a few examples
    for i, example in enumerate(EXAMPLES[:3], 1):
        await run_example(example, runner, session.id)

    print(f"\n{'='*60}")
    print("✅ Examples completed!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
