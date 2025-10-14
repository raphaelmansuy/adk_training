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
            from google.adk.plugins import BasePlugin
            from google.adk.plugins.save_files_as_artifacts_plugin import SaveFilesAsArtifactsPlugin
            from google.adk.events import Event
            from google.adk.runners import InMemoryRunner
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
            from observability_agent.agent import root_agent
            assert root_agent is not None
            assert root_agent.name == "observability_agent"
        except ImportError as e:
            pytest.fail(f"Agent import failed: {e}")

    def test_plugin_imports(self):
        """Test that plugin classes can be imported."""
        try:
            from observability_agent.agent import (
                MetricsCollectorPlugin,
                AlertingPlugin,
                PerformanceProfilerPlugin,
            )
            # All classes imported successfully
            assert callable(MetricsCollectorPlugin)
            assert callable(AlertingPlugin)
            assert callable(PerformanceProfilerPlugin)
        except ImportError as e:
            pytest.fail(f"Plugin class imports failed: {e}")

    def test_dataclass_imports(self):
        """Test that dataclasses can be imported."""
        try:
            from observability_agent.agent import (
                RequestMetrics,
                AggregateMetrics,
            )
            # All dataclasses imported successfully
            assert RequestMetrics is not None
            assert AggregateMetrics is not None
        except ImportError as e:
            pytest.fail(f"Dataclass imports failed: {e}")
