# Markdown to PDF Converter

Convert markdown files with YAML frontmatter to professional, print-optimized
PDFs with Docusaurus-inspired styling.

## Quick Start

```bash
# Install dependencies
pip install -r scripts/requirements-pdf.txt

# Convert a single file
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md

# Convert with specific output location
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md --output ./pdfs/

# Batch convert all tutorials
for file in docs/docs/*.md; do
  python scripts/markdown_to_pdf.py "$file" --output ./pdfs/
done
```

## Features

- **YAML Frontmatter Support**: Extract and preserve metadata automatically
- **Professional Styling**: Docusaurus-inspired design with clean typography
- **Print Optimization**: A4 page size with smart margins and formatting
- **Rich Content**: Syntax-highlighted code blocks, styled tables, blockquotes
- **Hyperlinks**: Clickable links with URL display
- **PDF Metadata**: Document title, author, keywords, creation date
- **Image Handling**: Automatic optimization and embedding

## Usage

### Convert Single File

```bash
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md
```

Output: `01_hello_world_agent.pdf` in same directory

### Specify Output Location

```bash
# Save to directory
python scripts/markdown_to_pdf.py input.md --output /path/to/output/

# Save with specific filename
python scripts/markdown_to_pdf.py input.md --output output.pdf
```

### Batch Processing

```bash
# Convert all TIL articles
for file in docs/docs/til/*.md; do
  python scripts/markdown_to_pdf.py "$file" --output ./pdfs/
done
```

### Help and Options

```bash
# Show help
python scripts/markdown_to_pdf.py --help

# Show version
python scripts/markdown_to_pdf.py --version

# Verbose output
python scripts/markdown_to_pdf.py input.md --verbose
```

## Supported Frontmatter

The script recognizes and includes these metadata fields:

```yaml
---
id: tutorial_id
title: "Tutorial Title"
description: "Short description"
author: "Author Name"
publication_date: "2025-01-19"
date: "2025-01-19"
tags: ["tag1", "tag2"]
difficulty: "beginner"
estimated_time: "30 minutes"
keywords: ["keyword1", "keyword2"]
status: "completed"
---
```

All fields are optional. Missing metadata is handled gracefully.

## Markdown Support

### Headings

```markdown
# H1 (blue underline)
## H2 (blue with border)
### H3 - H6 (various styles)
```

### Code Blocks

````markdown
```python
def hello():
    print("World")
```

```javascript
console.log("Hello");
```
````

### Lists

```markdown
- Item 1
  - Nested item
- Item 2

1. First
2. Second
   a. Nested
```

### Tables

```markdown
| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |
```

### Emphasis

```markdown
**Bold text**
_Italic text_
**_Bold italic_**
```

### Links and Images

```markdown
[Link text](https://example.com)
![Alt text](image.png)
```

### Blockquotes

```markdown
> This is a quote
> with multiple lines
```

## Output

### Document Structure

1. **Title Page**: Document title and metadata box
2. **Page Headers/Footers**: Chapter name, document title, page numbers
3. **Content**: Formatted markdown with syntax highlighting
4. **Professional Footer**: Generation timestamp and source reference

### File Size

- Simple tutorial (2-3 pages): 50-100 KB
- Detailed tutorial (10+ pages): 200-400 KB
- Images automatically optimized

## Styling

### Colors

- Primary Blue: `#3b82f6` (headings, links, borders)
- Dark Text: `#1f2937` (body)
- Light Background: `#f9fafb` (metadata, code)
- Dark Code: `#1f2937` (code blocks)

### Typography

- Body Font: System font stack (San Francisco, Segoe UI, etc.)
- Code Font: Monaco, Menlo, Ubuntu Mono
- Base Size: 11pt (print-optimized)
- Line Height: 1.6 (readable spacing)

### Page Format

- Size: A4
- Margins: 2cm on all sides
- Section Spacing: 1.5em before headings, 0.5em after
- Code Block Padding: 1em

## Troubleshooting

### Missing module

```bash
pip install -r scripts/requirements-pdf.txt
```

### PDF is blank or has rendering issues

1. Verify YAML frontmatter syntax:

```yaml
---
title: "Your Title"
---
```

1. Check for special characters - use quotes around titles with colons
1. Escape special characters properly

### Images not showing

- Ensure image paths are relative to markdown file
- Use absolute paths if relative paths fail
- Supported: PNG, JPEG, GIF, SVG

### PDF too large

WeasyPrint automatically optimizes. If still large:

- Reduce image dimensions before converting
- Consider splitting into multiple PDFs (< 50 pages each)
- Adjust code block styling to reduce space

### Special character encoding issues

1. Save markdown file as UTF-8
2. Verify special characters are properly encoded
3. Check YAML syntax is valid

## Performance Tips

- **Large Documents**: Split into multiple PDFs (> 50 pages)
- **Batch Processing**: Use shell scripts for many files
- **Image Optimization**: WeasyPrint handles automatically

## API Usage (Python)

Use the converter in your Python scripts:

```python
from scripts.markdown_to_pdf import MarkdownToPdfConverter

# Create converter
converter = MarkdownToPdfConverter('path/to/document.md')

# Generate PDF
output_pdf = converter.generate_pdf()

# Or specify output location
output_pdf = converter.generate_pdf('output_directory/')

print(f"PDF created: {output_pdf}")
```

## Customization

Edit the `generate_print_optimized_css()` method in `markdown_to_pdf.py`:

```python
def generate_print_optimized_css(self) -> str:
    """Generate professional, print-optimized CSS."""
    css = """
    /* Customize colors, fonts, spacing here */
    """
    return css
```

### Common Customizations

```css
/* Change heading colors */
h1, h2, h3 {
  color: #your-color;
}

/* Change page size */
@page {
  size: letter;  /* letter, legal, A4, A3 */
}

/* Change margins */
@page {
  margin: 1.5cm;
}

/* Change code styling */
pre {
  background: #your-color;
}

/* Change link styling */
a {
  color: #your-color;
}
```

## Requirements

- Python 3.9+
- Dependencies: `python-frontmatter`, `markdown`, `weasyprint`, `pillow`

## Related Documentation

- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/stable/)
- [Markdown Syntax Guide](https://www.markdownguide.org/)
- [YAML Frontmatter Reference](https://jekyllrb.com/docs/front-matter/)
