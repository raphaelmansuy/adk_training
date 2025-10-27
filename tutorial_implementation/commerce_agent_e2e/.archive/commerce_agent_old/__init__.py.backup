"""
Commerce Agent E2E - Production Ready Multi-User Commerce Assistant
Demonstrates session persistence, tool integration, and multi-agent coordination.

Enhanced Version: Adds multimodal support, structured responses, efficient preference
collection, and comprehensive cart management.
"""

from .agent import root_agent
from .search_agent import search_agent
from .preferences_agent import preferences_agent
from .models import (
    UserPreferences,
    Product,
    InteractionRecord,
    EngagementProfile,
)
from .database import init_database

# Import tools - both original and enhanced
from .tools import (
    manage_user_preferences,
    curate_products,
    generate_product_narrative,
    send_video_link,
    analyze_product_image,
    access_cart,
    modify_cart,
    process_checkout,
)

# Enhanced agent and sub-agents
from .agent_enhanced import enhanced_root_agent
from .sub_agents.preference_collector import preference_collector_agent
from .sub_agents.product_advisor import product_advisor_agent
from .sub_agents.visual_assistant import visual_assistant_agent
from .sub_agents.checkout_assistant import checkout_assistant_agent

# Enhanced types
from .types import (
    PreferenceCollectionResult,
    ProductRecommendations,
    VisualAnalysisResult,
    CartModificationResult,
    Cart,
)

# Callbacks
from .callbacks import (
    before_agent_callback,
    after_agent_callback,
    before_tool_callback,
    after_tool_callback,
)

__version__ = "0.2.0"  # Enhanced version
__all__ = [
    # Original exports
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
    # Enhanced exports
    "enhanced_root_agent",
    "preference_collector_agent",
    "product_advisor_agent",
    "visual_assistant_agent",
    "checkout_assistant_agent",
    "PreferenceCollectionResult",
    "ProductRecommendations",
    "VisualAnalysisResult",
    "CartModificationResult",
    "Cart",
    "send_video_link",
    "analyze_product_image",
    "access_cart",
    "modify_cart",
    "process_checkout",
    "before_agent_callback",
    "after_agent_callback",
    "before_tool_callback",
    "after_tool_callback",
]

