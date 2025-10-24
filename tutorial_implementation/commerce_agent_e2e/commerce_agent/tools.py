"""
Custom tools for Commerce Agent.
Implements preference management and product curation.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime

from .models import (
    UserPreferences,
    PriceRange,
    InteractionRecord,
    UserFavorite,
    EngagementProfile,
    Product,
    ToolResponse,
)
from .database import (
    get_user_preferences,
    save_user_preferences,
    add_interaction,
    get_user_history,
    add_favorite,
    get_user_favorites,
    get_cached_results,
    cache_search_results,
    get_engagement_profile,
    init_database,
)


def manage_user_preferences(
    action: str,
    user_id: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Manage user preferences with database persistence.
    
    Actions:
    - 'get': Retrieve current user preferences
    - 'update': Update user preferences (sports, price_range, brands)
    - 'add_history': Add interaction to user history
    - 'get_history': Get user interaction history
    - 'add_favorite': Add product to favorites
    - 'get_favorites': Get user's favorite products
    - 'get_profile': Get user engagement profile
    
    Args:
        action: The operation to perform
        user_id: The user identifier
        data: Action-specific data
    
    Returns:
        ToolResponse with status, report, and data
    """
    try:
        init_database()  # Ensure tables exist
        
        if action == "get":
            prefs = get_user_preferences(user_id)
            if prefs:
                return {
                    "status": "success",
                    "report": f"Retrieved preferences for user {user_id}",
                    "data": {"preferences": prefs.model_dump()}
                }
            else:
                # Return default preferences
                default_prefs = UserPreferences()
                return {
                    "status": "success",
                    "report": f"No preferences found for user {user_id}, returning defaults",
                    "data": {"preferences": default_prefs.model_dump()}
                }
        
        elif action == "update":
            if not data:
                raise ValueError("data required for update action")
            
            # Get existing or create new
            existing = get_user_preferences(user_id)
            if existing:
                updated_prefs = existing.model_copy(update=data)
            else:
                updated_prefs = UserPreferences(**data)
            
            save_user_preferences(user_id, updated_prefs)
            
            return {
                "status": "success",
                "report": f"Updated preferences for user {user_id}",
                "data": {"preferences": updated_prefs.model_dump()}
            }
        
        elif action == "add_history":
            if not data or "query" not in data or "session_id" not in data:
                raise ValueError("data must contain 'query' and 'session_id'")
            
            record = InteractionRecord(
                user_id=user_id,
                session_id=data["session_id"],
                query=data["query"],
                result_count=data.get("result_count", 0),
                products_found=data.get("products_found", [])
            )
            add_interaction(record)
            
            return {
                "status": "success",
                "report": f"Added interaction to history for user {user_id}",
                "data": {"interaction": record.model_dump()}
            }
        
        elif action == "get_history":
            history = get_user_history(user_id, limit=data.get("limit", 10) if data else 10)
            
            return {
                "status": "success",
                "report": f"Retrieved {len(history)} interactions for user {user_id}",
                "data": {"history": [h.model_dump() for h in history]}
            }
        
        elif action == "add_favorite":
            if not data or "product_id" not in data:
                raise ValueError("data must contain 'product_id' and 'product_name'")
            
            favorite = UserFavorite(
                user_id=user_id,
                product_id=data["product_id"],
                product_name=data.get("product_name", "Unknown Product"),
                url=data.get("url")
            )
            add_favorite(favorite)
            
            return {
                "status": "success",
                "report": f"Added {favorite.product_name} to favorites",
                "data": {"favorite": favorite.model_dump()}
            }
        
        elif action == "get_favorites":
            favorites = get_user_favorites(user_id)
            
            return {
                "status": "success",
                "report": f"Retrieved {len(favorites)} favorite products",
                "data": {"favorites": [f.model_dump() for f in favorites]}
            }
        
        elif action == "get_profile":
            profile = get_engagement_profile(user_id)
            
            return {
                "status": "success",
                "report": f"Retrieved engagement profile for user {user_id}",
                "data": {"profile": profile.model_dump()}
            }
        
        else:
            raise ValueError(f"Unknown action: {action}")
    
    except Exception as e:
        return {
            "status": "error",
            "report": f"Preference management failed: {str(e)}",
            "error": str(e),
            "data": None
        }


def curate_products(
    products: List[Dict[str, Any]],
    user_preferences: Optional[Dict[str, Any]] = None,
    limit: int = 3
) -> Dict[str, Any]:
    """
    Curate product recommendations based on user preferences and history.
    
    Args:
        products: List of product dicts from search results
        user_preferences: User preference dict with sports, price_range, brands
        limit: Number of products to return
    
    Returns:
        ToolResponse with curated products
    """
    try:
        if not products:
            return {
                "status": "success",
                "report": "No products to curate",
                "data": {"curated_products": []}
            }
        
        # Convert to Product objects
        product_objects = []
        for p in products:
            try:
                product_objects.append(Product(**p))
            except Exception:
                # Skip malformed products
                continue
        
        if not product_objects:
            return {
                "status": "success",
                "report": "No valid products to curate",
                "data": {"curated_products": []}
            }
        
        # Apply preference filters if available
        if user_preferences:
            prefs = UserPreferences(**user_preferences)
            
            # Filter by price range
            filtered = [
                p for p in product_objects
                if prefs.price_range.min_price <= p.price <= prefs.price_range.max_price
            ]
            
            # Prioritize by brand preference
            if prefs.brands:
                brand_matches = [p for p in filtered if p.brand in prefs.brands]
                other = [p for p in filtered if p.brand not in prefs.brands]
                filtered = brand_matches + other
            
            # Prioritize by category/sport
            if prefs.sports:
                category_matches = [p for p in filtered if p.category in prefs.sports]
                other = [p for p in filtered if p.category not in prefs.sports]
                filtered = category_matches + other
            
            product_objects = filtered
        
        # Sort by rating if available, then by price
        product_objects.sort(
            key=lambda p: (-p.rating if p.rating else 0, p.price),
            reverse=True
        )
        
        # Return top N
        curated = product_objects[:limit]
        
        return {
            "status": "success",
            "report": f"Curated {len(curated)} products from {len(products)} results",
            "data": {"curated_products": [p.model_dump() for p in curated]}
        }
    
    except Exception as e:
        return {
            "status": "error",
            "report": f"Product curation failed: {str(e)}",
            "error": str(e),
            "data": None
        }


def generate_product_narrative(
    product: Dict[str, Any],
    user_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Generate an engaging narrative around a product recommendation.
    This is called by the Storyteller agent for context enrichment.
    
    Args:
        product: Product dict with name, category, description
        user_context: User's interests and preferences for personalization
    
    Returns:
        ToolResponse with narrative
    """
    try:
        if not product or "name" not in product:
            return {
                "status": "error",
                "report": "Invalid product data",
                "error": "Missing product name",
                "data": None
            }
        
        product_obj = Product(**product)
        
        # This is a simple template - the Storyteller agent does actual generation
        template = f"""
        Discover the {product_obj.name}
        
        Category: {product_obj.category or 'General'}
        Price: €{product_obj.price}
        Brand: {product_obj.brand or 'Unknown'}
        """
        
        # Add personalization if context available
        if user_context and user_context.get("sports"):
            sports = user_context["sports"]
            template += f"\nPerfect for: {', '.join(sports)}"
        
        return {
            "status": "success",
            "report": f"Generated narrative for {product_obj.name}",
            "data": {
                "product_id": product_obj.product_id,
                "product_name": product_obj.name,
                "narrative_template": template
            }
        }
    
    except Exception as e:
        return {
            "status": "error",
            "report": f"Narrative generation failed: {str(e)}",
            "error": str(e),
            "data": None
        }
