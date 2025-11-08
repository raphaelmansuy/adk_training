#!/usr/bin/env python3
"""
Demo: Upload Policy Documents to File Search Store

This demo shows how to:
1. Create File Search Stores for different policy departments
2. Upload sample policy documents
3. Add metadata to documents
4. Verify successful uploads

Run this demo after setting GOOGLE_API_KEY in .env file:
    python demos/demo_upload.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_navigator.config import Config
from policy_navigator.utils import (
    validate_api_key,
    get_policy_files,
    get_store_name_for_policy,
)
from policy_navigator.stores import StoreManager
from policy_navigator.metadata import MetadataSchema


def main():
    """Run the upload demo."""

    print("\n" + "=" * 70)
    print("Policy Navigator - Demo: Upload Policy Documents")
    print("=" * 70 + "\n")

    # Validate API key
    if not validate_api_key():
        print("\n✗ GOOGLE_API_KEY not set. Please configure your API key.")
        print("  See .env.example for instructions.")
        return False

    try:
        store_manager = StoreManager()

        # Step 1: Create or reuse File Search Stores
        print("Step 1: Creating or Reusing File Search Stores")
        print("-" * 70)

        stores = {}
        for store_type, store_name in Config.get_store_names().items():
            print(f"  {store_type.upper()} store: {store_name}")
            try:
                # Check if store already exists (reuse pattern)
                existing_store = store_manager.get_store_by_display_name(store_name)
                if existing_store:
                    stores[store_type] = existing_store
                    print(f"    → Using existing store: {existing_store}\n")
                else:
                    # Create new store only if it doesn't exist
                    store_id = store_manager.create_policy_store(store_name)
                    stores[store_type] = store_id
                    print(f"    → Created new store: {store_id}\n")
            except Exception as e:
                print(f"    ✗ Failed: {str(e)}\n")

        # Step 2: Get policy files
        print("\nStep 2: Locating Policy Files")
        print("-" * 70)

        policy_files = get_policy_files()

        if not policy_files:
            print("  ✗ No policy files found in sample_policies/")
            return False

        print(f"  Found {len(policy_files)} policy files:")
        for pf in policy_files:
            print(f"    - {Path(pf).name}")

        # Step 3: Upload documents
        print("\n\nStep 3: Uploading Policy Documents")
        print("-" * 70)

        uploaded_count = 0
        for policy_file in policy_files:
            policy_name = Path(policy_file).name
            store_type = get_store_name_for_policy(policy_name)
            store_id = stores.get(store_type)

            if not store_id:
                print(f"\n  ✗ No store configured for {policy_name}")
                continue

            print(f"\n  Uploading: {policy_name}")
            print(f"    Store: {store_type}")

            # Get appropriate metadata
            if "hr" in policy_name.lower() or "handbook" in policy_name.lower():
                metadata = MetadataSchema.hr_metadata()
            elif "it" in policy_name.lower() or "security" in policy_name.lower():
                metadata = MetadataSchema.it_metadata()
            elif "remote" in policy_name.lower():
                metadata = MetadataSchema.remote_work_metadata()
            else:
                metadata = MetadataSchema.code_of_conduct_metadata()

            try:
                result = store_manager.upsert_file_to_store(
                    policy_file,
                    store_id,
                    display_name=policy_name,
                    metadata=metadata,
                )

                if result:
                    print("    ✓ Upsert successful")
                    uploaded_count += 1
                else:
                    print("    ✗ Upsert failed")

            except Exception as e:
                print(f"    ✗ Error: {str(e)}")

        # Step 4: List stores
        print("\n\nStep 4: Verifying Stores")
        print("-" * 70)

        try:
            all_stores = store_manager.list_stores()
            print(f"\n  Total File Search Stores: {len(all_stores)}")

            for store in all_stores:
                store_name = store.get("name", "Unknown")
                display_name = store.get("display_name", "Unknown")
                print(f"    - {display_name}")
                print(f"      ID: {store_name}")

        except Exception as e:
            print(f"  ✗ Failed to list stores: {str(e)}")

        # Summary
        print("\n\n" + "=" * 70)
        print("Demo Complete")
        print("=" * 70)
        print(f"\n✓ Successfully uploaded {uploaded_count}/{len(policy_files)} policies")
        print("\nNext steps:")
        print("  1. Run demo_search.py to test searching policies")
        print("  2. Run demo_full_workflow.py for complete workflow")
        print("  3. Use 'make dev' to start interactive web interface")
        print()

        return True

    except Exception as e:
        print(f"\n✗ Demo failed with error: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
