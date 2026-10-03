# Homepage validation — October 3, 2026

## Changes

Replaced the root homepage with a responsive, project-focused introduction; retained the previous homepage verbatim as `library.html`. Original Git blob: `a7bdf15eba45b2237ec6716f2c6f3769185acc66`. The writing archive and research content were not rewritten or revalidated.

The introduction and professional highlights use the education, research-assistant duties, forecasting scope, and reporting-automation experience supplied by Xavier Chen. No private CV, email, phone number, or credentials were published.

## Verified hosted results

For website commit `41f2805451666e6a5ae62dab902c093806548a4f`:

- [Portfolio checks, run 37130074892](https://github.com/Xiaowen-CHEN-Learner/Personal-Website/actions/runs/37130074892): the homepage job completed successfully, including unit tests, browser checks, and screenshot upload.
- The downloaded `portfolio-browser-evidence` artifact reports **12 checks passed at each of four viewports**: 320×800, 390×844, 768×1024, and 1440×1000. Its Chromium version was 143.0.7499.4. These checks used the checkout served over loopback HTTP on the hosted runner.
- The artifact also confirms a JavaScript-disabled check: six project cards and the contact link were visible.
- [GitHub Pages build and deployment, run 37130073763](https://github.com/Xiaowen-CHEN-Learner/Personal-Website/actions/runs/37130073763): completed successfully for the same website commit.

A successful deployment is not a separate browser test of the public GitHub Pages URL. The hosted browser checks exercised the checked-out website, not its public domain or linked project demos.

## Local checks completed

- 15 new homepage structural tests passed.
- 11 existing account-setup safety tests passed again (26 unit tests total).
- Chromium 144.0.7559.96 with Playwright 1.57.0: 11 checks passed at each of four viewports (320×800, 390×844, 768×1024, 1440×1000).
- A separate JavaScript-disabled check confirmed the six project cards and contact link remain visible.
- Full-page screenshots were captured at all four sizes.

The local browser prohibits loopback navigation, so the local visual checks used the HTML and CSS rendered **in memory**, without bypassing its network restrictions. The subsequent hosted run above tested HTTP serving separately.

## Automated workflow

`.github/workflows/portfolio-checks.yml` runs the unit tests, installs the pinned Playwright package and its Chromium browser, serves the checkout over loopback HTTP, and runs the browser script. It uploads screenshots and a JSON report as `portfolio-browser-evidence` with 30-day retention. Permissions are read-only; the workflow does not publish account changes or push commits.

Consult the actual Actions result for later changes. Browser and Python patch versions can differ between local and hosted runs.

## What the browser checks cover

One main heading; six project cards; no horizontal document overflow; keyboard skip-link focus and destination; Work, About, and Contact anchor navigation; applied heading styles; no JavaScript page errors; no unexpected remote runtime-resource requests. The HTTP mode additionally checks the homepage's 200 response.

## Limits

These are smoke checks, not a comprehensive accessibility audit or a cross-browser certification. They do not crawl external GitHub, LinkedIn, GitHub Pages demos, or the archived article destinations. Direct live-site retrieval from this editing environment was unsuccessful; that is not evidence that the public site is down.

The update neither reproduces market-data notebooks nor validates financial returns, data-redistribution rights, or the original writing archive. Account bio, pins, photo, repository names, descriptions, topics, and profile-repository creation remain outside this connection's available actions.

## Reproduce

```bash
python -m unittest discover -s tests -v
python -m pip install playwright==1.57.0
python -m playwright install chromium
python tools/check_browser.py
```

For a rendering-only environment, `python tools/check_browser.py --in-memory` skips HTTP navigation and reports that narrower scope. `--executable /path/to/chromium` selects an existing Chromium binary; the default uses Playwright's managed browser.
