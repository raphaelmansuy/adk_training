
"""Simple user preference management."""

from typing import Dict, Any
from google.adk.tools import ToolContext
# Note: ToolResult TypedDict available for reference but not used in signatures
# to maintain compatibility with ADK automatic function calling
from ..types import ToolResult


def save_preferences(
    sport: str,
    budget_max: int,
    experience_level: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """Save user preferences for personalized recommendations.
    
    Args:
        sport: Type of sport (e.g., "running", "cycling", "hiking")
        budget_max: Maximum budget in EUR
        experience_level: User's experience level ("beginner", "intermediate", "advanced")
        tool_context: ADK tool context
    
    Returns:
        Dictionary with status and report
    """
    try:
        # Save to user state (persists across sessions)
        # ADK v1.17+ uses tool_context.state directly, not invocation_context
        tool_context.state["user:pref_sport"] = sport
        tool_context.state["user:pref_budget"] = budget_max
        tool_context.state["user:pref_experience"] = experience_level
        
        return {
            "status": "success",
            "report": f"✓ Preferences saved: {sport}, max €{budget_max}, {experience_level} level",
            "data": {
                "sport": sport,
                "budget_max": budget_max,
                "experience_level": experience_level
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Failed to save preferences: {str(e)}",
            "error": str(e)
        }


def get_preferences(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieve saved user preferences.
    
    Args:
        tool_context: ADK tool context
    
    Returns:
        Dictionary with status, report, and preference data
    """
    try:
        # ADK v1.17+ uses tool_context.state directly, not invocation_context
        state = tool_context.state
        
        prefs = {
            "sport": state.get("user:pref_sport"),
            "budget_max": state.get("user:pref_budget"),
            "experience_level": state.get("user:pref_experience")
        }
        
        # Filter out None values
        prefs = {k: v for k, v in prefs.items() if v is not None}
        
        if not prefs:
            return {
                "status": "success",
                "report": "No preferences saved yet",
                "data": {}
            }
        
        return {
            "status": "success",
            "report": f"Retrieved preferences: {', '.join(f'{k}={v}' for k, v in prefs.items())}",
            "data": prefs
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Failed to retrieve preferences: {str(e)}",
            "error": str(e),
            "data": {}
        }
