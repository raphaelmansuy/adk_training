"""
Structured data types for Commerce Agent

Following ADK best practices from travel-concierge agent.
All response types use Pydantic for structured JSON generation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from google.genai import types


# Convenient declaration for controlled generation
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)


# ============================================================================
# USER PREFERENCES
# ============================================================================

class UserPreferences(BaseModel):
    """Structured user preferences for product recommendations."""
    
    sport_type: Optional[str] = Field(
        default=None,
        description="Type of sport: running, cycling, hiking, swimming, etc."
    )
    usage_scenario: Optional[str] = Field(
        default=None,
        description="Usage context: road, trail, track, gym, outdoor, indoor"
    )
    terrain_type: Optional[str] = Field(
        default=None,
        description="Terrain: rocky, muddy, paved, flat, hilly"
    )
    skill_level: Optional[str] = Field(
        default=None,
        description="Experience level: beginner, intermediate, advanced, professional"
    )
    budget_max: Optional[float] = Field(
        default=None,
        description="Maximum budget in EUR"
    )
    budget_min: Optional[float] = Field(
        default=None,
        description="Minimum budget in EUR"
    )
    preferred_brands: List[str] = Field(
        default_factory=list,
        description="Preferred or avoided brands"
    )
    size: Optional[str] = Field(
        default=None,
        description="Clothing or shoe size"
    )
    special_requirements: List[str] = Field(
        default_factory=list,
        description="Special needs: waterproof, breathable, cushioning, stability, etc."
    )
    color_preferences: List[str] = Field(
        default_factory=list,
        description="Color preferences"
    )


class PreferenceCollectionResult(BaseModel):
    """Result from preference collection process."""
    
    status: str = Field(
        description="Status: 'success' if complete, 'needs_more_info' if missing critical data"
    )
    preferences: UserPreferences = Field(
        description="Collected user preferences"
    )
    missing_info: List[str] = Field(
        default_factory=list,
        description="List of missing critical information"
    )
    next_questions: List[str] = Field(
        default_factory=list,
        description="Batch questions to ask for missing information"
    )
    completeness_score: float = Field(
        default=0.0,
        description="Percentage of critical fields completed (0.0-1.0)"
    )


# ============================================================================
# PRODUCT INFORMATION
# ============================================================================

class Price(BaseModel):
    """Product pricing information."""
    
    amount: float = Field(description="Price amount")
    currency: str = Field(default="EUR", description="Currency code")
    original_price: Optional[float] = Field(
        default=None,
        description="Original price if on sale"
    )
    discount_percentage: Optional[float] = Field(
        default=None,
        description="Discount percentage if applicable"
    )


class ProductSource(BaseModel):
    """Source attribution for product information."""
    
    domain: str = Field(description="Source domain (e.g., decathlon.com.hk)")
    url: str = Field(description="Direct product URL")
    verified: bool = Field(
        default=True,
        description="Whether URL was verified from search results"
    )
    confidence_score: Optional[float] = Field(
        default=None,
        description="Confidence in information accuracy (0.0-1.0)"
    )


class Product(BaseModel):
    """Detailed product information."""
    
    id: str = Field(description="Unique product identifier")
    name: str = Field(description="Product name")
    brand: str = Field(description="Brand name")
    description: str = Field(description="Product description")
    price: Price = Field(description="Pricing information")
    images: List[str] = Field(
        default_factory=list,
        description="Product image URLs"
    )
    rating: Optional[float] = Field(
        default=None,
        description="Average rating (0.0-5.0)"
    )
    review_count: Optional[int] = Field(
        default=None,
        description="Number of reviews"
    )
    availability: str = Field(
        default="unknown",
        description="Stock status: in_stock, low_stock, out_of_stock, unknown"
    )
    features: List[str] = Field(
        default_factory=list,
        description="Key product features"
    )
    specifications: Dict[str, Any] = Field(
        default_factory=dict,
        description="Technical specifications"
    )
    sources: List[ProductSource] = Field(
        default_factory=list,
        description="Source attribution for this product"
    )
    match_score: Optional[float] = Field(
        default=None,
        description="How well product matches user preferences (0.0-1.0)"
    )
    match_reasons: List[str] = Field(
        default_factory=list,
        description="Why this product was recommended"
    )


class ProductRecommendations(BaseModel):
    """Structured product recommendations with metadata."""
    
    products: List[Product] = Field(
        description="List of recommended products"
    )
    filters_applied: Dict[str, Any] = Field(
        default_factory=dict,
        description="Filters used in search"
    )
    search_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Search execution metadata"
    )
    total_results: int = Field(
        default=0,
        description="Total products found"
    )
    showing: int = Field(
        default=0,
        description="Number of products displayed"
    )
    confidence_score: float = Field(
        default=0.0,
        description="Overall confidence in recommendations (0.0-1.0)"
    )


# ============================================================================
# SHOPPING CART
# ============================================================================

class CartItem(BaseModel):
    """Item in shopping cart."""
    
    product_id: str = Field(description="Product identifier")
    product_name: str = Field(description="Product name")
    brand: str = Field(description="Brand name")
    quantity: int = Field(default=1, description="Quantity")
    unit_price: float = Field(description="Price per unit")
    total_price: float = Field(description="Total price for quantity")
    currency: str = Field(default="EUR")
    image_url: Optional[str] = Field(default=None)
    size: Optional[str] = Field(default=None)
    color: Optional[str] = Field(default=None)
    added_at: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp"
    )


class Cart(BaseModel):
    """Shopping cart state."""
    
    items: List[CartItem] = Field(
        default_factory=list,
        description="Items in cart"
    )
    subtotal: float = Field(
        default=0.0,
        description="Subtotal before tax/shipping"
    )
    tax: float = Field(default=0.0)
    shipping: float = Field(default=0.0)
    total: float = Field(default=0.0)
    currency: str = Field(default="EUR")
    item_count: int = Field(
        default=0,
        description="Total number of items"
    )
    last_modified: Optional[str] = Field(
        default=None,
        description="ISO 8601 timestamp"
    )


class CartModificationResult(BaseModel):
    """Result of cart modification operation."""
    
    status: str = Field(description="success or error")
    message: str = Field(description="Human-readable message")
    cart: Cart = Field(description="Updated cart state")
    items_added: List[str] = Field(
        default_factory=list,
        description="Product IDs added"
    )
    items_removed: List[str] = Field(
        default_factory=list,
        description="Product IDs removed"
    )


# ============================================================================
# VISUAL ANALYSIS
# ============================================================================

class VisualAnalysisResult(BaseModel):
    """Result from image/video analysis."""
    
    status: str = Field(description="success or error")
    identified_products: List[Product] = Field(
        default_factory=list,
        description="Products identified in image/video"
    )
    detected_brands: List[str] = Field(
        default_factory=list,
        description="Brands detected"
    )
    detected_colors: List[str] = Field(
        default_factory=list,
        description="Colors detected"
    )
    condition_assessment: Optional[str] = Field(
        default=None,
        description="Condition: new, good, worn, damaged"
    )
    fit_assessment: Optional[str] = Field(
        default=None,
        description="Fit assessment if applicable"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommendations based on analysis"
    )
    confidence_score: float = Field(
        default=0.0,
        description="Confidence in analysis (0.0-1.0)"
    )


# ============================================================================
# ORDER MANAGEMENT
# ============================================================================

class OrderSummary(BaseModel):
    """Order summary and confirmation."""
    
    order_id: str = Field(description="Unique order identifier")
    status: str = Field(
        description="Order status: pending, confirmed, processing, shipped, delivered, cancelled"
    )
    items: List[CartItem] = Field(description="Ordered items")
    subtotal: float = Field(description="Subtotal")
    tax: float = Field(description="Tax amount")
    shipping: float = Field(description="Shipping cost")
    total: float = Field(description="Total amount")
    currency: str = Field(default="EUR")
    payment_method: Optional[str] = Field(default=None)
    shipping_address: Optional[str] = Field(default=None)
    estimated_delivery: Optional[str] = Field(
        default=None,
        description="ISO 8601 date"
    )
    order_date: str = Field(description="ISO 8601 timestamp")
    tracking_number: Optional[str] = Field(default=None)


# ============================================================================
# SEARCH QUERIES
# ============================================================================

class SearchQuery(BaseModel):
    """Structured search query."""
    
    query_text: str = Field(description="Search query string")
    filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Search filters"
    )
    category: Optional[str] = Field(default=None)
    min_price: Optional[float] = Field(default=None)
    max_price: Optional[float] = Field(default=None)
    brands: List[str] = Field(default_factory=list)
    sort_by: Optional[str] = Field(
        default=None,
        description="Sort criteria: relevance, price_asc, price_desc, rating, newest"
    )
    page: int = Field(default=1)
    page_size: int = Field(default=10)
