# Tutorial 28: Using Other LLMs with LiteLLM
# Multi-LLM Agent with support for OpenAI, Claude, Ollama, and more

from __future__ import annotations

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool


def calculate_square(number: int) -> int:
    """
    Calculate the square of a number.
    
    Args:
        number: The number to square
        
    Returns:
        The square of the input number
    """
    return number ** 2


def get_weather(city: str) -> dict:
    """
    Get current weather for a city (mock implementation).
    
    Args:
        city: The city name
        
    Returns:
        Dictionary with weather information
    """
    # In production, this would call a real weather API
    return {
        'city': city,
        'temperature': 72,
        'condition': 'Sunny',
        'humidity': 45
    }


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of text (mock implementation).
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary with sentiment analysis results
    """
    # In production, use actual sentiment analysis
    return {
        'sentiment': 'positive',
        'confidence': 0.85,
        'key_phrases': ['exciting', 'innovative', 'breakthrough']
    }


# Default agent: Uses OpenAI GPT-4o-mini via LiteLLM
# This is a cost-effective choice for most tasks
# Note: Users can easily switch to other models by changing the model parameter

root_agent = Agent(
    name="multi_llm_agent",
    model=LiteLlm(model='openai/gpt-4o-mini'),  # OpenAI GPT-4o-mini via LiteLLM
    description=(
        "Multi-LLM agent supporting OpenAI, Claude, Ollama, and more via LiteLLM. "
        "This agent can use different LLM providers for various tasks."
    ),
    instruction="""
You are a versatile AI assistant powered by multiple LLM providers via LiteLLM.
You have access to various tools and can help with:
- Mathematical calculations (calculate_square)
- Weather information (get_weather)
- Sentiment analysis (analyze_sentiment)

Be helpful, accurate, and use the appropriate tools when needed.
Explain your reasoning clearly and provide detailed responses.
    """.strip(),
    tools=[
        FunctionTool(calculate_square),
        FunctionTool(get_weather),
        FunctionTool(analyze_sentiment)
    ]
)


# Alternative agent configurations (can be imported and used separately):

# OpenAI GPT-4o (full version) - for complex reasoning
gpt4o_agent = Agent(
    name="gpt4o_agent",
    model=LiteLlm(model='openai/gpt-4o'),
    description="Agent powered by OpenAI GPT-4o for complex reasoning tasks",
    instruction="You are a powerful reasoning assistant using GPT-4o.",
    tools=[
        FunctionTool(calculate_square),
        FunctionTool(get_weather),
        FunctionTool(analyze_sentiment)
    ]
)


# Anthropic Claude 3.7 Sonnet - for long-form content and analysis
claude_agent = Agent(
    name="claude_agent",
    model=LiteLlm(model='anthropic/claude-3-7-sonnet-20250219'),
    description="Agent powered by Claude 3.7 Sonnet for detailed analysis",
    instruction="""
You are a thoughtful analyst powered by Claude 3.7 Sonnet.
You excel at:
- Complex reasoning
- Long-form content
- Ethical considerations
- Following detailed instructions
    """.strip(),
    tools=[
        FunctionTool(calculate_square),
        FunctionTool(get_weather),
        FunctionTool(analyze_sentiment)
    ]
)


# Ollama Llama 3.3 - for local, privacy-first operation
# Note: Requires Ollama to be installed and running locally
# Use 'ollama_chat' prefix, NOT 'ollama' for proper function calling support
ollama_agent = Agent(
    name="ollama_agent",
    model=LiteLlm(model='ollama_chat/llama3.3'),  # ⚠️ Use ollama_chat, NOT ollama!
    description="Agent running locally with Llama 3.3 via Ollama for privacy",
    instruction="You are a helpful local assistant. All processing happens on-device.",
    tools=[
        FunctionTool(calculate_square),
        FunctionTool(get_weather),
        FunctionTool(analyze_sentiment)
    ]
)
