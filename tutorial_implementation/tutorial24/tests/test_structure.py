"""
Test project structure and configuration.
"""

import os
import pytest
from pathlib import Path


class TestProjectStructure:
    """Test that project structure is correct."""

    def test_project_root_exists(self):
        """Test that project root directory exists."""
        root_dir = Path(__file__).parent.parent
        assert root_dir.exists()
        assert root_dir.is_dir()

    def test_observability_agent_package_exists(self):
        """Test that observability_agent package exists."""
        root_dir = Path(__file__).parent.parent
        agent_dir = root_dir / "observability_agent"
        assert agent_dir.exists()
        assert agent_dir.is_dir()

    def test_init_files_exist(self):
        """Test that __init__.py files exist."""
        root_dir = Path(__file__).parent.parent
        assert (root_dir / "observability_agent" / "__init__.py").exists()
        assert (root_dir / "tests" / "__init__.py").exists()

    def test_agent_file_exists(self):
        """Test that agent.py exists."""
        root_dir = Path(__file__).parent.parent
        agent_file = root_dir / "observability_agent" / "agent.py"
        assert agent_file.exists()
        assert agent_file.is_file()

    def test_config_files_exist(self):
        """Test that configuration files exist."""
        root_dir = Path(__file__).parent.parent
        required_files = [
            "pyproject.toml",
            "requirements.txt",
            "Makefile",
            ".env.example"
        ]
        for filename in required_files:
            file_path = root_dir / filename
            assert file_path.exists(), f"Required file {filename} does not exist"
            assert file_path.is_file(), f"{filename} is not a file"

    def test_readme_exists(self):
        """Test that README.md exists."""
        root_dir = Path(__file__).parent.parent
        readme = root_dir / "README.md"
        assert readme.exists()
        assert readme.is_file()

    def test_env_example_not_committed(self):
        """Test that .env file is not committed (only .env.example should exist)."""
        root_dir = Path(__file__).parent.parent
        env_file = root_dir / ".env"
        env_example = root_dir / ".env.example"

        assert env_example.exists(), ".env.example should exist"
        # .env should NOT exist (only .env.example)
        assert not env_file.exists(), ".env should not be committed - use .env.example as template"

    def test_makefile_is_executable_conceptually(self):
        """Test that Makefile has correct permissions conceptually."""
        root_dir = Path(__file__).parent.parent
        makefile = root_dir / "Makefile"
        assert makefile.exists()
        # On Unix-like systems, check if it's readable
        assert os.access(makefile, os.R_OK), "Makefile should be readable"

    def test_requirements_format(self):
        """Test that requirements.txt has valid format."""
        root_dir = Path(__file__).parent.parent
        req_file = root_dir / "requirements.txt"

        with open(req_file, 'r') as f:
            content = f.read().strip()

        assert content, "requirements.txt should not be empty"

        # Check that it contains expected packages
        lines = content.split('\n')
        package_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]

        # Should have google-genai and google-adk
        package_names = [line.split('>=')[0].split('==')[0].strip() for line in package_lines]
        assert "google-genai" in package_names, "requirements.txt should include google-genai"
        assert "google-adk" in package_names, "requirements.txt should include google-adk"

    def test_pyproject_toml_format(self):
        """Test that pyproject.toml has valid format."""
        root_dir = Path(__file__).parent.parent
        toml_file = root_dir / "pyproject.toml"

        with open(toml_file, 'r') as f:
            content = f.read()

        assert "[build-system]" in content, "pyproject.toml should have build-system section"
        assert "[project]" in content, "pyproject.toml should have project section"
        assert "name = \"observability_agent\"" in content, "pyproject.toml should define observability_agent package"
        assert "google-genai" in content, "pyproject.toml should include google-genai dependency"
        assert "google-adk" in content, "pyproject.toml should include google-adk dependency"
