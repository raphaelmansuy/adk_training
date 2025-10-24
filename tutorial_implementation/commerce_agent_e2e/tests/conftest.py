"""
Test fixtures and configuration for Commerce Agent tests.
"""

import pytest
import pytest_asyncio
import os
import tempfile
from pathlib import Path

from commerce_agent.database import init_database, get_db_connection
from commerce_agent.models import UserPreferences, Product
from commerce_agent.config import TEST_USER_ID, TEST_SESSION_ID


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Setup test database - runs once per test session"""
    # Create temporary directory for test database
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "test_commerce_agent.db")
    
    # Set environment variable to use test database
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    
    yield
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)
    os.rmdir(temp_dir)


@pytest.fixture(autouse=True)
def clean_db_before_test():
    """Clean database before each test"""
    # Get connection and clear all tables
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Drop all tables
        c.execute("DELETE FROM product_cache")
        c.execute("DELETE FROM user_favorites")
        c.execute("DELETE FROM interaction_history")
        c.execute("DELETE FROM user_preferences")
        
        conn.commit()
        conn.close()
    except Exception:
        pass  # Tables might not exist yet
    
    # Initialize fresh database
    init_database()
    
    yield


@pytest.fixture
def sample_preferences() -> UserPreferences:
    """Sample user preferences"""
    return UserPreferences(
        sports=["running", "cycling"],
        price_range={"min_price": 30.0, "max_price": 150.0},
        brands=["Kalenji", "Quechua"]
    )


@pytest.fixture
def sample_product() -> Product:
    """Sample product"""
    return Product(
        product_id="123456",
        name="Kalenji Running Shoes",
        price=89.99,
        category="running",
        brand="Kalenji",
        rating=4.5,
        description="Comfortable running shoes"
    )


@pytest.fixture
def sample_products() -> list:
    """Sample product list"""
    return [
        {
            "product_id": "1001",
            "name": "Kalenji Running Shoes",
            "price": 79.99,
            "category": "running",
            "brand": "Kalenji",
            "rating": 4.5
        },
        {
            "product_id": "1002",
            "name": "Quechua Hiking Boots",
            "price": 149.99,
            "category": "hiking",
            "brand": "Quechua",
            "rating": 4.3
        },
        {
            "product_id": "1003",
            "name": "Expensive Bike Gear",
            "price": 299.99,
            "category": "cycling",
            "brand": "Premium Brand",
            "rating": 4.7
        },
    ]


@pytest_asyncio.fixture
async def test_user_id() -> str:
    """Test user ID"""
    return TEST_USER_ID


@pytest_asyncio.fixture
async def test_session_id() -> str:
    """Test session ID"""
    return TEST_SESSION_ID


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")
