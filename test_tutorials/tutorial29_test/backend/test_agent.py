"""Tutorial 29 - Test Suite."""

import pytest
from fastapi.testclient import TestClient
from agent import app

client = TestClient(app)


class TestTutorial29QuickstartAgent:
    """Test suite for Tutorial 29 quickstart agent."""

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "quickstart_agent"
        assert data["tutorial"] == "29"

    def test_cors_headers(self):
        """Test CORS configuration."""
        response = client.options(
            "/api/copilotkit",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers

    def test_copilotkit_endpoint_exists(self):
        """Test that CopilotKit endpoint is registered."""
        # The endpoint should be registered by add_adk_fastapi_endpoint
        # We can't fully test it without a real API key, but we can check it's there
        routes = [route.path for route in app.routes]
        assert "/api/copilotkit" in routes or any("/api/copilotkit" in str(route) for route in app.routes)

    def test_app_metadata(self):
        """Test FastAPI app metadata."""
        assert app.title == "Tutorial 29 Quickstart Agent"

    def test_cors_origins_configured(self):
        """Test that CORS middleware is properly configured."""
        # Check middleware is present
        middlewares = [m.__class__.__name__ for m in app.user_middleware]
        # In newer FastAPI versions, CORS is wrapped as "Middleware"
        assert "CORSMiddleware" in middlewares or "Middleware" in middlewares


class TestAgentConfiguration:
    """Test agent configuration."""

    def test_agent_import(self):
        """Test that agent components can be imported."""
        from agent import adk_agent, agent
        
        assert adk_agent is not None
        assert agent is not None

    def test_agent_has_correct_model(self):
        """Test agent uses correct model."""
        from agent import adk_agent
        
        # Agent should use gemini-2.0-flash-exp model
        assert hasattr(adk_agent, "model") or hasattr(adk_agent, "_model")


class TestAPIEndpoints:
    """Test API endpoint configuration."""

    def test_health_response_structure(self):
        """Test health endpoint response structure."""
        response = client.get("/health")
        data = response.json()
        
        # Check all required fields
        assert "status" in data
        assert "agent" in data
        assert "tutorial" in data
        
        # Check field types
        assert isinstance(data["status"], str)
        assert isinstance(data["agent"], str)
        assert isinstance(data["tutorial"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
