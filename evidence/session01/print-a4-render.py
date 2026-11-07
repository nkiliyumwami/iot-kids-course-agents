#!/usr/bin/env python3
"""A4 print check: render a lesson's worksheet.md and teacher-guide.md to PDF.

Markdown -> HTML with markdown-it-py (CommonMark + tables), then headless Google Chrome
--print-to-pdf. Page size A4 and 12 mm margins come from the CSS @page rule.
Page counts come from `pdfinfo`.

Usage: python3 print-a4-render.py lessons/01-traffic-light evidence/session01 <tag>
"""
import pathlib, re, subprocess, sys, tempfile

from markdown_it import MarkdownIt

CSS = """
@page { size: A4; margin: 12mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Nunito', 'DejaVu Sans', Arial, sans-serif; font-size: 10.5pt; line-height: 1.32; color: #111; margin: 0; }
h1 { font-size: 16pt; margin: 0 0 4pt; }
h2 { font-size: 12.5pt; margin: 8pt 0 3pt; }
p, ul, ol { margin: 3pt 0; }
blockquote { margin: 4pt 0; padding: 3pt 8pt; border-left: 3pt solid #c33; background: #fbecec; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0; page-break-inside: avoid; }
th, td { border: 0.6pt solid #555; padding: 3pt 4pt; vertical-align: top; text-align: left; }
th { background: #eee; }
td:empty::after { content: '\\00a0'; }
code, pre { font-family: 'JetBrains Mono', 'DejaVu Sans Mono', monospace; font-size: 9pt; }
pre { background: #f4f4f4; padding: 4pt 6pt; margin: 3pt 0; page-break-inside: avoid; }
"""
WORKSHEET_CSS = "td { height: 15pt; }"


def render(md_path, pdf_path, extra_css=""):
    html = MarkdownIt("commonmark").enable("table").render(md_path.read_text(encoding="utf-8"))
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra_css}</style></head><body>{html}</body></html>"
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "page.html"
        src.write_text(doc, encoding="utf-8")
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                        "--no-pdf-header-footer", f"--user-data-dir={tmp}/prof",
                        f"--print-to-pdf={pdf_path}", src.as_uri()],
                       check=True, capture_output=True)
    info = subprocess.run(["pdfinfo", str(pdf_path)], check=True, capture_output=True, text=True).stdout
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    size = re.search(r"^Page size:\s+(.*)$", info, re.M).group(1)
    return pages, size


if __name__ == "__main__":
    lesson, out, tag = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    for name, css in (("worksheet", WORKSHEET_CSS), ("teacher-guide", "")):
        pdf = out / f"print-a4-{tag}-{name}.pdf"
        pages, size = render(lesson / f"{name}.md", pdf.resolve(), css)
        print(f"{name}.md -> {pdf}: {pages} page(s), {size}")
