# Scripts Documentation

Utility scripts for the ADK Training repository.

## Scripts

### Verify Links

Verify all links in the Docusaurus website, checking both internal file
references and external URLs.

**Location**: `scripts/verify_links.py`  
**Documentation**: `scripts/docs/verify_links/README.md`

**Quick Start**:

```bash
pip install -r scripts/requirements-links.txt
python scripts/verify_links.py
```

**Features**:

- Internal and external link verification
- Concurrent multi-threaded checking
- JSON export for CI/CD integration
- Colored console output

[Full Documentation](verify_links/README.md)

### Markdown to PDF

Convert markdown files with YAML frontmatter to professional, print-optimized
PDFs with Docusaurus-inspired styling.

**Location**: `scripts/markdown_to_pdf.py`  
**Documentation**: `scripts/docs/markdown_to_pdf/README.md`

**Quick Start**:

```bash
pip install -r scripts/requirements-pdf.txt
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md
```

**Features**:

- YAML frontmatter support
- Professional print-optimized design
- Syntax-highlighted code blocks
- Automatic image optimization

[Full Documentation](markdown_to_pdf/README.md)

### Batch PDF Generator

Automatically convert all markdown tutorials and TIL articles to professional
PDFs with a single command.

**Location**: `scripts/batch_generate_pdfs.py`  
**Documentation**: `scripts/docs/batch_generate_pdfs/README.md`

**Quick Start**:

```bash
pip install -r scripts/requirements-pdf.txt
python scripts/batch_generate_pdfs.py
```

**Features**:

- Batch processing of all tutorials and TIL articles
- Smart caching to skip recently generated PDFs
- Real-time progress tracking
- Automatic error handling and reporting
- Timestamped execution logs

[Full Documentation](batch_generate_pdfs/README.md)

## Requirements Files

| File | Purpose |
|------|---------|
| `requirements-links.txt` | Dependencies for link verification |
| `requirements-pdf.txt` | Dependencies for PDF conversion |

## Installation

Each script has independent dependencies. Install only what you need:

```bash
# For link verification
pip install -r scripts/requirements-links.txt

# For PDF conversion
pip install -r scripts/requirements-pdf.txt

# For both
pip install -r scripts/requirements-links.txt -r scripts/requirements-pdf.txt
```

## Documentation Structure

```text
scripts/
├── docs/
│   ├── README.md (this file)
│   ├── verify_links/
│   │   └── README.md
│   ├── markdown_to_pdf/
│   │   └── README.md
│   └── batch_generate_pdfs/
│       └── README.md
├── verify_links.py
├── markdown_to_pdf.py
├── batch_generate_pdfs.py
├── requirements-links.txt
└── requirements-pdf.txt
```

## Quick Reference

### Link Verification

```bash
# Basic verification
python scripts/verify_links.py

# Skip external links (faster)
python scripts/verify_links.py --skip-external

# Export as JSON
python scripts/verify_links.py --json-output report.json

# Adjust settings
python scripts/verify_links.py --timeout 10 --workers 20
```

### PDF Conversion

```bash
# Convert single file
python scripts/markdown_to_pdf.py input.md

# Specify output
python scripts/markdown_to_pdf.py input.md --output output.pdf

# Batch convert
for file in docs/docs/*.md; do
  python scripts/markdown_to_pdf.py "$file" --output ./pdfs/
done
```

### Batch PDF Generation

```bash
# Generate all PDFs (tutorials and TIL articles)
python scripts/batch_generate_pdfs.py

# Verbose output showing each file
python scripts/batch_generate_pdfs.py --verbose

# Output goes to: pdf/ directory
# Logs go to: log/ directory
```

## Support

Each script includes:

- Comprehensive README in `scripts/docs/[script_name]/`
- Built-in help: `python scripts/[script_name].py --help`
- Troubleshooting section in documentation

For detailed usage, see individual script documentation.
