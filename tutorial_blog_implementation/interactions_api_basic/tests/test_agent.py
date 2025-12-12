"""
Tests for Interactions API Basic Agent

These tests validate:
- Module imports
- Tool definitions
- Agent configuration (without making API calls)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestImports:
    """Test that all module imports work correctly."""
    
    def test_import_main_module(self):
        """Test importing the main module."""
        from interactions_basic_agent import (
            create_basic_interaction,
            create_stateful_conversation,
            create_streaming_interaction,
            create_function_calling_interaction,
        )
        assert callable(create_basic_interaction)
        assert callable(create_stateful_conversation)
        assert callable(create_streaming_interaction)
        assert callable(create_function_calling_interaction)
    
    def test_import_tools(self):
        """Test importing tools module."""
        from interactions_basic_agent import (
            get_weather_tool,
            calculate_tool,
            AVAILABLE_TOOLS,
        )
        assert callable(get_weather_tool)
        assert callable(calculate_tool)
        assert isinstance(AVAILABLE_TOOLS, list)
    
    def test_import_constants(self):
        """Test importing constants."""
        from interactions_basic_agent import SUPPORTED_MODELS
        assert isinstance(SUPPORTED_MODELS, list)
        assert "gemini-2.5-flash" in SUPPORTED_MODELS


class TestToolDefinitions:
    """Test tool schema definitions."""
    
    def test_weather_tool_schema(self):
        """Test weather tool has correct schema."""
        from interactions_basic_agent import get_weather_tool
        
        tool = get_weather_tool()
        assert tool["type"] == "function"
        assert tool["name"] == "get_weather"
        assert "description" in tool
        assert "parameters" in tool
        assert "location" in tool["parameters"]["properties"]
    
    def test_calculate_tool_schema(self):
        """Test calculator tool has correct schema."""
        from interactions_basic_agent import calculate_tool
        
        tool = calculate_tool()
        assert tool["type"] == "function"
        assert tool["name"] == "calculate"
        assert "expression" in tool["parameters"]["properties"]
    
    def test_available_tools_not_empty(self):
        """Test that AVAILABLE_TOOLS contains tools."""
        from interactions_basic_agent import AVAILABLE_TOOLS
        
        assert len(AVAILABLE_TOOLS) > 0
        for tool in AVAILABLE_TOOLS:
            assert "type" in tool
            assert "name" in tool
            assert "parameters" in tool


class TestToolExecution:
    """Test tool execution mock implementations."""
    
    def test_execute_weather_tool(self):
        """Test weather tool execution."""
        from interactions_basic_agent.tools import execute_tool
        
        result = execute_tool("get_weather", {"location": "Paris"})
        assert "Paris" in result
        assert "weather" in result.lower()
    
    def test_execute_calculate_tool(self):
        """Test calculator tool execution."""
        from interactions_basic_agent.tools import execute_tool
        
        result = execute_tool("calculate", {"expression": "2 + 2"})
        assert "4" in result
    
    def test_execute_calculate_percentage(self):
        """Test calculator with percentage."""
        from interactions_basic_agent.tools import execute_tool
        
        result = execute_tool("calculate", {"expression": "10% of 200"})
        assert "20" in result
    
    def test_execute_unknown_tool(self):
        """Test unknown tool returns error message."""
        from interactions_basic_agent.tools import execute_tool
        
        result = execute_tool("unknown_tool", {})
        assert "Unknown tool" in result


class TestAgentConfiguration:
    """Test agent configuration without making API calls."""
    
    def test_supported_models(self):
        """Test supported models list."""
        from interactions_basic_agent.agent import SUPPORTED_MODELS, DEFAULT_MODEL
        
        assert len(SUPPORTED_MODELS) >= 4
        assert DEFAULT_MODEL in SUPPORTED_MODELS
        assert "gemini-2.5-flash" in SUPPORTED_MODELS
        assert "gemini-3-pro-preview" in SUPPORTED_MODELS
    
    def test_get_client_without_key_raises(self):
        """Test that get_client raises without API key."""
        from interactions_basic_agent.agent import get_client
        
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                get_client()
            assert "GOOGLE_API_KEY" in str(exc_info.value)
    
    @patch('interactions_basic_agent.agent.genai.Client')
    def test_get_client_with_key(self, mock_client):
        """Test get_client with API key."""
        from interactions_basic_agent.agent import get_client
        
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'}):
            client = get_client()
            mock_client.assert_called_once_with(api_key='test-key')
    
    @patch('interactions_basic_agent.agent.genai.Client')
    def test_get_client_with_explicit_key(self, mock_client):
        """Test get_client with explicit API key parameter."""
        from interactions_basic_agent.agent import get_client
        
        client = get_client(api_key='explicit-key')
        mock_client.assert_called_once_with(api_key='explicit-key')


class TestInteractionFunctions:
    """Test interaction functions with mocked client."""
    
    @patch('interactions_basic_agent.agent.get_client')
    def test_create_basic_interaction(self, mock_get_client):
        """Test basic interaction creation."""
        from interactions_basic_agent import create_basic_interaction
        
        # Setup mock
        mock_client = MagicMock()
        mock_interaction = MagicMock()
        mock_interaction.id = "test-interaction-id"
        mock_interaction.status = "completed"
        mock_interaction.outputs = [MagicMock(text="Test response")]
        mock_client.interactions.create.return_value = mock_interaction
        mock_get_client.return_value = mock_client
        
        # Test
        result = create_basic_interaction("Test prompt")
        
        assert result["id"] == "test-interaction-id"
        assert result["text"] == "Test response"
        assert result["status"] == "completed"
        mock_client.interactions.create.assert_called_once()
    
    @patch('interactions_basic_agent.agent.get_client')
    def test_create_stateful_conversation(self, mock_get_client):
        """Test stateful conversation creation."""
        from interactions_basic_agent import create_stateful_conversation
        
        # Setup mock
        mock_client = MagicMock()
        
        # Create mock interactions
        mock_int1 = MagicMock()
        mock_int1.id = "id-1"
        mock_int1.outputs = [MagicMock(text="Response 1")]
        
        mock_int2 = MagicMock()
        mock_int2.id = "id-2"
        mock_int2.outputs = [MagicMock(text="Response 2")]
        
        mock_client.interactions.create.side_effect = [mock_int1, mock_int2]
        mock_get_client.return_value = mock_client
        
        # Test
        results = create_stateful_conversation(["Message 1", "Message 2"])
        
        assert len(results) == 2
        assert results[0]["id"] == "id-1"
        assert results[1]["id"] == "id-2"
        assert results[0]["previous_id"] is None
        assert results[1]["previous_id"] == "id-1"
    
    @patch('interactions_basic_agent.agent.get_client')
    def test_create_function_calling_interaction(self, mock_get_client):
        """Test function calling interaction."""
        from interactions_basic_agent import create_function_calling_interaction
        
        # Setup mock - tool call response
        mock_client = MagicMock()
        mock_output = MagicMock()
        mock_output.type = "function_call"
        mock_output.name = "get_weather"
        mock_output.arguments = {"location": "Paris"}
        mock_output.id = "call-id-1"
        
        mock_interaction = MagicMock()
        mock_interaction.id = "int-id"
        mock_interaction.outputs = [mock_output]
        mock_client.interactions.create.return_value = mock_interaction
        mock_get_client.return_value = mock_client
        
        # Test without executor
        tools = [{"type": "function", "name": "get_weather"}]
        result = create_function_calling_interaction("Weather?", tools=tools)
        
        assert len(result["tool_calls"]) == 1
        assert result["tool_calls"][0]["name"] == "get_weather"


class TestBuiltInTools:
    """Test built-in tools configuration."""
    
    @patch('interactions_basic_agent.agent.get_client')
    def test_google_search_tool(self, mock_get_client):
        """Test Google Search built-in tool."""
        from interactions_basic_agent.agent import create_interaction_with_builtin_tools
        
        # Setup mock
        mock_client = MagicMock()
        mock_output = MagicMock()
        mock_output.type = "text"
        mock_output.text = "Search result"
        
        mock_interaction = MagicMock()
        mock_interaction.id = "search-int-id"
        mock_interaction.status = "completed"
        mock_interaction.outputs = [mock_output]
        mock_client.interactions.create.return_value = mock_interaction
        mock_get_client.return_value = mock_client
        
        # Test
        result = create_interaction_with_builtin_tools(
            "Who won the Super Bowl?",
            tool_type="google_search"
        )
        
        assert result["id"] == "search-int-id"
        assert result["text"] == "Search result"
        
        # Verify tool was passed correctly
        call_kwargs = mock_client.interactions.create.call_args[1]
        assert {"type": "google_search"} in call_kwargs["tools"]
    
    def test_invalid_builtin_tool_raises(self):
        """Test that invalid built-in tool raises error."""
        from interactions_basic_agent.agent import create_interaction_with_builtin_tools
        
        with patch('interactions_basic_agent.agent.get_client'):
            with pytest.raises(ValueError) as exc_info:
                create_interaction_with_builtin_tools(
                    "Test",
                    tool_type="invalid_tool"
                )
            assert "tool_type must be one of" in str(exc_info.value)
