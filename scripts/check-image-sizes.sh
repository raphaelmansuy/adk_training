#!/bin/bash
set -e

# Check Blog Image Sizes
# Quick check to see which images exceed LinkedIn's 5MB limit

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BLOG_IMG_DIR="$PROJECT_ROOT/docs/static/img/blog"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MAX_SIZE_BYTES=$((5 * 1024 * 1024))  # 5MB
MAX_SIZE_MB=5

echo -e "${BLUE}Blog Image Size Check (Max: ${MAX_SIZE_MB}MB for LinkedIn)${NC}"
echo ""

if [ ! -d "$BLOG_IMG_DIR" ]; then
    echo -e "${RED}Error: Directory not found: $BLOG_IMG_DIR${NC}"
    exit 1
fi

cd "$BLOG_IMG_DIR"

# Find all image files
image_files=($(find . -maxdepth 1 \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) ! -name "*.original.*" -type f))

if [ ${#image_files[@]} -eq 0 ]; then
    echo -e "${YELLOW}No image files found${NC}"
    exit 0
fi

over_limit=0
total_files=${#image_files[@]}

printf "%-50s %10s %10s\n" "Filename" "Size (MB)" "Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

for file in "${image_files[@]}"; do
    filename=$(basename "$file")
    filesize=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    filesize_mb=$(echo "scale=2; $filesize / 1024 / 1024" | bc)
    
    if [ "$filesize" -gt "$MAX_SIZE_BYTES" ]; then
        status="${RED}⚠ OVER LIMIT${NC}"
        over_limit=$((over_limit + 1))
    else
        status="${GREEN}✓ OK${NC}"
    fi
    
    printf "%-50s %9.2fMB " "$filename" "$filesize_mb"
    echo -e "$status"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Total images: ${total_files}"

if [ $over_limit -gt 0 ]; then
    echo -e "${RED}Images over ${MAX_SIZE_MB}MB limit: ${over_limit}${NC}"
    echo ""
    echo "Run optimization:"
    echo "  ./scripts/optimize-blog-images.sh"
else
    echo -e "${GREEN}All images are under ${MAX_SIZE_MB}MB limit ✓${NC}"
fi

echo ""
