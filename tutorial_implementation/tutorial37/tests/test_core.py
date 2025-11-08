"""
Unit tests for Policy Navigator tools and utilities.

Tests core functionality of policy management tools without requiring live API.
"""

import pytest
from unittest.mock import Mock, patch
from policy_navigator.metadata import MetadataSchema, PolicyDepartment, PolicyType
from policy_navigator.stores import StoreManager
from policy_navigator.utils import (
    get_sample_policies_dir,
    get_store_name_for_policy,
    format_response,
)


class TestMetadataSchema:
    """Tests for metadata schema generation."""

    def test_get_schema(self):
        """Test schema definition."""
        schema = MetadataSchema.get_schema()
        assert isinstance(schema, dict)
        assert "department" in schema
        assert "policy_type" in schema
        assert "effective_date" in schema
        assert schema["department"] == "string"
        assert schema["version"] == "numeric"

    def test_create_metadata(self):
        """Test metadata creation."""
        metadata = MetadataSchema.create_metadata(
            department="HR",
            policy_type="handbook",
            jurisdiction="US",
            version=2,
        )

        assert isinstance(metadata, list)
        assert len(metadata) > 0

        # Check specific fields
        dept_meta = next((m for m in metadata if m["key"] == "department"), None)
        assert dept_meta is not None
        assert dept_meta["string_value"] == "HR"

        version_meta = next((m for m in metadata if m["key"] == "version"), None)
        assert version_meta is not None
        assert version_meta["numeric_value"] == 2

    def test_hr_metadata(self):
        """Test HR metadata preset."""
        metadata = MetadataSchema.hr_metadata()
        assert isinstance(metadata, list)

        dept_meta = next((m for m in metadata if m["key"] == "department"), None)
        assert dept_meta["string_value"] == "HR"

    def test_it_metadata(self):
        """Test IT metadata preset."""
        metadata = MetadataSchema.it_metadata()
        assert isinstance(metadata, list)

        dept_meta = next((m for m in metadata if m["key"] == "department"), None)
        assert dept_meta["string_value"] == "IT"

    def test_code_of_conduct_metadata(self):
        """Test code of conduct metadata preset."""
        metadata = MetadataSchema.code_of_conduct_metadata()
        assert isinstance(metadata, list)

        type_meta = next((m for m in metadata if m["key"] == "policy_type"), None)
        assert type_meta["string_value"] == "code_of_conduct"

    def test_build_metadata_filter_single(self):
        """Test building single metadata filter."""
        filter_str = MetadataSchema.build_metadata_filter(department="HR")
        assert "department=" in filter_str
        assert "HR" in filter_str

    def test_build_metadata_filter_multiple(self):
        """Test building multiple metadata filters."""
        filter_str = MetadataSchema.build_metadata_filter(
            department="HR",
            policy_type="handbook",
            sensitivity="internal",
        )

        assert "department=" in filter_str
        assert "policy_type=" in filter_str
        assert "sensitivity=" in filter_str
        assert " AND " in filter_str

    def test_build_metadata_filter_empty(self):
        """Test building empty metadata filter."""
        filter_str = MetadataSchema.build_metadata_filter()
        assert filter_str == ""


class TestUtils:
    """Tests for utility functions."""

    def test_get_sample_policies_dir(self):
        """Test getting sample policies directory."""
        dir_path = get_sample_policies_dir()
        assert isinstance(dir_path, str)
        assert "sample_policies" in dir_path

    def test_get_store_name_for_policy_hr(self):
        """Test store name detection for HR policy."""
        store = get_store_name_for_policy("hr_handbook.md")
        assert "hr" in store.lower()

    def test_get_store_name_for_policy_it(self):
        """Test store name detection for IT policy."""
        store = get_store_name_for_policy("it_security_policy.pdf")
        assert "it" in store.lower()

    def test_get_store_name_for_policy_remote(self):
        """Test store name detection for remote work policy."""
        store = get_store_name_for_policy("remote_work_policy.md")
        assert "hr" in store.lower()

    def test_get_store_name_for_policy_conduct(self):
        """Test store name detection for code of conduct."""
        store = get_store_name_for_policy("code_of_conduct.md")
        assert "safety" in store.lower() or "general" in store.lower()

    def test_format_response_success(self):
        """Test formatting success response."""
        response = format_response("success", "Operation completed", {"count": 5})
        assert "✓" in response
        assert "Operation completed" in response
        assert "count" in response

    def test_format_response_error(self):
        """Test formatting error response."""
        response = format_response("error", "Operation failed", {"reason": "Invalid input"})
        assert "✗" in response
        assert "Operation failed" in response

    def test_format_response_warning(self):
        """Test formatting warning response."""
        response = format_response("warning", "Check this", {"info": "details"})
        assert "⚠" in response
        assert "Check this" in response


class TestEnums:
    """Tests for enum definitions."""

    def test_policy_department_enum(self):
        """Test PolicyDepartment enum."""
        assert PolicyDepartment.HR.value == "HR"
        assert PolicyDepartment.IT.value == "IT"
        assert PolicyDepartment.LEGAL.value == "Legal"
        assert PolicyDepartment.SAFETY.value == "Safety"

    def test_policy_type_enum(self):
        """Test PolicyType enum."""
        assert PolicyType.HANDBOOK.value == "handbook"
        assert PolicyType.PROCEDURE.value == "procedure"
        assert PolicyType.CODE_OF_CONDUCT.value == "code_of_conduct"


class TestConfig:
    """Tests for configuration."""

    def test_config_has_api_key_setting(self):
        """Test config has API key setting."""
        from policy_navigator.config import Config

        assert hasattr(Config, "GOOGLE_API_KEY")
        assert hasattr(Config, "DEFAULT_MODEL")
        assert hasattr(Config, "LOG_LEVEL")

    def test_config_get_store_names(self):
        """Test getting all store names."""
        from policy_navigator.config import Config

        stores = Config.get_store_names()
        assert isinstance(stores, dict)
        assert "hr" in stores
        assert "it" in stores
        assert "legal" in stores
        assert "safety" in stores


# Integration tests (mark as such so they can be skipped in CI without API key)


@pytest.mark.integration
class TestStoreManagerIntegration:
    """Integration tests for StoreManager (requires API key)."""

    @pytest.fixture
    def store_manager(self):
        """Create StoreManager for testing."""
        return StoreManager()

    def test_list_stores_returns_list(self, store_manager):
        """Test listing stores returns a list."""
        stores = store_manager.list_stores()
        assert isinstance(stores, list)

    def test_list_documents_mock(self, store_manager):
        """Test list_documents method with mocked API."""
        with patch.object(store_manager.client.file_search_stores.documents, 'list') as mock_list:
            # Mock the response
            mock_doc = Mock()
            mock_doc.name = 'fileSearchStores/123/documents/abc'
            mock_doc.display_name = 'test_document'
            mock_doc.create_time = '2025-01-01T00:00:00Z'
            mock_doc.update_time = '2025-01-01T00:00:00Z'
            mock_doc.state = 'ACTIVE'
            mock_doc.size_bytes = 1024
            
            mock_list.return_value = [mock_doc]
            
            docs = store_manager.list_documents('fileSearchStores/123')
            assert isinstance(docs, list)
            assert len(docs) == 1
            assert docs[0]['display_name'] == 'test_document'

    def test_find_document_by_display_name_mock(self, store_manager):
        """Test find_document_by_display_name with mocked API."""
        with patch.object(store_manager, 'list_documents') as mock_list:
            mock_list.return_value = [
                {
                    'name': 'fileSearchStores/123/documents/abc',
                    'display_name': 'policy1.md',
                    'create_time': '2025-01-01T00:00:00Z',
                }
            ]
            
            result = store_manager.find_document_by_display_name('fileSearchStores/123', 'policy1.md')
            assert result == 'fileSearchStores/123/documents/abc'

    def test_find_document_by_display_name_not_found(self, store_manager):
        """Test find_document_by_display_name when document not found."""
        with patch.object(store_manager, 'list_documents') as mock_list:
            mock_list.return_value = []
            
            result = store_manager.find_document_by_display_name('fileSearchStores/123', 'nonexistent.md')
            assert result is None

    def test_delete_document_mock(self, store_manager):
        """Test delete_document method with mocked API."""
        with patch.object(store_manager.client.file_search_stores.documents, 'delete') as mock_delete:
            mock_delete.return_value = None
            
            result = store_manager.delete_document('fileSearchStores/123/documents/abc')
            assert result is True
            mock_delete.assert_called_once()

    def test_upsert_file_to_store_new_document(self, store_manager):
        """Test upsert when document doesn't exist (new upload)."""
        with patch.object(store_manager, 'find_document_by_display_name') as mock_find, \
             patch.object(store_manager, 'upload_file_to_store') as mock_upload:
            
            # Document doesn't exist
            mock_find.return_value = None
            mock_upload.return_value = True
            
            # Create a temporary test file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write('test content')
                temp_file = f.name
            
            try:
                result = store_manager.upsert_file_to_store(
                    temp_file, 'fileSearchStores/123', 'test.md'
                )
                
                # Should only call upload, not delete
                assert result is True
                mock_find.assert_called_once()
                mock_upload.assert_called_once()
            finally:
                import os
                os.unlink(temp_file)

    def test_upsert_file_to_store_existing_document(self, store_manager):
        """Test upsert when document exists (replacement)."""
        with patch.object(store_manager, 'find_document_by_display_name') as mock_find, \
             patch.object(store_manager, 'delete_document') as mock_delete, \
             patch.object(store_manager, 'upload_file_to_store') as mock_upload, \
             patch('time.sleep'):  # Mock sleep to speed up test
            
            # Document exists
            mock_find.return_value = 'fileSearchStores/123/documents/old'
            mock_delete.return_value = True
            mock_upload.return_value = True
            
            # Create a temporary test file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write('updated content')
                temp_file = f.name
            
            try:
                result = store_manager.upsert_file_to_store(
                    temp_file, 'fileSearchStores/123', 'test.md'
                )
                
                # Should call find, delete, and upload
                assert result is True
                mock_find.assert_called_once()
                mock_delete.assert_called_once()
                mock_upload.assert_called_once()
            finally:
                import os
                os.unlink(temp_file)


@pytest.mark.integration
class TestPolicyToolsIntegration:
    """Integration tests for PolicyTools (requires API key)."""

    @pytest.fixture
    def policy_tools(self):
        """Create PolicyTools for testing."""
        from policy_navigator.tools import PolicyTools

        return PolicyTools()

    def test_search_policies_returns_dict(self, policy_tools):
        """Test search returns properly formatted dict."""
        # This would require a populated store in test environment
        pass
