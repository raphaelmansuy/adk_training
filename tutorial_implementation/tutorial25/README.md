# Tutorial 25: Best Practices - Production-Ready Agent Development

This implementation demonstrates comprehensive best practices for building production-ready agents with the Google Agent Development Kit (ADK), including security, performance optimization, reliability patterns, and observability.

## Overview

The **best_practices_agent** showcases enterprise-grade patterns for agent development:

- **Security Best Practices**: Input validation, XSS/SQL injection prevention, secure error handling
- **Reliability Patterns**: Retry logic with exponential backoff, circuit breaker for external services
- **Performance Optimization**: Caching with TTL, batch processing, efficient resource usage
- **Observability**: Health checks, metrics collection, system monitoring
- **Error Handling**: Comprehensive error handling with graceful degradation

## Architecture

```
Production-Ready Agent Architecture:
┌─────────────────────────────────────────────────────────┐
│                  Best Practices Agent                    │
│                  (gemini-2.0-flash-exp)                 │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┬───────────────┐
        ▼                 ▼                 ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Security   │  │ Reliability  │  │ Performance  │  │Observability │
│              │  │              │  │              │  │              │
│ • Validation │  │ • Retry      │  │ • Caching    │  │ • Metrics    │
│ • Sanitize   │  │ • Circuit    │  │ • Batching   │  │ • Health     │
│ • XSS Block  │  │   Breaker    │  │ • Optimize   │  │ • Logging    │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

## Key Components

### Security & Validation

**Input Validation Tool** (`validate_input_tool`)
- Pydantic-based validation with type checking
- Email format validation
- SQL injection pattern detection
- XSS prevention
- Text length limits
- Priority level validation

### Reliability & Resilience

**Retry with Backoff** (`retry_with_backoff_tool`)
- Automatic retry on transient failures
- Exponential backoff strategy (1s, 2s, 4s)
- Configurable max retries
- Detailed attempt tracking

**Circuit Breaker** (`circuit_breaker_call_tool`)
- Prevents cascading failures
- Automatic state management (CLOSED → OPEN → HALF_OPEN)
- Configurable failure threshold
- Timeout-based recovery

### Performance Optimization

**Caching System** (`cache_operation_tool`)
- Time-based cache with TTL
- Hit/miss tracking
- Performance statistics
- Automatic expiration

**Batch Processing** (`batch_process_tool`)
- Process multiple items efficiently
- Efficiency gain calculation
- Time savings reporting
- Resource optimization

### Observability & Monitoring

**Health Check** (`health_check_tool`)
- System health status (healthy/degraded/unhealthy)
- Circuit breaker state monitoring
- Cache statistics
- Comprehensive metrics

**Metrics Collection** (`get_metrics_tool`)
- Request counting
- Error rate tracking
- Average latency calculation
- Uptime monitoring
- Requests per second

## Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **Google AI API Key** from [AI Studio](https://aistudio.google.com/app/apikey)

### Setup

```bash
# Clone and navigate to tutorial
cd tutorial_implementation/tutorial25

# Install dependencies
make setup

# Set your API key
export GOOGLE_API_KEY=your_api_key_here

# Start the agent
make dev
```

### Demo Workflow

1. **Open** http://localhost:8000 in your browser
2. **Select** "best_practices_agent" from the dropdown
3. **Try these production scenarios**:

#### Security Validation
```
Validate this email: user@example.com
Validate this email: invalid-email
Try to validate text with SQL injection: DROP TABLE users
```

#### Reliability Patterns
```
Process order with retry logic: ORD-123
Call external service with circuit breaker
Demonstrate failure handling and recovery
```

#### Performance Optimization
```
Cache user preferences: theme=dark, language=en
Retrieve cached preferences
Show cache statistics
Batch process these orders: ORD-001, ORD-002, ORD-003
```

#### Monitoring & Observability
```
Show me the system health status
Display performance metrics
What's the current error rate?
Check circuit breaker status
```

## Example Prompts

### Input Validation Examples

**Valid Email Validation:**
```
Validate this email address: john.doe@example.com with text "Hello World" and high priority
```

Expected: ✅ Success with validated data

**Invalid Email Detection:**
```
Validate this email: not-an-email
```

Expected: ❌ Error with validation message

**XSS Prevention:**
```
Validate text containing: <script>alert('xss')</script>
```

Expected: ❌ Blocked with security warning

### Reliability Examples

**Retry Logic:**
```
Process this order with retry: ORD-12345
```

Expected: Multiple attempts with exponential backoff

**Circuit Breaker:**
```
Call the payment service
```

Expected: Protected call with circuit state reporting

### Performance Examples

**Caching:**
```
Cache this data: user_123 = premium_subscriber
Then retrieve it: get user_123
Show me cache statistics
```

Expected: Cache hit/miss tracking with performance stats

**Batch Processing:**
```
Batch process these items: Apple, Banana, Orange, Grape, Melon
```

Expected: Efficient processing with timing comparison

### Monitoring Examples

**Health Check:**
```
What's the system health status?
```

Expected: Comprehensive health report with metrics

**Performance Metrics:**
```
Show me the performance statistics
```

Expected: Request counts, latency, error rates, uptime

## Implementation Details

### Security Implementation

```python
# Pydantic validation model
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

class InputRequest(BaseModel):
    email: Optional[EmailStr] = Field(None)
    text: str = Field(..., min_length=1, max_length=10000)
    priority: str = Field("normal")

    @classmethod
    @field_validator('text')
    def validate_text(cls, v):
        dangerous = ['DROP TABLE', 'DELETE FROM', '; --', '<script>']
        # Check for dangerous patterns
```

### Circuit Breaker Pattern

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=3, timeout_seconds=30):
        self.state = CircuitState.CLOSED
        self.failures = 0
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            # Check timeout and potentially transition to HALF_OPEN
        
        try:
            result = func(*args, **kwargs)
            # Reset on success
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self.state = CircuitState.OPEN
```

### Caching Strategy

```python
class CachedDataStore:
    def __init__(self, ttl_seconds=300):
        self.cache = {}  # {key: (value, timestamp)}
        self.ttl = ttl_seconds
    
    def get(self, key):
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value  # Cache hit
            del self.cache[key]  # Expired
        return None  # Cache miss
```

### Metrics Collection

```python
class MetricsCollector:
    def record_request(self, latency, error=False):
        self.request_count += 1
        self.total_latency += latency
        if error:
            self.error_count += 1
    
    def get_metrics(self):
        return {
            'total_requests': self.request_count,
            'error_rate': self.error_count / self.request_count,
            'avg_latency_ms': self.total_latency / self.request_count
        }
```

## Testing

The implementation includes comprehensive test coverage:

### Run All Tests

```bash
# Basic test run
make test

# With coverage report
make test-cov
```

### Test Categories

**Import Tests** (`test_imports.py`)
- ✅ Agent module imports
- ✅ Tool function imports
- ✅ Class imports
- ✅ Dependency imports

**Structure Tests** (`test_structure.py`)
- ✅ Project structure validation
- ✅ Required files presence
- ✅ Configuration correctness

**Agent Tests** (`test_agent.py`)
- ✅ Agent configuration (85+ tests)
- ✅ Input validation with security checks
- ✅ Retry logic and exponential backoff
- ✅ Circuit breaker state management
- ✅ Caching operations and TTL
- ✅ Batch processing efficiency
- ✅ Health checks and metrics
- ✅ Error handling scenarios
- ✅ Integration workflows
- ✅ Performance characteristics

### Test Coverage

```bash
# Generate HTML coverage report
make test-cov

# Open coverage report
open htmlcov/index.html
```

## Production Deployment Patterns

### Pre-Deployment Checklist

- [x] Input validation implemented
- [x] Error handling comprehensive
- [x] Retry logic configured
- [x] Circuit breakers in place
- [x] Caching enabled
- [x] Monitoring configured
- [x] Health checks working
- [x] Tests passing (85+ tests)
- [x] Documentation complete

### Environment Configuration

```bash
# Development
export GOOGLE_API_KEY=your_dev_key

# Production
export GOOGLE_CLOUD_PROJECT=your-project
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### Deployment Options

**Option 1: Cloud Run (Recommended)**
```bash
adk deploy cloud_run
```

**Option 2: Vertex AI Agent Engine**
```bash
adk deploy agent_engine
```

**Option 3: GKE**
```bash
adk deploy gke
```

## Best Practices Demonstrated

### 1. Security

✅ **Input Validation**: Pydantic models with validators
✅ **Sanitization**: Remove dangerous patterns
✅ **Error Messages**: Informative but not leaking internals
✅ **Logging**: Structured logging without sensitive data

### 2. Reliability

✅ **Retry Logic**: Exponential backoff for transient failures
✅ **Circuit Breakers**: Prevent cascading failures
✅ **Graceful Degradation**: Fallback strategies
✅ **Timeout Management**: Prevent hanging requests

### 3. Performance

✅ **Caching**: Reduce redundant computations
✅ **Batch Processing**: Optimize bulk operations
✅ **Connection Pooling**: Efficient resource usage
✅ **Lazy Loading**: Load resources on demand

### 4. Observability

✅ **Metrics Collection**: Track key performance indicators
✅ **Health Checks**: Monitor system status
✅ **Structured Logging**: Consistent log format
✅ **Tracing**: Request flow visibility

### 5. Code Quality

✅ **Type Hints**: Full type annotations
✅ **Docstrings**: Comprehensive documentation
✅ **Error Handling**: Try-except with specific exceptions
✅ **Testing**: 85+ unit and integration tests

## Learning Outcomes

After working with this implementation, you'll understand:

1. **Security Patterns**
   - How to validate and sanitize inputs
   - Protection against common vulnerabilities
   - Secure error handling

2. **Reliability Patterns**
   - Implementing retry logic with exponential backoff
   - Circuit breaker pattern for external dependencies
   - Graceful degradation strategies

3. **Performance Optimization**
   - Caching strategies with TTL
   - Batch processing for efficiency
   - Resource optimization techniques

4. **Observability**
   - Metrics collection and reporting
   - Health check implementation
   - System monitoring patterns

5. **Production Readiness**
   - Comprehensive error handling
   - Testing strategies
   - Deployment best practices

## Real-World Applications

### E-commerce Platform
- Input validation for user orders
- Circuit breaker for payment gateway
- Caching for product catalog
- Metrics for order processing

### Customer Support System
- Retry logic for ticket creation
- Batch processing for bulk updates
- Health monitoring for uptime
- Performance tracking

### Data Processing Pipeline
- Validation for input data
- Circuit breaker for external APIs
- Caching for reference data
- Observability for pipeline health

### API Gateway
- Request validation
- Rate limiting with circuit breakers
- Response caching
- Comprehensive metrics

## Troubleshooting

### Common Issues

**Issue**: Validation failing on valid inputs
```bash
# Check validation logic
python -c "from best_practices_agent.agent import InputRequest; print(InputRequest(text='test', priority='normal'))"
```

**Issue**: Circuit breaker stuck in OPEN state
```bash
# Circuit breakers reset after timeout (30s default)
# Check current state with health check tool
```

**Issue**: Cache not returning values
```bash
# Check TTL settings (default 300s)
# Verify cache operations with stats tool
```

**Issue**: Tests failing
```bash
# Ensure dependencies installed
make setup

# Run tests with verbose output
pytest tests/ -v --tb=long
```

### Performance Tips

1. **Adjust Cache TTL**: Longer TTL for stable data
2. **Configure Retry Attempts**: Balance speed vs resilience
3. **Tune Circuit Breaker**: Adjust threshold based on service stability
4. **Batch Size**: Optimize batch size for your use case

## Advanced Usage

### Custom Validation Rules

```python
# Add custom validators to InputRequest
@validator('text')
def custom_validation(cls, v):
    # Your validation logic
    return v
```

### Adjusting Circuit Breaker

```python
# Create custom circuit breaker
custom_breaker = CircuitBreaker(
    failure_threshold=5,  # More lenient
    timeout_seconds=60    # Longer recovery
)
```

### Cache Configuration

```python
# Adjust cache TTL
data_cache = CachedDataStore(ttl_seconds=600)  # 10 minutes
```

## Resources

- **Tutorial Documentation**: [Tutorial 25: Best Practices](../../docs/tutorial/25_best_practices.md)
- **ADK Documentation**: https://google.github.io/adk-docs/
- **Gemini API**: https://ai.google.dev/docs
- **Production Deployment**: [Tutorial 23: Production Deployment](../../docs/tutorial/23_production_deployment.md)

## Next Steps

1. **Customize**: Adapt patterns to your specific use case
2. **Extend**: Add domain-specific tools and validations
3. **Deploy**: Use production deployment patterns from Tutorial 23
4. **Monitor**: Set up comprehensive observability
5. **Optimize**: Tune parameters based on production metrics

## Contributing

This implementation follows the established tutorial pattern:

1. **Working Code First**: Complete implementation before documentation
2. **Comprehensive Testing**: 85+ tests covering all functionality
3. **User-Friendly Setup**: Simple `make setup && make dev` workflow
4. **Clear Documentation**: Step-by-step guides and architecture explanations

## Links

- **Tutorial**: [Tutorial 25: Best Practices](../../docs/tutorial/25_best_practices.md)
- **ADK Documentation**: https://google.github.io/adk-docs/
- **Previous Tutorial**: [Tutorial 24: Advanced Observability](../tutorial24/)
- **Tutorial Series**: [Complete ADK Training](../../README.md)

---

**🎉 Congratulations!** You've completed the final tutorial in the ADK training series. You now have comprehensive knowledge of production-ready agent development patterns!

_Built with ❤️ for the ADK community_
