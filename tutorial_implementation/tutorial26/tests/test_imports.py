"""
Test suite for Tutorial 26: Import validation.
"""

import pytest


class TestCoreImports:
    """Test that core dependencies can be imported."""

    def test_import_google_adk_agents(self):
        """Test importing google.adk.agents."""
        try:
            from google.adk.agents import Agent
            assert Agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import google.adk.agents: {e}")

    def test_import_google_adk_tools(self):
        """Test importing google.adk.tools."""
        try:
            from google.adk.tools import FunctionTool
            assert FunctionTool is not None
        except ImportError as e:
            pytest.fail(f"Failed to import google.adk.tools: {e}")


class TestModuleImports:
    """Test that tutorial module can be imported."""

    def test_import_enterprise_agent_module(self):
        """Test importing enterprise_agent module."""
        try:
            import enterprise_agent
            assert enterprise_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import enterprise_agent: {e}")

    def test_import_root_agent(self):
        """Test importing root_agent from module."""
        try:
            from enterprise_agent import root_agent
            assert root_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import root_agent: {e}")

    def test_import_agent_module(self):
        """Test importing enterprise_agent.agent module."""
        try:
            from enterprise_agent import agent
            assert agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import enterprise_agent.agent: {e}")


class TestToolFunctionImports:
    """Test that tool functions can be imported."""

    def test_import_check_company_size(self):
        """Test importing check_company_size function."""
        try:
            from enterprise_agent.agent import check_company_size
            assert check_company_size is not None
            assert callable(check_company_size)
        except ImportError as e:
            pytest.fail(f"Failed to import check_company_size: {e}")

    def test_import_score_lead(self):
        """Test importing score_lead function."""
        try:
            from enterprise_agent.agent import score_lead
            assert score_lead is not None
            assert callable(score_lead)
        except ImportError as e:
            pytest.fail(f"Failed to import score_lead: {e}")

    def test_import_get_competitive_intel(self):
        """Test importing get_competitive_intel function."""
        try:
            from enterprise_agent.agent import get_competitive_intel
            assert get_competitive_intel is not None
            assert callable(get_competitive_intel)
        except ImportError as e:
            pytest.fail(f"Failed to import get_competitive_intel: {e}")


class TestModuleAttributes:
    """Test module-level attributes."""

    def test_module_has_all(self):
        """Test that module defines __all__."""
        import enterprise_agent
        assert hasattr(enterprise_agent, '__all__')
        assert 'root_agent' in enterprise_agent.__all__

    def test_root_agent_accessible(self):
        """Test that root_agent is accessible from module."""
        import enterprise_agent
        assert hasattr(enterprise_agent, 'root_agent')
        assert enterprise_agent.root_agent is not None
