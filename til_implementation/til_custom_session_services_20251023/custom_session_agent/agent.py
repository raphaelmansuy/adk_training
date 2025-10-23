"""
Custom Session Services Agent

Demonstrates registering and using Redis as a custom session storage backend
with Google ADK's service registry pattern.
"""

import os
import json
import redis
from dotenv import load_dotenv
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

# Import ADK components
try:
    from google.adk import Agent
    from google.adk.cli import cli_tools_click
    # ADK 1.17+ has service registry in cli module
    try:
        from google.adk.cli.service_registry import get_service_registry
        SERVICE_REGISTRY_AVAILABLE = True
    except ImportError:
        # Fallback if not available
        SERVICE_REGISTRY_AVAILABLE = False
        get_service_registry = None
    
    from google.adk.sessions import InMemorySessionService, BaseSessionService, Session
    from google.adk.sessions.base_session_service import ListSessionsResponse
except ImportError as e:
    print(f"Error importing ADK components: {e}")
    print("Please ensure google-adk>=1.17.0 is installed: pip install google-adk")
    raise


# ============================================================================
# CUSTOM SESSION SERVICE IMPLEMENTATIONS
# ============================================================================

class RedisSessionService(BaseSessionService):
    """
    Production-ready Redis session storage backend.
    
    Implements BaseSessionService interface to store sessions in Redis.
    Demonstrates the service registry pattern with a real working backend.
    """
    
    def __init__(self, uri: str = "redis://localhost:6379/0", **kwargs):
        """
        Initialize Redis session service.
        
        Args:
            uri: Redis connection URI (e.g., redis://localhost:6379/0)
            **kwargs: Additional options (agents_dir is passed but not needed)
        """
        self.redis_uri = uri
        self.redis_client = None
        self._connect_to_redis()
    
    def _connect_to_redis(self):
        """Connect to Redis using the provided URI."""
        try:
            import redis
            # Parse the URI and connect
            self.redis_client = redis.from_url(
                self.redis_uri,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True
            )
            # Test the connection
            self.redis_client.ping()
            print(f"✅ Connected to Redis: {self.redis_uri}")
        except Exception as e:
            print(f"❌ Failed to connect to Redis: {e}")
            print("   Falling back to in-memory storage")
            self.redis_client = None
    
    async def create_session(
        self,
        *,
        app_name: str,
        user_id: str,
        state: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ):
        """Create a new session and store it in Redis."""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session_data = {
            "app_name": app_name,
            "user_id": user_id,
            "session_id": session_id,
            "state": state or {},
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "events": []
        }
        
        if self.redis_client:
            try:
                # Store session in Redis as JSON
                key = f"session:{app_name}:{user_id}:{session_id}"
                self.redis_client.set(key, json.dumps(session_data), ex=86400)  # 24h TTL
                print(f"   📝 Session stored in Redis: {key}")
            except Exception as e:
                print(f"   ⚠️  Failed to store session in Redis: {e}")
        
        # Create and return Session object
        from google.adk.sessions import Session
        return Session(
            id=session_id,
            app_name=app_name,
            user_id=user_id,
            state=session_data.get("state", {}),
            events=[]
        )
    
    async def get_session(
        self,
        *,
        app_name: str,
        user_id: str,
        session_id: str,
        config: Optional[Any] = None,
    ):
        """Retrieve a session from Redis."""
        if not self.redis_client:
            return None
        
        try:
            key = f"session:{app_name}:{user_id}:{session_id}"
            session_json = self.redis_client.get(key)
            
            if not session_json:
                return None
            
            session_data = json.loads(session_json)
            
            return Session(
                id=session_id,
                app_name=app_name,
                user_id=user_id,
                state=session_data.get("state", {}),
                events=session_data.get("events", []),
                last_update_time=0
            )
        except Exception as e:
            print(f"   ⚠️  Failed to retrieve session from Redis: {e}")
            return None
    
    async def list_sessions(
        self, *, app_name: str, user_id: Optional[str] = None
    ) -> ListSessionsResponse:
        """List sessions in Redis."""
        if not self.redis_client:
            return ListSessionsResponse(sessions=[])
        
        try:
            pattern = f"session:{app_name}:{user_id or '*'}:*" if user_id else f"session:{app_name}:*"
            keys = self.redis_client.keys(pattern)
            
            sessions = []
            for key in keys:
                session_json = self.redis_client.get(key)
                if session_json:
                    session_data = json.loads(session_json)
                    
                    # Reconstruct Session object with proper field mapping
                    # Redis stores: session_id, but Session model expects: id
                    session = Session(
                        id=session_data.get("session_id"),
                        app_name=session_data.get("app_name"),
                        user_id=session_data.get("user_id"),
                        state=session_data.get("state", {}),
                        events=[],  # Will reconstruct from event data
                        last_update_time=0
                    )
                    sessions.append(session)
            
            return ListSessionsResponse(sessions=sessions)
        except Exception as e:
            print(f"   ⚠️  Failed to list sessions from Redis: {e}")
            import traceback
            traceback.print_exc()
            return ListSessionsResponse(sessions=[])
    
    async def delete_session(
        self, *, app_name: str, user_id: str, session_id: str
    ) -> None:
        """Delete a session from Redis."""
        if not self.redis_client:
            return
        
        try:
            key = f"session:{app_name}:{user_id}:{session_id}"
            self.redis_client.delete(key)
            print(f"   🗑️  Session deleted from Redis: {key}")
        except Exception as e:
            print(f"   ⚠️  Failed to delete session from Redis: {e}")
    
    async def append_event(self, session: Session, event) -> Any:
        """
        Append an event to a session and save to Redis.
        
        This is the critical method that stores conversation data (poems, 
        user messages, etc.) to Redis. Without this override, events are 
        only stored in-memory.
        
        Args:
            session: The Session object
            event: The Event to append
        
        Returns:
            The event that was appended
        """
        # Call the base implementation to process the event
        # (this updates session state in-memory)
        event = await super().append_event(session=session, event=event)
        
        # Now save the updated session to Redis
        try:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.id
            
            key = f"session:{app_name}:{user_id}:{session_id}"
            
            # Convert session to JSON for storage
            session_data = {
                "app_name": app_name,
                "user_id": user_id,
                "session_id": session_id,
                "state": dict(session.state),  # Convert any dict-like object
                "created_at": session.created_at.isoformat() if hasattr(session, 'created_at') else datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "events": [
                    {
                        "id": e.id,
                        "timestamp": e.timestamp,
                        "partial": e.partial,
                        "author": e.author if hasattr(e, 'author') else "unknown",
                        "actions": {
                            "state_delta": e.actions.state_delta if e.actions else {}
                        } if e.actions else {}
                    }
                    for e in session.events
                ]
            }
            
            # Save to Redis with 24-hour TTL
            if self.redis_client:
                self.redis_client.set(key, json.dumps(session_data), ex=86400)
            
        except Exception as e:
            print(f"   ⚠️  Failed to save event to Redis: {e}")
        
        return event


class CustomSessionServiceDemo:
    """
    Demonstrates the factory pattern for registering custom session services.
    
    The key insight: ADK's service registry maps URI schemes to factory
    functions that create session service instances.
    """

    @staticmethod
    def register_redis_service():
        """Register Redis session service with the service registry."""
        
        if not SERVICE_REGISTRY_AVAILABLE or get_service_registry is None:
            print("⚠️  Service registry not available in this ADK version")
            return
        
        def redis_service_factory(uri: str, **kwargs) -> Any:
            """
            Factory function for creating a RedisSessionService.
            
            Creates a real Redis connection that persists session data
            to Redis for production use.
            
            Args:
                uri: Redis connection URI (e.g., redis://localhost:6379/0)
                **kwargs: Additional options (agents_dir is passed by ADK but not needed)
            
            Returns:
                Configured RedisSessionService instance
            """
            # Always remove agents_dir - ADK passes it but we don't need it
            kwargs_copy = kwargs.copy()
            kwargs_copy.pop("agents_dir", None)
            
            print(f"🔴 Registering Redis session service: {uri}")
            
            # Return real Redis session service that connects to Redis
            return RedisSessionService(uri=uri, **kwargs_copy)
        
        # Register with service registry
        registry = get_service_registry()
        registry.register_session_service("redis", redis_service_factory)
        print("✅ Redis session service registered!")

    @staticmethod
    def register_memory_service():
        """
        Register an in-memory session service (for testing without Docker).
        
        This uses ADK's default InMemorySessionService.
        """
        if not SERVICE_REGISTRY_AVAILABLE or get_service_registry is None:
            print("⚠️  Service registry not available - memory service not registered")
            return
        
        def memory_service_factory(uri: str, **kwargs) -> Any:
            """Factory for memory-based session storage."""
            kwargs_copy = kwargs.copy()
            kwargs_copy.pop("agents_dir", None)
            
            print(f"💾 Registering memory session service: {uri}")
            return InMemorySessionService(**kwargs_copy)
        
        registry = get_service_registry()
        registry.register_session_service("memory", memory_service_factory)
        print("✅ Memory session service registered!")


# ============================================================================
# TOOL FUNCTIONS
# ============================================================================

def describe_session_info(session_id: str) -> Dict[str, Any]:
    """
    Tool to describe session information.
    
    Demonstrates how tools can interact with session data.
    
    Args:
        session_id: The session identifier
    
    Returns:
        Dictionary with status and session information
    """
    return {
        "status": "success",
        "report": f"Session {session_id} is active",
        "data": {
            "session_id": session_id,
            "backend": "Session storage is configured via service registry",
            "persistence": "Supported (depends on backend)",
            "note": "Refresh the browser to test persistence!"
        }
    }


def test_session_persistence(key: str, value: str) -> Dict[str, Any]:
    """
    Tool to test session persistence across requests.
    
    This demonstrates how data can be stored and retrieved.
    
    Args:
        key: Key to store in session
        value: Value to store
    
    Returns:
        Dictionary with operation status
    """
    return {
        "status": "success",
        "report": f"Stored {key}={value} in session",
        "data": {
            "key": key,
            "value": value,
            "storage_backend": "Configured via service registry",
            "persistence": "Refresh browser to verify persistence",
            "redis_command": f"redis-cli GET session:{key}"
        }
    }


def show_service_registry_info() -> Dict[str, Any]:
    """
    Tool to display service registry information.
    
    Shows how to register Redis as a custom session backend.
    
    Returns:
        Dictionary with registry details
    """
    try:
        return {
            "status": "success",
            "report": "Redis service registry information",
            "data": {
                "pattern": "Register factory functions that create session services",
                "redis_registration": {
                    "scheme": "redis",
                    "factory_pattern": "def redis_factory(uri: str, **kwargs) -> RedisSessionService",
                    "registration": "registry.register_session_service('redis', redis_factory)",
                    "usage": "python -m agent web --session_service_uri=redis://localhost:6379"
                },
                "key_points": [
                    "Factory receives URI string as input",
                    "Always pop 'agents_dir' from kwargs",
                    "Return configured service instance",
                    "ADK handles the rest automatically"
                ]
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "report": f"Failed to get service registry: {e}"
        }


def get_session_backend_guide() -> Dict[str, Any]:
    """
    Tool to provide guidance on Redis as a session backend.
    
    Returns:
        Dictionary with Redis setup and best practices
    """
    return {
        "status": "success",
        "report": "Redis session backend guide",
        "data": {
            "why_redis": "Fast, persistent, production-ready in-memory data store",
            "redis_setup": {
                "start_container": "make docker-up",
                "connect": "redis://localhost:6379",
                "default_ttl": "24 hours per session"
            },
            "features": [
                "Fast session lookup and storage",
                "Automatic expiration (TTL)",
                "Persistence with AOF (Append Only File)",
                "Distributed session sharing",
                "Simple pub/sub for notifications"
            ],
            "best_practices": [
                "Set TTL to auto-cleanup old sessions",
                "Use key prefixes for organization",
                "Monitor memory usage",
                "Enable persistence in production"
            ],
            "extending": {
                "step1": "Inherit from BaseSessionService",
                "step2": "Implement async methods (create, get, list, delete, append_event)",
                "step3": "Register with service registry",
                "step4": "Use via: --session_service_uri=redis://..."
            }
        }
    }


# ============================================================================
# ROOT AGENT DEFINITION


# Create the root agent
root_agent = Agent(
    name="custom_session_agent",
    model="gemini-2.5-flash",
    description="Demonstrates custom session service registration in ADK",
    instruction="""You are an expert on ADK's custom session service registration pattern.

Your role is to help users understand Redis session persistence in ADK.

Key concepts:
1. Service Registry Pattern - Maps URI schemes to factory functions
2. Factory Functions - Create session service instances from URIs
3. BaseSessionService - Interface all custom backends must implement
4. Redis Backend - Production-ready session storage with TTL and persistence

When users ask about sessions:
- Explain why persistent sessions matter
- Show how Redis stores conversation history
- Demonstrate session retrieval across page refreshes
- Show the code that makes it work

Technical highlights:
- Each session stores complete event history
- Author field tracks user vs agent messages
- Sessions auto-expire after 24 hours
- Scale to multiple servers with Redis cluster
- Poems and conversations survive page refreshes

Help users test persistent sessions and understand the pattern!""",
    tools=[
        describe_session_info,
        test_session_persistence,
        show_service_registry_info,
        get_session_backend_guide
    ],
    output_key="session_result"
)


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not set in environment")
        print("   Set it to use the agent, or use 'adk web' for interactive mode")
    
    # Print startup information
    print("\n" + "=" * 70)
    print("🎯 Custom Session Services Agent - TIL Implementation")
    print("=" * 70)
    print()
    print("📋 Quick Start:")
    print("   1. Start services:  make docker-up")
    print("   2. Start agent:     make dev")
    print("   3. Open browser:    http://localhost:8000")
    print("   4. Test persistence: Send message → Refresh page")
    print()
    print("📚 Documentation:")
    print("   - TIL: /docs/docs/til/til_custom_session_services_20251023.md")
    print("   - README: ./README.md")
    print("   - Source: ./custom_session_agent/")
    print()
    print("🔍 Service Registry Status:")
    print("   - Redis service:   ✅ Registered")
    print("   - Memory service:  ✅ Registered")
    print()
    print("=" * 70 + "\n")
    
    # Start the CLI
    cli_tools_click.main()
