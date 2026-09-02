#!/usr/bin/env python3
"""
GREN Propertykost - Validate every JSON-LD block + basic SEO meta on all pages
------------------------------------------------------------------------------
Usage: python scripts/audit_seo_meta.py [--strict]
Exit code 0 when JSON-LD parses everywhere; --strict also fails on missing H1,
long titles or missing meta description.
"""

import os
import re
import sys
import glob
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = sorted(
    [os.path.join(ROOT_DIR, "index.html"),
     os.path.join(ROOT_DIR, "artikel", "index.html")]
    + glob.glob(os.path.join(ROOT_DIR, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT_DIR, "_scheduled_content", "articles", "*.html"))
)

LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.IGNORECASE | re.DOTALL)


def check_file(path, strict):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    rel = os.path.relpath(path, ROOT_DIR)
    problems = []

    blocks = LD_RE.findall(content)
    if not blocks:
        problems.append("NO JSON-LD")
    for i, raw in enumerate(blocks):
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            problems.append(f"JSON-LD #{i + 1} INVALID: {e}")

    if strict:
        title = re.search(r"<title>([^<]*)</title>", content, re.I)
        title_len = len(title.group(1)) if title else 0
        if not title or not title.group(1).strip():
            problems.append("MISSING <title>")
        elif not (20 <= title_len <= 65):
            problems.append(f"TITLE LENGTH {title_len} (target 20-65)")
        if not re.search(r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']{50,}["\']', content, re.I):
            problems.append("MISSING/SHORT meta description")
        if content.count("<h1") != 1:
            problems.append(f"H1 count = {content.count('<h1')} (expected 1)")
        m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content, re.I)
        if not m:
            problems.append("MISSING canonical")
        elif m.group(1).startswith("http") and "gren.biz.id" not in m.group(1):
            problems.append(f"CANONICAL OTHER DOMAIN: {m.group(1)}")
        if not re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']https?://', content, re.I):
            problems.append("og:image NOT absolute")

    if problems:
        print(f"ISSUE {rel}")
        for p in problems:
            print(f"   - {p}")
        return 1
    return 0


def main():
    strict = "--strict" in sys.argv
    code = 0
    for path in FILES:
        code |= check_file(path, strict)
    if code:
        print(f"\nFound issues across files (strict={strict}).")
    else:
        print(f"All {len(FILES)} files OK: JSON-LD valid" + (" + meta OK." if strict else "."))
    sys.exit(code)


if __name__ == "__main__":
    main()
