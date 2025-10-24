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


class Product(BaseModel):
    """Decathlon product information"""
    product_id: str = Field(description="Unique product identifier")
    name: str = Field(description="Product name")
    price: float = Field(description="Price in EUR")
    currency: str = Field(default="EUR", description="Currency code")
    url: Optional[str] = Field(default=None, description="Product URL")
    category: Optional[str] = Field(default=None, description="Sport category")
    brand: Optional[str] = Field(default=None, description="Brand name")
    rating: Optional[float] = Field(
        default=None,
        description="User rating (0-5)"
    )
    description: Optional[str] = Field(default=None, description="Product description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "123456",
                "name": "Kalenji Running Shoes",
                "price": 89.99,
                "currency": "EUR",
                "category": "running",
                "brand": "Kalenji",
                "rating": 4.5
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
