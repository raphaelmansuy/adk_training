# Tutorial 34: Project Structure Tests
# Validates that project has required files and structure

import os
import pytest


class TestProjectStructure:
    """Test that project has correct structure."""

    def test_pubsub_agent_directory_exists(self):
        """Test that pubsub_agent directory exists."""
        assert os.path.isdir('pubsub_agent')

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        assert os.path.isdir('tests')

    def test_pubsub_agent_init_exists(self):
        """Test that pubsub_agent/__init__.py exists."""
        assert os.path.isfile('pubsub_agent/__init__.py')

    def test_pubsub_agent_agent_module_exists(self):
        """Test that pubsub_agent/agent.py exists."""
        assert os.path.isfile('pubsub_agent/agent.py')

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        assert os.path.isfile('pubsub_agent/.env.example')

    def test_tests_init_exists(self):
        """Test that tests/__init__.py exists."""
        assert os.path.isfile('tests/__init__.py')

    def test_test_agent_module_exists(self):
        """Test that tests/test_agent.py exists."""
        assert os.path.isfile('tests/test_agent.py')

    def test_test_imports_module_exists(self):
        """Test that tests/test_imports.py exists."""
        assert os.path.isfile('tests/test_imports.py')

    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.isfile('requirements.txt')

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        assert os.path.isfile('pyproject.toml')

    def test_makefile_exists(self):
        """Test that Makefile exists."""
        assert os.path.isfile('Makefile')

    def test_readme_exists(self):
        """Test that README.md exists."""
        assert os.path.isfile('README.md')


class TestConfigurationFiles:
    """Test configuration files have required content."""

    def test_requirements_includes_adk(self):
        """Test that requirements.txt includes google-adk."""
        with open('requirements.txt', 'r') as f:
            content = f.read()
            assert 'google-adk' in content

    def test_requirements_includes_pubsub(self):
        """Test that requirements.txt includes google-cloud-pubsub."""
        with open('requirements.txt', 'r') as f:
            content = f.read()
            assert 'google-cloud-pubsub' in content

    def test_pyproject_toml_valid_name(self):
        """Test that pyproject.toml has valid package name."""
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            assert 'name = "tutorial34"' in content

    def test_pyproject_toml_has_dependencies(self):
        """Test that pyproject.toml includes dependencies."""
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            assert 'google-adk' in content

    def test_env_example_has_api_key(self):
        """Test that .env.example has API key placeholder."""
        with open('pubsub_agent/.env.example', 'r') as f:
            content = f.read()
            assert 'GOOGLE_API_KEY' in content

    def test_env_example_has_gcp_project(self):
        """Test that .env.example has GCP_PROJECT."""
        with open('pubsub_agent/.env.example', 'r') as f:
            content = f.read()
            assert 'GCP_PROJECT' in content


class TestCodeQuality:
    """Test basic code quality standards."""

    def test_agent_py_is_valid_python(self):
        """Test that agent.py is valid Python."""
        with open('pubsub_agent/agent.py', 'r') as f:
            code = f.read()
            try:
                compile(code, 'pubsub_agent/agent.py', 'exec')
            except SyntaxError as e:
                pytest.fail(f"Syntax error in agent.py: {e}")

    def test_agent_py_has_docstrings(self):
        """Test that agent.py has module docstring."""
        with open('pubsub_agent/agent.py', 'r') as f:
            code = f.read()
            assert '"""' in code or "'''" in code

    def test_test_files_are_valid_python(self):
        """Test that all test files are valid Python."""
        test_files = [
            'tests/test_agent.py',
            'tests/test_imports.py',
            'tests/test_structure.py'
        ]

        for test_file in test_files:
            if os.path.isfile(test_file):
                with open(test_file, 'r') as f:
                    code = f.read()
                    try:
                        compile(code, test_file, 'exec')
                    except SyntaxError as e:
                        pytest.fail(f"Syntax error in {test_file}: {e}")


class TestEnvExample:
    """Test .env.example file is properly formatted."""

    def test_env_example_has_comments(self):
        """Test that .env.example has descriptive comments."""
        with open('pubsub_agent/.env.example', 'r') as f:
            content = f.read()
            assert '#' in content

    def test_env_example_has_no_real_secrets(self):
        """Test that .env.example has no real API keys."""
        with open('pubsub_agent/.env.example', 'r') as f:
            content = f.read()
            # Should only have placeholder values like "your-api-key-here"
            # Real keys start with specific patterns
            assert 'your-api-key-here' in content
            assert 'your-gcp-project-id' in content

    def test_env_example_not_in_env_pattern(self):
        """Test that file is named .env.example not .env."""
        # This prevents accidental secrets in version control
        assert os.path.isfile('pubsub_agent/.env.example')
        assert not os.path.isfile('pubsub_agent/.env')


class TestDocumentation:
    """Test documentation files exist and have content."""

    def test_readme_exists_and_has_content(self):
        """Test that README.md exists and is not empty."""
        assert os.path.isfile('README.md')
        with open('README.md', 'r') as f:
            content = f.read()
            assert len(content) > 100  # Should have substantial content

    def test_readme_has_title(self):
        """Test that README has a title."""
        with open('README.md', 'r') as f:
            content = f.read()
            assert '#' in content  # Should have at least one heading
