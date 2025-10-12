"""Tests for tool functions."""

import pytest


class TestSearchKnowledgeBase:
    """Test the search_knowledge_base tool."""

    def test_search_refund_policy(self):
        """Test searching for refund policy."""
        try:
            from agent.agent import search_knowledge_base

            result = search_knowledge_base("refund policy")
            assert result["status"] == "success"
            assert "article" in result
            assert "Refund" in result["article"]["title"]
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_search_shipping(self):
        """Test searching for shipping information."""
        try:
            from agent.agent import search_knowledge_base

            result = search_knowledge_base("shipping")
            assert result["status"] == "success"
            assert "article" in result
            assert "Shipping" in result["article"]["title"]
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_search_warranty(self):
        """Test searching for warranty information."""
        try:
            from agent.agent import search_knowledge_base

            result = search_knowledge_base("warranty")
            assert result["status"] == "success"
            assert "article" in result
            assert "Warranty" in result["article"]["title"]
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_search_unknown_returns_general(self):
        """Test that unknown queries return general support."""
        try:
            from agent.agent import search_knowledge_base

            result = search_knowledge_base("some unknown query")
            assert result["status"] == "success"
            assert "article" in result
            assert "Support" in result["article"]["title"]
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


class TestLookupOrderStatus:
    """Test the lookup_order_status tool."""

    def test_lookup_valid_order(self):
        """Test looking up a valid order."""
        try:
            from agent.agent import lookup_order_status

            result = lookup_order_status("ORD-12345")
            assert result["status"] == "success"
            assert "order" in result
            assert result["order"]["order_id"] == "ORD-12345"
            assert "status" in result["order"]
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_lookup_invalid_order(self):
        """Test looking up an invalid order."""
        try:
            from agent.agent import lookup_order_status

            result = lookup_order_status("ORD-99999")
            assert result["status"] == "error"
            assert "error" in result or "report" in result
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_lookup_lowercase_order_id(self):
        """Test that order ID lookup is case-insensitive."""
        try:
            from agent.agent import lookup_order_status

            result = lookup_order_status("ord-12345")
            assert result["status"] == "success"
            assert "order" in result
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


class TestCreateSupportTicket:
    """Test the create_support_ticket tool."""

    def test_create_normal_priority_ticket(self):
        """Test creating a normal priority ticket."""
        try:
            from agent.agent import create_support_ticket

            result = create_support_ticket("Test issue", "normal")
            assert result["status"] == "success"
            assert "ticket" in result
            assert "ticket_id" in result["ticket"]
            assert result["ticket"]["priority"] == "normal"
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_create_urgent_priority_ticket(self):
        """Test creating an urgent priority ticket."""
        try:
            from agent.agent import create_support_ticket

            result = create_support_ticket("Urgent issue", "urgent")
            assert result["status"] == "success"
            assert "ticket" in result
            assert result["ticket"]["priority"] == "urgent"
            assert "1-2 hours" in result["ticket"]["estimated_response"]
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_create_ticket_default_priority(self):
        """Test creating a ticket with default priority."""
        try:
            from agent.agent import create_support_ticket

            result = create_support_ticket("Test issue")
            assert result["status"] == "success"
            assert "ticket" in result
            assert result["ticket"]["priority"] == "normal"
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")

    def test_ticket_id_format(self):
        """Test that ticket ID has correct format."""
        try:
            from agent.agent import create_support_ticket

            result = create_support_ticket("Test issue")
            ticket_id = result["ticket"]["ticket_id"]
            assert ticket_id.startswith("TICKET-")
            assert len(ticket_id) > 7  # TICKET- plus hash
        except ImportError as e:
            pytest.skip(f"Import failed (dependencies not installed): {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
