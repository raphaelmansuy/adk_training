#!/usr/bin/env python3
"""
Clean up all File Search stores for a fresh start.

This script deletes all File Search stores associated with the policy navigator,
allowing you to start from a completely fresh state.

Usage:
    python scripts/cleanup_stores.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_navigator.stores import StoreManager
from loguru import logger


def main():
    """Delete all File Search stores."""
    try:
        store_manager = StoreManager()

        print("\nFetching all File Search stores...")
        stores = store_manager.list_stores()

        if not stores:
            print("✓ No File Search stores to delete")
            return True

        print(f"\nFound {len(stores)} stores:")
        for store in stores:
            display_name = store.get("display_name", "Unknown")
            store_id = store.get("name", "Unknown")
            print(f"  - {display_name} ({store_id})")

        print(f"\nDeleting all {len(stores)} stores...")
        print("-" * 70)

        deleted_count = 0
        for store in stores:
            store_id = store.get("name")
            display_name = store.get("display_name", "Unknown")

            try:
                if store_manager.delete_store(store_id, force=True):
                    print(f"✓ Deleted: {display_name}")
                    deleted_count += 1
                else:
                    print(f"✗ Failed to delete: {display_name}")
            except Exception as e:
                print(f"✗ Error deleting {display_name}: {str(e)}")

        print("-" * 70)
        print(f"\n✓ Successfully deleted {deleted_count}/{len(stores)} stores")
        print("\nTo start fresh with new stores, run:")
        print("  make demo-upload")

        return True

    except Exception as e:
        logger.error(f"Failed to cleanup stores: {str(e)}")
        print(f"\n✗ Error: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
