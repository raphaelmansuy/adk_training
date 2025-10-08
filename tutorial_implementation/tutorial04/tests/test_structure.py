"""
Test project structure for Tutorial 04: Sequential Workflows
"""

import os


class TestProjectStructure:
    """Test project structure and file organization"""

    def test_blog_pipeline_directory_exists(self):
        """Test blog_pipeline directory exists"""
        assert os.path.exists("blog_pipeline")

    def test_init_py_exists(self):
        """Test __init__.py exists"""
        assert os.path.exists("blog_pipeline/__init__.py")

    def test_agent_py_exists(self):
        """Test agent.py exists"""
        assert os.path.exists("blog_pipeline/agent.py")

    def test_env_example_exists(self):
        """Test .env.example exists"""
        assert os.path.exists("blog_pipeline/.env.example")

    def test_init_py_content(self):
        """Test __init__.py has correct content"""
        with open("blog_pipeline/__init__.py", "r") as f:
            content = f.read()
            assert "from .agent import root_agent" in content
            assert "__all__" in content

    def test_agent_py_is_python_file(self):
        """Test agent.py is a valid Python file"""
        with open("blog_pipeline/agent.py", "r") as f:
            content = f.read()
            assert "from __future__ import annotations" in content
            assert "SequentialAgent" in content

    def test_env_example_content(self):
        """Test .env.example has required variables"""
        with open("blog_pipeline/.env.example", "r") as f:
            content = f.read()
            assert "GOOGLE_GENAI_USE_VERTEXAI" in content
            assert "GOOGLE_API_KEY" in content


class TestTestStructure:
    """Test test file organization"""

    def test_tests_directory_exists(self):
        """Test tests directory exists"""
        assert os.path.exists("tests")

    def test_tests_init_py_exists(self):
        """Test tests/__init__.py exists"""
        assert os.path.exists("tests/__init__.py")

    def test_test_files_exist(self):
        """Test test files exist"""
        test_files = [f for f in os.listdir("tests") if f.startswith("test_")]
        assert len(test_files) > 0