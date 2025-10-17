"""Test imports for data analysis agent."""


def test_import_agent():
    """Test that agent module imports correctly."""
    from agent import agent
    
    assert agent is not None


def test_import_root_agent():
    """Test that root_agent is available."""
    from agent import root_agent
    
    assert root_agent is not None


def test_import_app():
    """Test that FastAPI app imports correctly."""
    from agent import app
    
    assert app is not None


def test_import_adk_dependencies():
    """Test that ADK dependencies are available."""
    from google.adk.agents import Agent
    
    assert Agent is not None


def test_import_ag_ui_adk():
    """Test that ag_ui_adk is available."""
    from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
    
    assert ADKAgent is not None
    assert add_adk_fastapi_endpoint is not None


def test_import_pandas():
    """Test that pandas is available."""
    import pandas as pd
    
    assert pd is not None


def test_import_fastapi():
    """Test that FastAPI is available."""
    from fastapi import FastAPI
    
    assert FastAPI is not None
