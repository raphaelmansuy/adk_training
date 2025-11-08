"""
File Search Store management utilities.

Provides functions to create, list, retrieve, and manage File Search Stores
for organizing policy documents by department or type.
"""

import time
import mimetypes
from typing import Optional, Dict, Any
from google import genai
from loguru import logger

from policy_navigator.config import Config


class StoreManager:
    """Manager for File Search Stores."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Store Manager.

        Args:
            api_key: Google API key (uses Config.GOOGLE_API_KEY if not provided)
        """
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.client = genai.Client(api_key=self.api_key)

    def create_policy_store(
        self, display_name: str, description: str = ""
    ) -> str:
        """
        Create a new File Search Store for policies.

        Args:
            display_name: Human-readable name for the store
            description: Description of the store purpose

        Returns:
            str: Store name (e.g., 'fileSearchStores/xxxxx')
        """
        try:
            logger.info(f"Creating File Search Store: {display_name}")

            store = self.client.file_search_stores.create(
                config={"display_name": display_name}
            )

            logger.info(f"✓ Store created: {store.name}")
            return store.name

        except Exception as e:
            logger.error(f"Failed to create store: {str(e)}")
            raise

    def get_store_info(self, store_name: str) -> Dict[str, Any]:
        """
        Get information about a File Search Store.

        Args:
            store_name: Full store name (e.g., 'fileSearchStores/xxxxx')

        Returns:
            dict: Store information
        """
        try:
            store = self.client.file_search_stores.get(name=store_name)
            return {
                "name": store.name,
                "display_name": getattr(store, "display_name", ""),
                "create_time": getattr(store, "create_time", ""),
                "update_time": getattr(store, "update_time", ""),
            }
        except Exception as e:
            logger.error(f"Failed to get store info: {str(e)}")
            raise

    def list_stores(self) -> list:
        """
        List all File Search Stores.

        Returns:
            list: List of store information dicts
        """
        try:
            stores = self.client.file_search_stores.list()
            store_list = []

            for store in stores:
                store_list.append(
                    {
                        "name": store.name,
                        "display_name": getattr(store, "display_name", ""),
                        "create_time": getattr(store, "create_time", ""),
                    }
                )

            logger.info(f"Found {len(store_list)} stores")
            return store_list

        except Exception as e:
            logger.error(f"Failed to list stores: {str(e)}")
            raise

    def get_store_by_display_name(self, display_name: str) -> Optional[str]:
        """
        Find a File Search Store by its display name.

        Returns the most recently created store if multiple stores have the same display name.

        Args:
            display_name: Display name of the store to find

        Returns:
            str: Full store name (e.g., 'fileSearchStores/xxxxx') or None if not found
        """
        try:
            stores = self.list_stores()
            matching_stores = [s for s in stores if s.get("display_name") == display_name]
            
            if not matching_stores:
                logger.warning(f"Store with display name '{display_name}' not found")
                return None
            
            # Return the most recently created store (latest create_time)
            most_recent = max(
                matching_stores, 
                key=lambda s: s.get("create_time", "")
            )
            return most_recent.get("name")
        except Exception as e:
            logger.error(f"Failed to find store by display name: {str(e)}")
            return None

    def delete_store(self, store_name: str) -> bool:
        """
        Delete a File Search Store.

        Args:
            store_name: Full store name (e.g., 'fileSearchStores/xxxxx')

        Returns:
            bool: True if deletion successful
        """
        try:
            logger.warning(f"Deleting File Search Store: {store_name}")
            self.client.file_search_stores.delete(name=store_name)
            logger.info("✓ Store deleted")
            return True
        except Exception as e:
            logger.error(f"Failed to delete store: {str(e)}")
            raise

    def upload_file_to_store(
        self,
        file_path: str,
        store_name: str,
        display_name: Optional[str] = None,
        metadata: Optional[list] = None,
    ) -> bool:
        """
        Upload a file to a File Search Store.

        Args:
            file_path: Path to the file to upload
            store_name: Target File Search Store name
            display_name: Optional display name for the document
            metadata: Optional custom metadata for the document

        Returns:
            bool: True if upload successful
        """
        try:
            if display_name is None:
                display_name = file_path.split("/")[-1]

            logger.info(f"Uploading {file_path} to store...")

            # Detect mime type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                # Set default mime types for common policy file types
                if file_path.endswith('.md'):
                    mime_type = 'text/markdown'
                elif file_path.endswith('.txt'):
                    mime_type = 'text/plain'
                elif file_path.endswith('.pdf'):
                    mime_type = 'application/pdf'
                else:
                    mime_type = 'text/plain'  # Default fallback

            with open(file_path, "rb") as f:
                config = {"display_name": display_name, "mime_type": mime_type}

                if metadata:
                    config["custom_metadata"] = metadata

                operation = (
                    self.client.file_search_stores.upload_to_file_search_store(
                        file=f, 
                        file_search_store_name=store_name, 
                        config=config
                    )
                )

            # Wait for indexing to complete
            timeout = time.time() + Config.INDEXING_TIMEOUT_SECONDS
            while not operation.done:
                if time.time() > timeout:
                    logger.error("Upload timeout")
                    return False

                time.sleep(2)
                operation = self.client.operations.get(operation)

            logger.info(f"✓ {display_name} uploaded and indexed")
            return True

        except Exception as e:
            logger.error(f"Failed to upload file: {str(e)}")
            raise

    def wait_for_operation(self, operation_name: str, timeout: int = 300) -> bool:
        """
        Wait for a File Search operation to complete.

        Args:
            operation_name: Name of the operation
            timeout: Timeout in seconds

        Returns:
            bool: True if operation completed successfully
        """
        try:
            start_time = time.time()

            while time.time() - start_time < timeout:
                operation = self.client.operations.get(operation_name)

                if operation.done:
                    logger.info("✓ Operation completed")
                    return True

                time.sleep(2)

            logger.error("Operation timeout")
            return False

        except Exception as e:
            logger.error(f"Failed to wait for operation: {str(e)}")
            raise


# Convenience functions
_store_manager: Optional[StoreManager] = None


def _get_manager() -> StoreManager:
    """Get or create StoreManager instance."""
    global _store_manager
    if _store_manager is None:
        _store_manager = StoreManager()
    return _store_manager


def create_policy_store(display_name: str, description: str = "") -> str:
    """Create a new File Search Store."""
    return _get_manager().create_policy_store(display_name, description)


def get_store_info(store_name: str) -> Dict[str, Any]:
    """Get information about a store."""
    return _get_manager().get_store_info(store_name)


def list_stores() -> list:
    """List all File Search Stores."""
    return _get_manager().list_stores()


def delete_store(store_name: str) -> bool:
    """Delete a File Search Store."""
    return _get_manager().delete_store(store_name)


def upload_file_to_store(
    file_path: str,
    store_name: str,
    display_name: Optional[str] = None,
    metadata: Optional[list] = None,
) -> bool:
    """Upload a file to a store."""
    return _get_manager().upload_file_to_store(
        file_path, store_name, display_name, metadata
    )
