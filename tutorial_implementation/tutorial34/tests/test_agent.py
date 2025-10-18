# Tutorial 34: Document Processing Agent - Agent Tests
# Validates multi-agent configuration with JSON output enforcement

import pytest
from typing import Dict, Any


class TestAgentConfiguration:
    """Test that the coordinator agent is properly configured."""

    def test_root_agent_import(self):
        """Test that root_agent can be imported."""
        from pubsub_agent.agent import root_agent
        assert root_agent is not None

    def test_agent_is_llm_agent_instance(self):
        """Test that root_agent is an LlmAgent instance."""
        from pubsub_agent.agent import root_agent
        from google.adk.agents import LlmAgent

        assert isinstance(root_agent, LlmAgent)

    def test_agent_name(self):
        """Test that agent has correct name."""
        from pubsub_agent.agent import root_agent

        assert hasattr(root_agent, 'name')
        assert root_agent.name == "pubsub_processor"

    def test_agent_model_is_gemini_25_flash(self):
        """Test that agent uses gemini-2.5-flash model."""
        from pubsub_agent.agent import root_agent

        assert hasattr(root_agent, 'model')
        assert root_agent.model == "gemini-2.5-flash"

    def test_agent_description(self):
        """Test that agent has description."""
        from pubsub_agent.agent import root_agent

        assert hasattr(root_agent, 'description')
        assert "event-driven" in root_agent.description.lower()
        assert "document processing" in root_agent.description.lower()
        assert "coordinator" in root_agent.description.lower()

    def test_agent_instruction(self):
        """Test that agent has instruction."""
        from pubsub_agent.agent import root_agent

        assert hasattr(root_agent, 'instruction')
        # Check for key routing responsibilities
        assert "financial" in root_agent.instruction.lower()
        assert "technical" in root_agent.instruction.lower()
        assert "sales" in root_agent.instruction.lower()
        assert "marketing" in root_agent.instruction.lower()

    def test_agent_has_tools(self):
        """Test that coordinator agent has sub-agent tools."""
        from pubsub_agent.agent import root_agent

        assert hasattr(root_agent, 'tools')
        assert root_agent.tools is not None
        # Should have 4 sub-agent tools (financial, technical, sales, marketing)
        assert len(root_agent.tools) == 4


class TestSubAgentConfiguration:
    """Test that each sub-agent is properly configured."""

    def test_financial_agent_import(self):
        """Test that financial_agent can be imported."""
        from pubsub_agent.agent import financial_agent
        assert financial_agent is not None

    def test_financial_agent_is_llm_agent(self):
        """Test that financial_agent is an LlmAgent instance."""
        from pubsub_agent.agent import financial_agent
        from google.adk.agents import LlmAgent

        assert isinstance(financial_agent, LlmAgent)

    def test_financial_agent_configuration(self):
        """Test financial_agent has correct configuration."""
        from pubsub_agent.agent import financial_agent

        assert financial_agent.name == "financial_analyzer"
        assert financial_agent.model == "gemini-2.5-flash"
        assert "financial" in financial_agent.description.lower()

    def test_financial_agent_output_schema(self):
        """Test financial_agent has output_schema for JSON enforcement."""
        from pubsub_agent.agent import financial_agent
        from pubsub_agent.agent import FinancialAnalysisOutput

        assert financial_agent.output_schema is not None
        assert financial_agent.output_schema == FinancialAnalysisOutput

    def test_technical_agent_import(self):
        """Test that technical_agent can be imported."""
        from pubsub_agent.agent import technical_agent
        assert technical_agent is not None

    def test_technical_agent_configuration(self):
        """Test technical_agent has correct configuration."""
        from pubsub_agent.agent import technical_agent

        assert technical_agent.name == "technical_analyzer"
        assert technical_agent.model == "gemini-2.5-flash"
        assert "technical" in technical_agent.description.lower()

    def test_technical_agent_output_schema(self):
        """Test technical_agent has output_schema for JSON enforcement."""
        from pubsub_agent.agent import technical_agent
        from pubsub_agent.agent import TechnicalAnalysisOutput

        assert technical_agent.output_schema is not None
        assert technical_agent.output_schema == TechnicalAnalysisOutput

    def test_sales_agent_import(self):
        """Test that sales_agent can be imported."""
        from pubsub_agent.agent import sales_agent
        assert sales_agent is not None

    def test_sales_agent_configuration(self):
        """Test sales_agent has correct configuration."""
        from pubsub_agent.agent import sales_agent

        assert sales_agent.name == "sales_analyzer"
        assert sales_agent.model == "gemini-2.5-flash"
        assert "sales" in sales_agent.description.lower()

    def test_sales_agent_output_schema(self):
        """Test sales_agent has output_schema for JSON enforcement."""
        from pubsub_agent.agent import sales_agent
        from pubsub_agent.agent import SalesAnalysisOutput

        assert sales_agent.output_schema is not None
        assert sales_agent.output_schema == SalesAnalysisOutput

    def test_marketing_agent_import(self):
        """Test that marketing_agent can be imported."""
        from pubsub_agent.agent import marketing_agent
        assert marketing_agent is not None

    def test_marketing_agent_configuration(self):
        """Test marketing_agent has correct configuration."""
        from pubsub_agent.agent import marketing_agent

        assert marketing_agent.name == "marketing_analyzer"
        assert marketing_agent.model == "gemini-2.5-flash"
        assert "marketing" in marketing_agent.description.lower()

    def test_marketing_agent_output_schema(self):
        """Test marketing_agent has output_schema for JSON enforcement."""
        from pubsub_agent.agent import marketing_agent
        from pubsub_agent.agent import MarketingAnalysisOutput

        assert marketing_agent.output_schema is not None
        assert marketing_agent.output_schema == MarketingAnalysisOutput


class TestAgentToolsAsSubAgents:
    """Test that sub-agents are properly wrapped as tools."""

    def test_financial_tool_import(self):
        """Test that financial_tool can be imported."""
        from pubsub_agent.agent import financial_tool
        assert financial_tool is not None

    def test_financial_tool_is_agent_tool(self):
        """Test that financial_tool is an AgentTool instance."""
        from pubsub_agent.agent import financial_tool
        from google.adk.tools import AgentTool

        assert isinstance(financial_tool, AgentTool)

    def test_technical_tool_is_agent_tool(self):
        """Test that technical_tool is an AgentTool instance."""
        from pubsub_agent.agent import technical_tool
        from google.adk.tools import AgentTool

        assert isinstance(technical_tool, AgentTool)

    def test_sales_tool_is_agent_tool(self):
        """Test that sales_tool is an AgentTool instance."""
        from pubsub_agent.agent import sales_tool
        from google.adk.tools import AgentTool

        assert isinstance(sales_tool, AgentTool)

    def test_marketing_tool_is_agent_tool(self):
        """Test that marketing_tool is an AgentTool instance."""
        from pubsub_agent.agent import marketing_tool
        from google.adk.tools import AgentTool

        assert isinstance(marketing_tool, AgentTool)


class TestOutputSchemas:
    """Test that Pydantic output schemas are properly defined."""

    def test_entity_extraction_schema_imports(self):
        """Test EntityExtraction schema can be imported."""
        from pubsub_agent.agent import EntityExtraction
        assert EntityExtraction is not None

    def test_document_summary_schema_imports(self):
        """Test DocumentSummary schema can be imported."""
        from pubsub_agent.agent import DocumentSummary
        assert DocumentSummary is not None

    def test_financial_analysis_output_schema(self):
        """Test FinancialAnalysisOutput has correct fields."""
        from pubsub_agent.agent import FinancialAnalysisOutput
        from pubsub_agent.agent import DocumentSummary, EntityExtraction

        # Test that it has required fields
        assert hasattr(FinancialAnalysisOutput, 'model_fields')
        fields = FinancialAnalysisOutput.model_fields
        assert 'summary' in fields
        assert 'entities' in fields
        assert 'financial_metrics' in fields
        assert 'fiscal_periods' in fields
        assert 'recommendations' in fields

    def test_technical_analysis_output_schema(self):
        """Test TechnicalAnalysisOutput has correct fields."""
        from pubsub_agent.agent import TechnicalAnalysisOutput

        fields = TechnicalAnalysisOutput.model_fields
        assert 'summary' in fields
        assert 'entities' in fields
        assert 'technologies' in fields
        assert 'components' in fields
        assert 'recommendations' in fields

    def test_sales_analysis_output_schema(self):
        """Test SalesAnalysisOutput has correct fields."""
        from pubsub_agent.agent import SalesAnalysisOutput

        fields = SalesAnalysisOutput.model_fields
        assert 'summary' in fields
        assert 'entities' in fields
        assert 'deals' in fields
        assert 'pipeline_value' in fields
        assert 'recommendations' in fields

    def test_marketing_analysis_output_schema(self):
        """Test MarketingAnalysisOutput has correct fields."""
        from pubsub_agent.agent import MarketingAnalysisOutput

        fields = MarketingAnalysisOutput.model_fields
        assert 'summary' in fields
        assert 'entities' in fields
        assert 'campaigns' in fields
        assert 'metrics' in fields
        assert 'recommendations' in fields

    def test_entity_extraction_instantiation(self):
        """Test EntityExtraction can be instantiated."""
        from pubsub_agent.agent import EntityExtraction

        entity = EntityExtraction(
            dates=["2024-10-08"],
            currency_amounts=["$1,200.50"],
            percentages=["35%"],
            numbers=["100"]
        )

        assert entity.dates == ["2024-10-08"]
        assert entity.currency_amounts == ["$1,200.50"]
        assert entity.percentages == ["35%"]
        assert entity.numbers == ["100"]

    def test_document_summary_instantiation(self):
        """Test DocumentSummary can be instantiated."""
        from pubsub_agent.agent import DocumentSummary

        summary = DocumentSummary(
            main_points=["Point 1", "Point 2"],
            key_insight="Main insight",
            summary="Brief summary"
        )

        assert summary.main_points == ["Point 1", "Point 2"]
        assert summary.key_insight == "Main insight"
        assert summary.summary == "Brief summary"


class TestAgentFunctionality:
    """Test basic agent functionality."""

    def test_root_agent_creation(self):
        """Test root_agent can be created without error."""
        try:
            from pubsub_agent.agent import root_agent
            assert root_agent is not None
            assert hasattr(root_agent, 'name')
        except Exception as e:
            pytest.fail(f"Root agent creation failed: {e}")

    def test_all_sub_agents_created(self):
        """Test all sub-agents are created without error."""
        try:
            from pubsub_agent.agent import (
                financial_agent,
                technical_agent,
                sales_agent,
                marketing_agent
            )
            assert financial_agent is not None
            assert technical_agent is not None
            assert sales_agent is not None
            assert marketing_agent is not None
        except Exception as e:
            pytest.fail(f"Sub-agent creation failed: {e}")

    def test_all_tools_created(self):
        """Test all AgentTools are created without error."""
        try:
            from pubsub_agent.agent import (
                financial_tool,
                technical_tool,
                sales_tool,
                marketing_tool
            )
            assert financial_tool is not None
            assert technical_tool is not None
            assert sales_tool is not None
            assert marketing_tool is not None
        except Exception as e:
            pytest.fail(f"Tool creation failed: {e}")

    def test_coordinator_agent_has_all_tools(self):
        """Test coordinator agent includes all sub-agent tools."""
        from pubsub_agent.agent import root_agent

        assert len(root_agent.tools) == 4

    def test_coordinator_instructions_include_routing(self):
        """Test coordinator instructions mention routing logic."""
        from pubsub_agent.agent import root_agent

        instruction = root_agent.instruction.lower()
        assert "route" in instruction
        assert "financial" in instruction
        assert "technical" in instruction
        assert "sales" in instruction
        assert "marketing" in instruction


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests for the multi-agent architecture."""

    def test_root_agent_can_be_instantiated(self):
        """Test that root agent can be instantiated without errors."""
        try:
            from pubsub_agent.agent import root_agent
            assert root_agent is not None
        except Exception as e:
            pytest.fail(f"Agent instantiation failed: {e}")

    def test_sub_agents_have_output_schemas(self):
        """Test that all sub-agents have output schemas set for JSON enforcement."""
        from pubsub_agent.agent import (
            financial_agent,
            technical_agent,
            sales_agent,
            marketing_agent
        )

        agents = [financial_agent, technical_agent, sales_agent, marketing_agent]
        for agent in agents:
            assert agent.output_schema is not None, f"{agent.name} missing output_schema"

    def test_coordinator_routing_strategy(self):
        """Test coordinator has proper routing instructions."""
        from pubsub_agent.agent import root_agent

        instruction = root_agent.instruction
        # Should have all routing keywords
        assert "financial" in instruction.lower()
        assert "technical" in instruction.lower()
        assert "sales" in instruction.lower()
        assert "marketing" in instruction.lower()
        # Should mention decision framework
        assert "keywords" in instruction.lower() or "framework" in instruction.lower()
