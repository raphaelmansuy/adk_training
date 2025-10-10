"""
Tutorial 18: Events and Observability
Customer Service Agent with Comprehensive Event Tracking

This module demonstrates:
- Event tracking and logging
- Metrics collection
- Real-time monitoring
- Escalation handling
- State management with EventActions

Based on Google ADK official Event and EventActions implementation.
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import Session, InMemorySessionService
from google.adk.events import Event, EventActions
from google.genai import types


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CustomerServiceMonitor:
    """Customer service agent with comprehensive event monitoring.
    
    Features:
    - Event tracking for all interactions
    - Tool call logging
    - Escalation handling
    - Metrics collection
    - Detailed reporting
    """

    def __init__(self):
        """Initialize customer service monitoring system."""
        
        # Event log storage
        self.events: List[Dict[str, Any]] = []
        
        # Create tools with event tracking
        
        def check_order_status(order_id: str) -> Dict[str, Any]:
            """
            Check order status.
            
            Args:
                order_id: Order identifier (e.g., 'ORD-001')
                
            Returns:
                Dict with status, report, and order details
            """
            self._log_tool_call('check_order_status', {'order_id': order_id})
            
            # Simulated order lookup
            order_statuses = {
                'ORD-001': 'shipped',
                'ORD-002': 'processing',
                'ORD-003': 'delivered'
            }
            
            status = order_statuses.get(order_id, 'not_found')
            
            if status == 'not_found':
                return {
                    'status': 'error',
                    'report': f'Order {order_id} not found',
                    'order_id': order_id,
                    'order_status': None
                }
            
            return {
                'status': 'success',
                'report': f'Order {order_id} status: {status}',
                'order_id': order_id,
                'order_status': status
            }
        
        def process_refund(order_id: str, amount: float) -> Dict[str, Any]:
            """
            Process refund request.
            
            Args:
                order_id: Order identifier
                amount: Refund amount
                
            Returns:
                Dict with status, report, and refund details
            """
            self._log_tool_call('process_refund', {
                'order_id': order_id,
                'amount': amount
            })
            
            # Escalate for amounts > 100
            if amount > 100:
                return {
                    'status': 'requires_approval',
                    'report': f'ESCALATE: Refund of ${amount} exceeds approval threshold',
                    'order_id': order_id,
                    'amount': amount,
                    'requires_approval': True
                }
            
            return {
                'status': 'success',
                'report': f'Refund of ${amount} approved for order {order_id}',
                'order_id': order_id,
                'amount': amount,
                'approved': True
            }
        
        def check_inventory(product_id: str) -> Dict[str, Any]:
            """
            Check product inventory.
            
            Args:
                product_id: Product identifier (e.g., 'PROD-A')
                
            Returns:
                Dict with status, report, and inventory details
            """
            self._log_tool_call('check_inventory', {'product_id': product_id})
            
            # Simulated inventory check
            inventory_levels = {
                'PROD-A': 150,
                'PROD-B': 5,
                'PROD-C': 0
            }
            
            inventory = inventory_levels.get(product_id, 0)
            
            return {
                'status': 'success',
                'report': f'Product {product_id} inventory: {inventory} units',
                'product_id': product_id,
                'inventory': inventory,
                'in_stock': inventory > 0
            }
        
        # Customer service agent
        self.agent = Agent(
            model='gemini-2.0-flash-exp',
            name='customer_service',
            description='Customer service agent with event tracking',
            instruction="""
You are a customer service agent helping customers with:
- Order status inquiries
- Refund requests
- Inventory checks
- General questions

Guidelines:
1. Always be polite and helpful
2. Use tools to get accurate information
3. For refunds > $100, explain that supervisor approval is required
4. Track all interactions
5. Log important decisions

Tools available:
- check_order_status: Get order status by order ID
- process_refund: Process refund (escalate if > $100)
- check_inventory: Check product availability by product ID

Always call the appropriate tool to get accurate information.
            """.strip(),
            tools=[
                check_order_status,
                process_refund,
                check_inventory
            ],
            generate_content_config=types.GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=1024
            )
        )
        
        # Create runner with session service
        session_service = InMemorySessionService()
        self.runner = Runner(
            app_name="observability_agent",
            agent=self.agent,
            session_service=session_service
        )
        self.session_service = session_service

    def _log_tool_call(self, tool_name: str, args: Dict[str, Any]):
        """Log tool invocation."""
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'tool_call',
            'tool': tool_name,
            'arguments': args
        })
        logger.info(f"Tool called: {tool_name} with args: {args}")

    def _log_agent_event(self, event_type: str, data: Dict[str, Any]):
        """Log agent event."""
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': data
        })
        logger.info(f"Agent event: {event_type} - {data}")

    async def handle_customer_query(
        self, 
        customer_id: str, 
        query: str
    ) -> Any:
        """
        Handle customer query with full event tracking.

        Args:
            customer_id: Customer identifier
            query: Customer query

        Returns:
            Agent response
        """
        
        print(f"\n{'='*70}")
        print(f"CUSTOMER: {customer_id}")
        print(f"QUERY: {query}")
        print(f"{'='*70}\n")

        # Log query event
        self._log_agent_event('customer_query', {
            'customer_id': customer_id,
            'query': query
        })

        # Create session with customer context
        session = await self.session_service.create_session(
            app_name="observability_agent",
            user_id=customer_id
        )
        
        # Set session state
        session.state['customer_id'] = customer_id
        session.state['query_time'] = datetime.now().isoformat()
        session.state['query_count'] = session.state.get('query_count', 0) + 1

        # Execute agent with proper run_async signature
        result_event = None
        async for event in self.runner.run_async(
            user_id=customer_id,
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)])
        ):
            result_event = event
            if event.turn_complete:
                break
        
        # Use the final event as result
        result = result_event if result_event else None

        # Log response
        response_text = ""
        if result and result.content and result.content.parts:
            response_text = result.content.parts[0].text

        self._log_agent_event('agent_response', {
            'customer_id': customer_id,
            'response': response_text
        })

        # Check for escalation
        if 'ESCALATE' in response_text or 'requires approval' in response_text.lower():
            self._log_agent_event('escalation', {
                'customer_id': customer_id,
                'reason': response_text
            })
            print("🚨 ESCALATED TO SUPERVISOR\n")

        print(f"🤖 AGENT RESPONSE:\n{response_text}\n")
        print(f"{'='*70}\n")

        return result

    def get_event_summary(self) -> str:
        """Generate event summary report."""
        
        total_events = len(self.events)
        
        event_types: Dict[str, int] = {}
        for event in self.events:
            event_type = event['type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        tool_calls = [e for e in self.events if e['type'] == 'tool_call']
        escalations = [e for e in self.events if e['type'] == 'escalation']
        
        summary = f"""
EVENT SUMMARY REPORT
{'='*70}

Total Events: {total_events}

Event Types:
"""
        
        for event_type, count in event_types.items():
            summary += f"  - {event_type}: {count}\n"
        
        summary += f"\nTool Calls: {len(tool_calls)}\n"
        
        if tool_calls:
            summary += "  Tools Used:\n"
            tool_usage: Dict[str, int] = {}
            for call in tool_calls:
                tool = call['tool']
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
            
            for tool, count in tool_usage.items():
                summary += f"    - {tool}: {count} calls\n"
        
        summary += f"\nEscalations: {len(escalations)}\n"
        
        if escalations:
            summary += "  Escalation Reasons:\n"
            for esc in escalations:
                summary += f"    - {esc['data']['reason']}\n"
        
        summary += f"\n{'='*70}"
        
        return summary

    def get_detailed_timeline(self) -> str:
        """Get detailed event timeline."""
        
        timeline = f"\nDETAILED EVENT TIMELINE\n{'='*70}\n"
        
        for i, event in enumerate(self.events, 1):
            timeline += f"\n[{i}] {event['timestamp']}\n"
            timeline += f"    Type: {event['type']}\n"
            
            if event['type'] == 'tool_call':
                timeline += f"    Tool: {event['tool']}\n"
                timeline += f"    Args: {event['arguments']}\n"
            elif event['type'] in ['customer_query', 'agent_response', 'escalation']:
                for key, value in event['data'].items():
                    # Truncate long values
                    value_str = str(value)
                    if len(value_str) > 100:
                        value_str = value_str[:97] + "..."
                    timeline += f"    {key}: {value_str}\n"
        
        timeline += f"\n{'='*70}\n"
        
        return timeline


# Observability helper classes

class EventLogger:
    """Custom event logger for structured logging."""

    def __init__(self):
        self.logger = logging.getLogger('agent_events')
        self.logger.setLevel(logging.INFO)

    def log_event(self, event: Event):
        """Log event with structured data."""
        event_data = {
            'invocation_id': event.invocation_id,
            'author': event.author,
            'content': event.content.parts[0].text if event.content and event.content.parts else None,
            'actions': {
                'state_delta': event.actions.state_delta if event.actions else None,
                'escalate': event.actions.escalate if event.actions else None,
                'transfer_to_agent': event.actions.transfer_to_agent if event.actions else None
            }
        }
        self.logger.info(f"Event: {event_data}")


@dataclass
class AgentMetrics:
    """Agent performance metrics."""
    invocation_count: int = 0
    total_latency: float = 0.0
    tool_call_count: int = 0
    error_count: int = 0
    escalation_count: int = 0


class MetricsCollector:
    """Collect agent metrics for monitoring."""

    def __init__(self):
        self.metrics: Dict[str, AgentMetrics] = {}

    def track_invocation(
        self, 
        agent_name: str, 
        latency: float,
        tool_calls: int = 0,
        had_error: bool = False, 
        escalated: bool = False
    ):
        """Track agent invocation metrics."""
        
        if agent_name not in self.metrics:
            self.metrics[agent_name] = AgentMetrics()
        
        m = self.metrics[agent_name]
        m.invocation_count += 1
        m.total_latency += latency
        m.tool_call_count += tool_calls
        
        if had_error:
            m.error_count += 1
        if escalated:
            m.escalation_count += 1

    def get_summary(self, agent_name: str) -> Dict[str, Any]:
        """Get metrics summary for agent."""
        
        if agent_name not in self.metrics:
            return {}
        
        m = self.metrics[agent_name]
        
        return {
            'invocations': m.invocation_count,
            'avg_latency': m.total_latency / m.invocation_count if m.invocation_count > 0 else 0,
            'total_tool_calls': m.tool_call_count,
            'error_rate': m.error_count / m.invocation_count if m.invocation_count > 0 else 0,
            'escalation_rate': m.escalation_count / m.invocation_count if m.invocation_count > 0 else 0
        }


class EventAlerter:
    """Alert on specific event patterns."""

    def __init__(self):
        self.rules: List[tuple[Callable[[Event], bool], Callable[[Event], None]]] = []

    def add_rule(
        self, 
        condition: Callable[[Event], bool],
        alert_fn: Callable[[Event], None]
    ):
        """Add alerting rule."""
        self.rules.append((condition, alert_fn))

    def check_event(self, event: Event):
        """Check event against all rules."""
        for condition, alert_fn in self.rules:
            if condition(event):
                alert_fn(event)


async def main():
    """Main entry point for demo."""
    
    print("\n" + "="*70)
    print("TUTORIAL 18: EVENTS & OBSERVABILITY DEMO")
    print("="*70)
    
    monitor = CustomerServiceMonitor()
    
    # Customer 1: Order status inquiry
    await monitor.handle_customer_query(
        customer_id='CUST-001',
        query='What is the status of my order ORD-001?'
    )
    
    await asyncio.sleep(1)
    
    # Customer 2: Refund request (small amount)
    await monitor.handle_customer_query(
        customer_id='CUST-002',
        query='I want a refund of $50 for order ORD-002'
    )
    
    await asyncio.sleep(1)
    
    # Customer 3: Refund request (large amount - triggers escalation)
    await monitor.handle_customer_query(
        customer_id='CUST-003',
        query='I need a refund of $150 for order ORD-003'
    )
    
    await asyncio.sleep(1)
    
    # Customer 4: Inventory check
    await monitor.handle_customer_query(
        customer_id='CUST-004',
        query='Is product PROD-B in stock?'
    )
    
    # Generate reports
    print("\n" + monitor.get_event_summary())
    print(monitor.get_detailed_timeline())


# Create instance and export root_agent for ADK discovery
_monitor_instance = None

def get_monitor():
    """Get or create CustomerServiceMonitor instance."""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = CustomerServiceMonitor()
    return _monitor_instance

# Export root_agent for ADK discovery
root_agent = get_monitor().agent


if __name__ == '__main__':
    asyncio.run(main())
