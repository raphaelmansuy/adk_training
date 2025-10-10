"""
Tests for observability classes (EventLogger, MetricsCollector, EventAlerter).
"""

import pytest
from unittest.mock import Mock
from observability_agent import EventLogger, MetricsCollector, EventAlerter, AgentMetrics
from google.adk.events import Event
from google.genai import types


class TestEventLogger:
    """Test EventLogger functionality."""

    def test_event_logger_initialization(self):
        """Test EventLogger initializes correctly."""
        logger = EventLogger()
        
        assert logger is not None
        assert logger.logger is not None

    def test_log_event_with_content(self):
        """Test logging event with content."""
        logger = EventLogger()
        
        event = Event(
            invocation_id='inv-123',
            author='test_agent',
            content=types.Content(parts=[types.Part(text='test message')])
        )
        
        # Should not raise exception
        logger.log_event(event)

    def test_log_event_without_content(self):
        """Test logging event without content."""
        logger = EventLogger()
        
        event = Event(
            invocation_id='inv-123',
            author='test_agent'
        )
        
        # Should not raise exception
        logger.log_event(event)


class TestMetricsCollector:
    """Test MetricsCollector functionality."""

    def test_metrics_collector_initialization(self):
        """Test MetricsCollector initializes correctly."""
        collector = MetricsCollector()
        
        assert collector is not None
        assert collector.metrics == {}

    def test_track_invocation_creates_metrics(self):
        """Test tracking invocation creates metrics entry."""
        collector = MetricsCollector()
        
        collector.track_invocation('test_agent', latency=0.5)
        
        assert 'test_agent' in collector.metrics
        assert collector.metrics['test_agent'].invocation_count == 1
        assert collector.metrics['test_agent'].total_latency == 0.5

    def test_track_multiple_invocations(self):
        """Test tracking multiple invocations."""
        collector = MetricsCollector()
        
        collector.track_invocation('test_agent', latency=0.5)
        collector.track_invocation('test_agent', latency=0.3)
        
        assert collector.metrics['test_agent'].invocation_count == 2
        assert collector.metrics['test_agent'].total_latency == 0.8

    def test_track_tool_calls(self):
        """Test tracking tool calls."""
        collector = MetricsCollector()
        
        collector.track_invocation('test_agent', latency=0.5, tool_calls=3)
        
        assert collector.metrics['test_agent'].tool_call_count == 3

    def test_track_errors(self):
        """Test tracking errors."""
        collector = MetricsCollector()
        
        collector.track_invocation('test_agent', latency=0.5, had_error=True)
        
        assert collector.metrics['test_agent'].error_count == 1

    def test_track_escalations(self):
        """Test tracking escalations."""
        collector = MetricsCollector()
        
        collector.track_invocation('test_agent', latency=0.5, escalated=True)
        
        assert collector.metrics['test_agent'].escalation_count == 1

    def test_get_summary_calculates_averages(self):
        """Test get_summary calculates correct averages."""
        collector = MetricsCollector()
        
        collector.track_invocation('test_agent', latency=0.5)
        collector.track_invocation('test_agent', latency=0.3)
        
        summary = collector.get_summary('test_agent')
        
        assert summary['invocations'] == 2
        assert summary['avg_latency'] == 0.4
        assert summary['error_rate'] == 0.0
        assert summary['escalation_rate'] == 0.0

    def test_get_summary_nonexistent_agent(self):
        """Test get_summary for non-existent agent."""
        collector = MetricsCollector()
        
        summary = collector.get_summary('nonexistent')
        
        assert summary == {}


class TestEventAlerter:
    """Test EventAlerter functionality."""

    def test_event_alerter_initialization(self):
        """Test EventAlerter initializes correctly."""
        alerter = EventAlerter()
        
        assert alerter is not None
        assert alerter.rules == []

    def test_add_rule(self):
        """Test adding alerting rule."""
        alerter = EventAlerter()
        
        condition = lambda e: True
        alert_fn = lambda e: None
        
        alerter.add_rule(condition, alert_fn)
        
        assert len(alerter.rules) == 1

    def test_check_event_triggers_alert(self):
        """Test event checking triggers alert when condition matches."""
        alerter = EventAlerter()
        
        alert_triggered = []
        
        def alert_fn(event):
            alert_triggered.append(event)
        
        # Rule that always triggers
        alerter.add_rule(lambda e: True, alert_fn)
        
        event = Event(invocation_id='inv-123', author='test')
        alerter.check_event(event)
        
        assert len(alert_triggered) == 1
        assert alert_triggered[0] == event

    def test_check_event_no_trigger(self):
        """Test event checking doesn't trigger when condition doesn't match."""
        alerter = EventAlerter()
        
        alert_triggered = []
        
        def alert_fn(event):
            alert_triggered.append(event)
        
        # Rule that never triggers
        alerter.add_rule(lambda e: False, alert_fn)
        
        event = Event(invocation_id='inv-123', author='test')
        alerter.check_event(event)
        
        assert len(alert_triggered) == 0

    def test_multiple_rules(self):
        """Test multiple alerting rules."""
        alerter = EventAlerter()
        
        alert1_triggered = []
        alert2_triggered = []
        
        alerter.add_rule(lambda e: True, lambda e: alert1_triggered.append(e))
        alerter.add_rule(lambda e: True, lambda e: alert2_triggered.append(e))
        
        event = Event(invocation_id='inv-123', author='test')
        alerter.check_event(event)
        
        assert len(alert1_triggered) == 1
        assert len(alert2_triggered) == 1


class TestAgentMetrics:
    """Test AgentMetrics dataclass."""

    def test_agent_metrics_initialization(self):
        """Test AgentMetrics initializes with defaults."""
        metrics = AgentMetrics()
        
        assert metrics.invocation_count == 0
        assert metrics.total_latency == 0.0
        assert metrics.tool_call_count == 0
        assert metrics.error_count == 0
        assert metrics.escalation_count == 0

    def test_agent_metrics_with_values(self):
        """Test AgentMetrics with custom values."""
        metrics = AgentMetrics(
            invocation_count=10,
            total_latency=5.5,
            tool_call_count=15,
            error_count=2,
            escalation_count=1
        )
        
        assert metrics.invocation_count == 10
        assert metrics.total_latency == 5.5
        assert metrics.tool_call_count == 15
        assert metrics.error_count == 2
        assert metrics.escalation_count == 1
