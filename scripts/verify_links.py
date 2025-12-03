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
from typing import Dict, List, Tuple, Set, Optional
import re
from urllib.parse import urlparse

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
        verbose: bool = False,
        retries: int = 2,
        backoff: float = 0.5,
        verify_anchors: bool = True,
        log_file: Optional[Path] = None,
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

        # HTTP retry/backoff settings
        self.retries = max(1, int(retries))
        self.backoff = float(backoff)

        # anchor verification
        self.verify_anchors = bool(verify_anchors)

        # optional log file to record details
        self.log_file = Path(log_file) if log_file else None

        # cache results for external URL checks to avoid duplicate requests
        self._external_cache: Dict[str, Tuple[bool, int, str]] = {}

    def should_skip_link(self, href: str) -> bool:
        """
        Determine if a link should be skipped.

        Args:
            href: The href value to check

        Returns:
            True if the link should be skipped, False otherwise
        """
        href_lower = href.lower().strip()

        # Skip empty links
        if not href_lower:
            return True
        # If the link is the simple '#' (anchor-only): only skip if anchor verification is disabled
        if href_lower == '#':
            return not self.verify_anchors

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

    def _normalize_anchor(self, anchor: str) -> str:
        """Normalize anchor/id text: many headings are transformed by Docusaurus (lower, hyphen)

        We do a best-effort normalization to match generated ids.
        """
        return re.sub(r"[^a-z0-9\-]", "", anchor.strip().lower().replace(' ', '-'))

    def _is_dropdown_trigger(self, tag) -> bool:
        """
        Check if an anchor tag is a dropdown trigger (non-navigating link).
        
        Docusaurus navbar dropdowns use href="#" with aria-haspopup="true" or
        role="button" to indicate a non-navigating dropdown trigger.
        
        Args:
            tag: BeautifulSoup tag element
            
        Returns:
            True if this is a dropdown trigger, False otherwise
        """
        href = tag.get('href', '').strip()
        if href != '#':
            return False
        
        # Check for dropdown/button attributes
        aria_haspopup = tag.get('aria-haspopup', '').lower()
        role = tag.get('role', '').lower()
        
        if aria_haspopup in ('true', 'menu', 'listbox'):
            return True
        if role == 'button':
            return True
            
        return False

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

            # Extract all anchor tags (include anchors and hrefs)
            for tag in soup.find_all('a', href=True):
                href = tag['href'].strip()
                if href is not None:
                    # Skip dropdown trigger links (href="#" with aria-haspopup or role="button")
                    if self._is_dropdown_trigger(tag):
                        self.stats['skipped_links'] = self.stats.get('skipped_links', 0) + 1
                        continue
                    links.append((href, str(html_file)))

        except Exception as e:
            logger.warning(f"Error reading {html_file}: {e}")

        return links

    def _candidate_targets_for_href(self, href: str, source_file: Path) -> List[Path]:
        """Return candidate filesystem targets for a given href / source_file.

        This tries the raw path, appending .html, index.html in dir, and common site mapping patterns.
        """
        candidates: List[Path] = []

        path_part = href.split('#')[0]

        # empty path part means anchor-only link
        if not path_part:
            return candidates

        # Normalize base path removals (site-specific)
        if path_part.startswith('/adk_training/'):
            path_part = '/' + path_part[len('/adk_training/') :]
        elif path_part.startswith('adk_training/'):
            path_part = path_part[len('adk_training/') :]

        # Absolute from build root
        if path_part.startswith('/'):
            candidates.append(self.build_dir / path_part.lstrip('/'))
        else:
            source_dir = Path(source_file).parent
            candidates.append((source_dir / path_part).resolve())

        # variations
        # add .html
        for base in list(candidates):
            candidates.append(base.with_suffix('.html'))
            if base.is_dir():
                candidates.append(base / 'index.html')

        # map /docs/<slug> -> /docs/<slug>/index.html
        if path_part.startswith('/docs/'):
            base = self.build_dir / path_part.lstrip('/')
            candidates.append(base.with_suffix('.html'))
            candidates.append(base / 'index.html')

        # deduplicate while preserving order
        seen = set()
        uniq = []
        for p in candidates:
            try:
                p = p.resolve()
            except Exception:
                p = Path(p)
            if str(p) not in seen:
                seen.add(str(p))
                uniq.append(p)

        return uniq

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
            anchor = ''
            if '#' in href:
                parts = href.split('#', 1)
                path_part = parts[0]
                anchor = parts[1]
            else:
                path_part = href

            # anchor-only links -> verify the anchor exists in the same source file
            if path_part.strip() == '':
                # Use the source_file itself to find anchor
                if not anchor:
                    return False, 'Empty anchor and no path'
                ok, msg = self.verify_anchor_in_file(source_file, anchor)
                return ok, msg

            # build a list of candidate target files
            candidates = self._candidate_targets_for_href(href, source_file)

            for target in candidates:
                # check file exists
                if target.exists() and target.is_file():
                    # if anchor present, check anchor exists in file
                    if anchor:
                        ok, msg = self.verify_anchor_in_file(target, anchor)
                        if ok:
                            return True, f'File exists + anchor found in {target.name}'
                        else:
                            # anchor missing in this target; keep checking other candidates
                            continue
                    return True, f'File exists: {target}'

            # if none of the candidates matched, return helpful message
            tried = ', '.join([str(c) for c in candidates[:6]])
            return False, f'File not found. Tried: {tried}'

        except Exception as e:
            return False, f'Error resolving link: {e}'

    def suggest_fix_for_link(self, href: str) -> Optional[str]:
        """
        Suggest a fix for a broken link based on common patterns.

        Args:
            href: The broken href

        Returns:
            Suggested fix or None if no suggestion available
        """
        import re

        # Pattern 1: Links with filename format (e.g., /01_hello_world_agent)
        # These should be /docs/{id_without_numbers}
        match = re.match(r'^/(\d+_)([a-z_]+)$', href)
        if match:
            suggested = f"/docs/{match.group(2)}"
            return suggested

        # Pattern 2: Links with /adk_training/ prefix but missing /docs/
        # e.g., /adk_training/01_hello_world_agent -> /adk_training/docs/hello_world_agent
        if '/adk_training/' in href:
            match = re.match(r'^/adk_training/(\d+_)?([a-z_]+)$', href)
            if match:
                doc_id = match.group(2)
                suggested = f"/adk_training/docs/{doc_id}"
                return suggested

        return None

    def verify_anchor_in_file(self, file_path: Path, anchor: str) -> Tuple[bool, str]:
        """Verify anchor/id exists inside the given HTML file.

        Will try id attribute and name anchors, plus best-effort normalized heading ids.
        Also handles URL-encoded anchors (e.g., %EF%B8%8F for emoji).
        """
        try:
            from urllib.parse import unquote
            
            if not file_path.exists():
                return False, f'File not found for anchor check: {file_path}'

            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Try both the original anchor and URL-decoded version
            anchors_to_try = [anchor]
            decoded_anchor = unquote(anchor)
            if decoded_anchor != anchor:
                anchors_to_try.append(decoded_anchor)

            for anch in anchors_to_try:
                # direct id match
                if soup.find(id=anch):
                    return True, 'Anchor id found'

                # old-style name anchors
                if soup.find('a', attrs={'name': anch}):
                    return True, 'Named anchor found'

                # check normalized anchor (headings often transform into lowercase-hyphen form)
                norm = self._normalize_anchor(anch)
                if soup.find(id=norm):
                    return True, 'Normalized anchor id found'

            # try to match by heading text -> generate slug id heuristically
            norm = self._normalize_anchor(anchor)
            headings = soup.find_all(re.compile('^h[1-6]$'))
            for h in headings:
                text = ' '.join(h.stripped_strings)
                if not text:
                    continue
                if self._normalize_anchor(text) == norm:
                    return True, 'Heading slug matches anchor'

            return False, 'Anchor not found in file'

        except Exception as e:
            return False, f'Error verifying anchor: {e}'

    def verify_external_link(self, url: str) -> Tuple[bool, int, str]:
        """
        Verify that an external link is accessible.

        Args:
            url: The external URL to verify

        Returns:
            Tuple of (is_working, status_code, message)
        """
        # Provide a more robust external link check: try HEAD first, on some servers
        # HEAD is refused or returns 405 -> fallback to GET. Also support retries.
        try:
            if url.startswith('//'):
                url = 'https:' + url

            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; DocusaurusLinkVerifier/1.0)'
            }

            session = requests.Session()

            # retry loop (simple fixed attempts)
            attempts = max(1, getattr(self, 'retries', 1))
            backoff = getattr(self, 'backoff', 0.5)
            last_status = 0
            last_message = ''

            for attempt in range(1, attempts + 1):
                try:
                    response = session.head(
                        url,
                        timeout=self.timeout,
                        headers=headers,
                        allow_redirects=True,
                        verify=True,
                    )

                    last_status = response.status_code

                    # Many servers reject HEAD requests with 405; try GET in that case
                    if response.status_code == 405 or response.status_code >= 400:
                        # fallback to GET to validate the link
                        response = session.get(
                            url,
                            timeout=self.timeout,
                            headers=headers,
                            allow_redirects=True,
                            stream=True,
                            verify=True,
                        )
                        last_status = response.status_code

                    is_working = last_status < 400
                    last_message = f'HTTP {last_status}'
                    return is_working, last_status, last_message

                except requests.exceptions.Timeout:
                    last_message = 'Timeout'
                except requests.exceptions.ConnectionError:
                    last_message = 'Connection error'
                except requests.exceptions.RequestException as e:
                    last_message = f'Request error: {str(e)[:120]}'

                # If not last attempt, wait a bit
                if attempt < attempts:
                    time.sleep(backoff * attempt)

            # exhausted retries
            return False, last_status or 0, last_message or 'Unknown error'

        except Exception as e:
            return False, 0, f'Unexpected error: {str(e)[:120]}'

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

            # Determine if link is external. However, some absolute URLs
            # point to the same published site (for example
            # https://raphaelmansuy.github.io/adk_training/docs/01_hello_world_agent)
            # which should be verified against the local build. Detect and
            # treat those as internal links.
            is_external = self.is_external_link(href)
            treated_as_internal = False

            if is_external:
                try:
                    parsed = urlparse(href)
                    # If the URL points to a github.io site for this repo and
                    # its path starts with /adk_training, treat as internal
                    if parsed.netloc.endswith('github.io') and parsed.path.startswith('/adk_training'):
                        # Use the path part as an internal href
                        href_path = parsed.path
                        treated_as_internal = True
                        self.stats['internal_links'] += 1
                        if not self.only_external:
                            self._verify_internal_link(href_path, source_file)
                    else:
                        # Real external URL
                        self.stats['external_links'] += 1
                        if not self.skip_external:
                            external_links_to_check.append((href, source_file))
                except Exception:
                    # Fallback to treating as external
                    self.stats['external_links'] += 1
                    if not self.skip_external:
                        external_links_to_check.append((href, source_file))

            if (not is_external) and (not treated_as_internal):
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
            link_info = {
                'url': href,
                'type': 'internal',
                'source': source_file,
                'error': message
            }
            # Add suggestion if available
            suggestion = self.suggest_fix_for_link(href)
            if suggestion:
                link_info['suggestion'] = suggestion
            self.broken_links.append(link_info)

    def _verify_external_links_concurrent(self, external_links: List[Tuple[str, str]]) -> None:
        """Verify external links concurrently."""
        unique_urls = set(url for url, _ in external_links)

        # Prepare URLs to actually check (skip ones in cache)
        urls_to_check = [u for u in unique_urls if u not in self._external_cache]

        # Add cached results first
        for url in unique_urls:
            if url in self._external_cache:
                is_working, status_code, message = self._external_cache[url]
                if is_working:
                    self.stats['working_links'] += 1
                    self.working_external_links.add(url)
                    logger.debug(f"✓ {url} - {message} (cached)")
                else:
                    self.stats['broken_links'] += 1
                    self.broken_external_links[url] = status_code
                    logger.warning(f"✗ {url} - {message} (cached)")

        if not urls_to_check:
            return

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.verify_external_link, url): url
                for url in urls_to_check
            }

            for future in as_completed(futures):
                url = futures[future]
                try:
                    is_working, status_code, message = future.result()

                    # cache result
                    self._external_cache[url] = (is_working, status_code, message)

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

                if 'suggestion' in link_info:
                    report.append(f"     💡 Suggestion: {Fore.YELLOW}{link_info['suggestion']}{Style.RESET_ALL}")

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

    def export_csv(self, filepath: Path) -> None:
        """Export broken links to a CSV file (simple table)"""
        try:
            import csv

            cols = ['url', 'type', 'error', 'status_code', 'source', 'suggestion']
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=cols)
                writer.writeheader()
                for b in self.broken_links:
                    row = {
                        'url': b.get('url'),
                        'type': b.get('type'),
                        'error': b.get('error'),
                        'status_code': b.get('status_code', ''),
                        'source': b.get('source') or ','.join(b.get('sources', [])),
                        'suggestion': b.get('suggestion', ''),
                    }
                    writer.writerow(row)

            logger.info(f"CSV report exported to: {filepath}")
        except Exception as e:
            logger.error(f"Error writing CSV: {e}")


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
        '--retries',
        type=int,
        default=2,
        help='Number of retry attempts for external links (default: 2)'
    )

    parser.add_argument(
        '--backoff',
        type=float,
        default=0.5,
        help='Backoff multiplier between retries (seconds, default: 0.5)'
    )

    parser.add_argument(
        '--no-verify-anchors',
        action='store_true',
        help='Do not verify anchor/id fragments (#anchor) inside pages'
    )

    parser.add_argument(
        '--log-file',
        type=Path,
        help='Optional path to write a detailed log file (JSON)'
    )

    parser.add_argument(
        '--json-output',
        type=Path,
        help='Export results to JSON file'
    )

    parser.add_argument(
        '--export-csv',
        type=Path,
        help='Export broken links to CSV file (path)'
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
        verbose=args.verbose,
        retries=args.retries,
        backoff=args.backoff,
        verify_anchors=(not args.no_verify_anchors),
        log_file=args.log_file,
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

        # Export JSON if requested (explicit json-output)
        if args.json_output:
            verifier.export_json(args.json_output)

        # Optional log file - write full JSON if requested (alias)
        if args.log_file:
            verifier.export_json(args.log_file)

        # Export CSV of broken links if requested
        if args.export_csv:
            try:
                verifier.export_csv(args.export_csv)
            except Exception as e:
                logger.error(f"Error writing CSV: {e}")

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
