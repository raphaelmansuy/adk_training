
"""Type definitions for Commerce Agent tools and callbacks.

This module provides TypedDict definitions for better type safety and IDE support.

⚠️ IMPORTANT: ADK Compatibility Note
These TypedDict types cannot be used directly in function signatures for tools
that use ADK's automatic function calling. Use `Dict[str, Any]` in signatures
instead, but ensure the returned dictionary matches these structures.

Example:
    def my_tool(...) -> Dict[str, Any]:  # Use this in signature
        result: ToolResult = {...}       # Can use TypedDict for type hints
        return result                    # Return matches ToolResult structure
"""

from typing import TypedDict, NotRequired, Any


class ToolResult(TypedDict):
    """Standard return type for all tool functions.
    
    ⚠️ Do not use as return type annotation in tool function signatures.
    ADK's automatic function calling cannot parse TypedDict return types.
    Use `Dict[str, Any]` instead but ensure returned dict matches this structure.
    
    Attributes:
        status: Either "success" or "error"
        report: Human-readable message describing the result
        data: Optional dictionary with result data
        error: Optional error message (only present when status="error")
    """
    status: str
    report: str
    data: NotRequired[dict[str, Any]]
    error: NotRequired[str]


class UserPreferences(TypedDict):
    """User preference data structure.
    
    Attributes:
        sport: Type of sport (e.g., "running", "cycling", "hiking")
        budget_max: Maximum budget in EUR
        experience_level: User's experience level ("beginner", "intermediate", "advanced")
    """
    sport: NotRequired[str]
    budget_max: NotRequired[int]
    experience_level: NotRequired[str]


class GroundingSource(TypedDict):
    """Grounding source information from Google Search.
    
    Attributes:
        title: Title of the source page
        uri: Full URL of the source
        domain: Extracted domain name (e.g., "decathlon.com")
    """
    title: str
    uri: str
    domain: NotRequired[str]


class GroundingSupport(TypedDict):
    """Grounding support for a specific text segment.
    
    Attributes:
        text: The text segment being supported
        start_index: Starting character position in the response
        end_index: Ending character position in the response
        source_indices: List of source indices from grounding_chunks
        confidence: Confidence level ("high", "medium", "low")
    """
    text: str
    start_index: int
    end_index: int
    source_indices: list[int]
    confidence: NotRequired[str]


class GroundingMetadata(TypedDict):
    """Complete grounding metadata from Google Search results.
    
    Attributes:
        sources: List of source information
        supports: List of text segments with source attribution
        search_suggestions: Optional list of related search queries
        total_sources: Total number of unique sources
    """
    sources: list[GroundingSource]
    supports: list[GroundingSupport]
    search_suggestions: NotRequired[list[str]]
    total_sources: int


__all__ = [
    "ToolResult",
    "UserPreferences",
    "GroundingSource",
    "GroundingSupport",
    "GroundingMetadata",
]
