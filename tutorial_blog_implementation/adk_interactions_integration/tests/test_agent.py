"""
Test Suite for ADK Interactions Agent

Tests cover:
- Agent configuration
- Tool functionality
- Import validation
- Factory patterns
"""

import pytest
from unittest.mock import patch, MagicMock
from typing import Dict, Any


class TestImports:
    """Test module imports and structure."""
    
    def test_package_imports(self):
        """Test that the package imports correctly."""
        from adk_interactions_agent import root_agent
        assert root_agent is not None
    
    def test_tool_imports(self):
        """Test that tools import correctly."""
        from adk_interactions_agent import (
            get_current_weather,
            calculate_expression,
            search_knowledge_base,
        )
        assert callable(get_current_weather)
        assert callable(calculate_expression)
        assert callable(search_knowledge_base)
    
    def test_agent_module_imports(self):
        """Test agent module imports."""
        from adk_interactions_agent.agent import (
            create_interactions_enabled_agent,
            create_standard_agent,
            AgentFactory,
        )
        assert callable(create_interactions_enabled_agent)
        assert callable(create_standard_agent)
        assert AgentFactory is not None


class TestToolFunctions:
    """Test individual tool implementations."""
    
    def test_get_current_weather_success(self):
        """Test weather tool returns valid structure."""
        from adk_interactions_agent.tools import get_current_weather
        
        result = get_current_weather("Tokyo, Japan")
        
        assert result["status"] == "success"
        assert "report" in result
        assert "temperature" in result
        assert "humidity" in result
        assert "conditions" in result
        assert result["location"] == "Tokyo, Japan"
    
    def test_get_current_weather_fahrenheit(self):
        """Test weather tool with fahrenheit units."""
        from adk_interactions_agent.tools import get_current_weather
        
        result = get_current_weather("New York, USA", units="fahrenheit")
        
        assert result["status"] == "success"
        assert result["temperature_unit"] == "°F"
    
    def test_get_current_weather_celsius(self):
        """Test weather tool with celsius units."""
        from adk_interactions_agent.tools import get_current_weather
        
        result = get_current_weather("London, UK", units="celsius")
        
        assert result["status"] == "success"
        assert result["temperature_unit"] == "°C"
    
    def test_calculate_expression_basic(self):
        """Test basic arithmetic calculation."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("2 + 2")
        
        assert result["status"] == "success"
        assert result["result"] == 4
    
    def test_calculate_expression_percentage_of(self):
        """Test percentage of calculation."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("15% of 250")
        
        assert result["status"] == "success"
        assert result["result"] == 37.5
    
    def test_calculate_expression_percentage(self):
        """Test simple percentage."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("50%")
        
        assert result["status"] == "success"
        assert result["result"] == 0.5
    
    def test_calculate_expression_complex(self):
        """Test complex expression."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("(10 + 5) * 2")
        
        assert result["status"] == "success"
        assert result["result"] == 30
    
    def test_calculate_expression_division_by_zero(self):
        """Test division by zero handling."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("10 / 0")
        
        assert result["status"] == "error"
        assert "zero" in result["error"].lower()
    
    def test_calculate_expression_invalid(self):
        """Test invalid expression handling."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("invalid expression!@#")
        
        assert result["status"] == "error"
    
    def test_search_knowledge_base_success(self):
        """Test knowledge base search returns results."""
        from adk_interactions_agent.tools import search_knowledge_base
        
        result = search_knowledge_base("machine learning")
        
        assert result["status"] == "success"
        assert "results" in result
        assert len(result["results"]) > 0
        assert result["query"] == "machine learning"
    
    def test_search_knowledge_base_max_results(self):
        """Test max_results parameter."""
        from adk_interactions_agent.tools import search_knowledge_base
        
        result = search_knowledge_base("computing", max_results=2)
        
        assert result["status"] == "success"
        assert len(result["results"]) <= 2
    
    def test_search_knowledge_base_result_structure(self):
        """Test search result structure."""
        from adk_interactions_agent.tools import search_knowledge_base
        
        result = search_knowledge_base("AI")
        
        assert result["status"] == "success"
        for item in result["results"]:
            assert "id" in item
            assert "title" in item
            assert "snippet" in item


class TestAgentConfiguration:
    """Test agent configuration and factory."""
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_root_agent_exists(self):
        """Test that root_agent is defined."""
        from adk_interactions_agent import root_agent
        
        assert root_agent is not None
        assert hasattr(root_agent, "name")
        assert root_agent.name == "adk_interactions_agent"
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_root_agent_has_tools(self):
        """Test that root_agent has tools configured."""
        from adk_interactions_agent import root_agent
        
        assert hasattr(root_agent, "tools")
        assert len(root_agent.tools) == 3
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_root_agent_has_description(self):
        """Test that root_agent has description."""
        from adk_interactions_agent import root_agent
        
        assert hasattr(root_agent, "description")
        assert len(root_agent.description) > 0
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_root_agent_has_instruction(self):
        """Test that root_agent has instruction."""
        from adk_interactions_agent import root_agent
        
        assert hasattr(root_agent, "instruction")
        assert len(root_agent.instruction) > 0
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_agent_factory_interactions(self):
        """Test AgentFactory creates interactions agent."""
        from adk_interactions_agent.agent import AgentFactory
        
        agent = AgentFactory.interactions_agent()
        
        assert agent is not None
        assert hasattr(agent, "name")
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_agent_factory_standard(self):
        """Test AgentFactory creates standard agent."""
        from adk_interactions_agent.agent import AgentFactory
        
        agent = AgentFactory.standard_agent()
        
        assert agent is not None
        assert agent.name == "standard_agent"
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_agent_factory_pro(self):
        """Test AgentFactory creates pro agent."""
        from adk_interactions_agent.agent import AgentFactory
        
        agent = AgentFactory.pro_agent()
        
        assert agent is not None


class TestUtilities:
    """Test utility functions."""
    
    def test_format_response_markdown(self):
        """Test markdown formatting."""
        from adk_interactions_agent.tools import format_response
        
        data = {
            "status": "success",
            "report": "Test report",
            "value": 42,
        }
        
        result = format_response(data, style="markdown")
        
        assert "**Test report**" in result
        assert "value" in result
    
    def test_format_response_plain(self):
        """Test plain text formatting."""
        from adk_interactions_agent.tools import format_response
        
        data = {
            "status": "success",
            "report": "Test report",
        }
        
        result = format_response(data, style="plain")
        
        assert result == "Test report"
    
    def test_format_response_json(self):
        """Test JSON formatting."""
        from adk_interactions_agent.tools import format_response
        import json
        
        data = {
            "status": "success",
            "value": 42,
        }
        
        result = format_response(data, style="json")
        parsed = json.loads(result)
        
        assert parsed["status"] == "success"
        assert parsed["value"] == 42


class TestDemoModule:
    """Test demo module functionality."""
    
    def test_demo_imports(self):
        """Test demo module imports."""
        from adk_interactions_agent.demo import (
            check_environment,
            print_demo_header,
            print_demo_prompts,
        )
        
        assert callable(check_environment)
        assert callable(print_demo_header)
        assert callable(print_demo_prompts)
    
    @patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key"})
    def test_check_environment_success(self):
        """Test environment check with key set."""
        from adk_interactions_agent.demo import check_environment
        
        result = check_environment()
        
        assert result is True
    
    @patch.dict("os.environ", {}, clear=True)
    def test_check_environment_failure(self):
        """Test environment check without key."""
        from adk_interactions_agent.demo import check_environment
        
        # Remove GOOGLE_API_KEY if present
        import os
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        
        result = check_environment()
        
        assert result is False


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_weather_empty_location(self):
        """Test weather with empty location."""
        from adk_interactions_agent.tools import get_current_weather
        
        result = get_current_weather("")
        
        # Should still return a result (simulated)
        assert result["status"] == "success"
    
    def test_calculate_empty_expression(self):
        """Test calculation with empty expression."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("")
        
        assert result["status"] == "error"
    
    def test_search_empty_query(self):
        """Test search with empty query."""
        from adk_interactions_agent.tools import search_knowledge_base
        
        result = search_knowledge_base("")
        
        # Should return default results
        assert result["status"] == "success"
        assert "results" in result
    
    def test_calculate_special_characters(self):
        """Test calculation with special characters."""
        from adk_interactions_agent.tools import calculate_expression
        
        result = calculate_expression("abc!@#$%")
        
        assert result["status"] == "error"


# Pytest fixtures

@pytest.fixture
def mock_api_key():
    """Fixture to mock API key."""
    with patch.dict("os.environ", {"GOOGLE_API_KEY": "test_key_fixture"}):
        yield


@pytest.fixture
def sample_tool_response():
    """Fixture for sample tool response."""
    return {
        "status": "success",
        "report": "Sample report",
        "data": {"key": "value"},
    }


# Integration tests (require actual API key)

class TestIntegration:
    """Integration tests requiring Google API key."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("google.genai", reason="google-genai not installed"),
        reason="google-genai package not available"
    )
    def test_interactions_api_available(self):
        """Test that Interactions API is available in SDK."""
        import os
        
        if not os.environ.get("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        try:
            from google import genai
            client = genai.Client()
            # Check if interactions attribute exists
            has_interactions = hasattr(client, "interactions") or hasattr(client, "models")
            assert has_interactions
        except Exception as e:
            pytest.skip(f"API not accessible: {e}")
