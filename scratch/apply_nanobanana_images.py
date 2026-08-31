import os
import re
from PIL import Image

brain_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026'
# Brain artifacts folder
artifact_dir = r'C:\Users\Nugi\.gemini\antigravity-ide\brain\728b9b4e-448f-4828-a552-b1e0d9e96147'
out_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\assets\images\artikel'
articles_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\_scheduled_content\articles'
live_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\artikel'

os.makedirs(out_dir, exist_ok=True)

# Find generated images by prefix in artifact_dir
generated_map = {
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
    'gold_vs_property': 'investasi-emas-vs-properti.webp'
}

for prefix, dest_name in generated_map.items():
    # Find matching file in artifact_dir
    matches = [f for f in os.listdir(artifact_dir) if f.startswith(prefix) and f.endswith(('.jpg', '.png'))]
    if matches:
        latest = sorted(matches)[-1]
        src_path = os.path.join(artifact_dir, latest)
        try:
            with Image.open(src_path) as img:
                img = img.convert('RGB')
                w, h = img.size
                target_w, target_h = 1280, 720
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                dest_path = os.path.join(out_dir, dest_name)
                img.save(dest_path, 'WEBP', quality=88)
                print(f'Converted & Saved: {dest_name} from {latest}')
        except Exception as e:
            print(f'Error converting {latest}: {e}')

# Now map the nanobanana generated images to matching articles
article_image_routing = {
    # AJB / Legalitas / Notaris / Warisan / Sengketa
    'tahapan-transaksi-ajb-notaris-rumah-kost': 'ajb-notaris-transaksi.webp',
    'panduan-legalitas-shm-vs-hgb-rumah-kost': 'ajb-notaris-transaksi.webp',
    'panduan-warisan-dan-hibah-properti-shm-keluarga': 'ajb-notaris-transaksi.webp',
    'kiat-menghindari-sengketa-tanah-girik-letter-c-jatinangor': 'ajb-notaris-transaksi.webp',
    'aspek-legalitas-dan-kontrak-kerja-staf-pengelola-kost': 'ajb-notaris-transaksi.webp',
    'perjanjian-sewa-dan-tata-tertib-penghuni-kost-eksklusif': 'ajb-notaris-transaksi.webp',
    
    # Smart Lock / IoT / Autopilot
    'fitur-smart-door-lock-dan-iot-keamanan-kost': 'smart-door-lock-iot.webp',
    'sistem-autopilot-operator-kost-profesional': 'smart-door-lock-iot.webp',
    
    # Rooftop / Lounge / Fasilitas Komunal
    'desain-rooftop-komunal-dan-area-laundry-gedung-kost': 'rooftop-lounge-jatinangor.webp',
    'fasilitas-pendukung-kuliner-dan-lifestyle-jatinangor': 'rooftop-lounge-jatinangor.webp',
    
    # Laundry Koin / Kafe
    'peluang-bisnis-laundry-koin-dan-cafe-komunal-di-gedung-kost': 'laundry-koin-komersial.webp',
    'sop-kebersihan-dan-maintenance-gedung-kost': 'laundry-koin-komersial.webp',
    
    # Sirkulasi Udara / Pencahayaan / Sanitari
    'sistem-sirkulasi-udara-silang-dan-kesehatan-kost': 'sirkulasi-udara-silang.webp',
    'desain-arsitektur-kost-modern-pencahayaan-alami': 'sirkulasi-udara-silang.webp',
    
    # Kamar Mandi / Sanitari / Air
    'standar-sanitari-dan-instalasi-pipa-air-anti-bocor': 'kamar-mandi-dalam-mewah.webp',
    'solusi-cadangan-air-bersih-toren-dan-ground-tank-kost': 'kamar-mandi-dalam-mewah.webp',
    'psikologi-mahasiswa-mapan-kamar-mandi-dalam-ac': 'kamar-mandi-dalam-mewah.webp',
    
    # Transportasi / Bus / Kereta Cepat / Akses
    'integrasi-bus-trans-metro-pasundan-koridor-5-jatinangor': 'bus-trans-metro-pasundan.webp',
    'dampak-kereta-cepat-whoosh-dan-feeder-tegalluar-jatinangor': 'bus-trans-metro-pasundan.webp',
    'akses-jalan-dan-jalur-pedestrian-kampus-jatinangor': 'bus-trans-metro-pasundan.webp',
    'dampak-operasional-penuh-bandara-kertajati-jatinangor': 'bus-trans-metro-pasundan.webp',
    
    # Bebas Banjir / Elevasi / Tata Ruang
    'keunggulan-lokasi-bebas-banjir-kontur-tanah-tinggi-jatinangor': 'kawasan-bebas-banjir-tinggi.webp',
    'analisis-tata-ruang-jatinangor-2030': 'kawasan-bebas-banjir-tinggi.webp',
    'peta-zona-ring-1-kampus-unpad-jatinangor': 'kawasan-bebas-banjir-tinggi.webp',
    
    # CCTV & Keamanan
    'panduan-instalasi-cctv-online-cloud-dan-keamanan-24-jam-kost': 'cctv-online-cloud-ai.webp',
    'asuransi-kebakaran-dan-bencana-gedung-kost': 'cctv-online-cloud-ai.webp',
    'manajemen-risiko-investasi-properti-sewa-miliaran': 'cctv-online-cloud-ai.webp',
    
    # Fasad Modern / Remodeling / Master
    'skema-revitalisasi-fasad-dan-remodeling-gedung-kost-tua': 'fasad-kost-modern-scandinavian.webp',
    'panduan-lengkap-investasi-properti-kost-tapak-jatinangor-2026': 'fasad-kost-modern-scandinavian.webp',
    'perbandingan-apartemen-vs-rumah-kost-tapak-jatinangor': 'fasad-kost-modern-scandinavian.webp',
    'panduan-investasi-rumah-kost-jatinangor-unpad': 'fasad-kost-modern-scandinavian.webp',
    'strategi-pemasaran-digital-kost-tiktok-dan-instagram-ads': 'fasad-kost-modern-scandinavian.webp',
    'pemilihan-material-bangunan-kost-low-maintenance': 'fasad-kost-modern-scandinavian.webp',
    'checklist-audit-bangunan-sebelum-beli-rumah-kost': 'fasad-kost-modern-scandinavian.webp',
    
    # Mahasiswa / Demografi / Kampus
    'pertumbuhan-mahasiswa-unpad-itb-permintaan-kost': 'mahasiswa-unpad-internasional.webp',
    'peluang-sewa-mahasiswa-internasional-unpad-jatinangor': 'mahasiswa-unpad-internasional.webp',
    'peluang-sewa-mahasiswa-pascasarjana-dan-dosen-unpad': 'mahasiswa-unpad-internasional.webp',
    'potensi-penyewa-praja-ipdn-dan-mahasiswa-ikopin-university': 'mahasiswa-unpad-internasional.webp',
    'perkembangan-fakultas-kedokteran-dan-farmasi-unpad': 'mahasiswa-unpad-internasional.webp',
    'fasilitas-kesehatan-dan-rumah-sakit-pendidikan-unpad': 'mahasiswa-unpad-internasional.webp',
    
    # Emas / Financial / Arus Kas / Pajak
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
    'strategi-sinking-fund-perawatan-properti-sewa': 'investasi-emas-vs-properti.webp'
}

def update_article_img(file_path):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    slug = os.path.basename(file_path)[:-5] if file_path.endswith('.html') else os.path.basename(os.path.dirname(file_path))
    assigned = article_image_routing.get(slug, 'fasad-kost-modern-scandinavian.webp')
    img_rel = f"../../assets/images/artikel/{assigned}"
    full_url = f"https://grenpropertykost.vercel.app/assets/images/artikel/{assigned}"
    
    # 1. og:image
    html = re.sub(
        r'<meta\s+property=[\'"]og:image[\'"]\s+content=[\'"].*?[\'"]\s*/>',
        f'<meta property="og:image" content="{img_rel}" />',
        html, flags=re.IGNORECASE
    )
    # 2. twitter:image
    html = re.sub(
        r'<meta\s+name=[\'"]twitter:image[\'"]\s+content=[\'"].*?[\'"]\s*/>',
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
        r'(<img\s+src=[\'"])\.\./\.\./assets/images/.*?([\'"]\s+alt=[\'"][^\'"]*[\'"]\s+class=[\'"]w-full h-auto max-h-\[480px\])',
        r'\g<1>' + img_rel + r'\g<2>',
        html
    )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Applied nanobanana image: {slug} -> {assigned}')

# Process scheduled articles
for f in os.listdir(articles_dir):
    if f.endswith('.html'):
        update_article_img(os.path.join(articles_dir, f))

# Process live articles
live_slugs = [
    'dampak-tol-cisumdawu-properti-jatinangor',
    'pasif-income-pensiun-properti-sewa',
    'panduan-investasi-rumah-kost-jatinangor-unpad',
    'analisis-rental-yield-dan-okupansi-kost-jatinangor',
    'perbandingan-apartemen-vs-rumah-kost-tapak-jatinangor'
]
for slug in live_slugs:
    lp = os.path.join(live_dir, slug, 'index.html')
    update_article_img(lp)

print('\nSuccessfully updated all articles with generated nanobanana images!')
