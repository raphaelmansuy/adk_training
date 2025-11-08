#!/usr/bin/env python3
"""
Demo: Search Policies Using File Search

This demo shows how to:
1. Search policies using semantic search
2. Filter policies by metadata
3. View citations and sources
4. Compare policies across stores

Run this demo after uploading policies:
    python demos/demo_search.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_navigator.config import Config
from policy_navigator.utils import validate_api_key
from policy_navigator.tools import (
    search_policies,
    filter_policies_by_metadata,
    compare_policies,
)


def print_result(title: str, result: dict):
    """Pretty print a result dictionary."""
    print(f"\n{title}")
    print("-" * 70)

    if result.get("status") == "error":
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
        return

    print(result.get("report", "Operation completed"))

    if "answer" in result:
        print(f"\nAnswer:\n{result['answer'][:500]}...")

    if "citations" in result and result["citations"]:
        print(f"\nCitations ({len(result['citations'])}):")
        for i, citation in enumerate(result["citations"][:3], 1):
            print(f"  {i}. {citation.get('source', 'Unknown source')[:100]}")

    if "results" in result:
        print(f"\nResults:\n{result['results'][:300]}...")


def main():
    """Run the search demo."""

    print("\n" + "=" * 70)
    print("Policy Navigator - Demo: Search Policies")
    print("=" * 70 + "\n")

    # Validate API key
    if not validate_api_key():
        print("✗ GOOGLE_API_KEY not set")
        return False

    try:
        # Test queries
        queries = [
            {
                "title": "Simple Policy Question",
                "query": "What are the vacation day policies?",
                "store": Config.HR_STORE_NAME,
                "type": "search",
            },
            {
                "title": "IT Security Question",
                "query": "What are our password requirements?",
                "store": Config.IT_STORE_NAME,
                "type": "search",
            },
            {
                "title": "Remote Work Policy",
                "query": "Can I work from home? What are the requirements?",
                "store": Config.HR_STORE_NAME,
                "type": "search",
            },
        ]

        print("Running example searches...\n")

        for i, test in enumerate(queries, 1):
            print(f"\nQuery {i}: {test['title']}")
            print("=" * 70)
            print(f"Question: {test['query']}")
            print(f"Store: {test['store']}")

            try:
                result = search_policies(test["query"], test["store"])
                print_result(f"Results:", result)

            except Exception as e:
                print(f"✗ Search failed: {str(e)}")

            print("\n")

        # Test filtering
        print("\n" + "=" * 70)
        print("Testing Metadata Filtering")
        print("=" * 70 + "\n")

        filter_tests = [
            {
                "title": "HR Policies Only",
                "params": {"store_name": Config.HR_STORE_NAME, "department": "HR"},
            },
            {
                "title": "IT Security Procedures",
                "params": {
                    "store_name": Config.IT_STORE_NAME,
                    "department": "IT",
                    "policy_type": "procedure",
                },
            },
        ]

        for test in filter_tests:
            print(f"\nFilter: {test['title']}")
            print("-" * 70)

            try:
                result = filter_policies_by_metadata(**test["params"])
                if result.get("status") == "success":
                    print(f"✓ Filter applied: {result.get('filter', 'N/A')}")
                    print(f"Results preview:\n{result.get('results', 'N/A')[:200]}...")
                else:
                    print(f"✗ Filter failed: {result.get('error', 'Unknown error')}")

            except Exception as e:
                print(f"✗ Error: {str(e)}")

        # Summary
        print("\n" + "=" * 70)
        print("Demo Complete")
        print("=" * 70)
        print("\n✓ Search operations demonstrated successfully!")
        print("\nFeatures shown:")
        print("  • Semantic search across policy documents")
        print("  • Citation tracking from source documents")
        print("  • Metadata filtering by department and type")
        print("  • Multi-document queries")
        print("\nNext steps:")
        print("  1. Run demo_full_workflow.py for complete workflow")
        print("  2. Use 'make dev' to start interactive web interface")
        print()

        return True

    except Exception as e:
        print(f"\n✗ Demo failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
