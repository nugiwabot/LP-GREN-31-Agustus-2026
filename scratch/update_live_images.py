import os
import re

live_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\artikel'

live_map = {
    'dampak-tol-cisumdawu-properti-jatinangor': 'bus-trans-metro-pasundan.webp',
    'pasif-income-pensiun-properti-sewa': 'investasi-emas-vs-properti.webp',
    'panduan-investasi-rumah-kost-jatinangor-unpad': 'fasad-kost-modern-scandinavian.webp',
    'analisis-rental-yield-dan-okupansi-kost-jatinangor': 'investasi-emas-vs-properti.webp',
    'perbandingan-apartemen-vs-rumah-kost-tapak-jatinangor': 'fasad-kost-modern-scandinavian.webp'
}

for slug, assigned in live_map.items():
    file_path = os.path.join(live_dir, slug, 'index.html')
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    img_rel = f"../../assets/images/artikel/{assigned}"
    full_url = f"https://grenpropertykost.vercel.app/assets/images/artikel/{assigned}"
    
    html = re.sub(
        r'<meta\s+property=[\'"]og:image[\'"]\s+content=[\'"].*?[\'"]\s*/>',
        f'<meta property="og:image" content="{img_rel}" />',
        html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'<meta\s+name=[\'"]twitter:image[\'"]\s+content=[\'"].*?[\'"]\s*/>',
        f'<meta name="twitter:image" content="{img_rel}" />',
        html, flags=re.IGNORECASE
    )
    html = re.sub(
        r'("image":\s*")https://grenpropertykost\.vercel\.app/assets/images/.*?(")',
        r'\g<1>' + full_url + r'\g<2>',
        html
    )
    html = re.sub(
        r'(<img\s+src=[\'"])\.\./\.\./assets/images/.*?([\'"]\s+alt=[\'"][^\'"]*[\'"]\s+class=[\'"]w-full h-auto max-h-\[480px\])',
        r'\g<1>' + img_rel + r'\g<2>',
        html
    )
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Correctly updated live article: {slug} -> {assigned}')

print('Live articles updated!')
