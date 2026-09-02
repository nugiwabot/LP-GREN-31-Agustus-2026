#!/usr/bin/env python3
"""
GREN Propertykost - Fix internal "Lanjut Membaca" links pointing to unpublished slugs
--------------------------------------------------------------------------------------
The read-next cards in both published articles and scheduled drafts often point to
articles whose publish_date is LATER (e.g. a page published Sept 2 linking to a
Sept 20 article), producing temporary 404s on live pages.

This script rewrites every read-next card whose target is not yet live
(no artikel/<slug>/index.html in the repo) to point at the most relevant
ALREADY-LIVE article (same topic via shared keywords), so no published page ever
contains a broken internal link. Future scheduled articles are unaffected because
their drafts are fixed now too.

Usage: python scripts/fix_readnext_future.py   (dry run)
       python scripts/fix_readnext_future.py --apply
"""

import os
import re
import sys
import glob
import json

from _common import normalize_readnext_cards

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "_scheduled_content", "manifest.json")
LIVE_DIR = os.path.join(ROOT_DIR, "artikel")

CARD_RE = re.compile(
    r'<a href="/artikel/([a-z0-9-]+)" class="read-next group">.*?</a>',
    re.IGNORECASE | re.DOTALL,
)

STOP_WORDS = {
    "dan", "yang", "untuk", "dengan", "dari", "pada", "ini", "itu", "adalah",
    "jatinangor", "properti", "kost", "rumah", "gren", "investasi", "sewa",
    "mahasiswa", "2026", "di", "ke", "atau", "agar", "agar", "menjadi",
    "serta", "jawa", "barat", "barat",
}


def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in STOP_WORDS}


def load_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_title(title):
    for suffix in (" — GREN Propertykost", " — GREN Property", " — GREN"):
        if title.endswith(suffix):
            title = title[: -len(suffix)]
    return title.strip()


def build_live_info(by_slug):
    live = {}
    for slug, item in by_slug.items():
        folder = os.path.join(LIVE_DIR, slug, "index.html")
        if os.path.exists(folder):
            desc = item.get("meta_description", "") or ""
            hay = f"{item.get('title','')} {item.get('category','')} {slug} {desc}"
            live[slug] = {"tokens": tokenize(hay), "item": item}
    return live


def pick_fallback(target_slug, own_slug, used_slugs, live, by_slug):
    target_item = by_slug.get(target_slug, {})
    desc = target_item.get("meta_description", "") or ""
    target_tokens = tokenize(f"{target_item.get('title','')} {target_item.get('category','')} {target_slug} {desc}")

    best = None
    best_score = -1
    for slug, info in live.items():
        if slug == own_slug or slug in used_slugs:
            continue
        score = len(info["tokens"] & target_tokens)
        if score > best_score:
            best_score = score
            best = slug
    if best is None:
        for slug in live:
            if slug != own_slug and slug not in used_slugs:
                best = slug
                break
    if best is None:
        for slug in live:
            if slug != own_slug:
                best = slug
                break
    return best or "panduan-investasi-rumah-kost-jatinangor-unpad"


def card_markup(slug, info, indent):
    from html import escape
    title = escape(clean_title(info["item"].get("title", slug.replace("-", " "))))
    kicker = escape(info["item"].get("category", "Artikel"))
    inner = indent + "  "
    return (
        f'<a href="/artikel/{slug}" class="read-next group">\n'
        f'{inner}<div class="kicker">{kicker}</div>\n'
        f'{inner}<div class="font-serif text-lg text-slate-900 group-hover:text-brand-700 transition-colors">{title}</div>\n'
        f'{indent}</a>'
    )


def iter_files():
    for path in sorted(glob.glob(os.path.join(ROOT_DIR, "artikel", "*", "index.html"))):
        yield path, os.path.basename(os.path.dirname(path))
    for path in sorted(glob.glob(os.path.join(ROOT_DIR, "_scheduled_content", "articles", "*.html"))):
        yield path, os.path.splitext(os.path.basename(path))[0]


def main():
    apply = "--apply" in sys.argv
    manifest = load_manifest()
    by_slug = {a["slug"]: a for a in manifest["articles"]}
    live = build_live_info(by_slug)
    changed_total = 0

    for path, own_slug in iter_files():
        if own_slug not in by_slug:
            continue
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        # Normalize legacy read-next markup first so old-style cards are retargeted too.
        original = normalize_readnext_cards(original)

        used_slugs = set()
        for m in CARD_RE.finditer(original):
            used_slugs.add(m.group(1))

        def repl(m):
            target = m.group(1)
            if target in live and target != own_slug:
                return m.group(0)
            fallback = pick_fallback(target, own_slug, used_slugs - {target}, live, by_slug)
            used_slugs.add(fallback)
            lead = m.group(0)[: len(m.group(0)) - len(m.group(0).lstrip())]
            details.append(f"    {target}  ->  {fallback}")
            return card_markup(fallback, live[fallback], lead)

        details = []
        new = CARD_RE.sub(repl, original)
        rel = os.path.relpath(path, ROOT_DIR)
        if new != original:
            changed_total += 1
            print(f"CHANGE {rel}")
            for d in details:
                print(d)
            if apply:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)

    if not apply:
        print(f"\nDry run: {changed_total} file(s) contain read-next links to unpublished slugs. Re-run with --apply.")
    else:
        print(f"\nApplied: {changed_total} file(s) updated.")


if __name__ == "__main__":
    main()
