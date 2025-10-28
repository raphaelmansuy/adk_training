

"""Commerce Agent - Simplified and Clean Architecture.

This agent helps users find sports products with Google Search grounding.
Following official ADK sample patterns for simplicity and maintainability.

Note: The grounding callback (create_grounding_callback) should be passed to Runner,
not to the Agent directly. See README for usage example.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import MODEL_NAME, AGENT_NAME
from .tools.search import search_products
from .tools.preferences import save_preferences, get_preferences
from .prompt import commerce_agent_instruction
# Export callback for use in Runner
from .callbacks import create_grounding_callback

root_agent = Agent(
    model=MODEL_NAME,
    name=AGENT_NAME,
    description="A personal sports shopping concierge that provides expert product recommendations using Google Search grounding and saved user preferences",
    instruction=commerce_agent_instruction,
    tools=[
        search_products,  # AgentTool wrapping Google Search
        FunctionTool(func=save_preferences),
        FunctionTool(func=get_preferences),
    ],
)

# Export callback for use with Runner:
# runner = Runner(
#     agent=root_agent,
#     after_model_callbacks=[create_grounding_callback(verbose=True)]
# )
__all__ = ["root_agent", "create_grounding_callback"]
