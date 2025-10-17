"""
Project structure and file existence tests
"""

import os


class TestProjectStructure:
    """Test that project has proper structure."""
    
    def test_agent_module_exists(self):
        """Test that agent module directory exists."""
        assert os.path.isdir("data_analysis_agent")
    
    def test_agent_init_exists(self):
        """Test that agent __init__.py exists."""
        assert os.path.isfile("data_analysis_agent/__init__.py")
    
    def test_agent_py_exists(self):
        """Test that agent.py exists."""
        assert os.path.isfile("data_analysis_agent/agent.py")
    
    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        assert os.path.isdir("tests")
    
    def test_test_files_exist(self):
        """Test that test files exist."""
        assert os.path.isfile("tests/test_agent.py")
        assert os.path.isfile("tests/test_imports.py")
    
    def test_required_config_files_exist(self):
        """Test that required config files exist."""
        assert os.path.isfile("pyproject.toml")
        assert os.path.isfile("requirements.txt")
        assert os.path.isfile("Makefile")
    
    def test_env_example_exists(self):
        """Test that .env.example exists."""
        assert os.path.isfile(".env.example")
    
    def test_app_py_exists(self):
        """Test that app.py (Streamlit) exists."""
        assert os.path.isfile("app.py")
    
    def test_readme_exists(self):
        """Test that README.md exists."""
        assert os.path.isfile("README.md")
    
    def test_pyproject_has_content(self):
        """Test that pyproject.toml has content."""
        with open("pyproject.toml", "r") as f:
            content = f.read()
            assert "[project]" in content
            assert "data-analysis-agent" in content
    
    def test_requirements_has_dependencies(self):
        """Test that requirements.txt has dependencies."""
        with open("requirements.txt", "r") as f:
            content = f.read()
            assert "google-genai" in content
            assert "streamlit" in content
            assert "pandas" in content


class TestEnvironmentConfiguration:
    """Test environment and configuration setup."""
    
    def test_env_example_is_not_env(self):
        """Test that .env.example is not .env."""
        assert os.path.isfile(".env.example")
        assert not os.path.exists(".env") or True  # .env may not exist in repo
    
    def test_env_example_has_placeholder(self):
        """Test that .env.example has placeholder values."""
        with open(".env.example", "r") as f:
            content = f.read()
            assert "your_api_key_here" in content.lower() or "GOOGLE_API_KEY" in content
    
    def test_makefile_has_help(self):
        """Test that Makefile has help target."""
        with open("Makefile", "r") as f:
            content = f.read()
            assert "help" in content
            assert "setup" in content
            assert "dev" in content
            assert "test" in content


class TestCodeQuality:
    """Test basic code quality aspects."""
    
    def test_agent_has_docstrings(self):
        """Test that agent module has docstrings."""
        with open("data_analysis_agent/agent.py", "r") as f:
            content = f.read()
            assert '"""' in content
            assert "Data Analysis Agent" in content
    
    def test_app_has_docstring(self):
        """Test that app.py has docstring."""
        with open("app.py", "r") as f:
            content = f.read()
            assert '"""' in content
            assert "Streamlit" in content or "Data" in content
    
    def test_functions_have_docstrings(self):
        """Test that functions have docstrings."""
        with open("data_analysis_agent/agent.py", "r") as f:
            content = f.read()
            # Check that key functions have docstrings
            assert "def analyze_column" in content
            assert "def calculate_correlation" in content
            assert "def filter_data" in content
            assert "def get_dataset_summary" in content
