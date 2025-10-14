"""
Best Practices Agent - Production-Ready Patterns

Demonstrates:
- Input validation with Pydantic
- Comprehensive error handling
- Circuit breaker pattern
- Retry logic with exponential backoff
- Performance optimization (caching, batching)
- Monitoring and health metrics
"""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Dict, Any, List, Optional
from functools import lru_cache
from enum import Enum
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# MODELS & VALIDATION
# ============================================================================

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class InputRequest(BaseModel):
    """Validated input request."""
    
    email: Optional[EmailStr] = Field(None, description="Email address to validate")
    text: str = Field(..., min_length=1, max_length=10000, description="Text content")
    priority: str = Field("normal", description="Priority level")
    
    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        """Validate priority values."""
        valid = ["low", "normal", "high", "urgent"]
        if v not in valid:
            raise ValueError(f"Priority must be one of: {', '.join(valid)}")
        return v
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        """Validate text content for dangerous patterns."""
        dangerous = ['DROP TABLE', 'DELETE FROM', '; --', '<SCRIPT>']
        v_upper = v.upper()
        
        for pattern in dangerous:
            if pattern in v_upper:
                raise ValueError(f"Potentially dangerous pattern detected: {pattern}")
        
        return v


# ============================================================================
# CIRCUIT BREAKER PATTERN
# ============================================================================

class CircuitBreaker:
    """
    Circuit breaker for external dependencies.
    
    Prevents cascading failures by temporarily blocking requests
    to failing services.
    """
    
    def __init__(self, failure_threshold: int = 3, timeout_seconds: int = 30):
        self.failure_threshold = failure_threshold
        self.timeout = timeout_seconds
        self.failures = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.success_count = 0
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        
        # Check if circuit is open
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                logger.info("Circuit breaker entering HALF_OPEN state")
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception(f"Circuit breaker is OPEN. Try again in {int(self.timeout - (time.time() - self.last_failure_time))}s")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset or close circuit
            if self.state == CircuitState.HALF_OPEN:
                logger.info("Circuit breaker closing after successful call")
                self.state = CircuitState.CLOSED
                self.failures = 0
                self.success_count = 0
            
            return result
            
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.failures >= self.failure_threshold:
                logger.warning(f"Circuit breaker opening after {self.failures} failures")
                self.state = CircuitState.OPEN
            
            raise


# Global circuit breaker instance
external_service_breaker = CircuitBreaker(failure_threshold=3, timeout_seconds=30)


# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================

class CachedDataStore:
    """Time-based cache with TTL."""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                self.hits += 1
                return value
            del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value: Any):
        """Store value with current timestamp."""
        self.cache[key] = (value, time.time())
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'size': len(self.cache)
        }


# Global cache instance
data_cache = CachedDataStore(ttl_seconds=300)


# ============================================================================
# METRICS & MONITORING
# ============================================================================

class MetricsCollector:
    """Collect and track system metrics."""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_latency = 0.0
        self.start_time = time.time()
    
    def record_request(self, latency: float, error: bool = False):
        """Record request metrics."""
        self.request_count += 1
        self.total_latency += latency
        if error:
            self.error_count += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / self.request_count if self.request_count > 0 else 0
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0
        
        return {
            'uptime_seconds': round(uptime, 2),
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'error_rate': f"{error_rate:.2f}%",
            'avg_latency_ms': round(avg_latency * 1000, 2),
            'requests_per_second': round(self.request_count / uptime, 2) if uptime > 0 else 0
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check."""
        metrics = self.get_metrics()
        
        # Determine health status
        error_rate = float(metrics['error_rate'].rstrip('%'))
        
        if error_rate > 50:
            status = "unhealthy"
        elif error_rate > 10:
            status = "degraded"
        else:
            status = "healthy"
        
        return {
            'status': status,
            'circuit_breaker_state': external_service_breaker.state.value,
            'cache_stats': data_cache.stats(),
            'metrics': metrics
        }


# Global metrics collector
metrics = MetricsCollector()


# ============================================================================
# TOOLS
# ============================================================================

def validate_input_tool(
    email: str,
    text: str,
    priority: str = "normal",
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Validate user input with comprehensive checks.
    
    Demonstrates:
    - Pydantic validation
    - Input sanitization
    - Security best practices
    
    Args:
        email: Email address to validate
        text: Text content to validate
        priority: Priority level (low, normal, high, urgent)
        tool_context: ADK tool context
    
    Returns:
        Dict with validation results
    """
    start_time = time.time()
    
    try:
        # Validate with Pydantic
        request = InputRequest(
            email=email if email else None,
            text=text,
            priority=priority
        )
        
        latency = time.time() - start_time
        metrics.record_request(latency, error=False)
        
        return {
            'status': 'success',
            'report': f'✅ Input validation passed for email={email}, priority={priority}',
            'validated_data': {
                'email': request.email,
                'text_length': len(request.text),
                'priority': request.priority
            },
            'validation_time_ms': round(latency * 1000, 2)
        }
        
    except ValueError as e:
        latency = time.time() - start_time
        metrics.record_request(latency, error=True)
        
        return {
            'status': 'error',
            'error': str(e),
            'report': f'❌ Validation failed: {str(e)}',
            'validation_time_ms': round(latency * 1000, 2)
        }
    
    except Exception as e:
        latency = time.time() - start_time
        metrics.record_request(latency, error=True)
        logger.error(f"Unexpected validation error: {e}")
        
        return {
            'status': 'error',
            'error': 'Internal validation error',
            'report': '❌ An unexpected error occurred during validation',
            'validation_time_ms': round(latency * 1000, 2)
        }


def retry_with_backoff_tool(
    operation: str,
    max_retries: int = 3,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Execute operation with retry logic and exponential backoff.
    
    Demonstrates:
    - Error handling
    - Retry patterns
    - Exponential backoff
    
    Args:
        operation: Operation to execute
        max_retries: Maximum number of retry attempts
        tool_context: ADK tool context
    
    Returns:
        Dict with execution results
    """
    start_time = time.time()
    
    def simulated_operation():
        """Simulate an operation that might fail."""
        # 30% chance of failure
        if random.random() < 0.3:
            raise Exception("Simulated transient error")
        return {"result": f"Successfully processed: {operation}"}
    
    attempts = []
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1} of {max_retries}")
            result = simulated_operation()
            
            latency = time.time() - start_time
            metrics.record_request(latency, error=False)
            
            return {
                'status': 'success',
                'report': f'✅ Operation succeeded on attempt {attempt + 1}',
                'result': result,
                'attempts': attempt + 1,
                'total_time_ms': round(latency * 1000, 2)
            }
            
        except Exception as e:
            attempts.append({
                'attempt': attempt + 1,
                'error': str(e),
                'timestamp': time.time()
            })
            
            if attempt < max_retries - 1:
                backoff_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {backoff_time}s")
                time.sleep(backoff_time)
            else:
                latency = time.time() - start_time
                metrics.record_request(latency, error=True)
                
                return {
                    'status': 'error',
                    'error': f'Operation failed after {max_retries} attempts',
                    'report': f'❌ All {max_retries} retry attempts failed',
                    'attempts': attempts,
                    'total_time_ms': round(latency * 1000, 2)
                }
    
    latency = time.time() - start_time
    metrics.record_request(latency, error=True)
    
    return {
        'status': 'error',
        'error': 'Max retries exceeded',
        'report': '❌ Operation failed',
        'total_time_ms': round(latency * 1000, 2)
    }


def circuit_breaker_call_tool(
    service_name: str,
    simulate_failure: bool = False,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Call external service with circuit breaker protection.
    
    Demonstrates:
    - Circuit breaker pattern
    - Graceful degradation
    - Failure isolation
    
    Args:
        service_name: Name of the service to call
        simulate_failure: Whether to simulate a failure
        tool_context: ADK tool context
    
    Returns:
        Dict with call results
    """
    start_time = time.time()
    
    def external_service_call():
        """Simulate external service call."""
        if simulate_failure:
            raise Exception(f"Service {service_name} is unavailable")
        return {"data": f"Response from {service_name}"}
    
    try:
        result = external_service_breaker.call(external_service_call)
        
        latency = time.time() - start_time
        metrics.record_request(latency, error=False)
        
        return {
            'status': 'success',
            'report': f'✅ Successfully called {service_name}',
            'result': result,
            'circuit_state': external_service_breaker.state.value,
            'latency_ms': round(latency * 1000, 2)
        }
        
    except Exception as e:
        latency = time.time() - start_time
        metrics.record_request(latency, error=True)
        
        return {
            'status': 'error',
            'error': str(e),
            'report': f'❌ Failed to call {service_name}: {str(e)}',
            'circuit_state': external_service_breaker.state.value,
            'failures': external_service_breaker.failures,
            'latency_ms': round(latency * 1000, 2)
        }


def cache_operation_tool(
    key: str,
    value: Optional[str] = None,
    operation: str = "get",
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Perform caching operations for performance optimization.
    
    Demonstrates:
    - Caching strategies
    - TTL management
    - Cache statistics
    
    Args:
        key: Cache key
        value: Value to cache (for set operation)
        operation: Operation to perform (get, set, stats)
        tool_context: ADK tool context
    
    Returns:
        Dict with operation results
    """
    start_time = time.time()
    
    try:
        if operation == "set":
            if value is None:
                return {
                    'status': 'error',
                    'error': 'Value required for set operation',
                    'report': '❌ Cannot set cache without value'
                }
            
            data_cache.set(key, value)
            
            return {
                'status': 'success',
                'report': f'✅ Cached value for key: {key}',
                'operation': 'set',
                'key': key
            }
        
        elif operation == "get":
            cached_value = data_cache.get(key)
            
            if cached_value is not None:
                return {
                    'status': 'success',
                    'report': f'✅ Cache HIT for key: {key}',
                    'operation': 'get',
                    'key': key,
                    'value': cached_value,
                    'cache_hit': True
                }
            else:
                return {
                    'status': 'success',
                    'report': f'ℹ️  Cache MISS for key: {key}',
                    'operation': 'get',
                    'key': key,
                    'cache_hit': False
                }
        
        elif operation == "stats":
            stats = data_cache.stats()
            
            return {
                'status': 'success',
                'report': '✅ Cache statistics retrieved',
                'operation': 'stats',
                'statistics': stats
            }
        
        else:
            return {
                'status': 'error',
                'error': f'Unknown operation: {operation}',
                'report': f'❌ Invalid operation. Use: get, set, or stats'
            }
    
    except Exception as e:
        latency = time.time() - start_time
        metrics.record_request(latency, error=True)
        logger.error(f"Cache operation error: {e}")
        
        return {
            'status': 'error',
            'error': str(e),
            'report': f'❌ Cache operation failed: {str(e)}'
        }


def batch_process_tool(
    items: List[str],
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Batch process multiple items for efficiency.
    
    Demonstrates:
    - Batch processing
    - Performance optimization
    - Resource efficiency
    
    Args:
        items: List of items to process
        tool_context: ADK tool context
    
    Returns:
        Dict with batch processing results
    """
    start_time = time.time()
    
    try:
        if not items or len(items) == 0:
            return {
                'status': 'error',
                'error': 'No items provided',
                'report': '❌ Cannot batch process empty list'
            }
        
        # Process items in batch
        results = []
        for i, item in enumerate(items):
            results.append({
                'index': i,
                'item': item,
                'processed': f"PROCESSED-{item}",
                'timestamp': time.time()
            })
        
        latency = time.time() - start_time
        metrics.record_request(latency, error=False)
        
        # Calculate efficiency gain
        sequential_time_estimate = len(items) * 0.1  # Assume 100ms per item
        time_saved = sequential_time_estimate - latency
        
        return {
            'status': 'success',
            'report': f'✅ Batch processed {len(items)} items in {round(latency * 1000, 2)}ms',
            'items_processed': len(items),
            'results': results,
            'processing_time_ms': round(latency * 1000, 2),
            'estimated_sequential_time_ms': round(sequential_time_estimate * 1000, 2),
            'time_saved_ms': round(time_saved * 1000, 2) if time_saved > 0 else 0,
            'efficiency_gain': f"{round(time_saved / sequential_time_estimate * 100, 1)}%" if sequential_time_estimate > 0 else "0%"
        }
        
    except Exception as e:
        latency = time.time() - start_time
        metrics.record_request(latency, error=True)
        logger.error(f"Batch processing error: {e}")
        
        return {
            'status': 'error',
            'error': str(e),
            'report': f'❌ Batch processing failed: {str(e)}'
        }


def health_check_tool(
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Perform comprehensive health check.
    
    Demonstrates:
    - Health monitoring
    - System metrics
    - Observability patterns
    
    Args:
        tool_context: ADK tool context
    
    Returns:
        Dict with health status
    """
    try:
        health = metrics.health_check()
        
        return {
            'status': 'success',
            'report': f'✅ System health: {health["status"].upper()}',
            'health': health
        }
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        
        return {
            'status': 'error',
            'error': str(e),
            'report': f'❌ Health check failed: {str(e)}'
        }


def get_metrics_tool(
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Get current system metrics.
    
    Demonstrates:
    - Metrics collection
    - Performance monitoring
    - Observability
    
    Args:
        tool_context: ADK tool context
    
    Returns:
        Dict with system metrics
    """
    try:
        system_metrics = metrics.get_metrics()
        
        return {
            'status': 'success',
            'report': f'✅ Retrieved system metrics ({system_metrics["total_requests"]} requests)',
            'metrics': system_metrics
        }
        
    except Exception as e:
        logger.error(f"Metrics retrieval error: {e}")
        
        return {
            'status': 'error',
            'error': str(e),
            'report': f'❌ Failed to retrieve metrics: {str(e)}'
        }


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

root_agent = Agent(
    name="best_practices_agent",
    model="gemini-2.0-flash-exp",
    description="Production-ready agent demonstrating best practices for security, performance, reliability, and observability",
    instruction="""
You are a production-ready agent demonstrating best practices for building robust, secure, and performant systems.

## Your Capabilities

You have access to tools that demonstrate:

**Security & Validation:**
- Input validation with comprehensive checks
- XSS and SQL injection protection
- Email validation

**Reliability & Resilience:**
- Retry logic with exponential backoff
- Circuit breaker pattern for external services
- Graceful error handling

**Performance Optimization:**
- Caching with TTL
- Batch processing for efficiency
- Response time optimization

**Observability & Monitoring:**
- Health checks
- System metrics collection
- Performance statistics

## How to Use Your Tools

1. **validate_input_tool**: Validate user inputs with security checks
2. **retry_with_backoff_tool**: Execute operations with retry logic
3. **circuit_breaker_call_tool**: Call external services safely
4. **cache_operation_tool**: Cache data for performance
5. **batch_process_tool**: Process multiple items efficiently
6. **health_check_tool**: Check system health status
7. **get_metrics_tool**: Get performance metrics

## Guidelines

- Always validate inputs before processing
- Handle errors gracefully with helpful messages
- Use caching when appropriate for performance
- Monitor system health and report issues
- Demonstrate production patterns in your responses
- Explain the best practices you're applying

## Example Interactions

User: "Validate this email: user@example.com"
→ Use validate_input_tool to demonstrate security validation

User: "Process order with retry logic"
→ Use retry_with_backoff_tool to show resilience patterns

User: "Call external service"
→ Use circuit_breaker_call_tool to demonstrate failure protection

User: "Show system health"
→ Use health_check_tool to display monitoring capabilities
""".strip(),
    tools=[
        validate_input_tool,
        retry_with_backoff_tool,
        circuit_breaker_call_tool,
        cache_operation_tool,
        batch_process_tool,
        health_check_tool,
        get_metrics_tool,
    ]
)


def main():
    """Main entry point for running the agent."""
    print("🚀 Best Practices Agent - Production-Ready Patterns")
    print("=" * 60)
    print("\nThis agent demonstrates:")
    print("  ✅ Input validation & security")
    print("  ✅ Error handling & retry logic")
    print("  ✅ Circuit breaker pattern")
    print("  ✅ Performance optimization")
    print("  ✅ Monitoring & observability")
    print("\n" + "=" * 60)
    print("\nRun 'adk web' to interact with the agent")
    print("Or use 'make dev' for development mode\n")


if __name__ == "__main__":
    main()
