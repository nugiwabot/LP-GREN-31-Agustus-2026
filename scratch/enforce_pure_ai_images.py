import os
import re

base_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026'
artikel_img_dir = os.path.join(base_dir, 'assets', 'images', 'artikel')
articles_dir = os.path.join(base_dir, '_scheduled_content', 'articles')
live_dir = os.path.join(base_dir, 'artikel')

# The 12 ONLY allowed pure AI-generated (nanobanana) images
allowed_ai_images = {
    'ajb-notaris-transaksi.webp',
    'bus-trans-metro-pasundan.webp',
    'cctv-online-cloud-ai.webp',
    'sirkulasi-udara-silang.webp',
    'kawasan-bebas-banjir-tinggi.webp',
    'investasi-emas-vs-properti.webp',
    'mahasiswa-unpad-internasional.webp',
    'laundry-koin-komersial.webp',
    'kamar-mandi-dalam-mewah.webp',
    'fasad-kost-modern-scandinavian.webp',
    'rooftop-lounge-jatinangor.webp',
    'smart-door-lock-iot.webp'
}

# 1. Delete any file in assets/images/artikel that is NOT in allowed_ai_images
for f in os.listdir(artikel_img_dir):
    if f not in allowed_ai_images:
        fp = os.path.join(artikel_img_dir, f)
        os.remove(fp)
        print(f'Deleted non-AI image: {f}')

print(f'\nRemaining pure AI images in assets/images/artikel/: {len(os.listdir(artikel_img_dir))}')
for f in sorted(os.listdir(artikel_img_dir)):
    print(f'  - {f}')

# 2. Strict Mapping for all 60 articles to ONLY these 12 pure AI images
category_ai_map = {
    # Legal / Notary / SHM / Inheritance / Contracts / Dispute
    'ajb': 'ajb-notaris-transaksi.webp',
    'notaris': 'ajb-notaris-transaksi.webp',
    'shm': 'ajb-notaris-transaksi.webp',
    'warisan': 'ajb-notaris-transaksi.webp',
    'hibah': 'ajb-notaris-transaksi.webp',
    'sengketa': 'ajb-notaris-transaksi.webp',
    'perjanjian-sewa': 'ajb-notaris-transaksi.webp',
    'kontrak-kerja': 'ajb-notaris-transaksi.webp',
    
    # Smart Lock / IoT / Autopilot
    'smart-door-lock': 'smart-door-lock-iot.webp',
    'autopilot': 'smart-door-lock-iot.webp',
    
    # Rooftop / Lounge / Community / Lifestyle
    'rooftop': 'rooftop-lounge-jatinangor.webp',
    'kuliner': 'rooftop-lounge-jatinangor.webp',
    'lifestyle': 'rooftop-lounge-jatinangor.webp',
    
    # Laundry Koin / Maintenance / SOP
    'laundry-koin': 'laundry-koin-komersial.webp',
    'sop-kebersihan': 'laundry-koin-komersial.webp',
    
    # Air Circulation / Windows / Architecture
    'sirkulasi-udara': 'sirkulasi-udara-silang.webp',
    'pencahayaan': 'sirkulasi-udara-silang.webp',
    
    # Bathroom / Water Tank / Sanitary
    'kamar-mandi': 'kamar-mandi-dalam-mewah.webp',
    'sanitari': 'kamar-mandi-dalam-mewah.webp',
    'cadangan-air': 'kamar-mandi-dalam-mewah.webp',
    'air-bersih': 'kamar-mandi-dalam-mewah.webp',
    
    # Transport / Bus / Tol / Kereta Cepat / Bandara / Akses
    'trans-metro': 'bus-trans-metro-pasundan.webp',
    'bus': 'bus-trans-metro-pasundan.webp',
    'whoosh': 'bus-trans-metro-pasundan.webp',
    'kereta-cepat': 'bus-trans-metro-pasundan.webp',
    'cisumdawu': 'bus-trans-metro-pasundan.webp',
    'tol': 'bus-trans-metro-pasundan.webp',
    'kertajati': 'bus-trans-metro-pasundan.webp',
    'bandara': 'bus-trans-metro-pasundan.webp',
    'pedestrian': 'bus-trans-metro-pasundan.webp',
    'akses-jalan': 'bus-trans-metro-pasundan.webp',
    
    # Flood Free / Elevation / Master Plan / Zoning
    'bebas-banjir': 'kawasan-bebas-banjir-tinggi.webp',
    'tata-ruang': 'kawasan-bebas-banjir-tinggi.webp',
    'ring-1': 'kawasan-bebas-banjir-tinggi.webp',
    'zona-ring': 'kawasan-bebas-banjir-tinggi.webp',
    
    # CCTV / Security / Risk / Insurance
    'cctv': 'cctv-online-cloud-ai.webp',
    'keamanan': 'cctv-online-cloud-ai.webp',
    'asuransi': 'cctv-online-cloud-ai.webp',
    'manajemen-risiko': 'cctv-online-cloud-ai.webp',
    
    # Students / University / Demand / Medicine / IPDN / International
    'pertumbuhan-mahasiswa': 'mahasiswa-unpad-internasional.webp',
    'kedokteran': 'mahasiswa-unpad-internasional.webp',
    'farmasi': 'mahasiswa-unpad-internasional.webp',
    'internasional': 'mahasiswa-unpad-internasional.webp',
    'pascasarjana': 'mahasiswa-unpad-internasional.webp',
    'ipdn': 'mahasiswa-unpad-internasional.webp',
    'ikopin': 'mahasiswa-unpad-internasional.webp',
    'kesehatan': 'mahasiswa-unpad-internasional.webp',
    'rumah-sakit': 'mahasiswa-unpad-internasional.webp',
    
    # Financial / Gold / Cashflow / Taxes / Yield / Payback / Sinking Fund
    'emas': 'investasi-emas-vs-properti.webp',
    'deposito': 'investasi-emas-vs-properti.webp',
    'reksadana': 'investasi-emas-vs-properti.webp',
    'cashflow': 'investasi-emas-vs-properti.webp',
    'rental-yield': 'investasi-emas-vs-properti.webp',
    'payback': 'investasi-emas-vs-properti.webp',
    'pajak': 'investasi-emas-vs-properti.webp',
    'bphtb': 'investasi-emas-vs-properti.webp',
    'cash-bertahap': 'investasi-emas-vs-properti.webp',
    'ihpr': 'investasi-emas-vs-properti.webp',
    'kenaikan-harga': 'investasi-emas-vs-properti.webp',
    'sinking-fund': 'investasi-emas-vs-properti.webp',
    'pasif-income': 'investasi-emas-vs-properti.webp',
    'pensiun': 'investasi-emas-vs-properti.webp',
    
    # Architecture / Facade / Building / Audit / PBG / Master
    'fasad': 'fasad-kost-modern-scandinavian.webp',
    'remodeling': 'fasad-kost-modern-scandinavian.webp',
    'pbg': 'fasad-kost-modern-scandinavian.webp',
    'audit-bangunan': 'fasad-kost-modern-scandinavian.webp',
    'material': 'fasad-kost-modern-scandinavian.webp',
    'pemasaran-digital': 'fasad-kost-modern-scandinavian.webp',
    'token-prabayar': 'fasad-kost-modern-scandinavian.webp',
    'listrik': 'fasad-kost-modern-scandinavian.webp',
    'simulasi-investasi': 'fasad-kost-modern-scandinavian.webp',
    'portofolio': 'fasad-kost-modern-scandinavian.webp',
    'apartemen': 'fasad-kost-modern-scandinavian.webp',
    'panduan-investasi': 'fasad-kost-modern-scandinavian.webp',
    'panduan-lengkap': 'fasad-kost-modern-scandinavian.webp'
}

def resolve_ai_image(slug):
    slug_lower = slug.lower()
    for kw, img in category_ai_map.items():
        if kw in slug_lower:
            return img
    return 'fasad-kost-modern-scandinavian.webp'

def update_file(file_path, slug):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    ai_img = resolve_ai_image(slug)
    img_rel = f"../../assets/images/artikel/{ai_img}"
    full_url = f"https://www.gren.biz.id/assets/images/artikel/{ai_img}"
    
    # 1. og:image
    html = re.sub(
        r'<meta\s+property=[\'"]og:image[\'"]\s+content=[\'"][^\'"]*[\'"]\s*/>',
        f'<meta property="og:image" content="{img_rel}" />',
        html, flags=re.IGNORECASE
    )
    # 2. twitter:image
    html = re.sub(
        r'<meta\s+name=[\'"]twitter:image[\'"]\s+content=[\'"][^\'"]*[\'"]\s*/>',
        f'<meta name="twitter:image" content="{img_rel}" />',
        html, flags=re.IGNORECASE
    )
    # 3. JSON-LD schema
    html = re.sub(
        r'("image":\s*")https://grenpropertykost\.vercel\.app/assets/images/.*?(")',
        r'\g<1>' + full_url + r'\g<2>',
        html
    )
    # 4. Hero <img>
    html = re.sub(
        r'(<img\s+[^>]*src=[\'"])\.\./\.\./assets/images/[^\'"]*([\'"][^>]*class=[\'"]w-full h-auto max-h-\[480px\])',
        r'\g<1>' + img_rel + r'\g<2>',
        html
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Updated {slug} -> {ai_img}')

# 3. Update all 55 scheduled articles
for f in os.listdir(articles_dir):
    if f.endswith('.html'):
        slug = f[:-5]
        update_file(os.path.join(articles_dir, f), slug)

# 4. Update 5 live articles
live_slugs = [
    'dampak-tol-cisumdawu-properti-jatinangor',
    'pasif-income-pensiun-properti-sewa',
    'panduan-investasi-rumah-kost-jatinangor-unpad',
    'analisis-rental-yield-dan-okupansi-kost-jatinangor',
    'perbandingan-apartemen-vs-rumah-kost-tapak-jatinangor'
]
for slug in live_slugs:
    lp = os.path.join(live_dir, slug, 'index.html')
    if os.path.exists(lp):
        update_file(lp, slug)

print('\nALL 60 ARTICLES ARE NOW STRICTLY USING ONLY PURE AI-GENERATED (NANOBANANA) IMAGES!')
