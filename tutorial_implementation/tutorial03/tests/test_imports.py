"""
Tests for import validation
"""

import pytest


class TestImports:
    """Test that all imports work correctly"""

    def test_google_adk_agents_import(self):
        """Test google.adk.agents import works"""
        try:
            from google.adk.agents import Agent
            assert Agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import Agent: {e}")

    def test_google_adk_tools_import(self):
        """Test google.adk.tools import works"""
        try:
            from google.adk.tools.openapi_tool import OpenAPIToolset
            assert OpenAPIToolset is not None
        except ImportError as e:
            pytest.fail(f"Failed to import OpenAPIToolset: {e}")

    def test_chuck_norris_agent_import(self):
        """Test chuck_norris_agent module imports"""
        try:
            import chuck_norris_agent
            assert chuck_norris_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import chuck_norris_agent: {e}")

    def test_chuck_norris_agent_agent_import(self):
        """Test chuck_norris_agent.agent module imports"""
        try:
            from chuck_norris_agent import agent
            assert agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import chuck_norris_agent.agent: {e}")

    def test_root_agent_exists(self):
        """Test root_agent can be imported from package"""
        try:
            from chuck_norris_agent import root_agent
            assert root_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import root_agent: {e}")

    def test_future_annotations_import(self):
        """Test __future__ annotations import works"""
        # Test that the __future__ module exists and annotations can be imported
        try:
            import __future__
            assert hasattr(__future__, 'annotations')
            # This validates the import capability without syntax issues
            assert True
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Failed to validate __future__ annotations: {e}")