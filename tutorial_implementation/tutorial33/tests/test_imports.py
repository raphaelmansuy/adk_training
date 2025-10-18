"""
Test imports and module availability for Support Bot Agent
"""

import pytest


def test_root_agent_import():
    """Test that root_agent can be imported from support_bot module."""
    from support_bot import root_agent
    assert root_agent is not None


def test_agent_import_from_agent_module():
    """Test that root_agent can be imported from agent.py directly."""
    from support_bot.agent import root_agent
    assert root_agent is not None


def test_tools_import():
    """Test that tool functions can be imported."""
    from support_bot.agent import search_knowledge_base, create_support_ticket
    assert search_knowledge_base is not None
    assert create_support_ticket is not None


def test_agent_name():
    """Test that agent has the correct name."""
    from support_bot.agent import root_agent
    assert root_agent.name == "support_bot"


def test_agent_model():
    """Test that agent uses the correct model."""
    from support_bot.agent import root_agent
    assert "gemini" in root_agent.model.lower()


def test_agent_has_tools():
    """Test that agent has tools configured."""
    from support_bot.agent import root_agent
    assert hasattr(root_agent, 'tools')
    assert len(root_agent.tools) > 0


def test_agent_has_description():
    """Test that agent has a description."""
    from support_bot.agent import root_agent
    assert root_agent.description is not None
    assert len(root_agent.description) > 0


def test_agent_has_instruction():
    """Test that agent has instructions."""
    from support_bot.agent import root_agent
    assert root_agent.instruction is not None
    assert len(root_agent.instruction) > 0
