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
