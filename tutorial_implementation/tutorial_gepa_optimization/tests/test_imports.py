"""
Test project structure and imports.
"""


class TestImports:
    """Test that all modules can be imported."""

    def test_import_agent_module(self):
        """Test importing agent module."""
        from gepa_agent import agent  # noqa: F401

    def test_import_root_agent(self):
        """Test importing root_agent."""
        from gepa_agent.agent import root_agent  # noqa: F401

        assert root_agent is not None

    def test_import_create_support_agent(self):
        """Test importing create_support_agent function."""
        from gepa_agent.agent import create_support_agent  # noqa: F401

    def test_import_tools(self):
        """Test importing tool classes."""
        from gepa_agent.agent import (  # noqa: F401
            VerifyCustomerIdentity,
            CheckReturnPolicy,
            ProcessRefund,
        )

    def test_import_constants(self):
        """Test importing constants."""
        from gepa_agent.agent import INITIAL_PROMPT  # noqa: F401

        assert INITIAL_PROMPT is not None


class TestProjectStructure:
    """Test project structure and organization."""

    def test_gepa_agent_package_exists(self):
        """Test gepa_agent package exists."""
        import gepa_agent  # noqa: F401

    def test_gepa_agent_has_init(self):
        """Test gepa_agent has __init__.py."""
        from gepa_agent import __all__, __version__  # noqa: F401

        assert __all__ is not None
        assert __version__ is not None

    def test_agent_py_exists(self):
        """Test agent.py exists in package."""
        from gepa_agent import agent  # noqa: F401

        assert hasattr(agent, "root_agent")
        assert hasattr(agent, "create_support_agent")
