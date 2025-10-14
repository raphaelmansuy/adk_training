"""Test that all required imports work correctly."""

import pytest


def test_adk_imports():
    """Test Google ADK imports."""
    try:
        from google.adk.agents import Agent
        from google.adk.runners import InMemoryRunner
        assert Agent is not None
        assert InMemoryRunner is not None
    except ImportError as e:
        pytest.fail(f"Failed to import ADK modules: {e}")


def test_fastapi_imports():
    """Test FastAPI imports."""
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn
        assert FastAPI is not None
        assert CORSMiddleware is not None
        assert uvicorn is not None
    except ImportError as e:
        pytest.fail(f"Failed to import FastAPI modules: {e}")


def test_ag_ui_imports():
    """Test AG-UI ADK imports."""
    try:
        from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
        assert ADKAgent is not None
        assert add_adk_fastapi_endpoint is not None
    except ImportError as e:
        pytest.fail(f"Failed to import ag_ui_adk: {e}")


def test_agent_module_imports():
    """Test that agent module can be imported."""
    try:
        from agent import agent, root_agent, app
        assert agent is not None
        assert root_agent is not None
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Failed to import agent module: {e}")
