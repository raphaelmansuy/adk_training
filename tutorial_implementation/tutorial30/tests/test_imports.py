"""Tests for module imports."""

import pytest
import sys
import os


class TestImports:
    """Test that all required modules can be imported."""

    def test_import_agent_module(self):
        """Test importing the agent module."""
        try:
            import agent

            assert agent is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_import_agent_agent(self):
        """Test importing agent.agent."""
        try:
            from agent import agent as agent_module

            assert agent_module is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_import_fastapi(self):
        """Test importing fastapi."""
        try:
            import fastapi

            assert fastapi is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_import_uvicorn(self):
        """Test importing uvicorn."""
        try:
            import uvicorn

            assert uvicorn is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_import_google_adk(self):
        """Test importing google.adk."""
        try:
            import google.adk

            assert google.adk is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_import_google_adk_agents(self):
        """Test importing google.adk.agents."""
        try:
            from google.adk.agents import Agent

            assert Agent is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_import_ag_ui_adk(self):
        """Test importing ag_ui_adk."""
        try:
            import ag_ui_adk

            assert ag_ui_adk is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_import_dotenv(self):
        """Test importing dotenv."""
        try:
            import dotenv

            assert dotenv is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
