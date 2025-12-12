"""
Tool definitions for Interactions API examples.

This module provides tool schemas compatible with the Interactions API's
function calling feature.
"""

from typing import Dict, Any, List


def get_weather_tool() -> Dict[str, Any]:
    """
    Get the weather tool definition.
    
    Returns a properly formatted tool schema for the Interactions API.
    
    Returns:
        Tool definition dictionary.
    """
    return {
        "type": "function",
        "name": "get_weather",
        "description": "Gets the current weather for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state/country, e.g. 'San Francisco, CA' or 'Paris, France'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit preference"
                }
            },
            "required": ["location"]
        }
    }


def calculate_tool() -> Dict[str, Any]:
    """
    Get the calculator tool definition.
    
    Returns:
        Tool definition dictionary for mathematical calculations.
    """
    return {
        "type": "function",
        "name": "calculate",
        "description": "Performs mathematical calculations. Use for arithmetic, percentages, and basic math.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate, e.g. '2 + 2' or '15% of 200'"
                }
            },
            "required": ["expression"]
        }
    }


def search_database_tool() -> Dict[str, Any]:
    """
    Get the database search tool definition.
    
    Returns:
        Tool definition for searching a database.
    """
    return {
        "type": "function",
        "name": "search_database",
        "description": "Searches a database for records matching the query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "table": {
                    "type": "string",
                    "description": "The table to search in",
                    "enum": ["users", "products", "orders"]
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                }
            },
            "required": ["query", "table"]
        }
    }


def schedule_meeting_tool() -> Dict[str, Any]:
    """
    Get the meeting scheduler tool definition.
    
    Returns:
        Tool definition for scheduling meetings.
    """
    return {
        "type": "function",
        "name": "schedule_meeting",
        "description": "Schedules a meeting with specified attendees at a given time and date.",
        "parameters": {
            "type": "object",
            "properties": {
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of attendee email addresses"
                },
                "date": {
                    "type": "string",
                    "description": "Date of the meeting (YYYY-MM-DD format)"
                },
                "time": {
                    "type": "string",
                    "description": "Time of the meeting (HH:MM format, 24-hour)"
                },
                "topic": {
                    "type": "string",
                    "description": "The subject/topic of the meeting"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Duration of the meeting in minutes",
                    "default": 60
                }
            },
            "required": ["attendees", "date", "time", "topic"]
        }
    }


# Collection of all available tools
AVAILABLE_TOOLS: List[Dict[str, Any]] = [
    get_weather_tool(),
    calculate_tool(),
    search_database_tool(),
    schedule_meeting_tool(),
]


# Mock implementations for demo purposes
def execute_tool(name: str, arguments: Dict[str, Any]) -> str:
    """
    Execute a tool with the given arguments.
    
    This is a mock implementation for demonstration purposes.
    In production, you would connect to real services.
    
    Args:
        name: The tool name.
        arguments: The tool arguments.
        
    Returns:
        String result from tool execution.
    """
    if name == "get_weather":
        location = arguments.get("location", "Unknown")
        unit = arguments.get("unit", "celsius")
        temp = "22°C" if unit == "celsius" else "72°F"
        return f"The weather in {location} is sunny with a temperature of {temp}."
    
    elif name == "calculate":
        expression = arguments.get("expression", "0")
        # Simple evaluation for demo - in production, use a proper parser
        try:
            # Handle percentages
            if "%" in expression and "of" in expression.lower():
                parts = expression.lower().replace("%", "").split("of")
                percent = float(parts[0].strip())
                value = float(parts[1].strip())
                result = (percent / 100) * value
            else:
                # WARNING: eval is unsafe for production!
                result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {e}"
    
    elif name == "search_database":
        query = arguments.get("query", "")
        table = arguments.get("table", "")
        limit = arguments.get("limit", 10)
        return f"Found 3 results in '{table}' for '{query}' (limit: {limit})"
    
    elif name == "schedule_meeting":
        topic = arguments.get("topic", "Meeting")
        date = arguments.get("date", "TBD")
        time = arguments.get("time", "TBD")
        attendees = arguments.get("attendees", [])
        return f"Meeting '{topic}' scheduled for {date} at {time} with {len(attendees)} attendees."
    
    else:
        return f"Unknown tool: {name}"
