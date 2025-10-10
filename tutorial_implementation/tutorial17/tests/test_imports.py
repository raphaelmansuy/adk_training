"""
Test Package Imports

Tests for importing the agent package and its components.
"""


class TestImports:
    """Test that the package can be imported correctly."""

    def test_import_root_agent(self):
        """Test that root_agent can be imported from the package."""
        try:
            from a2a_orchestrator import root_agent

            assert root_agent is not None
        except ImportError as e:
            assert False, f"Failed to import root_agent: {e}"

    def test_import_agent_module(self):
        """Test that the agent module can be imported."""
        try:
            from a2a_orchestrator import agent

            assert agent.root_agent is not None
        except ImportError as e:
            assert False, f"Failed to import agent module: {e}"

    def test_import_tools(self):
        """Test that tools can be imported."""
        try:
            from a2a_orchestrator.agent import (
                check_agent_availability, log_coordination_step)

            assert check_agent_availability is not None
            assert log_coordination_step is not None
        except ImportError as e:
            assert False, f"Failed to import tools: {e}"
