"""
ADK Agent with Interactions API Integration

This module demonstrates integrating Google's Interactions API with the
Agent Development Kit (ADK) for enhanced agentic workflows.

Key Features:
- Server-side state management via Interactions API
- Background execution for long-running tasks
- Native thought handling
- Seamless tool orchestration

Requirements:
- google-adk >= 1.18.0
- google-genai >= 1.55.0
- GOOGLE_API_KEY environment variable
"""

import os
from typing import Dict, Any

from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from dotenv import load_dotenv

from .tools import (
    get_current_weather,
    calculate_expression,
    search_knowledge_base,
)

load_dotenv()

# Agent instruction template
AGENT_INSTRUCTION = """You are a helpful AI assistant powered by the Gemini Interactions API.

You have access to the following tools:

1. **get_current_weather**: Get weather information for any location
   - Use when users ask about weather conditions
   - Provide location in "City, Country" format

2. **calculate_expression**: Perform mathematical calculations
   - Use for arithmetic, percentages, and equations
   - Handles complex expressions

3. **search_knowledge_base**: Search for information
   - Use for factual queries
   - Returns relevant documents and snippets

## Guidelines

- Always use the appropriate tool for the task
- Provide clear, helpful responses
- If a tool fails, explain the issue and offer alternatives
- For complex research questions, acknowledge limitations

## Example Interactions

User: "What's the weather in Tokyo?"
→ Use get_current_weather with location="Tokyo, Japan"

User: "Calculate 15% of 250"
→ Use calculate_expression with expression="15% of 250"

User: "Tell me about quantum computing"
→ Use search_knowledge_base with query="quantum computing fundamentals"
"""


def create_interactions_enabled_agent(
    model: str = "gemini-2.5-flash",
    use_interactions_api: bool = True,
) -> Agent:
    """
    Create an ADK agent with Interactions API backend.
    
    Args:
        model: The Gemini model to use.
        use_interactions_api: Whether to enable Interactions API.
        
    Returns:
        Configured Agent instance.
        
    Example:
        >>> agent = create_interactions_enabled_agent()
        >>> # Use with adk web or programmatically
    """
    return Agent(
        model=Gemini(
            model=model,
            # Enable Interactions API for this agent
            # This provides:
            # - Server-side state management
            # - Background execution support
            # - Native thought handling
            use_interactions_api=use_interactions_api,
        ),
        name="adk_interactions_agent",
        description="An ADK agent demonstrating Interactions API integration with tools for weather, calculations, and search.",
        instruction=AGENT_INSTRUCTION,
        tools=[
            get_current_weather,
            calculate_expression,
            search_knowledge_base,
        ],
    )


def create_standard_agent(model: str = "gemini-2.5-flash") -> Agent:
    """
    Create a standard ADK agent without Interactions API.
    
    This is useful for comparison or when you don't need
    Interactions API features.
    
    Args:
        model: The Gemini model to use.
        
    Returns:
        Configured Agent instance.
    """
    return Agent(
        model=model,
        name="standard_agent",
        description="A standard ADK agent for comparison.",
        instruction=AGENT_INSTRUCTION,
        tools=[
            get_current_weather,
            calculate_expression,
            search_knowledge_base,
        ],
    )


# Export the root_agent for ADK discovery
# This is required for `adk web` to find the agent
root_agent = create_interactions_enabled_agent()


# Alternative agents for different configurations
class AgentFactory:
    """Factory for creating different agent configurations."""
    
    @staticmethod
    def interactions_agent() -> Agent:
        """Create agent with Interactions API enabled."""
        return create_interactions_enabled_agent(use_interactions_api=True)
    
    @staticmethod
    def standard_agent() -> Agent:
        """Create standard agent without Interactions API."""
        return create_standard_agent()
    
    @staticmethod
    def pro_agent() -> Agent:
        """Create agent with Gemini Pro model."""
        return create_interactions_enabled_agent(
            model="gemini-2.5-pro",
            use_interactions_api=True
        )
