# Batch PDF Generator

Automatically convert all markdown tutorials and TIL articles to professional
PDFs with a single command.

## Quick Start

```bash
# Install dependencies (if not already done)
pip install -r scripts/requirements-pdf.txt

# Generate all PDFs
python scripts/batch_generate_pdfs.py

# Generate with verbose output
python scripts/batch_generate_pdfs.py --verbose
```

## Features

- **Batch Processing**: Convert all tutorials and TIL articles in one run
- **Smart Caching**: Skips recently generated PDFs (within 1 hour)
- **Progress Tracking**: Real-time progress with clear status indicators
- **Error Handling**: Continues processing on failures, reports summary
- **Automatic Logging**: Creates timestamped reports of each run
- **Organized Output**: Saves all PDFs to `pdf/` directory
- **Timeout Protection**: 2-minute timeout per file prevents hangs

## Usage

### Basic Usage

Generate PDFs for all markdown files:

```bash
python scripts/batch_generate_pdfs.py
```

### Verbose Output

See detailed information for each file:

```bash
python scripts/batch_generate_pdfs.py --verbose
```

### What Gets Generated

The script automatically processes:

**Tutorials** (from `docs/docs/`):

- All `*.md` files except:
  - `intro.md`
  - `contact.md`
  - `credits.md`
  - `license.md`
  - `completion-status.md`

**TIL Articles** (from `docs/docs/til/`):

- All `*.md` files except:
  - `TIL_TEMPLATE.md`
  - `TIL_INDEX.md`

## Output

### Console Output

```text
🚀 Starting PDF generation for 45 files...

📂 Output directory: /path/to/pdf/

[01/45] 🔄 Processing 01_hello_world_agent.md... ✅ (125.3 KB)
[02/45] 🔄 Processing 02_function_tools.md... ✅ (98.7 KB)
[03/45] ⏭️  SKIP  03_agents_composition.md (already exists)
...

============================================================
📊 PDF Generation Summary
============================================================
✅ Successful: 42
❌ Failed:     0
⏭️  Skipped:    3
📊 Total:      45
⏱️  Time:       245.3s
============================================================

📁 PDFs in pdf/: 45 files
📝 Log saved to: log/20250121_090030_batch_pdf_generation.md
```

### Logging

Each run creates a timestamped log in `log/`:

```markdown
# Batch PDF Generation Report

**Date:** 2025-01-21T09:00:30.123456

## Summary

- **Successful:** 42
- **Failed:** 0
- **Skipped:** 3
- **Total:** 45
- **Time:** 245.3s

## Details

- **Output Directory:** /path/to/pdf/
- **PDF Count:** 45
```

## Output Directory

All generated PDFs are saved to:

```text
pdf/
├── 01_hello_world_agent.pdf
├── 02_function_tools.pdf
├── 03_agents_composition.pdf
├── ...
├── til_context_compaction_20250119.pdf
├── til_pause_resume_20251020.pdf
└── til_rubric_based_tool_use_quality_20251021.pdf
```

## Smart Caching

The script uses intelligent caching to avoid regenerating PDFs:

- **Recent PDFs** (modified < 1 hour ago): Skipped
- **Old/Missing PDFs**: Regenerated

To force regeneration of all PDFs:

```bash
# Remove all PDFs in pdf/ directory
rm pdf/*.pdf

# Regenerate all
python scripts/batch_generate_pdfs.py
```

## Performance

### Typical Performance

- **Small sites** (< 30 files): 2-3 minutes
- **Medium sites** (30-60 files): 5-8 minutes
- **Large sites** (> 60 files): 10-20 minutes

### Optimization Tips

1. **First Run**: All PDFs generated, takes longest
2. **Subsequent Runs**: Most PDFs skipped (if unchanged), very fast
3. **Selective Regeneration**: Only modify markdown files you want to update
4. **Parallel Runs**: Don't run multiple instances simultaneously

## File Size

Typical PDF sizes:

- Simple tutorial (2-3 pages): 50-100 KB
- Detailed tutorial (10+ pages): 200-400 KB
- TIL article (5-8 pages): 100-150 KB

**Total disk space** for all PDFs: 15-25 MB (depending on content)

## Exit Codes

- `0`: All PDFs generated successfully
- `1`: One or more PDFs failed to generate

Use exit code in CI/CD:

```bash
python scripts/batch_generate_pdfs.py
if [ $? -eq 0 ]; then
  echo "All PDFs generated successfully"
else
  echo "Some PDFs failed to generate"
  exit 1
fi
```

## Troubleshooting

### "Module not found" error

Install missing dependencies:

```bash
pip install -r scripts/requirements-pdf.txt
```

### PDFs are not updating

The script skips recently modified PDFs. To force regeneration:

```bash
# Option 1: Delete specific PDFs
rm pdf/filename.pdf

# Option 2: Delete all PDFs
rm pdf/*.pdf

# Option 3: Wait 1 hour (cache expires)
```

### Script times out on a file

Some complex markdown files may take longer. Edit the timeout in the script:

```python
# Change timeout from 120 seconds to 300 seconds
timeout=300,  # Increase this value
```

### Disk space issues

Check available space:

```bash
df -h

# Clean old PDFs (keep only recent ones)
find pdf/ -type f -mtime +30 -delete
```

### Out of memory

If processing very large files:

1. Process subsets separately
2. Increase system virtual memory
3. Consider splitting documentation into smaller sections

## CI/CD Integration

### GitHub Actions

```yaml
name: Generate Documentation PDFs

on:
  push:
    branches: [main]
    paths:
      - 'docs/docs/**/*.md'

jobs:
  generate-pdfs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r scripts/requirements-pdf.txt

      - name: Generate PDFs
        run: python scripts/batch_generate_pdfs.py

      - name: Commit PDFs
        run: |
          git add pdf/
          git commit -m "docs: regenerate PDFs" || true
          git push
```

### Manual Trigger

```bash
# Generate PDFs locally
python scripts/batch_generate_pdfs.py

# Add and commit changes
git add pdf/
git commit -m "docs: regenerate PDFs"
git push
```

## Advanced Configuration

### Filter by Pattern

Modify the script to process only specific files:

```python
# Only process files matching a pattern
for md_file in sorted(docs_dir.glob("tutorial_*.md")):
    if md_file.name not in exclude_files:
        md_files.append((md_file, "tutorial"))
```

### Change Output Directory

Edit the script to use a different output directory:

```python
# Change output directory
pdf_dir = project_root / "docs" / "static" / "pdfs"
```

### Adjust Cache Timeout

Modify cache expiration time:

```python
# Change from 3600 seconds (1 hour) to 86400 (24 hours)
if file_age < 86400:  # 24 hours
```

## Requirements

- Python 3.9+
- Dependencies: `python-frontmatter`, `markdown`, `weasyprint`, `pillow`
- Free disk space: 30-50 MB
- RAM: 2+ GB (for processing large documents)

## Related Documentation

- [Markdown to PDF Converter](../markdown_to_pdf/README.md)
- [Scripts Overview](../README.md)
- [PDF Metadata Support](../markdown_to_pdf/README.md#supported-frontmatter)

## Log Files

Batch generation creates timestamped logs in `log/` directory:

- Pattern: `log/YYYYMMDD_HHMMSS_batch_pdf_generation.md`
- Contains: Summary, failed files list, execution time, PDF count
- Useful for: Tracking generation history, debugging failures
