"""
Tests for observability_agent configuration and initialization.
"""

import pytest
from observability_agent import CustomerServiceMonitor, root_agent
from google.adk.agents import Agent


class TestAgentConfiguration:
    """Test agent configuration and initialization."""

    def test_monitor_initialization(self):
        """Test CustomerServiceMonitor initializes correctly."""
        monitor = CustomerServiceMonitor()
        
        assert monitor is not None
        assert isinstance(monitor.agent, Agent)
        assert monitor.events == []
        assert monitor.runner is not None

    def test_agent_name(self):
        """Test agent has correct name."""
        monitor = CustomerServiceMonitor()
        
        assert monitor.agent.name == 'customer_service'

    def test_agent_model(self):
        """Test agent uses correct model."""
        monitor = CustomerServiceMonitor()
        
        assert 'gemini' in monitor.agent.model.lower()

    def test_agent_has_tools(self):
        """Test agent has required tools."""
        monitor = CustomerServiceMonitor()
        
        assert monitor.agent.tools is not None
        assert len(monitor.agent.tools) == 3

    def test_agent_instruction(self):
        """Test agent has instruction configured."""
        monitor = CustomerServiceMonitor()
        
        assert monitor.agent.instruction is not None
        assert len(monitor.agent.instruction) > 0
        assert 'customer service' in monitor.agent.instruction.lower()

    def test_root_agent_exported(self):
        """Test root_agent is properly exported."""
        assert root_agent is not None
        assert isinstance(root_agent, Agent)
        assert root_agent.name == 'customer_service'

    def test_agent_description(self):
        """Test agent has description."""
        monitor = CustomerServiceMonitor()
        
        assert monitor.agent.description is not None
        assert 'event tracking' in monitor.agent.description.lower()


class TestToolConfiguration:
    """Test tool configuration."""

    def test_tools_are_callable(self):
        """Test all tools are callable."""
        monitor = CustomerServiceMonitor()
        
        for tool in monitor.agent.tools:
            assert callable(tool)

    def test_check_order_status_tool(self):
        """Test check_order_status tool exists and is configured."""
        monitor = CustomerServiceMonitor()
        
        tool_names = [tool.__name__ for tool in monitor.agent.tools if hasattr(tool, '__name__')]
        assert 'check_order_status' in tool_names

    def test_process_refund_tool(self):
        """Test process_refund tool exists and is configured."""
        monitor = CustomerServiceMonitor()
        
        tool_names = [tool.__name__ for tool in monitor.agent.tools if hasattr(tool, '__name__')]
        assert 'process_refund' in tool_names

    def test_check_inventory_tool(self):
        """Test check_inventory tool exists and is configured."""
        monitor = CustomerServiceMonitor()
        
        tool_names = [tool.__name__ for tool in monitor.agent.tools if hasattr(tool, '__name__')]
        assert 'check_inventory' in tool_names
