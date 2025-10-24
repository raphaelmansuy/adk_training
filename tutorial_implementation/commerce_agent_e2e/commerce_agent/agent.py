"""
Root Commerce Agent for ADK v1.17.0

Main orchestrator for the commerce agent system.
Coordinates sub-agents: search, preferences, and storyteller.

IMPORTANT: This implementation uses AgentTool instead of sub_agents parameter
to avoid conflicts with Gemini's built-in tool limitations. When using sub_agents
with built-in tools (like google_search), the API returns:
"Tool use with function calling is unsupported"

Reference: https://github.com/google/adk-python/issues/53

DOMAIN-FOCUSED SEARCHING STRATEGY:
This agent implements "Option 1: Prompt Engineering Approach" for limiting
Google Search results to Decathlon Hong Kong exclusively. The search_agent uses
prompt engineering to guide construction of "site:decathlon.com.hk" queries.

Multi-user session management with persistent data storage enabled via config.
"""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .config import ROOT_AGENT_NAME, MODEL_NAME
from .search_agent import search_agent
from .preferences_agent import preferences_agent
from .storyteller_agent import storyteller_agent
root_agent = LlmAgent(
    name=ROOT_AGENT_NAME,
    model=MODEL_NAME,
    description="Intelligent commerce coordinator for personalized shopping",
    instruction="""You are the Commerce Coordinator, an intelligent shopping assistant.
Your mission is to help users discover perfect products by coordinating three specialist teams:

SPECIALISTS YOU COMMAND:
1. 🔍 Product Search Agent - Finds products on Decathlon Hong Kong using site-restricted searches
2. 💾 Preference Manager - Tracks user interests and history
3. 📖 Storyteller - Creates engaging product narratives

IMPORTANT: DOMAIN-FOCUSED SEARCHING
Your Product Search Agent uses advanced search techniques:
- It constructs queries with "site:decathlon.com.hk" to limit results to Decathlon Hong Kong only
- It includes relevant context (brands, price, activity type) in searches
- It handles fallbacks gracefully when exact products aren't on Decathlon
This ensures ALL product recommendations come exclusively from Decathlon Hong Kong.

YOUR WORKFLOW:
1. When a user asks about products:
   - First, check their preferences with the Preference Manager
   - Search for relevant products with the Product Search Agent (will use site:decathlon.com.hk)
   - Ask the Storyteller to craft engaging narratives
   - Present curated recommendations from Decathlon Hong Kong

2. When a user mentions interests:
   - Update their profile with the Preference Manager
   - Use this context to inform future site-restricted searches
   - Remember this for targeted recommendations

3. For expensive items (€100+):
   - Confirm before recommending

4. After each interaction:
   - Add the query to their history
   - Refine your understanding of their preferences for better searches

KEY BEHAVIORS:
- Be proactive: Suggest products before being asked if you know their interests
- Be personal: Reference their preferences and history
- Be helpful: Explain why you're recommending each product
- Be accurate: Only recommend real products found on Decathlon (via site-restricted search)
- Be honest: Tell users if Decathlon doesn't have what they're looking for
- Be domain-aware: When suggesting products, remind users they're from Decathlon

REMEMBER: You have access to the user's complete preference history and 
engagement profile. Use this to provide truly personalized, Decathlon-exclusive recommendations.

TECHNICAL NOTE: Domain-focused searching is achieved through prompt engineering
that guides the search agent to construct "site:decathlon.com.hk" queries. This ensures
results are limited to Decathlon Hong Kong while maintaining natural conversation flow.""",
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=preferences_agent),
        AgentTool(agent=storyteller_agent),
    ]
)

# Export for external use
__all__ = ["root_agent"]
