"""Tests for link integrity in the generated site.

Requires `quarto render` to have been run first.
"""
import re
import pytest
from pathlib import Path


EXPECTED_EXTERNAL_LINKS = [
    "https://github.com/timchen0326",
    "https://www.linkedin.com/in/timchen0326/",
    "https://timsplayland.vercel.app/",
]

SKIP_LINK_PATTERNS = [
    re.compile(r"^mailto:"),
    re.compile(r"^#"),
    re.compile(r"^https?://"),
    re.compile(r"javascript:"),
]


def read_html(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_local_hrefs(html: str) -> list[str]:
    all_hrefs = re.findall(r'href="([^"]+)"', html)
    local = []
    for href in all_hrefs:
        if any(p.match(href) for p in SKIP_LINK_PATTERNS):
            continue
        # Strip query strings and fragments
        clean = href.split("?")[0].split("#")[0]
        if clean:
            local.append(clean)
    return local


class TestLocalLinks:
    def test_no_broken_local_hrefs(self, docs_dir):
        broken = []
        for html_file in docs_dir.glob("**/*.html"):
            html = read_html(html_file)
            for href in extract_local_hrefs(html):
                resolved = (html_file.parent / href).resolve()
                if not resolved.exists():
                    broken.append(f"{html_file.relative_to(docs_dir)} → {href}")
        assert not broken, "Broken local links:\n" + "\n".join(broken)

    def test_resume_pdf_accessible(self, docs_dir):
        pdf = docs_dir / "assets" / "pdfs" / "resume_2025.pdf"
        assert pdf.exists(), "Resume PDF not found in docs/assets/pdfs/"


class TestExternalLinksPresent:
    """Confirm expected external links appear somewhere in the built site.

    Does NOT make HTTP requests — only checks that hrefs are present in HTML.
    """

    def test_github_link_present(self, docs_dir):
        index = docs_dir / "index.html"
        if not index.exists():
            pytest.skip("index.html not built yet")
        assert "github.com/timchen0326" in read_html(index)

    def test_linkedin_link_present(self, docs_dir):
        index = docs_dir / "index.html"
        if not index.exists():
            pytest.skip("index.html not built yet")
        assert "linkedin.com/in/timchen0326" in read_html(index)

    def test_portfolio_link_present(self, docs_dir):
        index = docs_dir / "index.html"
        if not index.exists():
            pytest.skip("index.html not built yet")
        assert "timsplayland.vercel.app" in read_html(index)


class TestNavbarLinks:
    def test_all_project_pages_reachable_from_index(self, docs_dir):
        index = docs_dir / "index.html"
        if not index.exists():
            pytest.skip("index.html not built yet")
        html = read_html(index)
        expected_slugs = [
            "student-analysis",
            "ml-challenge",
            "toronto-crime-analysis",
            "us-presidential-election",
            "toronto-shelter-analysis",
            "bike-theft-analysis",
            "imdb-analysis",
            "mayohr-intern",
            "traffic-collision-analysis",
        ]
        for slug in expected_slugs:
            assert slug in html, f"Navbar missing link to: {slug}"
