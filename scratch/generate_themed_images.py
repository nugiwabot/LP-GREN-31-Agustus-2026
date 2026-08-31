import os
import re
from PIL import Image

ref_dir = r'c:\Users\Nugi\Documents\Memori-Konten-Kreator-2\Markom & Digital Skill\Image Reference'
art_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\assets\images'
out_dir = r'c:\Users\Nugi\Documents\LP-GREN-31-Agustus-2026\assets\images\artikel'

os.makedirs(out_dir, exist_ok=True)

def crop_and_save_webp(src_path, dest_filename, max_width=1280):
    if not os.path.exists(src_path):
        print(f'Warning: {src_path} not found.')
        return False
    try:
        with Image.open(src_path) as img:
            img = img.convert('RGB')
            w, h = img.size
            
            # Target 16:9 aspect ratio crop
            target_aspect = 16.0 / 9.0
            current_aspect = w / h
            
            if current_aspect > target_aspect:
                # Too wide -> crop width
                new_w = int(h * target_aspect)
                left = (w - new_w) // 2
                img = img.crop((left, 0, left + new_w, h))
            elif current_aspect < target_aspect:
                # Too tall -> crop height (keep top/center)
                new_h = int(w / target_aspect)
                top = int((h - new_h) * 0.3) # 30% from top
                img = img.crop((0, top, w, top + new_h))
            
            # Resize if larger than max_width
            if img.width > max_width:
                new_height = int(max_width * 9 / 16)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            dest_path = os.path.join(out_dir, dest_filename)
            img.save(dest_path, 'WEBP', quality=85)
            print(f'Created: {dest_filename} ({img.size})')
            return True
    except Exception as e:
        print(f'Error processing {src_path}: {e}')
        return False

# 1. Process and generate diverse themed WebP images
images_to_create = [
    (os.path.join(ref_dir, 'FASAD UPDATE 2.png'), 'fasad-modern-flagship.webp'),
    (os.path.join(ref_dir, 'FASAD UPDATE 3.png'), 'fasad-modern-prespektif.webp'),
    (os.path.join(ref_dir, 'FASAD UPDATE 4.png'), 'fasad-modern-tropical.webp'),
    (os.path.join(ref_dir, 'FASAD UPDATE 5.png'), 'fasad-modern-scandinavian.webp'),
    (os.path.join(ref_dir, 'Blok A (1).png'), 'cluster-blok-a-kost.webp'),
    (os.path.join(ref_dir, 'Rukost 3 lantai 12 kamar (1).png'), 'unit-12-kamar-render.webp'),
    (os.path.join(ref_dir, 'Rukost 3 lantai 12 kamar (2).png'), 'unit-12-kamar-fasad.webp'),
    (os.path.join(ref_dir, 'Rukost 3 lantai 12 kamar (3).png'), 'unit-12-kamar-tampak-depan.webp'),
    (os.path.join(ref_dir, 'Rukost 3 lantai 12 kamar - berderet panjang.png'), 'unit-18-kamar-deret.webp'),
    (os.path.join(ref_dir, 'siteplan-render-hd.jpg'), 'master-siteplan-jatinangor.webp'),
    (os.path.join(ref_dir, '1.png'), 'desain-ruang-tamu-komunal.webp'),
    (os.path.join(ref_dir, '2.png'), 'lorong-kamar-smart-lock.webp'),
    (os.path.join(ref_dir, '4.png'), 'tampak-samping-modern.webp'),
    (os.path.join(ref_dir, 'Gambar (1).jpg'), 'kamar-tidur-furnished-ac.webp'),
    (os.path.join(ref_dir, 'Gambar (2).jpg'), 'kamar-mandi-dalam-shower.webp'),
    (os.path.join(ref_dir, 'Gambar (3).jpg'), 'area-belajar-meja-kerja.webp'),
    (os.path.join(ref_dir, 'Gambar (4).jpg'), 'dapur-komunal-bersih.webp'),
    (os.path.join(ref_dir, 'Gambar (5).jpg'), 'parkir-motor-aman-cctv.webp'),
    (os.path.join(ref_dir, 'Gambar (9).jpg'), 'instalasi-pipa-sanitari.webp'),
    (os.path.join(ref_dir, 'Gambar (10).jpg'), 'sirkulasi-udara-jendela.webp'),
    (os.path.join(ref_dir, 'Gambar (19).jpg'), 'rooftop-laundry-area.webp'),
    (os.path.join(ref_dir, 'Gambar (20).jpg'), 'kwh-meter-token-listrik.webp'),
    (os.path.join(ref_dir, 'Gambar (21).jpg'), 'struktur-bangunan-kokoh.webp'),
    (os.path.join(ref_dir, 'Gambar (22).jpg'), 'pencahayaan-alami-tangga.webp'),
    (os.path.join(art_dir, 'after-furnished.webp'), 'interior-kamar-eksklusif.webp'),
    (os.path.join(art_dir, 'tol-cisumdawu-jatinangor.jpg'), 'tol-cisumdawu-jatinangor.webp'),
    (os.path.join(art_dir, 'pertumbuhan-unpad-itb.jpg'), 'mahasiswa-unpad-itb-jatinangor.webp'),
    (os.path.join(art_dir, 'pensiun-passive-income.jpg'), 'pasif-income-pensiun-sejahtera.webp'),
    (os.path.join(art_dir, 'rumah-asli.jpg'), 'bangunan-asli-gren-kost.webp'),
    (os.path.join(art_dir, 'denah-12-kamar.webp'), 'denah-arsitektur-12kamar.webp'),
    (os.path.join(art_dir, 'denah-11-kamar.webp'), 'denah-arsitektur-11kamar.webp'),
]

for src, dst in images_to_create:
    crop_and_save_webp(src, dst)

print('\nAll themed WebP images generated successfully in assets/images/artikel/!')
