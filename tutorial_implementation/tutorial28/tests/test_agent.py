# Tutorial 28: Using Other LLMs - Agent Tests
# Validates agent configuration and tool functionality

import pytest
from unittest.mock import patch, MagicMock


class TestAgentConfiguration:
    """Test that agents are properly configured."""

    def test_root_agent_import(self):
        """Test that root_agent can be imported."""
        from multi_llm_agent.agent import root_agent
        assert root_agent is not None

    def test_root_agent_is_agent_instance(self):
        """Test that root_agent is an Agent instance."""
        from multi_llm_agent.agent import root_agent
        from google.adk.agents import Agent
        assert isinstance(root_agent, Agent)

    def test_root_agent_name(self):
        """Test that root_agent has correct name."""
        from multi_llm_agent.agent import root_agent
        assert hasattr(root_agent, 'name')
        assert root_agent.name == "multi_llm_agent"

    def test_root_agent_model(self):
        """Test that root_agent has correct model."""
        from multi_llm_agent.agent import root_agent
        from google.adk.models.lite_llm import LiteLlm
        assert hasattr(root_agent, 'model')
        assert isinstance(root_agent.model, LiteLlm)

    def test_root_agent_description(self):
        """Test that root_agent has description."""
        from multi_llm_agent.agent import root_agent
        assert hasattr(root_agent, 'description')
        assert "Multi-LLM agent" in root_agent.description
        assert "LiteLLM" in root_agent.description

    def test_root_agent_instruction(self):
        """Test that root_agent has instruction."""
        from multi_llm_agent.agent import root_agent
        assert hasattr(root_agent, 'instruction')
        assert len(root_agent.instruction) > 100
        assert "versatile AI assistant" in root_agent.instruction

    def test_root_agent_has_tools(self):
        """Test that root_agent has tools."""
        from multi_llm_agent.agent import root_agent
        assert hasattr(root_agent, 'tools')
        assert len(root_agent.tools) == 3  # calculate_square, get_weather, analyze_sentiment


class TestAlternativeAgents:
    """Test alternative agent configurations."""

    def test_gpt4o_agent_exists(self):
        """Test that gpt4o_agent can be imported."""
        from multi_llm_agent.agent import gpt4o_agent
        assert gpt4o_agent is not None

    def test_gpt4o_agent_has_correct_model(self):
        """Test that gpt4o_agent uses correct model."""
        from multi_llm_agent.agent import gpt4o_agent
        from google.adk.models.lite_llm import LiteLlm
        assert isinstance(gpt4o_agent.model, LiteLlm)
        # Note: Can't easily check the internal model string without accessing private attributes

    def test_claude_agent_exists(self):
        """Test that claude_agent can be imported."""
        from multi_llm_agent.agent import claude_agent
        assert claude_agent is not None

    def test_claude_agent_name(self):
        """Test that claude_agent has correct name."""
        from multi_llm_agent.agent import claude_agent
        assert claude_agent.name == "claude_agent"

    def test_ollama_agent_exists(self):
        """Test that ollama_agent can be imported."""
        from multi_llm_agent.agent import ollama_agent
        assert ollama_agent is not None

    def test_ollama_agent_description_mentions_privacy(self):
        """Test that ollama_agent description mentions privacy."""
        from multi_llm_agent.agent import ollama_agent
        assert "privacy" in ollama_agent.description.lower()
        assert "local" in ollama_agent.description.lower()

    def test_all_agents_have_same_tools(self):
        """Test that all agents have the same tool set."""
        from multi_llm_agent.agent import root_agent, gpt4o_agent, claude_agent, ollama_agent
        
        tool_count = len(root_agent.tools)
        assert len(gpt4o_agent.tools) == tool_count
        assert len(claude_agent.tools) == tool_count
        assert len(ollama_agent.tools) == tool_count


class TestToolFunctions:
    """Test tool functions work correctly."""

    def test_calculate_square_basic(self):
        """Test calculate_square with basic input."""
        from multi_llm_agent.agent import calculate_square
        assert calculate_square(5) == 25
        assert calculate_square(10) == 100
        assert calculate_square(0) == 0

    def test_calculate_square_negative(self):
        """Test calculate_square with negative input."""
        from multi_llm_agent.agent import calculate_square
        assert calculate_square(-5) == 25

    def test_get_weather_returns_dict(self):
        """Test that get_weather returns a dictionary."""
        from multi_llm_agent.agent import get_weather
        result = get_weather("San Francisco")
        assert isinstance(result, dict)

    def test_get_weather_has_required_fields(self):
        """Test that get_weather returns required fields."""
        from multi_llm_agent.agent import get_weather
        result = get_weather("New York")
        assert 'city' in result
        assert 'temperature' in result
        assert 'condition' in result
        assert 'humidity' in result

    def test_get_weather_city_name(self):
        """Test that get_weather preserves city name."""
        from multi_llm_agent.agent import get_weather
        result = get_weather("London")
        assert result['city'] == "London"

    def test_analyze_sentiment_returns_dict(self):
        """Test that analyze_sentiment returns a dictionary."""
        from multi_llm_agent.agent import analyze_sentiment
        result = analyze_sentiment("This is great!")
        assert isinstance(result, dict)

    def test_analyze_sentiment_has_required_fields(self):
        """Test that analyze_sentiment returns required fields."""
        from multi_llm_agent.agent import analyze_sentiment
        result = analyze_sentiment("Amazing product!")
        assert 'sentiment' in result
        assert 'confidence' in result
        assert 'key_phrases' in result

    def test_analyze_sentiment_confidence_is_float(self):
        """Test that confidence is a float."""
        from multi_llm_agent.agent import analyze_sentiment
        result = analyze_sentiment("Wonderful experience")
        assert isinstance(result['confidence'], float)
        assert 0 <= result['confidence'] <= 1

    def test_analyze_sentiment_key_phrases_is_list(self):
        """Test that key_phrases is a list."""
        from multi_llm_agent.agent import analyze_sentiment
        result = analyze_sentiment("Excellent service")
        assert isinstance(result['key_phrases'], list)
        assert len(result['key_phrases']) > 0


class TestModelTypes:
    """Test model type validation."""

    def test_root_agent_uses_litellm(self):
        """Test that root_agent uses LiteLlm model."""
        from multi_llm_agent.agent import root_agent
        from google.adk.models.lite_llm import LiteLlm
        assert isinstance(root_agent.model, LiteLlm)

    def test_all_alternative_agents_use_litellm(self):
        """Test that all alternative agents use LiteLlm models."""
        from multi_llm_agent.agent import gpt4o_agent, claude_agent, ollama_agent
        from google.adk.models.lite_llm import LiteLlm
        
        assert isinstance(gpt4o_agent.model, LiteLlm)
        assert isinstance(claude_agent.model, LiteLlm)
        assert isinstance(ollama_agent.model, LiteLlm)


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests that require real ADK components (optional)."""

    def test_agent_can_be_created_without_error(self):
        """Test that agent can be created without raising exceptions."""
        try:
            from multi_llm_agent.agent import root_agent
            assert root_agent is not None
        except Exception as e:
            pytest.fail(f"Agent creation failed: {e}")

    def test_all_agents_can_be_created(self):
        """Test that all agent variants can be created."""
        try:
            from multi_llm_agent.agent import (
                root_agent,
                gpt4o_agent,
                claude_agent,
                ollama_agent
            )
            assert root_agent is not None
            assert gpt4o_agent is not None
            assert claude_agent is not None
            assert ollama_agent is not None
        except Exception as e:
            pytest.fail(f"Agent creation failed: {e}")

    def test_tools_are_function_tools(self):
        """Test that tools are properly wrapped as FunctionTools."""
        from multi_llm_agent.agent import root_agent
        from google.adk.tools import FunctionTool
        
        for tool in root_agent.tools:
            assert isinstance(tool, FunctionTool)

    def test_tool_functions_are_callable(self):
        """Test that all tool functions are callable."""
        from multi_llm_agent.agent import calculate_square, get_weather, analyze_sentiment
        
        assert callable(calculate_square)
        assert callable(get_weather)
        assert callable(analyze_sentiment)
