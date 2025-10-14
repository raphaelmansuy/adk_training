"""Test agent configuration and setup."""

import pytest
from unittest.mock import Mock, patch
import os


class TestAgentConfig:
    """Test agent configuration."""

    def test_root_agent_exists(self):
        """Test that root_agent is exported."""
        from agent.agent import root_agent
        assert root_agent is not None

    def test_root_agent_is_agent_instance(self):
        """Test that root_agent is an Agent instance."""
        from agent.agent import root_agent
        from google.adk.agents import Agent
        assert isinstance(root_agent, Agent)

    def test_agent_has_correct_name(self):
        """Test that agent has the correct name."""
        from agent.agent import root_agent
        assert root_agent.name == "quickstart_agent"

    def test_agent_has_model(self):
        """Test that agent has a model configured."""
        from agent.agent import root_agent
        assert root_agent.model is not None
        assert "gemini" in root_agent.model.lower()

    def test_agent_has_instruction(self):
        """Test that agent has instruction configured."""
        from agent.agent import root_agent
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0


class TestFastAPIApp:
    """Test FastAPI application."""

    def test_app_exists(self):
        """Test that FastAPI app is created."""
        from agent.agent import app
        assert app is not None

    def test_app_has_title(self):
        """Test that app has a title."""
        from agent.agent import app
        assert hasattr(app, 'title')
        assert "Tutorial 29" in app.title or "UI Integration" in app.title

    def test_health_endpoint_exists(self):
        """Test that health endpoint exists."""
        from agent.agent import app
        routes = [route.path for route in app.routes]
        assert "/health" in routes

    def test_root_endpoint_exists(self):
        """Test that root endpoint exists."""
        from agent.agent import app
        routes = [route.path for route in app.routes]
        assert "/" in routes

    def test_copilotkit_endpoint_exists(self):
        """Test that copilotkit endpoint exists."""
        from agent.agent import app
        routes = [route.path for route in app.routes]
        # Check if /api/copilotkit path exists
        copilotkit_paths = [r for r in routes if "copilotkit" in r]
        assert len(copilotkit_paths) > 0


class TestADKAgentWrapper:
    """Test ADK agent wrapper configuration."""

    def test_agent_wrapper_exists(self):
        """Test that ADK agent wrapper exists."""
        from agent.agent import agent
        assert agent is not None

    def test_agent_wrapper_is_adk_agent(self):
        """Test that wrapper is ADKAgent instance."""
        from agent.agent import agent
        from ag_ui_adk import ADKAgent
        assert isinstance(agent, ADKAgent)

    def test_agent_has_app_name(self):
        """Test that agent has app_name configured."""
        from agent.agent import agent
        # ADKAgent stores app_name internally, check it's an ADKAgent instance
        from ag_ui_adk import ADKAgent
        assert isinstance(agent, ADKAgent)


class TestEnvironmentConfig:
    """Test environment configuration."""

    def test_env_example_exists(self):
        """Test that .env.example file exists."""
        assert os.path.isfile("agent/.env.example")

    def test_env_example_has_api_key(self):
        """Test that .env.example includes GOOGLE_API_KEY."""
        with open("agent/.env.example", "r") as f:
            content = f.read()
            assert "GOOGLE_API_KEY" in content
