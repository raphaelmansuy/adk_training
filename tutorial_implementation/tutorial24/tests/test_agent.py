"""
Test agent configuration and basic functionality.
"""

import pytest
from observability_agent.agent import root_agent


class TestAgentConfig:
    """Test agent configuration and setup."""

    def test_agent_name(self):
        """Test that agent has correct name."""
        assert root_agent.name == "observability_agent"

    def test_agent_model(self):
        """Test that agent uses correct model."""
        assert root_agent.model == "gemini-2.5-flash"

    def test_agent_description(self):
        """Test that agent has description."""
        assert "observability" in root_agent.description.lower() or "monitoring" in root_agent.description.lower()
        assert "production" in root_agent.description.lower()

    def test_agent_instruction(self):
        """Test that agent has comprehensive instruction."""
        assert "production" in root_agent.instruction.lower() or "assistant" in root_agent.instruction.lower()
        assert "helpful" in root_agent.instruction.lower()

    def test_agent_generate_config(self):
        """Test that agent has generate config."""
        assert root_agent.generate_content_config is not None
        assert root_agent.generate_content_config.temperature == 0.5
        assert root_agent.generate_content_config.max_output_tokens == 1024
