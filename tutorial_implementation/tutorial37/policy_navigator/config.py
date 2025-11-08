"""
Configuration module for Policy Navigator.

Handles environment variables, API configuration, and application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Policy Navigator."""

    # Google API Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CLOUD_PROJECT: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    # File Search Store Names
    HR_STORE_NAME: str = os.getenv("HR_STORE_NAME", "policy-navigator-hr")
    IT_STORE_NAME: str = os.getenv("IT_STORE_NAME", "policy-navigator-it")
    LEGAL_STORE_NAME: str = os.getenv("LEGAL_STORE_NAME", "policy-navigator-legal")
    SAFETY_STORE_NAME: str = os.getenv("SAFETY_STORE_NAME", "policy-navigator-safety")

    # Model Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")

    # Logging Configuration
    LOG_LEVEL: str = os.getenv("POLICY_NAVIGATOR_LOG_LEVEL", "INFO")

    # Debug Mode
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # File Search Configuration
    MAX_TOKENS_PER_CHUNK: int = 500
    MAX_OVERLAP_TOKENS: int = 50
    MAX_STORE_SIZE_GB: int = 20
    RECOMMENDED_STORE_SIZE_GB: int = 10

    # Timeout Configuration
    INDEXING_TIMEOUT_SECONDS: int = 300  # 5 minutes
    QUERY_TIMEOUT_SECONDS: int = 60  # 1 minute

    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration is properly set.

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        if not cls.GOOGLE_API_KEY:
            logger.warning(
                "GOOGLE_API_KEY not set. Set it in .env file or environment variables."
            )
            return False

        logger.info(f"Configuration loaded. Debug mode: {cls.DEBUG}")
        logger.info(f"Using model: {cls.DEFAULT_MODEL}")
        logger.info(f"Log level: {cls.LOG_LEVEL}")
        return True

    @classmethod
    def get_store_names(cls) -> dict[str, str]:
        """
        Get all configured store names.

        Returns:
            dict: Mapping of store type to store name
        """
        return {
            "hr": cls.HR_STORE_NAME,
            "it": cls.IT_STORE_NAME,
            "legal": cls.LEGAL_STORE_NAME,
            "safety": cls.SAFETY_STORE_NAME,
        }


# Initialize logger
logger.remove()  # Remove default handler
logger.add(
    lambda msg: print(msg, end=""),
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=Config.LOG_LEVEL,
)

# Validate configuration on import
Config.validate()
