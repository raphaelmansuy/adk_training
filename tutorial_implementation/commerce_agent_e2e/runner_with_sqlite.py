#!/usr/bin/env python3
"""
Commerce Agent Runner with SQLite Session Persistence

This demonstrates using DatabaseSessionService with SQLite for persistent session storage.
Sessions and user preferences survive application restarts.

Usage:
    python runner_with_sqlite.py

Features:
    - SQLite database for session persistence (sessions.db)
    - Multi-user support with complete isolation
    - Conversation history preserved across restarts
    - User preferences persisted in database
    - Grounding metadata callback enabled

Database:
    - Location: ./commerce_agent_sessions.db
    - WAL mode enabled for better concurrency
    - Automatic schema creation
"""

import asyncio
import os
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from commerce_agent import root_agent, create_grounding_callback


async def create_session_for_user(
    session_service: DatabaseSessionService,
    user_id: str,
    app_name: str = "commerce_agent"
):
    """
    Create or retrieve session for user.
    
    Args:
        session_service: DatabaseSessionService instance
        user_id: Unique user identifier
        app_name: Application name (default: commerce_agent)
    
    Returns:
        Session object with user's state and conversation history
    """
    # List existing sessions for user
    sessions = await session_service.list_sessions(
        app_name=app_name,
        user_id=user_id
    )
    
    if sessions['total_count'] > 0:
        # Use most recent session
        latest_session = sessions['sessions'][0]
        print(f"📋 Found existing session: {latest_session.id}")
        print(f"   State: {latest_session.state}")
        print(f"   Events: {len(latest_session.events)}")
        return latest_session
    else:
        # Create new session
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            state={}  # Empty initial state
        )
        print(f"✨ Created new session: {session.id}")
        return session


async def run_agent_with_sqlite():
    """
    Run commerce agent with SQLite persistent sessions.
    
    This demonstrates:
    1. DatabaseSessionService initialization with SQLite
    2. Session creation/retrieval
    3. Running agent with persistent state
    4. Verifying persistence across invocations
    """
    
    # ============================================================
    # Step 1: Initialize DatabaseSessionService with SQLite
    # ============================================================
    
    # Use SQLite with Write-Ahead Logging (WAL) mode for better concurrency
    db_url = "sqlite:///./commerce_agent_sessions.db?mode=wal"
    
    session_service = DatabaseSessionService(db_url=db_url)
    print(f"✅ DatabaseSessionService initialized")
    print(f"   Database: {db_url}")
    
    # ============================================================
    # Step 2: Create Runner with session service
    # ============================================================
    
    runner = Runner(
        agent=root_agent,
        app_name="commerce_agent",
        session_service=session_service,
        after_model_callbacks=[create_grounding_callback(verbose=True)]
    )
    print(f"✅ Runner initialized with SQLite session service")
    
    # ============================================================
    # Step 3: Create/retrieve session for user
    # ============================================================
    
    user_id = "athlete_test_001"
    session = await create_session_for_user(session_service, user_id)
    
    print(f"\n{'='*60}")
    print(f"Starting conversation with session: {session.id}")
    print(f"{'='*60}\n")
    
    # ============================================================
    # Step 4: First interaction - Set preferences
    # ============================================================
    
    message_1 = "I want running shoes under €150. I'm a beginner."
    
    print(f"👤 User: {message_1}\n")
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message={
            "role": "user",
            "parts": [{"text": message_1}]
        }
    ):
        if event.is_final_response():
            print(f"🤖 Agent: {event.content}\n")
    
    # ============================================================
    # Step 5: Verify state was persisted to SQLite
    # ============================================================
    
    session_after_first = await session_service.get_session(
        app_name="commerce_agent",
        user_id=user_id,
        session_id=session.id
    )
    
    print(f"\n{'='*60}")
    print(f"Session state after first interaction:")
    print(f"{'='*60}")
    print(f"State: {session_after_first.state}")
    print(f"Events: {len(session_after_first.events)}")
    print(f"Last update: {session_after_first.last_update_time}")
    
    # ============================================================
    # Step 6: Second interaction - Use saved preferences
    # ============================================================
    
    message_2 = "Show me some options"
    
    print(f"\n{'='*60}")
    print(f"Second interaction (preferences should be remembered):")
    print(f"{'='*60}\n")
    print(f"👤 User: {message_2}\n")
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message={
            "role": "user",
            "parts": [{"text": message_2}]
        }
    ):
        if event.is_final_response():
            print(f"🤖 Agent: {event.content}\n")
    
    # ============================================================
    # Step 7: Verify final state persistence
    # ============================================================
    
    session_final = await session_service.get_session(
        app_name="commerce_agent",
        user_id=user_id,
        session_id=session.id
    )
    
    print(f"\n{'='*60}")
    print(f"Final session state (persisted in SQLite):")
    print(f"{'='*60}")
    print(f"Session ID: {session_final.id}")
    print(f"User ID: {session_final.user_id}")
    print(f"State: {session_final.state}")
    print(f"Total events: {len(session_final.events)}")
    print(f"Last update: {session_final.last_update_time}")
    
    # ============================================================
    # Step 8: Demonstrate persistence across "restarts"
    # ============================================================
    
    print(f"\n{'='*60}")
    print(f"Simulating application restart...")
    print(f"{'='*60}\n")
    
    # Create new session service (simulating app restart)
    new_session_service = DatabaseSessionService(db_url=db_url)
    
    # Retrieve session from database
    restored_session = await new_session_service.get_session(
        app_name="commerce_agent",
        user_id=user_id,
        session_id=session.id
    )
    
    if restored_session:
        print(f"✅ Session restored from SQLite database!")
        print(f"   Session ID: {restored_session.id}")
        print(f"   User preferences preserved:")
        
        for key, value in restored_session.state.items():
            if key.startswith("user:"):
                print(f"      - {key}: {value}")
        
        print(f"   Conversation history: {len(restored_session.events)} events")
    else:
        print(f"❌ Failed to restore session")
    
    print(f"\n{'='*60}")
    print(f"SQLite Session Persistence Demo Complete!")
    print(f"{'='*60}")
    print(f"Database location: ./commerce_agent_sessions.db")
    print(f"You can inspect the database with: sqlite3 commerce_agent_sessions.db")


async def demo_multi_user():
    """
    Demonstrate multi-user isolation with SQLite.
    
    Shows that different users have completely isolated sessions and state.
    """
    
    print(f"\n{'='*60}")
    print(f"MULTI-USER ISOLATION DEMO")
    print(f"{'='*60}\n")
    
    db_url = "sqlite:///./commerce_agent_sessions.db?mode=wal"
    session_service = DatabaseSessionService(db_url=db_url)
    
    # Create sessions for two different users
    alice_session = await session_service.create_session(
        app_name="commerce_agent",
        user_id="alice@example.com",
        state={
            "user:sport": "running",
            "user:budget": 150,
            "user:experience": "advanced"
        }
    )
    
    bob_session = await session_service.create_session(
        app_name="commerce_agent",
        user_id="bob@example.com",
        state={
            "user:sport": "cycling",
            "user:budget": 300,
            "user:experience": "beginner"
        }
    )
    
    print(f"✅ Alice's session: {alice_session.id}")
    print(f"   State: {alice_session.state}")
    
    print(f"\n✅ Bob's session: {bob_session.id}")
    print(f"   State: {bob_session.state}")
    
    # Retrieve and verify isolation
    alice_restored = await session_service.get_session(
        app_name="commerce_agent",
        user_id="alice@example.com",
        session_id=alice_session.id
    )
    
    bob_restored = await session_service.get_session(
        app_name="commerce_agent",
        user_id="bob@example.com",
        session_id=bob_session.id
    )
    
    print(f"\n{'='*60}")
    print(f"Verification: Complete isolation between users")
    print(f"{'='*60}")
    print(f"Alice's sport: {alice_restored.state['user:sport']}")
    print(f"Bob's sport: {bob_restored.state['user:sport']}")
    
    assert alice_restored.state['user:sport'] == 'running'
    assert bob_restored.state['user:sport'] == 'cycling'
    
    print(f"\n✅ Multi-user isolation verified!")


if __name__ == "__main__":
    # Set API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not set")
        print("   Export your API key: export GOOGLE_API_KEY=your_key")
        exit(1)
    
    print(f"\n{'='*60}")
    print(f"COMMERCE AGENT - SQLITE SESSION PERSISTENCE")
    print(f"{'='*60}\n")
    
    # Run main demo
    asyncio.run(run_agent_with_sqlite())
    
    # Run multi-user demo
    asyncio.run(demo_multi_user())
