"""
Tests for project structure validation
"""

import os


class TestProjectStructure:
    """Test that project structure is correct"""

    def test_chuck_norris_agent_directory_exists(self):
        """Test chuck_norris_agent directory exists"""
        assert os.path.isdir("chuck_norris_agent")

    def test_init_py_exists(self):
        """Test __init__.py exists in chuck_norris_agent"""
        assert os.path.isfile("chuck_norris_agent/__init__.py")

    def test_agent_py_exists(self):
        """Test agent.py exists in chuck_norris_agent"""
        assert os.path.isfile("chuck_norris_agent/agent.py")

    def test_env_example_exists(self):
        """Test .env.example exists in chuck_norris_agent"""
        assert os.path.isfile("chuck_norris_agent/.env.example")

    def test_init_py_content(self):
        """Test __init__.py has correct content"""
        with open("chuck_norris_agent/__init__.py", "r") as f:
            content = f.read().strip()
        assert "from .agent import root_agent" in content
        assert "__all__ = ['root_agent']" in content

    def test_agent_py_is_python_file(self):
        """Test agent.py is a valid Python file"""
        with open("chuck_norris_agent/agent.py", "r") as f:
            content = f.read()
        assert "from __future__ import annotations" in content
        assert "from google.adk.agents import Agent" in content
        assert "root_agent = Agent(" in content

    def test_env_example_content(self):
        """Test .env.example has required variables"""
        with open("chuck_norris_agent/.env.example", "r") as f:
            content = f.read()
        assert "GOOGLE_GENAI_USE_VERTEXAI=FALSE" in content
        assert "GOOGLE_API_KEY=" in content


class TestTestStructure:
    """Test that test structure is correct"""

    def test_tests_directory_exists(self):
        """Test tests directory exists"""
        assert os.path.isdir("tests")

    def test_tests_init_py_exists(self):
        """Test tests/__init__.py exists"""
        assert os.path.isfile("tests/__init__.py")

    def test_test_files_exist(self):
        """Test all required test files exist"""
        required_files = [
            "tests/test_agent.py",
            "tests/test_imports.py",
            "tests/test_structure.py"
        ]
        for file_path in required_files:
            assert os.path.isfile(file_path), f"Missing test file: {file_path}"


class TestRootFiles:
    """Test root-level files exist and have correct content"""

    def test_readme_exists(self):
        """Test README.md exists"""
        assert os.path.isfile("README.md")

    def test_makefile_exists(self):
        """Test Makefile exists"""
        assert os.path.isfile("Makefile")

    def test_requirements_exists(self):
        """Test requirements.txt exists"""
        assert os.path.isfile("requirements.txt")

    def test_readme_content(self):
        """Test README.md has basic content"""
        with open("README.md", "r") as f:
            content = f.read()
        assert "Chuck Norris" in content
        assert "OpenAPI" in content

    def test_makefile_content(self):
        """Test Makefile has basic targets"""
        with open("Makefile", "r") as f:
            content = f.read()
        assert "setup:" in content
        assert "dev:" in content
        assert "test:" in content

    def test_requirements_content(self):
        """Test requirements.txt has google-adk"""
        with open("requirements.txt", "r") as f:
            content = f.read()
        assert "google-adk" in content