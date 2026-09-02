#!/usr/bin/env python3
"""
GREN Propertykost - Fix og:image / twitter:image & Schema Article image
-----------------------------------------------------------------------
1. Landing/hub pages (index.html, artikel/index.html):
   Only absolutize existing og:image/twitter:image (relative -> https://www.gren.biz.id/...).
2. Article pages (artikel/<slug>/index.html) & scheduled drafts:
   Overwrite og:image/twitter:image and the Article JSON-LD "image" with the
   ACTUAL HERO image (<figure class="mb-12"><img ...>) so social previews + AI
   snippets always match the article (many files currently point at unrelated images).
Usage: python scripts/fix_og_image_absolute.py   (dry run)
       python scripts/fix_og_image_absolute.py --apply
"""

import os
import re
import sys
import glob

from _common import to_absolute_image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LANDING_FILES = [
    os.path.join(ROOT_DIR, "index.html"),
    os.path.join(ROOT_DIR, "artikel", "index.html"),
]

ARTICLE_FILES = sorted(
    glob.glob(os.path.join(ROOT_DIR, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT_DIR, "_scheduled_content", "articles", "*.html"))
)


def find_hero_image(content):
    """Return absolute URL of the hero <img> inside the first <figure>."""
    fig = re.search(r"<figure\b[^>]*>(.*?)</figure>", content, re.IGNORECASE | re.DOTALL)
    if not fig:
        return None
    m = re.search(r'<img\b[^>]*?\ssrc=["\']([^"\']+)["\']', fig.group(1), re.IGNORECASE)
    if not m:
        return None
    return to_absolute_image(m.group(1))


def set_meta_image(content, meta_name, new_value):
    """Rewrite content= of <meta property=meta_name or name=meta_name>."""
    pat = re.compile(
        r"(<meta\s+(?:property|name)=[\"']" + re.escape(meta_name) + r"[\"'][^>]*?content=[\"'])([^\"']*)([\"'])",
        re.IGNORECASE,
    )
    content, n = pat.subn(lambda m: m.group(1) + new_value + m.group(3), content)
    return content, n


def set_schema_article_image(content, new_value):
    """Rewrite the first "image": in the first application/ld+json block."""
    pat_block = re.compile(r"(<script type=\"application/ld\+json\">)(.*?)(</script>)", re.IGNORECASE | re.DOTALL)

    def repl(m):
        block = m.group(2)
        block, n = re.subn(r'"image":\s*"[^"]*"', f'"image": "{new_value}"', block, count=1)
        if n:
            return m.group(1) + block + m.group(3)
        return m.group(0)

    content, n = pat_block.subn(repl, content)
    return content, n


def process_file(path, apply, with_hero):
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()
    content = original
    rel = os.path.relpath(path, ROOT_DIR)
    hero = find_hero_image(content) if with_hero else None

    changed = []
    if hero:
        content, n = set_meta_image(content, "og:image", hero)
        if n:
            changed.append("og:image->hero")
        content, n = set_meta_image(content, "twitter:image", hero)
        if n:
            changed.append("twitter:image->hero")
        content, n = set_schema_article_image(content, hero)
        if n:
            changed.append("schema.image->hero")
    else:
        # landing pages: absolutize existing values only
        for meta in ("og:image", "twitter:image"):
            pat = re.compile(
                r"(<meta\s+(?:property|name)=[\"']" + re.escape(meta) + r"[\"'][^>]*?content=[\"'])([^\"']*)([\"'])",
                re.IGNORECASE,
            )

            def fix(m, meta=meta):
                abs_img = to_absolute_image(m.group(2))
                if abs_img == m.group(2):
                    return m.group(0)
                return m.group(1) + abs_img + m.group(3)

            content, n = pat.subn(fix, content)
            if n:
                changed.append(f"{meta}->absolute")

    if content == original:
        print(f"SKIP   {rel}")
        return
    print(f"CHANGE {rel}  [{', '.join(changed)}]")
    if apply:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def main():
    apply = "--apply" in sys.argv
    for path in LANDING_FILES:
        process_file(path, apply, with_hero=False)
    for path in ARTICLE_FILES:
        process_file(path, apply, with_hero=True)
    if not apply:
        print("\nDry run only. Re-run with --apply to write changes.")
    else:
        print("\nApplied.")


if __name__ == "__main__":
    main()
