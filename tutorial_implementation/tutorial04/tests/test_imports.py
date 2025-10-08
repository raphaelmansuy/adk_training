"""
Test imports for Tutorial 04: Sequential Workflows
"""

from blog_pipeline.agent import root_agent
from google.adk.agents import Agent, SequentialAgent


class TestImports:
    """Test import functionality"""

    def test_google_adk_agents_import(self):
        """Test google.adk.agents import works"""
        assert Agent is not None
        assert SequentialAgent is not None

    def test_blog_pipeline_agent_import(self):
        """Test blog_pipeline.agent import works"""
        assert root_agent is not None

    def test_root_agent_exists(self):
        """Test root_agent is properly defined"""
        assert root_agent is not None
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'sub_agents')

    def test_future_annotations_import(self):
        """Test __future__ annotations import works"""
        import __future__
        assert hasattr(__future__, 'annotations')