#!/usr/bin/env python3
"""
Batch generate PDFs for all tutorials and TILs.

This script converts all markdown files in docs/docs/ and docs/docs/til/
to PDF files in the pdf/ directory.

Usage:
    python batch_generate_pdfs.py
    python batch_generate_pdfs.py --verbose
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import time

def generate_pdfs():
    """Generate PDFs for all markdown files."""
    
    # Get paths - adjust for scripts/ subdirectory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # Go up one level to project root
    docs_dir = project_root / "docs" / "docs"
    til_dir = docs_dir / "til"
    pdf_dir = project_root / "pdf"
    script_path = script_dir / "markdown_to_pdf.py"
    
    # Ensure pdf directory exists
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect markdown files
    md_files = []
    
    # Add tutorial files (exclude certain files)
    exclude_files = {
        "intro.md",
        "contact.md",
        "credits.md",
        "license.md",
        "completion-status.md",
        "TIL_TEMPLATE.md",
        "TIL_INDEX.md",
    }
    
    for md_file in sorted(docs_dir.glob("*.md")):
        if md_file.name not in exclude_files:
            md_files.append((md_file, "tutorial"))
    
    # Add TIL files (exclude template and index)
    for md_file in sorted(til_dir.glob("*.md")):
        if md_file.name not in exclude_files:
            md_files.append((md_file, "til"))
    
    total_files = len(md_files)
    successful = 0
    failed = 0
    skipped = 0
    failed_files = []
    
    print(f"🚀 Starting PDF generation for {total_files} files...\n")
    print(f"📂 Output directory: {pdf_dir}\n")
    
    start_time = time.time()
    
    for idx, (md_file, file_type) in enumerate(md_files, 1):
        pdf_file = pdf_dir / md_file.with_suffix(".pdf").name
        
        # Skip if already exists and is recent (within 1 hour)
        if pdf_file.exists():
            file_age = time.time() - pdf_file.stat().st_mtime
            if file_age < 3600:  # 1 hour
                print(f"[{idx:2d}/{total_files}] ⏭️  SKIP  {md_file.name} (already exists)")
                skipped += 1
                continue
        
        print(f"[{idx:2d}/{total_files}] 🔄 Processing {md_file.name}...", end=" ", flush=True)
        
        try:
            # Run the conversion script
            result = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    str(md_file),
                    "--output",
                    str(pdf_dir),
                ],
                capture_output=True,
                text=True,
                timeout=120,  # 2 minute timeout per file
            )
            
            if result.returncode == 0:
                if pdf_file.exists():
                    size_kb = pdf_file.stat().st_size / 1024
                    print(f"✅ ({size_kb:.1f} KB)")
                    successful += 1
                else:
                    print(f"❌ (PDF not created)")
                    failed += 1
                    failed_files.append((md_file.name, "PDF not found"))
            else:
                error_msg = result.stderr.split('\n')[-2] if result.stderr else "Unknown error"
                print(f"❌ ({error_msg})")
                failed += 1
                failed_files.append((md_file.name, error_msg))
                
        except subprocess.TimeoutExpired:
            print(f"❌ (Timeout)")
            failed += 1
            failed_files.append((md_file.name, "Timeout"))
        except Exception as e:
            print(f"❌ ({str(e)})")
            failed += 1
            failed_files.append((md_file.name, str(e)))
    
    elapsed_time = time.time() - start_time
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 PDF Generation Summary")
    print(f"{'='*60}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed:     {failed}")
    print(f"⏭️  Skipped:    {skipped}")
    print(f"📊 Total:      {total_files}")
    print(f"⏱️  Time:       {elapsed_time:.1f}s")
    print(f"{'='*60}\n")
    
    if failed_files:
        print("Failed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")
        print()
    
    # Verify PDFs in output directory
    pdf_count = len(list(pdf_dir.glob("*.pdf")))
    print(f"📁 PDFs in {pdf_dir.name}/: {pdf_count} files")
    
    # Create or update summary log
    log_file = project_root / "log" / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_batch_pdf_generation.md"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_file, "w") as f:
        f.write(f"# Batch PDF Generation Report\n\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- **Successful:** {successful}\n")
        f.write(f"- **Failed:** {failed}\n")
        f.write(f"- **Skipped:** {skipped}\n")
        f.write(f"- **Total:** {total_files}\n")
        f.write(f"- **Time:** {elapsed_time:.1f}s\n\n")
        
        if failed_files:
            f.write(f"## Failed Files\n\n")
            for filename, error in failed_files:
                f.write(f"- **{filename}**: {error}\n")
        
        f.write(f"\n## Details\n\n")
        f.write(f"- **Output Directory:** {pdf_dir}\n")
        f.write(f"- **PDF Count:** {pdf_count}\n")
    
    print(f"📝 Log saved to: {log_file}\n")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(generate_pdfs())
