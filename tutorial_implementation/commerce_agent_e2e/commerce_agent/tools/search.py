# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Search wrapper for sports product search."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

# Search agent with Google Search grounding
_search_agent = Agent(
    model="gemini-2.5-flash",
    name="sports_product_search",
    description="Search for sports products using Google Search with grounding",
    instruction="""Search for sports products and provide detailed information with purchase links.

When searching:
1. Use comprehensive queries like "best trail running shoes under 100 euros 2025"
2. Extract key product information: name, brand, price, features
3. **CRITICAL**: Display URLs from search results with clear retailer attribution
4. Present 3-5 products with clickable links

Response format:
- Product name and brand
- Price in EUR
- Key features (2-3 bullet points)
- **Purchase Link**: Show with visible retailer domain
- Brief explanation of why it fits user needs

IMPORTANT: Google Search provides grounding_chunks with web.uri and web.domain fields.
Extract these and format URLs to show the retailer domain visibly:
- Format: 🔗 **Buy at [domain]**: [full_url]
- Example: 🔗 **Buy at alltricks.com**: https://www.alltricks.com/...

Example response format:
"Brooks Divide 5 - €95
- Comfortable cushioning for beginners
- Good for mixed terrain  
- 🔗 **Buy at decathlon.com.hk**: https://decathlon.com.hk/brooks-divide-5"
""",
    tools=[google_search],
)

# Export as AgentTool for use in main agent
search_products = AgentTool(agent=_search_agent)
