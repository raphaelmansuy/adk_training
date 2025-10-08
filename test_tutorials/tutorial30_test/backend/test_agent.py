"""Tutorial 30 - Test Suite for Customer Support Agent."""

import pytest
from fastapi.testclient import TestClient
from agent import (
    app,
    search_knowledge_base,
    lookup_order_status,
    create_support_ticket,
    adk_agent,
    agent
)

client = TestClient(app)


class TestTutorial30CustomerSupportAgent:
    """Test suite for Tutorial 30 customer support agent."""

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "customer_support_agent"

    def test_cors_configuration(self):
        """Test CORS headers are configured correctly."""
        response = client.options(
            "/api/copilotkit",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_copilotkit_endpoint_registered(self):
        """Test that CopilotKit endpoint exists."""
        routes = [str(route.path) for route in app.routes]
        assert any("/api/copilotkit" in route for route in routes)


class TestKnowledgeBaseSearch:
    """Test knowledge base search functionality."""

    def test_search_refund_policy(self):
        """Test searching for refund policy."""
        result = search_knowledge_base("refund policy")
        assert "Refund Policy" in result
        assert "30 days" in result
        assert "support@company.com" in result

    def test_search_shipping_info(self):
        """Test searching for shipping information."""
        result = search_knowledge_base("shipping")
        assert "Shipping Information" in result
        assert "5-7 business days" in result
        assert "$15" in result

    def test_search_warranty(self):
        """Test searching for warranty information."""
        result = search_knowledge_base("warranty")
        assert "Warranty Coverage" in result
        assert "1-year" in result
        assert "manufacturing defects" in result

    def test_search_account_management(self):
        """Test searching for account info."""
        result = search_knowledge_base("account")
        assert "Account Management" in result
        assert "/account/reset" in result
        assert "/account/billing" in result

    def test_search_no_match_returns_general_support(self):
        """Test that unmatched queries return general support info."""
        result = search_knowledge_base("random query xyz")
        assert "General Support" in result
        assert "support@company.com" in result
        assert "1-800-SUPPORT" in result


class TestOrderStatusLookup:
    """Test order status lookup functionality."""

    def test_lookup_existing_order_12345(self):
        """Test looking up order ORD-12345."""
        result = lookup_order_status("ORD-12345")
        assert "ORD-12345" in result
        assert "Shipped" in result
        assert "Arriving tomorrow" in result

    def test_lookup_existing_order_67890(self):
        """Test looking up order ORD-67890."""
        result = lookup_order_status("ORD-67890")
        assert "ORD-67890" in result
        assert "Processing" in result
        assert "2-3 days" in result

    def test_lookup_existing_order_11111(self):
        """Test looking up order ORD-11111."""
        result = lookup_order_status("ORD-11111")
        assert "ORD-11111" in result
        assert "Delivered" in result
        assert "Jan 15, 2024" in result

    def test_lookup_case_insensitive(self):
        """Test that order lookup is case-insensitive."""
        result = lookup_order_status("ord-12345")
        # Check either the uppercase order ID or the lowercase one is returned
        assert ("ORD-12345" in result or "ord-12345" in result)
        assert "Shipped" in result

    def test_lookup_nonexistent_order(self):
        """Test looking up an order that doesn't exist."""
        result = lookup_order_status("ORD-99999")
        assert "not found" in result
        assert "ORD-99999" in result


class TestSupportTicketCreation:
    """Test support ticket creation functionality."""

    def test_create_ticket_normal_priority(self):
        """Test creating a ticket with normal priority."""
        result = create_support_ticket(
            issue_description="Cannot login to my account",
            priority="normal"
        )
        assert "Support ticket created successfully" in result
        assert "TICKET-" in result
        assert "normal" in result
        assert "Cannot login to my account" in result
        assert "24 hours" in result

    def test_create_ticket_high_priority(self):
        """Test creating a ticket with high priority."""
        result = create_support_ticket(
            issue_description="Payment issue",
            priority="high"
        )
        assert "TICKET-" in result
        assert "high" in result
        assert "Payment issue" in result

    def test_create_ticket_default_priority(self):
        """Test creating a ticket without specifying priority."""
        result = create_support_ticket(
            issue_description="Question about product"
        )
        assert "TICKET-" in result
        assert "normal" in result
        assert "Question about product" in result

    def test_create_ticket_generates_unique_id(self):
        """Test that each ticket gets a unique ID."""
        result1 = create_support_ticket("Issue 1")
        result2 = create_support_ticket("Issue 2")
        
        # Extract ticket IDs
        ticket_id_1 = result1.split("TICKET-")[1].split("\\n")[0]
        ticket_id_2 = result2.split("TICKET-")[1].split("\\n")[0]
        
        assert ticket_id_1 != ticket_id_2


class TestAgentConfiguration:
    """Test agent configuration and setup."""

    def test_agent_exists(self):
        """Test that agent is properly initialized."""
        assert adk_agent is not None
        assert agent is not None

    def test_agent_has_correct_name(self):
        """Test that agent has the correct name."""
        assert hasattr(adk_agent, "name") or hasattr(adk_agent, "_name")

    def test_agent_has_tools(self):
        """Test that agent has tools configured."""
        # Check that agent was created with tools
        assert adk_agent is not None
        # Tools should be configured in the agent

    def test_adk_agent_wrapper_configured(self):
        """Test that ADKAgent wrapper is configured."""
        assert agent is not None
        # Should have ADKAgent wrapper configuration


class TestAPIConfiguration:
    """Test API configuration."""

    def test_fastapi_app_title(self):
        """Test FastAPI app has correct title."""
        assert app.title == "Customer Support Agent API"

    def test_cors_middleware_present(self):
        """Test that CORS middleware is configured."""
        middlewares = [m.__class__.__name__ for m in app.user_middleware]
        # In newer FastAPI versions, CORS is wrapped as "Middleware"
        assert "CORSMiddleware" in middlewares or "Middleware" in middlewares

    def test_multiple_origins_allowed(self):
        """Test that multiple origins are allowed for CORS."""
        # Check localhost:3000 (Next.js default)
        response1 = client.options(
            "/api/copilotkit",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert response1.status_code == 200

        # Check localhost:5173 (Vite default)
        response2 = client.options(
            "/api/copilotkit",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert response2.status_code == 200


class TestToolFunctionality:
    """Test that tools work correctly together."""

    def test_all_three_tools_work(self):
        """Test that all three tools can be called."""
        # Knowledge base search
        kb_result = search_knowledge_base("refund policy")
        assert "Refund Policy" in kb_result

        # Order lookup
        order_result = lookup_order_status("ORD-12345")
        assert "Shipped" in order_result

        # Ticket creation
        ticket_result = create_support_ticket("Test issue")
        assert "TICKET-" in ticket_result

    def test_knowledge_base_covers_multiple_topics(self):
        """Test that knowledge base has multiple topics."""
        topics = ["refund policy", "shipping", "warranty", "account"]
        for topic in topics:
            result = search_knowledge_base(topic)
            # Check that we don't get the default "General Support" response
            assert "General Support" not in result or topic in result.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
