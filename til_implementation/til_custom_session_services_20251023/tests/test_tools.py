"""Test tool functions."""

import pytest


class TestToolFunctions:
    """Test that all tool functions return correct structure."""

    def test_describe_session_info_returns_dict(self):
        """Test describe_session_info returns proper dict."""
        try:
            from custom_session_agent.agent import describe_session_info
            result = describe_session_info("test_session_123")
            
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
            assert "data" in result
            assert result["status"] == "success"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_describe_session_info_contains_session_id(self):
        """Test describe_session_info returns session ID in data."""
        try:
            from custom_session_agent.agent import describe_session_info
            result = describe_session_info("session_xyz")
            
            assert result["data"]["session_id"] == "session_xyz"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_test_session_persistence_returns_dict(self):
        """Test test_session_persistence returns proper dict."""
        try:
            from custom_session_agent.agent import test_session_persistence
            result = test_session_persistence("user_name", "John Doe")
            
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
            assert "data" in result
            assert result["status"] == "success"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_test_session_persistence_stores_key_value(self):
        """Test test_session_persistence stores key and value."""
        try:
            from custom_session_agent.agent import test_session_persistence
            result = test_session_persistence("color", "blue")
            
            assert result["data"]["key"] == "color"
            assert result["data"]["value"] == "blue"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_show_service_registry_info_returns_dict(self):
        """Test show_service_registry_info returns proper dict."""
        try:
            from custom_session_agent.agent import show_service_registry_info
            result = show_service_registry_info()
            
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
            assert "data" in result
        except ImportError:
            pytest.skip("ADK not installed")

    def test_show_service_registry_info_contains_schemes(self):
        """Test show_service_registry_info mentions example schemes."""
        try:
            from custom_session_agent.agent import show_service_registry_info
            result = show_service_registry_info()
            
            assert "example_schemes" in result["data"]
            schemes = result["data"]["example_schemes"]
            assert "redis" in schemes
            assert "mongodb" in schemes
        except ImportError:
            pytest.skip("ADK not installed")

    def test_get_session_backend_guide_returns_dict(self):
        """Test get_session_backend_guide returns proper dict."""
        try:
            from custom_session_agent.agent import get_session_backend_guide
            result = get_session_backend_guide()
            
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
            assert "data" in result
            assert result["status"] == "success"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_get_session_backend_guide_contains_backends(self):
        """Test get_session_backend_guide mentions all backends."""
        try:
            from custom_session_agent.agent import get_session_backend_guide
            result = get_session_backend_guide()
            
            data = result["data"]
            assert "redis" in data
            assert "mongodb" in data
            assert "memory" in data
            assert "custom" in data
        except ImportError:
            pytest.skip("ADK not installed")

    def test_get_session_backend_guide_redis_info(self):
        """Test get_session_backend_guide has Redis information."""
        try:
            from custom_session_agent.agent import get_session_backend_guide
            result = get_session_backend_guide()
            
            redis_info = result["data"]["redis"]
            assert "description" in redis_info
            assert "use_cases" in redis_info
            assert "pros" in redis_info
            assert "cons" in redis_info
            assert "setup" in redis_info
        except ImportError:
            pytest.skip("ADK not installed")


class TestToolReturnStructure:
    """Test that all tools follow consistent return structure."""

    def test_all_tools_have_status_key(self):
        """Test all tools return status key."""
        try:
            from custom_session_agent.agent import (
                describe_session_info,
                test_session_persistence,
                show_service_registry_info,
                get_session_backend_guide,
            )
            
            tools = [
                (describe_session_info, ["session_1"]),
                (test_session_persistence, ["key", "value"]),
                (show_service_registry_info, []),
                (get_session_backend_guide, []),
            ]
            
            for tool, args in tools:
                result = tool(*args)
                assert "status" in result, f"{tool.__name__} missing status"
        except ImportError:
            pytest.skip("ADK not installed")

    def test_all_tools_have_report_key(self):
        """Test all tools return report key."""
        try:
            from custom_session_agent.agent import (
                describe_session_info,
                test_session_persistence,
                show_service_registry_info,
                get_session_backend_guide,
            )
            
            tools = [
                (describe_session_info, ["session_1"]),
                (test_session_persistence, ["key", "value"]),
                (show_service_registry_info, []),
                (get_session_backend_guide, []),
            ]
            
            for tool, args in tools:
                result = tool(*args)
                assert "report" in result, f"{tool.__name__} missing report"
        except ImportError:
            pytest.skip("ADK not installed")
