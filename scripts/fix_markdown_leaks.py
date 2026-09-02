#!/usr/bin/env python3
"""
GREN Propertykost - Remove leaked Markdown formatting from article HTML
-----------------------------------------------------------------------
Converts stray *emphasis* / **strong** Markdown (which was generated into HTML
body text) into proper <em>/<strong> tags so articles render cleanly and search
engines/AI parse the text without literal asterisks.

Conversion order (em before strong) handles nesting like:
  **"X" (*Gold Standard Tenants*)**  ->  <strong>"X" (<em>Gold Standard Tenants</em>)</strong>

Usage: python scripts/fix_markdown_leaks.py   (dry run)
       python scripts/fix_markdown_leaks.py --apply
"""

import os
import re
import sys
import glob

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = sorted(
    glob.glob(os.path.join(ROOT_DIR, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT_DIR, "_scheduled_content", "articles", "*.html"))
)

EM_PAT = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
STRONG_PAT = re.compile(r"\*\*([^*]+)\*\*")


def fix(content):
    content = EM_PAT.sub(r"<em>\1</em>", content)
    content = STRONG_PAT.sub(r"<strong>\1</strong>", content)
    return content


def main():
    apply = "--apply" in sys.argv
    total = 0
    for path in FILES:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        new = fix(original)
        rel = os.path.relpath(path, ROOT_DIR)
        if new == original:
            continue
        # count remaining stray asterisks for the report
        left = len(re.findall(r"\*", new))
        changed = len(re.findall(r"\*", original)) - left
        total += 1
        print(f"CHANGE {rel}  (asterisk pairs converted: {changed}, leftover '*': {left})")
        if apply:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
    if not apply:
        print(f"\nDry run: {total} files contain Markdown leaks. Re-run with --apply to fix.")
    else:
        print(f"\nApplied: {total} files fixed.")


if __name__ == "__main__":
    main()
