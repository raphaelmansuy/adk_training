"""
Test suite for Tutorial 26: Project structure validation.
"""

import os
import pytest


class TestProjectStructure:
    """Test that project has required files and directories."""

    def test_enterprise_agent_directory_exists(self):
        """Test that enterprise_agent directory exists."""
        assert os.path.isdir("enterprise_agent")

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        assert os.path.isdir("tests")

    def test_enterprise_agent_init_exists(self):
        """Test that enterprise_agent/__init__.py exists."""
        assert os.path.isfile("enterprise_agent/__init__.py")

    def test_enterprise_agent_agent_exists(self):
        """Test that enterprise_agent/agent.py exists."""
        assert os.path.isfile("enterprise_agent/agent.py")

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        assert os.path.isfile("enterprise_agent/.env.example")

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        assert os.path.isfile("pyproject.toml")

    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.isfile("requirements.txt")

    def test_makefile_exists(self):
        """Test that Makefile exists."""
        assert os.path.isfile("Makefile")

    def test_readme_exists(self):
        """Test that README.md exists."""
        assert os.path.isfile("README.md")


class TestTestFiles:
    """Test that all required test files exist."""

    def test_tests_init_exists(self):
        """Test that tests/__init__.py exists."""
        assert os.path.isfile("tests/__init__.py")

    def test_test_agent_exists(self):
        """Test that test_agent.py exists."""
        assert os.path.isfile("tests/test_agent.py")

    def test_test_tools_exists(self):
        """Test that test_tools.py exists."""
        assert os.path.isfile("tests/test_tools.py")

    def test_test_imports_exists(self):
        """Test that test_imports.py exists."""
        assert os.path.isfile("tests/test_imports.py")

    def test_test_structure_exists(self):
        """Test that test_structure.py exists."""
        assert os.path.isfile("tests/test_structure.py")


class TestFileContent:
    """Test that key files have expected content."""

    def test_pyproject_toml_has_name(self):
        """Test that pyproject.toml defines project name."""
        with open("pyproject.toml", "r") as f:
            content = f.read()
        assert "name" in content
        assert "tutorial26" in content.lower()

    def test_requirements_has_adk(self):
        """Test that requirements.txt includes google-adk."""
        with open("requirements.txt", "r") as f:
            content = f.read()
        assert "google-adk" in content.lower()

    def test_makefile_has_targets(self):
        """Test that Makefile has standard targets."""
        with open("Makefile", "r") as f:
            content = f.read()
        assert "setup:" in content
        assert "test:" in content
        assert "dev:" in content
        assert "clean:" in content

    def test_readme_has_tutorial_info(self):
        """Test that README.md contains tutorial information."""
        with open("README.md", "r") as f:
            content = f.read()
        assert "Tutorial 26" in content or "tutorial 26" in content.lower()

    def test_env_example_has_api_key(self):
        """Test that .env.example has API key placeholder."""
        with open("enterprise_agent/.env.example", "r") as f:
            content = f.read()
        assert "GOOGLE_API_KEY" in content
        assert "GOOGLE_GENAI_USE_VERTEXAI" in content
