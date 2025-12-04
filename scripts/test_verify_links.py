import os
from pathlib import Path

import pytest

from verify_links import LinkVerifier


def write_file(p: Path, contents: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contents, encoding='utf-8')


def test_anchor_only_same_file(tmp_path):
    # create page with an anchor and a link to the anchor
    page = tmp_path / 'page.html'
    write_file(page, '<html><body><h1 id="section-1">Section</h1><a href="#section-1">go</a></body></html>')

    verifier = LinkVerifier(build_dir=tmp_path, skip_external=True)
    verifier.process_links()

    # the link should be resolved inside the same file
    assert verifier.stats['broken_links'] == 0


def test_relative_file_resolution(tmp_path):
    # create files: index.html linking to page2 (without .html) and page2.html exists
    index = tmp_path / 'index.html'
    page2 = tmp_path / 'page2.html'

    write_file(page2, '<html><body><h1>Page 2</h1></body></html>')
    write_file(index, '<html><body><a href="page2">to page2</a></body></html>')

    verifier = LinkVerifier(build_dir=tmp_path, skip_external=True)
    verifier.process_links()
    assert verifier.stats['broken_links'] == 0


def test_directory_index_resolution(tmp_path):
    # create dir/index.html and a linking file referencing /dir/
    dir_index = tmp_path / 'dir' / 'index.html'
    write_file(dir_index, '<html><body><h1>Dir Index</h1></body></html>')

    linking = tmp_path / 'page.html'
    write_file(linking, '<html><body><a href="/dir/">dir</a></body></html>')

    verifier = LinkVerifier(build_dir=tmp_path, skip_external=True)
    verifier.process_links()
    assert verifier.stats['broken_links'] == 0


def test_external_head_fallback(monkeypatch):
    # fake session object
    class FakeResp:
        def __init__(self, code):
            self.status_code = code

    class FakeSession:
        def __init__(self):
            self._called = []

        def head(self, url, **kwargs):
            # return 405 for head
            return FakeResp(405)

        def get(self, url, **kwargs):
            return FakeResp(200)

    monkeypatch.setattr('verify_links.requests.Session', lambda: FakeSession())

    verifier = LinkVerifier(build_dir=Path('.'), skip_external=False, only_external=True, retries=1)
    ok, status, msg = verifier.verify_external_link('https://example.invalid')
    assert ok is True
    assert status == 200


def test_dropdown_trigger_skipped(tmp_path):
    """Test that navbar dropdown triggers (href='#' with aria-haspopup) are skipped."""
    page = tmp_path / 'page.html'
    # Include a dropdown trigger and a regular broken anchor link
    write_file(page, '''
    <html><body>
        <a href="#" aria-haspopup="true" role="button">Dropdown Menu</a>
        <a href="#nonexistent">Broken anchor</a>
    </body></html>
    ''')

    verifier = LinkVerifier(build_dir=tmp_path, skip_external=True)
    verifier.process_links()

    # The dropdown trigger should be skipped (not counted as broken)
    # The #nonexistent anchor should be counted as broken
    assert verifier.stats['skipped_links'] == 1
    assert verifier.stats['broken_links'] == 1


def test_url_encoded_anchor_resolution(tmp_path):
    """Test that URL-encoded anchors (e.g., emoji) are properly resolved."""
    page = tmp_path / 'page.html'
    # Create a page with an emoji ID and a URL-encoded link to it
    # %EF%B8%8F is the variation selector emoji
    write_file(page, '''
    <html><body>
        <h2 id="️-section">Section with emoji</h2>
        <a href="#%EF%B8%8F-section">Link to emoji section</a>
    </body></html>
    ''')

    verifier = LinkVerifier(build_dir=tmp_path, skip_external=True)
    verifier.process_links()

    # The URL-encoded anchor should resolve to the emoji ID
    assert verifier.stats['broken_links'] == 0
