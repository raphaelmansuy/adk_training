# LinkedIn Social Preview Cache Clear Guide

## Problem

LinkedIn caches OpenGraph metadata for shared URLs. Even after fixing the meta tags, LinkedIn may continue showing the old/default image until the cache is cleared.

## Solution: Clear LinkedIn Cache

### Method 1: LinkedIn Post Inspector (Recommended)

1. **Open LinkedIn Post Inspector**
   - Go to: https://www.linkedin.com/post-inspector/inspect/
   
2. **Enter Your URL**
   - Paste: `https://raphaelmansuy.github.io/adk_training/blog/2025/12/08/context-engineering-google-adk-architecture`
   
3. **Click "Inspect"**
   - LinkedIn will fetch fresh metadata from your page
   - This clears the cached version
   
4. **Verify the Preview**
   - Check that the correct image appears (context-engineering-social-card.png)
   - Verify dimensions are correct (2816x1536)
   
5. **Share Again**
   - Try sharing the URL on LinkedIn
   - The new image should now appear

### Method 2: URL Query Parameter Trick

If the Post Inspector doesn't work or is unavailable:

1. **Add a Query Parameter**
   - Original: `https://raphaelmansuy.github.io/adk_training/blog/2025/12/08/context-engineering-google-adk-architecture`
   - Modified: `https://raphaelmansuy.github.io/adk_training/blog/2025/12/08/context-engineering-google-adk-architecture?v=1`
   
2. **Share the Modified URL**
   - LinkedIn treats this as a "new" URL
   - It will fetch fresh metadata
   
3. **Increment the Parameter**
   - If still showing old image, try `?v=2`, `?v=3`, etc.
   - Each version forces a new cache entry

### Method 3: Wait for Natural Cache Expiry

LinkedIn's cache typically expires after:
- **7 days** for previously shared URLs
- **30 days** for rarely accessed URLs

If you can wait, the cache will refresh automatically.

## Verification Checklist

After clearing the cache, verify these meta tags are present in your HTML:

```bash
# Check from terminal
cd docs/build
grep 'og:image' blog/2025/12/08/context-engineering-google-adk-architecture/index.html
```

**Expected output:**

```html
<meta property="og:image" content="https://raphaelmansuy.github.io/adk_training/img/blog/context-engineering-social-card.png">
<meta property="og:image:secure_url" content="https://raphaelmansuy.github.io/adk_training/img/blog/context-engineering-social-card.png">
<meta property="og:image:width" content="2816">
<meta property="og:image:height" content="1536">
<meta property="og:image:type" content="image/png">
<meta property="og:image:alt" content="...">
```

## LinkedIn-Specific Requirements

LinkedIn requires these specific OpenGraph tags for optimal preview:

| Tag | Required | Purpose |
|-----|----------|---------|
| `og:image` | ✅ YES | Image URL |
| `og:image:secure_url` | ✅ YES | HTTPS version of image URL |
| `og:image:width` | ✅ YES | Image width in pixels |
| `og:image:height` | ✅ YES | Image height in pixels |
| `og:image:type` | ⚠️ Recommended | MIME type (image/png, image/jpeg) |
| `og:image:alt` | ⚠️ Recommended | Alt text for accessibility |

**All of these are now included in the build!** ✅

## Troubleshooting

### Issue: LinkedIn Still Shows Default Image

**Possible causes:**

1. **Cache not cleared**
   - Solution: Use Post Inspector multiple times
   - Try URL with query parameter (`?v=1`)

2. **Image URL not accessible**
   - Verify: https://raphaelmansuy.github.io/adk_training/img/blog/context-engineering-social-card.png
   - Should load in browser without errors

3. **Image too large**
   - Maximum: 5MB (ours is 5.7MB - might be at the limit!)
   - Consider optimizing: `pngquant --strip --quality=90-100 image.png`

4. **Wrong image dimensions in HTML**
   - Check build output for: `Updated og:image dimensions`
   - Verify meta tags match actual image size

### Issue: Image Appears but Wrong Aspect Ratio

**Solution:**

1. Verify actual image dimensions:
   ```bash
   file docs/static/img/blog/context-engineering-social-card.png
   ```

2. Verify meta tags match:
   ```bash
   grep 'og:image:width\|og:image:height' docs/build/blog/.../index.html
   ```

3. Rebuild if mismatch:
   ```bash
   cd docs && npm run build
   ```

### Issue: Different Platforms Show Different Images

**This is normal!**

- Twitter: May use `twitter:image` tag (separate from og:image)
- Facebook: Uses OpenGraph tags (same as LinkedIn)
- LinkedIn: Uses OpenGraph tags + secure_url

**Solution:** Verify all platforms have correct tags:

```html
<!-- OpenGraph (LinkedIn, Facebook) -->
<meta property="og:image" content="...">
<meta property="og:image:secure_url" content="...">

<!-- Twitter -->
<meta name="twitter:image" content="...">
```

## Best Practices for Future Posts

1. **Always use HTTPS** for og:image URLs
2. **Always include secure_url** (LinkedIn requirement)
3. **Match dimensions exactly** (width/height in meta = actual image size)
4. **Keep images under 5MB** (LinkedIn limit)
5. **Use Post Inspector** before sharing new posts
6. **Test on multiple platforms** (LinkedIn, Twitter, Facebook)

## Quick Test Commands

### Test the live URL
```bash
# Fetch just the meta tags
curl -s "https://raphaelmansuy.github.io/adk_training/blog/2025/12/08/context-engineering-google-adk-architecture" | grep -E 'og:image|twitter:image'
```

### Test local build
```bash
cd docs/build
grep -E 'og:image|twitter:image' blog/2025/12/08/context-engineering-google-adk-architecture/index.html
```

## Cache Clearing URLs

- **LinkedIn**: https://www.linkedin.com/post-inspector/inspect/
- **Twitter**: https://cards-dev.twitter.com/validator
- **Facebook**: https://developers.facebook.com/tools/debug/sharing/
- **Generic**: https://metatags.io/

## Image Optimization (If Needed)

If LinkedIn complains about image size (5.7MB is close to the 5MB limit):

```bash
# Compress without quality loss
pngquant --strip --quality=90-100 docs/static/img/blog/context-engineering-social-card.png -o context-engineering-social-card-optimized.png

# Replace original
mv context-engineering-social-card-optimized.png docs/static/img/blog/context-engineering-social-card.png

# Rebuild
cd docs && npm run build
```

## Timeline Expectations

After clearing LinkedIn cache:
- **Immediate**: Post Inspector shows correct image
- **1-5 minutes**: New shares show correct image
- **5-10 minutes**: All LinkedIn users see updated preview
- **24 hours**: Old cached shares may still show old image (normal)

## Contact LinkedIn Support

If after all steps the image still doesn't work:
1. Go to: https://www.linkedin.com/help/linkedin
2. Report: "Social preview not updating"
3. Provide: Your blog post URL
4. Include: Screenshot of Post Inspector results

---

**Last Updated**: 2025-12-08
**Status**: Enhanced plugin with LinkedIn-specific tags
**Meta Tags Added**: og:image:secure_url, og:image:type
