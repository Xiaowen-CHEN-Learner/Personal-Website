"""Dependency-free checks of the new homepage; not an external-link audit."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
    def select(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]

class HomepageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / 'index.html').read_text(encoding='utf-8')
        cls.page = Page(cls.text)
        cls.css = (ROOT / 'assets/portfolio.css').read_text(encoding='utf-8')
    def test_language(self):
        self.assertEqual(self.page.select('html')[0]['lang'], 'en')
    def test_single_main_heading(self):
        self.assertEqual(len(self.page.select('h1')), 1)
    def test_unique_ids(self):
        ids = [a['id'] for _, a in self.page.elements if 'id' in a]
        self.assertEqual(len(ids), len(set(ids)))
    def test_fragment_targets_exist(self):
        ids = {a['id'] for _, a in self.page.elements if 'id' in a}
        for a in self.page.select('a'):
            if a.get('href', '').startswith('#'):
                self.assertIn(a['href'][1:], ids)
    def test_keyboard_skip_link(self):
        first = self.page.select('a')[0]
        self.assertEqual(first.get('class'), 'skip-link')
        self.assertEqual(first.get('href'), '#main')
        self.assertEqual(self.page.select('main')[0].get('tabindex'), '-1')
    def test_navigation_has_label(self):
        self.assertTrue(self.page.select('nav')[0].get('aria-label'))
    def test_local_stylesheet_exists(self):
        links = self.page.select('link')
        css = [a['href'] for a in links if a.get('rel') == 'stylesheet']
        self.assertEqual(css, ['assets/portfolio.css'])
        self.assertTrue((ROOT / css[0]).is_file())
    def test_six_featured_projects(self):
        cards = [a for a in self.page.select('article') if a.get('class') == 'project-card']
        self.assertEqual(len(cards), 6)
    def test_no_placeholder_or_unsafe_links(self):
        for a in self.page.select('a'):
            href = a.get('href', '')
            self.assertTrue(href)
            self.assertNotIn(href, ('#', 'https://example.com'))
            self.assertIn(urlsplit(href).scheme, ('', 'https'))
    def test_no_external_runtime_dependencies(self):
        self.assertEqual(self.page.select('script'), [])
        self.assertNotIn('@import', self.css)
        self.assertNotIn('url(', self.css)
    def test_metadata(self):
        meta = self.page.select('meta')
        self.assertTrue(any(a.get('name') == 'viewport' for a in meta))
        self.assertTrue(any(a.get('name') == 'description' and a.get('content') for a in meta))
    def test_reduced_motion_and_focus(self):
        self.assertIn('prefers-reduced-motion:reduce', self.css)
        self.assertIn(':focus-visible', self.css)
    def test_archive_navigation_retained(self):
        self.assertTrue(any(a.get('href') == 'library.html' for a in self.page.select('a')))
    def test_no_email_or_telephone_publication(self):
        self.assertFalse(any(a.get('href', '').startswith(('mailto:', 'tel:')) for a in self.page.select('a')))
    def test_truthful_project_statuses(self):
        for phrase in ('synthetic inputs', 'not a deployed AI service', 'hypothetical $1 million', 'Expected December 2027'):
            self.assertIn(phrase, self.text)

if __name__ == '__main__':
    unittest.main()
