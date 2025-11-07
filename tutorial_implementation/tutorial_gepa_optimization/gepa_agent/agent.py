"""
GEPA Tutorial Agent: Simulated Customer Support Agent

This agent demonstrates GEPA (Genetic-Pareto Prompt Optimization) concepts
by implementing a customer support agent that handles various customer
requests. The prompt can be optimized using GEPA to improve handling of
identity verification, policy adherence, and explanation clarity.

The agent uses three tools:
1. verify_customer_identity - Verifies customer information
2. check_return_policy - Validates return eligibility
3. process_refund - Handles refund operations
"""

from typing import Any, Dict

from google.adk.agents import llm_agent
from google.adk.models import google_llm
from google.adk.tools import base_tool
from google.genai import types


class VerifyCustomerIdentity(base_tool.BaseTool):
    """Verifies customer identity before sensitive operations."""

    def __init__(self):
        super().__init__(
            name="verify_customer_identity",
            description="Verify customer identity by checking order number and email",
        )

    def _get_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name="verify_customer_identity",
            description="Verify customer identity for security-sensitive operations",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "order_id": types.Schema(
                        type=types.Type.STRING,
                        description="Customer order ID",
                    ),
                    "email": types.Schema(
                        type=types.Type.STRING,
                        description="Customer email address",
                    ),
                },
                required=["order_id", "email"],
            ),
        )

    async def run_async(
        self, *, args: Dict[str, Any], tool_context: Any
    ) -> str:
        """
        Verify customer identity.

        Returns success/failure based on simple validation logic.
        """
        order_id = args.get("order_id", "")
        email = args.get("email", "")

        # Simulate customer database lookup
        valid_customers = {
            "ORD-12345": "customer@example.com",
            "ORD-67890": "john@example.com",
            "ORD-11111": "jane@example.com",
        }

        if order_id in valid_customers:
            if valid_customers[order_id] == email:
                return (
                    f"✓ Customer verified successfully. Order: {order_id}, "
                    f"Email: {email}"
                )
            else:
                return (
                    f"✗ Email does not match for order {order_id}. "
                    f"Verification failed."
                )
        else:
            return f"✗ Order {order_id} not found in system."


class CheckReturnPolicy(base_tool.BaseTool):
    """Checks if an order is eligible for return based on return policy."""

    def __init__(self):
        super().__init__(
            name="check_return_policy",
            description="Check if an order is within the 30-day return window",
        )

    def _get_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name="check_return_policy",
            description="Validate return policy - 30-day return window",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "order_id": types.Schema(
                        type=types.Type.STRING,
                        description="Order ID to check",
                    ),
                    "days_since_purchase": types.Schema(
                        type=types.Type.INTEGER,
                        description="Days since order was placed",
                    ),
                },
                required=["order_id", "days_since_purchase"],
            ),
        )

    async def run_async(
        self, *, args: Dict[str, Any], tool_context: Any
    ) -> str:
        """
        Check return policy compliance.

        Returns whether order is within 30-day return window.
        """
        order_id = args.get("order_id", "")
        days = args.get("days_since_purchase", 0)

        if days <= 30:
            return (
                f"✓ Order {order_id} is eligible for return. "
                f"({days} days since purchase - within 30-day window)"
            )
        else:
            return (
                f"✗ Order {order_id} cannot be returned. "
                f"({days} days since purchase - OUTSIDE 30-day window). "
                f"Our return policy allows returns within 30 days of purchase."
            )


class ProcessRefund(base_tool.BaseTool):
    """Processes a refund for eligible orders."""

    def __init__(self):
        super().__init__(
            name="process_refund",
            description="Process refund for eligible customer orders",
        )

    def _get_declaration(self) -> types.FunctionDeclaration:
        return types.FunctionDeclaration(
            name="process_refund",
            description="Process refund after verification and policy check",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "order_id": types.Schema(
                        type=types.Type.STRING,
                        description="Order ID to refund",
                    ),
                    "amount": types.Schema(
                        type=types.Type.NUMBER,
                        description="Refund amount in dollars",
                    ),
                    "reason": types.Schema(
                        type=types.Type.STRING,
                        description="Reason for refund",
                    ),
                },
                required=["order_id", "amount", "reason"],
            ),
        )

    async def run_async(
        self, *, args: Dict[str, Any], tool_context: Any
    ) -> str:
        """
        Process refund operation.

        Returns confirmation with transaction details.
        """
        order_id = args.get("order_id", "")
        amount = args.get("amount", 0)
        reason = args.get("reason", "")

        # Generate transaction ID
        transaction_id = f"TXN-{order_id}-001"

        return (
            f"✓ Refund processed successfully!\n"
            f"  Transaction ID: {transaction_id}\n"
            f"  Order: {order_id}\n"
            f"  Amount: ${amount:.2f}\n"
            f"  Reason: {reason}\n"
            f"  Estimated return to account: 3-5 business days"
        )


# Initial prompt for the support agent
# This is the seed prompt that would be optimized by GEPA
INITIAL_PROMPT = """You are a helpful customer support agent for an online retailer.

Your role is to assist customers with their orders, returns, and refunds.

Important guidelines:
- Be polite and professional
- Understand customer issues thoroughly
- Use the available tools to help customers
- Follow company policies

When helping with refunds:
- Ask for necessary information (order ID, email)
- Verify customer identity
- Check return policy
- Explain your decisions clearly"""


def create_support_agent(
    prompt: str | None = None,
    model: str = "gemini-2.5-flash",
) -> llm_agent.LlmAgent:
    """
    Create a customer support agent.

    Args:
        prompt: Custom system prompt for the agent. If None, uses INITIAL_PROMPT
        model: LLM model to use

    Returns:
        Configured ADK LLM agent
    """
    if prompt is None:
        prompt = INITIAL_PROMPT

    return llm_agent.LlmAgent(
        name="customer_support_agent",
        model=google_llm.Gemini(model=model),
        instruction=prompt,
        tools=[
            VerifyCustomerIdentity(),
            CheckReturnPolicy(),
            ProcessRefund(),
        ],
        description="Customer support agent for handling orders and refunds",
    )


# Root agent export (required by ADK)
root_agent = create_support_agent()
