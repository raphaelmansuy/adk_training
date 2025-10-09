"""
Grounding Agent - Tutorial 11: Built-in Tools & Grounding

This agent demonstrates web grounding capabilities using Google Search
and other built-in ADK tools for accessing current information.
"""

from typing import Dict, Any
from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools import (
    google_search,
    FunctionTool
)
from google.adk.tools.tool_context import ToolContext
from google.genai import types


# ============================================================================
# CUSTOM TOOLS
# ============================================================================

def analyze_search_results(
    query: str,
    search_content: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Analyze search results and extract key insights.

    Args:
        query: The original search query
        search_content: The search results content
        tool_context: ADK tool context

    Returns:
        Dict with analysis results
    """
    try:
        # Simple analysis - count words and extract key phrases
        word_count = len(search_content.split())
        sentences = search_content.split('.')

        # Extract what appears to be key information
        key_insights = []
        for sentence in sentences[:5]:  # First 5 sentences
            sentence = sentence.strip()
            if len(sentence) > 20:  # Meaningful sentences only
                key_insights.append(sentence)

        analysis = {
            'query': query,
            'word_count': word_count,
            'key_insights': key_insights[:3],  # Top 3 insights
            'content_quality': 'good' if word_count > 50 else 'limited',
            'timestamp': datetime.now().isoformat()
        }

        return {
            'status': 'success',
            'report': f'Analyzed {word_count} words from search results for "{query}". Found {len(key_insights)} key insights.',
            'analysis': analysis
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to analyze search results: {str(e)}'
        }


def save_research_findings(
    topic: str,
    findings: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Save research findings as an artifact.

    Args:
        topic: Research topic
        findings: Research findings to save
        tool_context: ADK tool context

    Returns:
        Dict with save results
    """
    try:
        # Save as artifact
        filename = f"research_{topic.replace(' ', '_').lower()}.md"

        # Note: In a real implementation, this would save to artifact service
        # For demo purposes, we'll just return success
        version = "1.0"

        return {
            'status': 'success',
            'report': f'Research findings saved as {filename} (version {version})',
            'filename': filename,
            'version': version
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to save research findings: {str(e)}'
        }


# ============================================================================
# GROUNDING AGENTS
# ============================================================================

# Basic grounding agent with google_search only
basic_grounding_agent = Agent(
    name="basic_grounding_agent",
    model="gemini-2.0-flash",
    description="Basic web grounding agent using Google Search",
    instruction="""You are a web research assistant with access to current information via Google Search.

When asked questions:
1. Use google_search to find current, accurate information
2. Provide clear, factual answers based on search results
3. Always cite that information comes from web search
4. If information seems outdated or uncertain, mention this

Be helpful, accurate, and indicate when you're using search capabilities.""",
    tools=[google_search],
    output_key="grounding_response"
)

# Advanced grounding agent - demonstrates pattern for future tool mixing
advanced_grounding_agent = Agent(
    name="advanced_grounding_agent",
    model="gemini-2.0-flash",
    description="Advanced grounding agent with search and analysis tools",
    instruction="""You are an advanced research assistant with web search and analysis capabilities.

For research tasks:
1. Use google_search to find current information
2. Use analyze_search_results to process and summarize findings
3. Use save_research_findings to preserve important research
4. Provide a comprehensive summary

Always be thorough, cite your sources, and explain your process.""",
    tools=[
        google_search,  # Will work alone
        FunctionTool(analyze_search_results),
        FunctionTool(save_research_findings)
    ],
    output_key="advanced_research_response"
)

# Research assistant - focuses on analysis capabilities
# Demonstrates custom tools that would work with search in future versions
research_assistant = Agent(
    name="research_assistant",
    model="gemini-2.0-flash",
    description="Research assistant with analysis and documentation tools",
    instruction="""You are a research assistant specializing in analyzing and documenting information.

Your capabilities:
- **Analysis**: Use analyze_search_results to process and analyze content
- **Documentation**: Use save_research_findings to preserve research

Research Process:
1. Analyze provided information using analyze_search_results
2. Synthesize findings into clear, actionable insights
3. Document important research using save_research_findings

Guidelines:
- Be objective and factual in your analysis
- Provide timestamps for time-sensitive information
- Save significant findings for future reference

Note: Web search integration will be added once ADK supports mixing built-in and custom tools.""",
    tools=[
        FunctionTool(analyze_search_results),
        FunctionTool(save_research_findings)
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Lower temperature for factual research
        max_output_tokens=2048
    ),
    output_key="research_response"
)

# Default agent (used by ADK web interface)
root_agent = basic_grounding_agent