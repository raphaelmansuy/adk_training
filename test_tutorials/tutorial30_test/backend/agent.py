"""Customer support ADK agent with AG-UI integration - Tutorial 30."""

import os
from typing import Dict
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AG-UI ADK integration imports
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Google ADK imports
from google.adk.agents import LlmAgent

# Load environment variables
load_dotenv()

# Define knowledge base search tool
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information.
    
    Args:
        query: Search query to find relevant articles
        
    Returns:
        Formatted string with article title and content
    """
    # Mock knowledge base - replace with real database/vector store
    knowledge_base = {
        "refund policy": {
            "title": "Refund Policy",
            "content": "We offer full refunds within 30 days of purchase. " +
                      "Contact support@company.com to initiate a refund."
        },
        "shipping": {
            "title": "Shipping Information",
            "content": "Standard shipping takes 5-7 business days. " +
                      "Express shipping (2-3 days) available for $15 extra."
        },
        "warranty": {
            "title": "Warranty Coverage",
            "content": "All products include 1-year warranty covering " +
                      "manufacturing defects. Extended warranty available."
        },
        "account": {
            "title": "Account Management",
            "content": "Reset password at /account/reset. Update billing " +
                      "info at /account/billing. Cancel subscription anytime."
        }
    }
    
    # Simple keyword matching - use vector search in production
    query_lower = query.lower()
    for key, article in knowledge_base.items():
        if key in query_lower:
            return f"**{article['title']}**\n\n{article['content']}"
    
    # Default response
    return ("**General Support**\n\n"
            "Please contact our support team at support@company.com "
            "or call 1-800-SUPPORT for personalized assistance.")


def lookup_order_status(order_id: str) -> str:
    """
    Look up the status of a customer order.
    
    Args:
        order_id: The order ID to look up
        
    Returns:
        Order status information
    """
    # Mock order database - replace with real database
    orders = {
        "ORD-12345": "Shipped - Arriving tomorrow",
        "ORD-67890": "Processing - Ships in 2-3 days",
        "ORD-11111": "Delivered on Jan 15, 2024"
    }
    
    if order_id.upper() in orders:
        return f"Order {order_id}: {orders[order_id.upper()]}"
    return f"Order {order_id} not found. Please check the order ID and try again."


def create_support_ticket(issue_description: str, priority: str = "normal") -> str:
    """
    Create a support ticket for complex issues.
    
    Args:
        issue_description: Description of the customer's issue
        priority: Priority level (low, normal, high, urgent)
        
    Returns:
        Ticket confirmation with ticket ID
    """
    import uuid
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
    
    return (f"Support ticket created successfully!\n\n"
            f"**Ticket ID:** {ticket_id}\n"
            f"**Priority:** {priority}\n"
            f"**Issue:** {issue_description}\n\n"
            f"Our support team will contact you within 24 hours.")


# Create ADK agent with tools using the new API
adk_agent = LlmAgent(
    name="customer_support_agent",
    model="gemini-2.5-flash",  # or "gemini-2.0-flash-exp"
    instruction="""You are a helpful customer support agent for an e-commerce company.

Your responsibilities:
- Answer customer questions clearly and concisely
- Search the knowledge base when needed using search_knowledge_base()
- Look up order status using lookup_order_status() when customers ask about their orders
- Create support tickets using create_support_ticket() for complex issues
- Be empathetic and professional
- Escalate complex issues to human support when appropriate
- Never make up information - if unsure, say so

Guidelines:
- Greet customers warmly
- Use the appropriate tool for each type of query
- Offer next steps after answering
- Keep responses under 3 paragraphs unless more detail is requested
- Use a friendly but professional tone
- Format responses with markdown for better readability""",
    tools=[search_knowledge_base, lookup_order_status, create_support_ticket]
)

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="customer_support_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(title="Customer Support Agent API")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add ADK endpoint for CopilotKit
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent": "customer_support_agent"}

# Run with: uvicorn agent:app --reload --port 8000
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "agent:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
