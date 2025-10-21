"""Tests for imports and module structure."""


class TestImports:
    """Test module imports and exports."""

    def test_import_agent_from_module(self):
        """Test importing root_agent from tool_use_evaluator."""
        from tool_use_evaluator import root_agent
        assert root_agent
        assert root_agent.name == "tool_use_evaluator"

    def test_import_app(self):
        """Test importing app from app module."""
        from app import app
        assert app
        assert app.name == "tool_use_quality_app"

    def test_agent_has_root_agent_export(self):
        """Test that agent module exports root_agent."""
        from tool_use_evaluator.agent import root_agent as agent
        assert agent is not None
        assert hasattr(agent, "name")
        assert hasattr(agent, "tools")


class TestModuleStructure:
    """Test module structure and organization."""

    def test_package_init_exports(self):
        """Test __init__.py exports root_agent."""
        from tool_use_evaluator import root_agent
        assert root_agent.name == "tool_use_evaluator"

    def test_tool_use_evaluator_module_exists(self):
        """Test tool_use_evaluator module is properly structured."""
        import tool_use_evaluator
        assert hasattr(tool_use_evaluator, "root_agent")
