"""
Support Bot Agent for Team Support

This agent provides team support capabilities with tools for:
- Knowledge base search
- Support ticket creation
"""

from typing import Dict, Any
from google.adk.agents import Agent
import uuid
from datetime import datetime


# Mock knowledge base for the agent
KNOWLEDGE_BASE = {
    "password_reset": {
        "title": "How to Reset Your Password",
        "content": """To reset your password:
1. Visit https://account.company.com
2. Click "Forgot Password"
3. Enter your work email
4. Check your email for reset link
5. Create a new strong password (8+ chars, mix of letters/numbers/symbols)

If you don't receive the email within 5 minutes, check your spam folder or contact IT at it-help@company.com.""",
        "tags": ["password", "reset", "account", "login"]
    },
    "expense_report": {
        "title": "Filing Expense Reports",
        "content": """To file an expense report:
1. Log in to Expensify at https://expensify.company.com
2. Click "New Report"
3. Add expenses with receipts
4. Submit for manager approval
5. Reimbursement within 7 business days

Eligible expenses: Travel, meals (up to $50/day), software subscriptions (pre-approved).

Questions? Email finance@company.com""",
        "tags": ["expense", "reimbursement", "finance", "expensify"]
    },
    "vacation_policy": {
        "title": "Vacation and PTO Policy",
        "content": """Our PTO policy:
• 15 days PTO per year (prorated for first year)
• 5 sick days per year
• 10 company holidays
• Unlimited unpaid time off (with manager approval)

To request time off:
1. Submit in BambooHR at https://bamboo.company.com
2. Get manager approval
3. Update your Slack status
4. Add to team calendar

Plan ahead for busy periods (Q4, product launches).""",
        "tags": ["vacation", "pto", "time off", "leave", "holiday"]
    },
    "remote_work": {
        "title": "Remote Work Policy",
        "content": """Remote work options:
• Hybrid: 3 days in office, 2 remote (standard)
• Full remote: Available for approved roles
• Temporary remote: For travel, emergencies (notify manager)

Requirements:
• Reliable internet (50+ Mbps)
• Quiet workspace
• Available during core hours (10am-3pm local time)
• Regular video presence in meetings

Equipment stipend: $500/year for home office setup.""",
        "tags": ["remote", "work from home", "hybrid", "wfh"]
    },
    "it_support": {
        "title": "IT Support Contacts",
        "content": """IT Support channels:
• Slack: #it-support (fastest, 9am-6pm ET)
• Email: it-help@company.com (24h response)
• Phone: 1-800-IT-HELPS (urgent issues only)
• Portal: https://support.company.com

Common issues:
• VPN: Use Cisco AnyConnect, credentials = AD login
• Printer: Add via System Preferences → Printers
• Software installs: Request in #it-support

Emergency (P0): Call phone number for system outages.""",
        "tags": ["IT", "support", "help", "technical", "vpn", "printer"]
    }
}

# Store for created tickets
TICKETS = {}


def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Search the company knowledge base for information.

    This function searches through the knowledge base by matching keywords
    in titles, content, and tags. Returns the best matching article if found.

    Args:
        query: Search query (e.g., "password reset", "vacation policy")

    Returns:
        Dict with 'status', 'report', and optional 'article' data
    """
    try:
        query_lower = query.lower()

        # Search by tags and content
        matches = []
        for key, article in KNOWLEDGE_BASE.items():
            score = 0

            # Check title match
            if query_lower in article["title"].lower():
                score += 3

            # Check tag matches
            for tag in article["tags"]:
                if query_lower in tag.lower():
                    score += 2

            # Check content match
            if query_lower in article["content"].lower():
                score += 1

            if score > 0:
                matches.append((key, article, score))

        if matches:
            # Return best match
            best_key, best_article, best_score = sorted(
                matches, key=lambda x: x[2], reverse=True
            )[0]

            return {
                'status': 'success',
                'report': f"Found article: {best_article['title']}",
                'article': {
                    'title': best_article['title'],
                    'content': best_article['content']
                }
            }
        else:
            return {
                'status': 'success',
                'report': "No articles found matching your query. Try searching for: password, expense, vacation, remote, or IT support.",
                'article': None
            }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Error searching knowledge base: {str(e)}'
        }


def create_support_ticket(
    subject: str,
    description: str,
    priority: str = "normal"
) -> Dict[str, Any]:
    """
    Create a support ticket for complex issues.

    This function creates a support ticket that can be tracked and managed
    by the support team.

    Args:
        subject: Brief ticket subject line
        description: Detailed problem description
        priority: Ticket priority: "low", "normal", "high", or "urgent"

    Returns:
        Dict with ticket creation status and ticket ID
    """
    try:
        # Validate priority
        valid_priorities = ["low", "normal", "high", "urgent"]
        if priority.lower() not in valid_priorities:
            return {
                'status': 'error',
                'error': f'Invalid priority. Must be one of: {", ".join(valid_priorities)}',
                'report': f'Error: Invalid priority level "{priority}"'
            }

        # Create ticket
        ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        ticket = {
            'id': ticket_id,
            'subject': subject,
            'description': description,
            'priority': priority.lower(),
            'created_at': datetime.now().isoformat(),
            'status': 'open'
        }

        TICKETS[ticket_id] = ticket

        report = (
            f"✅ Support ticket created: **{ticket_id}**\n"
            f"Subject: {subject}\n"
            f"Priority: {priority.upper()}\n"
            f"Status: Open\n\n"
            f"Our support team will review your ticket shortly. "
            f"You can track it at: https://support.company.com/tickets/{ticket_id}"
        )

        return {
            'status': 'success',
            'report': report,
            'ticket': {
                'id': ticket_id,
                'subject': subject,
                'priority': priority,
                'created_at': ticket['created_at']
            }
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Error creating support ticket: {str(e)}'
        }


# Create the support bot agent with tools
root_agent = Agent(
    name="support_bot",
    model="gemini-2.5-flash",
    description="A team support assistant that helps with company policies and issues",
    instruction="""You are a helpful team support assistant for a tech company.

Your responsibilities:
- Answer questions using the knowledge base
- Help with company policies and procedures
- Provide IT support guidance
- Create support tickets for complex issues

Guidelines:
- ALWAYS use search_knowledge_base when users ask about:
  * Company policies (PTO, remote work, expenses)
  * IT support (passwords, VPN, printer, software)
  * Procedures and processes
- Use create_support_ticket for complex issues that need human review
- Format responses clearly with bullet points
- Include relevant links from knowledge base
- Use Slack formatting (*bold*, `code`, > quotes)
- If you can't find info, admit it and suggest contacting the right team
- Be empathetic and professional

Remember: You're helping employees be productive!""",
    tools=[
        search_knowledge_base,
        create_support_ticket
    ]
)
