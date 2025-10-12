"""Customer support ADK agent with AG-UI integration.

This agent provides customer support functionality with tools for knowledge base
search, order status lookup, and support ticket creation. It integrates with
Next.js frontends via the AG-UI protocol.
"""

import os
import uuid
import json
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import uvicorn

# AG-UI ADK integration imports
try:
    from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
except ImportError:
    raise ImportError(
        "ag_ui_adk not found. Install with: pip install ag-ui-adk"
    )

# Google ADK imports
from google.adk.agents import Agent

# Load environment variables
load_dotenv()


# ============================================================================
# Tool Definitions
# ============================================================================


def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Search the knowledge base for relevant information.

    Args:
        query: Search query to find relevant articles

    Returns:
        Dict with status, report, and article data
    """
    # Mock knowledge base - replace with real database/vector store in production
    knowledge_base = {
        "refund policy": {
            "title": "Refund Policy",
            "content": (
                "We offer full refunds within 30 days of purchase. "
                "Contact support@company.com to initiate a refund."
            ),
        },
        "shipping": {
            "title": "Shipping Information",
            "content": (
                "Standard shipping takes 5-7 business days. "
                "Express shipping (2-3 days) available for $15 extra."
            ),
        },
        "warranty": {
            "title": "Warranty Coverage",
            "content": (
                "All products include 1-year warranty covering "
                "manufacturing defects. Extended warranty available."
            ),
        },
        "account": {
            "title": "Account Management",
            "content": (
                "Reset password at /account/reset. Update billing "
                "info at /account/billing. Cancel subscription anytime."
            ),
        },
    }

    # Simple keyword matching - use vector search in production
    query_lower = query.lower()
    for key, article in knowledge_base.items():
        if key in query_lower:
            return {
                "status": "success",
                "report": f"Found article: {article['title']}",
                "article": article,
            }

    # Default response
    return {
        "status": "success",
        "report": "No specific article found, providing general support info",
        "article": {
            "title": "General Support",
            "content": (
                "Please contact our support team at support@company.com "
                "or call 1-800-SUPPORT for personalized assistance."
            ),
        },
    }


def lookup_order_status(order_id: str) -> Dict[str, Any]:
    """
    Look up the status of a customer order.

    Args:
        order_id: The order ID to look up (format: ORD-XXXXX)

    Returns:
        Dict with status, report, and order details
    """
    # Mock order database - replace with real database in production
    orders = {
        "ORD-12345": {
            "order_id": "ORD-12345",
            "status": "Shipped",
            "tracking": "1Z999AA10123456784",
            "estimated_delivery": "2025-10-12",
            "items": "2x Widget Pro, 1x Gadget Plus",
        },
        "ORD-67890": {
            "order_id": "ORD-67890",
            "status": "Processing",
            "tracking": None,
            "estimated_delivery": "2025-10-15",
            "items": "1x Premium Kit",
        },
        "ORD-11111": {
            "order_id": "ORD-11111",
            "status": "Delivered",
            "tracking": "1Z999AA10987654321",
            "estimated_delivery": "2025-01-15",
            "items": "3x Basic Widget",
        },
    }

    order_id_upper = order_id.upper()

    if order_id_upper in orders:
        order = orders[order_id_upper]
        return {
            "status": "success",
            "report": f"Order {order_id} found: {order['status']}",
            "order": order,
        }
    else:
        return {
            "status": "error",
            "report": f"Order {order_id} not found",
            "error": "Please check the order ID and try again.",
        }


def create_support_ticket(
    issue_description: str, priority: str = "normal"
) -> Dict[str, Any]:
    """
    Create a support ticket for complex issues.

    Args:
        issue_description: Description of the customer's issue
        priority: Priority level (low, normal, high, urgent)

    Returns:
        Dict with status, report, and ticket details
    """
    # Generate unique ticket ID
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"

    # Response time based on priority
    response_times = {
        "urgent": "1-2 hours",
        "high": "4-6 hours",
        "normal": "12-24 hours",
        "low": "24-48 hours",
    }

    estimated_response = response_times.get(priority, "24 hours")

    return {
        "status": "success",
        "report": f"Support ticket {ticket_id} created successfully",
        "ticket": {
            "ticket_id": ticket_id,
            "status": "Created",
            "priority": priority,
            "issue": issue_description,
            "estimated_response": estimated_response,
            "created_at": datetime.now().isoformat(),
        },
    }


# ============================================================================
# Agent Configuration
# ============================================================================

# Create ADK agent with tools
adk_agent = Agent(
    name="customer_support_agent",
    model="gemini-2.0-flash-exp",
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
    tools=[search_knowledge_base, lookup_order_status, create_support_ticket],
)

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="customer_support_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# Export for testing
root_agent = adk_agent


# ============================================================================
# Middleware for CopilotKit Compatibility
# ============================================================================

class MessageIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to inject message IDs for CopilotKit compatibility.
    
    CopilotKit sends messages without IDs, but AG-UI protocol requires them.
    This middleware adds UUIDs to any messages missing the 'id' field.
    """
    
    async def dispatch(self, request: Request, call_next):
        """Process requests and inject message IDs where needed."""
        # Only process POST requests to /api/copilotkit
        if request.method == "POST" and request.url.path == "/api/copilotkit":
            # Read the request body
            body = await request.body()
            
            try:
                # Parse JSON
                data = json.loads(body)
                
                print(f"🔍 Middleware: Received request with keys: {list(data.keys())}")
                print(f"📄 Middleware: Full request body: {json.dumps(data, indent=2)[:500]}")
                
                # Inject IDs into messages if missing
                if "messages" in data and isinstance(data["messages"], list):
                    modified = False
                    for i, msg in enumerate(data["messages"]):
                        if isinstance(msg, dict):
                            if "id" not in msg:
                                # Generate unique ID
                                msg["id"] = f"msg-{uuid.uuid4()}"
                                modified = True
                                print(f"✅ Middleware: Added ID to message {i}: {msg.get('role', 'unknown')}")
                            else:
                                print(f"ℹ️  Middleware: Message {i} already has ID: {msg['id']}")
                    
                    # Create new request with modified body if changes were made
                    if modified:
                        modified_body = json.dumps(data).encode()
                        print(f"📝 Middleware: Modified {len(data['messages'])} messages")
                        
                        # Replace the request body
                        async def receive():
                            return {"type": "http.request", "body": modified_body}
                        
                        request._receive = receive
                    else:
                        print("ℹ️  Middleware: No modifications needed")
                else:
                    print(f"⚠️  Middleware: No 'messages' field found in request")
            
            except json.JSONDecodeError as e:
                print(f"❌ Middleware: JSON decode error: {e}")
            except Exception as e:
                print(f"❌ Middleware: Unexpected error: {e}")
        
        # Continue with the request
        response = await call_next(request)
        return response


# ============================================================================
# FastAPI Application
# ============================================================================

# Create FastAPI app
app = FastAPI(
    title="Customer Support Agent API",
    description="ADK-powered customer support agent with AG-UI integration",
    version="1.0.0",
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default
        "http://localhost:5173",  # Vite default
        "http://localhost:8000",  # Local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to inject message IDs for CopilotKit compatibility
app.add_middleware(MessageIDMiddleware)

# Add ADK endpoint for CopilotKit
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")


# Health check endpoint
@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "customer_support_agent",
        "version": "1.0.0",
    }


@app.get("/")
def root() -> Dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "Customer Support Agent API",
        "endpoints": {
            "health": "/health",
            "copilotkit": "/api/copilotkit",
            "docs": "/docs",
        },
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Get configuration from environment
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    print("=" * 60)
    print("🤖 Customer Support Agent API")
    print("=" * 60)
    print(f"🌐 Server: http://{host}:{port}")
    print(f"📚 Docs: http://{host}:{port}/docs")
    print(f"💬 CopilotKit: http://{host}:{port}/api/copilotkit")
    print("=" * 60)

    # Run with uvicorn
    uvicorn.run(
        "agent:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )
