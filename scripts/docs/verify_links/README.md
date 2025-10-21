# Link Verification Script

Verify all links in the Docusaurus website, checking both internal file
references and external URLs.

## Quick Start

```bash
# Install dependencies
pip install -r scripts/requirements-links.txt

# Build Docusaurus (if needed)
cd docs && npm run build && cd ..

# Run verification
python scripts/verify_links.py
```

## Features

- **Internal Links**: Validates file existence and anchor references
- **External Links**: Checks HTTP status codes and redirects
- **Concurrent Processing**: Fast multi-threaded external verification
- **JSON Export**: Structured output for CI/CD integration
- **Colored Console Output**: Clear, easy-to-read results
- **Flexible Configuration**: Customize timeouts and workers

## Usage

### Common Commands

```bash
# Verify all links
python scripts/verify_links.py

# Skip external links (faster)
python scripts/verify_links.py --skip-external

# Only check external links
python scripts/verify_links.py --only-external

# Export results as JSON
python scripts/verify_links.py --json-output report.json

# Verbose output
python scripts/verify_links.py --verbose

# Adjust timeout and workers
python scripts/verify_links.py --timeout 10 --workers 20
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--build-dir` | `docs/build` | Path to Docusaurus build directory |
| `--skip-external` | - | Skip verification of external links |
| `--only-external` | - | Only verify external links |
| `--timeout` | `5` | HTTP request timeout in seconds |
| `--workers` | `10` | Number of concurrent threads |
| `--json-output` | - | Export results to JSON file |
| `--verbose` | - | Enable verbose logging |

## Output

### Console Output

```text
================================================================================
DOCUSAURUS LINK VERIFICATION REPORT
================================================================================

📊 STATISTICS:
  Total HTML files scanned: 156
  Total links found: 1,234
  Internal links: 892
  External links: 342
  Working links: 1,225
  Broken links: 9

❌ BROKEN LINKS (9):
  1. https://example.com/broken (external, HTTP 404)
  2. /docs/missing.html (internal, file not found)

Success Rate: 99.3%
================================================================================
```

### JSON Output

```json
{
  "timestamp": "2025-01-21 10:30:45",
  "statistics": {
    "total_files": 156,
    "total_links": 1234,
    "working_links": 1225,
    "broken_links": 9
  },
  "broken_links": [
    {
      "url": "https://example.com/broken",
      "type": "external",
      "status_code": 404,
      "error": "HTTP 404"
    }
  ]
}
```

## Exit Codes

- `0`: All links verified successfully
- `1`: One or more broken links found
- `130`: Verification interrupted by user (Ctrl+C)

## Link Categories

**Skipped** (not verified):

- Anchors only (`#section`)
- Email links (`mailto:user@example.com`)
- JavaScript (`javascript:void(0)`)
- Data URLs (`data:...`)
- Telephone/SMS (`tel:`, `sms:`)
- FTP (`ftp://`)

**Internal** (file existence checked):

- Relative paths (`../docs/guide.html`)
- Root-relative paths (`/docs/guide.html`)

**External** (HTTP status checked):

- Full URLs (`https://example.com`)
- Protocol-relative URLs (`//cdn.example.com`)

## Troubleshooting

### Build directory not found

```bash
cd docs && npm run build && cd ..
```

### Missing required package

```bash
pip install -r scripts/requirements-links.txt
```

### Too many timeouts

```bash
python scripts/verify_links.py --timeout 15
```

### Script is slow

```bash
# Skip external links for faster internal-only verification
python scripts/verify_links.py --skip-external
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Setup Node and Python
  run: |
    cd docs && npm install && npm run build && cd ..
    pip install -r scripts/requirements-links.txt

- name: Verify Links
  run: python scripts/verify_links.py --json-output report.json

- name: Upload Report
  uses: actions/upload-artifact@v3
  if: always()
  with:
    name: link-verification-report
    path: report.json
```

## Performance

- **Speed**: 30-120 seconds for typical sites
- **Concurrency**: 10 worker threads (configurable)
- **Memory**: Efficient for large sites
- **Internal links**: Sequential (file I/O)
- **External links**: Parallel (HTTP requests)

## Requirements

- Python 3.7+
- Docusaurus build directory at `docs/build/`
- Dependencies: `beautifulsoup4`, `requests`, `colorama`
