
"""Commerce Agent - A specialized e-commerce assistant using Google ADK.

This agent handles:
- Product searches and recommendations
- Price comparisons
- Technical specifications
- Delivery information
- User preferences management

The agent uses Google Search for grounding (source attribution) and maintains
user preferences across sessions.
"""

from .agent import root_agent
from .callbacks import create_grounding_callback
from .types import ToolResult, UserPreferences, GroundingMetadata, GroundingSource

__all__ = [
    "root_agent",
    "create_grounding_callback",
    "ToolResult",
    "UserPreferences",
    "GroundingMetadata",
    "GroundingSource",
]
