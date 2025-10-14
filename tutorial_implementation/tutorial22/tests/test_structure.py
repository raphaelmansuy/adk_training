# Tutorial 22: Model Selection & Optimization - Structure Tests
# Validates that the project structure follows ADK conventions

import os


class TestProjectStructure:
    """Test that the project follows required ADK structure."""

    def test_model_selector_directory_exists(self):
        """Test that model_selector directory exists."""
        assert os.path.isdir('model_selector'), "model_selector directory not found"

    def test_init_py_exists(self):
        """Test that __init__.py exists in model_selector."""
        init_file = os.path.join('model_selector', '__init__.py')
        assert os.path.isfile(init_file), "__init__.py not found in model_selector"

    def test_agent_py_exists(self):
        """Test that agent.py exists in model_selector."""
        agent_file = os.path.join('model_selector', 'agent.py')
        assert os.path.isfile(agent_file), "agent.py not found in model_selector"

    def test_env_example_exists(self):
        """Test that .env.example exists in model_selector."""
        env_file = os.path.join('model_selector', '.env.example')
        assert os.path.isfile(env_file), ".env.example not found in model_selector"

    def test_init_py_content(self):
        """Test that __init__.py has correct content."""
        init_file = os.path.join('model_selector', '__init__.py')
        with open(init_file, 'r') as f:
            content = f.read().strip()

        assert content == "from . import agent", f"__init__.py content incorrect: {content}"

    def test_agent_py_is_python_file(self):
        """Test that agent.py is a valid Python file."""
        agent_file = os.path.join('model_selector', 'agent.py')

        # Should be readable
        with open(agent_file, 'r') as f:
            content = f.read()

        assert len(content) > 0, "agent.py is empty"

        # Should contain Python code
        assert "from google.adk.agents import Agent" in content
        assert "root_agent = Agent(" in content
        assert "ModelSelector" in content

    def test_env_example_content(self):
        """Test that .env.example has required configuration."""
        env_file = os.path.join('model_selector', '.env.example')
        with open(env_file, 'r') as f:
            content = f.read()

        # Should contain required environment variables
        assert "GOOGLE_API_KEY=" in content


class TestTestStructure:
    """Test that the test directory structure is correct."""

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        assert os.path.isdir('tests'), "tests directory not found"

    def test_tests_init_py_exists(self):
        """Test that tests/__init__.py exists."""
        init_file = os.path.join('tests', '__init__.py')
        assert os.path.isfile(init_file), "tests/__init__.py not found"

    def test_test_files_exist(self):
        """Test that all test files exist."""
        test_files = [
            'test_agent.py',
            'test_imports.py',
            'test_structure.py'
        ]

        for test_file in test_files:
            file_path = os.path.join('tests', test_file)
            assert os.path.isfile(file_path), f"{test_file} not found in tests/"


class TestRootFiles:
    """Test that root-level files exist."""

    def test_readme_exists(self):
        """Test that README.md exists."""
        assert os.path.isfile('README.md'), "README.md not found"

    def test_makefile_exists(self):
        """Test that Makefile exists."""
        assert os.path.isfile('Makefile'), "Makefile not found"

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.isfile('requirements.txt'), "requirements.txt not found"

    def test_pyproject_exists(self):
        """Test that pyproject.toml exists."""
        assert os.path.isfile('pyproject.toml'), "pyproject.toml not found"

    def test_readme_content(self):
        """Test that README.md has basic content."""
        with open('README.md', 'r') as f:
            content = f.read()

        assert len(content) > 100, "README.md seems too short"
        assert "Tutorial 22" in content
        assert "Model Selection" in content

    def test_makefile_content(self):
        """Test that Makefile has basic targets."""
        with open('Makefile', 'r') as f:
            content = f.read()

        assert "help:" in content
        assert "setup:" in content
        assert "test:" in content
        assert "dev:" in content

    def test_requirements_content(self):
        """Test that requirements.txt has ADK."""
        with open('requirements.txt', 'r') as f:
            content = f.read()

        assert "google-adk" in content, "google-adk not found in requirements.txt"

    def test_pyproject_content(self):
        """Test that pyproject.toml has correct project name."""
        with open('pyproject.toml', 'r') as f:
            content = f.read()

        assert "tutorial22" in content, "tutorial22 not found in pyproject.toml"
        assert "Model Selection" in content
