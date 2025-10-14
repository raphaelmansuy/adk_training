"""Test the Best Practices Agent and its tools."""

import pytest
from best_practices_agent import root_agent
from best_practices_agent.agent import (
    validate_input_tool,
    retry_with_backoff_tool,
    circuit_breaker_call_tool,
    cache_operation_tool,
    batch_process_tool,
    health_check_tool,
    get_metrics_tool,
    CircuitBreaker,
    CachedDataStore,
    MetricsCollector,
    CircuitState,
    InputRequest,
)


# ============================================================================
# AGENT CONFIGURATION TESTS
# ============================================================================

class TestAgentConfiguration:
    """Test agent configuration and setup."""
    
    def test_agent_exists(self):
        """Test that root_agent is properly defined."""
        assert root_agent is not None
    
    def test_agent_name(self):
        """Test that agent has correct name."""
        assert root_agent.name == "best_practices_agent"
    
    def test_agent_model(self):
        """Test that agent uses correct model."""
        assert root_agent.model == "gemini-2.0-flash-exp"
    
    def test_agent_has_description(self):
        """Test that agent has description."""
        assert root_agent.description is not None
        assert len(root_agent.description) > 0
        assert "production-ready" in root_agent.description.lower()
    
    def test_agent_has_instruction(self):
        """Test that agent has instructions."""
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0
    
    def test_agent_has_tools(self):
        """Test that agent has all required tools."""
        assert root_agent.tools is not None
        assert len(root_agent.tools) == 7
        
        # Check tool names
        tool_names = [tool.__name__ for tool in root_agent.tools]
        expected_tools = [
            'validate_input_tool',
            'retry_with_backoff_tool',
            'circuit_breaker_call_tool',
            'cache_operation_tool',
            'batch_process_tool',
            'health_check_tool',
            'get_metrics_tool',
        ]
        
        for expected in expected_tools:
            assert expected in tool_names, f"Missing tool: {expected}"


# ============================================================================
# VALIDATION TESTS
# ============================================================================

class TestValidation:
    """Test input validation functionality."""
    
    def test_validate_valid_email(self):
        """Test validation with valid email."""
        result = validate_input_tool(
            email="user@example.com",
            text="Hello world",
            priority="normal"
        )
        
        assert result['status'] == 'success'
        assert 'validated_data' in result
        assert result['validated_data']['email'] == "user@example.com"
    
    def test_validate_invalid_email(self):
        """Test validation with invalid email."""
        result = validate_input_tool(
            email="invalid-email",
            text="Hello world",
            priority="normal"
        )
        
        assert result['status'] == 'error'
        assert 'error' in result
    
    def test_validate_invalid_priority(self):
        """Test validation with invalid priority."""
        result = validate_input_tool(
            email="user@example.com",
            text="Hello world",
            priority="super-urgent"  # Invalid
        )
        
        assert result['status'] == 'error'
        assert 'error' in result
    
    def test_validate_dangerous_text(self):
        """Test validation blocks dangerous patterns."""
        result = validate_input_tool(
            email="user@example.com",
            text="DROP TABLE users",
            priority="normal"
        )
        
        assert result['status'] == 'error'
        assert 'dangerous' in result['error'].lower() or 'dangerous' in result['report'].lower()
    
    def test_validate_xss_attempt(self):
        """Test validation blocks XSS attempts."""
        result = validate_input_tool(
            email="user@example.com",
            text="Hello <script>alert('xss')</script>",
            priority="normal"
        )
        
        assert result['status'] == 'error'
    
    def test_validate_empty_text(self):
        """Test validation rejects empty text."""
        result = validate_input_tool(
            email="user@example.com",
            text="",
            priority="normal"
        )
        
        assert result['status'] == 'error'
    
    def test_input_request_model(self):
        """Test InputRequest Pydantic model."""
        # Valid request
        request = InputRequest(
            email="test@example.com",
            text="Hello",
            priority="high"
        )
        assert request.email == "test@example.com"
        assert request.priority == "high"
        
        # Invalid priority should raise error
        with pytest.raises(ValueError):
            InputRequest(
                email="test@example.com",
                text="Hello",
                priority="invalid"
            )


# ============================================================================
# RETRY LOGIC TESTS
# ============================================================================

class TestRetryLogic:
    """Test retry with exponential backoff."""
    
    def test_retry_eventually_succeeds(self):
        """Test that retry logic can succeed."""
        result = retry_with_backoff_tool(
            operation="test_operation",
            max_retries=5
        )
        
        # Should eventually succeed (or document all attempts)
        assert 'status' in result
        assert 'attempts' in result or 'report' in result
    
    def test_retry_with_max_retries(self):
        """Test retry respects max_retries."""
        result = retry_with_backoff_tool(
            operation="test_operation",
            max_retries=1
        )
        
        assert 'status' in result
        assert 'report' in result
    
    def test_retry_includes_timing(self):
        """Test that retry includes timing information."""
        result = retry_with_backoff_tool(
            operation="test_operation",
            max_retries=2
        )
        
        assert 'total_time_ms' in result


# ============================================================================
# CIRCUIT BREAKER TESTS
# ============================================================================

class TestCircuitBreaker:
    """Test circuit breaker pattern."""
    
    def test_circuit_breaker_success(self):
        """Test circuit breaker with successful call."""
        result = circuit_breaker_call_tool(
            service_name="test_service",
            simulate_failure=False
        )
        
        assert result['status'] == 'success'
        assert result['circuit_state'] in ['closed', 'open', 'half_open']
    
    def test_circuit_breaker_failure(self):
        """Test circuit breaker with failed call."""
        result = circuit_breaker_call_tool(
            service_name="test_service",
            simulate_failure=True
        )
        
        assert result['status'] == 'error'
        assert 'circuit_state' in result
    
    def test_circuit_breaker_class(self):
        """Test CircuitBreaker class directly."""
        breaker = CircuitBreaker(failure_threshold=2, timeout_seconds=1)
        
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failures == 0
        
        # Simulate failures
        def failing_func():
            raise Exception("Test failure")
        
        # First failure
        with pytest.raises(Exception):
            breaker.call(failing_func)
        assert breaker.failures == 1
        
        # Second failure should open circuit
        with pytest.raises(Exception):
            breaker.call(failing_func)
        assert breaker.state == CircuitState.OPEN
    
    def test_circuit_breaker_enum(self):
        """Test CircuitState enum."""
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"


# ============================================================================
# CACHING TESTS
# ============================================================================

class TestCaching:
    """Test caching functionality."""
    
    def test_cache_set_and_get(self):
        """Test cache set and get operations."""
        # Set value
        set_result = cache_operation_tool(
            key="test_key",
            value="test_value",
            operation="set"
        )
        assert set_result['status'] == 'success'
        
        # Get value
        get_result = cache_operation_tool(
            key="test_key",
            operation="get"
        )
        assert get_result['status'] == 'success'
        assert get_result['cache_hit'] == True
        assert get_result['value'] == "test_value"
    
    def test_cache_miss(self):
        """Test cache miss scenario."""
        result = cache_operation_tool(
            key="nonexistent_key",
            operation="get"
        )
        
        assert result['status'] == 'success'
        assert result['cache_hit'] == False
    
    def test_cache_stats(self):
        """Test cache statistics."""
        result = cache_operation_tool(
            key="any",
            operation="stats"
        )
        
        assert result['status'] == 'success'
        assert 'statistics' in result
        assert 'hits' in result['statistics']
        assert 'misses' in result['statistics']
    
    def test_cache_set_without_value(self):
        """Test that cache set requires value."""
        result = cache_operation_tool(
            key="test_key",
            operation="set"
        )
        
        assert result['status'] == 'error'
    
    def test_cached_data_store_class(self):
        """Test CachedDataStore class directly."""
        cache = CachedDataStore(ttl_seconds=1)
        
        # Set and get within TTL
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        
        # Check stats
        stats = cache.stats()
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'hit_rate' in stats


# ============================================================================
# BATCH PROCESSING TESTS
# ============================================================================

class TestBatchProcessing:
    """Test batch processing functionality."""
    
    def test_batch_process_items(self):
        """Test batch processing of items."""
        items = ["item1", "item2", "item3"]
        result = batch_process_tool(items=items)
        
        assert result['status'] == 'success'
        assert result['items_processed'] == 3
        assert 'results' in result
        assert len(result['results']) == 3
    
    def test_batch_process_single_item(self):
        """Test batch processing with single item."""
        items = ["single_item"]
        result = batch_process_tool(items=items)
        
        assert result['status'] == 'success'
        assert result['items_processed'] == 1
    
    def test_batch_process_empty_list(self):
        """Test batch processing with empty list."""
        result = batch_process_tool(items=[])
        
        assert result['status'] == 'error'
    
    def test_batch_process_efficiency(self):
        """Test that batch processing reports efficiency."""
        items = ["a", "b", "c", "d", "e"]
        result = batch_process_tool(items=items)
        
        if result['status'] == 'success':
            assert 'processing_time_ms' in result
            assert 'efficiency_gain' in result


# ============================================================================
# MONITORING TESTS
# ============================================================================

class TestMonitoring:
    """Test monitoring and observability."""
    
    def test_health_check(self):
        """Test health check tool."""
        result = health_check_tool()
        
        assert result['status'] == 'success'
        assert 'health' in result
        assert 'status' in result['health']
        assert result['health']['status'] in ['healthy', 'degraded', 'unhealthy']
    
    def test_get_metrics(self):
        """Test metrics retrieval."""
        result = get_metrics_tool()
        
        assert result['status'] == 'success'
        assert 'metrics' in result
        assert 'total_requests' in result['metrics']
    
    def test_metrics_collector_class(self):
        """Test MetricsCollector class directly."""
        collector = MetricsCollector()
        
        # Record some requests
        collector.record_request(latency=0.1, error=False)
        collector.record_request(latency=0.2, error=True)
        
        metrics = collector.get_metrics()
        
        assert metrics['total_requests'] == 2
        assert metrics['total_errors'] == 1
        assert 'error_rate' in metrics
        assert 'avg_latency_ms' in metrics
        
        # Test health check
        health = collector.health_check()
        assert 'status' in health
        assert 'metrics' in health


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Test integration scenarios."""
    
    def test_full_workflow(self):
        """Test a complete workflow using multiple tools."""
        # 1. Validate input
        validation = validate_input_tool(
            email="user@example.com",
            text="Process order",
            priority="high"
        )
        assert validation['status'] == 'success'
        
        # 2. Cache some data
        cache_set = cache_operation_tool(
            key="workflow_data",
            value="important_data",
            operation="set"
        )
        assert cache_set['status'] == 'success'
        
        # 3. Batch process
        batch = batch_process_tool(items=["order1", "order2"])
        assert batch['status'] == 'success'
        
        # 4. Check health
        health = health_check_tool()
        assert health['status'] == 'success'
    
    def test_error_handling_workflow(self):
        """Test error handling across multiple operations."""
        # Invalid validation
        result1 = validate_input_tool(
            email="invalid",
            text="test",
            priority="normal"
        )
        assert result1['status'] == 'error'
        
        # Invalid cache operation
        result2 = cache_operation_tool(
            key="test",
            operation="invalid_op"
        )
        assert result2['status'] == 'error'
        
        # Empty batch
        result3 = batch_process_tool(items=[])
        assert result3['status'] == 'error'
        
        # Health should still work despite errors
        health = health_check_tool()
        assert health['status'] == 'success'


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Test performance characteristics."""
    
    def test_validation_performance(self):
        """Test that validation completes quickly."""
        result = validate_input_tool(
            email="test@example.com",
            text="Quick test",
            priority="normal"
        )
        
        if 'validation_time_ms' in result:
            # Should complete in reasonable time
            assert result['validation_time_ms'] < 1000  # Less than 1 second
    
    def test_batch_processing_faster_than_sequential(self):
        """Test that batch processing is efficient."""
        items = [f"item{i}" for i in range(10)]
        result = batch_process_tool(items=items)
        
        if result['status'] == 'success':
            # Batch should be faster than sequential
            if 'estimated_sequential_time_ms' in result:
                assert result['processing_time_ms'] <= result['estimated_sequential_time_ms']
