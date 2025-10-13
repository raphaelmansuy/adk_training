# Tutorial 20: YAML Configuration - Agent Tests
# Validates YAML configuration loading and agent setup

import pytest
from unittest.mock import patch


class TestYAMLConfiguration:
    """Test that YAML configuration loads correctly."""

    def test_config_file_exists(self):
        """Test that root_agent.yaml exists."""
        import os
        config_path = 'tutorial20/root_agent.yaml'
        assert os.path.exists(config_path), "tutorial20/root_agent.yaml should exist"

    def test_config_agent_loading(self):
        """Test that agent can be loaded from YAML configuration."""
        try:
            from google.adk.agents import config_agent_utils
            agent = config_agent_utils.from_config('tutorial20/root_agent.yaml')
            assert agent is not None
        except Exception as e:
            pytest.fail(f"Failed to load agent from YAML: {e}")

    def test_agent_basic_properties(self):
        """Test that loaded agent has correct basic properties."""
        from google.adk.agents import config_agent_utils

        agent = config_agent_utils.from_config('tutorial20/root_agent.yaml')

        assert hasattr(agent, 'name')
        assert agent.name == "customer_support"

        assert hasattr(agent, 'model')
        assert agent.model == "gemini-2.0-flash"

        assert hasattr(agent, 'description')
        assert "customer support agent" in agent.description.lower()

    def test_agent_instruction(self):
        """Test that agent has proper instruction."""
        from google.adk.agents import config_agent_utils

        agent = config_agent_utils.from_config('tutorial20/root_agent.yaml')

        assert hasattr(agent, 'instruction')
        instruction = agent.instruction
        assert "customer support agent" in instruction.lower()
        assert "available tools" in instruction.lower()

    def test_agent_has_no_sub_agents(self):
        """Test that agent has no sub-agents (single-agent configuration)."""
        from google.adk.agents import config_agent_utils

        agent = config_agent_utils.from_config('tutorial20/root_agent.yaml')

        assert hasattr(agent, 'sub_agents')
        assert len(agent.sub_agents) == 0  # Single-agent configuration

    def test_agent_has_tools(self):
        """Test that agent has tools configured."""
        from google.adk.agents import config_agent_utils

        agent = config_agent_utils.from_config('tutorial20/root_agent.yaml')

        assert hasattr(agent, 'tools')
        assert len(agent.tools) == 11  # All customer support tools

    def test_agent_tools_are_functions(self):
        """Test that agent tools are callable functions."""
        from google.adk.agents import config_agent_utils

        agent = config_agent_utils.from_config('tutorial20/root_agent.yaml')

        assert hasattr(agent, 'tools')
        for tool in agent.tools:
            assert callable(tool)


class TestConfigurationValidation:
    """Test configuration validation and error handling."""

    def test_invalid_config_path(self):
        """Test error handling for non-existent config file."""
        from google.adk.agents import config_agent_utils

        with pytest.raises(Exception):
            config_agent_utils.from_config('non_existent.yaml')

    @patch('google.adk.agents.config_agent_utils.from_config')
    def test_config_loading_error_handling(self, mock_from_config):
        """Test error handling during config loading."""
        mock_from_config.side_effect = Exception("YAML parsing error")

        with pytest.raises(Exception):
            from google.adk.agents import config_agent_utils
            config_agent_utils.from_config('tutorial20/root_agent.yaml')


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests that require real ADK (optional)."""

    def test_agent_creation_without_error(self):
        """Test that agent can be created without raising exceptions."""
        try:
            from google.adk.agents import config_agent_utils
            agent = config_agent_utils.from_config('tutorial20/root_agent.yaml')
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
        from google.adk.agents import config_agent_utils

        agent = config_agent_utils.from_config('root_agent.yaml')

        # These attributes should exist and be reasonable
        assert hasattr(agent, 'model')
        assert hasattr(agent, 'instruction')
        assert len(agent.instruction) > 20

        # Model should be a known Gemini model
        valid_models = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro']
        assert agent.model in valid_models

        # Should have no sub-agents (single-agent config)
        assert hasattr(agent, 'sub_agents')
        assert len(agent.sub_agents) == 0