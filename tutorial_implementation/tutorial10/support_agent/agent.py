"""
Customer Support Agent - For Evaluation Testing Demonstration

This agent demonstrates testable patterns:
- Clear tool usage (easy to validate trajectory)
- Structured responses (easy to compare)
- Deterministic behavior (where possible)
"""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from typing import Dict, Any
import uuid
from datetime import datetime

# ============================================================================
# TOOLS
# ============================================================================

def search_knowledge_base(
    query: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Search the knowledge base for information about common customer issues.

    Args:
        query: The search query to look for in the knowledge base
        tool_context: ADK tool context

    Returns:
        Dict with status, report, and search results
    """
    # In-memory knowledge base (deterministic for testing)
    knowledge_base = {
        "password reset": "To reset your password, go to Settings > Security > Reset Password. You'll receive an email with reset instructions within 5 minutes.",
        "refund policy": "We offer a 30-day money-back guarantee on all purchases. Contact support@example.com with your order number to initiate a refund.",
        "shipping": "Standard shipping takes 3-5 business days. Express shipping (1-2 days) is available for an additional $10. Track your order at example.com/track",
        "account": "Manage your account settings at example.com/account. You can update your profile, payment methods, and notification preferences.",
        "billing": "View your billing history and invoices at example.com/billing. Contact billing@example.com for payment-related questions.",
        "technical support": "For technical issues, please provide your system details and error messages. Our support team will respond within 24 hours."
    }

    # Simple keyword matching (case-insensitive)
    query_lower = query.lower()
    results = []

    for key, content in knowledge_base.items():
        if key in query_lower or any(word in query_lower for word in key.split()):
            results.append({
                "topic": key,
                "content": content
            })

    if results:
        return {
            'status': 'success',
            'report': f'Found {len(results)} relevant article(s) for "{query}"',
            'results': results
        }
    else:
        return {
            'status': 'success',
            'report': f'No articles found for "{query}". Please try rephrasing your question or contact support.',
            'results': []
        }


def create_ticket(
    issue: str,
    tool_context: ToolContext,
    priority: str = "normal"
) -> Dict[str, Any]:
    """
    Create a new support ticket for customer issues.

    Args:
        issue: Description of the customer's issue
        priority: Priority level (low, normal, high, urgent)
        tool_context: ADK tool context

    Returns:
        Dict with status, report, and ticket details
    """
    # Validate priority
    valid_priorities = ["low", "normal", "high", "urgent"]
    if priority not in valid_priorities:
        return {
            'status': 'error',
            'error': f'Invalid priority "{priority}". Must be one of: {", ".join(valid_priorities)}',
            'report': f'Failed to create ticket: invalid priority "{priority}"'
        }

    # Generate ticket ID
    ticket_id = f"TICK-{uuid.uuid4().hex[:8].upper()}"

    # Create ticket record
    ticket = {
        'ticket_id': ticket_id,
        'issue': issue,
        'priority': priority,
        'status': 'open',
        'created_at': datetime.now().isoformat(),
        'estimated_response': {
            'low': '5 business days',
            'normal': '2 business days',
            'high': '24 hours',
            'urgent': '4 hours'
        }.get(priority, '2 business days')
    }

    # Store in tool context state (in real implementation, this would be a database)
    if not hasattr(tool_context, 'tickets'):
        tool_context.tickets = {}
    tool_context.tickets[ticket_id] = ticket

    return {
        'status': 'success',
        'report': f'Ticket {ticket_id} created successfully with {priority} priority. Expected response time: {ticket["estimated_response"]}',
        'ticket': ticket
    }


def check_ticket_status(
    ticket_id: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Check the status of an existing support ticket.

    Args:
        ticket_id: The ticket ID to check
        tool_context: ADK tool context

    Returns:
        Dict with status, report, and ticket information
    """
    # Check if tickets exist in context
    if not hasattr(tool_context, 'tickets') or ticket_id not in tool_context.tickets:
        return {
            'status': 'error',
            'error': f'Ticket {ticket_id} not found',
            'report': f'Could not find ticket {ticket_id}. Please verify the ticket ID is correct.'
        }

    ticket = tool_context.tickets[ticket_id]

    return {
        'status': 'success',
        'report': f'Ticket {ticket_id} is currently {ticket["status"]} (Priority: {ticket["priority"]})',
        'ticket': ticket
    }


# ============================================================================
# AGENT DEFINITION
# ============================================================================

root_agent = Agent(
    name="support_agent",
    model="gemini-2.0-flash-exp",
    description="Customer support agent that can search knowledge base, create tickets, and check ticket status",
    instruction="""You are a helpful customer support agent. Help customers by:

1. First, try to answer their question using the knowledge base search tool
2. If you can't find relevant information, create a support ticket
3. If they mention a ticket ID, check its status

Always be polite, clear, and provide specific next steps. Use the tools appropriately based on the customer's needs.""",
    tools=[search_knowledge_base, create_ticket, check_ticket_status],
    output_key="support_response"
)