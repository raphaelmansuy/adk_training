"""
Configuration and constants for Commerce Agent.

Authentication Methods:
  1. Gemini API (simple, limited)
     - Set: GOOGLE_API_KEY=your_key
     - Get: https://aistudio.google.com/app/apikey
     
  2. Vertex AI (recommended, production-ready)
     - Set: GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
     - Set: GOOGLE_CLOUD_PROJECT=your_project_id
     - Guide: See log/20250124_173000_vertex_ai_setup_guide.md
     
ADK automatically selects the appropriate backend based on 
which credentials are available.
"""

import os
from typing import Optional

# ============================================================================
# Database Configuration
# ============================================================================
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./commerce_agent_sessions.db"
)

# ============================================================================
# ADK Configuration (Authentication)
# ============================================================================

# Vertex AI (Recommended)
ADK_PROJECT_ID: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT")
ADK_CREDENTIALS_PATH: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Gemini API (Alternative)
ADK_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")

# ============================================================================
# Agent Configuration
# ============================================================================

# Agent names
ROOT_AGENT_NAME = "CommerceCoordinator"
SEARCH_AGENT_NAME = "ProductSearchAgent"
PREFERENCES_AGENT_NAME = "PreferenceManager"
STORYTELLER_AGENT_NAME = "StorytellerAgent"

# Model name (works on both Gemini API and Vertex AI)
# Using Vertex AI? Set GOOGLE_APPLICATION_CREDENTIALS env var
# Using Gemini API? Set GOOGLE_API_KEY env var
MODEL_NAME = "gemini-2.5-flash"

# ============================================================================
# Search Configuration
# ============================================================================

# Domain to search (Decathlon)
DECATHLON_SEARCH_DOMAIN = "decathlon.com.hk"
DEFAULT_SEARCH_LIMIT = 5
CACHE_TTL_SECONDS = 3600  # 1 hour

# Price configuration
DEFAULT_MIN_PRICE = 0.0
DEFAULT_MAX_PRICE = 500.0

# Tool confirmation threshold
EXPENSIVE_PRODUCT_THRESHOLD = 100.0  # EUR

# ============================================================================
# Session Configuration
# ============================================================================

DEFAULT_SESSION_TIMEOUT = 3600  # 1 hour

# ============================================================================
# Test Configuration
# ============================================================================

TEST_USER_ID = "test_user"
TEST_SESSION_ID = "test_session"
TEST_APP_NAME = "commerce_agent"
