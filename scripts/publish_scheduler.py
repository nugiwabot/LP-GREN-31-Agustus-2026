#!/usr/bin/env python3
"""
GREN Propertykost - Automated Scheduled Publishing Engine
---------------------------------------------------------
This script reads `_scheduled_content/manifest.json`, checks if any scheduled
article has reached its release timestamp, and automatically publishes it:
1. Copies the article HTML into `artikel/<slug>/index.html`
2. Copies the image into `assets/images/<image_name>`
3. Injects the new card into the top of the grid in `artikel/index.html`
4. Updates `sitemap.xml` with the new URL and image metadata
5. Updates the manifest status to 'published'
"""

import os
import sys
import json
import shutil
from datetime import datetime, timezone, timedelta

# WIB Timezone (UTC+7)
WIB = timezone(timedelta(hours=7))

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "_scheduled_content", "manifest.json")
ARTIKEL_INDEX_PATH = os.path.join(ROOT_DIR, "artikel", "index.html")
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")

CATEGORY_CONFIG = {
    "panduan": {"name": "Infrastruktur & Makro", "bg": "bg-emerald-700", "text": "text-emerald-700", "badge_bg": "bg-emerald-50", "badge_label": "Makro Trend"},
    "finansial": {"name": "Finansial & Yield", "bg": "bg-amber-600", "text": "text-amber-600", "badge_bg": "bg-emerald-50", "badge_label": "Simulasi Data"},
    "pensiun": {"name": "Pensiun & Wealth", "bg": "bg-amber-700", "text": "text-amber-700", "badge_bg": "bg-amber-50", "badge_label": "Hari Tua Aman"},
    "komparasi": {"name": "Legalitas & Komparasi", "bg": "bg-indigo-700", "text": "text-indigo-700", "badge_bg": "bg-indigo-50", "badge_label": "Head to Head"}
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

def inject_card_into_index(item):
    if not os.path.exists(ARTIKEL_INDEX_PATH):
        print(f"[ERROR] artikel/index.html not found!")
        return False
    
    with open(ARTIKEL_INDEX_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    cat_info = CATEGORY_CONFIG.get(item["category"], CATEGORY_CONFIG["panduan"])
    
    card_html = f'''        <!-- CARD: {item["title"]} -->
        <article class="article-card bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col group" data-category="{item["category"]}">
          <div class="relative overflow-hidden aspect-[16/10] bg-slate-100">
            <a href="/artikel/{item["slug"]}">
              <img 
                src="../assets/images/{item["image"]}" 
                alt="{item["title"]}" 
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
            </a>
            <div class="absolute top-3 left-3">
              <span class="{cat_info["bg"]} text-white text-[11px] font-extrabold px-2.5 py-1 rounded-md shadow">
                {cat_info["name"]}
              </span>
            </div>
            <div class="absolute bottom-3 right-3 bg-slate-900/80 backdrop-blur text-white text-[11px] font-bold px-2 py-0.5 rounded">
              ⏱️ {item.get("read_time", "5 Menit")}
            </div>
          </div>

          <div class="p-6 flex-grow flex flex-col justify-between space-y-4">
            <div>
              <div class="text-xs text-slate-500 font-semibold mb-2">{item.get("publish_display_date", "Terbaru")} • Oleh {item.get("author", "Tim Riset GREN")}</div>
              <h3 class="text-lg font-bold text-slate-900 group-hover:text-brand-700 transition-colors line-clamp-2 leading-snug">
                <a href="/artikel/{item["slug"]}">
                  {item["title"]}
                </a>
              </h3>
              <p class="text-slate-600 text-xs sm:text-sm mt-2.5 line-clamp-3 leading-relaxed">
                {item["description"]}
              </p>
            </div>

            <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
              <a href="/artikel/{item["slug"]}" class="text-xs font-bold text-brand-700 group-hover:underline flex items-center gap-1">
                <span>Baca Selengkapnya</span> &rarr;
              </a>
              <span class="text-[11px] font-bold {cat_info["text"]} {cat_info["badge_bg"]} px-2 py-0.5 rounded">{cat_info["badge_label"]}</span>
            </div>
          </div>
        </article>
'''

        # Inject right after `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="articles-grid">`
    grid_marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="articles-grid">'
    if grid_marker in html:
        parts = html.split(grid_marker, 1)
        html = parts[0] + grid_marker + "\n" + card_html + parts[1]
        
        # Update article count text if present
        # e.g. <span id="article-count"...>5 Artikel Tersedia</span>
        import re
        html = re.sub(
            r'(<span id="article-count"[^>]*>)\s*\d+\s*Artikel Tersedia(</span>)',
            lambda m: f"{m.group(1)} {get_total_published_count()} Artikel Tersedia {m.group(2)}",
            html
        )

        with open(ARTIKEL_INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] Injected card for '{item['slug']}' into artikel/index.html")
        return True
    else:
        print("[ERROR] Could not find #articles-grid marker in artikel/index.html")
        return False

def inject_url_into_sitemap(item):
    if not os.path.exists(SITEMAP_PATH):
        print(f"[ERROR] sitemap.xml not found!")
        return False

    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        xml = f.read()

    today_str = datetime.now(WIB).strftime("%Y-%m-%d")
    url_entry = f'''  <!-- Artikel: {item["title"]} -->
  <url>
    <loc>https://grenpropertykost.vercel.app/artikel/{item["slug"]}</loc>
    <lastmod>{today_str}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
    <image:image>
      <image:loc>https://grenpropertykost.vercel.app/assets/images/{item["image"]}</image:loc>
      <image:title>{item["title"]}</image:title>
    </image:image>
  </url>
'''

    if "</urlset>" in xml:
        xml = xml.replace("</urlset>", url_entry + "\n</urlset>")
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"[OK] Added '{item['slug']}' to sitemap.xml")
        return True
    return False

def get_total_published_count():
    manifest = load_manifest()
    if not manifest:
        return 5
    return len([item for item in manifest.get("articles", []) if item.get("status") == "published"])

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
            release_time_str = item.get("release_timestamp")
            if not release_time_str:
                continue

            release_time = datetime.fromisoformat(release_time_str)
            if release_time <= now_wib:
                print(f"[PROCESS] Due article found: {item['title']} ({item['slug']})")

                # 1. Copy article HTML
                src_html = os.path.join(ROOT_DIR, "_scheduled_content", "articles", f"{item['slug']}.html")
                dst_dir = os.path.join(ROOT_DIR, "artikel", item["slug"])
                dst_html = os.path.join(dst_dir, "index.html")

                if os.path.exists(src_html):
                    os.makedirs(dst_dir, exist_ok=True)
                    shutil.copy2(src_html, dst_html)
                    print(f"  -> Created article page at {dst_html}")
                else:
                    print(f"  [WARN] Source HTML not found at {src_html}, skipping page copy.")

                # 2. Copy image
                src_img = os.path.join(ROOT_DIR, "_scheduled_content", "images", item["image"])
                dst_img = os.path.join(ROOT_DIR, "assets", "images", item["image"])
                if os.path.exists(src_img):
                    shutil.copy2(src_img, dst_img)
                    print(f"  -> Copied image to {dst_img}")

                # 3. Inject card into catalog
                inject_card_into_index(item)

                # 4. Inject URL into sitemap
                inject_url_into_sitemap(item)

                # 5. Update status
                item["status"] = "published"
                item["published_at"] = now_iso
                published_count += 1

    if published_count > 0:
        save_manifest(manifest)
        print(f"[SUCCESS] Successfully published {published_count} article(s)!")
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
