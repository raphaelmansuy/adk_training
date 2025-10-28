"""
End-to-End tests for Commerce Agent.
Tests complete workflows and user scenarios.
"""

import pytest
from commerce_agent.database import (
    init_database,
    get_user_preferences,
    get_user_history,
    get_user_favorites,
    get_engagement_profile,
)
from commerce_agent.tools import manage_user_preferences
from commerce_agent.models import UserPreferences, InteractionRecord


@pytest.mark.e2e
class TestUserScenarios:
    """Test complete user scenarios"""
    
    def setup_method(self):
        """Setup for each test"""
        init_database()
    
    def test_scenario_new_athlete(self):
        """Test complete flow for new athlete user"""
        user_id = "new_athlete"
        
        # Step 1: User sets preferences
        result = manage_user_preferences(
            action="update",
            user_id=user_id,
            data={"sports": ["running", "cycling"]}
        )
        assert result["status"] == "success"
        
        # Step 2: Query search
        result = manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={
                "session_id": "session_1",
                "query": "Find running shoes under 100",
                "result_count": 5
            }
        )
        assert result["status"] == "success"
        
        # Step 3: Add favorite product
        result = manage_user_preferences(
            action="add_favorite",
            user_id=user_id,
            data={
                "product_id": "kalenji_123",
                "product_name": "Kalenji Running Shoes",
                "url": "https://decathlon.fr/kalenji"
            }
        )
        assert result["status"] == "success"
        
        # Verify complete profile
        prefs = get_user_preferences(user_id)
        assert prefs is not None
        assert "running" in prefs.sports
        
        history = get_user_history(user_id)
        assert len(history) == 1
        assert history[0].query == "Find running shoes under 100"
        
        favorites = get_user_favorites(user_id)
        assert len(favorites) == 1
        assert favorites[0].product_name == "Kalenji Running Shoes"
    
    def test_scenario_returning_customer(self):
        """Test flow for returning customer with existing profile"""
        user_id = "returning_customer"
        
        # Session 1: Initial setup
        manage_user_preferences(
            action="update",
            user_id=user_id,
            data={"sports": ["yoga"]}
        )
        manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={
                "session_id": "session_1",
                "query": "Yoga mats",
                "result_count": 3
            }
        )
        
        # Session 2: Returning with new interests
        result = manage_user_preferences(
            action="update",
            user_id=user_id,
            data={"sports": ["yoga", "hiking"]}  # Add hiking
        )
        assert result["status"] == "success"
        
        # Verify preferences accumulated
        prefs = get_user_preferences(user_id)
        assert "yoga" in prefs.sports
        assert "hiking" in prefs.sports
        
        # Add new interaction
        manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={
                "session_id": "session_2",
                "query": "Hiking boots",
                "result_count": 4
            }
        )
        
        # Verify history has both interactions
        history = get_user_history(user_id, limit=10)
        assert len(history) == 2
    
    def test_scenario_multi_user_isolation(self):
        """Test that different users don't interfere with each other"""
        user_alice = "alice"
        user_bob = "bob"
        
        # Alice's profile
        manage_user_preferences(
            action="update",
            user_id=user_alice,
            data={"sports": ["running"]}
        )
        manage_user_preferences(
            action="add_favorite",
            user_id=user_alice,
            data={"product_id": "p1", "product_name": "Running Shoes"}
        )
        
        # Bob's profile
        manage_user_preferences(
            action="update",
            user_id=user_bob,
            data={"sports": ["cycling"]}
        )
        manage_user_preferences(
            action="add_favorite",
            user_id=user_bob,
            data={"product_id": "p2", "product_name": "Bike Helmet"}
        )
        
        # Verify complete isolation
        alice_prefs = get_user_preferences(user_alice)
        bob_prefs = get_user_preferences(user_bob)
        
        assert "running" in alice_prefs.sports
        assert "cycling" not in alice_prefs.sports
        
        assert "cycling" in bob_prefs.sports
        assert "running" not in bob_prefs.sports
        
        # Verify favorites are isolated
        alice_favs = get_user_favorites(user_alice)
        bob_favs = get_user_favorites(user_bob)
        
        assert len(alice_favs) == 1
        assert alice_favs[0].product_name == "Running Shoes"
        
        assert len(bob_favs) == 1
        assert bob_favs[0].product_name == "Bike Helmet"


@pytest.mark.e2e
class TestEngagementTracking:
    """Test engagement profile tracking"""
    
    def setup_method(self):
        """Setup for each test"""
        init_database()
    
    def test_engagement_profile_creation(self):
        """Test engagement profile is created correctly"""
        user_id = "engaged_user"
        
        # Build engagement
        manage_user_preferences(
            action="update",
            user_id=user_id,
            data={
                "sports": ["running", "cycling"],
                "brands": ["Kalenji", "Quechua"]
            }
        )
        
        manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={
                "session_id": "s1",
                "query": "Running shoes",
                "result_count": 5
            }
        )
        
        manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={
                "session_id": "s2",
                "query": "Cycling shorts",
                "result_count": 3
            }
        )
        
        # Get profile
        profile = get_engagement_profile(user_id)
        
        assert profile.total_interactions == 2
        assert "running" in profile.favorite_categories
        assert "cycling" in profile.favorite_categories
        assert "Kalenji" in profile.preferred_brands
        assert "Quechua" in profile.preferred_brands


@pytest.mark.e2e
class TestErrorRecovery:
    """Test error handling and recovery"""
    
    def setup_method(self):
        """Setup for each test"""
        init_database()
    
    def test_invalid_preference_update_recovered(self):
        """Test system recovers from invalid preference update"""
        user_id = "recovery_user"
        
        # Valid update
        manage_user_preferences(
            action="update",
            user_id=user_id,
            data={"sports": ["running"]}
        )
        
        # Invalid update attempt (missing required data)
        result = manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={}  # Missing required fields
        )
        assert result["status"] == "error"
        
        # System should recover - original data intact
        prefs = get_user_preferences(user_id)
        assert "running" in prefs.sports
    
    def test_missing_user_preference_defaults(self):
        """Test missing user returns default preferences"""
        result = manage_user_preferences(
            action="get",
            user_id="nonexistent_user"
        )
        
        assert result["status"] == "success"
        prefs = result["data"]["preferences"]
        assert isinstance(prefs["sports"], list)
        assert isinstance(prefs["price_range"], dict)


@pytest.mark.e2e
class TestDataPersistence:
    """Test that data persists across operations"""
    
    def setup_method(self):
        """Setup for each test"""
        init_database()
    
    def test_preferences_persist_across_operations(self):
        """Test preferences remain consistent after multiple operations"""
        user_id = "persistence_user"
        original_sports = ["running", "climbing"]
        
        # Set initial preferences
        manage_user_preferences(
            action="update",
            user_id=user_id,
            data={"sports": original_sports}
        )
        
        # Perform other operations
        manage_user_preferences(
            action="add_history",
            user_id=user_id,
            data={"session_id": "s1", "query": "test"}
        )
        manage_user_preferences(
            action="add_favorite",
            user_id=user_id,
            data={"product_id": "p1", "product_name": "Product"}
        )
        
        # Verify preferences unchanged
        prefs = get_user_preferences(user_id)
        assert set(prefs.sports) == set(original_sports)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
