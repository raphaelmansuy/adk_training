"""
Pydantic models for Commerce Agent.
Defines data structures for preferences, products, and interaction tracking.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class PriceRange(BaseModel):
    """User's preferred price range"""
    min_price: float = Field(default=0.0, description="Minimum price in EUR")
    max_price: float = Field(default=500.0, description="Maximum price in EUR")


class UserPreferences(BaseModel):
    """User sports and shopping preferences"""
    sports: List[str] = Field(
        default_factory=list,
        description="List of sports user is interested in"
    )
    price_range: PriceRange = Field(
        default_factory=PriceRange,
        description="Preferred price range"
    )
    brands: List[str] = Field(
        default_factory=list,
        description="Preferred brands"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "sports": ["running", "cycling"],
                "price_range": {"min_price": 30, "max_price": 150},
                "brands": ["Kalenji", "Quechua"]
            }
        }


class SourceCitation(BaseModel):
    """Citation source for a product fact or claim"""
    title: str = Field(description="Source title (website name, article)")
    uri: str = Field(description="Direct URL to source")
    domain: Optional[str] = Field(default=None, description="Domain name extracted from URL")
    snippet: Optional[str] = Field(default=None, description="Preview text from source")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Decathlon Official Store",
                "uri": "https://www.decathlon.com.hk/en/p/kalenji-shoes",
                "domain": "decathlon.com.hk",
                "snippet": "Kalenji Running Shoes - Lightweight performance..."
            }
        }


class GroundedSegment(BaseModel):
    """Text segment backed by source citations"""
    text: str = Field(description="The segment text")
    sources: List[SourceCitation] = Field(
        default_factory=list,
        description="Sources that support this segment"
    )
    confidence: Optional[float] = Field(
        default=None,
        description="Confidence score (0.0-1.0) for this segment's accuracy"
    )


class Product(BaseModel):
    """Decathlon product information with grounding metadata"""
    product_id: str = Field(description="Unique product identifier")
    name: str = Field(description="Product name")
    price: float = Field(description="Price in EUR")
    currency: str = Field(default="EUR", description="Currency code")
    url: Optional[str] = Field(default=None, description="Product URL from search results")
    category: Optional[str] = Field(default=None, description="Sport category")
    brand: Optional[str] = Field(default=None, description="Brand name")
    rating: Optional[float] = Field(
        default=None,
        description="User rating (0-5)"
    )
    description: Optional[str] = Field(default=None, description="Product description")
    
    # Grounding metadata for source attribution
    source_citations: List[SourceCitation] = Field(
        default_factory=list,
        description="Sources where this product information was found"
    )
    grounded_segments: List[GroundedSegment] = Field(
        default_factory=list,
        description="Product description segments with their supporting sources"
    )
    overall_grounding_score: Optional[float] = Field(
        default=None,
        description="Overall confidence score for product data accuracy (0.0-1.0)"
    )
    is_grounded: bool = Field(
        default=False,
        description="Whether product data is backed by actual search results"
    )
    search_timestamp: Optional[str] = Field(
        default=None,
        description="When this product data was retrieved from search"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "123456",
                "name": "Kalenji Running Shoes",
                "price": 89.99,
                "currency": "EUR",
                "category": "running",
                "brand": "Kalenji",
                "rating": 4.5,
                "url": "https://www.decathlon.com.hk/en/p/kalenji-shoes",
                "source_citations": [
                    {
                        "title": "Decathlon Hong Kong",
                        "uri": "https://www.decathlon.com.hk/en/p/kalenji-shoes",
                        "domain": "decathlon.com.hk"
                    }
                ],
                "is_grounded": True,
                "overall_grounding_score": 0.95
            }
        }


class InteractionRecord(BaseModel):
    """Record of user interaction with agent"""
    user_id: str
    session_id: str
    query: str
    result_count: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    products_found: List[str] = Field(default_factory=list)


class UserFavorite(BaseModel):
    """User's favorite product"""
    user_id: str
    product_id: str
    product_name: str
    url: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)


class EngagementProfile(BaseModel):
    """User engagement metrics"""
    total_interactions: int = 0
    favorite_categories: List[str] = Field(default_factory=list)
    preferred_brands: List[str] = Field(default_factory=list)
    last_interaction: Optional[datetime] = None
    avg_session_duration: float = 0.0  # seconds


class ToolResponse(BaseModel):
    """Standard response format for all tools"""
    status: str = Field(..., description="'success' or 'error'")
    report: str = Field(..., description="Human-readable status message")
    data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Tool-specific return data"
    )
    error: Optional[str] = Field(default=None, description="Error details if failed")
