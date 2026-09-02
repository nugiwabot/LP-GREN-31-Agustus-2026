#!/usr/bin/env python3
"""
GREN Propertykost - Automated Scheduled Publishing Engine
---------------------------------------------------------
This script reads `_scheduled_content/manifest.json`, checks if any scheduled
article has reached its release timestamp, and automatically publishes it:
1. Copies the article HTML into `artikel/<slug>/index.html`
2. Injects the new card into the top of the grid in `artikel/index.html`
3. Updates `sitemap.xml` with the new URL and image metadata
4. Updates the manifest status to 'published'
"""

import os
import sys
import json
import shutil
import re
from datetime import datetime, timezone, timedelta

# WIB Timezone (UTC+7)
WIB = timezone(timedelta(hours=7))

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "_scheduled_content", "manifest.json")
ARTIKEL_INDEX_PATH = os.path.join(ROOT_DIR, "artikel", "index.html")
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")
ARTICLES_DRAFT_DIR = os.path.join(ROOT_DIR, "_scheduled_content", "articles")

MONTH_NAMES_ID = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

CATEGORY_MAP = {
    "infrastruktur & kawasan": {"slug": "panduan", "badge": "Infrastruktur & Makro"},
    "infrastruktur & makro": {"slug": "panduan", "badge": "Infrastruktur & Makro"},
    "panduan investasi": {"slug": "panduan", "badge": "Panduan Investasi"},
    "finansial & arus kas": {"slug": "finansial", "badge": "Finansial & Yield"},
    "finansial & yield": {"slug": "finansial", "badge": "Finansial & Yield"},
    "wealth strategy & pensiun": {"slug": "pensiun", "badge": "Pensiun & Wealth"},
    "pensiun & wealth": {"slug": "pensiun", "badge": "Pensiun & Wealth"},
    "legalitas & komparasi": {"slug": "komparasi", "badge": "Legalitas & Komparasi"}
}

def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        print(f"[ERROR] Manifest not found at {MANIFEST_PATH}")
        return None
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_manifest(manifest):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def format_id_date(dt):
    day = dt.day
    month = MONTH_NAMES_ID[dt.month]
    year = dt.year
    return f"{day} {month} {year}"

def parse_article_meta(slug, item):
    """Extract metadata from draft HTML file or fallback to manifest data."""
    html_path = os.path.join(ARTICLES_DRAFT_DIR, f"{slug}.html")
    
    title = item.get("title", "").replace(" — GREN Property", "").replace(" — GREN Propertykost", "").strip()
    description = item.get("meta_description") or item.get("description", "")
    author = "Tim Riset GREN"
    image_rel = "../assets/images/gallery-1.webp"
    image_sitemap = "https://grenpropertykost.vercel.app/assets/images/gallery-1.webp"
    read_time = "5 Menit"

    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title from <title> or <h1>
        m_title = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        if m_title:
            t = m_title.group(1).split("—")[0].split("-")[0].strip()
            if t:
                title = t

        # Extract author
        m_auth = re.search(r'<meta\s+name=[\'"]author[\'"]\s+content=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
        if m_auth:
            author = m_auth.group(1).replace(" GREN Property", "").replace(" GREN Propertykost", "").strip()

        # Extract description
        m_desc = re.search(r'<meta\s+name=[\'"]description[\'"]\s+content=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
        if m_desc:
            description = m_desc.group(1).strip()

        # Extract og:image
        m_img = re.search(r'<meta\s+property=[\'"]og:image[\'"]\s+content=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
        if m_img:
            img_raw = m_img.group(1)
            # normalize relative path for artikel/index.html
            # if img_raw is ../../assets/images/artikel/xxx.webp -> ../assets/images/artikel/xxx.webp
            if img_raw.startswith("../../"):
                image_rel = "../" + img_raw[6:]
            elif img_raw.startswith("/"):
                image_rel = ".." + img_raw
            else:
                image_rel = img_raw

            filename = os.path.basename(img_raw)
            image_sitemap = f"https://grenpropertykost.vercel.app/assets/images/artikel/{filename}"

    # Category resolution
    cat_raw = (item.get("category") or "").lower().strip()
    cat_data = CATEGORY_MAP.get(cat_raw, {"slug": "panduan", "badge": item.get("category", "Panduan Investasi")})

    return {
        "title": title,
        "description": description,
        "author": author,
        "image_rel": image_rel,
        "image_sitemap": image_sitemap,
        "read_time": read_time,
        "category_slug": cat_data["slug"],
        "category_badge": cat_data["badge"]
    }

def inject_card_into_index(item, meta, release_dt):
    if not os.path.exists(ARTIKEL_INDEX_PATH):
        print(f"[ERROR] artikel/index.html not found!")
        return False
    
    with open(ARTIKEL_INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    slug = item["slug"]
    
    # Avoid duplicate injection
    if f'/artikel/{slug}' in html:
        print(f"[SKIP] Card for '{slug}' already present in artikel/index.html")
        return True

    date_str = format_id_date(release_dt)
    
    card_html = f'''        <!-- CARD: {meta["title"]} -->
        <article class="article-card bg-white border border-slate-200 flex flex-col group" data-category="{meta["category_slug"]}">
          <div class="relative overflow-hidden aspect-[16/10] bg-slate-100">
            <a href="/artikel/{slug}">
              <img src="{meta["image_rel"]}" alt="{meta["title"]}" class="w-full h-full object-cover group-hover:scale-[1.03] transition-transform duration-500" />
            </a>
            <span class="absolute top-4 left-4 badge badge-dark">{meta["category_badge"]}</span>
          </div>
          <div class="p-7 flex-grow flex flex-col justify-between">
            <div>
              <div class="text-xs text-slate-500 font-medium mb-2">{date_str} · {meta["author"]}</div>
              <h3 class="font-serif text-xl text-slate-900 leading-snug group-hover:text-brand-700 transition-colors line-clamp-2">
                <a href="/artikel/{slug}">{meta["title"]}</a>
              </h3>
              <p class="mt-3 text-sm text-slate-600 line-clamp-3 leading-relaxed">
                {meta["description"]}
              </p>
            </div>
            <div class="pt-5 mt-6 border-t border-slate-200 flex items-center justify-between">
              <a href="/artikel/{slug}" class="text-xs font-bold text-brand-700 uppercase tracking-[0.14em] flex items-center gap-1.5 group-hover:gap-3 transition-all">
                Baca Artikel
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"/></svg>
              </a>
              <span class="text-[0.62rem] uppercase tracking-[0.14em] text-slate-400 font-bold">{meta["read_time"]}</span>
            </div>
          </div>
        </article>
'''

    grid_marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="articles-grid">'
    if grid_marker in html:
        parts = html.split(grid_marker, 1)
        html = parts[0] + grid_marker + "\n" + card_html + parts[1]
        
        # Recount all article cards in index
        total_cards = len(re.findall(r'<article class="article-card', html))
        
        html = re.sub(
            r'(<span id="article-count"[^>]*>)\s*\d+\s*Artikel\s*(?:Tersedia|Ditemukan)?(</span>)',
            f'\\g<1>\n          {total_cards} Artikel Tersedia\n        \\g<2>',
            html
        )

        with open(ARTIKEL_INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] Injected card for '{slug}' into artikel/index.html (Total: {total_cards})")
        return True
    else:
        print("[ERROR] Could not find #articles-grid marker in artikel/index.html")
        return False

def inject_url_into_sitemap(item, meta, release_dt):
    if not os.path.exists(SITEMAP_PATH):
        print(f"[ERROR] sitemap.xml not found!")
        return False

    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        xml = f.read()

    slug = item["slug"]
    loc_url = f"https://grenpropertykost.vercel.app/artikel/{slug}"
    
    if loc_url in xml:
        return True

    date_str = release_dt.strftime("%Y-%m-%d")
    url_entry = f'''  <!-- Artikel: {meta["title"]} -->
  <url>
    <loc>{loc_url}</loc>
    <lastmod>{date_str}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
    <image:image>
      <image:loc>{meta["image_sitemap"]}</image:loc>
      <image:title>{meta["title"]}</image:title>
    </image:image>
  </url>
'''

    if "</urlset>" in xml:
        xml = xml.replace("</urlset>", url_entry + "\n</urlset>")
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"[OK] Added '{slug}' to sitemap.xml")
        return True
    return False

def run_publisher():
    manifest = load_manifest()
    if not manifest:
        sys.exit(1)

    now_wib = datetime.now(WIB)
    now_iso = now_wib.isoformat()
    print(f"[INFO] Running GREN Content Scheduler at {now_iso} WIB")

    published_count = 0

    for item in manifest.get("articles", []):
        if item.get("status") == "scheduled":
            release_time_str = item.get("publish_date") or item.get("release_timestamp")
            if not release_time_str:
                continue

            release_time = datetime.fromisoformat(release_time_str)
            if release_time <= now_wib:
                slug = item["slug"]
                print(f"[PROCESS] Publishing article #{item['id']}: {item['title']} ({slug})")

                # Parse meta from draft HTML
                meta = parse_article_meta(slug, item)

                # 1. Copy article HTML to live directory
                src_html = os.path.join(ROOT_DIR, "_scheduled_content", "articles", f"{slug}.html")
                dst_dir = os.path.join(ROOT_DIR, "artikel", slug)
                dst_html = os.path.join(dst_dir, "index.html")

                if os.path.exists(src_html):
                    os.makedirs(dst_dir, exist_ok=True)
                    shutil.copy2(src_html, dst_html)
                    print(f"  -> Published article page to {dst_html}")
                else:
                    print(f"  [WARN] Source HTML not found at {src_html}")

                # 2. Inject card into catalog artikel/index.html
                inject_card_into_index(item, meta, release_time)

                # 3. Inject URL into sitemap.xml
                inject_url_into_sitemap(item, meta, release_time)

                # 4. Update manifest entry
                item["status"] = "published"
                item["live_url"] = f"/artikel/{slug}"
                item["published_at"] = now_iso
                published_count += 1

    if published_count > 0:
        # Update manifest summary counts
        manifest["published_count"] = len([a for a in manifest["articles"] if a.get("status") == "published"])
        manifest["scheduled_count"] = len([a for a in manifest["articles"] if a.get("status") == "scheduled"])
        save_manifest(manifest)
        print(f"[SUCCESS] Successfully published {published_count} new article(s)! (Total published: {manifest['published_count']})")
        return True
    else:
        print("[INFO] No pending scheduled articles reached their release timestamp.")
        return False

if __name__ == "__main__":
    has_changes = run_publisher()
    if has_changes:
        sys.exit(0)
    else:
        sys.exit(0)
