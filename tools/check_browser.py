"""Chromium smoke checks and screenshots for the static homepage.

Uses a local loopback server. Checks the homepage, not legacy/external pages.
Install playwright and its Chromium browser to run; no server dependency.
"""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run(executable: str | None, output: Path, in_memory: bool = False) -> dict:
    from playwright.sync_api import sync_playwright
    output.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    mode = 'in-memory HTML/CSS; no HTTP validation' if in_memory else 'loopback HTTP server'
    report = {'scope': f'new homepage via {mode}; external links and legacy archive not visited', 'viewports': []}
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    css = (ROOT / 'assets/portfolio.css').read_text(encoding='utf-8')
    memory_html = html.replace('<link rel="stylesheet" href="assets/portfolio.css">', '<style>' + css + '</style>')
    def load(page):
        if in_memory:
            page.set_content(memory_html, wait_until='load')
        else:
            response = page.goto(base, wait_until='networkidle')
            assert response and response.status == 200, 'Homepage did not load'
    try:
        with sync_playwright() as p:
            options = {'headless': True}
            if executable:
                options['executable_path'] = executable
            browser = p.chromium.launch(**options)
            report['browser'] = browser.version
            try:
                for width, height in ((320, 800), (390, 844), (768, 1024), (1440, 1000)):
                    context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion='reduce')
                    page = context.new_page()
                    errors, external = [], []
                    page.on('pageerror', lambda e: errors.append(str(e)))
                    page.on('request', lambda r: external.append(r.url) if urlsplit(r.url).hostname != '127.0.0.1' else None)
                    load(page)
                    assert page.locator('h1').count() == 1, 'Expected one main heading'
                    assert page.locator('.project-card').count() == 6, 'Expected six project cards'
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), f'Horizontal overflow at {width}px'
                    page.keyboard.press('Tab')
                    assert page.locator('.skip-link').evaluate('(e) => e === document.activeElement'), 'Skip link is not first focus target'
                    page.keyboard.press('Enter')
                    assert page.locator('main').evaluate('(e) => e === document.activeElement'), 'Skip link did not focus main'
                    page.get_by_role('link', name='Selected work', exact=True).click()
                    assert page.url.endswith('#work'), 'Work navigation failed'
                    page.get_by_role('link', name='About', exact=True).click()
                    assert page.url.endswith('#about'), 'About navigation failed'
                    page.get_by_role('link', name='Contact', exact=True).click()
                    assert page.url.endswith('#contact'), 'Contact navigation failed'
                    assert page.locator('h1').evaluate('(e) => getComputedStyle(e).fontFamily').startswith('Georgia'), 'Stylesheet not applied'
                    assert not errors, errors
                    assert not external, f'Unexpected remote resource requests: {external}'
                    page.evaluate('document.activeElement.blur(); window.scrollTo(0, 0)')
                    page.screenshot(path=str(output / f'homepage-{width}.png'), full_page=True)
                    report['viewports'].append({'width': width, 'height': height, 'checks': 11 if in_memory else 12, 'result': 'passed'})
                    context.close()
                context = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
                page = context.new_page()
                load(page)
                assert page.locator('.project-card').count() == 6, 'No-JavaScript content missing'
                page.get_by_role('link', name='Contact via LinkedIn', exact=True).wait_for(state='visible')
                report['no_javascript'] = 'six project cards and contact link visible'
                context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
    (output / 'browser-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable', help='Optional existing Chromium executable; default uses the Playwright-managed browser.')
    parser.add_argument('--in-memory', action='store_true', help='Render local HTML/CSS in memory; no HTTP navigation or validation.')
    parser.add_argument('--output', type=Path, default=ROOT / 'browser-output')
    args = parser.parse_args()
    print(json.dumps(run(args.executable, args.output, args.in_memory), indent=2))
