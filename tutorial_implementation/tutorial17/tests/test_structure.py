"""
Test Project Structure

Tests for the project structure and required files.
"""

import os


class TestProjectStructure:
    """Test that the project has the required structure and files."""

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        assert os.path.exists("pyproject.toml"), "pyproject.toml not found"

    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.exists("requirements.txt"), "requirements.txt not found"

    def test_agent_directory_exists(self):
        """Test that the agent directory exists."""
        assert os.path.exists(
            "a2a_orchestrator"
        ), "a2a_orchestrator directory not found"

    def test_agent_init_exists(self):
        """Test that __init__.py exists in agent directory."""
        init_file = os.path.join("a2a_orchestrator", "__init__.py")
        assert os.path.exists(init_file), "__init__.py not found in a2a_orchestrator"

    def test_agent_py_exists(self):
        """Test that agent.py exists."""
        agent_file = os.path.join("a2a_orchestrator", "agent.py")
        assert os.path.exists(agent_file), "agent.py not found"

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        env_file = os.path.join("a2a_orchestrator", ".env.example")
        assert os.path.exists(env_file), ".env.example not found"

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        assert os.path.exists("tests"), "tests directory not found"

    def test_test_files_exist(self):
        """Test that test files exist."""
        test_files = ["test_agent.py", "test_imports.py", "test_structure.py"]
        for test_file in test_files:
            test_path = os.path.join("tests", test_file)
            assert os.path.exists(test_path), f"{test_file} not found"

    def test_init_imports_root_agent(self):
        """Test that __init__.py properly imports root_agent."""
        init_file = os.path.join("a2a_orchestrator", "__init__.py")
        with open(init_file, "r") as f:
            content = f.read()

        assert (
            "from .agent import root_agent" in content
        ), "__init__.py doesn't import root_agent"
        assert (
            "__all__ = ['root_agent']" in content
        ), "__init__.py doesn't export root_agent"

    def test_pyproject_has_correct_name(self):
        """Test that pyproject.toml has the correct project name."""
        with open("pyproject.toml", "r") as f:
            content = f.read()

        assert (
            'name = "tutorial17"' in content
        ), "pyproject.toml doesn't have correct name"

    def test_requirements_has_adk(self):
        """Test that requirements.txt includes google-adk."""
        with open("requirements.txt", "r") as f:
            content = f.read()

        assert "google-adk" in content, "requirements.txt doesn't include google-adk"

    def test_env_example_has_required_vars(self):
        """Test that .env.example has required environment variables."""
        env_file = os.path.join("a2a_orchestrator", ".env.example")
        with open(env_file, "r") as f:
            content = f.read()

        required_vars = [
            "GOOGLE_GENAI_USE_VERTEXAI",
            "GOOGLE_API_KEY",
            "RESEARCH_AGENT_TOKEN",
            "ANALYSIS_AGENT_TOKEN",
            "CONTENT_AGENT_TOKEN",
        ]

        for var in required_vars:
            assert var in content, f".env.example missing {var}"
