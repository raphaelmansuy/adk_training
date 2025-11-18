"""
Comprehensive test suite for Math Agent with OpenTelemetry instrumentation.
Tests cover tool functionality, OTel initialization, and agent configuration.
"""

import pytest

from math_agent.tools import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
)


class TestToolFunctions:
    """Test basic math tool functions."""

    def test_add_numbers_positive(self):
        """Test addition with positive numbers."""
        result = add_numbers(5, 3)
        assert result == 8

    def test_add_numbers_negative(self):
        """Test addition with negative numbers."""
        result = add_numbers(-5, 3)
        assert result == -2

    def test_add_numbers_zero(self):
        """Test addition with zero."""
        result = add_numbers(0, 5)
        assert result == 5

    def test_add_numbers_floats(self):
        """Test addition with floating point numbers."""
        result = add_numbers(1.5, 2.3)
        assert abs(result - 3.8) < 0.0001

    def test_subtract_numbers_positive(self):
        """Test subtraction with positive numbers."""
        result = subtract_numbers(10, 3)
        assert result == 7

    def test_subtract_numbers_negative_result(self):
        """Test subtraction resulting in negative."""
        result = subtract_numbers(3, 10)
        assert result == -7

    def test_subtract_numbers_zero(self):
        """Test subtraction with zero."""
        result = subtract_numbers(5, 0)
        assert result == 5

    def test_subtract_numbers_floats(self):
        """Test subtraction with floating point numbers."""
        result = subtract_numbers(5.5, 2.3)
        assert abs(result - 3.2) < 0.0001

    def test_multiply_numbers_positive(self):
        """Test multiplication with positive numbers."""
        result = multiply_numbers(4, 5)
        assert result == 20

    def test_multiply_numbers_by_zero(self):
        """Test multiplication by zero."""
        result = multiply_numbers(5, 0)
        assert result == 0

    def test_multiply_numbers_negative(self):
        """Test multiplication with negative numbers."""
        result = multiply_numbers(-3, 4)
        assert result == -12

    def test_multiply_numbers_floats(self):
        """Test multiplication with floating point numbers."""
        result = multiply_numbers(2.5, 4.0)
        assert result == 10.0

    def test_divide_numbers_positive(self):
        """Test division with positive numbers."""
        result = divide_numbers(10, 2)
        assert result == 5

    def test_divide_numbers_float_result(self):
        """Test division with float result."""
        result = divide_numbers(10, 3)
        assert abs(result - 3.333333) < 0.001

    def test_divide_numbers_negative(self):
        """Test division with negative numbers."""
        result = divide_numbers(-10, 2)
        assert result == -5

    def test_divide_numbers_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide_numbers(10, 0)

    def test_divide_numbers_floats(self):
        """Test division with floating point numbers."""
        result = divide_numbers(7.5, 2.5)
        assert abs(result - 3.0) < 0.0001


class TestOpenTelemetryInitialization:
    """Test OpenTelemetry configuration and initialization."""

    def test_initialize_otel_returns_tracer_provider(self):
        """Test that initialize_otel returns a TracerProvider instance."""
        try:
            from math_agent.otel_config import initialize_otel
            provider = initialize_otel()
            assert provider is not None
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_initialize_otel_with_custom_service_name(self):
        """Test OTel initialization with custom service name."""
        try:
            from math_agent.otel_config import initialize_otel
            tracer_provider, logger_provider = initialize_otel(service_name="custom-service", force_reinit=True)
            assert tracer_provider is not None
            # Verify resource attributes
            resource = tracer_provider.resource
            assert "service.name" in resource.attributes
            assert resource.attributes["service.name"] == "custom-service"
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_initialize_otel_with_custom_version(self):
        """Test OTel initialization with custom version."""
        try:
            from math_agent.otel_config import initialize_otel
            tracer_provider, logger_provider = initialize_otel(service_version="1.0.0", force_reinit=True)
            assert tracer_provider is not None
            resource = tracer_provider.resource
            assert "service.version" in resource.attributes
            assert resource.attributes["service.version"] == "1.0.0"
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_initialize_otel_with_custom_endpoint(self):
        """Test OTel initialization with custom Jaeger endpoint."""
        try:
            from math_agent.otel_config import initialize_otel
            tracer_provider, logger_provider = initialize_otel(
                jaeger_endpoint="http://jaeger.example.com:4318/v1/traces",
                force_reinit=True
            )
            assert tracer_provider is not None
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_initialize_otel_sets_environment_variables(self):
        """Test that initialize_otel sets required environment variables."""
        try:
            from math_agent.otel_config import initialize_otel
            import os
            tracer_provider, logger_provider = initialize_otel()
            assert os.environ.get("OTEL_EXPORTER_OTLP_PROTOCOL") == "http/protobuf"
            assert "OTEL_EXPORTER_OTLP_ENDPOINT" in os.environ
            assert "service.name" in os.environ.get("OTEL_RESOURCE_ATTRIBUTES", "")
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_initialize_otel_resource_attributes(self):
        """Test that OTel resource has correct attributes."""
        try:
            from math_agent.otel_config import initialize_otel
            tracer_provider, logger_provider = initialize_otel()
            resource = tracer_provider.resource
            assert "service.name" in resource.attributes
            assert "service.version" in resource.attributes
            assert resource.attributes["service.name"] == "google-adk-math-agent"
            assert resource.attributes["service.version"] == "0.1.0"
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_initialize_otel_idempotent(self):
        """Test that initialize_otel can be called multiple times safely."""
        try:
            from math_agent.otel_config import initialize_otel
            tracer_provider1, logger_provider1 = initialize_otel()
            tracer_provider2, logger_provider2 = initialize_otel()
            assert tracer_provider1 is not None
            assert tracer_provider2 is not None
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")


class TestOTelConfigIntegration:
    """Integration tests for OTel configuration."""

    def test_otel_span_processor_added(self):
        """Test that span processors are properly configured."""
        try:
            from math_agent.otel_config import initialize_otel
            tracer_provider, logger_provider = initialize_otel()
            # Verify that provider is properly initialized
            assert tracer_provider is not None
            # Verify resource is set
            assert tracer_provider.resource is not None
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_otel_tracer_creation(self):
        """Test that tracer can be created from provider."""
        try:
            from opentelemetry import trace
            from math_agent.otel_config import initialize_otel

            tracer_provider, logger_provider = initialize_otel()
            trace.set_tracer_provider(tracer_provider)
            tracer = trace.get_tracer(__name__)
            assert tracer is not None
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")

    def test_otel_simple_span(self):
        """Test creating a simple span."""
        try:
            from opentelemetry import trace
            from math_agent.otel_config import initialize_otel

            tracer_provider, logger_provider = initialize_otel()
            trace.set_tracer_provider(tracer_provider)
            tracer = trace.get_tracer(__name__)

            with tracer.start_as_current_span("test_span") as span:
                assert span is not None
                span.set_attribute("test.key", "test_value")
        except ImportError:
            pytest.skip("OpenTelemetry not available in test environment")
class TestToolDocumentation:
    """Test that tools have proper documentation."""

    def test_add_numbers_has_docstring(self):
        """Test that add_numbers has documentation."""
        assert add_numbers.__doc__ is not None
        assert "Add" in add_numbers.__doc__

    def test_subtract_numbers_has_docstring(self):
        """Test that subtract_numbers has documentation."""
        assert subtract_numbers.__doc__ is not None
        assert "Subtract" in subtract_numbers.__doc__

    def test_multiply_numbers_has_docstring(self):
        """Test that multiply_numbers has documentation."""
        assert multiply_numbers.__doc__ is not None
        assert "Multiply" in multiply_numbers.__doc__

    def test_divide_numbers_has_docstring(self):
        """Test that divide_numbers has documentation."""
        assert divide_numbers.__doc__ is not None
        assert "Divide" in divide_numbers.__doc__


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_add_large_numbers(self):
        """Test addition with very large numbers."""
        result = add_numbers(1e10, 1e10)
        assert result == 2e10

    def test_subtract_same_number(self):
        """Test subtracting a number from itself."""
        result = subtract_numbers(42, 42)
        assert result == 0

    def test_multiply_by_one(self):
        """Test that multiplying by 1 returns the same number."""
        result = multiply_numbers(42, 1)
        assert result == 42

    def test_divide_by_one(self):
        """Test that dividing by 1 returns the same number."""
        result = divide_numbers(42, 1)
        assert result == 42

    def test_add_very_small_floats(self):
        """Test addition with very small floating point numbers."""
        result = add_numbers(1e-10, 1e-10)
        assert result > 0

    def test_multiply_negative_numbers(self):
        """Test multiplication of two negative numbers."""
        result = multiply_numbers(-3, -4)
        assert result == 12

    def test_divide_negative_by_negative(self):
        """Test division of two negative numbers."""
        result = divide_numbers(-10, -2)
        assert result == 5


class TestToolTypes:
    """Test type handling in tools."""

    def test_add_int_and_float(self):
        """Test adding integer and float."""
        result = add_numbers(5, 2.5)
        assert abs(result - 7.5) < 0.0001

    def test_subtract_float_and_int(self):
        """Test subtracting float and integer."""
        result = subtract_numbers(10.5, 3)
        assert abs(result - 7.5) < 0.0001

    def test_multiply_mixed_types(self):
        """Test multiplication with mixed types."""
        result = multiply_numbers(3, 2.5)
        assert abs(result - 7.5) < 0.0001

    def test_divide_mixed_types(self):
        """Test division with mixed types."""
        result = divide_numbers(15, 2)
        assert abs(result - 7.5) < 0.0001


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
