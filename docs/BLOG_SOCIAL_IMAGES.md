# Blog Post Social Media Image Configuration Guide

## Overview

When you publish blog posts to LinkedIn, Twitter, or other social media platforms, the social preview image is determined by the OpenGraph (og:image) meta tags in your HTML. By default, Docusaurus uses the global site social card image and hardcoded dimensions (1200x630).

This project includes a custom solution to allow **per-blog-post custom images with proper dimensions** for optimal social media previews.

## How It Works

### 1. Image Setup

Create your blog post-specific social card image:

- **Location**: `/docs/static/img/blog/[your-blog-name]-social-card.png`
- **Dimensions**: 2816x1536 (or 1200x630 for standard, or your custom size)
- **Format**: PNG
- **Size**: Keep under 10MB for performance

Example: `/docs/static/img/blog/context-engineering-social-card.png`

### 2. Frontmatter Configuration

In your blog post markdown file (`.md` or `.mdx`), add the following fields to the frontmatter:

```yaml
---
title: "Your Blog Post Title"
description: "Your blog post description"
authors:
  - name: Your Name
    title: Your Title
    url: https://yourprofile
    image_url: https://your-avatar.png
tags: [tag1, tag2]
image: /img/blog/your-blog-name-social-card.png
image_width: 2816
image_height: 1536
keywords: [keyword1, keyword2]
---
```

### 3. Plugin Processing

The Docusaurus build includes a custom plugin (`docusaurus-plugin-og-image-dimensions.js`) that:

1. **During build**: Generates the blog post HTML with your blog-specific image in the og:image meta tag
2. **Post-processing**: Updates the og:image:width and og:image:height meta tags with your specified dimensions
3. **Falls back**: If no custom dimensions are specified, uses the default global values

## Configuration Files

### Blog Post Frontmatter Fields

| Field | Required | Example | Purpose |
|-------|----------|---------|---------|
| `image` | Yes | `/img/blog/my-social-card.png` | URL to your custom social card image |
| `image_width` | For custom sizing | `2816` | Width of your social card in pixels |
| `image_height` | For custom sizing | `1536` | Height of your social card in pixels |

### Plugin Implementation

**File**: `/docs/plugins/docusaurus-plugin-og-image-dimensions.js`

This plugin:
- Runs during the `postBuild` phase
- Scans all generated blog post HTML files
- Updates meta tags based on frontmatter values
- Only processes posts that specify custom dimensions

**Registration**: Added to `docusaurus.config.ts` under the `plugins` array

## Example: Context Engineering Blog Post

The blog post "Context Engineering: Inside Google's Architecture for Production AI Agents" uses this setup:

**File**: `/docs/blog/2025-12-08-context-engineering-google-adk-architecture.md`

```yaml
---
title: "Context Engineering: Inside Google's Architecture for Production AI Agents"
description: "Deep dive into Google's ADK framework..."
image: /img/blog/context-engineering-social-card.png
image_width: 2816
image_height: 1536
---
```

**Image**: `/docs/static/img/blog/context-engineering-social-card.png` (2816x1536px)

**Result**: When shared on LinkedIn/Twitter, uses the custom image with proper aspect ratio

## Metadata Output

When the blog post is built, the resulting HTML includes:

```html
<meta property="og:image" content="https://raphaelmansuy.github.io/adk_training/img/blog/context-engineering-social-card.png">
<meta property="og:image:width" content="2816">
<meta property="og:image:height" content="1536">
<meta name="twitter:image" content="https://raphaelmansuy.github.io/adk_training/img/blog/context-engineering-social-card.png">
```

This tells social platforms:
- Which image to display
- The exact dimensions for proper aspect ratio
- No distortion or incorrect scaling

## Social Media Platform Guidelines

### LinkedIn

- **Recommended**: 1200x630 (16:10 ratio) or 2:1 ratio
- **Supported**: Any aspect ratio, but 1.91:1 to 4:5 works best
- **Our setup**: 2816x1536 (1.833:1) works well on LinkedIn
- **Caching**: LinkedIn caches preview images. To update:
  1. Use the [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/inspect/)
  2. Paste your URL
  3. Click "Inspect"
  4. Clear cache by modifying the URL query parameter

### Twitter/X

- **Recommended**: 1200x675 (16:9) or 1200x630 (19:10)
- **Aspect ratio**: 16:9 or 2:1 work well
- **Card type**: `summary_large_image` (automatically used for og:image with proper dimensions)
- **Caching**: Similar to LinkedIn, Twitter caches. Use [Twitter Card Validator](https://cards-dev.twitter.com/validator) to refresh

### Facebook

- **Recommended**: 1200x630
- **Minimum**: 400x209
- **Aspect ratio**: 1.91:1 is ideal
- **Debugger**: Use [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/sharing/) to clear cache

## Troubleshooting

### Issue: Social preview still shows default image

**Solution**:

1. Verify the `image` field is correct in frontmatter
2. Check that the image file exists at the specified path
3. Rebuild: `npm run build` from the `/docs` directory
4. Clear social media platform cache using their respective debuggers

### Issue: Aspect ratio is wrong

**Solution**:

1. Verify `image_width` and `image_height` match your actual image
2. Get image dimensions: `identify filename.png` (requires ImageMagick)
3. Rebuild the site
4. Clear platform cache

### Issue: Plugin not running

**Solution**:

1. Check if plugin is registered in `docusaurus.config.ts`
2. Look for "Updated og:image dimensions" in build output
3. Verify plugin path: `require.resolve('./plugins/docusaurus-plugin-og-image-dimensions.js')`

## Image Optimization Tips

### Design Best Practices

1. **Safe Zone**: Keep important content in center 70% (avoid edges)
2. **Text**: Use large, readable fonts (40pt+)
3. **Contrast**: High contrast for text readability
4. **Branding**: Include logo/brand element
5. **Whitespace**: Don't fill entire image

### File Size Optimization

```bash
# Compress PNG without quality loss
pngquant --strip --quality=90-100 image.png

# Or use ImageMagick
convert image.png -strip image-optimized.png

# Verify size reduction
ls -lh image.png image-optimized.png
```

### Aspect Ratio Recommendations

| Platform | Ideal | Acceptable |
|----------|-------|-----------|
| LinkedIn | 1.91:1 or 2:1 | 1.33:1 to 4:5 |
| Twitter | 16:9 or 2:1 | 1.2:1 to 2:1 |
| Facebook | 1.91:1 | 1.33:1 to 2.4:1 |
| Slack | 1.3:1 | 1.2:1 to 2:1 |

Our blog uses **1.833:1** (2816x1536) which works across all platforms.

## Creating a New Blog Post

### Checklist

- [ ] Create markdown file in `/docs/blog/` with naming: `YYYY-MM-DD-slug.md`
- [ ] Add frontmatter with all required fields
- [ ] Create social card image (2816x1536px recommended)
- [ ] Save image to `/docs/static/img/blog/[slug]-social-card.png`
- [ ] Add `image_width` and `image_height` to frontmatter
- [ ] Build: `npm run build`
- [ ] Verify meta tags: `grep "og:image" build/blog/[slug]/index.html`
- [ ] Test on social media platform using their debugger tools

## Advanced: Custom Plugin Configuration

If you need different defaults or behavior, edit `/docs/plugins/docusaurus-plugin-og-image-dimensions.js`:

```javascript
// Example: Add support for image_alt field
if (htmlFile.includes('my-custom-image.png')) {
  html = html.replace(
    /<meta property="og:image:alt" content="[^"]*">/,
    `<meta property="og:image:alt" content="${frontmatter.image_alt || 'Image'}">`
  );
}
```

## File Structure

```
docs/
├── blog/
│   └── 2025-12-08-context-engineering-google-adk-architecture.md
├── static/
│   └── img/
│       └── blog/
│           └── context-engineering-social-card.png
├── plugins/
│   └── docusaurus-plugin-og-image-dimensions.js
└── docusaurus.config.ts
```

## Testing Your Meta Tags

### Quick Check (Local)

```bash
cd docs/build
grep -E "(og:image|twitter:image)" blog/your-post-slug/index.html | grep -v "alt"
```

### Full Check (Inspect HTML)

Open the built HTML file in a text editor and search for all `og:` and `twitter:` meta tags.

### Platform-Specific Tools

1. **LinkedIn**: https://www.linkedin.com/post-inspector/inspect/
2. **Twitter**: https://cards-dev.twitter.com/validator
3. **Facebook**: https://developers.facebook.com/tools/debug/sharing/
4. **Generic**: https://metatags.io/

## Resources

- [OpenGraph Protocol](https://ogp.me/)
- [Twitter Card Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards)
- [LinkedIn Sharing Best Practices](https://www.linkedin.com/business/learning/blog/product-tips/how-to-make-your-content-stand-out-on-linkedin)
- [Docusaurus Blog Documentation](https://docusaurus.io/docs/blog)

---

**Last Updated**: 2025-12-08
**Plugin Version**: 1.0
**Docusaurus Version**: 3.9+
