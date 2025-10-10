"""
Tests for imports and module structure.
"""

def test_import_customer_service_monitor():
    """Test CustomerServiceMonitor can be imported."""
    from observability_agent import CustomerServiceMonitor
    assert CustomerServiceMonitor is not None


def test_import_root_agent():
    """Test root_agent can be imported."""
    from observability_agent import root_agent
    assert root_agent is not None


def test_import_event_logger():
    """Test EventLogger can be imported."""
    from observability_agent import EventLogger
    assert EventLogger is not None


def test_import_metrics_collector():
    """Test MetricsCollector can be imported."""
    from observability_agent import MetricsCollector
    assert MetricsCollector is not None


def test_import_event_alerter():
    """Test EventAlerter can be imported."""
    from observability_agent import EventAlerter
    assert EventAlerter is not None


def test_import_agent_metrics():
    """Test AgentMetrics can be imported."""
    from observability_agent import AgentMetrics
    assert AgentMetrics is not None


def test_all_exports():
    """Test __all__ exports are correct."""
    import observability_agent
    
    expected_exports = [
        'CustomerServiceMonitor',
        'EventLogger',
        'MetricsCollector',
        'EventAlerter',
        'AgentMetrics',
        'root_agent'
    ]
    
    for export in expected_exports:
        assert export in observability_agent.__all__
