# Markdown to PDF Converter

Convert Markdown files (with YAML frontmatter) to professional, print-optimized PDFs inspired by Docusaurus styling.

## Features

✨ **YAML Frontmatter Support**

- Automatically extracts and preserves metadata (title, author, date, tags, etc.)
- Includes metadata in PDF properties and document header

📄 **Professional Typography**

- Optimized for printing on A4 paper
- Clear hierarchy with styled headings
- Justified paragraphs with proper orphan/widow control

🎨 **Docusaurus-Inspired Design**

- Color scheme matching the ADK Training Hub
- Modern, clean layout
- Professional spacing and typography

📊 **Rich Content Support**

- Syntax-highlighted code blocks
- Styled tables with alternating row colors
- Blockquotes and emphasis
- Lists and nested lists
- Hyperlinks with URL display

🖨️ **Print Optimization**

- A4 page size with professional margins
- Header and footer with page numbers
- No page breaks within tables or code blocks
- Optimized image handling
- High JPEG quality (95%)

🔗 **Hyperlink Support**

- All links are clickable in PDF readers
- External URLs displayed in footnotes

🏷️ **PDF Metadata**

- Document title, author, keywords, description
- Creation date and timestamp
- Custom metadata preservation

## Installation

1. **Install Python 3.9 or higher**

2. **Install dependencies:**

```bash
pip install -r scripts/requirements-pdf.txt
```

Or install individually:

```bash
pip install python-frontmatter markdown weasyprint pillow
```

## Usage

### Basic Usage

Convert a single markdown file:

```bash
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md
```

This creates `01_hello_world_agent.pdf` in the same directory.

### Specify Output Location

Save PDF to a specific directory:

```bash
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md --output ~/Desktop/
```

Save with a specific filename:

```bash
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md --output ./my_document.pdf
```

### TIL (Today I Learn) Articles

Convert TIL articles:

```bash
python scripts/markdown_to_pdf.py docs/docs/til/til_context_compaction_20250119.md
```

### Batch Processing

Convert all tutorials in a directory:

```bash
# Convert all markdown files in docs/docs/
for file in docs/docs/*.md; do
    python scripts/markdown_to_pdf.py "$file"
done
```

Or using zsh:

```bash
# Convert all files
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md --output ./pdfs/
python scripts/markdown_to_pdf.py docs/docs/02_function_tools.md --output ./pdfs/
# ... and so on
```

### Help and Version

```bash
# Show help
python scripts/markdown_to_pdf.py --help

# Show version
python scripts/markdown_to_pdf.py --version

# Verbose output
python scripts/markdown_to_pdf.py docs/docs/01_hello_world_agent.md --verbose
```

## Supported Frontmatter Fields

The script recognizes and includes these frontmatter fields in the PDF:

```yaml
---
id: tutorial_id
title: "Tutorial Title"
description: "Short description of the tutorial"
author: "Author Name"
publication_date: "2025-01-19"
date: "2025-01-19"
tags: ["tag1", "tag2", "tag3"]
difficulty: "beginner"
estimated_time: "30 minutes"
keywords: ["keyword1", "keyword2"]
status: "completed"
---
```

All fields are optional. The script will gracefully handle missing metadata.

## Output Examples

### Document Structure

The generated PDF includes:

1. **Title Page**

   - Document title (from frontmatter)
   - Metadata box with author, date, difficulty, reading time, tags, description

2. **Page Headers/Footers**

   - Chapter/section name (top left)
   - Document title (top right)
   - Page numbers (bottom center)

3. **Content**

   - Formatted markdown with syntax highlighting
   - Styled tables and lists
   - Preserved hyperlinks

4. **Professional Footer**
   - Generation timestamp
   - Source file reference

### File Size

Typical output sizes:

- Simple tutorial (2-3 pages): 50-100 KB
- Detailed tutorial (10+ pages): 200-400 KB
- Images are optimized automatically

## Markdown Features Supported

### Headings

```markdown
# H1 (blue underline)

## H2 (blue, with border)

### H3-H6 (various styles)
```

### Code Blocks

````markdown
```python
def hello():
    print("World")
```
````

````

### Lists
```markdown
- Item 1
  - Nested item
- Item 2

1. First
2. Second
   a. Nested
````

### Tables

```markdown
| Header 1 | Header 2 |
| -------- | -------- |
| Data 1   | Data 2   |
| Data 3   | Data 4   |
```

### Blockquotes

```markdown
> This is a quote
> with multiple lines
```

### Emphasis

```markdown
**Bold text** or **bold**
_Italic text_ or _italic_
**_Bold italic_**
```

### Links and Images

```markdown
[Link text](https://example.com)
![Alt text](image.png)
```

### Horizontal Rule

```markdown
---
```

## Styling Reference

### Colors (Docusaurus-Inspired)

- **Primary Blue**: #3b82f6 (headings, links, borders)
- **Dark Text**: #1f2937 (body text)
- **Light Background**: #f9fafb (metadata, code background)
- **Dark Code**: #1f2937 (code block background)

### Typography

- **Body Font**: System font stack (San Francisco, Segoe UI, etc.)
- **Code Font**: Monaco, Menlo, Ubuntu Mono, monospace
- **Base Size**: 11pt (print-optimized)
- **Line Height**: 1.6 (readable spacing)

### Margins & Spacing

- **Page Margins**: 2cm on all sides
- **Section Spacing**: 1.5em before headings, 0.5em after
- **Code Block Padding**: 1em

## Troubleshooting

### "ModuleNotFoundError: No module named 'frontmatter'"

Install missing dependencies:

```bash
pip install -r scripts/requirements-pdf.txt
```

### PDF appears blank or has rendering issues

1. Verify the markdown file has valid YAML frontmatter:

   ```yaml
   ---
   title: "Your Title"
   ---
   ```

2. Check for special characters in frontmatter that might break YAML:
   - Use quotes around titles with colons
   - Escape special characters properly

### Images not showing in PDF

- Ensure image paths are relative to the markdown file location
- Use absolute paths if relative paths don't work
- Supported formats: PNG, JPEG, GIF, SVG

### PDF is too large

- WeasyPrint automatically optimizes images
- Consider:
  - Reducing image dimensions before converting
  - Increasing JPEG quality threshold

### Encoding issues with special characters

The script uses UTF-8 encoding by default. If you encounter issues:

1. Ensure your markdown file is saved as UTF-8
2. Check that special characters are properly encoded
3. Verify frontmatter YAML syntax is valid

## Performance Tips

1. **Large Documents**: Break into multiple smaller PDFs if > 50 pages
2. **Image Optimization**: WeasyPrint handles this automatically
3. **Batch Processing**: Use shell scripts for multiple files

## API Usage (Python)

You can also use the converter in your Python scripts:

```python
from pathlib import Path
from scripts.markdown_to_pdf import MarkdownToPdfConverter

# Create converter
converter = MarkdownToPdfConverter('path/to/document.md')

# Generate PDF
output_pdf = converter.generate_pdf()
# or with specific output location
output_pdf = converter.generate_pdf('output_directory/')

print(f"PDF created: {output_pdf}")
```

## Customization

To customize styling, edit the `generate_print_optimized_css()` method in `markdown_to_pdf.py`:

```python
def generate_print_optimized_css(self) -> str:
    """Generate professional, print-optimized CSS."""
    css = """
    /* Customize colors, fonts, spacing here */
    """
    return css
```

Common customizations:

```css
/* Change heading colors */
h1,
h2,
h3 {
  color: #your-color;
}

/* Change page size (letter, legal, A4, A3, etc.) */
@page {
  size: letter;
}

/* Change margins */
@page {
  margin: 1.5cm;
}

/* Change code block styling */
pre {
  background: #your-color;
}

/* Change link styling */
a {
  color: #your-color;
}
```

## License

This script is part of the Google ADK Training Hub and follows the same license as the main project.

## Contributing

Improvements and bug reports welcome! Please submit issues and pull requests to the [GitHub repository](https://github.com/raphaelmansuy/adk_training).

## Related Documentation

- [Docusaurus Configuration](https://docusaurus.io/docs/configuration)
- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/stable/)
- [Markdown Syntax Guide](https://www.markdownguide.org/)
- [YAML Frontmatter Reference](https://jekyllrb.com/docs/front-matter/)

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-19  
**Maintained by**: Google ADK Training Hub
