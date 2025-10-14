"""Test that all imports work correctly."""

import pytest


def test_import_agent_module():
    """Test importing the agent module."""
    from production_agent import agent
    assert hasattr(agent, 'root_agent')


def test_import_root_agent():
    """Test importing root_agent directly."""
    from production_agent import root_agent
    assert root_agent is not None


def test_import_server_module():
    """Test importing the server module."""
    from production_agent import server
    assert hasattr(server, 'app')


def test_google_adk_imports():
    """Test that required Google ADK imports work."""
    try:
        from google.adk.agents import Agent, Runner
        from google.genai import types
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import Google ADK modules: {e}")


def test_fastapi_imports():
    """Test that FastAPI imports work."""
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import FastAPI modules: {e}")


def test_tool_functions_exist():
    """Test that tool functions are defined."""
    from production_agent.agent import (
        check_deployment_status,
        get_deployment_options,
        get_best_practices
    )
    
    assert callable(check_deployment_status)
    assert callable(get_deployment_options)
    assert callable(get_best_practices)
