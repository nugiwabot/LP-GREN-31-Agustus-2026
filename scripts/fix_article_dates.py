#!/usr/bin/env python3
"""
GREN Propertykost - Reconcile article dates with manifest publish slot
-----------------------------------------------------------------------
Problem: every draft/artikel embeds its own (often arbitrarily future) date in
  - <meta property="article:published_time|modified_time">
  - JSON-LD "datePublished"/"dateModified"
  - the visible header date ("· 6 September 2026")

while the scheduler + blog cards use manifest.json "publish_date". This makes
schema dates, visible dates and card dates contradict each other.

Rule applied here (manifest is authoritative for scheduled & scheduler-published):
  * scheduled articles  -> date := manifest publish_date
  * published articles whose file date is in the FUTURE (impossible) -> date := manifest publish_date
  * published articles with a real past date (hand-published pillars) -> LEFT UNTOUCHED

Usage: python scripts/fix_article_dates.py   (dry run)
       python scripts/fix_article_dates.py --apply
"""

import os
import re
import sys
import glob
import json
from datetime import datetime, date

from _common import display_date_from_iso

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "_scheduled_content", "manifest.json")

META_DATE_RE = re.compile(
    r'(<meta\s+property=["\']article:(?:published|modified)_time["\']\s+content=["\'])([^"\']+)(["\'])',
    re.IGNORECASE,
)
SCHEMA_DATE_RE = re.compile(r'("date(?:Published|Modified)":\s*")([^"]+)(")')
VISIBLE_DATE_RE = re.compile(r"(·\s*)\d{1,2}\s+[A-Za-z]+\s+\d{4}")


def display_date(iso):
    return display_date_from_iso(iso)


def load_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def iter_files():
    for path in sorted(glob.glob(os.path.join(ROOT_DIR, "artikel", "*", "index.html"))):
        yield path, os.path.basename(os.path.dirname(path))
    for path in sorted(glob.glob(os.path.join(ROOT_DIR, "_scheduled_content", "articles", "*.html"))):
        yield path, os.path.splitext(os.path.basename(path))[0]


def main():
    apply = "--apply" in sys.argv
    manifest = load_manifest()
    by_slug = {a["slug"]: a for a in manifest["articles"]}
    today = date.today()
    changed_total = 0

    for path, slug in iter_files():
        if slug not in by_slug:
            continue
        item = by_slug[slug]
        manifest_iso = item.get("publish_date") or item.get("release_timestamp")
        if not manifest_iso:
            continue

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # determine current file date
        m = META_DATE_RE.search(content)
        file_iso = m.group(2) if m else None
        if not file_iso:
            m2 = SCHEMA_DATE_RE.search(content)
            file_iso = m2.group(2) if m2 else None

        status = item.get("status", "scheduled")
        skip = False
        if file_iso:
            try:
                file_date = datetime.fromisoformat(file_iso).date()
            except ValueError:
                file_date = None
            if file_date is not None:
                if status == "published" and file_date <= today and file_date != datetime.fromisoformat(manifest_iso).date():
                    skip = True  # hand-published pillar with a real past date
        if skip:
            continue

        if file_iso == manifest_iso:
            continue

        rel = os.path.relpath(path, ROOT_DIR)
        display = display_date(manifest_iso)

        new_content = content
        new_content, n1 = META_DATE_RE.subn(lambda x: x.group(1) + manifest_iso + x.group(3), new_content)
        # schema datePublished/dateModified inside first ld+json block only
        block_re = re.compile(r"(<script type=\"application/ld\+json\">)(.*?)(</script>)", re.IGNORECASE | re.DOTALL)

        def repl_block(bm):
            inner = bm.group(2)
            inner, n = SCHEMA_DATE_RE.subn(lambda x: x.group(1) + manifest_iso + x.group(3), inner)
            return bm.group(1) + inner + bm.group(3)

        new_content, n2 = block_re.subn(repl_block, new_content)
        new_content, n3 = VISIBLE_DATE_RE.subn(lambda x: x.group(1) + display, new_content)

        if new_content != content:
            changed_total += 1
            print(f"CHANGE {rel}  {file_iso[:10] or '?'} -> {manifest_iso[:10]}  (meta:{n1} schema:{n2} visible:{n3})")
            if apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
        else:
            print(f"NOOP   {rel}")

    if not apply:
        print(f"\nDry run: {changed_total} file(s) would change. Re-run with --apply.")
    else:
        print(f"\nApplied: {changed_total} file(s) aligned to manifest publish dates.")


if __name__ == "__main__":
    main()
