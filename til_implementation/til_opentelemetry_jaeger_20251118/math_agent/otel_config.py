"""
OpenTelemetry configuration for ADK Math Agent.

This module demonstrates TWO approaches for OTel export:

1. **ADK Built-In Support (Recommended)** - Available in google-adk >= 1.17.0
   - For GCP Cloud Trace: Use `adk web --otel_to_cloud`
   - For Custom OTLP: Set OTEL_EXPORTER_OTLP_ENDPOINT environment variable

2. **Manual OTel Setup** - For detailed control or older ADK versions
   - Manually configure TracerProvider, exporters, and processors

This tutorial uses approach #2 (manual) to show all the details, but 
in production you should use approach #1 with ADK's built-in support.

References:
- ADK Official Docs: https://github.com/google/adk-python
- OpenTelemetry: https://opentelemetry.io/docs/instrumentation/python/
- Jaeger: https://www.jaegertracing.io/docs/
"""

import logging
import os
import sys
from typing import Optional

from opentelemetry import _logs, _events, trace
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._events import EventLoggerProvider


# ============================================================================
# SIMPLIFIED APPROACH: Let ADK handle OTel setup via environment variables
# ============================================================================
#
# For production use, you can SKIP this file entirely and just set env vars:
#
#   export OTEL_SERVICE_NAME=google-adk-math-agent
#   export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
#   export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
#   adk web .
#
# Then ADK (v1.17.0+) will automatically set up OTel for you!
#
# ============================================================================


def initialize_otel_env(
    service_name: str = "google-adk-math-agent",
    service_version: str = "0.1.0",
    jaeger_endpoint: str = "http://localhost:4318/v1/traces",
) -> None:
    """
    Set environment variables for ADK's built-in OpenTelemetry support.
    
    This is the RECOMMENDED approach in production.
    
    **How it works**:
    1. Sets environment variables that ADK reads automatically
    2. ADK (v1.17.0+) configures OTel exporters based on these vars
    3. All traces are automatically exported without manual setup
    
    **Usage**:
    
    ```python
    # Option A: Call this function (shown here)
    initialize_otel_env()
    from google.adk.agents import Agent
    # ... define agent ...
    
    # Option B: Set environment variables directly (even simpler)
    export OTEL_SERVICE_NAME=google-adk-math-agent
    export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
    adk web .
    ```
    
    Args:
        service_name: Service name for all telemetry
        service_version: Service version
        jaeger_endpoint: OTLP HTTP endpoint (for non-GCP backends)
    """
    # Set variables that ADK will read and use
    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)
    os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", 
                          jaeger_endpoint.rsplit("/v1", 1)[0])  # Remove /v1/traces
    os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
    
    # Enable capture of LLM prompts/responses in traces (useful for debugging)
    os.environ.setdefault("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "true")
    
    # Enable Python logging auto-instrumentation
    os.environ.setdefault("OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED", "true")
    
    # Resource attributes for better trace identification
    os.environ.setdefault("OTEL_RESOURCE_ATTRIBUTES",
                          f"service.name={service_name},service.version={service_version}")
    
    logger = logging.getLogger("otel_config")
    logger.info(f"✅ OTel environment configured for {service_name}")
    logger.info(f"   Exporter endpoint: {os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT')}")
    logger.info("   ADK will use these settings automatically (v1.17.0+)")


# ============================================================================
# MANUAL OTEL SETUP: For detailed control or older ADK versions
# ============================================================================
#
# If you need manual control over span processors, sampling, etc.,
# use this approach instead. It's more verbose but gives you full control.
#
# ============================================================================

# Global state for manual telemetry setup
_trace_provider = None
_logger_provider = None
_initialized = False


def initialize_otel(
    service_name: str = "google-adk-math-agent",
    service_version: str = "0.1.0",
    jaeger_endpoint: str = "http://localhost:4318/v1/traces",
    enable_logging: bool = True,
    enable_events: bool = True,
    log_level: int = logging.INFO,
    force_reinit: bool = False,
) -> tuple[TracerProvider, Optional[LoggerProvider]]:
    """
    **ALTERNATIVE**: Manually set up OpenTelemetry (for detailed control).
    
    ⚠️  **RECOMMENDED**: Use `initialize_otel_env()` instead!
    That approach leverages ADK's built-in support (v1.17.0+).
    
    This function is for:
    - Detailed control over span processors
    - Sampling configuration
    - Custom exporters or multiple processors
    - Older ADK versions (<1.17.0)
    
    Args:
        service_name: Service name for all telemetry
        service_version: Service version
        jaeger_endpoint: OTLP HTTP endpoint
        enable_logging: Enable OTel logging
        enable_events: Enable OTel events
        log_level: Python logging level
        force_reinit: Force re-initialization (for testing)
        
    Returns:
        Tuple of (TracerProvider, LoggerProvider or None)
    """
    global _trace_provider, _logger_provider, _initialized
    
    # Idempotent: only initialize once unless forced
    if _initialized and not force_reinit:
        return _trace_provider, _logger_provider
    
    # Set environment variables first (for framework autodiscovery)
    os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", jaeger_endpoint.rsplit("/v1", 1)[0])
    os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")
    os.environ.setdefault("OTEL_RESOURCE_ATTRIBUTES", 
                          f"service.name={service_name},service.version={service_version}")
    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)
    
    # Create resource
    resource = Resource(attributes={
        "service.name": service_name,
        "service.version": service_version,
        "telemetry.sdk.name": "opentelemetry",
        "telemetry.sdk.language": "python",
    })

    # Setup traces
    _trace_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=jaeger_endpoint)
    trace_processor = BatchSpanProcessor(trace_exporter)
    _trace_provider.add_span_processor(trace_processor)
    trace.set_tracer_provider(_trace_provider)

    # ====== LOGGING SETUP ======
    if enable_logging:
        _logger_provider = LoggerProvider(resource=resource)
        
        # Export logs to Jaeger via OTLP HTTP (Jaeger v2 supports OTLP logs)
        # Note: Logs are batched and exported asynchronously - errors during export
        # won't block the application but will be logged to stderr
        try:
            log_exporter = OTLPLogExporter(
                endpoint=jaeger_endpoint.replace("/v1/traces", "/v1/logs")
            )
            log_processor = BatchLogRecordProcessor(log_exporter)
            _logger_provider.add_log_record_processor(log_processor)
            _logs.set_logger_provider(_logger_provider)
        except Exception as e:
            # If log export fails, continue with just console logging
            logger = logging.getLogger("otel_config")
            logger.warning(f"Failed to setup OTLP log export: {e}. Continuing with console logging only.")
            _logs.set_logger_provider(_logger_provider)
        
        # Enable events for gen_ai semantic conventions
        if enable_events:
            event_logger_provider = EventLoggerProvider(_logger_provider)
            _events.set_event_logger_provider(event_logger_provider)
    
    # ====== PYTHON LOGGING SETUP (for console output) ======
    _setup_python_logging(service_name, log_level)
    
    # Mark as initialized
    _initialized = True

    return _trace_provider, _logger_provider


def get_tracer_provider() -> Optional[TracerProvider]:
    """Get the global tracer provider (or None if not initialized)."""
    return _trace_provider


def force_flush(timeout_millis: int = 30000) -> bool:
    """
    Force flush any pending spans and logs to Jaeger.
    
    ⚠️  CRITICAL for adk web: This must be called after agent invocation
    to ensure spans are sent to Jaeger before the HTTP response is returned.
    
    Args:
        timeout_millis: Maximum time to wait for flush (default 30 seconds)
        
    Returns:
        True if flush succeeded, False if timed out
    """
    global _trace_provider, _logger_provider
    
    if _trace_provider is None:
        return True
    
    # Flush traces
    success = _trace_provider.force_flush(timeout_millis)
    
    # Flush logs if available
    if _logger_provider is not None:
        success = _logger_provider.force_flush(timeout_millis) and success
    
    return success


def _setup_python_logging(service_name: str, log_level: int) -> None:
    """
    Configure Python logging to export to OpenTelemetry (and then to Jaeger).
    
    This function:
    1. Configures root logger with specified level
    2. Creates custom handler that bridges Python logging to OTel
    3. Logs appear both in console AND in Jaeger via OTLP export
    
    The logs are automatically correlated with traces via OpenTelemetry context.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Only configure if no handlers already exist
    if not root_logger.handlers:
        # Create console handler for immediate visibility
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        # Format: timestamp | service | level | logger | message
        formatter = logging.Formatter(
            fmt=(
                f"%(asctime)s | {service_name} | %(levelname)s | "
                "%(name)s | %(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # Create OTel handler that bridges to LoggerProvider
        # This sends logs to Jaeger via OTLP export
        from opentelemetry.sdk._logs import LoggingHandler
        otel_handler = LoggingHandler(level=log_level, logger_provider=_logs.get_logger_provider())
        root_logger.addHandler(otel_handler)

    # Suppress verbose OTel exporter logs (log export errors are expected in dev)
    logging.getLogger("opentelemetry.exporter.otlp.proto.http._log_exporter").setLevel(
        logging.CRITICAL
    )
    logging.getLogger("opentelemetry").setLevel(
        logging.DEBUG if log_level == logging.DEBUG else logging.WARNING
    )
