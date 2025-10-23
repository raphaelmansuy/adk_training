"""Test imports and basic module structure."""

import pytest


class TestImports:
    """Test that all required modules can be imported."""

    def test_agent_module_imports(self):
        """Test that agent module can be imported."""
        try:
            import custom_session_agent.agent
            assert hasattr(custom_session_agent.agent, "root_agent")
        except ImportError:
            pytest.skip("ADK not installed")

    def test_custom_session_service_demo_exists(self):
        """Test that CustomSessionServiceDemo class exists."""
        try:
            from custom_session_agent.agent import CustomSessionServiceDemo
            assert CustomSessionServiceDemo is not None
        except ImportError:
            pytest.skip("ADK not installed")

    def test_tool_functions_exist(self):
        """Test that all tool functions are defined."""
        try:
            from custom_session_agent.agent import (
                describe_session_info,
                test_session_persistence,
                show_service_registry_info,
                get_session_backend_guide,
            )
            assert callable(describe_session_info)
            assert callable(test_session_persistence)
            assert callable(show_service_registry_info)
            assert callable(get_session_backend_guide)
        except ImportError:
            pytest.skip("ADK not installed")


class TestEnvConfig:
    """Test environment configuration."""

    def test_env_example_exists(self):
        """Test that .env.example file exists."""
        import os
        env_example_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            ".env.example"
        )
        assert os.path.exists(env_example_path), ".env.example should exist"

    def test_env_contains_required_vars(self):
        """Test that .env.example contains required variables."""
        import os
        env_example_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            ".env.example"
        )
        with open(env_example_path, "r") as f:
            content = f.read()
        
        required_vars = [
            "GOOGLE_API_KEY",
            "REDIS_HOST",
            "REDIS_PORT",
            "MONGODB_HOST",
            "SESSION_SERVICE_TYPE",
        ]
        
        for var in required_vars:
            assert var in content, f"{var} should be in .env.example"
