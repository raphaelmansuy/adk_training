"""
Commerce Agent Implementation for ADK v1.17.0
Multi-user session management with persistent data storage.

IMPORTANT: This implementation uses AgentTool instead of sub_agents parameter
to avoid conflicts with Gemini's built-in tool limitations. When using sub_agents
with built-in tools (like google_search), the API returns:
"Tool use with function calling is unsupported"

The workaround is to wrap agents with AgentTool as regular tools.
Reference: https://github.com/google/adk-python/issues/53

DOMAIN-FOCUSED SEARCHING STRATEGY:
This agent implements "Option 1: Prompt Engineering Approach" for limiting
Google Search results to Decathlon.fr exclusively. Rather than using the
`exclude_domains` parameter (which only works on Vertex AI backend), we use
prompt engineering to guide the search_agent to construct "site:decathlon.fr"
queries.

How it works:
1. search_agent receives detailed instructions about site-restricted searches
2. When a user asks for products, search_agent constructs queries like:
   - "site:decathlon.fr running shoes"
   - "site:decathlon.fr women's yoga mat"
3. Google Search automatically limits results to Decathlon.fr
4. This approach works with both Gemini API and Vertex AI backends

Example user queries that trigger Decathlon-focused searches:
- "I need new running shoes"
- "Find me a yoga mat around €40"
- "What cycling helmets does Decathlon have?"
- "Show me beginner mountain bikes"

All searches will automatically be directed to Decathlon via site: operator.
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
# DOMAIN-FOCUSED SEARCHING: Uses prompt engineering to prioritize Decathlon.fr
search_agent = LlmAgent(
    name=SEARCH_AGENT_NAME,
    model=MODEL_NAME,
    description="Search for sports products on Decathlon",
    instruction="""You are a product search specialist for Decathlon.fr.
Your role is to search for sports equipment and apparel exclusively on Decathlon.

CRITICAL SEARCH STRATEGY - Domain-Focused Searching:
When using Google Search, ALWAYS structure your queries to find Decathlon products:

1. PRIMARY METHOD - Site-Restricted Search:
   Include "site:decathlon.fr" in your search query
   Example searches:
   - "site:decathlon.fr running shoes Nike"
   - "site:decathlon.fr women's yoga mat"
   - "site:decathlon.fr mountain bike helmet"
   This directly limits results to Decathlon's website

2. CONTEXT-AWARE SEARCHING:
   If a user mentions a brand, include it: "site:decathlon.fr Kalenji running"
   If a user mentions a price range, add it: "site:decathlon.fr €50 €100 trail shoes"
   If a user mentions a sport/activity, specify it: "site:decathlon.fr beginner cycling"

3. DECATHLON-SPECIFIC TERMINOLOGY:
   Use Decathlon brand names where relevant:
   - Kalenji (running)
   - Quechua (hiking/outdoor)
   - Newfeel (urban sports)
   - Kiprun (trail running)
   - Rockrider (mountain biking)
   - Triban (road cycling)

4. RESULT INTERPRETATION:
   - Always verify results come from decathlon.fr
   - If results don't include Decathlon products, retry with different keywords
   - Focus on Decathlon's own branded products when available

5. FALLBACK HANDLING:
   - If specific product not found on Decathlon, suggest closest Decathlon alternative
   - Be transparent: "We don't have [exact product], but here's what Decathlon offers..."

When a user asks for products:
1. Construct a site-restricted search query with "site:decathlon.fr"
2. Use the Google Search tool with this focused query
3. Format results with product names, prices, and Decathlon links
4. Include relevant product details from the search results
5. Always verify and highlight Decathlon as the source

Provide clear, organized, Decathlon-focused results.""",
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
#
# DOMAIN-FOCUSED SEARCH STRATEGY:
# The search_agent uses prompt engineering with "site:decathlon.fr" queries
# to limit Google Search results to Decathlon products exclusively.
root_agent = LlmAgent(
    name=ROOT_AGENT_NAME,
    model=MODEL_NAME,
    description="Intelligent commerce coordinator for personalized shopping",
    instruction="""You are the Commerce Coordinator, an intelligent shopping assistant.
Your mission is to help users discover perfect products by coordinating three specialist teams:

SPECIALISTS YOU COMMAND:
1. 🔍 Product Search Agent - Finds products on Decathlon using site-restricted searches
2. 💾 Preference Manager - Tracks user interests and history
3. 📖 Storyteller - Creates engaging product narratives

IMPORTANT: DOMAIN-FOCUSED SEARCHING
Your Product Search Agent uses advanced search techniques:
- It constructs queries with "site:decathlon.fr" to limit results to Decathlon only
- It includes relevant context (brands, price, activity type) in searches
- It handles fallbacks gracefully when exact products aren't on Decathlon
This ensures ALL product recommendations come exclusively from Decathlon.

YOUR WORKFLOW:
1. When a user asks about products:
   - First, check their preferences with the Preference Manager
   - Search for relevant products with the Product Search Agent (will use site:decathlon.fr)
   - Ask the Storyteller to craft engaging narratives
   - Present curated recommendations from Decathlon

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
that guides the search agent to construct "site:decathlon.fr" queries. This ensures
results are limited to Decathlon while maintaining natural conversation flow.""",
    tools=[
        AgentTool(agent=search_agent),
        AgentTool(agent=preferences_agent),
        AgentTool(agent=storyteller_agent),
    ]
)

# Export for external use
__all__ = ["root_agent", "search_agent", "preferences_agent", "storyteller_agent"]
