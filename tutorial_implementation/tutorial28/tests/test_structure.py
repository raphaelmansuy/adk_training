# Tutorial 28: Using Other LLMs - Structure Tests
# Validates project structure and configuration

import pytest
import os
from pathlib import Path


class TestProjectStructure:
    """Test that project has correct structure."""

    def test_project_root_exists(self):
        """Test that project root directory exists."""
        project_root = Path(__file__).parent.parent
        assert project_root.exists()
        assert project_root.is_dir()

    def test_agent_package_exists(self):
        """Test that agent package exists."""
        project_root = Path(__file__).parent.parent
        agent_dir = project_root / "multi_llm_agent"
        assert agent_dir.exists()
        assert agent_dir.is_dir()

    def test_agent_init_exists(self):
        """Test that agent __init__.py exists."""
        project_root = Path(__file__).parent.parent
        init_file = project_root / "multi_llm_agent" / "__init__.py"
        assert init_file.exists()
        assert init_file.is_file()

    def test_agent_file_exists(self):
        """Test that agent.py exists."""
        project_root = Path(__file__).parent.parent
        agent_file = project_root / "multi_llm_agent" / "agent.py"
        assert agent_file.exists()
        assert agent_file.is_file()

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        project_root = Path(__file__).parent.parent
        env_example = project_root / "multi_llm_agent" / ".env.example"
        assert env_example.exists()
        assert env_example.is_file()

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        project_root = Path(__file__).parent.parent
        requirements = project_root / "requirements.txt"
        assert requirements.exists()
        assert requirements.is_file()

    def test_pyproject_exists(self):
        """Test that pyproject.toml exists."""
        project_root = Path(__file__).parent.parent
        pyproject = project_root / "pyproject.toml"
        assert pyproject.exists()
        assert pyproject.is_file()

    def test_makefile_exists(self):
        """Test that Makefile exists."""
        project_root = Path(__file__).parent.parent
        makefile = project_root / "Makefile"
        assert makefile.exists()
        assert makefile.is_file()

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        project_root = Path(__file__).parent.parent
        tests_dir = project_root / "tests"
        assert tests_dir.exists()
        assert tests_dir.is_dir()

    def test_readme_exists(self):
        """Test that README.md exists."""
        project_root = Path(__file__).parent.parent
        readme = project_root / "README.md"
        assert readme.exists()
        assert readme.is_file()


class TestConfiguration:
    """Test configuration files."""

    def test_requirements_has_adk(self):
        """Test that requirements.txt includes google-adk."""
        project_root = Path(__file__).parent.parent
        requirements = project_root / "requirements.txt"
        content = requirements.read_text()
        assert "google-adk" in content

    def test_requirements_has_litellm(self):
        """Test that requirements.txt includes litellm."""
        project_root = Path(__file__).parent.parent
        requirements = project_root / "requirements.txt"
        content = requirements.read_text()
        assert "litellm" in content

    def test_requirements_has_openai(self):
        """Test that requirements.txt includes openai."""
        project_root = Path(__file__).parent.parent
        requirements = project_root / "requirements.txt"
        content = requirements.read_text()
        assert "openai" in content

    def test_requirements_has_anthropic(self):
        """Test that requirements.txt includes anthropic."""
        project_root = Path(__file__).parent.parent
        requirements = project_root / "requirements.txt"
        content = requirements.read_text()
        assert "anthropic" in content

    def test_pyproject_has_correct_name(self):
        """Test that pyproject.toml has correct package name."""
        project_root = Path(__file__).parent.parent
        pyproject = project_root / "pyproject.toml"
        content = pyproject.read_text()
        assert 'name = "tutorial28"' in content

    def test_env_example_has_all_keys(self):
        """Test that .env.example has all required key templates."""
        project_root = Path(__file__).parent.parent
        env_example = project_root / "multi_llm_agent" / ".env.example"
        content = env_example.read_text()
        
        assert "GOOGLE_API_KEY" in content
        assert "OPENAI_API_KEY" in content
        assert "ANTHROPIC_API_KEY" in content
        assert "OLLAMA_API_BASE" in content
