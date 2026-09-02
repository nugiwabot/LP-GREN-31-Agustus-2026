#!/usr/bin/env python3
"""Post-restyle cleanup:
- remove duplicate leftover HTML comments around replaced blocks
- strip trailing colon inside takeaway titles (nested span form)
- normalize takeaway-title inner markup
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = (
    glob.glob(os.path.join(ROOT, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT, "_scheduled_content", "articles", "*.html"))
)

RULES = [
    ("dup-nav-comment",
     re.compile(r"<!-- NAVIGATION HEADER -->\s*\n\s*<!-- NAVIGATION HEADER -->"),
     "<!-- NAVIGATION HEADER -->"),
    ("dup-fonts-comment",
     re.compile(r"<!-- Fonts & Tailwind -->\s*\n\s*<!-- Design system:"),
     "<!-- Design system:"),
    ("dup-article-comment",
     re.compile(r"<!-- ARTICLE MAIN CONTENT -->\s*\n\s*<!-- ARTICLE MAIN CONTENT -->"),
     "<!-- ARTICLE MAIN CONTENT -->"),
    ("takeaway-title-whitespace",
     re.compile(r'<div class="takeaway-title">\s*\n\s*\n\s*<span>([^<]*?):\s*</span>\s*\n\s*</div>'),
     r'<div class="takeaway-title">\1</div>'),
    ("takeaway-title-colon",
     re.compile(r'<div class="takeaway-title">\s*(?:<span>)?([^<]*?):\s*(?:</span>)?\s*</div>'),
     lambda m: '<div class="takeaway-title">' + m.group(1).strip() + "</div>"),
    ("badge-whitespace",
     re.compile(r'<span class="badge badge-dark">\s*\n\s*([^<]*?)\s*\n\s*</span>'),
     r'<span class="badge badge-dark">\1</span>'),
]


def clean(content):
    for label, pat, repl in RULES:
        content = pat.sub(repl, content)
    return content


def main():
    apply = "--apply" in sys.argv
    for path in sorted(FILES):
        with open(path, encoding="utf-8") as f:
            original = f.read()
        new = clean(original)
        rel = os.path.relpath(path, ROOT)
        if apply:
            if new != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
                print("APPLIED", rel)
            else:
                print("SKIP   ", rel)
        else:
            print("DRY    ", rel, "CHANGED" if new != original else "clean")


if __name__ == "__main__":
    main()
