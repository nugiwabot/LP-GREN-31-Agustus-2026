#!/usr/bin/env python3
"""
Restyle GREN Propertykost article pages to the new premium design system.

Applies the shared theme (assets/theme.js + theme.css + brand.js) and premium
chrome to every article page:
  - artikel/<slug>/index.html          (5 live articles)
  - _scheduled_content/articles/*.html (55 scheduled articles)

Usage:
  python scripts/restyle_articles.py            # dry-run: print per-file counts
  python scripts/restyle_articles.py --apply    # write changes
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = (
    glob.glob(os.path.join(ROOT, "artikel", "*", "index.html"))
    + glob.glob(os.path.join(ROOT, "_scheduled_content", "articles", "*.html"))
)
FILES = [f for f in FILES if "template-artikel-master" not in f]

PREFIX = "../../"

NEW_HEAD = """  <!-- Design system: Tailwind CDN + shared theme + shared helpers -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="__P__assets/theme.js"></script>
  <link rel="stylesheet" href="__P__assets/theme.css" />
  <script src="__P__assets/brand.js"></script>
"""

NEW_HEADER = """  <!-- NAVIGATION HEADER -->
  <header class="bg-slate-50/95 backdrop-blur-md sticky top-0 z-40 border-b border-slate-200">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between py-3">
      <a href="__P__" class="flex items-center gap-3">
        <img src="__P__assets/images/logo.webp" alt="Logo GREN Propertykost" class="h-10 w-auto object-contain" onerror="this.src='__P__Logo GREN Propertykost.png'"/>
        <span class="flex flex-col leading-none">
          <span class="font-serif text-lg sm:text-xl text-slate-900 tracking-tight">
            GREN <span class="text-brand-700">Propertykost</span>
          </span>
          <span class="text-[0.6rem] font-bold tracking-[0.3em] text-slate-500 uppercase mt-1">Jatinangor</span>
        </span>
      </a>

      <div class="flex items-center gap-4">
        <a href="/artikel" class="text-xs sm:text-sm font-semibold text-slate-600 hover:text-brand-700 transition-colors">
          &larr; Daftar Artikel
        </a>
        <a href="__P__#tipe-unit" class="text-xs sm:text-sm font-bold text-brand-700 hover:text-brand-900 hidden md:inline">
          Pricelist Unit
        </a>
        <a href="javascript:void(0)" onclick="openDirectWA()" class="btn btn-primary !py-2.5 !px-4 !text-[0.7rem]">
          Konsultasi WA
        </a>
      </div>
    </div>
  </header>
"""

NEW_FOOTER = """  <footer class="bg-slate-950 text-slate-400 py-12 border-t border-slate-800 text-sm mt-12">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-4">
      <div class="flex items-center justify-center gap-3">
        <img src="__P__assets/images/logo.webp" alt="Logo GREN" class="h-8 w-auto object-contain bg-white/10 p-1" onerror="this.src='__P__Logo GREN Propertykost.png'"/>
        <span class="font-serif text-lg text-white">GREN <span class="text-brand-600">Propertykost</span></span>
      </div>
      <p class="text-xs text-slate-500 max-w-lg mx-auto">
        Jl. GKPN, Cipacing, Jatinangor, Kabupaten Sumedang, Jawa Barat 45363.
      </p>
      <div class="pt-4 text-xs text-slate-600">
        &copy; 2026 GREN Propertykost. Hak cipta dilindungi.
      </div>
    </div>
  </footer>
"""

NEW_WA = """  <div class="fixed bottom-6 right-6 z-50">
    <a
      href="javascript:void(0)"
      onclick="openDirectWA()"
      class="btn btn-wa !py-3.5 !px-5 text-xs sm:text-sm"
      aria-label="Konsultasi WhatsApp"
    >
      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.711 2.598 2.664-.698c1.024.557 1.776.819 2.796.819 3.183 0 5.77-2.587 5.77-5.768.001-3.18-2.585-5.766-5.77-5.766zm9.969 5.766c0 5.514-4.486 10-10 10-1.823 0-3.529-.49-5.002-1.341l-5.998 1.568 1.602-5.856c-.958-1.536-1.502-3.348-1.502-5.371 0-5.514 4.486-10 10-10s10 4.486 10 10z"/></svg>
      <span>Konsultasi WhatsApp</span>
    </a>
  </div>
"""

# ---------------------------------------------------------------------------
# Replacement rules: (label, regex, replacement, flags)
# ---------------------------------------------------------------------------
RULES = [
    # 1. theme-color
    ("theme-color", re.compile(r'content="#15803d"'), 'content="#27482F"', 0),

    # 2. emoji / decorative chars (explicit chars; en-dash – is NOT stripped)
    ("emoji", re.compile("[" + "".join([
        "\U000023F1", "\uFE0F", "\U000026A1", "\U00002696", "\U00002B50",
        "\U0001F4D6", "\U00002600", "\U0001F319", "\U0001F446", "\U0001F512",
        "\U00002728", "\U0001F3AF", "\U0001F4B0", "\U00002194", "\U00002714",
        "\U00002713", "\U00002705", "\U00002764", "\U00002192",
    ]) + "]"), "", 0),
    ("bullet", re.compile(r"\u2022"), "\u00b7", 0),
    ("rarr", re.compile(r"&rarr;"), "", 0),
    ("empty-span", re.compile(r"<span></span>"), "", 0),

    # 3. head design block (fonts + tailwind CDN + inline config + <style>)
    ("head",
     re.compile(
         r'<link rel="preconnect" href="https://fonts\.googleapis\.com" />\s*\n'
         r'\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin />\s*\n'
         r'\s*<link href="https://fonts\.googleapis\.com/css2\?family=Plus\+Jakarta\+Sans[^"]*" rel="stylesheet" />[\s\S]*?'
         r'<script src="https://cdn\.tailwindcss\.com"></script>[\s\S]*?</style>',
         re.DOTALL),
     NEW_HEAD, 0),

    # 4. body class
    ("body-class",
     re.compile(r'class="antialiased[^"]*flex flex-col min-h-screen"'),
     'class="antialiased flex flex-col min-h-screen"', 0),

    # 5. nav header
    ("header", re.compile(r'<header class="bg-white/95[^"]*">[\s\S]*?</header>', re.DOTALL), NEW_HEADER, 0),

    # 6. article header container + pieces
    ("art-header",
     re.compile(r'<header class="bg-white border-b border-slate-200 py-\d+ lg:py-\d+">'),
     '<header class="bg-slate-50 border-b border-slate-200 py-12 lg:py-16">', 0),
    ("breadcrumb-nav",
     re.compile(r'class="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-\d+ flex-wrap" aria-label="Breadcrumb"'),
     'class="flex items-center gap-2 text-xs font-semibold text-slate-500 mb-7 flex-wrap" aria-label="Breadcrumb"', 0),
    ("cat-badge",
     re.compile(r'<span class="bg-[a-z0-9]+-[0-9]+ text-white text-\[11px\] font-extrabold uppercase px-2\.5 py-1 rounded shadow-sm">'),
     '<span class="badge badge-dark">', 0),
    ("art-h1",
     re.compile(r'<h1 class="text-2xl sm:text-4xl lg:text-5xl font-black text-slate-950 tracking-tight leading-tight">'),
     '<h1 class="display text-3xl sm:text-4xl lg:text-[2.75rem] text-slate-950">', 0),
    ("art-lead",
     re.compile(r'<p class="mt-5 text-base sm:text-lg text-slate-600 font-normal leading-relaxed">'),
     '<p class="mt-6 text-base sm:text-lg text-slate-600 leading-relaxed">', 0),
    ("author-box",
     re.compile(r'<div class="mt-8 pt-6 border-t border-slate-100 flex items-center justify-between flex-wrap gap-4">'),
     '<div class="mt-9 pt-6 border-t border-slate-200 flex items-center gap-4">', 0),
    ("author-avatar",
     re.compile(r'<div class="w-10 h-10 rounded-full bg-[a-z0-9]+-[0-9]+ text-white font-bold flex items-center justify-center text-sm shadow">'),
     '<div class="w-11 h-11 border border-brand-700 text-brand-700 flex items-center justify-center font-serif text-sm">', 0),

    # 7. hero image -> figure (supports with/without loading, light/dark caption)
    ("hero-figure",
     re.compile(
         r'<div class="mb-10 rounded-3xl overflow-hidden shadow-lg border border-slate-200 bg-[a-z0-9-]+">\s*'
         r'(<img[^>]*/>)\s*'
         r'<div class="p-3[^"]*">\s*(.*?)\s*</div>\s*</div>',
         re.DOTALL),
     '<figure class="mb-12">\n        \\1\n        <figcaption class="mt-3 text-xs text-slate-500 text-center font-medium">\n          \\2\n        </figcaption>\n      </figure>', 0),

    # 8. takeaways
    ("takeaway-box",
     re.compile(r'<div class="bg-[a-z]+-50 border-l-4 border-[a-z]+-[0-9]+ p-6 rounded-r-2xl mb-10 shadow-sm">'),
     '<div class="takeaway mb-12">', 0),
    ("takeaway-title",
     re.compile(r'<div class="text-xs font-black uppercase text-[a-z]+-[0-9]+ tracking-wider mb-2 flex items-center gap-1\.5">'),
     '<div class="takeaway-title">', 0),
    ("takeaway-colon",
     re.compile(r'(<div class="takeaway-title">[^<]*):</div>'),
     r'\1</div>', 0),
    ("takeaway-ul",
     re.compile(r'<ul class="text-xs sm:text-sm text-slate-800 space-y-2 font-medium">'),
     '<ul>', 0),
    ("takeaway-li",
     re.compile(r'<li>\s*[\u00b7\u2022]\s*<strong>'),
     '<li><strong>', 0),

    # 9. article content wrapper
    ("content-wrap",
     re.compile(r'<div class="article-content bg-white p-6 sm:p-10 rounded-3xl border border-slate-200 shadow-sm">'),
     '<div class="article-content">', 0),

    # 10. tables
    ("table",
     re.compile(r'<table class="w-full text-left text-xs sm:text-sm border-collapse border border-slate-200[^"]*">'),
     '<table class="table-premium">', 0),
    ("tr-dark", re.compile(r'<tr class="bg-slate-900 text-white">'), '<tr>', 0),
    ("tr-dark2", re.compile(r'<tr class="bg-slate-100 text-slate-800">'), '<tr>', 0),
    ("tr-even", re.compile(r'<tr class="bg-slate-50">'), '<tr>', 0),
    ("tr-brand", re.compile(r'<tr class="bg-brand-50">'), '<tr>', 0),
    ("tr-amber", re.compile(r'<tr class="bg-amber-50">'), '<tr>', 0),
    ("th",
     re.compile(r'<th class="border border-slate-700 p-3 font-bold[^"]*">'),
     '<th>', 0),
    ("td-brand",
     re.compile(r'<td class="border border-slate-200 p-3 font-bold text-brand-800 bg-brand-50">'),
     '<td class="font-bold text-brand-700">', 0),
    ("td-amber",
     re.compile(r'<td class="border border-slate-200 p-3 font-bold text-amber-900">'),
     '<td class="font-bold text-accent-700">', 0),
    ("td-emerald",
     re.compile(r'<td class="border border-slate-200 p-3 font-black text-emerald-800">'),
     '<td class="font-bold text-brand-700">', 0),
    ("td-brand-bold",
     re.compile(r'<td class="border border-slate-200 p-3 font-bold text-brand-700">'),
     '<td class="font-bold text-brand-700">', 0),
    ("td-bold", re.compile(r'<td class="border border-slate-200 p-3 font-bold[^"]*">'), '<td class="font-bold">', 0),
    ("td-plain", re.compile(r'<td class="border border-slate-200 p-3[^"]*">'), '<td>', 0),

    # 11. in-article CTA
    ("cta-box",
     re.compile(r'<div class="mt-1[02] p-8 rounded-3xl bg-[^"]*text-white text-center space-y-4[^"]*">'),
     '<div class="cta-panel mt-12">', 0),
    ("cta-label",
     re.compile(r'<span class="bg-[a-z]+-[0-9]+ text-white text-\[11px\] font-extrabold uppercase px-3 py-1 rounded-full">|<span class="bg-accent-500 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase">'),
     '<span class="cta-label">', 0),
    ("cta-h3",
     re.compile(r'<h3 class="text-xl sm:text-2xl font-extrabold text-white !mt-2">|<h3 class="text-xl sm:text-2xl font-extrabold text-white !mt-0">|<h3 class="text-xl font-extrabold text-white !mt-0">'),
     '<h3 class="mt-3">', 0),
    ("cta-p",
     re.compile(r'<p class="text-slate-300 text-xs sm:text-sm max-w-lg mx-auto[^"]*">|<p class="text-slate-300 text-xs sm:text-sm max-w-xl mx-auto[^"]*">'),
     '<p>', 0),
    ("cta-btn",
     re.compile(
         r'<a\s+href="javascript:void\(0\)"\s+onclick="openDirectWA\(\'([^\']*)\'\)"\s+class="[^"]*">',
         re.DOTALL),
     r'<a href="javascript:void(0)" onclick="openDirectWA(\'\1\')" class="btn btn-accent">', 0),
    ("cta-link",
     re.compile(
         r'<a href="([^"]*)" class="inline-flex items-center gap-2 bg-accent-500 hover:bg-accent-600 text-slate-950 font-black text-sm px-6 py-3 rounded-xl transition-all">\s*'
         r'<span>(.*?)</span>\s*</a>',
         re.DOTALL),
     r'<a href="\1" class="btn btn-accent">\2</a>', 0),

    # 12. read next
    ("readnext-wrap",
     re.compile(
         r'<div class="mt-12">\s*<h3 class="text-lg font-bold text-slate-900 mb-4">[^<]*(?:Artikel|Baca)[^<]*</h3>\s*<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">'),
     '<div class="mt-14">\n        <span class="eyebrow"><span class="rule w-10"></span>Lanjut Membaca</span>\n        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 mt-6">', 0),
    ("readnext-card",
     re.compile(
         r'<a href="([^"]*)" class="p-5 rounded-2xl bg-white border border-slate-200 hover:border-brand-700 shadow-sm transition-all block group">\s*'
         r'<span class="text-xs font-bold text-[a-z]+-700 block mb-1">(.*?)</span>\s*'
         r'<span class="text-sm font-bold text-slate-900 group-hover:text-brand-700 transition-colors block">(.*?)</span>',
         re.DOTALL),
     r'<a href="\1" class="read-next group">\n            <div class="kicker">\2</div>\n            <div class="font-serif text-lg text-slate-900 group-hover:text-brand-700 transition-colors">\3</div>\n          </a>', 0),

    # 13. footer
    ("footer",
     re.compile(r'<footer class="bg-slate-950 text-slate-400 py-12 border-t border-slate-800 text-sm mt-12">[\s\S]*?</footer>', re.DOTALL),
     NEW_FOOTER, 0),

    # 14. floating WA
    ("wa-float",
     re.compile(r'<div class="fixed bottom-6 right-6 z-50">\s*<a[^>]*>[\s\S]*?</a>\s*</div>', re.DOTALL),
     NEW_WA, 0),

    # 15. remove old inline WA helper script
    ("inline-script",
     re.compile(r'<script>\s*function getCleanPhone\(\)[\s\S]*?</script>', re.DOTALL),
     "", 0),
]


def restyle(content, prefix=PREFIX):
    content = content.replace("__P__", prefix, 0)  # no-op guard; placeholders handled below
    counts = {}
    for label, pattern, repl, flags in RULES:
        # placeholders in replacement templates use __P__ for asset prefix
        if isinstance(repl, str):
            repl = repl.replace("__P__", prefix)
        new_content, n = pattern.subn(repl, content)
        counts[label] = n
        content = new_content
    return content, counts


def main():
    apply = "--apply" in sys.argv
    total_files = 0
    for path in sorted(FILES):
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        new_content, counts = restyle(original)
        changed = len(counts) > 0 and any(v > 0 for v in counts.values())
        total_files += 1
        rel = os.path.relpath(path, ROOT)
        touched = [k for k, v in counts.items() if v > 0]
        if apply:
            if changed and new_content != original:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print("APPLIED %-72s %s" % (rel, ", ".join(touched)))
            else:
                print("SKIP    %-72s (no change)" % rel)
        else:
            print("%-6s %-72s %s" % ("DRY", rel, ", ".join(touched) if touched else "no matches"))
    print("\nTotal files: %d" % total_files)


if __name__ == "__main__":
    main()
