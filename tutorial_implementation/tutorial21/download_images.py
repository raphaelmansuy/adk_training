#!/usr/bin/env python3
"""
Download sample product images for Tutorial 21
"""
import urllib.request
from pathlib import Path

# Sample images directory
sample_dir = Path(__file__).parent / '_sample_images'
sample_dir.mkdir(exist_ok=True)

# Free product images from Unsplash (royalty-free)
images = {
    'laptop.jpg': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80',
    'headphones.jpg': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
    'smartwatch.jpg': 'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&q=80'
}

print("Downloading sample product images...")
print(f"Target directory: {sample_dir}")
print()

for filename, url in images.items():
    output_path = sample_dir / filename
    
    try:
        print(f"Downloading {filename}...")
        print(f"  URL: {url}")
        
        # Download with proper headers
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        with open(output_path, 'wb') as f:
            f.write(data)
            
        print(f"  ✓ Saved to {output_path} ({len(data):,} bytes)")
        print()
        
    except Exception as e:
        print(f"  ✗ Error downloading {filename}: {e}")
        print()

print("Done! Sample images are ready for use.")
print("\nImages sourced from Unsplash (https://unsplash.com)")
print("License: Free to use under Unsplash License")
