"""
Commerce Agent E2E - Production Ready Multi-User Commerce Assistant
Demonstrates session persistence, tool integration, and multi-agent coordination.
"""

from .agent import root_agent
from .search_agent import search_agent
from .preferences_agent import preferences_agent
from .tools import manage_user_preferences, curate_products, generate_product_narrative
from .models import (
    UserPreferences,
    Product,
    InteractionRecord,
    EngagementProfile,
)
from .database import init_database

__version__ = "0.1.0"
__all__ = [
    "root_agent",
    "search_agent",
    "preferences_agent",
    "manage_user_preferences",
    "curate_products",
    "generate_product_narrative",
    "UserPreferences",
    "Product",
    "InteractionRecord",
    "EngagementProfile",
    "init_database",
]
