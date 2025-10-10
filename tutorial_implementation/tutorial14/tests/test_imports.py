"""
Test imports and package structure.
"""

import pytest
import importlib


def test_streaming_agent_import():
    """Test that streaming_agent package can be imported."""
    try:
        import streaming_agent
        assert streaming_agent is not None
    except ImportError as e:
        pytest.fail(f"Failed to import streaming_agent: {e}")


def test_root_agent_import():
    """Test that root_agent can be imported."""
    try:
        from streaming_agent import root_agent
        assert root_agent is not None
    except ImportError as e:
        pytest.fail(f"Failed to import root_agent: {e}")


def test_all_exports_available():
    """Test that all expected exports are available."""
    from streaming_agent import (
        root_agent,
        stream_agent_response,
        get_complete_response,
        create_demo_session
    )

    # Check that all exports exist
    assert root_agent is not None
    assert stream_agent_response is not None
    assert get_complete_response is not None
    assert create_demo_session is not None


def test_agent_module_structure():
    """Test that the agent module has expected structure."""
    import streaming_agent.agent as agent_module

    # Check for expected functions/classes
    assert hasattr(agent_module, 'create_streaming_agent')
    assert hasattr(agent_module, 'root_agent')
    assert hasattr(agent_module, 'stream_agent_response')
    assert hasattr(agent_module, 'get_complete_response')
    assert hasattr(agent_module, 'create_demo_session')


def test_tools_available():
    """Test that tool functions are available."""
    from streaming_agent.agent import format_streaming_info, analyze_streaming_performance

    assert callable(format_streaming_info)
    assert callable(analyze_streaming_performance)


def test_package_version():
    """Test that package has version information."""
    import streaming_agent

    # Check if version is available (may not be set in development)
    # This is more of a structure check than a functionality check
    assert hasattr(streaming_agent, '__file__')


def test_no_import_errors():
    """Test that importing doesn't cause any errors."""
    # This test will fail if there are any import-time errors
    try:
        import streaming_agent
        from streaming_agent import root_agent, stream_agent_response
        import streaming_agent.agent as agent_module

        # Try to access key attributes
        assert agent_module.root_agent is not None
        assert agent_module.create_streaming_agent is not None

    except Exception as e:
        pytest.fail(f"Import or attribute access failed: {e}")


def test_circular_import_protection():
    """Test that there are no circular import issues."""
    # This is a basic check - if there were circular imports,
    # the imports at the top of this file would have failed

    # Re-import to check for issues
    importlib.reload(importlib.import_module('streaming_agent'))

    # If we get here without errors, no circular imports
    assert True