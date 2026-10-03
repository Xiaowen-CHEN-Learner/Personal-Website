# Xavier Chen — Finance Research & Analytics

A project-focused portfolio connecting my financial-analysis background with research notebooks, working Python examples, and financial-education tools.

[![Portfolio checks](https://github.com/Xiaowen-CHEN-Learner/Personal-Website/actions/workflows/portfolio-checks.yml/badge.svg)](https://github.com/Xiaowen-CHEN-Learner/Personal-Website/actions/workflows/portfolio-checks.yml)

**[Portfolio website](https://xiaowen-chen-learner.github.io/Personal-Website/)** · **[LinkedIn](https://www.linkedin.com/in/xiaowen-chen/)** · **[GitHub](https://github.com/Xiaowen-CHEN-Learner)**

## What is here

The homepage introduces my finance and research background and links to six selected projects: equity research, quantamental investing, fixed income, finance games, AI research workflows, and a precious-metals academic portfolio. It distinguishes research, prototypes, and runnable examples.

`library.html` preserves the previous research-library homepage byte-for-byte, including its existing article index. Archived statements and figures retain their original dates and were not revalidated in this update. The earlier `Personal website/` version is also retained.

## Tech stack

Semantic HTML and a local CSS file. The new homepage needs no JavaScript, external fonts, analytics, build step, or backend. The legacy writing archive has its original JavaScript and external resources.

## Installation and usage

```bash
git clone https://github.com/Xiaowen-CHEN-Learner/Personal-Website.git
cd Personal-Website
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/`. Use the selected-work cards to open project repositories, or choose Writing archive for the earlier article index. The GitHub Pages project path and repository name have not changed.

## Tests and visual evidence

```bash
python -m unittest discover -s tests -v
python -m pip install playwright==1.57.0
python -m playwright install chromium
python tools/check_browser.py
```

The browser script tests the homepage at 320, 390, 768, and 1440 pixels, checks keyboard navigation and horizontal overflow, and captures full-page screenshots. It also checks that project cards and contact information remain visible without JavaScript.

Open **Actions → Portfolio checks → a completed run → portfolio-browser-evidence** for its screenshots and JSON report. Artifacts are retained for 30 days. The badge reflects actual workflow status, not a static claim of success.

[Validation scope and local results](docs/PORTFOLIO_VALIDATION.md). Tests do not establish full accessibility compliance, correctness of investment research, or the availability of external destinations.

## Repository structure

```text
index.html                     Project-focused homepage
assets/portfolio.css           Responsive styles and print/reduced-motion rules
library.html                   Preserved earlier writing archive
Personal website/              Earlier HTML iteration
tests/test_homepage.py         Homepage structural checks
tools/check_browser.py         Chromium checks and screenshot generation
docs/PORTFOLIO_VALIDATION.md    Scope, results, and limitations
```

## Profile setup and reusable documentation

[Prepared profile README](docs/PROFILE_README.md) · [Project README template](docs/PROJECT_README_TEMPLATE.md) · [Account setup instructions](docs/FINISH_GITHUB_SETUP.md)

The existing `tools/finish_github_setup.py` previews changes by default and requires your own authenticated GitHub CLI for `--apply`. This website update does not apply account settings, create a profile repository, or change pins, photos, topics, repository names, visibility, or licenses.

## Contributing and attribution

Open an issue with the affected page, browser, viewport, and reproduction steps. Do not upload credentials, confidential information, or restricted datasets. Code and documentation include AI-assisted work; personal background is supplied by Xavier Chen, and research credit belongs with each linked project.

No project-wide license has been added. Third-party content retains its own rights and restrictions. Educational research only, not investment advice.
