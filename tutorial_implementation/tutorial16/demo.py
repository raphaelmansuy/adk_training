#!/usr/bin/env python3
"""
Tutorial 16: MCP Integration - Demo Script
Demonstrates MCP filesystem operations and document organization.

Run with:
    python demo.py
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp_agent import root_agent


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_filesystem_operations():
    """Demonstrate basic filesystem operations via MCP."""
    print_header("MCP Filesystem Operations Demo")

    print("🚀 MCP Agent Configuration:")
    print(f"   Model: {root_agent.model}")
    print(f"   Name: {root_agent.name}")
    print(f"   Tools: {len(root_agent.tools)} MCP toolset(s)")
    print()

    print("📝 Available Operations:")
    print("   - List files in directory")
    print("   - Read file contents")
    print("   - Create new files")
    print("   - Search for files")
    print("   - Get file information")
    print("   - Move/rename files")
    print("   - Create directories")
    print()

    print("💡 Try these queries in ADK web interface:")
    print()
    print("1. List files:")
    print("   'List all files in the current directory'")
    print()
    print("2. Read a file:")
    print("   'Read the contents of README.md'")
    print()
    print("3. Create a file:")
    print("   'Create a test file called demo.txt with content: Hello MCP!'")
    print()
    print("4. Search files:")
    print("   'Find all Python files in this directory'")
    print()
    print("5. File info:")
    print("   'What is the size of requirements.txt?'")
    print()


def demo_connection_types():
    """Demonstrate different MCP connection types."""
    print_header("MCP Connection Types (ADK 1.16.0+)")

    print("📡 Available Connection Methods:")
    print()

    print("1. Stdio (Local):")
    print("   - Best for: Local development, file operations")
    print("   - Uses: Node.js npx command")
    print("   - Example: Filesystem, local databases")
    print()

    print("2. SSE (Server-Sent Events):")
    print("   - Best for: Real-time data streaming")
    print("   - Uses: HTTPS endpoint")
    print("   - Supports: OAuth2 authentication")
    print("   - Example: Live dashboards, monitoring")
    print()

    print("3. HTTP Streaming:")
    print("   - Best for: Bidirectional communication")
    print("   - Uses: HTTPS endpoint")
    print("   - Supports: OAuth2 authentication")
    print("   - Example: Interactive APIs, complex workflows")
    print()


def demo_authentication():
    """Demonstrate MCP authentication options."""
    print_header("MCP Authentication (Production)")

    print("🔐 Supported Authentication Methods:")
    print()

    print("1. OAuth2 (Recommended):")
    print("   - Most secure for production")
    print("   - Automatic token refresh")
    print("   - Supports scopes and permissions")
    print()

    print("2. Bearer Token:")
    print("   - Simple API authentication")
    print("   - Good for internal services")
    print()

    print("3. HTTP Basic:")
    print("   - Username/password authentication")
    print("   - Use for legacy systems only")
    print()

    print("4. API Key:")
    print("   - Header-based authentication")
    print("   - Common for cloud services")
    print()


def demo_best_practices():
    """Demonstrate MCP best practices."""
    print_header("MCP Best Practices")

    print("✅ DO:")
    print("   - Validate directory paths before connecting")
    print("   - Use OAuth2 for production deployments")
    print("   - Enable retry_on_closed_resource")
    print("   - Provide clear instructions to agents")
    print("   - Handle connection errors gracefully")
    print("   - Store credentials securely (env vars)")
    print()

    print("❌ DON'T:")
    print("   - Hardcode API keys or credentials")
    print("   - Ignore connection failures")
    print("   - Use Basic auth for internet-facing services")
    print("   - Share credentials across environments")
    print()


def demo_quick_start():
    """Show quick start commands."""
    print_header("Quick Start Guide")

    print("🚀 Get Started in 3 Steps:")
    print()

    print("1. Setup:")
    print("   $ make setup")
    print()

    print("2. Configure:")
    print("   $ cp mcp_agent/.env.example mcp_agent/.env")
    print("   # Edit .env and add your GOOGLE_API_KEY")
    print()

    print("3. Run:")
    print("   $ make dev")
    print("   # Open http://localhost:8000")
    print()

    print("📚 Resources:")
    print("   - Tutorial: docs/tutorial/16_mcp_integration.md")
    print("   - MCP Spec: https://spec.modelcontextprotocol.io/")
    print("   - Servers: https://github.com/modelcontextprotocol/servers")
    print()


def main():
    """Run all demos."""
    print("\n" + "🎓 " * 35)
    print("  Tutorial 16: Model Context Protocol (MCP) Integration")
    print("🎓 " * 35)

    try:
        demo_quick_start()
        demo_filesystem_operations()
        demo_connection_types()
        demo_authentication()
        demo_best_practices()

        print_header("Next Steps")
        print("✅ Ready to try MCP integration!")
        print()
        print("1. Run 'make dev' to start ADK server")
        print("2. Open http://localhost:8000 in your browser")
        print("3. Try the demo queries above")
        print("4. Explore other MCP servers from the community")
        print()
        print("📖 Continue to Tutorial 17: Agent-to-Agent Communication")
        print()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  - Ensure you've run 'make setup'")
        print("  - Check that Node.js and npx are installed")
        print("  - Verify your .env configuration")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
