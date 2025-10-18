"""
Test agent imports and configuration
"""

import pytest
from data_viz_agent import root_agent


def test_agent_imported():
    """Test that root_agent can be imported."""
    assert root_agent is not None


def test_agent_configuration():
    """Test that agent is properly configured."""
    assert root_agent.name == "data_viz_agent"
    assert root_agent.model == "gemini-2.0-flash"
    assert root_agent.code_executor is not None


def test_agent_has_code_executor():
    """Test that agent has code execution capability."""
    from google.adk.code_executors import BuiltInCodeExecutor
    assert isinstance(root_agent.code_executor, BuiltInCodeExecutor)


def test_agent_instruction_set():
    """Test that agent has proper instruction."""
    assert root_agent.instruction is not None
    assert "visualization" in root_agent.instruction.lower()
    assert "matplotlib" in root_agent.instruction.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
