#!/usr/bin/env python3
"""Second-pass cleanup: convert remaining in-article CTA buttons (bg-emerald-600)
that were skipped because the generic rule matched the floating WA anchor first.
Targets only anchors inside the CTA panel (class contains bg-emerald-600)."""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = (
    glob.glob(os.path.join(ROOT, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT, "_scheduled_content", "articles", "*.html"))
)

CTA_BTN = re.compile(
    r'<a\s+href="javascript:void\(0\)"\s+onclick="openDirectWA\(\'([^\']*)\'\)"\s+class="inline-flex items-center gap-2 bg-emerald-600[^"]*"\s*>',
    re.DOTALL,
)

CTA_LINK_EMERALD = re.compile(
    r'<a href="([^"]*)" class="inline-flex items-center gap-2 bg-emerald-600[^"]*"\s*>',
    re.DOTALL,
)


def main():
    apply = "--apply" in sys.argv
    for path in sorted(FILES):
        with open(path, encoding="utf-8") as f:
            original = f.read()
        content = original
        content, n1 = CTA_BTN.subn(
            r'<a href="javascript:void(0)" onclick="openDirectWA(\'\1\')" class="btn btn-accent">',
            content,
        )
        content, n2 = CTA_LINK_EMERALD.subn(
            r'<a href="\1" class="btn btn-accent">',
            content,
        )
        rel = os.path.relpath(path, ROOT)
        if apply:
            if content != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                print("APPLIED", rel, "cta-btn=%d cta-link=%d" % (n1, n2))
            else:
                print("SKIP   ", rel)
        else:
            if n1 or n2:
                print("DRY    ", rel, "cta-btn=%d cta-link=%d" % (n1, n2))


if __name__ == "__main__":
    main()
