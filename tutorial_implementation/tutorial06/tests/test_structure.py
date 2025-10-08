"""
Test project structure for Tutorial 06: Multi-Agent Systems - Content Publishing System
"""

import os


class TestProjectStructure:
    """Test project file and directory structure"""

    def test_content_publisher_directory_exists(self):
        """Test content_publisher directory exists"""
        assert os.path.isdir("content_publisher")

    def test_init_py_exists(self):
        """Test __init__.py exists"""
        assert os.path.isfile("content_publisher/__init__.py")

    def test_agent_py_exists(self):
        """Test agent.py exists"""
        assert os.path.isfile("content_publisher/agent.py")

    def test_env_example_exists(self):
        """Test .env.example exists"""
        assert os.path.isfile("content_publisher/.env.example")

    def test_init_py_content(self):
        """Test __init__.py has correct import"""
        with open("content_publisher/__init__.py", "r") as f:
            content = f.read().strip()
            assert "from . import agent" in content

    def test_agent_py_is_python_file(self):
        """Test agent.py is a valid Python file"""
        with open("content_publisher/agent.py", "r") as f:
            content = f.read()
            assert "from __future__ import annotations" in content
            assert "root_agent = content_publishing_system" in content

    def test_env_example_content(self):
        """Test .env.example has required variables"""
        with open("content_publisher/.env.example", "r") as f:
            content = f.read()
            assert "GOOGLE_GENAI_USE_VERTEXAI=FALSE" in content
            assert "GOOGLE_API_KEY=" in content


class TestTestStructure:
    """Test test directory and file structure"""

    def test_tests_directory_exists(self):
        """Test tests directory exists"""
        assert os.path.isdir("tests")

    def test_tests_init_py_exists(self):
        """Test tests/__init__.py exists"""
        assert os.path.isfile("tests/__init__.py")

    def test_test_files_exist(self):
        """Test test files exist"""
        assert os.path.isfile("tests/test_agent.py")
        assert os.path.isfile("tests/test_imports.py")
        assert os.path.isfile("tests/test_structure.py")