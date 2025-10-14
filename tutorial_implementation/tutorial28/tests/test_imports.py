# Tutorial 28: Using Other LLMs - Import Tests
# Validates that all required imports work correctly

import pytest


class TestImports:
    """Test that all required imports work."""

    def test_adk_imports(self):
        """Test that ADK core imports work."""
        from google.adk.agents import Agent
        from google.adk.runners import InMemoryRunner
        from google.adk.models.lite_llm import LiteLlm
        from google.adk.tools import FunctionTool
        
        assert Agent is not None
        assert InMemoryRunner is not None
        assert LiteLlm is not None
        assert FunctionTool is not None

    def test_litellm_import(self):
        """Test that LiteLLM imports work."""
        import litellm
        assert litellm is not None

    def test_openai_import(self):
        """Test that OpenAI imports work."""
        import openai
        assert openai is not None

    def test_anthropic_import(self):
        """Test that Anthropic imports work."""
        import anthropic
        assert anthropic is not None

    def test_agent_package_import(self):
        """Test that agent package can be imported."""
        from multi_llm_agent import agent
        assert agent is not None

    def test_root_agent_import(self):
        """Test that root_agent can be imported."""
        from multi_llm_agent.agent import root_agent
        assert root_agent is not None

    def test_alternative_agents_import(self):
        """Test that alternative agents can be imported."""
        from multi_llm_agent.agent import gpt4o_agent, claude_agent, ollama_agent
        assert gpt4o_agent is not None
        assert claude_agent is not None
        assert ollama_agent is not None

    def test_tool_functions_import(self):
        """Test that tool functions can be imported."""
        from multi_llm_agent.agent import calculate_square, get_weather, analyze_sentiment
        assert calculate_square is not None
        assert get_weather is not None
        assert analyze_sentiment is not None
