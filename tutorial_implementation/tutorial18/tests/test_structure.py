"""
Tests for project structure and required files.
"""

import os


def test_required_files_exist():
    """Test all required project files exist."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    required_files = [
        'pyproject.toml',
        'requirements.txt',
        'Makefile',
        'README.md',
        '.env.example',
        'observability_agent/__init__.py',
        'observability_agent/agent.py',
        'tests/test_agent.py',
        'tests/test_events.py',
        'tests/test_observability.py',
        'tests/test_imports.py',
        'tests/test_structure.py'
    ]
    
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        assert os.path.exists(full_path), f"Required file missing: {file_path}"


def test_observability_agent_is_package():
    """Test observability_agent directory is a proper Python package."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    init_file = os.path.join(base_dir, 'observability_agent', '__init__.py')
    
    assert os.path.exists(init_file)
    assert os.path.isfile(init_file)


def test_tests_directory_exists():
    """Test tests directory exists."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tests_dir = os.path.join(base_dir, 'tests')
    
    assert os.path.exists(tests_dir)
    assert os.path.isdir(tests_dir)


def test_pyproject_toml_valid():
    """Test pyproject.toml contains required fields."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pyproject_path = os.path.join(base_dir, 'pyproject.toml')
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    assert '[project]' in content
    assert 'name = "observability_agent"' in content
    assert 'google-genai' in content


def test_makefile_has_required_targets():
    """Test Makefile has required targets."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    makefile_path = os.path.join(base_dir, 'Makefile')
    
    with open(makefile_path, 'r') as f:
        content = f.read()
    
    required_targets = ['setup', 'dev', 'test', 'demo', 'clean', 'coverage']
    
    for target in required_targets:
        assert f'{target}:' in content, f"Makefile missing target: {target}"
