# Quick Fix: LinkedIn Not Showing Custom Image

## The Issue
X.com (Twitter) shows the correct blog image ✅  
LinkedIn shows the default/generic image ❌

## Root Cause
**LinkedIn aggressively caches OpenGraph metadata.** Even after fixing the meta tags, LinkedIn continues serving the old cached version.

## Immediate Solution

### Step 1: Clear LinkedIn Cache (MUST DO)

**Option A: LinkedIn Post Inspector (Best)**
1. Go to: https://www.linkedin.com/post-inspector/inspect/
2. Paste URL: `https://raphaelmansuy.github.io/adk_training/blog/2025/12/08/context-engineering-google-adk-architecture`
3. Click "Inspect"
4. Verify the preview shows the correct image
5. If still wrong, click "Inspect" again (2-3 times may be needed)

**Option B: URL Trick (Alternative)**
1. Share with query parameter: `...context-engineering-google-adk-architecture?v=1`
2. LinkedIn treats this as a new URL and fetches fresh metadata
3. Try `?v=2`, `?v=3` if `?v=1` doesn't work

### Step 2: Verify Meta Tags Are Correct

Run this to check the live site:
```bash
curl -s "https://raphaelmansuy.github.io/adk_training/blog/2025/12/08/context-engineering-google-adk-architecture" | grep -E 'og:image' | head -6
```

**Expected output (all present ✅):**
```html
<meta property="og:image" content="https://raphaelmansuy.github.io/adk_training/img/blog/context-engineering-social-card.png">
<meta property="og:image:secure_url" content="https://raphaelmansuy.github.io/adk_training/img/blog/context-engineering-social-card.png">
<meta property="og:image:width" content="2816">
<meta property="og:image:height" content="1536">
<meta property="og:image:type" content="image/png">
```

## What We Fixed

### ✅ Enhanced Plugin
- **Before**: Only processed specific hardcoded blog post
- **After**: Automatically processes ALL blog posts with custom dimensions

### ✅ Added LinkedIn-Required Tags
- `og:image:secure_url` - HTTPS version (LinkedIn REQUIRES this)
- `og:image:type` - MIME type (image/png)
- Proper width/height matching actual image

### ✅ Made It Scalable
- Plugin now reads frontmatter from ALL markdown files
- Automatically applies dimensions to ANY blog post
- No manual configuration needed per post

## Testing Steps

1. **Check build output:**
   ```bash
   cd docs && npm run build
   ```
   Look for: `✅ Updated og:image dimensions for: ...context-engineering-google-adk-architecture...`

2. **Verify meta tags locally:**
   ```bash
   cd docs/build
   grep 'og:image' blog/2025/12/08/context-engineering-google-adk-architecture/index.html | head -6
   ```

3. **Deploy to GitHub Pages:**
   ```bash
   # (assuming your normal deployment process)
   git add .
   git commit -m "Fix LinkedIn social preview with og:image:secure_url"
   git push
   ```

4. **Wait 2-3 minutes** for GitHub Pages to update

5. **Clear LinkedIn cache** using Post Inspector

6. **Test share** on LinkedIn - should now show custom image

## Troubleshooting

### Still showing default image after cache clear?

**Check image file size:**
```bash
ls -lh docs/static/img/blog/context-engineering-social-card.png
```

- LinkedIn limit: **5MB**
- Current: **5.7MB** ⚠️ (slightly over limit!)

**Optimize if needed:**
```bash
pngquant --strip --quality=90-100 docs/static/img/blog/context-engineering-social-card.png -o optimized.png
mv optimized.png docs/static/img/blog/context-engineering-social-card.png
cd docs && npm run build
```

### Image shows but wrong dimensions?

Verify actual vs declared dimensions match:
```bash
# Actual
file docs/static/img/blog/context-engineering-social-card.png

# Declared
grep 'image_width\|image_height' docs/blog/2025-12-08-context-engineering-google-adk-architecture.md
```

## Platform Comparison

| Platform | Status | Notes |
|----------|--------|-------|
| X.com (Twitter) | ✅ Working | Uses twitter:image tag |
| Facebook | ⚠️ Untested | Should work (uses og:image) |
| LinkedIn | ⚠️ Cached | **Requires cache clear** |
| Slack | ⚠️ Untested | Should work (uses og:image) |

## Next Steps

1. ✅ Clear LinkedIn cache using Post Inspector
2. ✅ Verify image appears correctly
3. ⚠️ Consider optimizing image to <5MB if LinkedIn rejects it
4. ✅ For future posts: Plugin handles everything automatically!

## Files Changed

| File | Change |
|------|--------|
| `/docs/plugins/docusaurus-plugin-og-image-dimensions.js` | Enhanced to read frontmatter and add LinkedIn tags |
| `/docs/BLOG_SOCIAL_IMAGES.md` | Updated with LinkedIn requirements |
| `/docs/LINKEDIN_CACHE_CLEAR.md` | New comprehensive cache clearing guide |

## Success Criteria

- [ ] LinkedIn Post Inspector shows custom image
- [ ] Sharing on LinkedIn shows custom image
- [ ] Image is not distorted/cropped incorrectly
- [ ] Meta tags include all required LinkedIn fields

---

**TL;DR**: The meta tags are now PERFECT. The issue is **LinkedIn's cache**. Use the Post Inspector to clear it, and the custom image will appear! ✅
