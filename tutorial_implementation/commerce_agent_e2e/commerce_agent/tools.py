"""
Custom tools for Commerce Agent.
Implements preference management, product curation, and citation validation.

These tools enhance the commerce agent with:
- User preference tracking and personalization
- Product recommendation curation based on preferences
- Citation validation to prevent URL hallucination
- Grounding metadata verification
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from .models import (
    UserPreferences,
    InteractionRecord,
    UserFavorite,
    Product,
)
from .database import (
    get_user_preferences,
    save_user_preferences,
    add_interaction,
    get_user_history,
    add_favorite,
    get_user_favorites,
    get_engagement_profile,
    init_database,
)

logger = logging.getLogger(__name__)


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


def validate_citations(
    product: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validate product citations and grounding metadata.
    
    Checks:
    1. All URLs are from known retailer domains
    2. URLs match their source domains
    3. No fabricated URL patterns detected
    4. Grounding metadata is present
    5. Source citations exist for all URLs
    
    Args:
        product: Product dict with source_citations and grounding metadata
    
    Returns:
        ToolResponse with validation results
    """
    try:
        if not product:
            return {
                "status": "error",
                "report": "Invalid product data",
                "error": "Product cannot be empty",
                "data": None
            }
        
        product_obj = Product(**product)
        issues = []
        warnings = []
        
        # Check 1: URL validity
        if product_obj.url:
            from urllib.parse import urlparse
            try:
                parsed = urlparse(product_obj.url)
                domain = parsed.netloc
                
                # Whitelist of known retailer domains
                known_domains = [
                    "decathlon.com.hk",
                    "nike.com",
                    "adidas.com",
                    "intersport.com",
                    "amazon.com",
                    "ebay.com",
                    "sports-direct.com",
                    "rei.com",
                    "thenorthface.com",
                ]
                
                if domain not in known_domains:
                    warnings.append(f"URL domain '{domain}' not in known retailers list")
                
                # Check for hallucinated URL patterns
                suspicious_patterns = [
                    "/_/R-p-",  # Fabricated Decathlon pattern
                    "/en/p/[^/]*/?mc=",  # Fake product URL pattern
                    "//invalid",
                    "example.com"
                ]
                
                for pattern in suspicious_patterns:
                    if pattern.replace("[^/]*", ".*") in product_obj.url:
                        issues.append(f"URL contains suspicious pattern: {pattern}")
            
            except Exception as e:
                issues.append(f"URL parsing error: {str(e)}")
        
        else:
            warnings.append("No product URL provided")
        
        # Check 2: Source citations exist
        if not product_obj.source_citations:
            warnings.append("No source citations found")
        else:
            # Validate each citation
            for i, citation in enumerate(product_obj.source_citations):
                if not citation.uri:
                    issues.append(f"Citation {i} has no URI")
                
                if not citation.title:
                    issues.append(f"Citation {i} has no title")
                
                # Check if main URL matches citation domain
                if product_obj.url and citation.uri:
                    from urllib.parse import urlparse
                    main_domain = urlparse(product_obj.url).netloc
                    citation_domain = urlparse(citation.uri).netloc
                    
                    if main_domain != citation_domain:
                        warnings.append(
                            f"Main URL domain '{main_domain}' differs from citation "
                            f"domain '{citation_domain}' - check if appropriate"
                        )
        
        # Check 3: Grounding status
        if not product_obj.is_grounded:
            warnings.append("Product is not marked as grounded (no backing sources)")
        
        # Check 4: Overall grounding score
        if product_obj.overall_grounding_score:
            if product_obj.overall_grounding_score < 0.5:
                warnings.append(
                    f"Low grounding score: {product_obj.overall_grounding_score:.0%} "
                    "(consider additional verification)"
                )
        
        # Build response
        is_valid = len(issues) == 0
        status = "success" if is_valid else "error"
        
        report_parts = []
        if is_valid:
            report_parts.append("✅ Citations validated successfully")
        else:
            report_parts.append(f"❌ Found {len(issues)} citation issue(s)")
            for issue in issues:
                report_parts.append(f"  • {issue}")
        
        if warnings:
            report_parts.append(f"⚠️  {len(warnings)} warning(s):")
            for warning in warnings:
                report_parts.append(f"  • {warning}")
        
        report = "\n".join(report_parts)
        
        return {
            "status": status,
            "report": report,
            "data": {
                "is_valid": is_valid,
                "issues": issues,
                "warnings": warnings,
                "has_sources": len(product_obj.source_citations) > 0,
                "is_grounded": product_obj.is_grounded,
                "grounding_score": product_obj.overall_grounding_score,
                "validation_timestamp": datetime.utcnow().isoformat()
            }
        }
    
    except Exception as e:
        logger.error(f"Citation validation error: {str(e)}")
        return {
            "status": "error",
            "report": f"Citation validation failed: {str(e)}",
            "error": str(e),
            "data": None
        }


def extract_sources_from_product(
    product: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Extract and format source citations from a product.
    
    Returns sources in a format suitable for display to users.
    
    Args:
        product: Product dict with source_citations
    
    Returns:
        ToolResponse with formatted sources
    """
    try:
        product_obj = Product(**product)
        
        if not product_obj.source_citations:
            return {
                "status": "success",
                "report": "No sources available for this product",
                "data": {"sources": [], "formatted": "No sources found"}
            }
        
        # Group by domain
        by_domain = {}
        for citation in product_obj.source_citations:
            domain = citation.domain or "Unknown Domain"
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(citation)
        
        # Format for display
        formatted_lines = ["**Product Sources:**"]
        for i, (domain, citations) in enumerate(by_domain.items(), 1):
            formatted_lines.append(f"{i}. {domain}")
            for citation in citations:
                formatted_lines.append(f"   📎 {citation.title}")
                if citation.uri:
                    formatted_lines.append(f"   🔗 {citation.uri}")
                if citation.snippet:
                    formatted_lines.append(f"   \"{citation.snippet[:80]}...\"")
        
        return {
            "status": "success",
            "report": f"Extracted {len(product_obj.source_citations)} sources",
            "data": {
                "sources": [c.__dict__ for c in product_obj.source_citations],
                "sources_by_domain": {
                    domain: [c.__dict__ for c in citations]
                    for domain, citations in by_domain.items()
                },
                "unique_domains": list(by_domain.keys()),
                "formatted": "\n".join(formatted_lines)
            }
        }
    
    except Exception as e:
        return {
            "status": "error",
            "report": f"Source extraction failed: {str(e)}",
            "error": str(e),
            "data": None
        }

