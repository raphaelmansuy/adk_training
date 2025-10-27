# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple user preference management."""

from typing import Dict, Any
from google.adk.tools import ToolContext


def save_preferences(
    sport: str,
    budget_max: int,
    experience_level: str,
    tool_context: ToolContext
) -> str:
    """Save user preferences for personalized recommendations.
    
    Args:
        sport: Type of sport (e.g., "running", "cycling", "hiking")
        budget_max: Maximum budget in EUR
        experience_level: User's experience level ("beginner", "intermediate", "advanced")
        tool_context: ADK tool context
    
    Returns:
        Confirmation message
    """
    # Save to user state (persists across sessions)
    tool_context.invocation_context.state["user:pref_sport"] = sport
    tool_context.invocation_context.state["user:pref_budget"] = budget_max
    tool_context.invocation_context.state["user:pref_experience"] = experience_level
    
    return f"✓ Preferences saved: {sport}, max €{budget_max}, {experience_level} level"


def get_preferences(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieve saved user preferences.
    
    Args:
        tool_context: ADK tool context
    
    Returns:
        Dictionary of saved preferences
    """
    state = tool_context.invocation_context.state
    
    prefs = {
        "sport": state.get("user:pref_sport"),
        "budget_max": state.get("user:pref_budget"),
        "experience_level": state.get("user:pref_experience")
    }
    
    # Filter out None values
    prefs = {k: v for k, v in prefs.items() if v is not None}
    
    if not prefs:
        return {"message": "No preferences saved yet"}
    
    return prefs
