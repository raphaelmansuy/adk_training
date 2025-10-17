"""Test project structure and required files."""

import os
from pathlib import Path


def test_project_structure():
    """Test that all required files and directories exist."""
    project_root = Path(__file__).parent.parent
    
    # Required files
    required_files = [
        "production_agent/__init__.py",
        "production_agent/agent.py",
        "production_agent/server.py",
        "requirements.txt",
        "pyproject.toml",
        "Makefile",
        "README.md",
        ".env.example",
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        assert full_path.exists(), f"Required file missing: {file_path}"


def test_required_directories():
    """Test that required directories exist."""
    project_root = Path(__file__).parent.parent
    
    required_dirs = [
        "production_agent",
        "tests",
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        assert full_path.is_dir(), f"Required directory missing: {dir_path}"


def test_env_example_format():
    """Test that .env.example has proper format."""
    project_root = Path(__file__).parent.parent
    env_example = project_root / ".env.example"
    
    content = env_example.read_text()
    
    # Check for important environment variables
    required_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
        "GOOGLE_GENAI_USE_VERTEXAI",
        "GOOGLE_API_KEY",
        "MODEL",
    ]
    
    for var in required_vars:
        assert var in content, f"Environment variable missing in .env.example: {var}"


def test_requirements_file():
    """Test that requirements.txt contains necessary packages."""
    project_root = Path(__file__).parent.parent
    requirements = project_root / "requirements.txt"
    
    content = requirements.read_text()
    
    # Check for critical packages
    required_packages = [
        "google-genai",
        "fastapi",
        "uvicorn",
        "pytest",
    ]
    
    for package in required_packages:
        assert package in content, f"Package missing in requirements.txt: {package}"


def test_pyproject_toml():
    """Test that pyproject.toml is properly configured."""
    project_root = Path(__file__).parent.parent
    pyproject = project_root / "pyproject.toml"
    
    content = pyproject.read_text()
    
    # Check for important sections
    assert "[project]" in content
    assert 'name = "production_agent"' in content
    assert "google-genai" in content


def test_makefile_targets():
    """Test that Makefile has required targets."""
    project_root = Path(__file__).parent.parent
    makefile = project_root / "Makefile"
    
    content = makefile.read_text()
    
    # Check for required targets
    required_targets = [
        "setup:",
        "dev:",
        "test:",
        "demo:",
        "clean:",
    ]
    
    for target in required_targets:
        assert target in content, f"Makefile target missing: {target}"
