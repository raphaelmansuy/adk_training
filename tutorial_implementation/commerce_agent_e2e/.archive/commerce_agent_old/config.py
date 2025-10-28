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

# Enhanced agent names
ENHANCED_ROOT_AGENT_NAME = "EnhancedCommerceCoordinator"
PREFERENCE_COLLECTOR_NAME = "PreferenceCollector"
PRODUCT_ADVISOR_NAME = "ProductAdvisor"
VISUAL_ASSISTANT_NAME = "VisualAssistant"
CHECKOUT_ASSISTANT_NAME = "CheckoutAssistant"

# Model name (works on both Gemini API and Vertex AI)
# Using Vertex AI? Set GOOGLE_APPLICATION_CREDENTIALS env var
# Using Gemini API? Set GOOGLE_API_KEY env var
MODEL_NAME = "gemini-2.5-flash"

# Enhanced agent model parameters
ENHANCED_MODEL_TEMPERATURE = 0.7  # Balanced creativity/consistency
ENHANCED_MODEL_TOP_P = 0.9  # High diversity for recommendations
ENHANCED_MODEL_TOP_K = 40  # Moderate token sampling

# ============================================================================
# Enhanced Agent Features
# ============================================================================

# Feature flags for enhanced agent
ENABLE_MULTIMODAL = True  # Enable image/video analysis
ENABLE_STRUCTURED_RESPONSES = True  # Force Pydantic JSON schemas
ENABLE_BATCHED_QUESTIONS = True  # Collect preferences efficiently
ENABLE_CART_MANAGEMENT = True  # Full cart CRUD operations
ENABLE_VISUAL_CALLBACKS = True  # Logging/metrics callbacks

# Multimodal configuration
MAX_IMAGE_SIZE_MB = 10  # Maximum image size for analysis
SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "webp"]
VIDEO_LINK_TIMEOUT_SECONDS = 30  # Timeout for video link sharing

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
