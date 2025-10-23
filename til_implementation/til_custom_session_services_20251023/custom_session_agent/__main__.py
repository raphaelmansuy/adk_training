"""
Entry point for custom_session_agent.

This script registers custom session services BEFORE ADK CLI initializes.
This ensures that when you run: python -m custom_session_agent web
The Redis service will be available for use.
"""

from custom_session_agent.agent import CustomSessionServiceDemo

try:
    from google.adk.cli import cli_tools_click
except ImportError:
    # Fallback for testing/development without ADK installed
    def cli_tools_click():
        pass


def main():
    """Main entry point that registers services before ADK CLI starts."""
    # Register custom services BEFORE ADK CLI initializes
    CustomSessionServiceDemo.register_redis_service()
    CustomSessionServiceDemo.register_memory_service()
    
    print("\n" + "=" * 70)
    print("🎯 Custom Session Services - Entry Point")
    print("=" * 70)
    print()
    print("✅ Redis service registered and ready!")
    print("✅ Memory service registered and ready!")
    print()
    print("To use custom session services:")
    print("  python -m custom_session_agent web --session_service_uri=redis://")
    print()
    print("=" * 70 + "\n")
    
    # Now start ADK CLI with services registered
    cli_tools_click.main()


if __name__ == "__main__":
    main()
