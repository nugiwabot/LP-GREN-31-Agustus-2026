#!/usr/bin/env python3
"""Fix duplicate </a> introduced in read-next cards, and convert any
read-next cards that were missed because their kicker used -600 colors."""
import glob
import os
import sys

from _common import normalize_readnext_cards

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = (
    glob.glob(os.path.join(ROOT, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT, "_scheduled_content", "articles", "*.html"))
)


def fix(content):
    return normalize_readnext_cards(content)


def main():
    apply = "--apply" in sys.argv
    for path in sorted(FILES):
        with open(path, encoding="utf-8") as f:
            original = f.read()
        new = fix(original)
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
