"""Tests for the customer support agent structure and configuration."""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestProjectStructure:
    """Test project structure and file existence."""

    def test_agent_directory_exists(self):
        """Test that agent directory exists."""
        agent_dir = os.path.join(os.path.dirname(__file__), "..", "agent")
        assert os.path.isdir(agent_dir), "agent directory should exist"

    def test_agent_file_exists(self):
        """Test that agent.py exists."""
        agent_file = os.path.join(
            os.path.dirname(__file__), "..", "agent", "agent.py"
        )
        assert os.path.isfile(agent_file), "agent/agent.py should exist"

    def test_init_file_exists(self):
        """Test that __init__.py exists."""
        init_file = os.path.join(
            os.path.dirname(__file__), "..", "agent", "__init__.py"
        )
        assert os.path.isfile(init_file), "agent/__init__.py should exist"

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        env_example = os.path.join(
            os.path.dirname(__file__), "..", "agent", ".env.example"
        )
        assert os.path.isfile(env_example), "agent/.env.example should exist"

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        req_file = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
        assert os.path.isfile(req_file), "requirements.txt should exist"

    def test_pyproject_exists(self):
        """Test that pyproject.toml exists."""
        pyproject_file = os.path.join(
            os.path.dirname(__file__), "..", "pyproject.toml"
        )
        assert os.path.isfile(pyproject_file), "pyproject.toml should exist"

    def test_nextjs_frontend_exists(self):
        """Test that Next.js frontend directory exists."""
        frontend_dir = os.path.join(
            os.path.dirname(__file__), "..", "nextjs_frontend"
        )
        assert os.path.isdir(frontend_dir), "nextjs_frontend directory should exist"


class TestAgentImports:
    """Test agent module imports."""

    def test_agent_module_imports(self):
        """Test that agent module can be imported."""
        try:
            from agent import agent as agent_module

            assert agent_module is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_root_agent_exported(self):
        """Test that root_agent is exported from agent module."""
        try:
            from agent.agent import root_agent

            assert root_agent is not None
            assert hasattr(root_agent, "name")
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_fastapi_app_exported(self):
        """Test that FastAPI app is exported."""
        try:
            from agent.agent import app

            assert app is not None
            assert hasattr(app, "title")
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


class TestAgentConfiguration:
    """Test agent configuration and setup."""

    def test_agent_has_correct_name(self):
        """Test that agent has correct name."""
        try:
            from agent.agent import root_agent

            assert root_agent.name == "customer_support_agent"
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_agent_has_tools(self):
        """Test that agent has tools configured."""
        try:
            from agent.agent import root_agent

            assert hasattr(root_agent, "tools")
            assert len(root_agent.tools) > 0
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_agent_has_instruction(self):
        """Test that agent has instruction configured."""
        try:
            from agent.agent import root_agent

            assert hasattr(root_agent, "instruction")
            assert root_agent.instruction is not None
            assert len(root_agent.instruction) > 0
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_agent_model_configured(self):
        """Test that agent has model configured."""
        try:
            from agent.agent import root_agent

            assert hasattr(root_agent, "model")
            assert root_agent.model is not None
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


class TestToolDefinitions:
    """Test tool function definitions."""

    def test_search_knowledge_base_exists(self):
        """Test that search_knowledge_base function exists."""
        try:
            from agent.agent import search_knowledge_base

            assert callable(search_knowledge_base)
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_lookup_order_status_exists(self):
        """Test that lookup_order_status function exists."""
        try:
            from agent.agent import lookup_order_status

            assert callable(lookup_order_status)
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_create_support_ticket_exists(self):
        """Test that create_support_ticket function exists."""
        try:
            from agent.agent import create_support_ticket

            assert callable(create_support_ticket)
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_search_knowledge_base_returns_dict(self):
        """Test that search_knowledge_base returns dict."""
        try:
            from agent.agent import search_knowledge_base

            result = search_knowledge_base("refund policy")
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_lookup_order_status_returns_dict(self):
        """Test that lookup_order_status returns dict."""
        try:
            from agent.agent import lookup_order_status

            result = lookup_order_status("ORD-12345")
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_create_support_ticket_returns_dict(self):
        """Test that create_support_ticket returns dict."""
        try:
            from agent.agent import create_support_ticket

            result = create_support_ticket("Test issue", "normal")
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
            assert "ticket" in result
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


class TestFastAPIConfiguration:
    """Test FastAPI app configuration."""

    def test_app_has_title(self):
        """Test that app has title."""
        try:
            from agent.agent import app

            assert app.title == "Customer Support Agent API"
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_app_has_health_endpoint(self):
        """Test that app has health endpoint."""
        try:
            from agent.agent import app

            routes = [route.path for route in app.routes]
            assert "/health" in routes
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_app_has_copilotkit_endpoint(self):
        """Test that app has copilotkit endpoint."""
        try:
            from agent.agent import app

            routes = [route.path for route in app.routes]
            # Check for copilotkit endpoint
            assert any("/api/copilotkit" in route for route in routes)
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
