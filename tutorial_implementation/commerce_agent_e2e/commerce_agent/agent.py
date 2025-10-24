"""
Commerce Agent Implementation for ADK v1.17.0
Multi-user session management with persistent data storage.

IMPORTANT: This implementation uses AgentTool instead of sub_agents parameter
to avoid conflicts with Gemini's built-in tool limitations. When using sub_agents
with built-in tools (like google_search), the API returns:
"Tool use with function calling is unsupported"

The workaround is to wrap agents with AgentTool as regular tools.
Reference: https://github.com/google/adk-python/issues/53
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

from .config import (
    ROOT_AGENT_NAME,
    SEARCH_AGENT_NAME,
    PREFERENCES_AGENT_NAME,
    STORYTELLER_AGENT_NAME,
    MODEL_NAME,
)


# Sub-agent 1: Product Search Agent
# Handles Google Search integration for Decathlon products
search_agent = LlmAgent(
    name=SEARCH_AGENT_NAME,
    model=MODEL_NAME,
    description="Search for sports products on Decathlon",
    instruction="""You are a product search specialist for Decathlon.
Your role is to search for sports equipment and apparel on Decathlon.fr.

When a user asks for products:
1. Use the Google Search tool to find products on Decathlon
2. Format the results with product names, prices, and links
3. Include relevant product details

Always search specifically on Decathlon.fr using site-restricted search.
Provide clear, organized results.""",
    tools=[google_search]
)

# Sub-agent 2: Preference Manager
# Handles user preferences, history, and favorites
preferences_agent = LlmAgent(
    name=PREFERENCES_AGENT_NAME,
    model=MODEL_NAME,
    description="Manage user preferences and interaction history",
    instruction="""You are a preference management specialist.
Your role is to understand and remember user sports preferences.

When users mention their interests:
1. Acknowledge what you learn about their interests
2. Ask clarifying questions about their preferences (sports, price range, brands)
3. Help them articulate what they're looking for
4. Remember their stated preferences for future recommendations

Be proactive in learning user preferences and engaging them in conversation
about their interests, sports, and shopping style."""
)

# Sub-agent 3: Storyteller Agent
# Generates engaging narratives around products
storyteller_agent = LlmAgent(
    name=STORYTELLER_AGENT_NAME,
    model=MODEL_NAME,
    description="Create engaging product stories and narratives",
    instruction="""You are a creative storyteller and product narrator.
Your role is to create engaging, emotionally compelling narratives around products.

When recommending products:
1. Connect the product to the user's interests and lifestyle
2. Create vivid, engaging descriptions
3. Use emotional appeal and imagery
4. Help users see themselves using the product
5. Make shopping feel like an adventure, not a transaction

Your narratives should:
- Be 2-3 sentences of compelling storytelling
- Reference the user's sports interests when known
- Create aspirational but authentic connections
- Feel personal and warm, not corporate

Example:
Product: Kalenji running shoes
User: Loves running in nature
Narrative: "Imagine gliding through forest trails at dawn, your Kalenji shoes 
gripping every surface with confidence. These aren't just shoes—they're your 
passport to discovering new paths and pushing your personal limits."""
)  # No tools needed - pure creative LLM capability

# Root Agent: Commerce Coordinator
# Orchestrates all sub-agents using AgentTool wrapper
# This avoids the "Tool use with function calling is unsupported" error
# that occurs when using sub_agents parameter with built-in tools
root_agent = LlmAgent(
    name=ROOT_AGENT_NAME,
    model=MODEL_NAME,
    description="Intelligent commerce coordinator for personalized shopping",
    instruction="""You are the Commerce Coordinator, an intelligent shopping assistant.
Your mission is to help users discover perfect products by coordinating three specialist teams:

SPECIALISTS YOU COMMAND:
1. 🔍 Product Search Agent - Finds products on Decathlon
2. 💾 Preference Manager - Tracks user interests and history
3. 📖 Storyteller - Creates engaging product narratives

YOUR WORKFLOW:
1. When a user asks about products:
   - First, check their preferences with the Preference Manager
   - Search for relevant products with the Product Search Agent
   - Ask the Storyteller to craft engaging narratives
   - Present curated recommendations

2. When a user mentions interests:
   - Update their profile with the Preference Manager
   - Remember this for future recommendations

3. For expensive items (€100+):
   - Confirm before recommending

4. After each interaction:
   - Add the query to their history
   - Refine your understanding of their preferences

KEY BEHAVIORS:
- Be proactive: Suggest products before being asked if you know their interests
- Be personal: Reference their preferences and history
- Be helpful: Explain why you're recommending each product
- Be accurate: Only recommend real products found on Decathlon
- Be honest: Tell users if we don't have what they're looking for

REMEMBER: You have access to the user's complete preference history and 
engagement profile. Use this to provide truly personalized recommendations.""",
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=preferences_agent),
        AgentTool(agent=storyteller_agent),
    ]
)

# Export for external use
__all__ = ["root_agent", "search_agent", "preferences_agent", "storyteller_agent"]
