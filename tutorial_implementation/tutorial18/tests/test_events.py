"""
Tests for event tracking functionality.
"""

import pytest
from datetime import datetime
from observability_agent import CustomerServiceMonitor


class TestEventLogging:
    """Test event logging functionality."""

    def test_tool_call_logging(self):
        """Test tool calls are logged correctly."""
        monitor = CustomerServiceMonitor()
        
        # Log a tool call
        monitor._log_tool_call('test_tool', {'arg1': 'value1'})
        
        assert len(monitor.events) == 1
        assert monitor.events[0]['type'] == 'tool_call'
        assert monitor.events[0]['tool'] == 'test_tool'
        assert monitor.events[0]['arguments'] == {'arg1': 'value1'}

    def test_agent_event_logging(self):
        """Test agent events are logged correctly."""
        monitor = CustomerServiceMonitor()
        
        # Log an agent event
        monitor._log_agent_event('test_event', {'key': 'value'})
        
        assert len(monitor.events) == 1
        assert monitor.events[0]['type'] == 'test_event'
        assert monitor.events[0]['data'] == {'key': 'value'}

    def test_event_timestamp(self):
        """Test events have timestamps."""
        monitor = CustomerServiceMonitor()
        
        monitor._log_tool_call('test_tool', {})
        
        assert 'timestamp' in monitor.events[0]
        # Verify timestamp is ISO format
        datetime.fromisoformat(monitor.events[0]['timestamp'])

    def test_multiple_events_logged(self):
        """Test multiple events are logged correctly."""
        monitor = CustomerServiceMonitor()
        
        monitor._log_tool_call('tool1', {'a': 1})
        monitor._log_tool_call('tool2', {'b': 2})
        monitor._log_agent_event('event1', {'c': 3})
        
        assert len(monitor.events) == 3
        assert monitor.events[0]['tool'] == 'tool1'
        assert monitor.events[1]['tool'] == 'tool2'
        assert monitor.events[2]['type'] == 'event1'


class TestEventReporting:
    """Test event reporting functionality."""

    def test_event_summary_generation(self):
        """Test event summary report generation."""
        monitor = CustomerServiceMonitor()
        
        # Add some test events
        monitor._log_tool_call('check_order_status', {'order_id': 'ORD-001'})
        monitor._log_agent_event('customer_query', {'query': 'test'})
        
        summary = monitor.get_event_summary()
        
        assert 'EVENT SUMMARY REPORT' in summary
        assert 'Total Events: 2' in summary
        assert 'tool_call: 1' in summary
        assert 'customer_query: 1' in summary

    def test_detailed_timeline_generation(self):
        """Test detailed timeline generation."""
        monitor = CustomerServiceMonitor()
        
        monitor._log_tool_call('test_tool', {'arg': 'value'})
        
        timeline = monitor.get_detailed_timeline()
        
        assert 'DETAILED EVENT TIMELINE' in timeline
        assert 'Type: tool_call' in timeline
        assert 'Tool: test_tool' in timeline

    def test_tool_usage_statistics(self):
        """Test tool usage statistics in summary."""
        monitor = CustomerServiceMonitor()
        
        # Log multiple tool calls
        monitor._log_tool_call('tool1', {})
        monitor._log_tool_call('tool1', {})
        monitor._log_tool_call('tool2', {})
        
        summary = monitor.get_event_summary()
        
        assert 'tool1: 2 calls' in summary
        assert 'tool2: 1 calls' in summary

    def test_escalation_tracking(self):
        """Test escalation tracking in reports."""
        monitor = CustomerServiceMonitor()
        
        monitor._log_agent_event('escalation', {
            'customer_id': 'CUST-001',
            'reason': 'High value refund'
        })
        
        summary = monitor.get_event_summary()
        
        assert 'Escalations: 1' in summary
        assert 'High value refund' in summary
