#!/bin/bash
set -e

# Blog Image Optimization Script
# Optimizes all images in docs/static/img/blog/ to be under 5MB for LinkedIn/social media compatibility
# Preserves originals as .original files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BLOG_IMG_DIR="$PROJECT_ROOT/docs/static/img/blog"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# LinkedIn/social media limits
MAX_SIZE_BYTES=$((5 * 1024 * 1024))  # 5MB
MAX_SIZE_MB=5

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Blog Image Optimization for Social Media${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if pngquant is installed
if ! command -v pngquant &> /dev/null; then
    echo -e "${RED}Error: pngquant is not installed${NC}"
    echo ""
    echo "Install it with:"
    echo "  macOS:   brew install pngquant"
    echo "  Ubuntu:  sudo apt-get install pngquant"
    echo "  CentOS:  sudo yum install pngquant"
    echo ""
    exit 1
fi

# Check if directory exists
if [ ! -d "$BLOG_IMG_DIR" ]; then
    echo -e "${RED}Error: Blog image directory not found: $BLOG_IMG_DIR${NC}"
    exit 1
fi

cd "$BLOG_IMG_DIR"

echo -e "${BLUE}Scanning directory:${NC} $BLOG_IMG_DIR"
echo ""

# Find all PNG files
png_files=($(find . -maxdepth 1 -name "*.png" ! -name "*.original.png" -type f))

if [ ${#png_files[@]} -eq 0 ]; then
    echo -e "${YELLOW}No PNG files found to optimize${NC}"
    exit 0
fi

total_files=${#png_files[@]}
optimized_count=0
skipped_count=0
error_count=0

echo -e "${BLUE}Found ${total_files} PNG file(s)${NC}"
echo ""

for file in "${png_files[@]}"; do
    filename=$(basename "$file")
    filesize=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    filesize_mb=$(echo "scale=2; $filesize / 1024 / 1024" | bc)
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}Processing:${NC} $filename"
    echo -e "${BLUE}Current size:${NC} ${filesize_mb}MB (${filesize} bytes)"
    
    if [ "$filesize" -le "$MAX_SIZE_BYTES" ]; then
        echo -e "${GREEN}✓ Already under ${MAX_SIZE_MB}MB - skipping${NC}"
        skipped_count=$((skipped_count + 1))
        echo ""
        continue
    fi
    
    echo -e "${YELLOW}⚠ Over ${MAX_SIZE_MB}MB limit - optimizing...${NC}"
    
    # Backup original if not already backed up
    if [ ! -f "${filename}.original" ]; then
        echo "  → Creating backup: ${filename}.original"
        cp "$filename" "${filename}.original"
    fi
    
    # Try optimization with different quality settings
    temp_file="${filename}.tmp"
    optimized=false
    
    for quality in "85-95" "80-90" "75-85" "70-80"; do
        echo "  → Trying quality=$quality..."
        
        if pngquant --strip --quality="$quality" "$filename" -o "$temp_file" 2>/dev/null; then
            new_size=$(stat -f%z "$temp_file" 2>/dev/null || stat -c%s "$temp_file" 2>/dev/null)
            new_size_mb=$(echo "scale=2; $new_size / 1024 / 1024" | bc)
            
            if [ "$new_size" -le "$MAX_SIZE_BYTES" ]; then
                echo -e "  → ${GREEN}Success! New size: ${new_size_mb}MB${NC}"
                mv "$temp_file" "$filename"
                optimized=true
                break
            else
                echo "  → Still too large (${new_size_mb}MB), trying lower quality..."
                rm -f "$temp_file"
            fi
        fi
    done
    
    if [ "$optimized" = true ]; then
        reduction=$(echo "scale=1; ($filesize - $new_size) * 100 / $filesize" | bc)
        echo -e "${GREEN}✓ Optimized: ${filesize_mb}MB → ${new_size_mb}MB (${reduction}% reduction)${NC}"
        optimized_count=$((optimized_count + 1))
    else
        echo -e "${RED}✗ Failed to optimize to under ${MAX_SIZE_MB}MB${NC}"
        echo -e "${YELLOW}  Consider manually resizing or using a different image format${NC}"
        error_count=$((error_count + 1))
        
        # Restore original if optimization failed
        if [ -f "${filename}.original" ]; then
            cp "${filename}.original" "$filename"
        fi
    fi
    
    echo ""
done

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Optimization Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Total files:     ${total_files}"
echo -e "${GREEN}Optimized:       ${optimized_count}${NC}"
echo -e "${YELLOW}Skipped:         ${skipped_count}${NC}"
echo -e "${RED}Failed:          ${error_count}${NC}"
echo ""

if [ $optimized_count -gt 0 ]; then
    echo -e "${GREEN}✓ Successfully optimized ${optimized_count} image(s)${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review the optimized images"
    echo "  2. Rebuild: cd docs && npm run build"
    echo "  3. Commit changes: git add docs/static/img/blog/"
    echo "  4. Deploy: git push"
    echo ""
fi

if [ $error_count -gt 0 ]; then
    echo -e "${YELLOW}⚠ Some images could not be optimized to under ${MAX_SIZE_MB}MB${NC}"
    echo "Consider:"
    echo "  - Reducing image dimensions (e.g., 2816x1536 → 2000x1125)"
    echo "  - Converting to JPEG format"
    echo "  - Using online tools like TinyPNG.com"
    echo ""
fi

exit 0
