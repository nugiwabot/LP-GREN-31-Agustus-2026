#!/usr/bin/env python3
"""Shared helpers for GREN Propertykost SEO/site scripts.

Single source of truth for image-URL normalization, Indonesian month
formatting and read-next card normalization so the one-time fixers and the
production scheduler cannot drift apart.
"""

import re
from datetime import datetime

MONTH_NAMES_ID = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]


def to_absolute_image(value, domain="https://www.gren.biz.id"):
    """Normalize a (possibly relative) og:image path into an absolute https URL."""
    value = value.strip().strip('"')
    if not value or value.lower().startswith(("http://", "https://", "data:")):
        return value
    while value.startswith("../"):
        value = value[3:]
    value = value.lstrip("./")
    return f"{domain}/{value}"


def format_id_date(dt):
    return f"{dt.day} {MONTH_NAMES_ID[dt.month]} {dt.year}"


def display_date_from_iso(iso):
    return format_id_date(datetime.fromisoformat(iso))


# Read-next card normalization (old p-5 rounded-2xl markup -> new read-next markup)
OLD_CARD = re.compile(
    r'<a href="([^"]*)" class="p-5 rounded-2xl bg-white border border-slate-200 hover:border-brand-700 shadow-sm transition-all block group">\s*'
    r'<span class="text-xs font-bold text-[a-z0-9]+-[0-9]+ block mb-1">(.*?)</span>\s*'
    r'<span class="text-sm font-bold text-slate-900 group-hover:text-brand-700 transition-colors block">(.*?)</span>\s*'
    r'</a>',
    re.DOTALL,
)
NEW_CARD = r'<a href="\1" class="read-next group">\n            <div class="kicker">\2</div>\n            <div class="font-serif text-lg text-slate-900 group-hover:text-brand-700 transition-colors">\3</div>\n          </a>'
DUP_CLOSE = re.compile(r"</a>\s*\n\s*</a>")


def normalize_readnext_cards(content):
    """Convert legacy read-next cards to the current markup (idempotent)."""
    content = OLD_CARD.sub(NEW_CARD, content)
    content = DUP_CLOSE.sub("</a>", content)
    return content
