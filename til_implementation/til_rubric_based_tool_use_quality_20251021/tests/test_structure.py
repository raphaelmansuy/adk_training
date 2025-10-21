"""Tests for app configuration."""


class TestAppConfiguration:
    """Test ADK app configuration."""

    def test_app_creation(self):
        """Test app is properly created."""
        from app import app
        assert app
        assert app.name == "tool_use_quality_app"

    def test_app_has_root_agent(self):
        """Test app is configured with root agent."""
        from app import app
        assert app.root_agent
        assert app.root_agent.name == "tool_use_evaluator"

    def test_app_root_agent_has_tools(self):
        """Test app's root agent has tools configured."""
        from app import app
        tools = app.root_agent.tools
        assert len(tools) == 4
        tool_names = [t.__name__ for t in tools]
        assert "analyze_data" in tool_names
