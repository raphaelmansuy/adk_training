"""
Utility functions for Policy Navigator.

Helper functions for file handling, logging, and common operations.
"""

import os
from pathlib import Path
from typing import List
from loguru import logger


def get_sample_policies_dir() -> str:
    """
    Get the sample policies directory path.

    Returns:
        str: Absolute path to sample_policies directory
    """
    current_dir = Path(__file__).parent.parent
    return str(current_dir / "sample_policies")


def get_policy_files(
    directory: str = None,
    file_types: List[str] = None,
) -> List[str]:
    """
    Get list of policy files from directory.

    Args:
        directory: Directory to search (uses sample_policies if None)
        file_types: List of file extensions to include (default: ['.md', '.txt', '.pdf'])

    Returns:
        list: List of absolute file paths
    """
    if directory is None:
        directory = get_sample_policies_dir()

    if file_types is None:
        file_types = [".md", ".txt", ".pdf"]

    if not os.path.exists(directory):
        logger.warning(f"Directory not found: {directory}")
        return []

    policy_files = []
    for file in os.listdir(directory):
        if any(file.endswith(ftype) for ftype in file_types):
            full_path = os.path.join(directory, file)
            policy_files.append(full_path)

    logger.info(f"Found {len(policy_files)} policy files in {directory}")
    return sorted(policy_files)


def get_specific_policy(
    policy_name: str,
    directory: str = None,
) -> str:
    """
    Get absolute path to a specific policy file.

    Args:
        policy_name: Name of the policy (e.g., 'hr_handbook.md')
        directory: Directory to search (uses sample_policies if None)

    Returns:
        str: Absolute path to policy file, or empty string if not found
    """
    if directory is None:
        directory = get_sample_policies_dir()

    full_path = os.path.join(directory, policy_name)

    if os.path.exists(full_path):
        return full_path

    logger.warning(f"Policy file not found: {policy_name}")
    return ""


def validate_api_key() -> bool:
    """
    Validate that GOOGLE_API_KEY is set.

    Returns:
        bool: True if API key is set
    """
    from policy_navigator.config import Config

    if not Config.GOOGLE_API_KEY:
        logger.error(
            "GOOGLE_API_KEY not set. Please set it in .env file or as environment variable."
        )
        return False

    return True


def get_store_name_for_policy(policy_file: str) -> str:
    """
    Determine appropriate store type based on policy file.

    Args:
        policy_file: Path or name of policy file

    Returns:
        str: Store type (e.g., 'hr', 'it', 'legal', 'safety')
    """
    policy_lower = policy_file.lower()

    if "hr" in policy_lower or "handbook" in policy_lower:
        return "hr"
    elif "it" in policy_lower or "security" in policy_lower:
        return "it"
    elif "legal" in policy_lower or "compliance" in policy_lower:
        return "legal"
    elif "safety" in policy_lower or "conduct" in policy_lower:
        return "safety"
    elif "remote" in policy_lower:
        return "hr"  # Remote work is HR-related
    else:
        return "hr"  # Default to HR


def format_response(
    status: str,
    message: str,
    details: dict = None,
) -> str:
    """
    Format a response message for display.

    Args:
        status: Status ('success', 'error', 'warning')
        message: Main message
        details: Optional details dictionary

    Returns:
        str: Formatted message
    """
    prefix = {
        "success": "✓",
        "error": "✗",
        "warning": "⚠",
    }.get(status, "→")

    result = f"{prefix} {message}\n"

    if details:
        for key, value in details.items():
            if isinstance(value, list):
                result += f"  {key}:\n"
                for item in value:
                    result += f"    - {item}\n"
            else:
                result += f"  {key}: {value}\n"

    return result
