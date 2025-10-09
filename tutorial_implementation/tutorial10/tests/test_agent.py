"""
Comprehensive pytest test suite for support agent.

Run with: pytest tests/test_agent.py -v
"""

import pytest
from unittest.mock import Mock
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from support_agent.agent import (
    root_agent,
    search_knowledge_base,
    create_ticket,
    check_ticket_status
)


class TestToolFunctions:
    """Test tools in isolation"""

    def setup_method(self):
        """Setup before each test"""
        # Create a mock ToolContext for testing
        self.tool_context = Mock()
        self.tool_context.tickets = {}

    def test_search_knowledge_base_password_reset(self):
        """Test knowledge base search for password reset"""
        result = search_knowledge_base("password reset", self.tool_context)

        assert result["status"] == "success"
        assert "password" in result["report"].lower()
        assert len(result["results"]) > 0
        assert "reset your password" in result["results"][0]["content"]

    def test_search_knowledge_base_refund_policy(self):
        """Test knowledge base search for refund policy"""
        result = search_knowledge_base("refund", self.tool_context)

        assert result["status"] == "success"
        assert "refund" in result["report"].lower()
        assert len(result["results"]) > 0
        assert "30-day" in result["results"][0]["content"]

    def test_search_knowledge_base_shipping(self):
        """Test knowledge base search for shipping info"""
        result = search_knowledge_base("shipping", self.tool_context)

        assert result["status"] == "success"
        assert "shipping" in result["report"].lower()
        assert len(result["results"]) > 0
        assert "3-5 business days" in result["results"][0]["content"]

    def test_search_knowledge_base_not_found(self):
        """Test knowledge base search for non-existent topic"""
        result = search_knowledge_base("nonexistent topic", self.tool_context)

        assert result["status"] == "success"
        assert "no articles found" in result["report"].lower()
        assert len(result["results"]) == 0

    def test_create_ticket_normal_priority(self):
        """Test ticket creation with normal priority"""
        result = create_ticket("My account is locked", self.tool_context, "normal")

        assert result["status"] == "success"
        assert "created successfully" in result["report"]
        assert "normal" in result["report"]
        assert result["ticket"]["priority"] == "normal"
        assert result["ticket"]["status"] == "open"
        assert "ticket_id" in result["ticket"]

    def test_create_ticket_high_priority(self):
        """Test ticket creation with high priority"""
        result = create_ticket("Website is down", self.tool_context, "high")

        assert result["status"] == "success"
        assert "high priority" in result["report"]
        assert result["ticket"]["priority"] == "high"
        assert "24 hours" in result["ticket"]["estimated_response"]

    def test_create_ticket_invalid_priority(self):
        """Test ticket creation with invalid priority"""
        result = create_ticket("Test issue", self.tool_context, "invalid")

        assert result["status"] == "error"
        assert "Invalid priority" in result["error"]
        assert "ticket" not in result

    def test_create_ticket_unique_ids(self):
        """Test that ticket IDs are unique"""
        result1 = create_ticket("Issue 1", self.tool_context)
        result2 = create_ticket("Issue 2", self.tool_context)

        assert result1["ticket"]["ticket_id"] != result2["ticket"]["ticket_id"]

    def test_check_ticket_status_existing(self):
        """Test checking status of existing ticket"""
        # Create a ticket first
        create_result = create_ticket("Test issue", self.tool_context)
        ticket_id = create_result["ticket"]["ticket_id"]

        # Check its status
        status_result = check_ticket_status(ticket_id, self.tool_context)

        assert status_result["status"] == "success"
        assert ticket_id in status_result["report"]
        assert status_result["ticket"]["status"] == "open"

    def test_check_ticket_status_not_found(self):
        """Test checking status of non-existent ticket"""
        result = check_ticket_status("TICK-NONEXISTENT", self.tool_context)

        assert result["status"] == "error"
        assert "not found" in result["error"]
        assert "ticket" not in result


class TestAgentConfiguration:
    """Test agent setup and configuration"""

    def test_agent_exists(self):
        """Test that the agent is properly defined"""
        assert root_agent is not None
        assert hasattr(root_agent, 'name')

    def test_agent_name(self):
        """Test agent has correct name"""
        assert root_agent.name == "support_agent"

    def test_agent_has_tools(self):
        """Test agent has the required tools"""
        tool_names = [tool.__name__ for tool in root_agent.tools]
        assert "search_knowledge_base" in tool_names
        assert "create_ticket" in tool_names
        assert "check_ticket_status" in tool_names

    def test_agent_model(self):
        """Test agent uses correct model"""
        assert root_agent.model == "gemini-2.0-flash-exp"

    def test_agent_has_description(self):
        """Test agent has description"""
        assert root_agent.description is not None
        assert "support" in root_agent.description.lower()

    def test_agent_has_instruction(self):
        """Test agent has instruction"""
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0

    def test_agent_output_key(self):
        """Test agent has correct output key"""
        assert root_agent.output_key == "support_response"


class TestIntegration:
    """Integration tests for multi-step workflows"""

    def setup_method(self):
        """Setup before each test"""
        self.tool_context = Mock()
        self.tool_context.tickets = {}

    def test_knowledge_base_completeness(self):
        """Test that knowledge base covers expected topics"""
        topics = ["password", "refund", "shipping", "account", "billing", "technical"]

        for topic in topics:
            result = search_knowledge_base(topic, self.tool_context)
            assert result["status"] == "success"
            assert len(result["results"]) > 0, f"No results found for topic: {topic}"

    def test_ticket_creation_workflow(self):
        """Test complete ticket creation and status check workflow"""
        # Create ticket
        create_result = create_ticket("Website loading slowly", self.tool_context, "high")
        assert create_result["status"] == "success"

        ticket_id = create_result["ticket"]["ticket_id"]

        # Check status
        status_result = check_ticket_status(ticket_id, self.tool_context)
        assert status_result["status"] == "success"
        assert status_result["ticket"]["ticket_id"] == ticket_id
        assert status_result["ticket"]["status"] == "open"


class TestAgentEvaluation:
    """Agent evaluation tests using AgentEvaluator"""

    @pytest.mark.asyncio
    async def test_simple_kb_search(self):
        """Test simple knowledge base search evaluation"""
        await AgentEvaluator.evaluate(
            agent_module="support_agent",
            eval_dataset_file_path_or_dir="tests/simple.test.json",
            num_runs=1
        )

    @pytest.mark.asyncio
    async def test_ticket_creation(self):
        """Test ticket creation flow evaluation"""
        await AgentEvaluator.evaluate(
            agent_module="support_agent",
            eval_dataset_file_path_or_dir="tests/ticket_creation.test.json",
            num_runs=1
        )

    @pytest.mark.asyncio
    async def test_multi_turn_conversation(self):
        """Test complex multi-turn conversation"""
        await AgentEvaluator.evaluate(
            agent_module="support_agent",
            eval_dataset_file_path_or_dir="tests/complex.evalset.json",
            num_runs=1
        )
if __name__ == "__main__":
    pytest.main([__file__, "-v"])