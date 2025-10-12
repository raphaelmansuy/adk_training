"""Tests for project structure."""

import os
import pytest


class TestProjectStructure:
    """Test the project structure and required files."""

    def test_agent_directory_exists(self):
        """Test that agent directory exists."""
        assert os.path.isdir("agent"), "agent directory should exist"

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        assert os.path.isdir("tests"), "tests directory should exist"

    def test_nextjs_frontend_directory_exists(self):
        """Test that nextjs_frontend directory exists."""
        assert os.path.isdir("nextjs_frontend"), "nextjs_frontend directory should exist"

    def test_agent_init_exists(self):
        """Test that agent/__init__.py exists."""
        assert os.path.isfile(
            "agent/__init__.py"
        ), "agent/__init__.py should exist"

    def test_agent_py_exists(self):
        """Test that agent/agent.py exists."""
        assert os.path.isfile("agent/agent.py"), "agent/agent.py should exist"

    def test_env_example_exists(self):
        """Test that agent/.env.example exists."""
        assert os.path.isfile(
            "agent/.env.example"
        ), "agent/.env.example should exist"

    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.isfile("requirements.txt"), "requirements.txt should exist"

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        assert os.path.isfile("pyproject.toml"), "pyproject.toml should exist"

    def test_makefile_exists(self):
        """Test that Makefile exists."""
        assert os.path.isfile("Makefile"), "Makefile should exist"

    def test_readme_exists(self):
        """Test that README.md exists."""
        assert os.path.isfile("README.md"), "README.md should exist"

    def test_nextjs_package_json_exists(self):
        """Test that nextjs_frontend/package.json exists."""
        assert os.path.isfile(
            "nextjs_frontend/package.json"
        ), "nextjs_frontend/package.json should exist"

    def test_nextjs_app_directory_exists(self):
        """Test that nextjs_frontend/app directory exists."""
        assert os.path.isdir(
            "nextjs_frontend/app"
        ), "nextjs_frontend/app directory should exist"

    def test_nextjs_page_exists(self):
        """Test that nextjs_frontend/app/page.tsx exists."""
        assert os.path.isfile(
            "nextjs_frontend/app/page.tsx"
        ), "nextjs_frontend/app/page.tsx should exist"

    def test_nextjs_layout_exists(self):
        """Test that nextjs_frontend/app/layout.tsx exists."""
        assert os.path.isfile(
            "nextjs_frontend/app/layout.tsx"
        ), "nextjs_frontend/app/layout.tsx should exist"


class TestRequirementsContent:
    """Test the content of requirements.txt."""

    def test_requirements_has_google_adk(self):
        """Test that requirements.txt includes google-adk."""
        with open("requirements.txt", "r") as f:
            content = f.read()
        assert "google-adk" in content.lower(), "requirements.txt should include google-adk"

    def test_requirements_has_fastapi(self):
        """Test that requirements.txt includes fastapi."""
        with open("requirements.txt", "r") as f:
            content = f.read()
        assert "fastapi" in content.lower(), "requirements.txt should include fastapi"

    def test_requirements_has_uvicorn(self):
        """Test that requirements.txt includes uvicorn."""
        with open("requirements.txt", "r") as f:
            content = f.read()
        assert "uvicorn" in content.lower(), "requirements.txt should include uvicorn"

    def test_requirements_has_ag_ui_adk(self):
        """Test that requirements.txt includes ag-ui-adk."""
        with open("requirements.txt", "r") as f:
            content = f.read()
        assert "ag-ui-adk" in content.lower() or "ag_ui_adk" in content.lower(), \
            "requirements.txt should include ag-ui-adk"


class TestEnvExample:
    """Test the .env.example file."""

    def test_env_example_has_google_api_key(self):
        """Test that .env.example mentions GOOGLE_API_KEY."""
        with open("agent/.env.example", "r") as f:
            content = f.read()
        assert "GOOGLE_API_KEY" in content, ".env.example should mention GOOGLE_API_KEY"

    def test_env_example_no_real_key(self):
        """Test that .env.example doesn't contain real API keys."""
        with open("agent/.env.example", "r") as f:
            content = f.read()
        # Check that the value is a placeholder
        lines = [line for line in content.split("\n") if "GOOGLE_API_KEY" in line and not line.strip().startswith("#")]
        if lines:
            assert "your" in lines[0].lower() or "placeholder" in lines[0].lower() or "example" in lines[0].lower(), \
                ".env.example should not contain real API keys"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
