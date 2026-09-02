import os
import re

articles_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\_scheduled_content\articles'
live_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\artikel'

# Mapping rule based on keywords in slug
slug_image_map = {
    # Toll / Transport / Infrastructure
    'tol-cisumdawu': 'tol-cisumdawu-jatinangor.webp',
    'kereta-cepat-whoosh': 'tol-cisumdawu-jatinangor.webp',
    'bandara-kertajati': 'tol-cisumdawu-jatinangor.webp',
    'bus-trans-metro': 'tol-cisumdawu-jatinangor.webp',
    'akses-jalan': 'tampak-samping-modern.webp',
    'tata-ruang': 'master-siteplan-jatinangor.webp',
    'peta-zona-ring-1': 'master-siteplan-jatinangor.webp',
    'bebas-banjir': 'cluster-blok-a-kost.webp',
    
    # Students / University / Demand
    'pertumbuhan-mahasiswa': 'mahasiswa-unpad-itb-jatinangor.webp',
    'kedokteran-dan-farmasi': 'mahasiswa-unpad-itb-jatinangor.webp',
    'mahasiswa-internasional': 'mahasiswa-unpad-itb-jatinangor.webp',
    'mahasiswa-pascasarjana': 'mahasiswa-unpad-itb-jatinangor.webp',
    'praja-ipdn': 'mahasiswa-unpad-itb-jatinangor.webp',
    'fasilitas-kesehatan': 'bangunan-asli-gren-kost.webp',
    'fasilitas-pendukung-kuliner': 'desain-ruang-tamu-komunal.webp',
    
    # Financial / Cashflow / Wealth
    'pasif-income-pensiun': 'pasif-income-pensiun-sejahtera.webp',
    'rental-yield': 'unit-12-kamar-fasad.webp',
    'deposito-bank': 'pasif-income-pensiun-sejahtera.webp',
    'payback-period': 'unit-12-kamar-render.webp',
    'manajemen-risiko': 'fasad-modern-flagship.webp',
    'cash-bertahap': 'fasad-modern-prespektif.webp',
    'historis-kenaikan-harga': 'fasad-modern-tropical.webp',
    'kalkulasi-keuntungan': 'unit-18-kamar-deret.webp',
    'investasi-emas': 'unit-12-kamar-tampak-depan.webp',
    'ihpr-jabar': 'fasad-modern-scandinavian.webp',
    'portofolio-multi-unit': 'unit-18-kamar-deret.webp',
    'bedah-finansial-unit-kost-18': 'unit-18-kamar-deret.webp',
    'simulasi-investasi-unit-kost-11': 'denah-arsitektur-11kamar.webp',
    'simulasi-investasi-unit-kost-12': 'denah-arsitektur-12kamar.webp',
    
    # Legal / Notary / Tax / Inheritance
    'perbandingan-apartemen': 'fasad-modern-flagship.webp',
    'panduan-legalitas-shm': 'bangunan-asli-gren-kost.webp',
    'izin-pbg-slf': 'struktur-bangunan-kokoh.webp',
    'legalitas-pbg': 'struktur-bangunan-kokoh.webp',
    'pajak-properti-sewa': 'fasad-modern-scandinavian.webp',
    'pajak-bphtb': 'fasad-modern-tropical.webp',
    'tahapan-transaksi-ajb': 'fasad-modern-flagship.webp',
    'asuransi-kebakaran': 'fasad-modern-prespektif.webp',
    'panduan-warisan': 'pasif-income-pensiun-sejahtera.webp',
    'kontrak-kerja-staf': 'desain-ruang-tamu-komunal.webp',
    'perjanjian-sewa': 'desain-ruang-tamu-komunal.webp',
    'sengketa-tanah': 'master-siteplan-jatinangor.webp',
    'checklist-audit-bangunan': 'struktur-bangunan-kokoh.webp',
    'panduan-investasi-rumah-kost-jatinangor-unpad': 'fasad-modern-flagship.webp',
    'panduan-lengkap-investasi': 'fasad-modern-flagship.webp',
    
    # Architecture / Amenities / Facilities
    'psikologi-mahasiswa-mapan': 'kamar-tidur-furnished-ac.webp',
    'sistem-autopilot': 'lorong-kamar-smart-lock.webp',
    'desain-arsitektur': 'fasad-modern-tropical.webp',
    'sop-kebersihan': 'dapur-komunal-bersih.webp',
    'sinking-fund': 'struktur-bangunan-kokoh.webp',
    'smart-door-lock': 'lorong-kamar-smart-lock.webp',
    'pemilihan-material': 'struktur-bangunan-kokoh.webp',
    'efisiensi-listrik': 'kwh-meter-token-listrik.webp',
    'desain-rooftop': 'rooftop-laundry-area.webp',
    'sistem-sirkulasi-udara': 'sirkulasi-udara-jendela.webp',
    'standar-sanitari': 'instalasi-pipa-sanitari.webp',
    'solusi-cadangan-air': 'instalasi-pipa-sanitari.webp',
    'strategi-pemasaran-digital': 'kamar-tidur-furnished-ac.webp',
    'revitalisasi-fasad': 'fasad-modern-scandinavian.webp',
    'cctv-online': 'parkir-motor-aman-cctv.webp',
    'laundry-koin': 'rooftop-laundry-area.webp'
}

def get_image_for_slug(slug):
    for key, img in slug_image_map.items():
        if key in slug:
            return img
    return 'fasad-modern-flagship.webp'

def update_html_file(file_path, is_live_folder=False):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Determine slug
    if is_live_folder:
        slug = os.path.basename(os.path.dirname(file_path))
        img_rel_path = f"../../assets/images/artikel/{get_image_for_slug(slug)}"
    else:
        slug = os.path.basename(file_path)[:-5]
        img_rel_path = f"../../assets/images/artikel/{get_image_for_slug(slug)}"
    
    assigned_img = get_image_for_slug(slug)
    full_url_img = f"https://www.gren.biz.id/assets/images/artikel/{assigned_img}"
    
    # 1. Update og:image
    html = re.sub(
        r'<meta\s+property=[\'"]og:image[\'"]\s+content=[\'"].*?[\'"]\s*/>',
        f'<meta property="og:image" content="{img_rel_path}" />',
        html,
        flags=re.IGNORECASE
    )
    
    # 2. Update twitter:image
    html = re.sub(
        r'<meta\s+name=[\'"]twitter:image[\'"]\s+content=[\'"].*?[\'"]\s*/>',
        f'<meta name="twitter:image" content="{img_rel_path}" />',
        html,
        flags=re.IGNORECASE
    )
    
    # 3. Update schema JSON-LD image
    html = re.sub(
        r'("image":\s*")https://grenpropertykost\.vercel\.app/assets/images/.*?(")',
        r'\g<1>' + full_url_img + r'\g<2>',
        html
    )
    
    # 4. Update Hero Image tag (first <img src=... after HERO IMAGE comment or in article main)
    # Replace any ../../assets/images/gallery-X.webp or old image in hero section
    html = re.sub(
        r'(<img\s+src=[\'"])\.\./\.\./assets/images/[^\'"]+([\'"]\s+alt=[\'"][^\'"]*[\'"]\s+class=[\'"]w-full h-auto max-h-\[480px\])',
        r'\g<1>' + img_rel_path + r'\g<2>',
        html
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Updated image for: {slug} -> {assigned_img}')

# Update all 55 scheduled draft articles
for f in os.listdir(articles_dir):
    if f.endswith('.html'):
        update_html_file(os.path.join(articles_dir, f), is_live_folder=False)

# Update 5 live articles
live_slugs = [
    'dampak-tol-cisumdawu-properti-jatinangor',
    'pasif-income-pensiun-properti-sewa',
    'panduan-investasi-rumah-kost-jatinangor-unpad',
    'analisis-rental-yield-dan-okupansi-kost-jatinangor',
    'perbandingan-apartemen-vs-rumah-kost-tapak-jatinangor'
]
for slug in live_slugs:
    lp = os.path.join(live_dir, slug, 'index.html')
    update_html_file(lp, is_live_folder=True)

print('\nSuccessfully updated all 60 articles with contextual custom WebP images!')
