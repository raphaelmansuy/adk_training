"""Test that all required imports work correctly."""

import pytest


def test_import_agent():
    """Test that agent module can be imported."""
    from best_practices_agent import root_agent
    assert root_agent is not None


def test_import_google_adk():
    """Test that Google ADK can be imported."""
    from google.adk.agents import Agent
    assert Agent is not None


def test_import_pydantic():
    """Test that Pydantic can be imported."""
    from pydantic import BaseModel, Field
    assert BaseModel is not None
    assert Field is not None


def test_import_google_genai():
    """Test that Google GenAI can be imported."""
    from google.genai import types
    assert types is not None


def test_all_tools_importable():
    """Test that all tools can be imported from agent module."""
    from best_practices_agent.agent import (
        validate_input_tool,
        retry_with_backoff_tool,
        circuit_breaker_call_tool,
        cache_operation_tool,
        batch_process_tool,
        health_check_tool,
        get_metrics_tool,
    )
    
    assert validate_input_tool is not None
    assert retry_with_backoff_tool is not None
    assert circuit_breaker_call_tool is not None
    assert cache_operation_tool is not None
    assert batch_process_tool is not None
    assert health_check_tool is not None
    assert get_metrics_tool is not None


def test_import_classes():
    """Test that supporting classes can be imported."""
    from best_practices_agent.agent import (
        CircuitBreaker,
        CachedDataStore,
        MetricsCollector,
        CircuitState,
    )
    
    assert CircuitBreaker is not None
    assert CachedDataStore is not None
    assert MetricsCollector is not None
    assert CircuitState is not None
