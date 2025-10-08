"""
Test imports for Tutorial 06: Multi-Agent Systems - Content Publishing System
"""

import pytest


class TestImports:
    """Test that all required imports work"""

    def test_google_adk_agents_import(self):
        """Test google.adk.agents imports successfully"""
        try:
            from google.adk.agents import Agent, ParallelAgent, SequentialAgent
        except ImportError as e:
            pytest.fail(f"Failed to import google.adk.agents: {e}")

    def test_content_publisher_agent_import(self):
        """Test content_publisher.agent imports successfully"""
        try:
            import content_publisher.agent
        except ImportError as e:
            pytest.fail(f"Failed to import content_publisher.agent: {e}")

    def test_root_agent_exists(self):
        """Test root_agent is defined and accessible"""
        try:
            from content_publisher.agent import root_agent
            assert root_agent is not None
        except (ImportError, AttributeError) as e:
            pytest.fail(f"root_agent not accessible: {e}")

    def test_future_annotations_import(self):
        """Test __future__ annotations import works"""
        try:
            exec("from __future__ import annotations")
        except ImportError as e:
            pytest.fail(f"Failed to import __future__.annotations: {e}")