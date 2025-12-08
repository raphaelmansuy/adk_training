# Blog Image Optimization Guide

## Overview

Social media platforms (LinkedIn, Twitter, Facebook) have strict image size limits for social preview cards. LinkedIn's limit is **5MB**, which is critical for proper image display.

This project includes automated tools to optimize blog images for social media compatibility.

## Quick Start

### Check Image Sizes

```bash
cd docs
npm run check-images
```

This shows which images exceed the 5MB limit.

### Optimize All Images

```bash
cd docs
npm run optimize-images
```

This automatically compresses images to under 5MB while preserving quality.

### Safe Build with Pre-Checks

```bash
cd docs
npm run build:safe
```

This runs pre-build checks including image optimization before building.

## Tools Overview

### 1. `scripts/check-image-sizes.sh`

**Purpose:** Quick check of all blog images  
**Usage:** `./scripts/check-image-sizes.sh` or `npm run check-images`

**Output:**
```
Filename                                        Size (MB)    Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
context-engineering-social-card.png               5.73MB    ⚠ OVER LIMIT
another-image.png                                 2.41MB    ✓ OK
```

### 2. `scripts/optimize-blog-images.sh`

**Purpose:** Automatically optimize images to under 5MB  
**Usage:** `./scripts/optimize-blog-images.sh` or `npm run optimize-images`

**Features:**
- Backs up originals as `.original` files
- Progressive quality reduction (85-95% → 70-80%)
- Preserves images already under 5MB
- Shows before/after sizes and reduction percentage

**Output:**
```
Processing: context-engineering-social-card.png
Current size: 5.73MB
⚠ Over 5MB limit - optimizing...
  → Trying quality=85-95...
  → Success! New size: 4.82MB
✓ Optimized: 5.73MB → 4.82MB (15.8% reduction)
```

### 3. `scripts/pre-build-checks.sh`

**Purpose:** Comprehensive pre-build validation  
**Usage:** `./scripts/pre-build-checks.sh` or `npm run build:safe`

**Checks:**
1. Image sizes (warns if over 5MB)
2. Blog post frontmatter (warns if missing `image_width`/`image_height`)
3. Offers to run optimization automatically

## Requirements

### Install pngquant

**macOS:**
```bash
brew install pngquant
```

**Ubuntu/Debian:**
```bash
sudo apt-get install pngquant
```

**CentOS/RHEL:**
```bash
sudo yum install pngquant
```

**Verify installation:**
```bash
pngquant --version
```

## Workflow

### For New Blog Posts

1. **Create your social card image** (2816x1536px recommended)
2. **Save to** `docs/static/img/blog/[post-slug]-social-card.png`
3. **Check size:**
   ```bash
   npm run check-images
   ```
4. **If over 5MB, optimize:**
   ```bash
   npm run optimize-images
   ```
5. **Add to frontmatter:**
   ```yaml
   image: /img/blog/[post-slug]-social-card.png
   image_width: 2816
   image_height: 1536
   ```
6. **Build with checks:**
   ```bash
   npm run build:safe
   ```

### Before Deployment

```bash
# From project root
cd docs

# Check all images
npm run check-images

# Optimize if needed
npm run optimize-images

# Build with validation
npm run build:safe

# Or standard build
npm run build
```

## Image Guidelines

### Size Limits

| Platform | Max Size | Recommended |
|----------|----------|-------------|
| LinkedIn | 5MB | < 4.5MB (buffer) |
| Twitter | 5MB | < 4.5MB |
| Facebook | 8MB | < 5MB |
| Slack | 5MB | < 4.5MB |

**Our target:** Under 5MB for universal compatibility

### Dimensions

| Platform | Ideal Dimensions | Aspect Ratio |
|----------|------------------|--------------|
| LinkedIn | 1200x630 or 2816x1536 | 1.91:1 or 1.83:1 |
| Twitter | 1200x675 | 16:9 |
| Facebook | 1200x630 | 1.91:1 |
| All | 2816x1536 | 1.83:1 (our standard) |

### Quality vs Size

The optimization script tries these quality levels:
1. **85-95%**: Best quality, smallest compression
2. **80-90%**: Good quality, moderate compression
3. **75-85%**: Acceptable quality, higher compression
4. **70-80%**: Visible compression, maximum size reduction

Most images hit the 5MB target at 85-95% quality.

## Manual Optimization

If automatic optimization fails:

### Option 1: Reduce Dimensions

```bash
# Requires ImageMagick
brew install imagemagick

# Resize to 2000x1125 (maintains 16:9)
convert original.png -resize 2000x1125 resized.png
```

### Option 2: Convert to JPEG

```bash
convert original.png -quality 90 optimized.jpg
```

JPEG typically produces smaller files than PNG for photos/gradients.

### Option 3: Online Tools

- **TinyPNG:** https://tinypng.com/ (up to 5MB)
- **Squoosh:** https://squoosh.app/ (Google's tool)
- **Compressor.io:** https://compressor.io/

## Troubleshooting

### "pngquant: command not found"

Install pngquant (see Requirements section above).

### "Still too large after optimization"

Try manual methods:
1. Reduce dimensions (e.g., 2816x1536 → 2000x1125)
2. Convert to JPEG format
3. Use online compression tools

### "Original quality loss"

Original files are backed up as `.original` files:
```bash
cd docs/static/img/blog
cp image.png.original image.png  # Restore original
```

### Build fails with "Image over 5MB"

The plugin will still work, but LinkedIn may reject the image. Optimize before deploying.

## CI/CD Integration

### GitHub Actions

Add to `.github/workflows/deploy.yml`:

```yaml
- name: Check image sizes
  working-directory: ./docs
  run: npm run check-images

- name: Optimize images if needed
  working-directory: ./docs
  run: |
    if npm run check-images | grep -q "OVER LIMIT"; then
      npm run optimize-images
    fi

- name: Build with Docusaurus
  working-directory: ./docs
  run: npm run build
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd docs
if npm run check-images | grep -q "OVER LIMIT"; then
    echo "Error: Images over 5MB detected"
    echo "Run: npm run optimize-images"
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## File Structure

```
project/
├── scripts/
│   ├── check-image-sizes.sh       # Quick size check
│   ├── optimize-blog-images.sh    # Automatic optimization
│   └── pre-build-checks.sh        # Comprehensive validation
├── docs/
│   ├── package.json               # Added npm scripts
│   ├── static/img/blog/
│   │   ├── image.png              # Current version
│   │   └── image.png.original     # Backup (created by optimizer)
│   └── blog/
│       └── 2025-12-08-post.md     # Frontmatter with image_width/height
```

## Best Practices

1. **Always check before committing:**
   ```bash
   npm run check-images
   ```

2. **Optimize proactively:**
   ```bash
   npm run optimize-images
   ```

3. **Use build:safe for important deployments:**
   ```bash
   npm run build:safe
   ```

4. **Keep originals:** The optimizer preserves originals automatically

5. **Test on LinkedIn:** Use Post Inspector after deployment

## Resources

- **LinkedIn Image Guidelines:** https://www.linkedin.com/help/linkedin/answer/46687
- **Twitter Card Validator:** https://cards-dev.twitter.com/validator
- **Facebook Sharing Debugger:** https://developers.facebook.com/tools/debug/
- **OpenGraph Protocol:** https://ogp.me/

---

**Last Updated:** 2025-12-08  
**Maintainer:** ADK Training Team  
**Status:** Production Ready
