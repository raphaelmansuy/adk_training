"""
Product Search Agent for Decathlon

Handles Google Search integration with domain-focused searching strategy.
Implements "Option 1: Prompt Engineering Approach" to limit results to Decathlon Hong Kong exclusively.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from .config import SEARCH_AGENT_NAME, MODEL_NAME


search_agent = LlmAgent(
    name=SEARCH_AGENT_NAME,
    model=MODEL_NAME,
    description="Search for sports products on Decathlon Hong Kong",
    instruction="""You are a product search specialist for Decathlon Hong Kong.
Your role is to search for sports equipment and apparel exclusively on Decathlon Hong Kong.


You must return links.

Provide clear, organized, Decathlon Hong Kong-focused results.""",
    tools=[google_search]
)

__all__ = ["search_agent"]
