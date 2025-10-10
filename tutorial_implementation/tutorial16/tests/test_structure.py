"""
Test project structure
"""

import os
import pytest


class TestProjectStructure:
    """Test that project has required structure"""

    def test_mcp_agent_directory_exists(self):
        """Test mcp_agent directory exists"""
        assert os.path.isdir('mcp_agent')

    def test_tests_directory_exists(self):
        """Test tests directory exists"""
        assert os.path.isdir('tests')

    def test_mcp_agent_init_exists(self):
        """Test mcp_agent/__init__.py exists"""
        assert os.path.isfile('mcp_agent/__init__.py')

    def test_mcp_agent_agent_exists(self):
        """Test mcp_agent/agent.py exists"""
        assert os.path.isfile('mcp_agent/agent.py')

    def test_mcp_agent_document_organizer_exists(self):
        """Test mcp_agent/document_organizer.py exists"""
        assert os.path.isfile('mcp_agent/document_organizer.py')

    def test_env_example_exists(self):
        """Test .env.example exists"""
        assert os.path.isfile('mcp_agent/.env.example')

    def test_requirements_txt_exists(self):
        """Test requirements.txt exists"""
        assert os.path.isfile('requirements.txt')

    def test_pyproject_toml_exists(self):
        """Test pyproject.toml exists"""
        assert os.path.isfile('pyproject.toml')

    def test_makefile_exists(self):
        """Test Makefile exists"""
        assert os.path.isfile('Makefile')

    def test_readme_exists(self):
        """Test README.md exists"""
        assert os.path.isfile('README.md')

    def test_test_files_exist(self):
        """Test all test files exist"""
        assert os.path.isfile('tests/__init__.py')
        assert os.path.isfile('tests/test_agent.py')
        assert os.path.isfile('tests/test_imports.py')
        assert os.path.isfile('tests/test_structure.py')


class TestFileContent:
    """Test that files have required content"""

    def test_mcp_agent_init_exports_root_agent(self):
        """Test __init__.py exports root_agent"""
        with open('mcp_agent/__init__.py', 'r') as f:
            content = f.read()
            assert 'root_agent' in content

    def test_agent_py_defines_root_agent(self):
        """Test agent.py defines root_agent"""
        with open('mcp_agent/agent.py', 'r') as f:
            content = f.read()
            assert 'root_agent' in content
            assert 'MCPToolset' in content

    def test_env_example_has_api_key(self):
        """Test .env.example has API key placeholder"""
        with open('mcp_agent/.env.example', 'r') as f:
            content = f.read()
            assert 'GOOGLE_API_KEY' in content

    def test_requirements_txt_has_google_genai(self):
        """Test requirements.txt has google-genai"""
        with open('requirements.txt', 'r') as f:
            content = f.read()
            assert 'google-genai' in content

    def test_pyproject_toml_has_package_name(self):
        """Test pyproject.toml has package name"""
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            assert 'name' in content
            assert 'mcp_agent' in content or 'mcp-agent' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
