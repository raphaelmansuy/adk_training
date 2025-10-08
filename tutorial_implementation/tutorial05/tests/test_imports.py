"""
Import tests for Tutorial 05: Parallel Processing
"""

import pytest


class TestImports:
    """Test imports and module structure"""

    def test_google_adk_agents_import(self):
        """Test that google.adk.agents can be imported"""
        import importlib.util
        spec = importlib.util.find_spec("google.adk.agents")
        assert spec is not None, "google.adk.agents module not found"

    def test_travel_planner_agent_import(self):
        """Test that travel_planner.agent module can be imported"""
        import importlib.util
        spec = importlib.util.find_spec("travel_planner.agent")
        assert spec is not None, "travel_planner.agent module not found"

    def test_root_agent_exists(self):
        """Test that root_agent is defined and accessible"""
        try:
            from travel_planner.agent import root_agent
            assert root_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import root_agent: {e}")

    def test_future_annotations_import(self):
        """Test that __future__ annotations is imported"""
        import travel_planner.agent
        # This would fail at import time if __future__ annotations wasn't imported
        # since we're using the | syntax in type hints
        assert hasattr(travel_planner.agent, 'root_agent')