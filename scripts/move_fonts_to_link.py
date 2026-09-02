#!/usr/bin/env python3
"""Move Google Fonts from @import (in theme.css) into <link> tags in every page head.
This guarantees Fraunces/Manrope load on HTTPS (Vercel) — @import inside a CSS
file served via CDN/edge cache frequently fails or is delayed, causing fallback
fonts (thinner text). Also strips the now-unneeded @import from theme.css."""
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONT_HREF = (
    "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;"
    "0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500"
    "&family=Manrope:wght@400;500;600;700&display=swap"
)

# The two preconnect links already exist in every new-design head block.
OLD_PRECONNECT = (
    '  <link rel="preconnect" href="https://fonts.googleapis.com" />\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
)

FONT_LINK = '  <link href="' + FONT_HREF + '" rel="stylesheet" />\n'

NEW_BLOCK = OLD_PRECONNECT + FONT_LINK

HTML_FILES = (
    [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "artikel", "index.html")]
    + [os.path.join(ROOT, "artikel", "template-artikel-master.html")]
    + glob.glob(os.path.join(ROOT, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT, "_scheduled_content", "articles", "*.html"))
)

CSS_PATH = os.path.join(ROOT, "assets", "theme.css")

IMPORT_LINE = (
    "@import url('" + FONT_HREF + "');\n\n"
)


def process_html(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    if "fonts.googleapis.com/css2?family=Fraunces" in s:
        return s, False  # already has the font link
    if OLD_PRECONNECT in s:
        s = s.replace(OLD_PRECONNECT, NEW_BLOCK, 1)
        return s, True
    return s, False


def main():
    apply = "--apply" in sys.argv
    n_html = 0
    for path in sorted(HTML_FILES):
        new, changed = process_html(path)
        rel = os.path.relpath(path, ROOT)
        if changed:
            n_html += 1
            if apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
                print("APPLIED", rel)
            else:
                print("DRY    ", rel)

    # theme.css: drop the @import line (fonts now via <link>)
    css = open(CSS_PATH, encoding="utf-8").read()
    new_css = css.replace(IMPORT_LINE, "")
    if new_css != css:
        print("CSS    theme.css", "APPLIED" if apply else "DRY")
        if apply:
            open(CSS_PATH, "w", encoding="utf-8").write(new_css)

    print("html files updated:", n_html)


if __name__ == "__main__":
    main()
