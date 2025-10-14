# Tutorial 21: Real Product Images from Unsplash

**Date**: 2025-10-13 20:31:00
**Status**: ✅ Complete

## Enhancement

Added real product images from Unsplash to replace synthetic placeholder images
in Tutorial 21's sample images directory.

## Changes

### Downloaded Images

Downloaded three high-quality product images from Unsplash:

1. **laptop.jpg** (38.5 KB, 800x533px)
   - Modern laptop computer
   - Source: https://images.unsplash.com/photo-1496181133206-80ce9b88a853

2. **headphones.jpg** (41.1 KB, 800x533px)
   - Wireless headphones
   - Source: https://images.unsplash.com/photo-1505740420928-5e560c06d30e

3. **smartwatch.jpg** (53.3 KB, 800x533px)
   - Smart watch device
   - Source: https://images.unsplash.com/photo-1579586337278-3befd40fd17a

All images are:
- Royalty-free under Unsplash License
- Optimized size (800x533px, <55 KB each)
- JPEG format, RGB mode
- Ready for vision AI analysis

### New Files

**download_images.py** (60+ lines):
- Automated script to download sample images
- Uses urllib for reliable downloads
- Proper User-Agent headers
- Error handling for network issues
- Attribution and licensing information

### Documentation Updates

**README.md**:
- Added "Sample Images" section
- Credit to Unsplash with license link
- Instructions for downloading fresh images
- Added Unsplash to Resources section

**Makefile**:
- Added `download-images` target
- Makes it easy to refresh sample images

## Benefits

1. **Realistic Demos**: Real product photos instead of colored rectangles
2. **Better Testing**: Vision AI analysis works with actual product images
3. **Professional Quality**: High-quality photos from Unsplash
4. **Easy Updates**: Script can download fresh images anytime
5. **Proper Attribution**: Clear licensing and credits

## Verification

All images successfully loaded and tested:

```bash
✓ laptop.jpg: image/jpeg, 39,412 bytes
✓ headphones.jpg: image/jpeg, 42,046 bytes  
✓ smartwatch.jpg: image/jpeg, 54,608 bytes
```

Image loading tests passing:
- 5/5 image loading tests ✅
- All MIME types detected correctly
- File paths resolved properly

## Usage

### Download Images

```bash
cd tutorial_implementation/tutorial21
make download-images
```

or

```bash
python3 download_images.py
```

### Use in Demos

Images are automatically available in `_sample_images/` directory for:
- ADK web interface demos
- Command-line testing
- Automated test suite
- Documentation examples

## Attribution

Images sourced from [Unsplash](https://unsplash.com) - the internet's source of
freely usable images. Used under the
[Unsplash License](https://unsplash.com/license):

> Unsplash grants you an irrevocable, nonexclusive, worldwide copyright license
> to download, copy, modify, distribute, perform, and use photos from Unsplash
> for free, including for commercial purposes, without permission from or
> attributing the photographer or Unsplash.

## Impact

**Before**:
- Synthetic colored rectangles (create_sample_image function)
- Not realistic for product catalog demos
- Limited visual appeal

**After**:
- Professional product photography
- Realistic vision AI analysis scenarios
- Better demonstration of capabilities
- More engaging tutorials

## Files Modified

1. `_sample_images/laptop.jpg` - New real product image
2. `_sample_images/headphones.jpg` - New real product image
3. `_sample_images/smartwatch.jpg` - New real product image
4. `download_images.py` - New automated download script
5. `README.md` - Added Sample Images section and attribution
6. `Makefile` - Added download-images target

## Technical Notes

- Images optimized at 800x533px (Unsplash w=800 parameter)
- JPEG quality 80 (Unsplash q=80 parameter)
- Total size: ~136 KB for all three images
- Suitable for Gemini vision API (well under 20MB limit)
- Fast loading and processing

## Next Steps

Users can now:
- Run demos with realistic product images
- Test vision analysis with actual products
- Upload their own images for comparison
- Download fresh images anytime with the script

The tutorial now provides a more professional and realistic experience for
learning multimodal AI with Google ADK.
