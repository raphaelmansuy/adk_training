"""
Test plugin functionality and configuration.
"""

import pytest
import asyncio
import time
from observability_agent.agent import (
    MetricsCollectorPlugin,
    AlertingPlugin,
    PerformanceProfilerPlugin,
    RequestMetrics,
    AggregateMetrics,
)


class TestDataClasses:
    """Test data classes for metrics."""

    def test_request_metrics_creation(self):
        """Test RequestMetrics can be created."""
        metrics = RequestMetrics(
            request_id="test-001",
            agent_name="test_agent",
            start_time=time.time()
        )
        assert metrics.request_id == "test-001"
        assert metrics.agent_name == "test_agent"
        assert metrics.success is True
        assert metrics.error is None

    def test_aggregate_metrics_creation(self):
        """Test AggregateMetrics can be created."""
        metrics = AggregateMetrics()
        assert metrics.total_requests == 0
        assert metrics.successful_requests == 0
        assert metrics.failed_requests == 0
        assert metrics.success_rate == 0.0
        assert metrics.avg_latency == 0.0
        assert metrics.avg_tokens == 0.0

    def test_aggregate_metrics_success_rate(self):
        """Test success rate calculation."""
        metrics = AggregateMetrics()
        metrics.total_requests = 10
        metrics.successful_requests = 8
        metrics.failed_requests = 2
        assert metrics.success_rate == 0.8

    def test_aggregate_metrics_avg_latency(self):
        """Test average latency calculation."""
        metrics = AggregateMetrics()
        metrics.total_requests = 5
        metrics.total_latency = 10.0
        assert metrics.avg_latency == 2.0

    def test_aggregate_metrics_avg_tokens(self):
        """Test average tokens calculation."""
        metrics = AggregateMetrics()
        metrics.total_requests = 4
        metrics.total_tokens = 400
        assert metrics.avg_tokens == 100.0


class TestMetricsCollectorPlugin:
    """Test MetricsCollectorPlugin functionality."""

    def test_plugin_initialization(self):
        """Test plugin can be initialized."""
        plugin = MetricsCollectorPlugin()
        assert plugin is not None
        assert plugin.metrics is not None
        assert isinstance(plugin.metrics, AggregateMetrics)
        assert plugin.current_requests == {}

    def test_get_summary(self):
        """Test get_summary returns formatted string."""
        plugin = MetricsCollectorPlugin()
        summary = plugin.get_summary()
        assert isinstance(summary, str)
        assert "METRICS SUMMARY" in summary
        assert "Total Requests:" in summary
        assert "Success Rate:" in summary


class TestAlertingPlugin:
    """Test AlertingPlugin functionality."""

    def test_plugin_initialization(self):
        """Test plugin can be initialized."""
        plugin = AlertingPlugin()
        assert plugin is not None
        assert plugin.latency_threshold == 5.0
        assert plugin.error_threshold == 3
        assert plugin.consecutive_errors == 0

    def test_plugin_initialization_custom_thresholds(self):
        """Test plugin can be initialized with custom thresholds."""
        plugin = AlertingPlugin(latency_threshold=3.0, error_threshold=2)
        assert plugin.latency_threshold == 3.0
        assert plugin.error_threshold == 2


class TestPerformanceProfilerPlugin:
    """Test PerformanceProfilerPlugin functionality."""

    def test_plugin_initialization(self):
        """Test plugin can be initialized."""
        plugin = PerformanceProfilerPlugin()
        assert plugin is not None
        assert plugin.profiles == []
        assert plugin.current_profile is None

    def test_get_profile_summary_empty(self):
        """Test get_profile_summary with no profiles."""
        plugin = PerformanceProfilerPlugin()
        summary = plugin.get_profile_summary()
        assert isinstance(summary, str)
        assert "No profiles collected" in summary

    def test_profile_data_structure(self):
        """Test that profiles can be added."""
        plugin = PerformanceProfilerPlugin()
        
        # Simulate adding a profile
        profile = {
            'tool': 'test_tool',
            'start_time': time.time(),
            'end_time': time.time() + 1.0,
            'duration': 1.0
        }
        plugin.profiles.append(profile)
        
        assert len(plugin.profiles) == 1
        assert plugin.profiles[0]['tool'] == 'test_tool'
        assert 'duration' in plugin.profiles[0]


class TestPluginIntegration:
    """Test plugin integration scenarios."""

    def test_all_plugins_can_be_instantiated(self):
        """Test that all plugins can be created together."""
        plugins = [
            MetricsCollectorPlugin(),
            AlertingPlugin(),
            PerformanceProfilerPlugin(),
        ]
        assert len(plugins) == 3
        assert all(plugin is not None for plugin in plugins)

    def test_plugins_are_base_plugin_instances(self):
        """Test that all plugins inherit from BasePlugin."""
        from google.adk.plugins import BasePlugin
        
        plugins = [
            MetricsCollectorPlugin(),
            AlertingPlugin(),
            PerformanceProfilerPlugin(),
        ]
        
        for plugin in plugins:
            assert isinstance(plugin, BasePlugin)
