"""
Callbacks for Commerce Agent

Implements before/after tool callbacks for:
- Logging and debugging
- State persistence
- Performance tracking
- Error handling
"""

import logging
from datetime import datetime
from google.adk.tools import ToolContext
from typing import Any

logger = logging.getLogger(__name__)


def before_agent_callback(ctx: ToolContext) -> None:
    """
    Called before agent execution starts.
    
    Initializes session state and logs session start.
    """
    logger.info(f"Starting agent session: {ctx.session_id}")
    
    # Initialize state structures if not present
    if 'session_start_time' not in ctx.state:
        ctx.state['session_start_time'] = datetime.now().isoformat()
    
    if 'turn_count' not in ctx.state:
        ctx.state['turn_count'] = 0
    
    if 'tool_usage_count' not in ctx.state:
        ctx.state['tool_usage_count'] = 0
    
    # Initialize shopping-specific state
    if 'cart' not in ctx.state:
        ctx.state['cart'] = {
            'items': [],
            'subtotal': 0.0,
            'tax': 0.0,
            'shipping': 0.0,
            'total': 0.0,
            'currency': 'EUR',
            'item_count': 0
        }
    
    if 'user_preferences' not in ctx.state:
        ctx.state['user_preferences'] = {}
    
    if 'search_history' not in ctx.state:
        ctx.state['search_history'] = []
    
    # Increment turn count
    ctx.state['turn_count'] += 1
    
    logger.info(f"Session turn {ctx.state['turn_count']}")


def after_agent_callback(ctx: ToolContext) -> None:
    """
    Called after agent execution completes.
    
    Logs session metrics and persists important state.
    """
    try:
        session_duration = (
            datetime.now() - datetime.fromisoformat(ctx.state.get('session_start_time', datetime.now().isoformat()))
        ).total_seconds()
        
        logger.info(f"Agent session completed")
        logger.info(f"Duration: {session_duration:.2f}s")
        logger.info(f"Turns: {ctx.state.get('turn_count', 0)}")
        logger.info(f"Tools used: {ctx.state.get('tool_usage_count', 0)}")
        
        # Log shopping metrics
        cart_items = ctx.state.get('cart', {}).get('item_count', 0)
        cart_total = ctx.state.get('cart', {}).get('total', 0.0)
        logger.info(f"Cart: {cart_items} items, €{cart_total:.2f}")
        
    except Exception as e:
        logger.error(f"Error in after_agent_callback: {e}")


def before_tool_callback(ctx: ToolContext) -> None:
    """
    Called before tool execution.
    
    Logs tool invocation details.
    """
    logger.info(f"Invoking tool: {ctx.tool_name}")
    logger.debug(f"Tool arguments: {ctx.arguments}")
    
    # Track tool usage
    if 'tool_usage_count' in ctx.state:
        ctx.state['tool_usage_count'] += 1
    
    # Track tool-specific metrics
    if 'tool_usage_by_name' not in ctx.state:
        ctx.state['tool_usage_by_name'] = {}
    
    tool_name = ctx.tool_name
    if tool_name not in ctx.state['tool_usage_by_name']:
        ctx.state['tool_usage_by_name'][tool_name] = 0
    ctx.state['tool_usage_by_name'][tool_name] += 1


def after_tool_callback(ctx: ToolContext) -> None:
    """
    Called after tool execution.
    
    Logs tool results and errors.
    """
    logger.info(f"Tool {ctx.tool_name} completed")
    
    # Check for errors
    if hasattr(ctx, 'result'):
        if isinstance(ctx.result, dict):
            status = ctx.result.get('status')
            if status == 'error':
                logger.warning(f"Tool {ctx.tool_name} returned error: {ctx.result.get('error')}")
            else:
                logger.debug(f"Tool result: {ctx.result}")
    
    # Special handling for cart modifications
    if ctx.tool_name == 'modify_cart':
        if hasattr(ctx, 'result') and isinstance(ctx.result, dict):
            items_added = ctx.result.get('items_added', [])
            items_removed = ctx.result.get('items_removed', [])
            logger.info(f"Cart modified: +{len(items_added)} items, -{len(items_removed)} items")
    
    # Special handling for checkout
    if ctx.tool_name == 'process_checkout':
        if hasattr(ctx, 'result') and isinstance(ctx.result, dict):
            if ctx.result.get('status') == 'confirmed':
                order_id = ctx.result.get('order_id')
                total = ctx.result.get('total', 0.0)
                logger.info(f"Order confirmed: {order_id}, Total: €{total:.2f}")


def rate_limit_callback(ctx: ToolContext) -> None:
    """
    Rate limiting callback (if needed).
    
    Can be used to implement request throttling.
    """
    # Placeholder for rate limiting logic
    pass


# Export callbacks
__all__ = [
    'before_agent_callback',
    'after_agent_callback',
    'before_tool_callback',
    'after_tool_callback',
    'rate_limit_callback',
]
