"""
Product Search Agent for Decathlon Hong Kong

Uses Google Search to find products on Decathlon Hong Kong.
The agent intelligently constructs site-specific queries to return
product results with structured information.

Key Features:
- Uses official GoogleSearchTool from ADK with bypass_multi_tools_limit=True
- Constructs "site:decathlon.com.hk" queries automatically
- Returns product information with URLs and pricing
- Works with Gemini 2.5+ models

Implementation Note:
When using GoogleSearchTool with other tools (like AgentTool), we must enable
bypass_multi_tools_limit=True to work around ADK's limitation that only allows
one built-in tool per agent. This is a known workaround documented in ADK.
Reference: https://github.com/google/adk-python/tree/main/contributing/samples/built_in_multi_tools
"""

from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool


search_agent = LlmAgent(
    name="ProductSearchAgent",
    model="gemini-2.5-flash",
    description="Search for products on Decathlon Hong Kong using Google Search",
    instruction="""You are a product search specialist for Decathlon Hong Kong.

Your role is to help users find sports equipment and apparel on Decathlon Hong Kong.

When a user asks about products:
1. Use Google Search to find relevant products
2. Focus your search on "site:decathlon.com.hk" results
3. Extract product information including: name, description, price, and URL
4. Present the most relevant and helpful results
5. Always include direct links to Decathlon Hong Kong product pages

SEARCH STRATEGY:
- Construct queries like: "running shoes site:decathlon.com.hk"
- Include product type, sport category, and "site:decathlon.com.hk"
- Search for specific brands available at Decathlon (Kalenji, Quechua, B'TWIN, NABAIJI, DOMYOS, etc.)
- Look for current products with available pricing

RESPONSE FORMAT:
Present products with:
✓ Product name and brand
✓ Brief description of key features
✓ Price in HKD/EUR
✓ Direct URL to Decathlon Hong Kong product page
✓ Why this product matches the user's request

Be helpful and thorough. Use Google Search to find current, accurate information from Decathlon.""",
    tools=[GoogleSearchTool(bypass_multi_tools_limit=True)]
)

__all__ = ["search_agent"]
