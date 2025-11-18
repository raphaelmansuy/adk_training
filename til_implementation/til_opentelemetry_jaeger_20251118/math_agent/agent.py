"""
ADK Math Agent with OpenTelemetry instrumentation.
Demonstrates distributed tracing with Jaeger backend.
"""

import asyncio
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from math_agent.tools import add_numbers, subtract_numbers, multiply_numbers, divide_numbers

# Initialize OpenTelemetry FIRST (before any ADK imports)
from math_agent.otel_config import initialize_otel

initialize_otel()


# Create tools (description comes from function docstrings)
add_tool = FunctionTool(func=add_numbers)
subtract_tool = FunctionTool(func=subtract_numbers)
multiply_tool = FunctionTool(func=multiply_numbers)
divide_tool = FunctionTool(func=divide_numbers)

# Create root agent
root_agent = Agent(
    name="math_assistant",
    model="gemini-2.5-flash",
    description="A helpful math assistant that can perform basic arithmetic operations.",
    instruction="""You are a helpful math assistant. You can add, subtract, multiply, and divide numbers.
When asked to perform math operations, use the appropriate tools.
Always show your work and explain the answer clearly.
If the user asks for division by zero, politely explain that it's not possible.""",
    tools=[add_tool, subtract_tool, multiply_tool, divide_tool],
)


async def run_agent(query: str) -> str:
    """
    Run the agent with a given query and return the response.
    
    Args:
        query: User question
        
    Returns:
        Agent's response text
    """
    response = await root_agent.run(
        input=query,
    )
    return response


async def main():
    """Main entry point for demonstration."""
    queries = [
        "What is 123 + 456?",
        "Calculate 1000 - 234",
        "Multiply 12 by 15",
        "What is 100 divided by 4?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        try:
            result = await run_agent(query)
            print(f"Response: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
