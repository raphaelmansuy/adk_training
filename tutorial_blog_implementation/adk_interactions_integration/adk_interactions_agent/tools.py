"""
Tool Definitions for ADK Interactions Agent

This module contains the tool functions used by the ADK agent.
Tools follow the ADK convention of returning structured dictionaries
with status, report, and data fields.
"""

import random
from typing import Dict, Any


def get_current_weather(location: str, units: str = "celsius") -> Dict[str, Any]:
    """
    Get the current weather for a specific location.
    
    This is a simulated weather tool that returns realistic-looking
    weather data. In production, you would integrate with a real
    weather API like OpenWeatherMap or WeatherAPI.
    
    Args:
        location: The location to get weather for (e.g., "Tokyo, Japan").
        units: Temperature units - "celsius" or "fahrenheit".
        
    Returns:
        Dictionary with weather information:
        - status: "success" or "error"
        - report: Human-readable summary
        - temperature: Current temperature
        - humidity: Humidity percentage
        - conditions: Weather conditions
        - wind_speed: Wind speed
        - location: Parsed location name
        
    Example:
        >>> result = get_current_weather("Tokyo, Japan")
        >>> print(result["report"])
        "Weather in Tokyo, Japan: 22°C, Partly Cloudy, Humidity: 65%"
    """
    try:
        # Simulate weather data (replace with real API in production)
        temperature_c = random.randint(5, 35)
        humidity = random.randint(30, 90)
        
        conditions_list = [
            "Sunny",
            "Partly Cloudy",
            "Cloudy",
            "Light Rain",
            "Clear",
            "Overcast",
            "Scattered Clouds",
        ]
        conditions = random.choice(conditions_list)
        wind_speed = random.randint(5, 30)
        
        # Convert temperature if needed
        if units.lower() == "fahrenheit":
            temperature = int(temperature_c * 9 / 5 + 32)
            temp_unit = "°F"
        else:
            temperature = temperature_c
            temp_unit = "°C"
        
        return {
            "status": "success",
            "report": f"Weather in {location}: {temperature}{temp_unit}, {conditions}, Humidity: {humidity}%",
            "temperature": temperature,
            "temperature_unit": temp_unit,
            "humidity": humidity,
            "conditions": conditions,
            "wind_speed": wind_speed,
            "wind_unit": "km/h",
            "location": location,
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "report": f"Failed to get weather for {location}: {str(e)}",
        }


def calculate_expression(expression: str) -> Dict[str, Any]:
    """
    Safely calculate a mathematical expression.
    
    Supports:
    - Basic arithmetic: +, -, *, /, **, //
    - Parentheses for grouping
    - Percentage calculations ("15% of 250")
    - Common math operations
    
    Args:
        expression: Mathematical expression to evaluate.
        
    Returns:
        Dictionary with calculation result:
        - status: "success" or "error"
        - report: Human-readable result
        - result: Numeric result
        - expression: Original expression
        
    Example:
        >>> result = calculate_expression("15% of 250")
        >>> print(result["result"])
        37.5
    """
    try:
        # Handle percentage notation
        expr = expression.lower().strip()
        
        # Parse "X% of Y" format
        if "% of" in expr:
            parts = expr.split("% of")
            if len(parts) == 2:
                percent = float(parts[0].strip())
                value = float(parts[1].strip())
                result = (percent / 100) * value
                return {
                    "status": "success",
                    "report": f"{expression} = {result}",
                    "result": result,
                    "expression": expression,
                }
        
        # Handle simple percentage
        if expr.endswith("%"):
            number = float(expr[:-1].strip())
            result = number / 100
            return {
                "status": "success",
                "report": f"{expression} = {result}",
                "result": result,
                "expression": expression,
            }
        
        # Safe evaluation using allowed characters only
        allowed_chars = set("0123456789+-*/(). ")
        sanitized = "".join(c for c in expression if c in allowed_chars)
        
        if not sanitized:
            return {
                "status": "error",
                "error": "Invalid expression",
                "report": f"Could not parse expression: {expression}",
            }
        
        # Evaluate the expression safely
        result = eval(sanitized, {"__builtins__": {}}, {})
        
        return {
            "status": "success",
            "report": f"{expression} = {result}",
            "result": result,
            "expression": expression,
        }
        
    except ZeroDivisionError:
        return {
            "status": "error",
            "error": "Division by zero",
            "report": "Cannot divide by zero",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "report": f"Failed to calculate: {str(e)}",
        }


def search_knowledge_base(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    Search a knowledge base for information.
    
    This is a simulated knowledge base search. In production, you would
    integrate with a real search backend like Elasticsearch, Pinecone,
    or a custom vector database.
    
    Args:
        query: Search query string.
        max_results: Maximum number of results to return.
        
    Returns:
        Dictionary with search results:
        - status: "success" or "error"
        - report: Human-readable summary
        - results: List of matching documents
        - query: Original query
        - total_results: Number of results found
        
    Example:
        >>> result = search_knowledge_base("quantum computing")
        >>> for doc in result["results"]:
        ...     print(doc["title"])
    """
    try:
        # Simulated knowledge base entries
        knowledge_base = [
            {
                "id": "kb001",
                "title": "Introduction to Quantum Computing",
                "snippet": "Quantum computing harnesses quantum mechanics to process information in fundamentally new ways, using qubits instead of classical bits.",
                "relevance": 0.95,
            },
            {
                "id": "kb002",
                "title": "Machine Learning Fundamentals",
                "snippet": "Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.",
                "relevance": 0.88,
            },
            {
                "id": "kb003",
                "title": "Cloud Computing Architecture",
                "snippet": "Cloud computing delivers computing services over the internet, offering scalable resources on demand.",
                "relevance": 0.82,
            },
            {
                "id": "kb004",
                "title": "Natural Language Processing",
                "snippet": "NLP enables computers to understand, interpret, and generate human language, powering applications from chatbots to translation.",
                "relevance": 0.85,
            },
            {
                "id": "kb005",
                "title": "Deep Learning and Neural Networks",
                "snippet": "Deep learning uses multi-layer neural networks to learn complex patterns in data, enabling breakthroughs in image and speech recognition.",
                "relevance": 0.91,
            },
            {
                "id": "kb006",
                "title": "Agent-Based AI Systems",
                "snippet": "AI agents are autonomous systems that perceive their environment and take actions to achieve specific goals using reasoning and tools.",
                "relevance": 0.87,
            },
        ]
        
        # Simple keyword matching (use vector search in production)
        query_terms = set(query.lower().split())
        scored_results = []
        
        for entry in knowledge_base:
            title_terms = set(entry["title"].lower().split())
            snippet_terms = set(entry["snippet"].lower().split())
            all_terms = title_terms | snippet_terms
            
            # Calculate relevance based on term overlap
            overlap = len(query_terms & all_terms)
            if overlap > 0:
                score = overlap * entry["relevance"]
                scored_results.append((score, entry))
        
        # Sort by score and take top results
        scored_results.sort(key=lambda x: x[0], reverse=True)
        top_results = [entry for _, entry in scored_results[:max_results]]
        
        # If no direct matches, return some results anyway (simulation)
        if not top_results:
            top_results = knowledge_base[:max_results]
        
        return {
            "status": "success",
            "report": f"Found {len(top_results)} results for '{query}'",
            "results": top_results,
            "query": query,
            "total_results": len(top_results),
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "report": f"Search failed: {str(e)}",
        }


# Additional utility tools

def format_response(data: Dict[str, Any], style: str = "markdown") -> str:
    """
    Format tool response data for display.
    
    Args:
        data: Tool response dictionary.
        style: Output format - "markdown", "plain", or "json".
        
    Returns:
        Formatted string representation.
    """
    if style == "json":
        import json
        return json.dumps(data, indent=2)
    
    if style == "markdown":
        lines = []
        if "report" in data:
            lines.append(f"**{data['report']}**\n")
        for key, value in data.items():
            if key not in ("status", "report", "error"):
                if isinstance(value, list):
                    lines.append(f"- **{key}**: {len(value)} items")
                else:
                    lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)
    
    # Plain text
    return data.get("report", str(data))
