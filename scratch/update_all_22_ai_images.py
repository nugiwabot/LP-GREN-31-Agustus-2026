import os
import re
import shutil
from PIL import Image

base_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026'
artifact_dir = r'C:\Users\Nugi\.gemini\antigravity-ide\brain\728b9b4e-448f-4828-a552-b1e0d9e96147'
out_webp_dir = os.path.join(base_dir, 'assets', 'images', 'artikel')
raw_dest_dir = os.path.join(base_dir, 'assets', 'images', 'raw_generated')
articles_dir = os.path.join(base_dir, '_scheduled_content', 'articles')
live_dir = os.path.join(base_dir, 'artikel')

os.makedirs(out_webp_dir, exist_ok=True)
os.makedirs(raw_dest_dir, exist_ok=True)

# Master prefix to webp mapping
all_ai_generated = {
    'ajb_notaris_legal': 'ajb-notaris-transaksi.webp',
    'smart_lock_door': 'smart-door-lock-iot.webp',
    'rooftop_lounge_sunset': 'rooftop-lounge-jatinangor.webp',
    'laundry_koin_modern': 'laundry-koin-komersial.webp',
    'cross_ventilation_room': 'sirkulasi-udara-silang.webp',
    'luxury_ensuite_bathroom': 'kamar-mandi-dalam-mewah.webp',
    'bus_trans_metro': 'bus-trans-metro-pasundan.webp',
    'elevated_flood_free': 'kawasan-bebas-banjir-tinggi.webp',
    'cctv_ip_security': 'cctv-online-cloud-ai.webp',
    'modern_facade_kost': 'fasad-kost-modern-scandinavian.webp',
    'international_students': 'mahasiswa-unpad-internasional.webp',
    'gold_vs_property': 'investasi-emas-vs-properti.webp',
    'unpad_hospital_facade': 'rumah-sakit-pendidikan-unpad.webp',
    'prepaid_kwh_meter_box': 'meteran-listrik-token-prabayar.webp',
    'ipdn_praja_parade': 'praja-ipdn-kampus-jatinangor.webp',
    'whoosh_fast_train_station': 'kereta-cepat-whoosh-jatinangor.webp',
    'culinary_cafe_lifestyle': 'kuliner-kafe-lifestyle-mahasiswa.webp',
    'sinking_fund_maintenance': 'manajemen-maintenance-gedung.webp',
    'clean_water_filtration_tank': 'toren-air-ground-tank-filtrasi.webp',
    'pedestrian_walkway_campus': 'jalur-pedestrian-kampus-unpad.webp',
    'study_room_interior_desk': 'kamar-kost-meja-belajar-ac.webp',
    'shm_land_certificate_book': 'buku-sertifikat-shm-asli.webp'
}

# 1. Convert and Save all 22 WebP & Raw JPEGs
for prefix, webp_name in all_ai_generated.items():
    matches = [f for f in os.listdir(artifact_dir) if f.startswith(prefix) and f.endswith(('.jpg', '.png'))]
    if matches:
        latest = sorted(matches)[-1]
        src_path = os.path.join(artifact_dir, latest)
        
        # Save raw master
        shutil.copy2(src_path, os.path.join(raw_dest_dir, latest))
        
        # Convert to 16:9 WebP
        try:
            with Image.open(src_path) as img:
                img = img.convert('RGB')
                w, h = img.size
                target_w, target_h = 1280, 720
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                dest_path = os.path.join(out_webp_dir, webp_name)
                img.save(dest_path, 'WEBP', quality=88)
                print(f'Processed & Saved: {webp_name}')
        except Exception as e:
            print(f'Error processing {latest}: {e}')

# 2. Granular Topic Matching for all 60 articles
topic_to_image = {
    # Legal / Notary / SHM / Inheritance / Contracts / Dispute
    'tahapan-transaksi-ajb-notaris-rumah-kost': 'ajb-notaris-transaksi.webp',
    'panduan-legalitas-shm-vs-hgb-rumah-kost': 'buku-sertifikat-shm-asli.webp',
    'panduan-warisan-dan-hibah-properti-shm-keluarga': 'buku-sertifikat-shm-asli.webp',
    'kiat-menghindari-sengketa-tanah-girik-letter-c-jatinangor': 'buku-sertifikat-shm-asli.webp',
    'aspek-legalitas-dan-kontrak-kerja-staf-pengelola-kost': 'ajb-notaris-transaksi.webp',
    'perjanjian-sewa-dan-tata-tertib-penghuni-kost-eksklusif': 'ajb-notaris-transaksi.webp',
    'legalitas-pbg-bangunan-kost-bertingkat-sumedang': 'buku-sertifikat-shm-asli.webp',
    'izin-pbg-slf-rumah-kost-pemda-sumedang': 'buku-sertifikat-shm-asli.webp',
    'checklist-audit-bangunan-sebelum-beli-rumah-kost': 'manajemen-maintenance-gedung.webp',
    'pemilihan-material-bangunan-kost-low-maintenance': 'manajemen-maintenance-gedung.webp',
    
    # Smart Lock / IoT / Autopilot
    'fitur-smart-door-lock-dan-iot-keamanan-kost': 'smart-door-lock-iot.webp',
    'sistem-autopilot-operator-kost-profesional': 'smart-door-lock-iot.webp',
    
    # Rooftop / Lounge / Culinary / Lifestyle
    'desain-rooftop-komunal-dan-area-laundry-gedung-kost': 'rooftop-lounge-jatinangor.webp',
    'fasilitas-pendukung-kuliner-dan-lifestyle-jatinangor': 'kuliner-kafe-lifestyle-mahasiswa.webp',
    
    # Laundry Koin / Maintenance / Sinking Fund
    'peluang-bisnis-laundry-koin-dan-cafe-komunal-di-gedung-kost': 'laundry-koin-komersial.webp',
    'sop-kebersihan-dan-maintenance-gedung-kost': 'manajemen-maintenance-gedung.webp',
    'strategi-sinking-fund-perawatan-properti-sewa': 'manajemen-maintenance-gedung.webp',
    
    # Sirkulasi Udara / Pencahayaan / Kamar Tidur Furnished
    'sistem-sirkulasi-udara-silang-dan-kesehatan-kost': 'sirkulasi-udara-silang.webp',
    'desain-arsitektur-kost-modern-pencahayaan-alami': 'sirkulasi-udara-silang.webp',
    'psikologi-mahasiswa-mapan-kamar-mandi-dalam-ac': 'kamar-kost-meja-belajar-ac.webp',
    'strategi-pemasaran-digital-kost-tiktok-dan-instagram-ads': 'kamar-kost-meja-belajar-ac.webp',
    
    # Kamar Mandi / Air Bersih / Sanitari
    'standar-sanitari-dan-instalasi-pipa-air-anti-bocor': 'kamar-mandi-dalam-mewah.webp',
    'solusi-cadangan-air-bersih-toren-dan-ground-tank-kost': 'toren-air-ground-tank-filtrasi.webp',
    
    # Transport / Bus / Whoosh / Kereta / Tol / Pedestrian / Bandara
    'integrasi-bus-trans-metro-pasundan-koridor-5-jatinangor': 'bus-trans-metro-pasundan.webp',
    'dampak-kereta-cepat-whoosh-dan-feeder-tegalluar-jatinangor': 'kereta-cepat-whoosh-jatinangor.webp',
    'akses-jalan-dan-jalur-pedestrian-kampus-jatinangor': 'jalur-pedestrian-kampus-unpad.webp',
    'dampak-operasional-penuh-bandara-kertajati-jatinangor': 'kereta-cepat-whoosh-jatinangor.webp',
    'dampak-tol-cisumdawu-properti-jatinangor': 'bus-trans-metro-pasundan.webp',
    
    # Bebas Banjir / Topografi / Tata Ruang / Ring 1
    'keunggulan-lokasi-bebas-banjir-kontur-tanah-tinggi-jatinangor': 'kawasan-bebas-banjir-tinggi.webp',
    'analisis-tata-ruang-jatinangor-2030': 'kawasan-bebas-banjir-tinggi.webp',
    'peta-zona-ring-1-kampus-unpad-jatinangor': 'kawasan-bebas-banjir-tinggi.webp',
    
    # CCTV & Keamanan / Asuransi / Risiko
    'panduan-instalasi-cctv-online-cloud-dan-keamanan-24-jam-kost': 'cctv-online-cloud-ai.webp',
    'asuransi-kebakaran-dan-bencana-gedung-kost': 'cctv-online-cloud-ai.webp',
    'manajemen-risiko-investasi-properti-sewa-miliaran': 'cctv-online-cloud-ai.webp',
    
    # Mahasiswa / Kampus / Kedokteran / IPDN / Kesehatan
    'pertumbuhan-mahasiswa-unpad-itb-permintaan-kost': 'mahasiswa-unpad-internasional.webp',
    'peluang-sewa-mahasiswa-internasional-unpad-jatinangor': 'mahasiswa-unpad-internasional.webp',
    'peluang-sewa-mahasiswa-pascasarjana-dan-dosen-unpad': 'mahasiswa-unpad-internasional.webp',
    'potensi-penyewa-praja-ipdn-dan-mahasiswa-ikopin-university': 'praja-ipdn-kampus-jatinangor.webp',
    'perkembangan-fakultas-kedokteran-dan-farmasi-unpad': 'rumah-sakit-pendidikan-unpad.webp',
    'fasilitas-kesehatan-dan-rumah-sakit-pendidikan-unpad': 'rumah-sakit-pendidikan-unpad.webp',
    
    # Listrik & Token
    'efisiensi-listrik-token-prabayar-per-kamar-kost': 'meteran-listrik-token-prabayar.webp',
    
    # Finansial / Emas / Yield / Arus Kas / Pensiun / Pajak / Deposito
    'investasi-emas-antam-vs-rumah-kost-tapak-jatinangor': 'investasi-emas-vs-properti.webp',
    'kalkulasi-keuntungan-properti-tapak-vs-reksadana': 'investasi-emas-vs-properti.webp',
    'mengapa-deposito-bank-kalah-lawan-inflasi': 'investasi-emas-vs-properti.webp',
    'bedah-finansial-unit-kost-18-kamar-cashflow': 'investasi-emas-vs-properti.webp',
    'analisis-rental-yield-dan-okupansi-kost-jatinangor': 'investasi-emas-vs-properti.webp',
    'menghitung-payback-period-bisnis-kost-tapak': 'investasi-emas-vs-properti.webp',
    'pajak-properti-sewa-pph-final-dan-pbb-rumah-kost': 'investasi-emas-vs-properti.webp',
    'panduan-pajak-bphtb-dan-npop-kabupaten-sumedang': 'investasi-emas-vs-properti.webp',
    'skema-pembayaran-cash-bertahap-developer-bebas-bunga': 'investasi-emas-vs-properti.webp',
    'historis-kenaikan-harga-tanah-jatinangor-10-tahun': 'investasi-emas-vs-properti.webp',
    'analisis-pertumbuhan-indeks-harga-properti-residensial-ihpr-jabar': 'investasi-emas-vs-properti.webp',
    'pasif-income-pensiun-properti-sewa': 'investasi-emas-vs-properti.webp',
    
    # Fasad Modern / Simulasi Unit / Remodeling / Master Guide
    'skema-revitalisasi-fasad-dan-remodeling-gedung-kost-tua': 'fasad-kost-modern-scandinavian.webp',
    'panduan-lengkap-investasi-properti-kost-tapak-jatinangor-2026': 'fasad-kost-modern-scandinavian.webp',
    'perbandingan-apartemen-vs-rumah-kost-tapak-jatinangor': 'fasad-kost-modern-scandinavian.webp',
    'panduan-investasi-rumah-kost-jatinangor-unpad': 'fasad-kost-modern-scandinavian.webp',
    'simulasi-investasi-unit-kost-11-kamar-unpad': 'fasad-kost-modern-scandinavian.webp',
    'simulasi-investasi-unit-kost-12-kamar-unpad': 'fasad-kost-modern-scandinavian.webp',
    'simulasi-portofolio-multi-unit-kost-keluarga': 'fasad-kost-modern-scandinavian.webp'
}

def update_article_html(file_path, slug):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    img_name = topic_to_image.get(slug, 'fasad-kost-modern-scandinavian.webp')
    img_rel = f"../../assets/images/artikel/{img_name}"
    full_url = f"https://www.gren.biz.id/assets/images/artikel/{img_name}"
    
    html = re.sub(
        r'<meta\s+property=[\'"]og:image[\'"]\s+content=[\'"][^\'"]*[\'"]\s*/>',
        f'<meta property="og:image" content="{img_rel}" />',
        html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'<meta\s+name=[\'"]twitter:image[\'"]\s+content=[\'"][^\'"]*[\'"]\s*/>',
        f'<meta name="twitter:image" content="{img_rel}" />',
        html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'("image":\s*")https://grenpropertykost\.vercel\.app/assets/images/.*?(")',
        r'\g<1>' + full_url + r'\g<2>',
        html
    )
    html = re.sub(
        r'(<img\s+[^>]*src=[\'"])\.\./\.\./assets/images/[^\'"]*([\'"][^>]*class=[\'"]w-full h-auto max-h-\[480px\])',
        r'\g<1>' + img_rel + r'\g<2>',
        html
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Article [{slug}] -> {img_name}')

# 3. Update all 55 scheduled articles
for f in os.listdir(articles_dir):
    if f.endswith('.html'):
        slug = f[:-5]
        update_article_html(os.path.join(articles_dir, f), slug)

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
        update_article_html(lp, slug)

print('\nSuccessfully updated all 60 articles with 22 tailored pure AI images!')
