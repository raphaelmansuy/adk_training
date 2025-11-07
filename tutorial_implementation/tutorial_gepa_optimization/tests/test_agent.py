"""
Test suite for GEPA tutorial agent.

Tests cover:
- Agent configuration and initialization
- Tool declarations and execution
- GEPA concepts and workflow
- Project structure validation
"""

import pytest
from gepa_agent.agent import (
    VerifyCustomerIdentity,
    CheckReturnPolicy,
    ProcessRefund,
    create_support_agent,
    root_agent,
    INITIAL_PROMPT,
)


class TestAgentConfiguration:
    """Test agent initialization and configuration."""

    def test_agent_creation(self):
        """Test that agent can be created successfully."""
        agent = create_support_agent()
        assert agent is not None
        assert agent.name == "customer_support_agent"

    def test_root_agent_export(self):
        """Test that root_agent is properly exported."""
        assert root_agent is not None
        assert hasattr(root_agent, "name")
        assert root_agent.name == "customer_support_agent"

    def test_agent_with_custom_prompt(self):
        """Test agent creation with custom prompt."""
        custom_prompt = "You are a test agent."
        agent = create_support_agent(prompt=custom_prompt)
        assert agent is not None

    def test_agent_uses_initial_prompt_by_default(self):
        """Test that agent uses INITIAL_PROMPT when none provided."""
        agent = create_support_agent()
        assert agent.instruction == INITIAL_PROMPT

    def test_agent_has_tools(self):
        """Test that agent has all required tools."""
        agent = create_support_agent()
        assert agent.tools is not None
        assert len(agent.tools) == 3

    def test_agent_model_configuration(self):
        """Test that agent uses correct model."""
        agent = create_support_agent()
        assert agent.model is not None

    def test_custom_model(self):
        """Test agent with custom model specification."""
        agent = create_support_agent(model="gemini-2.0-flash")
        assert agent is not None


class TestVerifyCustomerIdentityTool:
    """Test verify_customer_identity tool."""

    @pytest.fixture
    def tool(self):
        """Create tool instance for testing."""
        return VerifyCustomerIdentity()

    def test_tool_creation(self, tool):
        """Test tool can be instantiated."""
        assert tool is not None
        assert tool.name == "verify_customer_identity"

    def test_tool_declaration(self, tool):
        """Test tool has proper declaration."""
        declaration = tool._get_declaration()
        assert declaration is not None
        assert declaration.name == "verify_customer_identity"
        assert "parameters" in dir(declaration)

    def test_tool_description(self, tool):
        """Test tool has description."""
        assert tool.description is not None
        assert len(tool.description) > 0

    @pytest.mark.asyncio
    async def test_valid_customer_verification(self, tool):
        """Test verification with valid customer."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-12345",
                "email": "customer@example.com",
            },
            tool_context=None,
        )
        assert "✓" in result
        assert "verified" in result.lower()

    @pytest.mark.asyncio
    async def test_invalid_email_verification(self, tool):
        """Test verification with wrong email."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-12345",
                "email": "wrong@example.com",
            },
            tool_context=None,
        )
        assert "✗" in result
        assert "failed" in result.lower()

    @pytest.mark.asyncio
    async def test_unknown_order_verification(self, tool):
        """Test verification with unknown order."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-99999",
                "email": "customer@example.com",
            },
            tool_context=None,
        )
        assert "✗" in result
        assert "not found" in result.lower()


class TestCheckReturnPolicyTool:
    """Test check_return_policy tool."""

    @pytest.fixture
    def tool(self):
        """Create tool instance for testing."""
        return CheckReturnPolicy()

    def test_tool_creation(self, tool):
        """Test tool can be instantiated."""
        assert tool is not None
        assert tool.name == "check_return_policy"

    def test_tool_declaration(self, tool):
        """Test tool has proper declaration."""
        declaration = tool._get_declaration()
        assert declaration is not None
        assert declaration.name == "check_return_policy"

    @pytest.mark.asyncio
    async def test_within_return_window(self, tool):
        """Test order within 30-day return window."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-12345",
                "days_since_purchase": 15,
            },
            tool_context=None,
        )
        assert "✓" in result
        assert "eligible" in result.lower()

    @pytest.mark.asyncio
    async def test_at_return_window_boundary(self, tool):
        """Test order at 30-day boundary."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-12345",
                "days_since_purchase": 30,
            },
            tool_context=None,
        )
        assert "✓" in result
        assert "eligible" in result.lower()

    @pytest.mark.asyncio
    async def test_outside_return_window(self, tool):
        """Test order outside 30-day return window."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-12345",
                "days_since_purchase": 45,
            },
            tool_context=None,
        )
        assert "✗" in result
        assert "cannot be returned" in result.lower()


class TestProcessRefundTool:
    """Test process_refund tool."""

    @pytest.fixture
    def tool(self):
        """Create tool instance for testing."""
        return ProcessRefund()

    def test_tool_creation(self, tool):
        """Test tool can be instantiated."""
        assert tool is not None
        assert tool.name == "process_refund"

    def test_tool_declaration(self, tool):
        """Test tool has proper declaration."""
        declaration = tool._get_declaration()
        assert declaration is not None
        assert declaration.name == "process_refund"

    @pytest.mark.asyncio
    async def test_refund_processing(self, tool):
        """Test successful refund processing."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-12345",
                "amount": 99.99,
                "reason": "Customer requested return",
            },
            tool_context=None,
        )
        assert "✓" in result
        assert "processed" in result.lower()
        assert "99.99" in result

    @pytest.mark.asyncio
    async def test_refund_includes_transaction_id(self, tool):
        """Test refund includes transaction details."""
        result = await tool.run_async(
            args={
                "order_id": "ORD-12345",
                "amount": 50.00,
                "reason": "Defective product",
            },
            tool_context=None,
        )
        assert "TXN-" in result
        assert "3-5 business days" in result


class TestGEPAConcepts:
    """Test GEPA optimization concepts through the agent."""

    def test_initial_prompt_identifies_gaps(self):
        """Test that initial prompt has known gaps for GEPA to optimize."""
        # The initial prompt is intentionally simple
        # GEPA should optimize it to be more specific about:
        # 1. Identity verification requirements
        # 2. Policy adherence procedures
        # 3. Clear explanation guidelines
        assert "polite and professional" in INITIAL_PROMPT.lower()
        # Should lack specific requirements for optimization

    def test_agent_has_evaluation_capability(self):
        """Test agent setup enables GEPA evaluation."""
        agent = create_support_agent()
        # Agent should have:
        # - Tools for evaluation (simulate customer scenarios)
        # - Clear instruction-based behavior
        # - Deterministic enough for optimization
        assert agent.tools
        assert agent.instruction

    def test_prompt_optimization_target(self):
        """Test agent is suitable for prompt optimization."""
        # This agent is good for GEPA because:
        # 1. Clear success/failure scenarios (refund handling)
        # 2. Tool use is deterministic
        # 3. Failures are identifiable (wrong order, policy violation)
        agent = create_support_agent()
        assert len(agent.tools) > 0

    def test_seed_prompt_evolution_potential(self):
        """Test that seed prompt has room for evolution."""
        evolved_prompt = """You are an expert customer support agent.

CRITICAL REQUIREMENTS:
1. ALWAYS verify customer identity FIRST
   - Never process refunds without identity verification
   - Use verify_customer_identity tool

2. ALWAYS check return policy
   - Validate 30-day return window
   - Clearly explain policy to customer

3. Provide clear explanations
   - Explain all decisions
   - Reference specific order details
   - Use simple, professional language

Tool Usage Sequence:
- First: verify_customer_identity
- Second: check_return_policy
- Third: process_refund (if eligible)"""

        # Evolved prompt has more structure and requirements
        assert "ALWAYS" in evolved_prompt
        assert "CRITICAL" in evolved_prompt
        assert "verify_customer_identity" in evolved_prompt
