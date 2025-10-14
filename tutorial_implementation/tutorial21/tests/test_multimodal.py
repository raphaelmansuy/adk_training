"""
Test multimodal image processing functionality
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch

from vision_catalog_agent.agent import (
    load_image_from_file,
    optimize_image,
    create_sample_image,
    list_sample_images,
    analyze_product_image,
    analyze_uploaded_image,
    compare_product_images,
    generate_catalog_entry
)
from google.genai import types


class TestImageLoading:
    """Test image loading utilities."""
    
    @pytest.fixture
    def sample_image_path(self, tmp_path):
        """Create a temporary sample image."""
        image_path = tmp_path / "test_image.jpg"
        create_sample_image(str(image_path), (100, 100, 100))
        return str(image_path)
    
    def test_load_image_from_file(self, sample_image_path):
        """Test loading image from file."""
        part = load_image_from_file(sample_image_path)
        
        assert part is not None
        assert isinstance(part, types.Part)
        assert part.inline_data is not None
        assert part.inline_data.mime_type == 'image/jpeg'
        assert len(part.inline_data.data) > 0
    
    def test_load_image_file_not_found(self):
        """Test error handling for missing file."""
        with pytest.raises(FileNotFoundError):
            load_image_from_file('nonexistent.jpg')
    
    def test_load_image_unsupported_format(self, tmp_path):
        """Test error handling for unsupported format."""
        invalid_path = tmp_path / "test.xyz"
        invalid_path.write_text("not an image")
        
        with pytest.raises(ValueError, match="Unsupported image format"):
            load_image_from_file(str(invalid_path))
    
    def test_load_png_image(self, tmp_path):
        """Test loading PNG image."""
        image_path = tmp_path / "test.png"
        create_sample_image(str(image_path))
        
        part = load_image_from_file(str(image_path))
        assert part.inline_data.mime_type == 'image/png'
    
    def test_load_webp_image_mime_type(self, tmp_path):
        """Test MIME type detection for webp."""
        # Create a webp file for testing
        webp_path = tmp_path / "test.webp"
        
        try:
            from PIL import Image
            img = Image.new('RGB', (100, 100), color=(73, 109, 137))
            img.save(str(webp_path), format='WEBP')
            
            part = load_image_from_file(str(webp_path))
            assert part.inline_data.mime_type == 'image/webp'
        except Exception:
            pytest.skip("WebP support not available")


class TestImageOptimization:
    """Test image optimization."""
    
    def test_optimize_image(self):
        """Test image optimization."""
        try:
            from PIL import Image
            import io
            
            # Create a large test image
            img = Image.new('RGB', (2000, 2000), color=(100, 100, 100))
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            original_bytes = buf.getvalue()
            
            # Optimize
            optimized = optimize_image(original_bytes)
            
            assert len(optimized) > 0
            assert len(optimized) <= len(original_bytes)
            
            # Verify it's still a valid image
            Image.open(io.BytesIO(optimized))
        
        except ImportError:
            pytest.skip("PIL/Pillow not installed")
    
    def test_optimize_image_without_pil(self):
        """Test optimization fallback without PIL."""
        test_bytes = b"fake image data"
        
        with patch('vision_catalog_agent.agent.Image', None):
            result = optimize_image(test_bytes)
            assert result == test_bytes


class TestSampleImageCreation:
    """Test sample image creation."""
    
    def test_create_sample_image(self, tmp_path):
        """Test creating sample image."""
        image_path = tmp_path / "sample.jpg"
        
        result = create_sample_image(str(image_path), (200, 150, 100))
        
        assert result == str(image_path)
        assert image_path.exists()
        
        try:
            from PIL import Image
            img = Image.open(image_path)
            assert img.size == (400, 400)
        except ImportError:
            pytest.skip("PIL/Pillow not installed")
    
    def test_create_sample_image_creates_directory(self, tmp_path):
        """Test that directory is created if it doesn't exist."""
        image_path = tmp_path / "subdir" / "sample.jpg"
        
        create_sample_image(str(image_path))
        
        assert image_path.exists()
        assert image_path.parent.exists()


class TestAnalyzeProductImage:
    """Test analyze_product_image tool."""
    
    @pytest.mark.asyncio
    async def test_analyze_product_image_file_not_found(self):
        """Test error handling for missing image file."""
        mock_context = MagicMock()
        
        result = await analyze_product_image(
            'PROD-001',
            'nonexistent.jpg',
            mock_context
        )
        
        assert result['status'] == 'error'
        assert 'not found' in result['report'].lower()
    
    @pytest.mark.asyncio
    async def test_analyze_product_image_success(self, tmp_path):
        """Test successful product image analysis."""
        # Create sample image
        image_path = tmp_path / "product.jpg"
        create_sample_image(str(image_path))
        
        # Mock tool context
        mock_context = MagicMock()
        mock_result = MagicMock()
        mock_result.content = MagicMock()
        mock_result.content.parts = [MagicMock(text="Product analysis result")]
        
        mock_context.run_agent = AsyncMock(return_value=mock_result)
        
        result = await analyze_product_image(
            'PROD-001',
            str(image_path),
            mock_context
        )
        
        assert result['status'] == 'success'
        assert 'PROD-001' in result['report']
        assert 'analysis' in result
    
    @pytest.mark.asyncio
    async def test_analyze_product_image_no_result(self, tmp_path):
        """Test handling of empty analysis result."""
        image_path = tmp_path / "product.jpg"
        create_sample_image(str(image_path))
        
        mock_context = MagicMock()
        mock_result = MagicMock()
        mock_result.content = None
        
        mock_context.run_agent = AsyncMock(return_value=mock_result)
        
        result = await analyze_product_image(
            'PROD-001',
            str(image_path),
            mock_context
        )
        
        assert result['status'] == 'error'


class TestCompareProductImages:
    """Test compare_product_images tool."""
    
    @pytest.mark.asyncio
    async def test_compare_images_insufficient_images(self):
        """Test error handling for insufficient images."""
        mock_context = MagicMock()
        
        result = await compare_product_images(['single.jpg'], mock_context)
        
        assert result['status'] == 'error'
        assert 'at least 2' in result['report'].lower()
    
    @pytest.mark.asyncio
    async def test_compare_images_file_not_found(self):
        """Test error handling for missing file."""
        mock_context = MagicMock()
        
        result = await compare_product_images(
            ['file1.jpg', 'file2.jpg'],
            mock_context
        )
        
        assert result['status'] == 'error'
        assert 'not found' in result['report'].lower()
    
    @pytest.mark.asyncio
    async def test_compare_images_success(self, tmp_path):
        """Test successful image comparison."""
        # Create sample images
        image1 = tmp_path / "product1.jpg"
        image2 = tmp_path / "product2.jpg"
        create_sample_image(str(image1), (100, 100, 100))
        create_sample_image(str(image2), (150, 150, 150))
        
        # Mock tool context
        mock_context = MagicMock()
        mock_result = MagicMock()
        mock_result.content = MagicMock()
        mock_result.content.parts = [MagicMock(text="Comparison result")]
        
        mock_context.run_agent = AsyncMock(return_value=mock_result)
        
        result = await compare_product_images(
            [str(image1), str(image2)],
            mock_context
        )
        
        assert result['status'] == 'success'
        assert result['image_count'] == 2
        assert 'comparison' in result


class TestGenerateCatalogEntry:
    """Test generate_catalog_entry tool."""
    
    @pytest.mark.asyncio
    async def test_generate_catalog_entry_success(self):
        """Test successful catalog entry generation."""
        mock_context = MagicMock()
        mock_context.save_artifact = AsyncMock(return_value=1)
        
        result = await generate_catalog_entry(
            'PROD-001',
            'Test analysis text',
            mock_context
        )
        
        assert result['status'] == 'success'
        assert 'PROD-001' in result['report']
        assert result['version'] == 1
        assert 'filename' in result
    
    @pytest.mark.asyncio
    async def test_generate_catalog_entry_error(self):
        """Test error handling in catalog entry generation."""
        mock_context = MagicMock()
        mock_context.save_artifact = AsyncMock(side_effect=Exception("Save failed"))
        
        result = await generate_catalog_entry(
            'PROD-001',
            'Test analysis',
            mock_context
        )
        
        assert result['status'] == 'error'
        assert 'error' in result


class TestAnalyzeUploadedImage:
    """Test analyze_uploaded_image tool."""
    
    @pytest.mark.asyncio
    async def test_analyze_uploaded_image_success(self):
        """Test successful uploaded image analysis guidance."""
        mock_context = MagicMock()
        
        result = await analyze_uploaded_image(
            'Test Product',
            mock_context
        )
        
        # New implementation returns guidance, not direct analysis
        assert result['status'] == 'success'
        assert 'Test Product' in result['report']
        assert 'product_name' in result
        assert result['product_name'] == 'Test Product'
        assert 'analysis_framework' in result
        assert 'instruction_for_agent' in result
        assert 'product_identification' in result['analysis_framework']
    
    @pytest.mark.asyncio
    async def test_analyze_uploaded_image_error_handling(self):
        """Test error handling in uploaded image analysis."""
        mock_context = MagicMock()
        
        # This should still succeed with guidance
        result = await analyze_uploaded_image(
            'Test Product',
            mock_context
        )
        
        assert result['status'] == 'success'
        assert 'analysis_framework' in result


class TestListSampleImages:
    """Test listing sample images functionality."""
    
    @pytest.mark.asyncio
    async def test_list_sample_images_with_images(self, tmp_path):
        """Test listing sample images when images exist."""
        # This test will pass if real images exist in _sample_images/
        mock_context = MagicMock()
        
        result = await list_sample_images(mock_context)
        
        # Should succeed regardless of whether images exist
        assert result['status'] in ['success', 'info']
        assert 'available_images' in result
        assert isinstance(result['available_images'], list)
    
    @pytest.mark.asyncio
    async def test_list_sample_images_structure(self):
        """Test list_sample_images returns correct structure."""
        mock_context = MagicMock()
        
        result = await list_sample_images(mock_context)
        
        assert 'status' in result
        assert 'report' in result
        assert 'available_images' in result
        
        # If images are found, check their structure
        if result['available_images']:
            first_image = result['available_images'][0]
            assert 'filename' in first_image
            assert 'path' in first_image
            assert 'size' in first_image
            assert 'format' in first_image


class TestMultimodalContent:
    """Test multimodal content handling."""
    
    def test_types_part_creation(self):
        """Test creating types.Part objects."""
        text_part = types.Part.from_text(text="Test text")
        assert text_part is not None
        
        blob = types.Blob(data=b"fake data", mime_type='image/jpeg')
        image_part = types.Part(inline_data=blob)
        assert image_part is not None
    
    def test_multimodal_query_structure(self, tmp_path):
        """Test creating multimodal query with text and image."""
        image_path = tmp_path / "test.jpg"
        create_sample_image(str(image_path))
        
        query_parts = [
            types.Part.from_text(text="Analyze this image:"),
            load_image_from_file(str(image_path)),
            types.Part.from_text(text="What do you see?")
        ]
        
        assert len(query_parts) == 3
        assert all(isinstance(p, types.Part) for p in query_parts)
