#!/usr/bin/env python3
"""A4 print check with Playwright (headless Chromium), for machines without Google Chrome (the Azure VM).

Same Markdown -> HTML step and the same CSS as print-a4-render.py (A4, 12 mm margins, 10.5 pt body,
15 pt worksheet rows); only the PDF engine differs. Page counts come from pypdf.

Usage: python3 print-a4-render-playwright.py lessons/01-traffic-light evidence/session01 <tag>
"""
import importlib.util, pathlib, sys

from markdown_it import MarkdownIt
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

_spec = importlib.util.spec_from_file_location("chrome_render", pathlib.Path(__file__).with_name("print-a4-render.py"))
_base = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_base)
CSS, WORKSHEET_CSS = _base.CSS, _base.WORKSHEET_CSS

if __name__ == "__main__":
    lesson, out, tag = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        print(f"engine: Playwright Chromium {browser.version}")
        page = browser.new_page()
        for name, css in (("worksheet", WORKSHEET_CSS), ("teacher-guide", "")):
            html = MarkdownIt("commonmark").enable("table").render((lesson / f"{name}.md").read_text(encoding="utf-8"))
            page.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{css}</style></head><body>{html}</body></html>")
            pdf = out / f"print-a4-{tag}-{name}.pdf"
            page.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
            r = PdfReader(str(pdf)); box = r.pages[0].mediabox
            print(f"{name}.md -> {pdf}: {len(r.pages)} page(s), {float(box.width):.2f} x {float(box.height):.2f} pts")
        browser.close()
