# Tutorial 20: YAML Configuration - Customer Support Tools
# Tool implementations for the customer support system
# These functions are referenced by name in root_agent.yaml

from typing import Dict, Any


def check_customer_status(customer_id: str) -> Dict[str, Any]:
    """
    Check if customer is premium member.

    Args:
        customer_id: Customer identifier

    Returns:
        Dict with status, report, and customer tier information
    """
    # Simulated lookup - in production, would query database
    premium_customers = ['CUST-001', 'CUST-003', 'CUST-005']

    is_premium = customer_id in premium_customers
    tier = 'premium' if is_premium else 'standard'

    return {
        'status': 'success',
        'report': f'Customer {customer_id} is {tier} member',
        'data': {
            'customer_id': customer_id,
            'tier': tier,
            'is_premium': is_premium
        }
    }


def log_interaction(customer_id: str, interaction_type: str, summary: str) -> Dict[str, Any]:
    """
    Log customer interaction for records.

    Args:
        customer_id: Customer identifier
        interaction_type: Type of interaction (inquiry, complaint, etc.)
        summary: Brief summary of the interaction

    Returns:
        Dict with status and confirmation
    """
    # In production, would log to database or CRM system
    print(f"[LOG] {customer_id} - {interaction_type}: {summary}")

    return {
        'status': 'success',
        'report': 'Interaction logged successfully',
        'data': {
            'customer_id': customer_id,
            'interaction_type': interaction_type,
            'summary': summary,
            'timestamp': '2025-10-13T10:00:00Z'  # Would be actual timestamp
        }
    }


def get_order_status(order_id: str) -> Dict[str, Any]:
    """
    Get status of an order by ID.

    Args:
        order_id: Order identifier

    Returns:
        Dict with order status information
    """
    # Simulated order lookup - in production, would query order database
    orders = {
        'ORD-001': {'status': 'shipped', 'date': '2025-10-08'},
        'ORD-002': {'status': 'processing', 'date': '2025-10-10'},
        'ORD-003': {'status': 'delivered', 'date': '2025-10-07'},
        'ORD-004': {'status': 'cancelled', 'date': '2025-10-09'}
    }

    order = orders.get(order_id)
    if not order:
        return {
            'status': 'error',
            'error': f'Order {order_id} not found',
            'report': f'No order found with ID {order_id}'
        }

    return {
        'status': 'success',
        'report': f'Order {order_id} status: {order["status"]}',
        'data': {
            'order_id': order_id,
            'status': order['status'],
            'order_date': order['date']
        }
    }


def track_shipment(order_id: str) -> Dict[str, Any]:
    """
    Get shipment tracking information.

    Args:
        order_id: Order identifier

    Returns:
        Dict with tracking information
    """
    # Simulated tracking lookup - in production, would query shipping API
    tracking = {
        'ORD-001': {
            'carrier': 'UPS',
            'tracking_number': '1Z999AA10123456784',
            'estimated_delivery': '2025-10-10',
            'status': 'In transit'
        },
        'ORD-003': {
            'carrier': 'FedEx',
            'tracking_number': '7898765432109',
            'estimated_delivery': 'Delivered on 2025-10-07',
            'status': 'Delivered'
        }
    }

    info = tracking.get(order_id)
    if not info:
        return {
            'status': 'error',
            'error': f'No tracking available for order {order_id}',
            'report': f'No tracking information found for {order_id}'
        }

    return {
        'status': 'success',
        'report': f'Tracking: {info["carrier"]} {info["tracking_number"]}, ETA: {info["estimated_delivery"]}',
        'data': {
            'order_id': order_id,
            'carrier': info['carrier'],
            'tracking_number': info['tracking_number'],
            'estimated_delivery': info['estimated_delivery'],
            'status': info['status']
        }
    }


def cancel_order(order_id: str, reason: str) -> Dict[str, Any]:
    """
    Cancel an order (requires authorization).

    Args:
        order_id: Order identifier
        reason: Reason for cancellation

    Returns:
        Dict with cancellation status
    """
    # Simulated order cancellation - in production, would have authorization checks
    cancellable_orders = ['ORD-001', 'ORD-002']  # Only processing/shipped orders can be cancelled

    if order_id not in cancellable_orders:
        return {
            'status': 'error',
            'error': f'Order {order_id} cannot be cancelled',
            'report': f'Order {order_id} is not eligible for cancellation'
        }

    return {
        'status': 'success',
        'report': f'Order {order_id} cancelled. Reason: {reason}',
        'data': {
            'order_id': order_id,
            'reason': reason,
            'refund_status': 'pending',
            'cancelled_at': '2025-10-13T10:00:00Z'
        }
    }


def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Search technical documentation.

    Args:
        query: Search query

    Returns:
        Dict with relevant documentation
    """
    # Simulated knowledge base search - in production, would query documentation system
    kb = {
        'login': 'To reset password, go to Settings > Security > Reset Password',
        'connection': 'Check internet connection and restart the app',
        'error': 'Clear app cache: Settings > Apps > Clear Cache',
        'update': 'Go to Settings > Updates > Check for Updates',
        'sync': 'Ensure device is connected and try Settings > Sync > Sync Now'
    }

    query_lower = query.lower()
    results = []

    for key, value in kb.items():
        if key in query_lower:
            results.append({
                'topic': key,
                'solution': value
            })

    if not results:
        return {
            'status': 'success',
            'report': 'No matching article found',
            'data': {
                'query': query,
                'results': [],
                'suggestion': 'Try searching for: login, connection, error, update, sync'
            }
        }

    return {
        'status': 'success',
        'report': f'Found {len(results)} relevant article(s)',
        'data': {
            'query': query,
            'results': results
        }
    }


def run_diagnostic(issue_type: str) -> Dict[str, Any]:
    """
    Run diagnostic tests.

    Args:
        issue_type: Type of issue to diagnose

    Returns:
        Dict with diagnostic results
    """
    # Simulated diagnostic - in production, would run actual diagnostic tests
    diagnostics = {
        'connection': {
            'tests': ['Network connectivity', 'Server response', 'DNS resolution'],
            'result': 'All systems operational',
            'recommendation': 'Clear cache and restart'
        },
        'performance': {
            'tests': ['Memory usage', 'CPU usage', 'Disk space'],
            'result': 'Performance within normal range',
            'recommendation': 'Close unused applications'
        },
        'login': {
            'tests': ['Authentication service', 'Session management', 'Password validation'],
            'result': 'Authentication systems operational',
            'recommendation': 'Check password and try again'
        }
    }

    diagnostic = diagnostics.get(issue_type.lower())
    if not diagnostic:
        return {
            'status': 'error',
            'error': f'Unknown issue type: {issue_type}',
            'report': f'No diagnostic available for {issue_type}'
        }

    return {
        'status': 'success',
        'report': f'Diagnostic for {issue_type}: {diagnostic["result"]}. Suggested: {diagnostic["recommendation"]}',
        'data': {
            'issue_type': issue_type,
            'tests_run': diagnostic['tests'],
            'result': diagnostic['result'],
            'recommendation': diagnostic['recommendation']
        }
    }


def create_ticket(customer_id: str, issue: str, priority: str) -> Dict[str, Any]:
    """
    Create support ticket for escalation.

    Args:
        customer_id: Customer identifier
        issue: Description of the issue
        priority: Priority level (low, medium, high, urgent)

    Returns:
        Dict with ticket information
    """
    # Simulated ticket creation - in production, would create in ticketing system
    import random
    ticket_id = f"TKT-{random.randint(1000, 9999):04d}"

    valid_priorities = ['low', 'medium', 'high', 'urgent']
    if priority.lower() not in valid_priorities:
        priority = 'medium'  # Default to medium

    return {
        'status': 'success',
        'report': f'Support ticket {ticket_id} created with {priority} priority',
        'data': {
            'ticket_id': ticket_id,
            'customer_id': customer_id,
            'issue': issue,
            'priority': priority,
            'status': 'open',
            'created_at': '2025-10-13T10:00:00Z',
            'estimated_response': '2 hours' if priority in ['high', 'urgent'] else '24 hours'
        }
    }


def get_billing_history(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve billing history.

    Args:
        customer_id: Customer identifier

    Returns:
        Dict with billing history
    """
    # Simulated billing lookup - in production, would query billing database
    billing_history = {
        'CUST-001': [
            {'date': '2025-09-01', 'amount': 49.99, 'description': 'Monthly subscription'},
            {'date': '2025-08-01', 'amount': 49.99, 'description': 'Monthly subscription'},
            {'date': '2025-07-15', 'amount': 29.99, 'description': 'One-time purchase'}
        ],
        'CUST-002': [
            {'date': '2025-09-15', 'amount': 19.99, 'description': 'Basic plan'},
            {'date': '2025-08-15', 'amount': 19.99, 'description': 'Basic plan'}
        ]
    }

    history = billing_history.get(customer_id, [])

    if not history:
        return {
            'status': 'error',
            'error': f'No billing history found for {customer_id}',
            'report': f'No billing records found for customer {customer_id}'
        }

    total = sum(item['amount'] for item in history)

    return {
        'status': 'success',
        'report': f'Found {len(history)} billing records for {customer_id}',
        'data': {
            'customer_id': customer_id,
            'transactions': history,
            'total_amount': total,
            'currency': 'USD'
        }
    }


def process_refund(order_id: str, amount: float) -> Dict[str, Any]:
    """
    Process refund (requires approval for amounts > $100).

    Args:
        order_id: Order identifier
        amount: Refund amount

    Returns:
        Dict with refund status
    """
    if amount > 100:
        return {
            'status': 'error',
            'error': 'REQUIRES_APPROVAL',
            'report': f'Refund of ${amount} for {order_id} needs manager approval',
            'data': {
                'order_id': order_id,
                'amount': amount,
                'status': 'pending_approval',
                'approval_required': True
            }
        }

    return {
        'status': 'success',
        'report': f'Refund of ${amount} approved for {order_id}. Funds will appear in 3-5 business days.',
        'data': {
            'order_id': order_id,
            'amount': amount,
            'status': 'approved',
            'processing_time': '3-5 business days',
            'refund_id': f'REF-{order_id}-{amount:.0f}'
        }
    }


def update_payment_method(customer_id: str, payment_type: str) -> Dict[str, Any]:
    """
    Update stored payment method.

    Args:
        customer_id: Customer identifier
        payment_type: New payment method type

    Returns:
        Dict with update confirmation
    """
    # Simulated payment method update - in production, would update payment system
    valid_types = ['credit_card', 'debit_card', 'paypal', 'bank_transfer']

    if payment_type.lower() not in valid_types:
        return {
            'status': 'error',
            'error': f'Invalid payment type: {payment_type}',
            'report': f'Payment type must be one of: {", ".join(valid_types)}'
        }

    return {
        'status': 'success',
        'report': f'Payment method for {customer_id} updated to {payment_type}',
        'data': {
            'customer_id': customer_id,
            'payment_type': payment_type,
            'updated_at': '2025-10-13T10:00:00Z',
            'verification_required': True,
            'status': 'pending_verification'
        }
    }