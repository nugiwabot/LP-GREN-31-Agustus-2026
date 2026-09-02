#!/usr/bin/env python3
"""
GREN Propertykost - Add favicon link to every HTML page
--------------------------------------------------------
Inserts a favicon + apple-touch-icon link (absolute URL, safe at any depth)
right after the <meta name="theme-color"> tag if it is not already present.

Usage: python scripts/add_favicon.py   (dry run)
       python scripts/add_favicon.py --apply
"""

import os
import re
import sys
import glob

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAVICON = '  <link rel="icon" type="image/png" href="https://www.gren.biz.id/assets/images/logo.webp" />\n'

FILES = sorted(
    [os.path.join(ROOT_DIR, "index.html"),
     os.path.join(ROOT_DIR, "artikel", "index.html"),
     os.path.join(ROOT_DIR, "artikel", "template-artikel-master.html")]
    + glob.glob(os.path.join(ROOT_DIR, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT_DIR, "_scheduled_content", "articles", "*.html"))
)

ANCHOR = re.compile(r'(<meta name="theme-color" content="#27482F"[^>]*/?>)\n?', re.IGNORECASE)


def main():
    apply = "--apply" in sys.argv
    changed = 0
    for path in FILES:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if "rel=\"icon\"" in content:
            continue
        new = ANCHOR.sub(lambda m: m.group(1) + "\n" + FAVICON.rstrip("\n"), content, count=1)
        if new != content:
            changed += 1
            rel = os.path.relpath(path, ROOT_DIR)
            print(f"CHANGE {rel}")
            if apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    if not apply:
        print(f"\nDry run: {changed} file(s) would gain a favicon link. Re-run with --apply.")
    else:
        print(f"\nApplied favicon to {changed} file(s).")


if __name__ == "__main__":
    main()
