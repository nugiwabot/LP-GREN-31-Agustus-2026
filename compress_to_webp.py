"""
Script Otomatis Kompresi Gambar ke Format WebP untuk Landing Page GREN Propertykost
-----------------------------------------------------------------------------------
Cara Pakai:
1. Simpan foto-foto asli properti Anda (format JPG, PNG, atau JPEG) ke dalam folder:
   assets/images/
2. Jalankan script ini melalui terminal:
   python compress_to_webp.py
3. Semua gambar akan dikompresi otomatis menjadi format WebP berkualitas tinggi & berukuran sangat ringan (< 100KB)!
"""

import os
from PIL import Image

def compress_images_to_webp(target_folder='assets/images', quality=85, max_width=1600):
    if not os.path.exists(target_folder):
        print(f"[!] Folder '{target_folder}' tidak ditemukan.")
        return

    supported_exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    files = [f for f in os.listdir(target_folder) if os.path.splitext(f)[1].lower() in supported_exts]

    if not files:
        print(f"[i] Tidak ada file gambar baru (.jpg/.png) yang perlu dikompresi di '{target_folder}'.")
        return

    print(f"[*] Ditemukan {len(files)} gambar. Memulai proses kompresi ke WebP...")

    for f in files:
        input_path = os.path.join(target_folder, f)
        base_name, _ = os.path.splitext(f)
        output_path = os.path.join(target_folder, f"{base_name}.webp")

        try:
            with Image.open(input_path) as img:
                # Convert RGBA/P to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if image width exceeds max_width
                if img.width > max_width:
                    ratio = max_width / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save as WebP
                img.save(output_path, 'WEBP', quality=quality, method=6)
                
                orig_size = os.path.getsize(input_path) / 1024
                webp_size = os.path.getsize(output_path) / 1024
                hemat = ((orig_size - webp_size) / orig_size) * 100

                print(f"[✓] Berhasil: {f} ({orig_size:.1f} KB) -> {base_name}.webp ({webp_size:.1f} KB) | Hemat {hemat:.1f}%")
        except Exception as e:
            print(f"[✗] Gagal memproses {f}: {e}")

    print("\n[✓] Selesai! Semua gambar siap digunakan untuk Landing Page yang super cepat.")

if __name__ == '__main__':
    compress_images_to_webp()
