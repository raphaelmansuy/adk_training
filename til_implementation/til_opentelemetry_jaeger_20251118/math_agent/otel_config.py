"""
OpenTelemetry initialization for ADK Math Agent.
Must be imported before any ADK modules to ensure early spans are captured.
"""

import os
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace


def initialize_otel(
    service_name: str = "google-adk-math-agent",
    service_version: str = "0.1.0",
    jaeger_endpoint: str = "http://localhost:4318/v1/traces",
) -> TracerProvider:
    """
    Initialize OpenTelemetry with OTLP exporter for Jaeger.
    
    Must be called before importing ADK modules.
    
    Args:
        service_name: Service name for traces
        service_version: Service version for traces
        jaeger_endpoint: OTLP HTTP endpoint (default: localhost Jaeger)
        
    Returns:
        Configured TracerProvider
    """
    resource = Resource(
        attributes={
            "service.name": service_name,
            "service.version": service_version,
        }
    )

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=jaeger_endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Also set environment variables for redundancy
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = jaeger_endpoint
    os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = f"service.name={service_name}"

    return provider
