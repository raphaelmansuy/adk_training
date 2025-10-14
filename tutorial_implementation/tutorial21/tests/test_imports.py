"""
Test imports for vision_catalog_agent
"""

import pytest


def test_import_agent_module():
    """Test importing the main agent module."""
    from vision_catalog_agent import agent
    assert agent is not None


def test_import_root_agent():
    """Test importing root_agent."""
    from vision_catalog_agent import root_agent
    assert root_agent is not None


def test_import_adk_dependencies():
    """Test importing ADK dependencies."""
    from google.adk.agents import Agent
    from google.adk.tools import FunctionTool
    from google.genai import types
    
    assert Agent is not None
    assert FunctionTool is not None
    assert types is not None


def test_import_image_utilities():
    """Test importing image processing utilities."""
    from vision_catalog_agent.agent import (
        load_image_from_file,
        optimize_image,
        create_sample_image,
        analyze_uploaded_image
    )
    
    assert load_image_from_file is not None
    assert optimize_image is not None
    assert create_sample_image is not None
    assert analyze_uploaded_image is not None


def test_import_agents():
    """Test importing agent components."""
    from vision_catalog_agent.agent import (
        vision_analyzer,
        catalog_generator,
        root_agent
    )
    
    assert vision_analyzer is not None
    assert catalog_generator is not None
    assert root_agent is not None


def test_import_tools():
    """Test importing tool functions."""
    from vision_catalog_agent.agent import (
        list_sample_images,
        generate_catalog_entry,
        generate_product_mockup,
        analyze_product_image,
        analyze_uploaded_image,
        compare_product_images
    )
    
    assert list_sample_images is not None
    assert generate_catalog_entry is not None
    assert generate_product_mockup is not None
    assert analyze_product_image is not None
    assert analyze_uploaded_image is not None
    assert compare_product_images is not None


def test_pil_available():
    """Test PIL/Pillow is available."""
    try:
        from PIL import Image
        assert Image is not None
    except ImportError:
        pytest.skip("PIL/Pillow not installed")
