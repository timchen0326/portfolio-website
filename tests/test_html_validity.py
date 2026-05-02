"""Tests for generated HTML correctness.

Requires `quarto render` to have been run first.
"""
import re
import pytest
from pathlib import Path


def get_html_files(docs_dir: Path):
    return list(docs_dir.glob("**/*.html"))


class TestHtmlContent:
    def test_html_files_exist(self, docs_dir):
        files = get_html_files(docs_dir)
        assert len(files) > 0, "No HTML files in docs/ — run quarto render"

    def test_each_page_has_title(self, docs_dir):
        for html_file in get_html_files(docs_dir):
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            assert "<title>" in content, f"{html_file.name}: missing <title>"

    def test_each_page_has_nav(self, docs_dir):
        for html_file in get_html_files(docs_dir):
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            assert "<nav" in content, f"{html_file.name}: missing <nav>"

    def test_each_page_has_closing_html_tag(self, docs_dir):
        for html_file in get_html_files(docs_dir):
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            assert "</html>" in content, f"{html_file.name}: unclosed <html>"

    def test_no_raw_template_placeholders(self, docs_dir):
        placeholder_pattern = re.compile(r"\{\{[^}]+\}\}")
        for html_file in get_html_files(docs_dir):
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            matches = placeholder_pattern.findall(content)
            assert not matches, f"{html_file.name}: unrendered template vars: {matches}"


class TestHtmlAssetRefs:
    def test_global_css_referenced(self, docs_dir):
        for html_file in get_html_files(docs_dir):
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            assert "styles.css" in content, f"{html_file.name}: missing styles.css ref"

    def test_coffee_page_has_coffee_css(self, docs_dir):
        coffee = docs_dir / "pages" / "coffee.html"
        if not coffee.exists():
            pytest.skip("pages/coffee.html not built yet")
        content = coffee.read_text(encoding="utf-8", errors="ignore")
        assert "coffee-style.css" in content
