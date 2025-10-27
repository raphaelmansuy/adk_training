"""Enhanced tools for Commerce Agent."""

# Import enhanced tools
from .multimodal_tools import send_video_link, analyze_product_image
from .cart_tools import access_cart, modify_cart, process_checkout

# Import original tools from parent directory tools.py
# This resolves the package/module naming conflict
import sys
from pathlib import Path

# Add parent directory to path temporarily
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

# Import from tools.py module in parent directory
try:
    # Import the tools.py module
    import importlib.util
    _tools_path = _parent_dir / "tools.py"
    _spec = importlib.util.spec_from_file_location("_original_tools", _tools_path)
    _original_tools = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_original_tools)
    
    # Export the functions
    manage_user_preferences = _original_tools.manage_user_preferences
    curate_products = _original_tools.curate_products
    generate_product_narrative = _original_tools.generate_product_narrative
except Exception as e:
    # Fallback - tools not available
    manage_user_preferences = None
    curate_products = None
    generate_product_narrative = None

__all__ = [
    # Enhanced tools
    'send_video_link',
    'analyze_product_image',
    'access_cart',
    'modify_cart',
    'process_checkout',
    # Original tools
    'manage_user_preferences',
    'curate_products',
    'generate_product_narrative',
]

