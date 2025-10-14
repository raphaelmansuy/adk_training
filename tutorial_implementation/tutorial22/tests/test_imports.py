# Tutorial 22: Model Selection & Optimization - Import Tests
# Validates that all required imports work correctly

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

    def test_google_adk_runner_import(self):
        """Test that we can import Runner from google.adk.runners."""
        try:
            from google.adk.runners import Runner
            assert Runner is not None
        except ImportError as e:
            pytest.fail(f"Failed to import Runner from google.adk.runners: {e}")

    def test_google_genai_types_import(self):
        """Test that we can import types from google.genai."""
        try:
            from google.genai import types
            assert types is not None
        except ImportError as e:
            pytest.fail(f"Failed to import types from google.genai: {e}")

    def test_tool_context_import(self):
        """Test that we can import ToolContext."""
        try:
            from google.adk.tools.tool_context import ToolContext
            assert ToolContext is not None
        except ImportError as e:
            pytest.fail(f"Failed to import ToolContext: {e}")

    def test_model_selector_import(self):
        """Test that we can import the model_selector module."""
        try:
            import model_selector
            assert model_selector is not None
        except ImportError as e:
            pytest.fail(f"Failed to import model_selector module: {e}")

    def test_model_selector_agent_import(self):
        """Test that we can import the agent module from model_selector."""
        try:
            from model_selector import agent
            assert agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import agent from model_selector: {e}")

    def test_root_agent_exists(self):
        """Test that root_agent is defined in the agent module."""
        try:
            from model_selector.agent import root_agent
            assert root_agent is not None
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Failed to import root_agent: {e}")

    def test_model_selector_class_import(self):
        """Test that ModelSelector class can be imported."""
        try:
            from model_selector.agent import ModelSelector
            assert ModelSelector is not None
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Failed to import ModelSelector: {e}")

    def test_model_benchmark_import(self):
        """Test that ModelBenchmark dataclass can be imported."""
        try:
            from model_selector.agent import ModelBenchmark
            assert ModelBenchmark is not None
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Failed to import ModelBenchmark: {e}")

    def test_tool_functions_import(self):
        """Test that tool functions can be imported."""
        try:
            from model_selector.agent import (
                recommend_model_for_use_case,
                get_model_info
            )
            assert recommend_model_for_use_case is not None
            assert get_model_info is not None
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Failed to import tool functions: {e}")
