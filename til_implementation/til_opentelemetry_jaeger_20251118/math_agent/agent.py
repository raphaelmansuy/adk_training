"""
ADK Math Agent with OpenTelemetry instrumentation.
Demonstrates distributed tracing and structured logging with Jaeger backend.

Key Features:
- Automatic trace capture for all agent invocations
- Structured logs correlated with traces
- Tool execution tracing
- LLM request/response logging

**How OTel is configured**: 
- For `adk web`: Set OTEL environment variables, ADK handles the rest
- For standalone demo: We explicitly call initialize_otel_env() for clarity
"""

import asyncio
import logging
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part
from math_agent.tools import add_numbers, subtract_numbers, multiply_numbers, divide_numbers

# Initialize OpenTelemetry FIRST (before any ADK imports)
# 
# For adk web: Use initialize_otel_env() to set env vars (ADK handles setup)
# For demo: Use initialize_otel() to manually set up TracerProvider
#
# We detect the context by checking if __name__ == "__main__" (demo) or not (adk web)
from math_agent.otel_config import initialize_otel_env, initialize_otel, force_flush

# When running as "python -m math_agent.agent", __name__ will be "__main__"
# When imported by adk web, __name__ will be "math_agent.agent"
# We detect this after this module is fully loaded
def _init_otel():
    """Initialize OTel with appropriate approach."""
    # Check if we're running as main (demo) or as an imported module (adk web)
    is_demo = __name__ == "__main__"
    
    if is_demo:
        # For demo: Manually initialize TracerProvider to export traces
        initialize_otel(
            service_name="google-adk-math-agent",
            service_version="0.1.0",
            jaeger_endpoint="http://localhost:4318/v1/traces",
        )
    else:
        # For adk web: Just set environment variables, ADK will handle the rest
        initialize_otel_env(
            service_name="google-adk-math-agent",
            service_version="0.1.0",
            jaeger_endpoint="http://localhost:4318/v1/traces",
        )

# Call initialization
_init_otel()

# Get logger after OTel initialization
logger = logging.getLogger("math_agent")
logger.info("OpenTelemetry configured via environment variables")


# Create tools (description comes from function docstrings)
add_tool = FunctionTool(func=add_numbers)
subtract_tool = FunctionTool(func=subtract_numbers)
multiply_tool = FunctionTool(func=multiply_numbers)
divide_tool = FunctionTool(func=divide_numbers)

logger.info("Created 4 math tools: add, subtract, multiply, divide")

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

logger.info("Created math_assistant agent with gemini-2.5-flash model")


async def run_agent(query: str) -> str:
    """
    Run the agent with a given query and return the response.
    
    Uses InMemoryRunner to manage the invocation. Each invocation automatically 
    creates a trace that includes:
    - Agent invocation details
    - Tool execution spans
    - LLM request/response data
    - OpenTelemetry semantic conventions for gen_ai
    
    ⚠️  CRITICAL for adk web: Spans are flushed after execution to ensure
    they're sent to Jaeger before this function returns.
    
    Args:
        query: User question
        
    Returns:
        Agent's response text
    """
    logger.info(f"Running agent with query: {query}")
    try:
        # Create a runner for this invocation
        runner = InMemoryRunner(agent=root_agent, app_name="math-agent-demo")
        
        # Create session for this user
        session = await runner.session_service.create_session(
            user_id="demo_user",
            app_name="math-agent-demo"
        )
        
        # Prepare user message
        user_message = Content(role="user", parts=[Part(text=query)])
        
        # Run the agent and collect response
        response_text = ""
        async for event in runner.run_async(
            session_id=session.id,
            user_id="demo_user",
            new_message=user_message
        ):
            # Extract text from response events
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text
        
        logger.info("Agent responded successfully")
        
        # ⚠️  CRITICAL: Flush spans/logs to Jaeger BEFORE returning
        # This is especially important for adk web where we're in an async
        # handler that will return immediately. Without this, traces might
        # not reach Jaeger before the request completes.
        force_flush(timeout_millis=5000)
        
        return response_text if response_text else "No response"
    except Exception as e:
        logger.error(f"Agent invocation failed: {e}", exc_info=True)
        # Still try to flush even on error
        force_flush(timeout_millis=5000)
        raise


async def main():
    """Main entry point for demonstration."""
    logger.info("Starting math agent demonstration")
    
    queries = [
        "What is 123 + 456?",
        "Calculate 1000 - 234",
        "Multiply 12 by 15",
        "What is 100 divided by 4?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Query: {query}")
        try:
            result = await run_agent(query)
            print(f"Response: {result}")
        except Exception as e:
            print(f"Error: {e}")
    
    logger.info("Math agent demonstration completed")
    
    # Give time for final spans to be exported
    await asyncio.sleep(1)
    
    # Final flush to ensure all data reaches Jaeger
    force_flush(timeout_millis=5000)


if __name__ == "__main__":
    asyncio.run(main())
