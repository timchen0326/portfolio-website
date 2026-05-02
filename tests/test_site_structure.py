"""Tests for source file organization and asset presence.

Run `quarto render` before running tests that check docs/.
"""
import pytest
from pathlib import Path

EXPECTED_SOURCE_PAGES = [
    "pages/courses.qmd",
    "pages/coffee.qmd",
]

EXPECTED_SOURCE_PROJECTS = [
    "projects/student-analysis.qmd",
    "projects/ml-challenge.qmd",
    "projects/toronto-crime-analysis.qmd",
    "projects/us-presidential-election.qmd",
    "projects/toronto-shelter-analysis.qmd",
    "projects/bike-theft-analysis.qmd",
    "projects/imdb-analysis.qmd",
    "projects/mayohr-intern.qmd",
    "projects/traffic-collision-analysis.qmd",
]

EXPECTED_ASSETS = [
    "assets/css/styles.css",
    "assets/css/coffee-style.css",
    "assets/data/enhanced_student_habits_performance_dataset.csv",
    "assets/images/Canon-0806.JPG",
    "assets/pdfs/resume_2025.pdf",
    "assets/pdfs/Bike Theft Analysis.pdf",
    "assets/pdfs/IMDb Analysis.pdf",
]

EXPECTED_BUILT_PAGES = [
    "index.html",
    "pages/courses.html",
    "pages/coffee.html",
    "projects/student-analysis.html",
    "projects/ml-challenge.html",
    "projects/toronto-crime-analysis.html",
    "projects/us-presidential-election.html",
    "projects/toronto-shelter-analysis.html",
    "projects/bike-theft-analysis.html",
    "projects/imdb-analysis.html",
    "projects/mayohr-intern.html",
    "projects/traffic-collision-analysis.html",
]


class TestSourceOrganization:
    def test_index_at_root(self, project_dir):
        assert (project_dir / "index.qmd").exists()

    def test_no_loose_qmds_in_root(self, project_dir):
        allowed_root = {"index.qmd", "projects.qmd"}
        loose = [f.name for f in project_dir.glob("*.qmd") if f.name not in allowed_root]
        assert loose == [], f"Unexpected QMD files in root: {loose}"

    def test_pages_exist(self, project_dir):
        for path in EXPECTED_SOURCE_PAGES:
            assert (project_dir / path).exists(), f"Missing: {path}"

    def test_projects_exist(self, project_dir):
        for path in EXPECTED_SOURCE_PROJECTS:
            assert (project_dir / path).exists(), f"Missing: {path}"

    def test_quarto_config_exists(self, project_dir):
        assert (project_dir / "_quarto.yml").exists()


class TestAssets:
    def test_all_assets_present(self, project_dir):
        for asset in EXPECTED_ASSETS:
            assert (project_dir / asset).exists(), f"Missing asset: {asset}"

    def test_no_css_in_root(self, project_dir):
        root_css = list(project_dir.glob("*.css"))
        assert root_css == [], f"CSS files should be in assets/css/, found in root: {root_css}"

    def test_no_csvs_in_root(self, project_dir):
        root_csv = list(project_dir.glob("*.csv"))
        assert root_csv == [], f"CSV files should be in assets/data/, found in root: {root_csv}"

    def test_data_file_readable(self, project_dir):
        data = project_dir / "assets" / "data" / "enhanced_student_habits_performance_dataset.csv"
        assert data.stat().st_size > 0, "Data CSV is empty"


class TestBuiltSite:
    """Require `quarto render` before running this class."""

    def test_built_pages_exist(self, docs_dir):
        for page in EXPECTED_BUILT_PAGES:
            assert (docs_dir / page).exists(), f"Built page missing (run quarto render): {page}"

    def test_docs_has_search_json(self, docs_dir):
        assert (docs_dir / "search.json").exists()

    def test_docs_has_sitemap(self, docs_dir):
        assert (docs_dir / "sitemap.xml").exists()
