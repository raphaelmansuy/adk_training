#!/usr/bin/env python3
"""
Quick integration test to verify Redis session storage works end-to-end.

This tests:
1. RedisSessionService connects to Redis
2. Sessions are actually stored in Redis
3. Sessions can be retrieved from Redis
"""

import asyncio
import json
from custom_session_agent.agent import RedisSessionService


async def test_redis_session_storage():
    """Test that sessions are actually stored in Redis."""
    
    print("🧪 Testing Redis Session Storage Integration\n")
    
    # Create Redis session service
    service = RedisSessionService(uri="redis://localhost:6379/0")
    
    if not service.redis_client:
        print("❌ Failed to connect to Redis!")
        return False
    
    print("✅ Connected to Redis\n")
    
    # Clear any previous test data
    print("📝 Cleaning up old test data...")
    service.redis_client.delete("session:test_app:test_user:test_session")
    
    # Test 1: Create a session
    print("\n1️⃣ Creating a test session...")
    session = await service.create_session(
        app_name="test_app",
        user_id="test_user",
        state={"test_key": "test_value"},
        session_id="test_session"
    )
    print(f"   ✅ Session created: {session.id}")
    
    # Test 2: Verify data is in Redis
    print("\n2️⃣ Verifying data is stored in Redis...")
    key = f"session:test_app:test_user:test_session"
    redis_data = service.redis_client.get(key)
    
    if not redis_data:
        print(f"   ❌ Session not found in Redis at key: {key}")
        return False
    
    print(f"   ✅ Session found in Redis!")
    print(f"   📍 Key: {key}")
    
    # Parse and display the data
    session_data = json.loads(redis_data)
    print(f"   📊 Session data:")
    print(f"      - app_name: {session_data.get('app_name')}")
    print(f"      - user_id: {session_data.get('user_id')}")
    print(f"      - session_id: {session_data.get('session_id')}")
    print(f"      - state: {session_data.get('state')}")
    
    # Test 3: Retrieve the session
    print("\n3️⃣ Retrieving session from Redis...")
    retrieved_session = await service.get_session(
        app_name="test_app",
        user_id="test_user",
        session_id="test_session"
    )
    
    if not retrieved_session:
        print("   ❌ Failed to retrieve session")
        return False
    
    print(f"   ✅ Session retrieved successfully")
    print(f"   📊 Retrieved data:")
    print(f"      - session_id: {retrieved_session.id}")
    print(f"      - state: {retrieved_session.state}")
    
    # Test 4: List all sessions
    print("\n4️⃣ Listing all sessions for app...")
    response = await service.list_sessions(app_name="test_app")
    sessions = response.get("sessions", [])
    print(f"   ✅ Found {len(sessions)} session(s)")
    for sess in sessions:
        print(f"      - {sess.get('session_id')}")
    
    # Test 5: Verify in Redis CLI
    print("\n5️⃣ All Redis keys for this app:")
    all_keys = service.redis_client.keys("session:test_app:*")
    for k in all_keys:
        print(f"      - {k}")
    
    # Clean up
    print("\n🧹 Cleaning up test data...")
    service.redis_client.delete(key)
    print("✅ Cleanup complete")
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - Redis session storage is working!")
    print("=" * 70)
    print("\nYou can now:")
    print("1. Run: make dev")
    print("2. Open: http://127.0.0.1:8000")
    print("3. Send messages to test persistence")
    print("4. Check Redis: docker-compose exec redis redis-cli KEYS session:*")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_redis_session_storage())
    exit(0 if success else 1)
