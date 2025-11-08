#!/usr/bin/env python3
"""
Demo: Search Policies Using File Search
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_navigator.config import Config
from policy_navigator.utils import validate_api_key
from policy_navigator.tools import search_policies, filter_policies_by_metadata
from policy_navigator.formatter import format_answer


def main():
    """Run the search demo."""
    # Suppress INFO logs
    import logging
    logging.getLogger("policy_navigator").setLevel(logging.WARNING)

    print("\n" + "=" * 70)
    print("Policy Navigator - Demo: Search Policies")
    print("=" * 70)

    if not validate_api_key():
        print("✗ GOOGLE_API_KEY not set")
        return False

    try:
        # Test queries
        print("\n🔍 Running Policy Searches\n")
        
        queries = [
            {
                "title": "What are the vacation day policies?",
                "store": Config.HR_STORE_NAME,
            },
            {
                "title": "What are our password requirements?",
                "store": Config.IT_STORE_NAME,
            },
            {
                "title": "Can I work from home? What are the requirements?",
                "store": Config.HR_STORE_NAME,
            },
        ]

        for test in queries:
            try:
                result = search_policies(test["title"], test["store"])
                formatted = format_answer(
                    question=test["title"],
                    answer=result.get("answer", ""),
                    citations=result.get("citations", []),
                    store_name=test["store"],
                )
                print(formatted)
            except Exception as e:
                print(f"\n✗ Search failed: {str(e)}\n")

        # Test filtering
        print("\n🔍 Policy Filtering Examples\n")
        print("=" * 70 + "\n")

        filter_tests = [
            {
                "title": "HR Department Policies",
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
            try:
                result = filter_policies_by_metadata(**test["params"])
                print(f"\n✓ {test['title']}")
                print("-" * 70)
                print(result.get("results", "No results"))
                print()
            except Exception as e:
                print(f"✗ Error: {str(e)}\n")

        print("=" * 70)
        print("✓ Demo Complete\n")
        return True

    except Exception as e:
        print(f"\n✗ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
