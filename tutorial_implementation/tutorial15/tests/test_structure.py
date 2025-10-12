"""
Test Project Structure
Verify required files and directories exist.
"""

import os
import pytest


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_readme_exists():
    """Test README.md exists."""
    readme_path = os.path.join(PROJECT_ROOT, 'README.md')
    assert os.path.exists(readme_path), "README.md not found"


def test_requirements_exists():
    """Test requirements.txt exists."""
    requirements_path = os.path.join(PROJECT_ROOT, 'requirements.txt')
    assert os.path.exists(requirements_path), "requirements.txt not found"


def test_pyproject_exists():
    """Test pyproject.toml exists."""
    pyproject_path = os.path.join(PROJECT_ROOT, 'pyproject.toml')
    assert os.path.exists(pyproject_path), "pyproject.toml not found"


def test_makefile_exists():
    """Test Makefile exists."""
    makefile_path = os.path.join(PROJECT_ROOT, 'Makefile')
    assert os.path.exists(makefile_path), "Makefile not found"


def test_env_example_exists():
    """Test .env.example exists."""
    env_example_path = os.path.join(PROJECT_ROOT, '.env.example')
    assert os.path.exists(env_example_path), ".env.example not found"


def test_voice_assistant_package_exists():
    """Test voice_assistant package directory exists."""
    package_dir = os.path.join(PROJECT_ROOT, 'voice_assistant')
    assert os.path.isdir(package_dir), "voice_assistant package directory not found"


def test_voice_assistant_init_exists():
    """Test voice_assistant/__init__.py exists."""
    init_path = os.path.join(PROJECT_ROOT, 'voice_assistant', '__init__.py')
    assert os.path.exists(init_path), "voice_assistant/__init__.py not found"


def test_voice_assistant_agent_exists():
    """Test voice_assistant/agent.py exists."""
    agent_path = os.path.join(PROJECT_ROOT, 'voice_assistant', 'agent.py')
    assert os.path.exists(agent_path), "voice_assistant/agent.py not found"


def test_voice_assistant_basic_live_exists():
    """Test voice_assistant/basic_live.py exists."""
    basic_live_path = os.path.join(PROJECT_ROOT, 'voice_assistant', 'basic_live.py')
    assert os.path.exists(basic_live_path), "voice_assistant/basic_live.py not found"


def test_voice_assistant_demo_exists():
    """Test voice_assistant/demo.py exists."""
    demo_path = os.path.join(PROJECT_ROOT, 'voice_assistant', 'demo.py')
    assert os.path.exists(demo_path), "voice_assistant/demo.py not found"


def test_voice_assistant_interactive_exists():
    """Test voice_assistant/interactive.py exists."""
    interactive_path = os.path.join(PROJECT_ROOT, 'voice_assistant', 'interactive.py')
    assert os.path.exists(interactive_path), "voice_assistant/interactive.py not found"


def test_voice_assistant_advanced_exists():
    """Test voice_assistant/advanced.py exists."""
    advanced_path = os.path.join(PROJECT_ROOT, 'voice_assistant', 'advanced.py')
    assert os.path.exists(advanced_path), "voice_assistant/advanced.py not found"


def test_voice_assistant_multi_agent_exists():
    """Test voice_assistant/multi_agent.py exists."""
    multi_agent_path = os.path.join(PROJECT_ROOT, 'voice_assistant', 'multi_agent.py')
    assert os.path.exists(multi_agent_path), "voice_assistant/multi_agent.py not found"


def test_tests_directory_exists():
    """Test tests/ directory exists."""
    tests_dir = os.path.join(PROJECT_ROOT, 'tests')
    assert os.path.isdir(tests_dir), "tests directory not found"


def test_test_imports_exists():
    """Test tests/test_imports.py exists."""
    test_imports_path = os.path.join(PROJECT_ROOT, 'tests', 'test_imports.py')
    assert os.path.exists(test_imports_path), "tests/test_imports.py not found"


def test_test_agent_exists():
    """Test tests/test_agent.py exists."""
    test_agent_path = os.path.join(PROJECT_ROOT, 'tests', 'test_agent.py')
    assert os.path.exists(test_agent_path), "tests/test_agent.py not found"


def test_readme_has_content():
    """Test README.md has meaningful content."""
    readme_path = os.path.join(PROJECT_ROOT, 'README.md')
    with open(readme_path, 'r') as f:
        content = f.read()
    
    assert len(content) > 100, "README.md is too short"
    assert "Tutorial 15" in content, "README.md missing tutorial reference"
    assert "Live API" in content, "README.md missing Live API reference"


def test_requirements_has_dependencies():
    """Test requirements.txt has required dependencies."""
    requirements_path = os.path.join(PROJECT_ROOT, 'requirements.txt')
    with open(requirements_path, 'r') as f:
        content = f.read()
    
    assert 'google-genai' in content, "requirements.txt missing google-genai"
    assert 'pyaudio' in content, "requirements.txt missing pyaudio"
    assert 'pytest' in content, "requirements.txt missing pytest"


def test_pyproject_has_metadata():
    """Test pyproject.toml has required metadata."""
    pyproject_path = os.path.join(PROJECT_ROOT, 'pyproject.toml')
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    assert 'name = "voice_assistant"' in content, "pyproject.toml missing package name"
    assert 'google-genai' in content, "pyproject.toml missing google-genai dependency"
