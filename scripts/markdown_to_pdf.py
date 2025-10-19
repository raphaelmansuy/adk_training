#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "python-frontmatter>=1.0.0",
#   "markdown>=3.4.0",
#   "weasyprint>=60.0",
#   "pillow>=10.0.0",
# ]
# ///
"""
Markdown to PDF Converter with YAML Frontmatter Support

Converts Markdown files (with YAML frontmatter) to high-quality, print-optimized PDFs.
Respects Docusaurus rendering configuration and creates professional documents.

Usage:
    ./markdown_to_pdf.py <markdown_file> [--output <output_path>]
    ./markdown_to_pdf.py --help

Example:
    ./markdown_to_pdf.py docs/docs/01_hello_world_agent.md
    ./markdown_to_pdf.py docs/docs/til/til_context_compaction_20250119.md --output ~/Desktop/

Features:
    - Parses YAML frontmatter (title, author, date, tags, etc.)
    - Professional typography optimized for printing
    - Docusaurus-inspired design with Dracula syntax highlighting
    - Pygments-powered code highlighting with 40+ language support
    - Hyperlink support with proper path resolution
    - Image and GIF support (automatic embedding)
    - Table of contents generation from headings
    - A4 page size with professional layout
    - Metadata preserved in PDF
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import logging
from datetime import datetime
import re

# First, try to import frontmatter and markdown
try:
    import frontmatter
    from markdown import markdown
except ImportError as e:
    print(f"❌ Missing required dependencies: {e}")
    print("\nPlease install required packages:")
    print("  uv run --script <script_name>")
    sys.exit(1)

# Then, try to import WeasyPrint with special error handling for macOS system libraries
try:
    from weasyprint import HTML, CSS
except (ImportError, OSError) as e:
    error_msg = str(e)
    print(f"❌ WeasyPrint import failed: {e}")
    
    # Check for WeasyPrint system library issues on macOS
    if "libgobject-2.0" in error_msg or "cannot load library" in error_msg or "dlopen" in error_msg:
        print("\n📌 WeasyPrint requires system libraries on macOS.")
        print("\n✨ Solutions:")
        print("\n  1️⃣  Using Homebrew (recommended):")
        print("     brew install weasyprint")
        print("     # Then run the script again")
        print("\n  2️⃣  Set library path manually:")
        print("     export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH")
        print("     ./scripts/markdown_to_pdf.py <markdown_file>")
        print("\n  3️⃣  Using Macports:")
        print("     sudo port install py-pip pango libffi")
        print("     pip install weasyprint")
        print("\n📖 Reference: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#troubleshooting")
    else:
        print("\nPlease install required packages:")
        print("  pip install python-frontmatter markdown weasyprint pillow")
    sys.exit(1)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MarkdownToPdfConverter:
    """Convert Markdown with YAML frontmatter to print-optimized PDF."""

    def __init__(self, markdown_file: str) -> None:
        """
        Initialize the converter with a markdown file path.

        Args:
            markdown_file: Path to markdown file
        """
        self.markdown_file = Path(markdown_file).resolve()  # Convert to absolute path

    def validate_file(self) -> None:
        """Validate that markdown file exists and is readable."""
        if not self.markdown_file.exists():
            raise FileNotFoundError(f"Markdown file not found: {self.markdown_file}")
        if not self.markdown_file.is_file():
            raise ValueError(f"Not a file: {self.markdown_file}")
        if self.markdown_file.suffix.lower() not in ['.md', '.markdown']:
            raise ValueError(f"Not a markdown file: {self.markdown_file}")

    def parse_frontmatter(self) -> None:
        """Parse YAML frontmatter and markdown content."""
        logger.info(f"📖 Parsing frontmatter from {self.markdown_file.name}")
        try:
            with open(self.markdown_file, 'r', encoding='utf-8') as f:
                self.post = frontmatter.load(f)
                self.frontmatter_data = self.post.metadata
                self.markdown_content = self.post.content
            logger.info("✅ Frontmatter parsed successfully")
        except Exception as e:
            logger.error(f"❌ Error parsing frontmatter: {e}")
            raise

    def get_metadata_field(self, field: str, default: str = "") -> str:
        """
        Safely get metadata field with fallback.

        Args:
            field: Field name to retrieve
            default: Default value if field not found

        Returns:
            Field value or default
        """
        return str(self.frontmatter_data.get(field, default))

    def resolve_image_paths(self, html_content: str) -> str:
        """
        Resolve relative image paths to be compatible with PDF rendering.
        Handles both GIFs and static images from Docusaurus public directories.

        Args:
            html_content: HTML content with potential relative image paths

        Returns:
            HTML with resolved image paths
        """
        base_path = self.markdown_file.parent
        docs_dir = self.markdown_file.parent.parent  # Assuming markdown is in docs/docs/

        # Replace relative image paths - handle alt and src in any order
        def replace_src(match):
            # Extract all attributes
            full_tag = match.group(0)
            
            # Extract src and alt from img tag
            src_match = re.search(r'src="([^"]*)"', full_tag)
            alt_match = re.search(r'alt="([^"]*)"', full_tag)
            
            if not src_match:
                return full_tag
                
            src = src_match.group(1)
            alt_text = alt_match.group(1) if alt_match else ""
            
            logger.info(f"Processing image src: {src}")
            
            # Skip if already absolute URL (http, https, data URI)
            if src.startswith(('http://', 'https://', 'data:')):
                logger.debug(f"✓ Keeping absolute URL: {src}")
                return full_tag
            
            # Handle Docusaurus public assets (/img/*, /static/*, etc.)
            if src.startswith('/'):
                # Try multiple locations for Docusaurus assets
                relative_path = src.lstrip('/')
                
                # Check in docs/static directory first
                static_path = docs_dir / 'static' / relative_path
                if static_path.exists():
                    logger.info(f"📷 Found image in docs/static: {src}")
                    file_uri = static_path.as_uri()
                    return f'<img alt="{alt_text}" src="{file_uri}" />'
                
                # Check in docs/build/img (Docusaurus build output)
                build_path = docs_dir / 'build' / relative_path.replace('img/', '', 1)
                if build_path.exists():
                    logger.info(f"📷 Found image in build: {src}")
                    file_uri = build_path.as_uri()
                    return f'<img alt="{alt_text}" src="{file_uri}" />'
                
                # Fallback: try the path as-is relative to project root
                alt_path = docs_dir.parent / relative_path
                if alt_path.exists():
                    logger.info(f"📷 Found image at root level: {src}")
                    file_uri = alt_path.as_uri()
                    return f'<img alt="{alt_text}" src="{file_uri}" />'
                
                logger.warning(f"⚠️  Docusaurus asset not found: {src}")
                return full_tag
            
            # Convert relative path to absolute
            full_path = base_path / src
            if full_path.exists():
                logger.info(f"📷 Found image: {src}")
                file_uri = full_path.as_uri()
                return f'<img alt="{alt_text}" src="{file_uri}" />'
            
            # If file doesn't exist, log warning and keep as-is
            logger.warning(f"⚠️  Image not found: {src}")
            return full_tag

        # Pattern to find img tags (self-closing or with closing tag)
        html_content = re.sub(r'<img\s+[^>]*/?>', replace_src, html_content)
        return html_content

    def clean_docusaurus_directives(self, content: str) -> str:
        """
        Remove Docusaurus-specific directives like import/export statements.

        Args:
            content: Markdown content with potential Docusaurus directives

        Returns:
            Cleaned markdown content
        """
        # Remove import/export statements (Docusaurus JSX directives)
        content = re.sub(r'^import\s+.+from\s+.+;?\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^export\s+.+;?\s*$', '', content, flags=re.MULTILINE)
        # Remove multiple consecutive blank lines
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        return content

    def convert_markdown_to_html(self) -> str:
        """
        Convert markdown content to HTML with proper code highlighting.

        Returns:
            HTML string representation of markdown content
        """
        logger.info("🔄 Converting markdown to HTML")
        try:
            # First, clean Docusaurus directives
            cleaned_content = self.clean_docusaurus_directives(self.markdown_content)

            # Convert markdown to HTML with extensions
            html_content = markdown(
                cleaned_content,
                extensions=[
                    'extra',           # Footnotes, definition lists, etc.
                    'codehilite',      # Code highlighting
                    'toc',             # Table of contents
                    'tables',          # Table support
                    'fenced_code',     # Fenced code blocks
                    'nl2br',           # Newline to break
                    'md_in_html',      # Markdown in HTML
                ]
            )

            # Resolve image paths
            html_content = self.resolve_image_paths(html_content)

            logger.info("✅ Markdown converted to HTML")
            return html_content
        except Exception as e:
            logger.error(f"❌ Error converting markdown: {e}")
            raise

    def generate_print_optimized_css(self) -> str:
        """
        Generate professional, print-optimized CSS with Docusaurus styling and Dracula syntax highlighting.

        Returns:
            CSS string for PDF rendering
        """
        css = """
/* Dracula color scheme variables */
:root {
    --dracula-background: #282a36;
    --dracula-current-line: #44475a;
    --dracula-selection: #44475a;
    --dracula-foreground: #f8f8f2;
    --dracula-comment: #6272a4;
    --dracula-red: #ff5555;
    --dracula-orange: #ffb86c;
    --dracula-yellow: #f1fa8c;
    --dracula-green: #50fa7b;
    --dracula-purple: #bd93f9;
    --dracula-cyan: #8be9fd;
    --dracula-pink: #ff79c6;
}

@page {
    /* A4 page size with professional margins */
    size: A4;
    margin: 2cm;
    
    /* Header and footer */
    @top-left {
        content: string(section);
        font-size: 9pt;
        color: #6b7280;
        border-bottom: 1pt solid #e5e7eb;
        padding-bottom: 0.4cm;
        margin-bottom: 0.3cm;
    }
    
    @top-right {
        content: string(title);
        font-size: 9pt;
        color: #6b7280;
        border-bottom: 1pt solid #e5e7eb;
        padding-bottom: 0.4cm;
        margin-bottom: 0.3cm;
    }
    
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 8pt;
        color: #9ca3af;
        margin-top: 0.4cm;
        border-top: 1pt solid #e5e7eb;
        padding-top: 0.4cm;
    }
}

/* First page special styling */
@page :first {
    margin-top: 3cm;
    @top-left { content: ""; border: none; }
    @top-right { content: ""; border: none; }
    @bottom-center { content: ""; border: none; }
}

/* Body styles - System font stack like Docusaurus */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, system-ui, sans-serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #1f2937;
    background: white;
    padding: 0;
    margin: 0;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Typography - Docusaurus heading styles */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    letter-spacing: -0.025em;
    page-break-after: avoid;
    margin-top: 1.5em;
    margin-bottom: 0.6em;
    color: #1f2937;
    line-height: 1.25;
}

h1 {
    font-size: 28pt;
    border-bottom: 3pt solid #3b82f6;
    padding-bottom: 0.5em;
    margin-bottom: 1em;
    margin-top: 0;
}

h2 {
    font-size: 22pt;
    border-bottom: 2pt solid #e5e7eb;
    padding-bottom: 0.3em;
    color: #3b82f6;
}

h3 {
    font-size: 18pt;
    color: #3b82f6;
    border-left: 4pt solid #3b82f6;
    padding-left: 0.5em;
}

h4 {
    font-size: 16pt;
    color: #1f2937;
}

h5 {
    font-size: 14pt;
    color: #374151;
}

h6 {
    font-size: 12pt;
    font-style: italic;
    color: #6b7280;
}

/* Paragraphs with proper spacing */
p {
    margin: 0.8em 0;
    text-align: justify;
    orphans: 3;
    widows: 3;
}

/* Links - styled like Docusaurus */
a {
    color: #3b82f6;
    text-decoration: none;
    border-bottom: 1pt solid #3b82f6;
}

a[href]::after {
    content: " (" attr(href) ")";
    font-size: 8pt;
    color: #6b7280;
    border: none;
}

/* Lists with proper spacing */
ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin: 0.4em 0;
    line-height: 1.6;
}

ul li {
    list-style-type: disc;
}

ol li {
    list-style-type: decimal;
}

/* Nested lists */
ul ul, ol ol, ul ol, ol ul {
    margin: 0.3em 0;
    padding-left: 1.5em;
}

/* Inline code - Docusaurus style */
code {
    font-family: 'JetBrains Mono', 'Fira Code', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 10pt;
    background: #f3f4f6;
    padding: 0.15em 0.35em;
    border-radius: 4px;
    color: #111827;
    border: 1pt solid #e5e7eb;
}

/* Code blocks - Dracula theme with syntax highlighting */
pre {
    background: var(--dracula-background);
    color: var(--dracula-foreground);
    padding: 1.2em;
    border-radius: 8px;
    overflow: hidden;
    font-size: 10pt;
    line-height: 1.5;
    margin: 1.2em 0;
    page-break-inside: avoid;
    border: 1pt solid var(--dracula-current-line);
}

pre code {
    background: transparent;
    padding: 0;
    color: var(--dracula-foreground);
    border: none;
    font-family: 'JetBrains Mono', 'Fira Code', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

/* Syntax highlighting tokens - Dracula colors */
.token.comment,
.token.prolog,
.token.doctype,
.token.cdata {
    color: var(--dracula-comment);
}

.token.keyword,
.token.namespace {
    color: var(--dracula-pink);
    font-weight: 600;
}

.token.string,
.token.char,
.token.regex,
.token.inserted {
    color: var(--dracula-yellow);
}

.token.number,
.token.boolean {
    color: var(--dracula-purple);
    font-weight: 600;
}

.token.function,
.token.attr-name {
    color: var(--dracula-green);
    font-weight: 500;
}

.token.variable,
.token.constant,
.token.deleted {
    color: var(--dracula-orange);
}

.token.property {
    color: var(--dracula-cyan);
}

.token.class-name {
    color: var(--dracula-cyan);
    font-weight: 600;
}

.token.punctuation {
    color: var(--dracula-foreground);
}

.token.operator {
    color: var(--dracula-pink);
}

.token.entity {
    color: var(--dracula-green);
}

.token.url {
    color: var(--dracula-yellow);
}

.token.symbol {
    color: var(--dracula-green);
}

.token.selector {
    color: var(--dracula-pink);
}

.token.atrule {
    color: var(--dracula-cyan);
}

.token.important,
.token.bold {
    font-weight: 700;
}

.token.italic {
    font-style: italic;
}

/* Pygments token styling - for markdown codehilite */
.c { color: var(--dracula-comment); }          /* Comment */
.c1 { color: var(--dracula-comment); }         /* Comment.Single */
.cm { color: var(--dracula-comment); }         /* Comment.Multiline */
.cp { color: var(--dracula-cyan); }            /* Comment.Preproc */
.cs { color: var(--dracula-comment); }         /* Comment.Special */
.k { color: var(--dracula-pink); font-weight: 600; }   /* Keyword */
.kc { color: var(--dracula-purple); }          /* Keyword.Constant */
.kd { color: var(--dracula-pink); font-weight: 600; }  /* Keyword.Declaration */
.kn { color: var(--dracula-pink); }            /* Keyword.Namespace */
.kp { color: var(--dracula-pink); }            /* Keyword.Pseudo */
.kr { color: var(--dracula-pink); font-weight: 600; }  /* Keyword.Reserved */
.kt { color: var(--dracula-cyan); }            /* Keyword.Type */
.m { color: var(--dracula-purple); }           /* Number */
.mf { color: var(--dracula-purple); }          /* Number.Float */
.mh { color: var(--dracula-purple); }          /* Number.Hex */
.mi { color: var(--dracula-purple); }          /* Number.Integer */
.mo { color: var(--dracula-purple); }          /* Number.Oct */
.s { color: var(--dracula-yellow); }           /* String */
.s1 { color: var(--dracula-yellow); }          /* String.Single */
.s2 { color: var(--dracula-yellow); }          /* String.Double */
.se { color: var(--dracula-orange); }          /* String.Escape */
.sh { color: var(--dracula-yellow); }          /* String.Heredoc */
.si { color: var(--dracula-orange); }          /* String.Interpol */
.sx { color: var(--dracula-yellow); }          /* String.Other */
.sr { color: var(--dracula-yellow); }          /* String.Regex */
.ss { color: var(--dracula-yellow); }          /* String.Symbol */
.nb { color: var(--dracula-cyan); }            /* Name.Builtin */
.nc { color: var(--dracula-cyan); }            /* Name.Class */
.no { color: var(--dracula-orange); }          /* Name.Constant */
.nd { color: var(--dracula-cyan); }            /* Name.Decorator */
.ni { color: var(--dracula-cyan); }            /* Name.Entity */
.ne { color: var(--dracula-red); }             /* Name.Exception */
.nf { color: var(--dracula-green); font-weight: 500; } /* Name.Function */
.nl { color: var(--dracula-cyan); }            /* Name.Label */
.nn { color: var(--dracula-cyan); }            /* Name.Namespace */
.nt { color: var(--dracula-pink); }            /* Name.Tag */
.nv { color: var(--dracula-cyan); }            /* Name.Variable */
.ow { color: var(--dracula-pink); }            /* Operator.Word */
.w { color: var(--dracula-foreground); }       /* Text.Whitespace */
.mb { color: var(--dracula-purple); }          /* Number.Bin */
.bp { color: var(--dracula-cyan); }            /* Name.Builtin.Pseudo */
.dl { color: var(--dracula-yellow); }          /* String.Delimiter */
.err { color: var(--dracula-red); }            /* Error */
.g { }                                          /* Generic */
.gd { color: var(--dracula-red); }             /* Generic.Deleted */
.gh { color: var(--dracula-cyan); font-weight: 600; } /* Generic.Heading */
.gi { color: var(--dracula-green); }           /* Generic.Inserted */
.go { color: var(--dracula-comment); }         /* Generic.Output */
.gp { color: var(--dracula-comment); }         /* Generic.Prompt */
.gs { font-weight: 600; }                      /* Generic.Strong */
.gu { color: var(--dracula-cyan); font-weight: 600; } /* Generic.Subheading */
.gt { color: var(--dracula-red); }             /* Generic.Traceback */
.o { color: var(--dracula-pink); }             /* Operator */
.p { color: var(--dracula-foreground); }       /* Punctuation */

/* Tables - Professional styling */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1.2em 0;
    page-break-inside: avoid;
    border: 1pt solid #e5e7eb;
}

thead {
    background: #3b82f6;
    color: white;
}

th {
    padding: 0.7em 0.6em;
    text-align: left;
    font-weight: 600;
    border: 1pt solid #d1d5db;
    background: #3b82f6;
    color: white;
}

td {
    padding: 0.6em;
    border: 1pt solid #d1d5db;
    line-height: 1.5;
}

tbody tr:nth-child(odd) {
    background: #f9fafb;
}

tbody tr:nth-child(even) {
    background: white;
}

tbody tr:hover {
    background: #f3f4f6;
}

/* Blockquotes - styled like Docusaurus */
blockquote {
    margin: 1.2em 0;
    padding: 0.8em 1em;
    border-left: 4pt solid #3b82f6;
    background: #eff6ff;
    page-break-inside: avoid;
    border-radius: 0 4px 4px 0;
}

blockquote p {
    margin: 0.3em 0;
    color: #0c5bb0;
}

blockquote strong {
    color: #0c5bb0;
}

/* Images and GIFs - Optimized for print */
img {
    max-width: 100%;
    height: auto;
    page-break-inside: avoid;
    margin: 1.2em 0;
    border-radius: 6px;
    border: 1pt solid #e5e7eb;
    display: block;
}

/* Image captions */
figure {
    margin: 1.2em 0;
    page-break-inside: avoid;
}

figcaption {
    font-size: 10pt;
    color: #6b7280;
    margin-top: 0.4em;
    text-align: center;
    font-style: italic;
}

/* Strong and emphasis */
strong, b {
    font-weight: 600;
    color: #111827;
}

em, i {
    font-style: italic;
}

/* Horizontal rules */
hr {
    border: none;
    border-top: 2pt solid #e5e7eb;
    margin: 2em 0;
    page-break-inside: avoid;
}

/* Page breaks */
.page-break {
    page-break-after: always;
}

/* Utility classes for frontmatter */
.frontmatter-title {
    string-set: title content();
}

.frontmatter-section {
    string-set: section content();
}

/* Document metadata section */
.doc-meta {
    background: #f0f9ff;
    padding: 1em;
    border-radius: 8px;
    margin: 1.5em 0;
    font-size: 10pt;
    color: #6b7280;
    page-break-inside: avoid;
    border: 1pt solid #dbeafe;
    border-left: 4pt solid #3b82f6;
}

.doc-meta-item {
    display: block;
    margin: 0.4em 0;
    line-height: 1.4;
}

.doc-meta-label {
    font-weight: 700;
    color: #1f2937;
    margin-right: 0.3em;
}

/* Document content wrapper */
.doc-content {
    margin-top: 1.5em;
}

/* Ensure no widows and orphans */
p, li, td, th, blockquote {
    orphans: 3;
    widows: 3;
}

/* Print-specific optimizations */
@media print {
    body {
        background: white !important;
    }
    
    a {
        color: #0066cc !important;
    }
    
    img {
        page-break-inside: avoid;
    }
    
    pre {
        page-break-inside: avoid;
    }
    
    table {
        page-break-inside: avoid;
    }
}
        """
        return css

    def build_html_document(self, html_content: str) -> str:
        """
        Build complete HTML document with metadata.

        Args:
            html_content: HTML content from markdown conversion

        Returns:
            Complete HTML document string
        """
        # Extract metadata
        title = self.get_metadata_field('title', 'Document')
        description = self.get_metadata_field('description', '')
        author = self.get_metadata_field('author', '')
        date = self.get_metadata_field('publication_date', '')
        tags = self.frontmatter_data.get('tags', [])
        difficulty = self.get_metadata_field('difficulty', '')
        estimated_time = self.get_metadata_field('estimated_time', '')

        # Format tags
        tags_str = ', '.join(tags) if isinstance(tags, list) else str(tags)

        # Get base URL for resolving relative paths
        # Set to the docs directory so /img/* resolves to docs/static/img/*
        docs_dir = self.markdown_file.parent.parent  # Go up from docs/docs to docs/
        base_url = docs_dir.as_uri()

        # Build HTML document
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <base href="{base_url}/static/">
    <title>{title}</title>
    <meta name="description" content="{description}">
    {f'<meta name="author" content="{author}">' if author else ''}
    <meta name="keywords" content="{tags_str}">
</head>
<body>
    <!-- Document title with metadata -->
    <h1 class="frontmatter-title">{title}</h1>
    
    <!-- Metadata section -->
    <div class="doc-meta">
        {f'<span class="doc-meta-item"><span class="doc-meta-label">Author:</span> {author}</span>' if author else ''}
        {f'<span class="doc-meta-item"><span class="doc-meta-label">Date:</span> {date}</span>' if date else ''}
        {f'<span class="doc-meta-item"><span class="doc-meta-label">Difficulty:</span> {difficulty}</span>' if difficulty else ''}
        {f'<span class="doc-meta-item"><span class="doc-meta-label">Reading Time:</span> {estimated_time}</span>' if estimated_time else ''}
        {f'<span class="doc-meta-item"><span class="doc-meta-label">Tags:</span> {tags_str}</span>' if tags_str else ''}
        {f'<span class="doc-meta-item"><span class="doc-meta-label">Description:</span> {description}</span>' if description else ''}
    </div>
    
    <!-- Main content -->
    <div class="doc-content">
        {html_content}
    </div>
    
    <!-- Generated footer -->
    <div style="margin-top: 3em; border-top: 2pt solid #e5e7eb; padding-top: 1em; font-size: 9pt; color: #9ca3af;">
        <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} from {self.markdown_file.name}</p>
        <p>Source: Google ADK Training Hub</p>
    </div>
</body>
</html>"""
        return html_doc

    def generate_pdf(self, output_path: Optional[Path] = None) -> Path:
        """
        Generate PDF from markdown file.

        Args:
            output_path: Optional output directory or file path

        Returns:
            Path to generated PDF file
        """
        # Parse frontmatter
        self.parse_frontmatter()

        # Convert markdown to HTML
        html_content = self.convert_markdown_to_html()

        # Build complete HTML document
        complete_html = self.build_html_document(html_content)

        # Generate CSS
        css_content = self.generate_print_optimized_css()

        # Determine output path
        if output_path is None:
            output_pdf = self.markdown_file.with_suffix('.pdf')
        else:
            output_path = Path(output_path)
            if output_path.is_dir():
                output_pdf = output_path / self.markdown_file.with_suffix('.pdf').name
            else:
                output_pdf = output_path

        logger.info(f"📝 Generating PDF: {output_pdf}")

        try:
            # Render HTML to PDF
            HTML(string=complete_html).write_pdf(
                target=str(output_pdf),
                stylesheets=[CSS(string=css_content)],
                optimize_images=True,
                jpeg_quality=95,
                pdf_tags=True,
                custom_metadata=True,
            )
            logger.info(f"✅ PDF generated successfully: {output_pdf}")
            logger.info(f"📊 File size: {output_pdf.stat().st_size / 1024:.1f} KB")
            return output_pdf
        except Exception as e:
            logger.error(f"❌ Error generating PDF: {e}")
            raise


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog='markdown_to_pdf',
        description='Convert Markdown files (with YAML frontmatter) to high-quality print-optimized PDFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s docs/docs/01_hello_world_agent.md
  %(prog)s docs/docs/til/til_context_compaction_20250119.md --output ~/Desktop/
  %(prog)s docs/docs/*.md --output ./output/

Features:
  ✨ YAML frontmatter parsing (title, author, date, tags, etc.)
  📄 Professional typography optimized for printing
  🎨 Docusaurus-inspired color scheme
  📊 Code syntax highlighting
  🔗 Hyperlink support
  📑 Table of contents
  🖨️  A4 page size with professional layout
  🏷️  PDF metadata preservation
        """
    )

    parser.add_argument(
        'markdown_file',
        help='Path to markdown file to convert (supports wildcards)',
        metavar='FILE'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output directory or file path (default: same directory as input)',
        metavar='PATH',
        default=None
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        # Convert markdown to PDF
        converter = MarkdownToPdfConverter(args.markdown_file)
        output_pdf = converter.generate_pdf(args.output)

        print(f"\n✅ Success! PDF created: {output_pdf}")
        print(f"📂 Location: {output_pdf.absolute()}")

    except FileNotFoundError as e:
        logger.error(f"❌ File error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"❌ Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
