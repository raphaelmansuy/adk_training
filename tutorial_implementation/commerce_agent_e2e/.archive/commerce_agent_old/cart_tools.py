"""
Shopping cart management tools.
Handles cart operations, checkout, and order processing.
"""

import logging
import uuid
from typing import Dict, Any, List
from google.adk.tools import ToolContext
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def access_cart(customer_id: str, ctx: ToolContext = None) -> Dict[str, Any]:
    """
    Retrieves current shopping cart contents for a customer.
    
    Args:
        customer_id: Customer identifier
        ctx: Tool context for state management
        
    Returns:
        {
            'status': 'success',
            'cart': {
                'items': [List of CartItem dicts],
                'subtotal': 245.00,
                'tax': 49.00,
                'shipping': 0.00,
                'total': 294.00,
                'currency': 'EUR',
                'item_count': 3,
                'last_modified': '2025-01-26T10:30:00Z'
            }
        }
        
    Example:
        >>> access_cart(customer_id='user123')
        {'status': 'success', 'cart': {...}}
    """
    logger.info(f"Accessing cart for customer: {customer_id}")
    
    try:
        # Get cart from session state or create empty cart
        if ctx and 'cart' in ctx.state:
            cart = ctx.state['cart']
        else:
            cart = {
                'items': [],
                'subtotal': 0.0,
                'tax': 0.0,
                'shipping': 0.0,
                'total': 0.0,
                'currency': 'EUR',
                'item_count': 0,
                'last_modified': datetime.now().isoformat()
            }
            if ctx:
                ctx.state['cart'] = cart
        
        return {
            'status': 'success',
            'cart': cart,
            'message': f"Cart contains {cart['item_count']} items"
        }
        
    except Exception as e:
        logger.error(f"Error accessing cart: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Failed to access cart'
        }


def modify_cart(
    customer_id: str,
    items_to_add: List[Dict[str, Any]] = None,
    items_to_remove: List[str] = None,
    ctx: ToolContext = None
) -> Dict[str, Any]:
    """
    Modifies shopping cart by adding or removing items.
    
    Args:
        customer_id: Customer identifier
        items_to_add: List of items to add with format:
            [
                {
                    'product_id': 'salomon-speedcross-6',
                    'product_name': 'Salomon Speedcross 6',
                    'brand': 'Salomon',
                    'quantity': 1,
                    'unit_price': 175.00,
                    'size': 'EU 42',
                    'color': 'Black',
                    'image_url': '...'
                }
            ]
        items_to_remove: List of product IDs to remove
        ctx: Tool context for state management
        
    Returns:
        CartModificationResult dict with updated cart state
        
    Example:
        >>> modify_cart(
        ...     customer_id='user123',
        ...     items_to_add=[{'product_id': 'shoe-1', 'quantity': 1, 'unit_price': 100.0}]
        ... )
        {'status': 'success', 'message': 'Added 1 item', 'cart': {...}}
    """
    logger.info(f"Modifying cart for customer: {customer_id}")
    
    try:
        # Get current cart
        current_cart = ctx.state.get('cart', {
            'items': [],
            'subtotal': 0.0,
            'tax': 0.0,
            'shipping': 0.0,
            'total': 0.0,
            'currency': 'EUR',
            'item_count': 0,
            'last_modified': datetime.now().isoformat()
        }) if ctx else {
            'items': [],
            'subtotal': 0.0,
            'tax': 0.0,
            'shipping': 0.0,
            'total': 0.0,
            'currency': 'EUR',
            'item_count': 0,
            'last_modified': datetime.now().isoformat()
        }
        
        items_added = []
        items_removed = []
        
        # Remove items
        if items_to_remove:
            current_cart['items'] = [
                item for item in current_cart['items']
                if item['product_id'] not in items_to_remove
            ]
            items_removed = items_to_remove
        
        # Add items
        if items_to_add:
            for new_item in items_to_add:
                # Calculate total price for this item
                total_price = new_item['unit_price'] * new_item.get('quantity', 1)
                
                cart_item = {
                    'product_id': new_item['product_id'],
                    'product_name': new_item.get('product_name', 'Unknown Product'),
                    'brand': new_item.get('brand', 'Unknown'),
                    'quantity': new_item.get('quantity', 1),
                    'unit_price': new_item['unit_price'],
                    'total_price': total_price,
                    'currency': new_item.get('currency', 'EUR'),
                    'size': new_item.get('size'),
                    'color': new_item.get('color'),
                    'image_url': new_item.get('image_url'),
                    'added_at': datetime.now().isoformat()
                }
                
                current_cart['items'].append(cart_item)
                items_added.append(new_item['product_id'])
        
        # Recalculate totals
        subtotal = sum(item['total_price'] for item in current_cart['items'])
        tax = subtotal * 0.20  # 20% VAT
        
        # Calculate shipping (free over €50)
        shipping = 0.0 if subtotal >= 50.0 else 5.95
        
        total = subtotal + tax + shipping
        
        current_cart.update({
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'shipping': round(shipping, 2),
            'total': round(total, 2),
            'item_count': len(current_cart['items']),
            'last_modified': datetime.now().isoformat()
        })
        
        # Update state
        if ctx:
            ctx.state['cart'] = current_cart
        
        return {
            'status': 'success',
            'message': f"Added {len(items_added)} item(s), removed {len(items_removed)} item(s)",
            'cart': current_cart,
            'items_added': items_added,
            'items_removed': items_removed
        }
        
    except Exception as e:
        logger.error(f"Error modifying cart: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Failed to modify cart',
            'cart': current_cart if 'current_cart' in locals() else {},
            'items_added': [],
            'items_removed': []
        }


def process_checkout(
    customer_id: str,
    payment_method: str,
    shipping_address: str,
    ctx: ToolContext = None
) -> Dict[str, Any]:
    """
    Processes checkout and creates order confirmation.
    
    Args:
        customer_id: Customer identifier
        payment_method: Payment method (credit_card, paypal, apple_pay, google_pay)
        shipping_address: Shipping address string
        ctx: Tool context for state management
        
    Returns:
        OrderSummary dict with order confirmation
        
    Example:
        >>> process_checkout(
        ...     customer_id='user123',
        ...     payment_method='credit_card',
        ...     shipping_address='123 Main St, City, Country'
        ... )
        {'status': 'confirmed', 'order_id': 'ORD-...', ...}
    """
    logger.info(f"Processing checkout for customer: {customer_id}")
    
    try:
        # Get cart from state
        cart = ctx.state.get('cart', {}) if ctx else {}
        
        if not cart.get('items'):
            return {
                'status': 'error',
                'error': 'Cart is empty',
                'message': 'Cannot checkout with empty cart'
            }
        
        # Generate order ID
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Calculate estimated delivery (3-5 business days)
        estimated_delivery = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
        
        # Generate tracking number (mock)
        tracking_number = f"TRK-{str(uuid.uuid4())[:12].upper()}"
        
        order_summary = {
            'order_id': order_id,
            'status': 'confirmed',
            'items': cart['items'],
            'subtotal': cart['subtotal'],
            'tax': cart['tax'],
            'shipping': cart['shipping'],
            'total': cart['total'],
            'currency': cart['currency'],
            'payment_method': payment_method,
            'shipping_address': shipping_address,
            'estimated_delivery': estimated_delivery,
            'order_date': datetime.now().isoformat(),
            'tracking_number': tracking_number
        }
        
        # Store order in state
        if ctx:
            if 'orders' not in ctx.state:
                ctx.state['orders'] = []
            ctx.state['orders'].append(order_summary)
            
            # Clear cart after successful checkout
            ctx.state['cart'] = {
                'items': [],
                'subtotal': 0.0,
                'tax': 0.0,
                'shipping': 0.0,
                'total': 0.0,
                'currency': 'EUR',
                'item_count': 0,
                'last_modified': datetime.now().isoformat()
            }
        
        return order_summary
        
    except Exception as e:
        logger.error(f"Error processing checkout: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Failed to process checkout. Please try again.'
        }
