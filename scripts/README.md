# Link Verifier (scripts/verify_links.py)

Small utility used by the project to verify links in a Docusaurus build
directory.

Features added:

- Verifies internal and external links.
- Performs detailed internal link resolution (file, .html, /index.html
  fallbacks).
- Verifies anchor/id fragments inside target pages (best-effort
  normalization).
- Robust external checks: uses HEAD then falls back to GET. Configurable
  retries and backoff.
- Caching for external checks to avoid duplicate requests.
- CLI options for bypassing external checks, tuning retries/backoff,
  log export (JSON/CSV) and toggling anchor checks.
- Unit tests and smoke tests included.

## Usage examples

```bash
# Basic check of local build (skips external checks for speed)
python scripts/verify_links.py --skip-external

# Full check with retries for external links
python scripts/verify_links.py --retries 3 --backoff 1

# Save JSON/CSV reports
python scripts/verify_links.py --json-output links.json --export-csv broken.csv
```

## Notes

The script is safe to run on large Docusaurus build directories but may
make many external HTTP requests when not using --skip-external. Prefer
running with --skip-external if you only want local link checks.

---

# Image Optimization Scripts

## Overview

Three scripts for optimizing blog images to meet social media size limits (LinkedIn: 5MB, Twitter: 5MB, Facebook: 8MB).

## Scripts

### 1. check-image-sizes.sh
Quick check of blog image sizes against 5MB limit.

**Usage:** `./scripts/check-image-sizes.sh` or `make check-images`

### 2. optimize-blog-images.sh
Automatically optimize images to <5MB using pngquant.

**Usage:** `./scripts/optimize-blog-images.sh` or `make optimize-images`
**Requires:** `brew install pngquant`

### 3. pre-build-checks.sh
Pre-build validation (checks images + frontmatter).

**Usage:** `./scripts/pre-build-checks.sh` or `npm run build:safe`

## Quick Workflow

```bash
make check-images       # Check sizes
make optimize-images    # Optimize if needed
cd docs && npm run build:safe  # Build with validation
```

## Documentation

- Full guide: `docs/IMAGE_OPTIMIZATION.md`
- LinkedIn fix: `docs/LINKEDIN_FIX_COMPLETE.md`

**Status:** Production Ready (2025-12-08)

---

# Image Optimization Scripts

Three scripts for blog image optimization:
- check-image-sizes.sh: Check sizes
- optimize-blog-images.sh: Optimize to <5MB
- pre-build-checks.sh: Pre-build validation

Usage: make check-images, make optimize-images
Docs: docs/IMAGE_OPTIMIZATION.md
