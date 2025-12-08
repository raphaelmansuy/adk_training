#!/bin/bash
set -e

# Pre-Build Checks
# Run this before building to ensure all images are optimized

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Pre-Build Checks${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check 1: Image sizes
echo -e "${BLUE}[1/2] Checking blog image sizes...${NC}"
if "$SCRIPT_DIR/check-image-sizes.sh" | grep -q "OVER LIMIT"; then
    echo ""
    echo -e "${YELLOW}⚠ Warning: Some images exceed LinkedIn's 5MB limit${NC}"
    echo ""
    read -p "Run optimization now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        "$SCRIPT_DIR/optimize-blog-images.sh"
    else
        echo -e "${YELLOW}Skipping optimization. Images may not display correctly on LinkedIn.${NC}"
    fi
else
    echo -e "${GREEN}✓ All images are under 5MB limit${NC}"
fi

echo ""

# Check 2: Verify frontmatter
echo -e "${BLUE}[2/2] Checking blog post frontmatter...${NC}"

BLOG_DIR="$SCRIPT_DIR/../docs/blog"
missing_dimensions=0

if [ -d "$BLOG_DIR" ]; then
    for mdfile in "$BLOG_DIR"/*.md; do
        if [ -f "$mdfile" ]; then
            if grep -q "^image: /img/blog/" "$mdfile"; then
                if ! grep -q "^image_width:" "$mdfile" || ! grep -q "^image_height:" "$mdfile"; then
                    echo -e "${YELLOW}⚠ Missing dimensions: $(basename "$mdfile")${NC}"
                    missing_dimensions=$((missing_dimensions + 1))
                fi
            fi
        fi
    done
fi

if [ $missing_dimensions -eq 0 ]; then
    echo -e "${GREEN}✓ All blog posts with images have dimensions${NC}"
else
    echo -e "${YELLOW}⚠ ${missing_dimensions} blog post(s) missing image_width/image_height${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Pre-build checks complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
