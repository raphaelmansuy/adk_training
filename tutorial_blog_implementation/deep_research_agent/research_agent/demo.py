"""
Demo script for Deep Research Agent

Usage:
    python -m research_agent.demo          # Run actual research (requires API key)
    python -m research_agent.demo --mock   # Run mock demo (no API key needed)
"""

import sys
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from package directory
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)


def mock_demo():
    """Run a mock demonstration without API calls."""
    print("=" * 60)
    print("🔬 Deep Research Agent Demo (Mock Mode)")
    print("=" * 60)
    print("")
    print("This demonstrates the structure without making API calls.")
    print("")
    
    # Simulate research structure
    print("📝 Query: 'Analyze AI code assistant market trends in 2025'")
    print("")
    print("🚀 Starting research...")
    print(f"   Interaction ID: mock-interaction-12345")
    print("")
    
    # Simulate thought process
    thoughts = [
        "Planning research strategy for AI code assistants market",
        "Searching for recent market reports and analysis",
        "Reading documentation from major providers: GitHub Copilot, Cursor, Codeium",
        "Analyzing pricing models and feature comparisons",
        "Synthesizing findings into comprehensive report",
    ]
    
    for i, thought in enumerate(thoughts, 1):
        time.sleep(0.5)  # Simulate processing
        print(f"💭 Thought {i}: {thought}")
    
    print("")
    print("📊 Research Report (Mock):")
    print("-" * 40)
    print("""
# AI Code Assistant Market Analysis 2025

## Executive Summary
The AI code assistant market has grown significantly, with adoption 
rates increasing 300% since 2023. Key players include GitHub Copilot,
Cursor, and Codeium.

## Key Players
| Provider | Pricing | Key Features |
|----------|---------|--------------|
| GitHub Copilot | $10-19/mo | IDE integration, chat |
| Cursor | $20/mo | AI-native editor |
| Codeium | Free tier | Multi-IDE support |

## Market Trends
1. Integration of agentic capabilities
2. Focus on enterprise security features
3. Shift toward specialized vertical solutions

## Future Outlook
Market expected to reach $15B by 2028 with 45% CAGR.
    """)
    print("-" * 40)
    print("")
    print("✅ Research complete (mock)")
    print("   Elapsed time: 3.2 seconds (simulated)")
    print("")
    print("💡 To run actual research, use: make research")
    print("   (requires GOOGLE_API_KEY to be set)")


def real_demo():
    """Run actual research with the API."""
    import os
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY not set!")
        print("")
        print("Set your API key:")
        print("  export GOOGLE_API_KEY='your-key-here'")
        print("")
        print("Or run mock demo:")
        print("  python -m research_agent.demo --mock")
        sys.exit(1)
    
    from . import DeepResearchAgent, ResearchStatus
    import os
    
    print("=" * 60)
    print("🔬 Deep Research Agent - Live Demo")
    print("=" * 60)
    print("")
    
    # Show which backend is being used
    use_vertex_ai = os.getenv("USE_VERTEX_AI", "false").lower() == "true"
    if use_vertex_ai:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("VERTEX_AI_PROJECT_ID")
        region = os.getenv("VERTEX_AI_REGION", "us-central1")
        print(f"📍 Backend: Vertex AI (project={project_id}, region={region})")
    else:
        print("📍 Backend: Google AI Studio")
    print("")
    print("⚠️  This will make actual API calls and may take several minutes.")
    print("")
    
    query = "What are the top 3 developments in large language models in December 2025? Please provide references and URLs for the sources you cite."
    print(f"📝 Query: '{query}'")
    print("")
    
    def status_callback(status: str, elapsed: float):
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        print(f"   [{mins:02d}:{secs:02d}] Status: {status}")
    
    print("🚀 Starting research...")
    print("")
    
    agent = DeepResearchAgent()
    
    try:
        result = agent.research(
            query,
            poll_interval=10,
            on_status=status_callback
        )
        
        print("")
        
        if result.status == ResearchStatus.COMPLETED:
            print("=" * 60)
            print("📊 Research Report")
            print("=" * 60)
            print("")
            print(result.report)
            print("")
            print("=" * 60)
            print(f"✅ Research complete!")
            print(f"   Interaction ID: {result.id}")
            print(f"   Elapsed time: {result.elapsed_seconds:.1f} seconds")
            print(f"   Citations found: {len(result.citations)}")
            
            if result.citations:
                print("")
                print("📚 Citations:")
                for i, citation in enumerate(result.citations[:10], 1):  # Show first 10
                    print(f"   {i}. {citation}")
                if len(result.citations) > 10:
                    print(f"   ... and {len(result.citations) - 10} more")
        else:
            print(f"❌ Research failed: {result.error}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    if "--mock" in sys.argv:
        mock_demo()
    else:
        real_demo()


if __name__ == "__main__":
    main()
