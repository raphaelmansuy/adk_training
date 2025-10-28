"""
Unit tests for Commerce Agent tools.
Tests individual tool functions in isolation.
"""

import pytest
from commerce_agent.tools import (
    manage_user_preferences,
    curate_products,
    generate_product_narrative,
)
from commerce_agent.database import init_database
from commerce_agent.models import UserPreferences, Product


@pytest.mark.unit
class TestPreferencesTool:
    """Test preference management tool"""
    
    def setup_method(self):
        """Setup before each test"""
        init_database()
    
    def test_manage_preferences_get_new_user(self):
        """Test getting preferences for new user returns defaults"""
        result = manage_user_preferences(
            action="get",
            user_id="new_user_123"
        )
        
        assert result["status"] == "success"
        assert "preferences" in result["data"]
        assert isinstance(result["data"]["preferences"]["sports"], list)
    
    def test_manage_preferences_update(self):
        """Test updating user preferences"""
        user_id = "update_test_user"
        
        result = manage_user_preferences(
            action="update",
            user_id=user_id,
            data={
                "sports": ["running", "cycling"],
                "price_range": {"min_price": 50.0, "max_price": 200.0},
                "brands": ["Kalenji", "Quechua"]
            }
        )
        
        assert result["status"] == "success"
        prefs = result["data"]["preferences"]
        assert "running" in prefs["sports"]
        assert "cycling" in prefs["sports"]
    
    def test_manage_preferences_get_existing(self):
        """Test retrieving previously saved preferences"""
        user_id = "existing_user_456"
        
        # First, save preferences
        manage_user_preferences(
            action="update",
            user_id=user_id,
            data={"sports": ["yoga"]}
        )
        
        # Then retrieve
        result = manage_user_preferences(
            action="get",
            user_id=user_id
        )
        
        assert result["status"] == "success"
        assert "yoga" in result["data"]["preferences"]["sports"]
    
    def test_manage_preferences_add_history(self):
        """Test adding interaction to history"""
        user_id = "history_user"
        
        result = manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={
                "session_id": "session_789",
                "query": "Find running shoes",
                "result_count": 5
            }
        )
        
        assert result["status"] == "success"
        assert result["data"]["interaction"]["query"] == "Find running shoes"
    
    def test_manage_preferences_add_favorite(self):
        """Test adding product to favorites"""
        user_id = "favorite_user"
        
        result = manage_user_preferences(
            action="add_favorite",
            user_id=user_id,
            data={
                "product_id": "prod_123",
                "product_name": "Awesome Shoes",
                "url": "https://decathlon.fr/product"
            }
        )
        
        assert result["status"] == "success"
        assert result["data"]["favorite"]["product_name"] == "Awesome Shoes"
    
    def test_manage_preferences_get_favorites(self):
        """Test retrieving user favorites"""
        user_id = "favorites_user"
        
        # Add some favorites
        manage_user_preferences(
            action="add_favorite",
            user_id=user_id,
            data={"product_id": "p1", "product_name": "Product 1"}
        )
        manage_user_preferences(
            action="add_favorite",
            user_id=user_id,
            data={"product_id": "p2", "product_name": "Product 2"}
        )
        
        # Retrieve favorites
        result = manage_user_preferences(
            action="get_favorites",
            user_id=user_id
        )
        
        assert result["status"] == "success"
        assert len(result["data"]["favorites"]) == 2
    
    def test_manage_preferences_invalid_action(self):
        """Test invalid action returns error"""
        result = manage_user_preferences(
            action="invalid_action",
            user_id="any_user"
        )
        
        assert result["status"] == "error"
        assert "Unknown action" in result["report"]


@pytest.mark.unit
class TestProductCuration:
    """Test product curation tool"""
    
    def test_curate_products_empty_list(self):
        """Test curation with empty product list"""
        result = curate_products(products=[])
        
        assert result["status"] == "success"
        assert result["data"]["curated_products"] == []
    
    def test_curate_products_basic(self, sample_products):
        """Test basic product curation without filters"""
        result = curate_products(products=sample_products, limit=2)
        
        assert result["status"] == "success"
        assert len(result["data"]["curated_products"]) <= 2
    
    def test_curate_products_with_price_filter(self, sample_products):
        """Test curation with price range filter"""
        result = curate_products(
            products=sample_products,
            user_preferences={
                "sports": [],
                "price_range": {"min_price": 50.0, "max_price": 100.0},
                "brands": []
            },
            limit=5
        )
        
        assert result["status"] == "success"
        curated = result["data"]["curated_products"]
        
        # All products should be within price range
        for product in curated:
            assert 50.0 <= product["price"] <= 100.0
    
    def test_curate_products_with_brand_filter(self, sample_products):
        """Test curation prioritizes preferred brands"""
        result = curate_products(
            products=sample_products,
            user_preferences={
                "sports": [],
                "price_range": {"min_price": 0.0, "max_price": 500.0},
                "brands": ["Kalenji"]
            },
            limit=5
        )
        
        assert result["status"] == "success"
        curated = result["data"]["curated_products"]
        
        # Should have at least one product
        assert len(curated) > 0
    
    def test_curate_products_respects_limit(self, sample_products):
        """Test curation respects limit parameter"""
        result = curate_products(products=sample_products, limit=1)
        
        assert len(result["data"]["curated_products"]) <= 1


@pytest.mark.unit
class TestProductNarrative:
    """Test product narrative generation"""
    
    def test_generate_narrative_valid_product(self, sample_product):
        """Test narrative generation for valid product"""
        result = generate_product_narrative(
            product=sample_product.model_dump()
        )
        
        assert result["status"] == "success"
        assert "narrative_template" in result["data"]
        assert sample_product.name in result["data"]["narrative_template"]
    
    def test_generate_narrative_with_context(self, sample_product):
        """Test narrative with user context"""
        result = generate_product_narrative(
            product=sample_product.model_dump(),
            user_context={"sports": ["running", "cycling"]}
        )
        
        assert result["status"] == "success"
        narrative = result["data"]["narrative_template"]
        assert "running" in narrative or "cycling" in narrative
    
    def test_generate_narrative_missing_product_name(self):
        """Test error handling for invalid product"""
        result = generate_product_narrative(
            product={}  # Missing required fields
        )
        
        assert result["status"] == "error"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
