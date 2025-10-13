"""
Test that all required imports work correctly.
"""

import pytest


class TestImports:
    """Test that all imports work correctly."""

    def test_google_adk_imports(self):
        """Test that ADK imports work."""
        try:
            from google.adk.agents import Agent
            from google.adk.tools.load_artifacts_tool import load_artifacts_tool
            from google.adk.artifacts import InMemoryArtifactService
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            # All imports successful
            assert True
        except ImportError as e:
            pytest.fail(f"ADK import failed: {e}")

    def test_google_genai_imports(self):
        """Test that Google GenAI imports work."""
        try:
            from google.genai import types
            # Test that Part can be created
            part = types.Part.from_text(text="test")
            assert part is not None
            assert True
        except ImportError as e:
            pytest.fail(f"Google GenAI import failed: {e}")

    def test_agent_imports(self):
        """Test that agent module imports work."""
        try:
            from artifact_agent.agent import root_agent
            assert root_agent is not None
            assert root_agent.name == "artifact_agent"
        except ImportError as e:
            pytest.fail(f"Agent import failed: {e}")

    def test_tool_functions_import(self):
        """Test that tool functions can be imported."""
        try:
            from artifact_agent.agent import (
                extract_text_tool,
                summarize_document_tool,
                translate_document_tool,
                create_final_report_tool,
                list_artifacts_tool,
                load_artifact_tool,
            )
            # All functions imported successfully
            assert callable(extract_text_tool)
            assert callable(summarize_document_tool)
            assert callable(translate_document_tool)
            assert callable(create_final_report_tool)
            assert callable(list_artifacts_tool)
            assert callable(load_artifact_tool)
        except ImportError as e:
            pytest.fail(f"Tool function imports failed: {e}")