# Tim Chen — Portfolio Website

Personal portfolio and data analysis showcase built with [Quarto](https://quarto.org/) and hosted at [weitingchen.com](https://weitingchen.com).

## Project Structure

```
portfolio-website/
├── index.qmd                   # Homepage (must stay at root)
├── _quarto.yml                 # Site config, navbar, theme
├── pages/
│   ├── courses.qmd             # University of Toronto coursework
│   └── coffee.qmd              # Coffee hobby page
├── projects/
│   ├── student-analysis.qmd    # Student habits & academic performance (Python/ML)
│   ├── ml-challenge.qmd        # ML challenge project
│   ├── toronto-crime-analysis.qmd
│   ├── toronto-shelter-analysis.qmd
│   ├── bike-theft-analysis.qmd
│   ├── imdb-analysis.qmd
│   ├── mayohr-intern.qmd       # MAYOHR internship report
│   ├── traffic-collision-analysis.qmd
│   └── us-presidential-election.qmd
├── assets/
│   ├── css/                    # Global and page-specific stylesheets
│   ├── data/                   # Raw datasets used in analyses
│   ├── images/                 # Photos and graphics
│   └── pdfs/                   # Resume and project report PDFs
├── tests/                      # pytest test suite (see Testing below)
└── docs/                       # Generated site output (GitHub Pages)
```

## Prerequisites

- [Quarto 1.7+](https://quarto.org/docs/get-started/)
- Python 3.10+ with `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`
- R (optional, for R-based analyses)

## Local Development

```bash
# Preview with live reload
quarto preview

# Full render to docs/
quarto render
```

## Testing

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

Tests cover:
- **Source organization** — no loose QMD files in root, all pages and projects present
- **Asset presence** — CSS, data, images, PDFs all in correct locations
- **Built site** — all 12 HTML pages rendered, search index and sitemap present
- **HTML validity** — titles, nav, closing tags, no unrendered template placeholders
- **Link integrity** — no broken local hrefs, external profile links present

> Run `quarto render` before running tests that check `docs/`.

## Deployment

The `docs/` folder is published via GitHub Pages. After rendering:

```bash
git add docs/
git commit -m "chore: rebuild site"
git push
```

## Stack

| Tool | Purpose |
|------|---------|
| Quarto | Static site generation |
| Bootstrap (cosmo) | Theme |
| Python | Data analysis (pandas, sklearn, matplotlib) |
| GitHub Pages | Hosting via `docs/` output |
