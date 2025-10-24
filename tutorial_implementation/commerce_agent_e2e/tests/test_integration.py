"""
Integration tests for Commerce Agent.
Tests agent configuration and basic functionality.
"""

import pytest
from commerce_agent.agent import (
    root_agent,
    search_agent,
    preferences_agent,
    storyteller_agent,
)
from commerce_agent.database import init_database


@pytest.mark.integration
class TestAgentConfiguration:
    """Test agent configurations"""
    
    def test_search_agent_exists(self):
        """Test search agent is properly configured"""
        assert search_agent is not None
        assert search_agent.name == "ProductSearchAgent"
        assert search_agent.model == "gemini-2.5-flash"
    
    def test_preferences_agent_exists(self):
        """Test preferences agent is properly configured"""
        assert preferences_agent is not None
        assert preferences_agent.name == "PreferenceManager"
    
    def test_storyteller_agent_exists(self):
        """Test storyteller agent is properly configured"""
        assert storyteller_agent is not None
        assert storyteller_agent.name == "StorytellerAgent"
    
    def test_root_agent_exists(self):
        """Test root agent is properly configured"""
        assert root_agent is not None
        assert root_agent.name == "CommerceCoordinator"
        assert root_agent.model == "gemini-2.5-flash"
    
    def test_root_agent_has_sub_agents(self):
        """Test root agent has sub-agents"""
        assert hasattr(root_agent, "sub_agents")
        # Should have 3 sub-agents
        assert len(root_agent.sub_agents) == 3
    
    def test_agent_models_are_valid(self):
        """Test all agents use valid model names"""
        valid_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        
        assert search_agent.model in valid_models
        assert preferences_agent.model in valid_models
        assert storyteller_agent.model in valid_models
        assert root_agent.model in valid_models
    
    def test_agent_instructions_are_set(self):
        """Test all agents have instructions"""
        assert search_agent.instruction is not None and len(search_agent.instruction) > 0
        assert preferences_agent.instruction is not None and len(preferences_agent.instruction) > 0
        assert storyteller_agent.instruction is not None and len(storyteller_agent.instruction) > 0
        assert root_agent.instruction is not None and len(root_agent.instruction) > 0


@pytest.mark.integration
class TestDatabaseIntegration:
    """Test database integration"""
    
    def test_database_initializes(self):
        """Test database can be initialized"""
        try:
            init_database()
            assert True
        except Exception as e:
            assert False, f"Database initialization failed: {str(e)}"
    
    def test_database_multiple_users(self):
        """Test database handles multiple users correctly"""
        from commerce_agent.database import (
            save_user_preferences,
            get_user_preferences,
        )
        from commerce_agent.models import UserPreferences
        
        init_database()
        
        # Create two users with different preferences
        user1_prefs = UserPreferences(sports=["running"])
        user2_prefs = UserPreferences(sports=["cycling"])
        
        save_user_preferences("user_1", user1_prefs)
        save_user_preferences("user_2", user2_prefs)
        
        # Verify isolation
        retrieved_1 = get_user_preferences("user_1")
        retrieved_2 = get_user_preferences("user_2")
        
        assert retrieved_1.sports == ["running"]
        assert retrieved_2.sports == ["cycling"]


@pytest.mark.integration
class TestToolIntegration:
    """Test tool integration"""
    
    def test_preference_tool_callable(self):
        """Test preference management tool is callable"""
        from commerce_agent.tools import manage_user_preferences
        
        result = manage_user_preferences(
            action="get",
            user_id="test_user"
        )
        
        assert "status" in result
        assert "report" in result
        assert "data" in result
    
    def test_curation_tool_callable(self):
        """Test product curation tool is callable"""
        from commerce_agent.tools import curate_products
        
        result = curate_products(products=[])
        
        assert "status" in result
        assert "report" in result
        assert "data" in result
    
    def test_narrative_tool_callable(self):
        """Test narrative generation tool is callable"""
        from commerce_agent.tools import generate_product_narrative
        
        result = generate_product_narrative(
            product={"name": "Test Product"}
        )
        
        assert "status" in result
        assert "report" in result


@pytest.mark.integration
class TestImportPaths:
    """Test all public imports work correctly"""
    
    def test_import_root_agent(self):
        """Test root agent can be imported"""
        from commerce_agent import root_agent
        assert root_agent is not None
    
    def test_import_all_agents(self):
        """Test all agents can be imported"""
        from commerce_agent import (
            root_agent,
            search_agent,
            preferences_agent,
            storyteller_agent,
        )
        assert all([root_agent, search_agent, preferences_agent, storyteller_agent])
    
    def test_import_tools(self):
        """Test all tools can be imported"""
        from commerce_agent import (
            manage_user_preferences,
            curate_products,
            generate_product_narrative,
        )
        assert all([manage_user_preferences, curate_products, generate_product_narrative])
    
    def test_import_models(self):
        """Test all models can be imported"""
        from commerce_agent import (
            UserPreferences,
            Product,
            InteractionRecord,
            EngagementProfile,
        )
        assert all([UserPreferences, Product, InteractionRecord, EngagementProfile])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
