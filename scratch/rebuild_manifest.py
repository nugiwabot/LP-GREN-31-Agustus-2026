import os
import json
import re
from datetime import datetime, timedelta

articles_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\_scheduled_content\articles'
live_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\artikel'
manifest_path = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\_scheduled_content\manifest.json'

live_slugs = [
    'dampak-tol-cisumdawu-properti-jatinangor',
    'pasif-income-pensiun-properti-sewa',
    'panduan-investasi-rumah-kost-jatinangor-unpad',
    'analisis-rental-yield-dan-okupansi-kost-jatinangor',
    'perbandingan-apartemen-vs-rumah-kost-tapak-jatinangor'
]

draft_files = sorted([f for f in os.listdir(articles_dir) if f.endswith('.html')])

def extract_meta(file_path):
    if not os.path.exists(file_path):
        return '', '', 'Investasi Properti'
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else ''
    
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
    desc = desc_match.group(1).strip() if desc_match else ''
    
    sec_match = re.search(r'<meta\s+property=["\']article:section["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE | re.DOTALL)
    sec = sec_match.group(1).strip() if sec_match else 'Investasi Properti'
    
    return title, desc, sec

all_articles = []

# 1. Add 5 Live Articles
for i, slug in enumerate(live_slugs, 1):
    file_path = os.path.join(live_dir, slug, 'index.html')
    title, desc, sec = extract_meta(file_path)
    all_articles.append({
        'id': i,
        'slug': slug,
        'status': 'published',
        'publish_date': '2026-08-31T08:00:00+07:00',
        'title': title,
        'meta_description': desc,
        'category': sec,
        'live_url': f'/artikel/{slug}'
    })

# 2. Add 55 Scheduled Draft Articles
start_date = datetime(2026, 9, 1, 8, 0, 0)
current_date = start_date

for i, df in enumerate(draft_files, 6):
    slug = df[:-5]
    file_path = os.path.join(articles_dir, df)
    title, desc, sec = extract_meta(file_path)
    
    # 2 articles per day: 08:00 and 16:00
    publish_iso = current_date.strftime('%Y-%m-%dT%H:%M:%S+07:00')
    
    all_articles.append({
        'id': i,
        'slug': slug,
        'status': 'scheduled',
        'publish_date': publish_iso,
        'title': title,
        'meta_description': desc,
        'category': sec,
        'draft_path': f'_scheduled_content/articles/{df}',
        'destination_path': f'artikel/{slug}/index.html'
    })
    
    if current_date.hour == 8:
        current_date = current_date.replace(hour=16)
    else:
        current_date = current_date + timedelta(days=1)
        current_date = current_date.replace(hour=8)

manifest_data = {
    'version': '2.0',
    'frequency': '2_posts_daily',
    'schedule_times': ['08:00 WIB', '16:00 WIB'],
    'total_articles': len(all_articles),
    'published_count': len(live_slugs),
    'scheduled_count': len(draft_files),
    'articles': all_articles
}

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest_data, f, indent=2, ensure_ascii=False)

print(f'Successfully built master manifest with {len(all_articles)} total articles!')
print(f'Live: {len(live_slugs)}, Scheduled: {len(draft_files)}')
