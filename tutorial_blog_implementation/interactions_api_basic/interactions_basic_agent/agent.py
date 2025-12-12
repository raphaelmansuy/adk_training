"""
Interactions API Basic Agent Implementation

This module demonstrates core functionality of Google's Interactions API:
- Basic text interactions
- Server-side state management
- Streaming responses
- Function calling

Requirements:
- google-genai >= 1.55.0
- GOOGLE_API_KEY environment variable set
"""

import os
from typing import Optional, Generator, Any, Dict, List

# Import google.genai - the Interactions API is available in version 1.55.0+
try:
    from google import genai
    from google.genai import types
except ImportError:
    raise ImportError(
        "google-genai >= 1.55.0 is required for Interactions API. "
        "Install with: pip install 'google-genai>=1.55.0'"
    )

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supported models for Interactions API
SUPPORTED_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite", 
    "gemini-2.5-pro",
    "gemini-3-pro-preview",
]

# Default model
DEFAULT_MODEL = "gemini-2.5-flash"


def get_client(api_key: Optional[str] = None) -> genai.Client:
    """
    Create a Google GenAI client for the Interactions API.
    
    Args:
        api_key: Optional API key. If not provided, uses GOOGLE_API_KEY env var.
        
    Returns:
        Configured genai.Client instance.
        
    Raises:
        ValueError: If no API key is available.
    """
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is required. "
            "Get your key at: https://aistudio.google.com/apikey"
        )
    return genai.Client(api_key=key)


def create_basic_interaction(
    prompt: str,
    model: str = DEFAULT_MODEL,
    client: Optional[genai.Client] = None,
) -> Dict[str, Any]:
    """
    Create a basic interaction with the Gemini model.
    
    This is the simplest form of using the Interactions API - 
    a single request-response interaction.
    
    Args:
        prompt: The text prompt to send to the model.
        model: The model identifier (default: gemini-2.5-flash).
        client: Optional pre-configured client.
        
    Returns:
        Dictionary with interaction details:
        - id: Unique interaction identifier
        - text: The model's response text
        - status: Interaction status
        - usage: Token usage information
        
    Example:
        >>> result = create_basic_interaction("Tell me a joke")
        >>> print(result["text"])
    """
    if client is None:
        client = get_client()
    
    interaction = client.interactions.create(
        model=model,
        input=prompt
    )
    
    return {
        "id": interaction.id,
        "text": interaction.outputs[-1].text if interaction.outputs else "",
        "status": interaction.status,
        "usage": interaction.usage if hasattr(interaction, "usage") else None,
    }


def create_stateful_conversation(
    messages: List[str],
    model: str = DEFAULT_MODEL,
    client: Optional[genai.Client] = None,
) -> List[Dict[str, Any]]:
    """
    Create a multi-turn conversation with server-side state management.
    
    This demonstrates the key advantage of the Interactions API - 
    the server manages conversation history, reducing token costs
    and client complexity.
    
    Args:
        messages: List of user messages to send sequentially.
        model: The model identifier.
        client: Optional pre-configured client.
        
    Returns:
        List of interaction results, each containing:
        - id: Interaction ID
        - text: Model response
        - previous_id: ID of previous interaction (if any)
        
    Example:
        >>> results = create_stateful_conversation([
        ...     "My name is Alex",
        ...     "What is my name?"
        ... ])
        >>> print(results[-1]["text"])  # "Your name is Alex"
    """
    if client is None:
        client = get_client()
    
    results = []
    previous_id = None
    
    for message in messages:
        kwargs = {
            "model": model,
            "input": message,
        }
        
        # Add previous interaction ID for context continuity
        if previous_id:
            kwargs["previous_interaction_id"] = previous_id
        
        interaction = client.interactions.create(**kwargs)
        
        result = {
            "id": interaction.id,
            "text": interaction.outputs[-1].text if interaction.outputs else "",
            "previous_id": previous_id,
        }
        results.append(result)
        
        # Update for next iteration
        previous_id = interaction.id
    
    return results


def create_streaming_interaction(
    prompt: str,
    model: str = DEFAULT_MODEL,
    client: Optional[genai.Client] = None,
) -> Generator[str, None, None]:
    """
    Create a streaming interaction for real-time response output.
    
    Streaming is useful for:
    - Showing progress to users
    - Reducing perceived latency
    - Processing long responses incrementally
    
    Args:
        prompt: The text prompt.
        model: The model identifier.
        client: Optional pre-configured client.
        
    Yields:
        Text chunks as they arrive from the model.
        
    Example:
        >>> for chunk in create_streaming_interaction("Explain AI"):
        ...     print(chunk, end="", flush=True)
    """
    if client is None:
        client = get_client()
    
    stream = client.interactions.create(
        model=model,
        input=prompt,
        stream=True
    )
    
    for chunk in stream:
        if chunk.event_type == "content.delta":
            if hasattr(chunk.delta, "text") and chunk.delta.text:
                yield chunk.delta.text


def create_function_calling_interaction(
    prompt: str,
    tools: List[Dict[str, Any]],
    model: str = DEFAULT_MODEL,
    client: Optional[genai.Client] = None,
    tool_executor: Optional[callable] = None,
) -> Dict[str, Any]:
    """
    Create an interaction with function calling capabilities.
    
    The Interactions API supports sophisticated tool use:
    - Custom function definitions
    - Built-in tools (google_search, code_execution)
    - Remote MCP servers
    
    Args:
        prompt: The user's request.
        tools: List of tool definitions.
        model: The model identifier.
        client: Optional pre-configured client.
        tool_executor: Optional function to execute tool calls.
                      Should accept (name, arguments) and return result.
        
    Returns:
        Dictionary with:
        - id: Interaction ID
        - text: Final response text
        - tool_calls: List of tool calls made
        - tool_results: Results from tool execution (if executor provided)
        
    Example:
        >>> tools = [get_weather_tool()]
        >>> result = create_function_calling_interaction(
        ...     "What's the weather in Paris?",
        ...     tools=tools,
        ...     tool_executor=my_weather_function
        ... )
    """
    if client is None:
        client = get_client()
    
    # Initial interaction with tools
    interaction = client.interactions.create(
        model=model,
        input=prompt,
        tools=tools
    )
    
    result = {
        "id": interaction.id,
        "text": "",
        "tool_calls": [],
        "tool_results": [],
    }
    
    # Process outputs
    for output in interaction.outputs:
        if output.type == "function_call":
            tool_call = {
                "name": output.name,
                "arguments": output.arguments,
                "call_id": output.id,
            }
            result["tool_calls"].append(tool_call)
            
            # Execute tool if executor provided
            if tool_executor:
                tool_result = tool_executor(output.name, output.arguments)
                result["tool_results"].append(tool_result)
                
                # Send result back to model
                follow_up = client.interactions.create(
                    model=model,
                    previous_interaction_id=interaction.id,
                    input=[{
                        "type": "function_result",
                        "name": output.name,
                        "call_id": output.id,
                        "result": str(tool_result)
                    }]
                )
                
                # Update with final response
                if follow_up.outputs:
                    result["text"] = follow_up.outputs[-1].text
                    result["id"] = follow_up.id
                    
        elif output.type == "text":
            result["text"] = output.text
    
    return result


def create_interaction_with_builtin_tools(
    prompt: str,
    tool_type: str = "google_search",
    model: str = DEFAULT_MODEL,
    client: Optional[genai.Client] = None,
) -> Dict[str, Any]:
    """
    Create an interaction using built-in tools.
    
    Available built-in tools:
    - google_search: Search the web for current information
    - code_execution: Execute Python code
    - url_context: Read and summarize web pages
    
    Args:
        prompt: The user's request.
        tool_type: One of "google_search", "code_execution", "url_context".
        model: The model identifier.
        client: Optional pre-configured client.
        
    Returns:
        Dictionary with interaction results.
        
    Example:
        >>> result = create_interaction_with_builtin_tools(
        ...     "Who won the 2024 Super Bowl?",
        ...     tool_type="google_search"
        ... )
    """
    if client is None:
        client = get_client()
    
    valid_tools = ["google_search", "code_execution", "url_context"]
    if tool_type not in valid_tools:
        raise ValueError(f"tool_type must be one of {valid_tools}")
    
    interaction = client.interactions.create(
        model=model,
        input=prompt,
        tools=[{"type": tool_type}]
    )
    
    # Extract text output (filtering tool-specific outputs)
    text_output = next(
        (o for o in interaction.outputs if o.type == "text"),
        None
    )
    
    return {
        "id": interaction.id,
        "text": text_output.text if text_output else "",
        "status": interaction.status,
        "outputs": [
            {"type": o.type, "content": getattr(o, "text", str(o))}
            for o in interaction.outputs
        ],
    }
