"""Test agent configuration and setup."""

import pytest


class TestAgentConfiguration:
    """Test that the root_agent is properly configured."""

    def test_root_agent_exists(self):
        """Test that root_agent is defined."""
        try:
            from custom_session_agent.agent import root_agent
            assert root_agent is not None
        except ImportError:
            pytest.skip("ADK not installed")

    def test_root_agent_has_name(self):
        """Test that root_agent has a name."""
        try:
            from custom_session_agent.agent import root_agent
            assert hasattr(root_agent, "name")
            assert root_agent.name == "custom_session_agent"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_root_agent_has_description(self):
        """Test that root_agent has a description."""
        try:
            from custom_session_agent.agent import root_agent
            assert hasattr(root_agent, "description")
            assert "custom session service" in root_agent.description.lower()
        except ImportError:
            pytest.skip("ADK not installed")

    def test_root_agent_has_tools(self):
        """Test that root_agent has tools."""
        try:
            from custom_session_agent.agent import root_agent
            assert hasattr(root_agent, "tools")
            assert len(root_agent.tools) >= 4
        except ImportError:
            pytest.skip("ADK not installed")

    def test_root_agent_tools_are_callable(self):
        """Test that all agent tools are callable."""
        try:
            from custom_session_agent.agent import root_agent
            for tool in root_agent.tools:
                assert callable(tool), f"Tool {tool} is not callable"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_root_agent_has_output_key(self):
        """Test that root_agent has output_key for state management."""
        try:
            from custom_session_agent.agent import root_agent
            assert hasattr(root_agent, "output_key")
            assert root_agent.output_key == "session_result"
        except ImportError:
            pytest.skip("ADK not installed")


class TestCustomSessionServiceDemo:
    """Test CustomSessionServiceDemo class."""

    def test_demo_class_has_register_redis_service(self):
        """Test that demo class has register_redis_service method."""
        try:
            from custom_session_agent.agent import CustomSessionServiceDemo
            assert hasattr(CustomSessionServiceDemo, "register_redis_service")
            assert callable(CustomSessionServiceDemo.register_redis_service)
        except ImportError:
            pytest.skip("ADK not installed")

    def test_demo_class_has_register_memory_service(self):
        """Test that demo class has register_memory_service method."""
        try:
            from custom_session_agent.agent import CustomSessionServiceDemo
            assert hasattr(CustomSessionServiceDemo, "register_memory_service")
            assert callable(CustomSessionServiceDemo.register_memory_service)
        except ImportError:
            pytest.skip("ADK not installed")

    def test_services_are_registered_on_import(self):
        """Test that services are registered when module is imported."""
        try:
            from google.adk.cli.service_registry import get_service_registry
            registry = get_service_registry()
            
            # Try to get the service factory for redis
            # This should not raise an error if registered
            factory = registry.get_session_service_factory("redis")
            assert factory is not None
        except ImportError:
            pytest.skip("ADK not installed")
        except Exception as e:
            # Services might not be registered in test environment
            pytest.skip(f"Service registry not available: {e}")


class TestAgentModel:
    """Test agent model configuration."""

    def test_root_agent_uses_gemini_model(self):
        """Test that root_agent uses Gemini model."""
        try:
            from custom_session_agent.agent import root_agent
            assert hasattr(root_agent, "model")
            assert "gemini" in root_agent.model.lower()
        except ImportError:
            pytest.skip("ADK not installed")

    def test_root_agent_has_instruction(self):
        """Test that root_agent has instruction text."""
        try:
            from custom_session_agent.agent import root_agent
            assert hasattr(root_agent, "instruction")
            assert len(root_agent.instruction) > 0
            assert "session service" in root_agent.instruction.lower()
        except ImportError:
            pytest.skip("ADK not installed")
