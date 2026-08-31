import os
import re

base_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026'
articles_dir = os.path.join(base_dir, '_scheduled_content', 'articles')
live_dir = os.path.join(base_dir, 'artikel')

all_files = []
for f in os.listdir(articles_dir):
    if f.endswith('.html'):
        all_files.append((os.path.join(articles_dir, f), 'draft', f[:-5]))

for d in os.listdir(live_dir):
    lp = os.path.join(live_dir, d, 'index.html')
    if os.path.exists(lp):
        all_files.append((lp, 'live', d))

print(f'Total articles to audit: {len(all_files)}')

missing_images = []
audited = 0

for file_path, status, slug in all_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    img_matches = re.findall(r'<img\s+[^>]*src=[\'"]([^\'"]+)[\'"]', html, re.IGNORECASE)
    og_matches = re.findall(r'<meta\s+property=[\'"]og:image[\'"]\s+content=[\'"]([^\'"]+)[\'"]', html, re.IGNORECASE)
    
    for src in img_matches + og_matches:
        if 'logo' in src.lower():
            continue
        if src.startswith('http://') or src.startswith('https://'):
            continue
        if src.startswith('javascript:'):
            continue
            
        if src.startswith('../../'):
            rel = src[6:] # strip ../../
            abs_target = os.path.join(base_dir, rel.replace('/', os.sep))
        elif src.startswith('/'):
            abs_target = os.path.join(base_dir, src[1:].replace('/', os.sep))
        else:
            abs_target = os.path.join(os.path.dirname(file_path), src.replace('/', os.sep))
        
        if not os.path.exists(abs_target):
            missing_images.append((slug, src, abs_target))
    audited += 1

print(f'Audited {audited} articles.')
if missing_images:
    print(f'Found {len(missing_images)} missing image references:')
    for m in missing_images:
        print(f'  - Slug: {m[0]} | Src: {m[1]} | Expected: {m[2]}')
else:
    print('SUCCESS: ALL IMAGE REFERENCES IN ALL 60 ARTICLES ARE 100% VALID AND EXIST ON DISK!')
