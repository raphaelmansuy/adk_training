"""
Test project structure for vision_catalog_agent
"""

import os
from pathlib import Path


class TestProjectStructure:
    """Test project structure and required files."""
    
    @property
    def project_root(self):
        """Get project root directory."""
        return Path(__file__).parent.parent
    
    def test_project_root_exists(self):
        """Test project root directory exists."""
        assert self.project_root.exists()
        assert self.project_root.is_dir()
    
    def test_agent_directory_exists(self):
        """Test agent directory exists."""
        agent_dir = self.project_root / 'vision_catalog_agent'
        assert agent_dir.exists()
        assert agent_dir.is_dir()
    
    def test_tests_directory_exists(self):
        """Test tests directory exists."""
        tests_dir = self.project_root / 'tests'
        assert tests_dir.exists()
        assert tests_dir.is_dir()
    
    def test_requirements_file_exists(self):
        """Test requirements.txt exists."""
        requirements = self.project_root / 'requirements.txt'
        assert requirements.exists()
        assert requirements.is_file()
    
    def test_pyproject_file_exists(self):
        """Test pyproject.toml exists."""
        pyproject = self.project_root / 'pyproject.toml'
        assert pyproject.exists()
        assert pyproject.is_file()
    
    def test_makefile_exists(self):
        """Test Makefile exists."""
        makefile = self.project_root / 'Makefile'
        assert makefile.exists()
        assert makefile.is_file()
    
    def test_env_example_exists(self):
        """Test .env.example exists."""
        env_example = self.project_root / '.env.example'
        assert env_example.exists()
        assert env_example.is_file()
    
    def test_adkignore_exists(self):
        """Test .adkignore exists."""
        adkignore = self.project_root / '.adkignore'
        assert adkignore.exists()
        assert adkignore.is_file()
    
    def test_agent_init_exists(self):
        """Test agent __init__.py exists."""
        init_file = self.project_root / 'vision_catalog_agent' / '__init__.py'
        assert init_file.exists()
        assert init_file.is_file()
    
    def test_agent_py_exists(self):
        """Test agent.py exists."""
        agent_file = self.project_root / 'vision_catalog_agent' / 'agent.py'
        assert agent_file.exists()
        assert agent_file.is_file()


class TestRequiredDependencies:
    """Test required dependencies are listed."""
    
    @property
    def requirements_path(self):
        """Get requirements.txt path."""
        return Path(__file__).parent.parent / 'requirements.txt'
    
    def test_requirements_content(self):
        """Test requirements.txt has required packages."""
        with open(self.requirements_path) as f:
            content = f.read().lower()
        
        required = [
            'google-genai',
            'pillow',
            'pytest'
        ]
        
        for package in required:
            assert package in content, f"Missing required package: {package}"


class TestPyprojectConfiguration:
    """Test pyproject.toml configuration."""
    
    @property
    def pyproject_path(self):
        """Get pyproject.toml path."""
        return Path(__file__).parent.parent / 'pyproject.toml'
    
    def test_pyproject_content(self):
        """Test pyproject.toml has required sections."""
        with open(self.pyproject_path) as f:
            content = f.read()
        
        required_sections = [
            '[build-system]',
            '[project]',
            '[tool.pytest.ini_options]'
        ]
        
        for section in required_sections:
            assert section in content, f"Missing section: {section}"
    
    def test_project_name(self):
        """Test project name is set correctly."""
        with open(self.pyproject_path) as f:
            content = f.read()
        
        assert 'name = "vision_catalog_agent"' in content


class TestMakefileTargets:
    """Test Makefile has required targets."""
    
    @property
    def makefile_path(self):
        """Get Makefile path."""
        return Path(__file__).parent.parent / 'Makefile'
    
    def test_makefile_targets(self):
        """Test Makefile has standard targets."""
        with open(self.makefile_path) as f:
            content = f.read()
        
        required_targets = [
            'setup:',
            'dev:',
            'test:',
            'demo:',
            'clean:'
        ]
        
        for target in required_targets:
            assert target in content, f"Missing Makefile target: {target}"


class TestSampleImagesDirectory:
    """Test sample images directory structure."""
    
    @property
    def sample_dir(self):
        """Get _sample_images directory."""
        return Path(__file__).parent.parent / '_sample_images'
    
    def test_sample_dir_exists(self):
        """Test _sample_images directory exists."""
        assert self.sample_dir.exists()
        assert self.sample_dir.is_dir()
