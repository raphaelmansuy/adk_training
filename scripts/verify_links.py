#!/usr/bin/env python3
"""
Docusaurus Link Verification Script

This script verifies all links in a Docusaurus-built website by:
1. Scanning HTML files in the build directory
2. Extracting all links (internal and external)
3. Validating each link with appropriate checks
4. Generating a comprehensive report

Usage:
    python scripts/verify_links.py [OPTIONS]

Examples:
    # Basic verification
    python scripts/verify_links.py

    # Skip external link checking
    python scripts/verify_links.py --skip-external

    # Check only external links with custom timeout
    python scripts/verify_links.py --only-external --timeout 10

    # Export results to JSON
    python scripts/verify_links.py --json-output links_report.json

    # Verbose output with detailed logging
    python scripts/verify_links.py --verbose

Author: Development Team
Version: 1.0.0
"""

import argparse
import json
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple, Set

try:
    from bs4 import BeautifulSoup
    import requests
    from colorama import Fore, Style, init
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Please install requirements: pip install -r scripts/requirements-links.txt")
    sys.exit(1)

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class LinkVerifier:
    """Main class for verifying links in Docusaurus websites."""

    # Links that should be skipped
    SKIP_PROTOCOLS = {'mailto:', 'javascript:', 'data:', 'tel:', 'sms:', 'ftp://'}

    def __init__(
        self,
        build_dir: Path,
        timeout: int = 5,
        max_workers: int = 10,
        skip_external: bool = False,
        only_external: bool = False,
        verbose: bool = False
    ):
        """
        Initialize the LinkVerifier.

        Args:
            build_dir: Path to the Docusaurus build directory
            timeout: Timeout for HTTP requests in seconds
            max_workers: Maximum number of concurrent threads for external link checking
            skip_external: Skip checking external links
            only_external: Only check external links
            verbose: Enable verbose logging
        """
        self.build_dir = Path(build_dir)
        self.timeout = timeout
        self.max_workers = max_workers
        self.skip_external = skip_external
        self.only_external = only_external

        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        # Statistics
        self.stats = {
            'total_files': 0,
            'total_links': 0,
            'internal_links': 0,
            'external_links': 0,
            'skipped_links': 0,
            'working_links': 0,
            'broken_links': 0,
        }

        # Track broken links with details
        self.broken_links: List[Dict] = []
        self.working_external_links: Set[str] = set()
        self.broken_external_links: Dict[str, int] = {}

    def should_skip_link(self, href: str) -> bool:
        """
        Determine if a link should be skipped.

        Args:
            href: The href value to check

        Returns:
            True if the link should be skipped, False otherwise
        """
        href_lower = href.lower().strip()

        # Skip empty links and anchors
        if not href_lower or href_lower == '#':
            return True

        # Skip special protocols
        for protocol in self.SKIP_PROTOCOLS:
            if href_lower.startswith(protocol):
                return True

        return False

    def is_external_link(self, href: str) -> bool:
        """
        Determine if a link is external.

        Args:
            href: The href value to check

        Returns:
            True if the link is external, False otherwise
        """
        href_lower = href.lower().strip()

        # External links start with http/https or //
        return href_lower.startswith(('http://', 'https://', '//'))

    def extract_links_from_file(self, html_file: Path) -> List[Tuple[str, str]]:
        """
        Extract all links from an HTML file.

        Args:
            html_file: Path to the HTML file

        Returns:
            List of tuples (href, source_file)
        """
        links = []

        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Extract all anchor tags
            for tag in soup.find_all('a', href=True):
                href = tag['href'].strip()
                if href:
                    links.append((href, str(html_file)))

        except Exception as e:
            logger.warning(f"Error reading {html_file}: {e}")

        return links

    def verify_internal_link(self, href: str, source_file: Path) -> Tuple[bool, str]:
        """
        Verify that an internal link points to an existing file.

        Args:
            href: The href to verify
            source_file: The source HTML file

        Returns:
            Tuple of (is_working, message)
        """
        try:
            # Extract the path part (remove anchor)
            path_part = href.split('#')[0]

            if not path_part:
                return True, "Anchor-only link"

            # Resolve the target path
            if path_part.startswith('/'):
                # Absolute path from build root
                target = self.build_dir / path_part.lstrip('/')
            else:
                # Relative path
                source_dir = Path(source_file).parent
                target = (source_dir / path_part).resolve()

            # Check if file exists
            if target.exists() and target.is_file():
                return True, "File exists"

            # Check if it's a directory with index.html
            if target.is_dir() and (target / 'index.html').exists():
                return True, "Directory with index.html"

            return False, f"File not found: {target}"

        except Exception as e:
            return False, f"Error resolving link: {e}"

    def verify_external_link(self, url: str) -> Tuple[bool, int, str]:
        """
        Verify that an external link is accessible.

        Args:
            url: The external URL to verify

        Returns:
            Tuple of (is_working, status_code, message)
        """
        try:
            # Add scheme if missing
            if url.startswith('//'):
                url = 'https:' + url

            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; DocusaurusLinkVerifier/1.0)'
            }

            response = requests.head(
                url,
                timeout=self.timeout,
                headers=headers,
                allow_redirects=True,
                verify=True
            )

            # Consider 2xx and 3xx status codes as working
            is_working = response.status_code < 400
            return is_working, response.status_code, f"HTTP {response.status_code}"

        except requests.exceptions.Timeout:
            return False, 0, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, 0, "Connection error"
        except requests.exceptions.RequestException as e:
            return False, 0, f"Request error: {str(e)[:50]}"
        except Exception as e:
            return False, 0, f"Unexpected error: {str(e)[:50]}"

    def scan_html_files(self) -> List[Path]:
        """
        Scan the build directory for HTML files.

        Returns:
            List of HTML file paths
        """
        if not self.build_dir.exists():
            logger.error(f"Build directory not found: {self.build_dir}")
            return []

        html_files = list(self.build_dir.rglob('*.html'))
        logger.info(f"Found {len(html_files)} HTML files")
        return html_files

    def process_links(self) -> None:
        """Process all links found in HTML files."""
        logger.info("Starting link verification...")

        # Scan for HTML files
        html_files = self.scan_html_files()
        self.stats['total_files'] = len(html_files)

        if not html_files:
            logger.warning("No HTML files found in build directory")
            return

        # Extract all links
        all_links: List[Tuple[str, str]] = []
        for html_file in html_files:
            links = self.extract_links_from_file(html_file)
            all_links.extend(links)

        self.stats['total_links'] = len(all_links)

        # Process links
        external_links_to_check = []

        for href, source_file in all_links:
            if self.should_skip_link(href):
                self.stats['skipped_links'] += 1
                continue

            is_external = self.is_external_link(href)

            if is_external:
                self.stats['external_links'] += 1
                if not self.skip_external:
                    external_links_to_check.append((href, source_file))
            else:
                self.stats['internal_links'] += 1
                if not self.only_external:
                    self._verify_internal_link(href, source_file)

        # Verify external links concurrently
        if external_links_to_check:
            logger.info(f"Verifying {len(external_links_to_check)} external links...")
            self._verify_external_links_concurrent(external_links_to_check)

    def _verify_internal_link(self, href: str, source_file: str) -> None:
        """Verify a single internal link."""
        is_working, message = self.verify_internal_link(href, Path(source_file))

        if is_working:
            self.stats['working_links'] += 1
            logger.debug(f"✓ {href}")
        else:
            self.stats['broken_links'] += 1
            logger.warning(f"✗ {href} - {message}")
            self.broken_links.append({
                'url': href,
                'type': 'internal',
                'source': source_file,
                'error': message
            })

    def _verify_external_links_concurrent(self, external_links: List[Tuple[str, str]]) -> None:
        """Verify external links concurrently."""
        unique_urls = set(url for url, _ in external_links)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.verify_external_link, url): url
                for url in unique_urls
            }

            for future in as_completed(futures):
                url = futures[future]
                try:
                    is_working, status_code, message = future.result()

                    if is_working:
                        self.stats['working_links'] += 1
                        self.working_external_links.add(url)
                        logger.debug(f"✓ {url} - {message}")
                    else:
                        self.stats['broken_links'] += 1
                        self.broken_external_links[url] = status_code
                        logger.warning(f"✗ {url} - {message}")
                        # Find source files for this URL
                        sources = [src for src_url, src in external_links if src_url == url]
                        self.broken_links.append({
                            'url': url,
                            'type': 'external',
                            'status_code': status_code,
                            'error': message,
                            'sources': sources[:3]  # Limit to 3 sources
                        })

                except Exception as e:
                    logger.error(f"Error verifying {url}: {e}")
                    self.stats['broken_links'] += 1

    def generate_report(self) -> str:
        """
        Generate a human-readable report of the verification results.

        Returns:
            Formatted report string
        """
        report = []
        report.append("\n" + "=" * 80)
        report.append("DOCUSAURUS LINK VERIFICATION REPORT")
        report.append("=" * 80)

        # Statistics section
        report.append("\n📊 STATISTICS:")
        report.append(f"  Total HTML files scanned: {self.stats['total_files']}")
        report.append(f"  Total links found: {self.stats['total_links']}")
        report.append(f"  Internal links: {self.stats['internal_links']}")
        report.append(f"  External links: {self.stats['external_links']}")
        report.append(f"  Skipped links: {self.stats['skipped_links']}")
        report.append(f"  Working links: {Fore.GREEN}{self.stats['working_links']}{Style.RESET_ALL}")
        report.append(f"  Broken links: {Fore.RED}{self.stats['broken_links']}{Style.RESET_ALL}")

        # Broken links section
        if self.broken_links:
            report.append(f"\n❌ BROKEN LINKS ({len(self.broken_links)}):")
            report.append("-" * 80)

            for idx, link_info in enumerate(self.broken_links, 1):
                report.append(f"\n  {idx}. {Fore.RED}{link_info['url']}{Style.RESET_ALL}")
                report.append(f"     Type: {link_info['type']}")
                report.append(f"     Error: {link_info['error']}")

                if link_info['type'] == 'external' and 'status_code' in link_info:
                    report.append(f"     Status Code: {link_info['status_code']}")

                if 'source' in link_info:
                    report.append(f"     Source: {link_info['source']}")
                elif 'sources' in link_info:
                    for source in link_info['sources']:
                        report.append(f"     Source: {source}")

        else:
            report.append(f"\n{Fore.GREEN}✓ All links are working!{Style.RESET_ALL}")

        # Summary section
        report.append("\n" + "=" * 80)
        success_rate = (
            (self.stats['working_links'] / self.stats['total_links'] * 100)
            if self.stats['total_links'] > 0
            else 100
        )
        report.append(f"Success Rate: {Fore.GREEN if success_rate == 100 else Fore.YELLOW}{success_rate:.1f}%{Style.RESET_ALL}")
        report.append("=" * 80 + "\n")

        return "\n".join(report)

    def export_json(self, filepath: Path) -> None:
        """
        Export verification results to JSON file.

        Args:
            filepath: Path where to save the JSON report
        """
        report_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'statistics': self.stats,
            'broken_links': self.broken_links,
            'working_external_links': list(self.working_external_links),
            'broken_external_links': self.broken_external_links,
        }

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2)
            logger.info(f"JSON report exported to: {filepath}")
        except Exception as e:
            logger.error(f"Error exporting JSON report: {e}")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Verify all links in a Docusaurus website',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic verification
  python scripts/verify_links.py

  # Skip external link checking
  python scripts/verify_links.py --skip-external

  # Check only external links with custom timeout
  python scripts/verify_links.py --only-external --timeout 10

  # Export results to JSON
  python scripts/verify_links.py --json-output links_report.json

  # Verbose output with detailed logging
  python scripts/verify_links.py --verbose
        """
    )

    parser.add_argument(
        '--build-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'docs' / 'build',
        help='Path to Docusaurus build directory (default: docs/build)'
    )

    parser.add_argument(
        '--skip-external',
        action='store_true',
        help='Skip verification of external links'
    )

    parser.add_argument(
        '--only-external',
        action='store_true',
        help='Only verify external links'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=5,
        help='Timeout for HTTP requests in seconds (default: 5)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=10,
        help='Maximum number of concurrent threads (default: 10)'
    )

    parser.add_argument(
        '--json-output',
        type=Path,
        help='Export results to JSON file'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Validate build directory
    if not args.build_dir.exists():
        logger.error(f"Build directory not found: {args.build_dir}")
        logger.info("Please build the Docusaurus site first: cd docs && npm run build")
        return 1

    # Create verifier and run verification
    verifier = LinkVerifier(
        build_dir=args.build_dir,
        timeout=args.timeout,
        max_workers=args.workers,
        skip_external=args.skip_external,
        only_external=args.only_external,
        verbose=args.verbose
    )

    try:
        start_time = time.time()
        verifier.process_links()
        elapsed_time = time.time() - start_time

        # Print report
        report = verifier.generate_report()
        print(report)

        # Add timing info
        logger.info(f"Verification completed in {elapsed_time:.2f} seconds")

        # Export JSON if requested
        if args.json_output:
            verifier.export_json(args.json_output)

        # Return appropriate exit code
        if verifier.stats['broken_links'] > 0:
            return 1
        return 0

    except KeyboardInterrupt:
        logger.warning("Verification interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error during verification: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
