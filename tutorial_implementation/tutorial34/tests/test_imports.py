# Tutorial 34: Import and Module Tests
# Validates that all imports and modules are properly structured

import pytest
import sys


class TestModuleStructure:
    """Test the module structure is correct."""

    def test_pubsub_agent_module_exists(self):
        """Test that pubsub_agent module exists."""
        import pubsub_agent
        assert pubsub_agent is not None

    def test_pubsub_agent_agent_module_exists(self):
        """Test that pubsub_agent.agent module exists."""
        import pubsub_agent.agent
        assert pubsub_agent.agent is not None

    def test_agent_module_has_root_agent(self):
        """Test that agent module exports root_agent."""
        from pubsub_agent import agent
        assert hasattr(agent, 'root_agent')

    def test_root_agent_is_exported(self):
        """Test that root_agent can be imported directly."""
        from pubsub_agent.agent import root_agent
        assert root_agent is not None


class TestImports:
    """Test all necessary imports work."""

    def test_google_adk_agents_import(self):
        """Test that google.adk.agents can be imported."""
        from google.adk.agents import Agent
        assert Agent is not None

    def test_structured_output_schemas_import(self):
        """Test that Pydantic output schemas can be imported."""
        from pubsub_agent.agent import (
            DocumentSummary,
            EntityExtraction,
            FinancialAnalysisOutput,
            TechnicalAnalysisOutput,
            SalesAnalysisOutput,
            MarketingAnalysisOutput
        )
        assert DocumentSummary is not None
        assert EntityExtraction is not None
        assert FinancialAnalysisOutput is not None
        assert TechnicalAnalysisOutput is not None
        assert SalesAnalysisOutput is not None
        assert MarketingAnalysisOutput is not None

    def test_agent_import(self):
        """Test agent can be imported."""
        from pubsub_agent.agent import root_agent
        assert root_agent is not None


class TestModuleExports:
    """Test that modules export required items."""

    def test_agent_module_exports_agent_instance(self):
        """Test agent module exports Agent instance."""
        from pubsub_agent.agent import root_agent
        from google.adk.agents import LlmAgent
        assert isinstance(root_agent, LlmAgent)

    def test_structured_schemas_are_pydantic_models(self):
        """Test that output schemas are Pydantic models."""
        from pubsub_agent.agent import (
            DocumentSummary,
            EntityExtraction,
            FinancialAnalysisOutput,
            TechnicalAnalysisOutput,
            SalesAnalysisOutput,
            MarketingAnalysisOutput
        )
        from pydantic import BaseModel

        assert issubclass(DocumentSummary, BaseModel)
        assert issubclass(EntityExtraction, BaseModel)
        assert issubclass(FinancialAnalysisOutput, BaseModel)
        assert issubclass(TechnicalAnalysisOutput, BaseModel)
        assert issubclass(SalesAnalysisOutput, BaseModel)
        assert issubclass(MarketingAnalysisOutput, BaseModel)

    def test_agent_uses_gemini_2_5_flash(self):
        """Test that agent is configured with gemini-2.5-flash model."""
        from pubsub_agent.agent import root_agent
        assert root_agent.model == "gemini-2.5-flash"

    def test_agent_has_descriptive_instruction(self):
        """Test that agent has comprehensive instruction."""
        from pubsub_agent.agent import root_agent
        assert root_agent.instruction is not None
        assert "extract" in root_agent.instruction.lower()
        assert "structured" in root_agent.instruction.lower()


class TestPackageInit:
    """Test __init__.py structure."""

    def test_package_init_exists(self):
        """Test that __init__.py exists and can be imported."""
        import pubsub_agent
        # If we got here, __init__.py was successfully imported
        assert True

    def test_agent_module_imported_in_init(self):
        """Test that agent module is imported in __init__.py."""
        import pubsub_agent
        assert hasattr(pubsub_agent, 'agent')

