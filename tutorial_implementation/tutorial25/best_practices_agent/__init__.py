"""
Best Practices Agent - Production-Ready Patterns

This module demonstrates comprehensive best practices for building
production-ready agents including:
- Security (input validation, error handling)
- Performance (caching, batching)
- Reliability (retry logic, circuit breakers)
- Observability (metrics, health checks)
"""

from .agent import root_agent

__all__ = ["root_agent"]
