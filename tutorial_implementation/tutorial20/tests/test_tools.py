# Tutorial 20: YAML Configuration - Tool Tests
# Validates tool function implementations

import pytest
from customer_support.tools.customer_tools import (
    check_customer_status,
    log_interaction,
    get_order_status,
    track_shipment,
    cancel_order,
    search_knowledge_base,
    run_diagnostic,
    create_ticket,
    get_billing_history,
    process_refund,
    update_payment_method,
)


class TestCustomerTools:
    """Test customer-related tool functions."""

    def test_check_customer_status_premium(self):
        """Test checking premium customer status."""
        result = check_customer_status('CUST-001')

        assert result['status'] == 'success'
        assert 'premium' in result['report']
        assert result['data']['tier'] == 'premium'
        assert result['data']['is_premium'] is True

    def test_check_customer_status_standard(self):
        """Test checking standard customer status."""
        result = check_customer_status('CUST-999')

        assert result['status'] == 'success'
        assert 'standard' in result['report']
        assert result['data']['tier'] == 'standard'
        assert result['data']['is_premium'] is False

    def test_log_interaction(self):
        """Test logging customer interaction."""
        result = log_interaction('CUST-001', 'inquiry', 'Asked about order status')

        assert result['status'] == 'success'
        assert 'logged successfully' in result['report']
        assert result['data']['customer_id'] == 'CUST-001'
        assert result['data']['interaction_type'] == 'inquiry'


class TestOrderTools:
    """Test order-related tool functions."""

    def test_get_order_status_found(self):
        """Test getting status of existing order."""
        result = get_order_status('ORD-001')

        assert result['status'] == 'success'
        assert 'shipped' in result['report']
        assert result['data']['status'] == 'shipped'

    def test_get_order_status_not_found(self):
        """Test getting status of non-existent order."""
        result = get_order_status('ORD-999')

        assert result['status'] == 'error'
        assert 'No order found with ID' in result['report']

    def test_track_shipment_found(self):
        """Test tracking existing shipment."""
        result = track_shipment('ORD-001')

        assert result['status'] == 'success'
        assert 'UPS' in result['report']
        assert result['data']['carrier'] == 'UPS'

    def test_track_shipment_not_found(self):
        """Test tracking non-existent shipment."""
        result = track_shipment('ORD-999')

        assert result['status'] == 'error'
        assert 'No tracking information found' in result['report']

    def test_cancel_order_success(self):
        """Test cancelling eligible order."""
        result = cancel_order('ORD-001', 'Changed mind')

        assert result['status'] == 'success'
        assert 'cancelled' in result['report']
        assert result['data']['reason'] == 'Changed mind'

    def test_cancel_order_ineligible(self):
        """Test cancelling ineligible order."""
        result = cancel_order('ORD-004', 'Order already cancelled')

        assert result['status'] == 'error'
        assert 'not eligible for cancellation' in result['report']


class TestTechnicalTools:
    """Test technical support tool functions."""

    def test_search_knowledge_base_found(self):
        """Test searching knowledge base with matching query."""
        result = search_knowledge_base('login issue')

        assert result['status'] == 'success'
        assert len(result['data']['results']) > 0
        assert 'login' in result['data']['results'][0]['topic']

    def test_search_knowledge_base_not_found(self):
        """Test searching knowledge base with no matches."""
        result = search_knowledge_base('quantum physics')

        assert result['status'] == 'success'
        assert len(result['data']['results']) == 0
        assert 'No matching article found' in result['report']

    def test_run_diagnostic_known_issue(self):
        """Test running diagnostic for known issue type."""
        result = run_diagnostic('connection')

        assert result['status'] == 'success'
        assert 'All systems operational' in result['report']
        assert result['data']['issue_type'] == 'connection'

    def test_run_diagnostic_unknown_issue(self):
        """Test running diagnostic for unknown issue type."""
        result = run_diagnostic('unknown_problem')

        assert result['status'] == 'error'
        assert 'No diagnostic available' in result['report']

    def test_create_ticket(self):
        """Test creating support ticket."""
        result = create_ticket('CUST-001', 'App crashes on startup', 'high')

        assert result['status'] == 'success'
        assert 'created with high priority' in result['report']
        assert result['data']['priority'] == 'high'
        assert 'ticket_id' in result['data']


class TestBillingTools:
    """Test billing-related tool functions."""

    def test_get_billing_history_found(self):
        """Test getting billing history for existing customer."""
        result = get_billing_history('CUST-001')

        assert result['status'] == 'success'
        assert len(result['data']['transactions']) > 0
        assert result['data']['total_amount'] > 0

    def test_get_billing_history_not_found(self):
        """Test getting billing history for non-existent customer."""
        result = get_billing_history('CUST-999')

        assert result['status'] == 'error'
        assert 'No billing records found' in result['report']

    def test_process_refund_small_amount(self):
        """Test processing small refund."""
        result = process_refund('ORD-001', 50.00)

        assert result['status'] == 'success'
        assert 'approved' in result['report']
        assert result['data']['status'] == 'approved'

    def test_process_refund_large_amount(self):
        """Test processing large refund requiring approval."""
        result = process_refund('ORD-001', 150.00)

        assert result['status'] == 'error'
        assert 'REQUIRES_APPROVAL' in result['error']
        assert 'needs manager approval' in result['report']

    def test_update_payment_method_valid(self):
        """Test updating to valid payment method."""
        result = update_payment_method('CUST-001', 'paypal')

        assert result['status'] == 'success'
        assert 'updated to paypal' in result['report']
        assert result['data']['payment_type'] == 'paypal'

    def test_update_payment_method_invalid(self):
        """Test updating to invalid payment method."""
        result = update_payment_method('CUST-001', 'cryptocurrency')

        assert result['status'] == 'error'
        assert 'Payment type must be one of:' in result['report']


class TestToolReturnFormats:
    """Test that all tools return proper format."""

    def test_all_tools_return_dict(self):
        """Test that all tools return dictionary objects."""
        tools = [
            lambda: check_customer_status('CUST-001'),
            lambda: log_interaction('CUST-001', 'test', 'test'),
            lambda: get_order_status('ORD-001'),
            lambda: track_shipment('ORD-001'),
            lambda: cancel_order('ORD-001', 'test'),
            lambda: search_knowledge_base('login'),
            lambda: run_diagnostic('connection'),
            lambda: create_ticket('CUST-001', 'test', 'medium'),
            lambda: get_billing_history('CUST-001'),
            lambda: process_refund('ORD-001', 10.00),
            lambda: update_payment_method('CUST-001', 'credit_card'),
        ]

        for tool_func in tools:
            result = tool_func()
            assert isinstance(result, dict), f"Tool {tool_func.__name__} should return dict"

    def test_tools_have_required_fields(self):
        """Test that tools return required fields."""
        result = check_customer_status('CUST-001')

        assert 'status' in result
        assert 'report' in result
        assert 'data' in result

        assert result['status'] in ['success', 'error']

    def test_error_responses_have_error_field(self):
        """Test that error responses include error field."""
        result = get_order_status('ORD-999')  # Non-existent order

        assert result['status'] == 'error'
        assert 'error' in result
        assert len(result['error']) > 0