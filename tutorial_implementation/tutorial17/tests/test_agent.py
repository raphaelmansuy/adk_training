"""
Test suite for the A2A Agent implementation.
Tests agent configuration, tools, and A2A setup.
"""

import pytest
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent


class TestA2AAgent:
    """Test the main A2A agent configuration."""
    
    def test_root_agent_exists(self):
        """Test that root_agent exists and has correct configuration."""
        from a2a_orchestrator.agent import root_agent
        
        assert isinstance(root_agent, Agent)
        assert root_agent.name == "a2a_orchestrator"
        assert root_agent.description == "Coordinates multiple remote specialized agents using official ADK A2A"
    
    def test_root_agent_has_sub_agents(self):
        """Test that root_agent has the correct sub-agents."""
        from a2a_orchestrator.agent import root_agent
        
        assert hasattr(root_agent, 'sub_agents')
        assert len(root_agent.sub_agents) == 3
        
        agent_names = [agent.name for agent in root_agent.sub_agents]
        assert "research_specialist" in agent_names
        assert "data_analyst" in agent_names
        assert "content_writer" in agent_names
    
    def test_root_agent_has_tools(self):
        """Test that root_agent has the required tools."""
        from a2a_orchestrator.agent import root_agent
        
        assert hasattr(root_agent, 'tools')
        assert len(root_agent.tools) >= 2
        
        # Check tool names using the tool's name property
        tool_names = [tool.name for tool in root_agent.tools]
        assert "check_agent_availability" in tool_names
        assert "log_coordination_step" in tool_names
    
    def test_check_agent_availability_function(self):
        """Test the check_agent_availability tool function."""
        from a2a_orchestrator.agent import check_agent_availability
        
        # Test with invalid URL (should return error)
        result = check_agent_availability("test_agent", "http://invalid-url:9999")
        assert result["status"] == "error"
        assert result["available"] is False


class TestAgentConfiguration:
    """Test agent configuration and setup."""
    
    def test_agent_model_configuration(self):
        """Test that agent uses the correct model."""
        from a2a_orchestrator.agent import root_agent
        
        assert root_agent.model == "gemini-2.0-flash"
    
    def test_agent_instruction_exists(self):
        """Test that agent has instruction."""
        from a2a_orchestrator.agent import root_agent
        
        assert hasattr(root_agent, 'instruction')
        assert root_agent.instruction is not None
        assert len(root_agent.instruction.strip()) > 0
    
    def test_sub_agent_configurations(self):
        """Test that sub-agents have correct configurations."""
        from a2a_orchestrator.agent import root_agent
        
        for sub_agent in root_agent.sub_agents:
            assert isinstance(sub_agent, RemoteA2aAgent)
            # RemoteA2aAgent uses agent_card parameter instead of base_url
            assert hasattr(sub_agent, 'name')
            assert hasattr(sub_agent, 'description')
            # Check that it's a remote agent (has remote connection capabilities)


class TestTools:
    """Test the agent tools."""
    
    def test_check_agent_availability_returns_dict(self):
        """Test that check_agent_availability returns proper format."""
        from a2a_orchestrator.agent import check_agent_availability
        
        result = check_agent_availability("test", "http://invalid:9999")
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "available" in result
        assert "report" in result
    
    def test_log_coordination_step_returns_dict(self):
        """Test that log_coordination_step returns proper format."""
        from a2a_orchestrator.agent import log_coordination_step
        
        result = log_coordination_step("test step", "test_agent")
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "report" in result
        assert "step" in result
        assert "agent" in result
        assert result["status"] == "success"