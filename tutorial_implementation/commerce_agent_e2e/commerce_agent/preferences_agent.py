"""
Preference Manager Agent for Commerce

Handles user preferences, interaction history, and personalization.
Tracks user interests and sports preferences for targeted recommendations.
"""

from google.adk.agents import LlmAgent

from .config import PREFERENCES_AGENT_NAME, MODEL_NAME


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

__all__ = ["preferences_agent"]
