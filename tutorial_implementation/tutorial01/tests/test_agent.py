# Tutorial 01: Hello World Agent - Agent Tests
# Validates agent configuration and basic functionality

import pytest
from unittest.mock import patch, MagicMock


class TestAgentConfiguration:
    """Test that the agent is properly configured."""

    def test_root_agent_import(self):
        """Test that root_agent can be imported."""
        from hello_agent.agent import root_agent
        assert root_agent is not None

    def test_agent_is_agent_instance(self):
        """Test that root_agent is an Agent instance."""
        from hello_agent.agent import root_agent
        from google.adk.agents import Agent

        assert isinstance(root_agent, Agent)

    def test_agent_name(self):
        """Test that agent has correct name."""
        from hello_agent.agent import root_agent

        assert hasattr(root_agent, 'name')
        assert root_agent.name == "hello_assistant"

    def test_agent_model(self):
        """Test that agent has correct model."""
        from hello_agent.agent import root_agent

        assert hasattr(root_agent, 'model')
        assert root_agent.model == "gemini-2.0-flash"

    def test_agent_description(self):
        """Test that agent has description."""
        from hello_agent.agent import root_agent

        assert hasattr(root_agent, 'description')
        assert "friendly AI assistant" in root_agent.description

    def test_agent_instruction(self):
        """Test that agent has instruction."""
        from hello_agent.agent import root_agent

        assert hasattr(root_agent, 'instruction')
        assert "warm and helpful assistant" in root_agent.instruction
        assert "Greet users enthusiastically" in root_agent.instruction

    def test_agent_instruction_length(self):
        """Test that instruction is reasonable length."""
        from hello_agent.agent import root_agent

        instruction = root_agent.instruction
        assert len(instruction) > 50  # Should be substantial
        assert len(instruction) < 1000  # Shouldn't be too long


class TestAgentFunctionality:
    """Test basic agent functionality (mocked)."""

    @patch('google.adk.agents.Agent')
    def test_agent_creation_mock(self, mock_agent_class):
        """Test agent creation with mocked Agent class."""
        mock_agent = MagicMock()
        mock_agent_class.return_value = mock_agent

        # Re-import to trigger the creation
        import importlib
        import hello_agent.agent
        importlib.reload(hello_agent.agent)

        # Verify Agent was called with correct parameters
        mock_agent_class.assert_called_once()
        call_args = mock_agent_class.call_args

        assert call_args[1]['name'] == 'hello_assistant'
        assert call_args[1]['model'] == 'gemini-2.0-flash'
        assert 'friendly' in call_args[1]['description']
        assert 'warm and helpful' in call_args[1]['instruction']


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests that require real ADK (optional)."""

    def test_agent_can_be_created_without_error(self):
        """Test that agent can be created without raising exceptions."""
        try:
            from hello_agent.agent import root_agent
            # If we get here without exception, basic creation works
            assert True
        except Exception as e:
            pytest.fail(f"Agent creation failed: {e}")

    @pytest.mark.skipif(
        not hasattr(pytest, 'env') or not pytest.env.get('GOOGLE_API_KEY'),
        reason="Requires GOOGLE_API_KEY environment variable"
    )
    def test_agent_has_valid_configuration_for_api(self):
        """Test that agent configuration is valid for API calls."""
        from hello_agent.agent import root_agent

        # These attributes should exist and be reasonable
        assert hasattr(root_agent, 'model')
        assert hasattr(root_agent, 'instruction')
        assert len(root_agent.instruction) > 20

        # Model should be a known Gemini model
        valid_models = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro']
        assert root_agent.model in valid_models