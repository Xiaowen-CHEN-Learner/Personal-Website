# Xavier Chen — Personal Portfolio Website

A static personal website supporting my portfolio in finance, investment research, and applied technology.

**[Published site URL](https://xiaowen-chen-learner.github.io/Personal-Website/)** · **[LinkedIn](https://www.linkedin.com/in/xiaowen-chen/)** · **[GitHub](https://github.com/Xiaowen-CHEN-Learner)**

## Profile and repository setup

[Professional profile README](docs/PROFILE_README.md) · [Project README template](docs/PROJECT_README_TEMPLATE.md) · [Finish account setup](docs/FINISH_GITHUB_SETUP.md)

The [setup script](tools/finish_github_setup.py) can activate the profile README and apply the prepared bio, descriptions, and topics using your own authenticated GitHub CLI. It defaults to preview-only mode. Eleven local safety tests passed; the authenticated account-update path has not been run in this editing session. Pins and photo remain interface-only steps.

## Project description

This repository contains my personal website and an earlier HTML iteration. It complements the research notebooks, written analysis, and educational tools available across my GitHub account.

The published URL above is the address recorded in the original README. Deployment availability and browser behaviour should be checked separately; these documentation/tooling updates do not rebuild or retest the website.

## Tech stack

Static HTML with inline styling and browser scripting where present. The repository contains no JavaScript package-manager manifest or backend application. The optional profile-setup utility uses Python's standard library and GitHub CLI.

## Installation

Clone the repository and serve it locally with Python 3:

```bash
git clone https://github.com/Xiaowen-CHEN-Learner/Personal-Website.git
cd Personal-Website
python -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/` in a browser. On Windows, `py -m http.server 8000 --bind 127.0.0.1` can be used when the Python launcher is installed.

## Usage

The root `index.html` is the website entry point. The `Personal website/` directory retains an earlier HTML version. Review links, factual claims, mobile layout, accessibility, and external resources before publishing changes.

No JavaScript package installation is required for basic static serving. To test the separate setup utility without applying account changes:

```bash
python -m unittest discover -s tests -v
python tools/finish_github_setup.py
```

## Selected project repositories

| Project | Focus |
| --- | --- |
| [Learn Finance Through Games](https://github.com/Xiaowen-CHEN-Learner/Learn-Finance-Though-Games) | Interactive finance education using HTML, CSS, JavaScript, and historical-data resources |
| [Quantamental Investing Research](https://github.com/Xiaowen-CHEN-Learner/Quantitative-investing_Quantamental-approach) | Python notebooks for VIX/index experiments and market-sentiment exploration |
| [Equity Research Portfolio](https://github.com/Xiaowen-CHEN-Learner/Equity-research) | Written investment research and industry notes |
| [Market Price and Catalyst Visualizations](https://github.com/Xiaowen-CHEN-Learner/AI-Projects---Price-Catalysts) | Market charts, event annotations, and visualization experiments |
| [AI Research Workflows](https://github.com/Xiaowen-CHEN-Learner/From-prompt-to-AI-system) | Reusable Markdown instructions and portfolio-review examples |
| [Fixed-Income Research Lab](https://github.com/Xiaowen-CHEN-Learner/Headhunt_FixedIncome) | Offline bond-pricing example with 15 local unit tests, plus dated research inputs |

## Portfolio maintenance

Use a consistent professional name, keep project descriptions aligned with actual implementation, and distinguish completed work from roadmaps. Update education and experience dates when they change.

Keep private contact details, confidential employer material, restricted datasets, and credentials out of the website. Credit collaborators and AI assistance, and distinguish individual responsibilities.

## Roadmap

Align the website's visible introduction and project cards with the research portfolio; add representative screenshots or result summaries; verify demos, accessibility, and mobile layouts. Consolidate experimental versions only after preserving unique work. These website changes remain pending; the account setup utility does not perform them.

## Contact and license

[Xavier Chen on LinkedIn](https://www.linkedin.com/in/xiaowen-chen/)

No project-wide license is included. This README does not grant rights to third-party assets or linked research materials.
