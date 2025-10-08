# Tutorial 01: Hello World Agent - Import Tests
# Validates that all required imports work correctly

import ast
import pytest


class TestImports:
    """Test that all ADK imports work correctly."""

    def test_google_adk_agents_import(self):
        """Test that we can import Agent from google.adk.agents."""
        try:
            from google.adk.agents import Agent
            assert Agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import Agent from google.adk.agents: {e}")

    def test_hello_agent_import(self):
        """Test that we can import the hello_agent module."""
        try:
            import hello_agent
            assert hello_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import hello_agent module: {e}")

    def test_hello_agent_agent_import(self):
        """Test that we can import the agent module from hello_agent."""
        try:
            from hello_agent import agent
            assert agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import agent from hello_agent: {e}")

    def test_root_agent_exists(self):
        """Test that root_agent is defined in the agent module."""
        try:
            from hello_agent.agent import root_agent
            assert root_agent is not None
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Failed to import root_agent: {e}")

    def test_future_annotations_import(self):
        """Test that __future__ annotations import works."""
        # This tests that the __future__ import syntax is valid
        # We can't actually import it here due to Python's import rules,
        # but we can verify it exists in the agent file
        # Read the agent.py file and check for the import
        try:
            with open('hello_agent/agent.py', 'r') as f:
                content = f.read()

            # Parse the AST and look for __future__ import
            tree = ast.parse(content)
            future_imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.module == '__future__':
                        future_imports.extend(alias.name for alias in node.names)

            assert 'annotations' in future_imports, "annotations not imported from __future__"
        except Exception as e:
            pytest.fail(f"Failed to validate __future__ import in agent.py: {e}")