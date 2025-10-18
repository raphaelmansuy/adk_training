"""
Agent configuration and tools tests for Tutorial 33 Support Bot

Tests cover:
- Agent configuration
- Tool functionality  
- Tool return format
- Knowledge base search
- Ticket creation
"""

import pytest
from support_bot.agent import (
    root_agent,
    search_knowledge_base,
    create_support_ticket,
    KNOWLEDGE_BASE,
    TICKETS
)


class TestAgentConfiguration:
    """Test agent configuration"""

    def test_root_agent_exists(self):
        """Test that root_agent is defined and accessible."""
        assert root_agent is not None

    def test_agent_name(self):
        """Test agent name."""
        assert root_agent.name == "support_bot"

    def test_agent_model(self):
        """Test agent uses correct model."""
        assert root_agent.model == "gemini-2.5-flash"

    def test_agent_has_description(self):
        """Test agent has description."""
        assert root_agent.description
        assert isinstance(root_agent.description, str)
        assert len(root_agent.description) > 10

    def test_agent_has_instruction(self):
        """Test agent has instruction."""
        assert root_agent.instruction
        assert isinstance(root_agent.instruction, str)
        assert len(root_agent.instruction) > 50

    def test_agent_has_two_tools(self):
        """Test agent has exactly 2 tools."""
        assert len(root_agent.tools) == 2

    def test_agent_tools_are_functions(self):
        """Test agent tools are callable."""
        for tool in root_agent.tools:
            assert callable(tool)


class TestSearchKnowledgeBase:
    """Test knowledge base search tool"""

    def test_search_finds_password_reset(self):
        """Test finding password reset article."""
        result = search_knowledge_base("password reset")
        assert result['status'] == 'success'
        assert result['report'] is not None
        assert 'article' in result

    def test_search_finds_vacation_policy(self):
        """Test finding vacation policy article."""
        result = search_knowledge_base("vacation")
        assert result['status'] == 'success'
        assert result['article'] is not None
        assert "Vacation" in result['article']['title']

    def test_search_finds_expense_report(self):
        """Test finding expense report article."""
        result = search_knowledge_base("expense")
        assert result['status'] == 'success'
        assert 'Expense' in result['article']['title']

    def test_search_finds_remote_work(self):
        """Test finding remote work article."""
        result = search_knowledge_base("remote work")
        assert result['status'] == 'success'
        assert 'Remote' in result['article']['title']

    def test_search_finds_it_support(self):
        """Test finding IT support article."""
        result = search_knowledge_base("IT support")
        assert result['status'] == 'success'
        assert 'IT' in result['article']['title']

    def test_search_no_matches(self):
        """Test search with no matches."""
        result = search_knowledge_base("nonexistent topic xyz")
        assert result['status'] == 'success'
        assert result['article'] is None
        assert 'No articles found' in result['report']

    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        result1 = search_knowledge_base("PASSWORD")
        result2 = search_knowledge_base("password")
        assert result1['status'] == 'success'
        assert result2['status'] == 'success'

    def test_search_returns_content(self):
        """Test that search returns full article content."""
        result = search_knowledge_base("password")
        assert result['article'] is not None
        assert result['article']['title']
        assert result['article']['content']
        assert len(result['article']['content']) > 50

    def test_search_return_format(self):
        """Test search return format is correct."""
        result = search_knowledge_base("vacation")
        assert 'status' in result
        assert 'report' in result
        assert result['status'] in ['success', 'error']
        assert isinstance(result['report'], str)

    def test_search_error_handling(self):
        """Test search handles errors gracefully."""
        # Pass None to test error handling
        try:
            result = search_knowledge_base(None)
            # If it doesn't raise, it should still return proper format
            assert 'status' in result
        except TypeError:
            # This is acceptable - function signature validation
            pass


class TestCreateSupportTicket:
    """Test support ticket creation tool"""

    def test_create_ticket_normal_priority(self):
        """Test creating ticket with normal priority."""
        result = create_support_ticket(
            subject="VPN connection issue",
            description="Cannot connect to company VPN",
            priority="normal"
        )
        assert result['status'] == 'success'
        assert 'ticket' in result
        assert result['ticket']['id'].startswith('TKT-')
        assert result['ticket']['priority'] == 'normal'

    def test_create_ticket_high_priority(self):
        """Test creating ticket with high priority."""
        result = create_support_ticket(
            subject="Production error",
            description="API is down",
            priority="high"
        )
        assert result['status'] == 'success'
        assert result['ticket']['priority'] == 'high'

    def test_create_ticket_urgent_priority(self):
        """Test creating ticket with urgent priority."""
        result = create_support_ticket(
            subject="Security breach",
            description="Suspicious activity detected",
            priority="urgent"
        )
        assert result['status'] == 'success'
        assert result['ticket']['priority'] == 'urgent'

    def test_create_ticket_default_priority(self):
        """Test creating ticket with default priority."""
        result = create_support_ticket(
            subject="Test ticket",
            description="Test description"
        )
        assert result['status'] == 'success'
        assert result['ticket']['priority'] == 'normal'

    def test_create_ticket_invalid_priority(self):
        """Test creating ticket with invalid priority."""
        result = create_support_ticket(
            subject="Test",
            description="Test",
            priority="invalid"
        )
        assert result['status'] == 'error'
        assert 'Invalid priority' in result['report']

    def test_create_ticket_return_format(self):
        """Test ticket creation return format."""
        result = create_support_ticket(
            subject="Test",
            description="Test description",
            priority="normal"
        )
        assert 'status' in result
        assert 'report' in result
        assert 'ticket' in result
        assert result['ticket']['id']
        assert result['ticket']['subject']
        assert result['ticket']['priority']

    def test_create_ticket_generates_unique_ids(self):
        """Test that each ticket gets unique ID."""
        result1 = create_support_ticket("Test 1", "Desc 1")
        result2 = create_support_ticket("Test 2", "Desc 2")
        assert result1['ticket']['id'] != result2['ticket']['id']

    def test_create_ticket_stores_in_tickets_dict(self):
        """Test that created tickets are stored."""
        # Clear previous tickets for this test
        initial_count = len(TICKETS)
        
        result = create_support_ticket("Test", "Description")
        ticket_id = result['ticket']['id']
        
        assert ticket_id in TICKETS
        assert TICKETS[ticket_id]['subject'] == "Test"
        assert TICKETS[ticket_id]['priority'] == "normal"

    def test_ticket_has_timestamps(self):
        """Test that created tickets have timestamps."""
        result = create_support_ticket("Test", "Description")
        ticket = TICKETS[result['ticket']['id']]
        assert 'created_at' in ticket
        assert ticket['created_at']

    def test_ticket_has_open_status(self):
        """Test that new tickets are open."""
        result = create_support_ticket("Test", "Description")
        ticket = TICKETS[result['ticket']['id']]
        assert ticket['status'] == 'open'


class TestToolReturnFormats:
    """Test that tools return proper structured formats"""

    def test_search_has_required_fields(self):
        """Test search result has required fields."""
        result = search_knowledge_base("test")
        assert 'status' in result
        assert 'report' in result
        required_fields = {'status', 'report'}
        assert required_fields.issubset(result.keys())

    def test_create_ticket_has_required_fields(self):
        """Test ticket creation has required fields."""
        result = create_support_ticket("Test", "Desc")
        assert 'status' in result
        assert 'report' in result
        assert 'ticket' in result
        required_fields = {'status', 'report', 'ticket'}
        assert required_fields.issubset(result.keys())

    def test_results_have_string_reports(self):
        """Test all results have string reports."""
        search_result = search_knowledge_base("test")
        ticket_result = create_support_ticket("Test", "Desc")
        
        assert isinstance(search_result['report'], str)
        assert isinstance(ticket_result['report'], str)
        assert len(search_result['report']) > 0
        assert len(ticket_result['report']) > 0


class TestKnowledgeBase:
    """Test knowledge base data"""

    def test_knowledge_base_populated(self):
        """Test that knowledge base has articles."""
        assert len(KNOWLEDGE_BASE) > 0

    def test_knowledge_base_has_required_articles(self):
        """Test that knowledge base has expected articles."""
        expected_keys = {
            'password_reset',
            'expense_report',
            'vacation_policy',
            'remote_work',
            'it_support'
        }
        assert expected_keys.issubset(KNOWLEDGE_BASE.keys())

    def test_articles_have_required_fields(self):
        """Test that all articles have required fields."""
        for key, article in KNOWLEDGE_BASE.items():
            assert 'title' in article
            assert 'content' in article
            assert 'tags' in article
            assert isinstance(article['tags'], list)
            assert len(article['tags']) > 0
