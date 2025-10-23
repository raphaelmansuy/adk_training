#!/usr/bin/env python3
"""
Helper script to view session data stored in Redis in a readable format.

Usage:
    python view_sessions.py              # Show all sessions
    python view_sessions.py <session_id> # Show specific session
"""

import redis
import json
import sys
from typing import Optional

def connect_to_redis(uri: str = "redis://localhost:6379/0") -> redis.Redis:
    """Connect to Redis."""
    try:
        client = redis.from_url(uri, decode_responses=True)
        client.ping()
        return client
    except Exception as e:
        print(f"❌ Failed to connect to Redis: {e}")
        sys.exit(1)

def print_session(key: str, data: dict) -> None:
    """Pretty print a session."""
    print(f"\n{'=' * 80}")
    print(f"📋 SESSION KEY: {key}")
    print('=' * 80)
    
    print(f"\n🔑 Session ID:     {data.get('session_id', 'N/A')}")
    print(f"📱 App Name:       {data.get('app_name', 'N/A')}")
    print(f"👤 User ID:        {data.get('user_id', 'N/A')}")
    print(f"📅 Created:        {data.get('created_at', 'N/A')}")
    print(f"🔄 Updated:        {data.get('updated_at', 'N/A')}")
    
    state = data.get('state', {})
    if state:
        print(f"\n📦 SESSION STATE ({len(state)} items):")
        for key, value in state.items():
            print(f"   • {key}: {json.dumps(value) if not isinstance(value, (str, int, float, bool)) else value}")
    else:
        print(f"\n📦 SESSION STATE: (empty)")
    
    events = data.get('events', [])
    if events:
        print(f"\n📝 EVENTS ({len(events)} total):")
        for i, event in enumerate(events, 1):
            print(f"   {i}. {json.dumps(event, indent=6)}")
    else:
        print(f"\n📝 EVENTS: (none)")
    
    print()

def view_all_sessions() -> None:
    """Display all sessions stored in Redis."""
    client = connect_to_redis()
    
    print("\n" + "=" * 80)
    print("🔍 REDIS SESSIONS - ALL")
    print("=" * 80)
    
    # Find all session keys
    keys = client.keys("session:*")
    
    if not keys:
        print("\n❌ No sessions found in Redis")
        return
    
    print(f"\n✅ Found {len(keys)} session(s) in Redis\n")
    
    for i, key in enumerate(sorted(keys), 1):
        session_json = client.get(key)
        if session_json:
            try:
                session_data = json.loads(session_json)
                print(f"\n{i}. {key}")
                print(f"   📝 State keys: {list(session_data.get('state', {}).keys())}")
                print(f"   ⏱️  Created: {session_data.get('created_at', 'N/A')}")
                print(f"   📊 Events: {len(session_data.get('events', []))}")
            except json.JSONDecodeError:
                print(f"❌ Failed to parse session data for key: {key}")

def view_session(session_id: str) -> None:
    """Display a specific session."""
    client = connect_to_redis()
    
    # Try to find the session key
    pattern = f"session:*{session_id}*"
    keys = client.keys(pattern)
    
    if not keys:
        print(f"\n❌ No session found matching: {session_id}")
        return
    
    if len(keys) > 1:
        print(f"\n⚠️  Multiple sessions match '{session_id}':")
        for key in keys:
            print(f"   • {key}")
        print("\nShowing first match...\n")
    
    key = keys[0]
    session_json = client.get(key)
    
    if not session_json:
        print(f"❌ Session not found: {key}")
        return
    
    try:
        session_data = json.loads(session_json)
        print_session(key, session_data)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse session data: {e}")

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # View specific session
        session_id = sys.argv[1]
        view_session(session_id)
    else:
        # View all sessions
        view_all_sessions()
    
    print("\n" + "=" * 80)
    print("💡 TIP: To view specific session, run:")
    print("   python view_sessions.py <session_id>")
    print("\n🔗 REDIS COMMANDS:")
    print("   redis-cli KEYS 'session:*'")
    print("   redis-cli GET 'session:app:user:id'")
    print("   redis-cli TTL 'session:app:user:id'  # Check expiration")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
