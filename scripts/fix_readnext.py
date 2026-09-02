#!/usr/bin/env python3
"""Fix duplicate </a> introduced in read-next cards, and convert any
read-next cards that were missed because their kicker used -600 colors."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = (
    glob.glob(os.path.join(ROOT, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT, "_scheduled_content", "articles", "*.html"))
)

# Convert leftover old-style read-next card (any kicker color) into new markup.
OLD_CARD = re.compile(
    r'<a href="([^"]*)" class="p-5 rounded-2xl bg-white border border-slate-200 hover:border-brand-700 shadow-sm transition-all block group">\s*'
    r'<span class="text-xs font-bold text-[a-z0-9]+-[0-9]+ block mb-1">(.*?)</span>\s*'
    r'<span class="text-sm font-bold text-slate-900 group-hover:text-brand-700 transition-colors block">(.*?)</span>\s*'
    r'</a>',
    re.DOTALL,
)
NEW_CARD = r'<a href="\1" class="read-next group">\n            <div class="kicker">\2</div>\n            <div class="font-serif text-lg text-slate-900 group-hover:text-brand-700 transition-colors">\3</div>\n          </a>'

# Remove duplicate closing </a> that the earlier replacement left behind.
DUP_CLOSE = re.compile(r"</a>\s*\n\s*</a>")


def fix(content):
    content = OLD_CARD.sub(NEW_CARD, content)
    content = DUP_CLOSE.sub("</a>", content)
    return content


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
