#!/usr/bin/env python3
"""
GREN Propertykost - Full Sitemap Rebuilder
------------------------------------------
Regenerates `sitemap.xml` from the actual live state of the repo:
  - Always includes homepage + /artikel hub.
  - Iterates every published article under artikel/ (slug folders with index.html),
    reading each article's own og:image + publish date so image URLs stay accurate.
Homepage / hub <lastmod> is derived from the newest published article so a rerun on
a later day produces byte-stable output when content is unchanged.

Usage: python scripts/build_sitemap.py          (dry run - writes nothing)
       python scripts/build_sitemap.py --apply   (writes sitemap.xml)
The publish_scheduler.py remains append-only and is safe to keep running afterwards.
"""

import os
import re
import sys
import glob
from datetime import date, datetime
from html import escape
from xml.sax.saxutils import escape as xml_escape

from _common import to_absolute_image

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")
ARTIKEL_DIR = os.path.join(ROOT_DIR, "artikel")
DOMAIN = "https://www.gren.biz.id"


def extract_og_image(content):
    """Return absolute URL of the og:image from already-loaded HTML content."""
    m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not m:
        m = re.search(r'<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:image["\']', content, re.IGNORECASE)
    if m:
        return to_absolute_image(m.group(1))
    return None


def collect_articles():
    """Return list of dicts for each live article slug folder (single file read each)."""
    articles = []
    for folder in sorted(glob.glob(os.path.join(ARTIKEL_DIR, "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(folder))
        with open(folder, "r", encoding="utf-8") as f:
            content = f.read()

        entry = {"slug": slug}
        m = re.search(r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if m:
            try:
                entry["lastmod"] = datetime.fromisoformat(m.group(1)).date().isoformat()
            except ValueError:
                entry["lastmod"] = date.fromtimestamp(os.path.getmtime(folder)).isoformat()
        else:
            entry["lastmod"] = date.fromtimestamp(os.path.getmtime(folder)).isoformat()

        m = re.search(r"<title>([^<]+)</title>", content, re.IGNORECASE)
        entry["title"] = m.group(1).strip() if m else slug.replace("-", " ").title()

        img = extract_og_image(content)
        if img:
            entry["image"] = img
        articles.append(entry)
    return articles


def build_xml(articles, lastmod):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    lines.append('        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')
    lines.append("")

    # 1. Homepage
    lines.append("  <!-- 1. Halaman Beranda Utama -->")
    lines.append("  <url>")
    lines.append("    <loc>https://www.gren.biz.id/</loc>")
    lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append("    <changefreq>daily</changefreq>")
    lines.append("    <priority>1.0</priority>")
    for img in ("https://www.gren.biz.id/assets/images/rumah-asli.jpg",
                "https://www.gren.biz.id/assets/images/gallery-2.webp"):
        lines.append("    <image:image>")
        lines.append(f"      <image:loc>{xml_escape(img)}</image:loc>")
        lines.append("    </image:image>")
    lines.append("  </url>")
    lines.append("")

    # 2. Blog hub
    lines.append("  <!-- 2. Halaman Direktori Artikel / Blog Hub -->")
    lines.append("  <url>")
    lines.append("    <loc>https://www.gren.biz.id/artikel</loc>")
    lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append("    <changefreq>daily</changefreq>")
    lines.append("    <priority>0.9</priority>")
    lines.append("  </url>")
    lines.append("")

    # 3..N published articles
    for a in articles:
        loc_url = f"{DOMAIN}/artikel/{a['slug']}"
        title = escape(a["title"])
        lines.append(f"  <!-- Artikel: {title} -->")
        lines.append("  <url>")
        lines.append(f"    <loc>{xml_escape(loc_url)}</loc>")
        lines.append(f"    <lastmod>{a['lastmod']}</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("    <priority>0.85</priority>")
        if a.get("image"):
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{xml_escape(a['image'])}</image:loc>")
            lines.append(f"      <image:title>{title}</image:title>")
            lines.append("    </image:image>")
        lines.append("  </url>")
        lines.append("")

    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines)


def main():
    apply = "--apply" in sys.argv
    articles = collect_articles()
    if articles:
        lastmod = max(a["lastmod"] for a in articles)
    else:
        lastmod = date.today().isoformat()
    xml = build_xml(articles, lastmod)

    if not apply:
        print(f"[DRY] Would write sitemap.xml with {len(articles) + 2} URLs "
              f"({len(articles)} articles + homepage + hub), lastmod {lastmod}.")
        return 0

    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"[OK] Regenerated sitemap.xml with {len(articles) + 2} URLs "
          f"({len(articles)} articles + homepage + hub), lastmod {lastmod}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
