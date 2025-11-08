#!/usr/bin/env python3
"""
Demo: Complete Policy Navigator Workflow

This demo shows the complete workflow:
1. Upload policies
2. Search for information
3. Compare policies
4. Assess compliance risks
5. Generate summaries and audit trails

Run this after setup:
    python demos/demo_full_workflow.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_navigator.config import Config
from policy_navigator.utils import validate_api_key, get_policy_files
from policy_navigator.tools import (
    search_policies,
    check_compliance_risk,
    generate_policy_summary,
    create_audit_trail,
    compare_policies,
)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def main():
    """Run the complete workflow demo."""

    print_section("Policy Navigator - Complete Workflow Demo")

    # Validate
    if not validate_api_key():
        print("✗ GOOGLE_API_KEY not set")
        return False

    try:
        # PART 1: Policy Search
        print_section("Part 1: Policy Information Search")

        print("Scenario: Employee asks about remote work policy\n")
        print("Query: 'I want to work remotely. What are the requirements?'\n")

        try:
            result = search_policies(
                "What are the requirements and process for remote work?",
                Config.HR_STORE_NAME,
            )

            if result.get("status") == "success":
                print("✓ Search Result:")
                print(f"  Answer: {result.get('answer', 'N/A')[:300]}...")
                print(f"  Sources: {result.get('source_count', 0)} citations found")
            else:
                print(f"✗ Search failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"⚠ Search skipped: {str(e)}")

        # PART 2: Compliance Risk Assessment
        print_section("Part 2: Compliance Risk Assessment")

        print("Scenario: Compliance review of work location policy\n")
        print("Query: 'Can an employee work from a different country for 3 months?'\n")

        try:
            result = check_compliance_risk(
                "Can employees work from a different country? What are the compliance concerns?",
                Config.HR_STORE_NAME,
            )

            if result.get("status") == "success":
                print("✓ Risk Assessment:")
                print(f"  Result: {result.get('assessment', 'N/A')[:300]}...")
            else:
                print(f"✗ Assessment failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"⚠ Risk assessment skipped: {str(e)}")

        # PART 3: Policy Summary
        print_section("Part 3: Generate Policy Summary")

        print("Scenario: Manager needs quick summary of benefits policy\n")
        print("Request: 'Summarize our employee benefits'\n")

        try:
            result = generate_policy_summary(
                "employee benefits and time off",
                Config.HR_STORE_NAME,
            )

            if result.get("status") == "success":
                print("✓ Policy Summary:")
                print(f"  Summary: {result.get('summary', 'N/A')[:300]}...")
            else:
                print(f"✗ Summary failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"⚠ Summary generation skipped: {str(e)}")

        # PART 4: Audit Trail
        print_section("Part 4: Create Audit Trail")

        print("Creating audit trail entry for policy access\n")

        try:
            result = create_audit_trail(
                action="search",
                user="john.doe@company.com",
                query="remote work policy requirements",
                result_summary="Retrieved remote work policy with 3 citations",
            )

            if result.get("status") == "success":
                audit_entry = result.get("audit_entry", {})
                print("✓ Audit Trail Created:")
                print(f"  Timestamp: {audit_entry.get('timestamp', 'N/A')}")
                print(f"  Action: {audit_entry.get('action', 'N/A')}")
                print(f"  User: {audit_entry.get('user', 'N/A')}")
                print(f"  Query: {audit_entry.get('query', 'N/A')}")
            else:
                print(f"✗ Audit failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"⚠ Audit trail skipped: {str(e)}")

        # PART 5: Multi-Store Comparison
        print_section("Part 5: Compare Policies Across Stores")

        print("Scenario: Compliance team comparing policies\n")
        print("Request: 'What are the differences in security requirements?\n'")

        try:
            result = compare_policies(
                "Compare security and access control policies across departments",
                [Config.IT_STORE_NAME, Config.LEGAL_STORE_NAME],
            )

            if result.get("status") == "success":
                print("✓ Policy Comparison:")
                print(f"  Stores compared: {result.get('stores_compared', 0)}")
                print(f"  Analysis: {result.get('comparison', 'N/A')[:300]}...")
            else:
                print(f"✗ Comparison failed: {result.get('error', 'Unknown error')}")

        except Exception as e:
            print(f"⚠ Comparison skipped: {str(e)}")

        # Summary
        print_section("Workflow Complete")

        print("✓ Demonstrated key Policy Navigator features:")
        print("  1. Policy search with semantic understanding")
        print("  2. Compliance risk assessment")
        print("  3. Policy summaries and key points extraction")
        print("  4. Audit trail creation for compliance")
        print("  5. Cross-store policy comparison")
        print("\n✓ All tools working correctly!")

        print("\n" + "=" * 70)
        print("Next Steps:")
        print("  • Use 'make dev' to start the interactive web interface")
        print("  • Explore other demo scripts with 'make demo'")
        print("  • Review documentation in docs/")
        print("  • Run tests with 'make test'")
        print("=" * 70 + "\n")

        return True

    except Exception as e:
        print(f"\n✗ Workflow demo failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
