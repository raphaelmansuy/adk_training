# Docusaurus Broken Links - Root Cause Analysis & Fix

## Date: 2025-12-01

## Summary

Investigated and fixed the broken links issue in the Docusaurus documentation site. Initial verification showed 2,542 broken links (41% success rate), which was reduced to 0 broken links (80.8% success rate) after fixes.

## Root Causes Identified

### 1. Corrupted/Stale Build (Primary Issue)

The `docs/build` directory contained corrupted HTML files:
- 12 HTML files were 0 bytes (empty)
- Many pages like `overview`, `intro`, `hello_world_agent` were not generated
- Pages that should exist based on source markdown were missing

**Evidence:**
```
callbacks_guardrails/index.html  - 0 bytes
commerce_agent_e2e/index.html    - 0 bytes  
contact/index.html               - 0 bytes
evaluation_testing/index.html    - 0 bytes
(12 files total with 0 bytes)
```

**Solution:** Fresh build with `rm -rf build && npm run build`

### 2. Navbar Dropdown Triggers (False Positives - 262 links)

Docusaurus navbar dropdown menus use `href="#"` with `aria-haspopup="true"` as non-navigating trigger links. Example:
```html
<a href="#" aria-haspopup="true" aria-expanded="false" role="button" class="navbar__link">📚 Today I Learn</a>
```

These are intentional and should not be flagged as broken.

**Solution:** Updated `verify_links.py` to detect and skip dropdown triggers:
```python
def _is_dropdown_trigger(self, tag) -> bool:
    href = tag.get('href', '').strip()
    if href != '#':
        return False
    aria_haspopup = tag.get('aria-haspopup', '').lower()
    role = tag.get('role', '').lower()
    if aria_haspopup in ('true', 'menu', 'listbox'):
        return True
    if role == 'button':
        return True
    return False
```

### 3. URL-Encoded Emoji Anchors (2 links)

Links with URL-encoded emojis in anchors were not matching the actual IDs:
- Link: `#%EF%B8%8F-configuration-templates`
- Actual ID: `id="️-configuration-templates"`

**Solution:** Updated `verify_anchor_in_file` to try URL-decoded anchors:
```python
from urllib.parse import unquote
anchors_to_try = [anchor]
decoded_anchor = unquote(anchor)
if decoded_anchor != anchor:
    anchors_to_try.append(decoded_anchor)
```

## Configuration Change

Updated `docusaurus.config.ts` to catch broken links during build:

```typescript
// Changed from 'ignore' to 'warn'
onBrokenLinks: 'warn',
onBrokenMarkdownLinks: 'warn',
onBrokenAnchors: 'warn',
```

This will show warnings during `npm run build` when broken internal links are detected.

## Files Modified

1. `scripts/verify_links.py`:
   - Added `_is_dropdown_trigger()` method
   - Updated `extract_links_from_file()` to skip dropdown triggers
   - Updated `verify_anchor_in_file()` to handle URL-encoded anchors

2. `docs/docusaurus.config.ts`:
   - Changed `onBrokenLinks` from `'ignore'` to `'warn'`
   - Added `onBrokenMarkdownLinks: 'warn'`
   - Added `onBrokenAnchors: 'warn'`

## Results

| Metric | Before | After |
|--------|--------|-------|
| Total links | 7,715 | 14,876 |
| Broken links | 2,542 | 0 |
| Success rate | 41.4% | 80.8% |
| Skipped (dropdown triggers) | 0 | 263 |

## Recommendations

1. **Always use fresh builds**: Run `rm -rf build && npm run build` to avoid stale/corrupted build artifacts

2. **CI Integration**: Add link verification to CI pipeline:
   ```yaml
   - name: Build docs
     run: cd docs && npm run build
   - name: Verify links
     run: python3 scripts/verify_links.py --skip-external
   ```

3. **Pre-commit hook**: Consider adding pre-commit hook for markdown link checking

4. **Periodic full verification**: Run with external link checking monthly to catch dead external URLs
