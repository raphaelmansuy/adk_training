"""
Test agent configuration and basic functionality.
"""

import pytest
from artifact_agent.agent import root_agent


class TestAgentConfig:
    """Test agent configuration and setup."""

    def test_agent_name(self):
        """Test that agent has correct name."""
        assert root_agent.name == "artifact_agent"

    def test_agent_model(self):
        """Test that agent uses correct model."""
        assert root_agent.model == "gemini-2.5-flash"

    def test_agent_description(self):
        """Test that agent has description."""
        assert "artifact" in root_agent.description.lower()
        assert "document" in root_agent.description.lower()

    def test_agent_instruction(self):
        """Test that agent has comprehensive instruction."""
        assert "artifacts" in root_agent.instruction.lower()
        assert "document" in root_agent.instruction.lower()
        assert "versioning" in root_agent.instruction.lower()

    def test_agent_tools(self):
        """Test that agent has expected tools."""
        tool_names = [tool.name for tool in root_agent.tools if hasattr(tool, 'name')]
        # Check for built-in load_artifacts_tool
        assert any("load_artifacts" in name for name in tool_names)

    def test_agent_has_multiple_tools(self):
        """Test that agent has multiple tools configured."""
        assert len(root_agent.tools) >= 6  # Should have at least 6 tools