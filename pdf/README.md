# PDF Directory - Complete Tutorial and TIL Collection

This directory contains high-quality PDF versions of all tutorials and TIL (Today I Learned) documents from the Google ADK Training Hub.

## 📊 Contents

- **49 Total PDFs** (16 MB total size)
- **35 Tutorial PDFs** (00_setup_authentication through 34_pubsub_adk_integration)
- **13 Reference/Guide PDFs** (cheat sheets, patterns, deployment guides, etc.)
- **1 TIL PDF** (Context Compaction - 20250119)

## ✨ Features

### Quality Features

- ✅ **Professional Typography** - System font stack like modern web interfaces
- ✅ **Syntax Highlighting** - Dracula color scheme for code blocks (40+ language support)
- ✅ **Mermaid Diagrams** - All diagrams rendered at 2X resolution (192 DPI equivalent)
- ✅ **Image Support** - All images and GIFs embedded with proper resolution
- ✅ **Metadata Preservation** - YAML frontmatter converted to PDF metadata
- ✅ **Print Optimized** - A4 page size with professional margins and headers/footers
- ✅ **Table Support** - Professional styling with alternating row colors
- ✅ **Responsive Layout** - Optimized for both screen and print viewing

### Technical Details

- **PDF Version**: 1.7
- **Encoding**: UTF-8
- **Image Quality**: 95% JPEG quality, optimized
- **Code Highlighting**: Pygments-powered with Dracula theme
- **Diagram Rendering**: mermaid-cli (mmdc) with 2X scale factor
- **Typography**: Professional serif/sans-serif mix for readability

## 📂 File Organization

### Tutorial PDFs (Numbered 00-34)

```
00_setup_authentication.pdf
01_hello_world_agent.pdf
02_function_tools.pdf
03_openapi_tools.pdf
04_sequential_workflows.pdf    (Contains Mermaid diagrams)
...
34_pubsub_adk_integration.pdf
```

### Reference & Guide PDFs

```
adk-cheat-sheet.pdf
advanced-patterns.pdf
agent-architecture.pdf
decision-frameworks.pdf
glossary.pdf
learning-paths.pdf
llm-integration.pdf
overview.pdf
production-deployment.pdf
reference-guide.pdf
tools-capabilities.pdf
tutorial_index.pdf
workflows-orchestration.pdf
```

### TIL (Today I Learned) PDFs

```
til_context_compaction_20250119.pdf
```

## 🚀 Usage

### Opening PDFs

- **macOS**: Double-click to open in Preview or your default PDF viewer
- **Windows**: Double-click to open in Edge or Adobe Reader
- **Linux**: Open with your preferred PDF viewer (Evince, Okular, etc.)

### Printing

- **Color Printing**: Full color with syntax highlighting (recommended)
- **B&W Printing**: Still readable but code highlighting less visible
- **Page Range**: All PDFs support printing specific page ranges
- **Paper Size**: Optimized for A4 (can print on Letter size with scaling)

### Digital Reading

- **Screen Viewing**: Optimized for 100% zoom on most screens
- **Mobile Viewing**: Most PDFs work well on tablets and large phones
- **Bookmarking**: Use your PDF viewer's bookmark feature to navigate

## 📈 Statistics

### Size Breakdown (Approximate)

- **Small PDFs** (< 200 KB): Setup, loops, callbacks, etc.
- **Medium PDFs** (200-600 KB): Most tutorials
- **Large PDFs** (> 600 KB): Advanced tutorials with many diagrams
- **Largest PDFs**: Sequential Workflows (1.2 MB), Multi-Agent Systems (778 KB)

### Content Summary

| Category | Count | Size |
|----------|-------|------|
| Tutorials | 35 | ~13 MB |
| Reference Guides | 13 | ~3 MB |
| TIL Articles | 1 | ~184 KB |
| **Total** | **49** | **~16 MB** |

## 🔄 Batch Generation

### Regenerating PDFs

To regenerate all PDFs (for example, after updating markdown files):

```bash
cd /path/to/adk_training
python batch_generate_pdfs.py
```

### Requirements for Generation

- Python 3.8+
- Node.js and npm (for Mermaid diagram rendering)
- Required Python packages: `python-frontmatter`, `markdown`, `weasyprint`, `pillow`
- Optional: `mermaid-cli` installed globally for faster rendering

```bash
# Install dependencies
pip install python-frontmatter markdown weasyprint pillow

# Install mermaid-cli globally (optional but recommended)
npm install -g @mermaid-js/mermaid-cli
```

### Generation Performance

- **Speed**: ~2.2 seconds per PDF on average
- **Total Time**: ~110 seconds for all 49 PDFs
- **Parallelization**: Currently sequential (can be modified for batch processing)

## 📝 Generation Process

### What Happens During Generation

1. **Frontmatter Parsing** - Extracts YAML metadata (title, author, tags, etc.)
2. **Mermaid Diagram Extraction** - Identifies all mermaid code blocks
3. **Diagram Rendering** - Uses mermaid-cli to render to PNG at 2X resolution
4. **Markdown to HTML** - Converts with syntax highlighting
5. **Image Resolution** - Embeds all images with proper paths
6. **CSS Styling** - Applies professional print-optimized styles
7. **PDF Generation** - WeasyPrint renders final PDF

### Fallback Behavior

- **No mermaid-cli**: Diagrams are skipped (gracefully)
- **Missing Images**: Paths are preserved but noted as warnings
- **Large Diagrams**: Automatically scaled to fit page width

## 🐛 Troubleshooting

### PDF Generation Fails

**Issue**: `WeasyPrint import failed` on macOS

**Solution**:
```bash
# Option 1: Using Homebrew
brew install weasyprint

# Option 2: Set library path
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH
```

### Mermaid Diagrams Not Rendering

**Issue**: Mermaid diagrams appear as text in PDF

**Solution**:
```bash
# Install mermaid-cli globally
npm install -g @mermaid-js/mermaid-cli

# Regenerate PDFs
python batch_generate_pdfs.py
```

### Slow PDF Generation

**Issue**: Generation takes several minutes

**Solution**:
- Install `mmdc` globally: `npm install -g @mermaid-js/mermaid-cli`
- This avoids the npx package download overhead on each diagram

## 📚 Related Resources

- **Source Markdown**: `/docs/docs/*.md` and `/docs/docs/til/`
- **Conversion Script**: `/scripts/markdown_to_pdf.py`
- **Batch Generation Script**: `/batch_generate_pdfs.py`
- **Conversion Log**: `/log/` (contains detailed generation reports)

## 📋 PDF Metadata

All PDFs include the following metadata (extracted from frontmatter):

- **Title**: Full tutorial/article name
- **Author**: Original author (if specified)
- **Subject**: Article description
- **Keywords**: Tags for searching
- **Producer**: WeasyPrint 64.1
- **Creation Date**: Generation timestamp

Example metadata extraction (using macOS):

```bash
mdls 01_hello_world_agent.pdf
```

Or with pdfinfo:

```bash
pdfinfo 01_hello_world_agent.pdf
```

## 🎨 Customization

To customize PDF generation (fonts, colors, margins, etc.):

1. Edit `/scripts/markdown_to_pdf.py`
2. Modify the `generate_print_optimized_css()` method
3. Regenerate PDFs: `python batch_generate_pdfs.py`

Key customization points:

- **Fonts**: Lines 450-470 in the CSS section
- **Colors**: Dracula theme variables at lines 445-453
- **Page Margins**: `@page { margin: 2cm; }` at line 473
- **Header/Footer**: Lines 476-502 contain page formatting

## 📄 License

These PDFs are generated from markdown source files in the ADK Training repository. 
Licensing follows the original content's license terms.

---

**Last Updated**: October 19, 2025
**Generation Time**: ~110 seconds
**Total Size**: ~16 MB
**Format**: PDF 1.7 (Portable Document Format)

For questions or issues, see the main repository README or contact the maintainers.
