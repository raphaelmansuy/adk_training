"""
Test suite for Tutorial 26: Gemini Enterprise agent configuration and functionality.
"""

import pytest
from enterprise_agent.agent import root_agent


class TestAgentConfiguration:
    """Test the enterprise lead qualifier agent configuration."""

    def test_agent_exists(self):
        """Test that root_agent is defined."""
        assert root_agent is not None, "root_agent should be defined"

    def test_agent_name(self):
        """Test agent has correct name."""
        assert root_agent.name == "lead_qualifier"

    def test_agent_model(self):
        """Test agent uses correct model."""
        assert root_agent.model == "gemini-2.0-flash"

    def test_agent_description(self):
        """Test agent has description."""
        assert root_agent.description is not None
        assert len(root_agent.description) > 0
        assert "enterprise" in root_agent.description.lower()
        assert "qualification" in root_agent.description.lower()

    def test_agent_instruction(self):
        """Test agent has instruction."""
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0

    def test_instruction_content(self):
        """Test instruction contains key qualification criteria."""
        instruction = root_agent.instruction.lower()
        
        # Should mention key qualification criteria
        assert "company size" in instruction or "employees" in instruction
        assert "industry" in instruction or "industries" in instruction
        assert "budget" in instruction or "enterprise" in instruction
        
        # Should mention scoring thresholds
        assert "70" in instruction or "qualified" in instruction
        assert "score" in instruction

    def test_agent_has_tools(self):
        """Test agent has tools configured."""
        assert hasattr(root_agent, 'tools')
        assert root_agent.tools is not None
        assert len(root_agent.tools) > 0

    def test_agent_tool_count(self):
        """Test agent has expected number of tools."""
        # Should have at least check_company_size and score_lead
        assert len(root_agent.tools) >= 2


class TestAgentType:
    """Test that agent is correct type for enterprise deployment."""

    def test_agent_is_agent_instance(self):
        """Test that root_agent is an Agent instance."""
        from google.adk.agents import Agent
        assert isinstance(root_agent, Agent)

    def test_not_sequential_agent(self):
        """Test that this is a simple agent, not a workflow."""
        from google.adk.agents import SequentialAgent
        assert not isinstance(root_agent, SequentialAgent)

    def test_not_parallel_agent(self):
        """Test that this is a simple agent, not a parallel workflow."""
        from google.adk.agents import ParallelAgent
        assert not isinstance(root_agent, ParallelAgent)
