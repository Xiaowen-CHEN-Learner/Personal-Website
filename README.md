# Xavier Chen — AI-Driven Investment Research

A research-focused portfolio built around the [Fordham research project 2026–2027](https://github.com/Xiaowen-CHEN-Learner/Fordham-research-project-2026-2027): 17 weekly reports across two tracks (Financial Markets and Investment with AI), plus the repositories, notebooks, and tools behind them.

[![Portfolio checks](https://github.com/Xiaowen-CHEN-Learner/Personal-Website/actions/workflows/portfolio-checks.yml/badge.svg)](https://github.com/Xiaowen-CHEN-Learner/Personal-Website/actions/workflows/portfolio-checks.yml)

**[Portfolio website](https://xiaowen-chen-learner.github.io/Personal-Website/)** · **[LinkedIn](https://www.linkedin.com/in/xiaowen-chen/)** · **[GitHub](https://github.com/Xiaowen-CHEN-Learner)**

## What is here

The homepage opens with a dark, futuristic hero on turning AI into working investment research, a six-step "AI implementation & transformation" grid (prompt engineering, building AI tools, Claude-assisted theses, shipping AI-built products, research pipelines, human judgment) with each step linked to its report, then three featured reports (the NEWSROOM.md Desk Brief pipeline, the Claude-assisted uranium and nuclear energy thesis, and the 2-year Treasury fixed-income final project), followed by the complete list of 17 reports organized by track, each linking to its dated PDF on GitHub. Below that, six selected repositories (precious-metals portfolio, AI research workflows, finance games, fixed income, equity research, quantamental investing) are tied back to the reports they support. Research, prototypes, and runnable examples are labeled as such.

`library.html` preserves the previous research-library homepage byte-for-byte, including its existing article index. Archived statements and figures retain their original dates and were not revalidated in this update. The earlier `Personal website/` version is also retained.

## Tech stack

Semantic HTML and a local CSS file. The dark theme uses CSS gradients, system fonts, and one reduced-motion-aware keyframe animation; the homepage needs no JavaScript, external fonts, analytics, build step, or backend. The legacy writing archive has its original JavaScript and external resources.

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

The structural tests also verify that the research section lists exactly 17 report links, each a space-free URL to a PDF in the research repository. The browser script tests the homepage at 320, 390, 768, and 1440 pixels, checks keyboard navigation and horizontal overflow, and captures full-page screenshots. It also checks that project cards and contact information remain visible without JavaScript.

Open **Actions → Portfolio checks → a completed run → portfolio-browser-evidence** for its screenshots and JSON report. Artifacts are retained for 30 days. The badge reflects actual workflow status, not a static claim of success.

[Validation scope and local results](docs/PORTFOLIO_VALIDATION.md). Tests do not establish full accessibility compliance, correctness of investment research, or the availability of external destinations.

## Repository structure

```text
index.html                     Research-focused homepage (17 report links + 6 repositories)
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
