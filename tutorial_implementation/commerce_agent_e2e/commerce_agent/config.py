"""
Configuration and constants for Commerce Agent.
"""

import os
from typing import Optional

# Database configuration
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./commerce_agent_sessions.db"
)

# ADK Configuration
ADK_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
ADK_PROJECT_ID: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT")

# Agent names and models
ROOT_AGENT_NAME = "CommerceCoordinator"
SEARCH_AGENT_NAME = "ProductSearchAgent"
PREFERENCES_AGENT_NAME = "PreferenceManager"
STORYTELLER_AGENT_NAME = "StorytellerAgent"

MODEL_NAME = "gemini-2.5-flash"

# Search configuration
DECATHLON_SEARCH_DOMAIN = "decathlon.fr"
DEFAULT_SEARCH_LIMIT = 5
CACHE_TTL_SECONDS = 3600  # 1 hour

# Price configuration
DEFAULT_MIN_PRICE = 0.0
DEFAULT_MAX_PRICE = 500.0

# Tool confirmation threshold
EXPENSIVE_PRODUCT_THRESHOLD = 100.0  # EUR

# Session configuration
DEFAULT_SESSION_TIMEOUT = 3600  # 1 hour

# Test configuration
TEST_USER_ID = "test_user"
TEST_SESSION_ID = "test_session"
TEST_APP_NAME = "commerce_agent"
