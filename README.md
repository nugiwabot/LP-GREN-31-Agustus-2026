# 🏰 Landing Page GREN Propertykost Jatinangor

Landing page premium, rapi, dan berkonversi tinggi (*high-converting*) untuk kampanye **Meta Ads (Facebook/Instagram)** dan **Google Ads** produk **GREN Propertykost Jatinangor**.

---

## ⚙️ Cara Mengubah Nomor WhatsApp & Pasang Pixel Iklan (SANGAT MUDAH)

Anda **TIDAK PERLU** membuka atau mengedit file `index.html`. Cukup buka file **`config.js`** di folder ini:

```javascript
window.LANDING_CONFIG = {
  // 1. Ganti dengan nomor WhatsApp penerima lead Anda (awali dengan 628, tanpa + atau spasi)
  nomorWhatsApp: "6281234567890", 

  // 2. Data Brand / Properti
  namaProperti: "GREN Propertykost Jatinangor",
  developer: "GREN Property",

  // 3. Pasang ID Tracking Iklan (Cukup isi ID di dalam tanda kutip "")
  metaPixelId: "123456789012345",       // ID Meta Pixel (Facebook Ads)
  googleAnalyticsId: "G-XXXXXXXXXX",     // ID Google Analytics 4
  googleAdsId: "AW-XXXXXXXXX",           // ID Google Ads Conversion
  tiktokPixelId: "",                     // ID TikTok Ads Pixel
};
```
Setiap kali Anda mengubah nomor WhatsApp atau Pixel ID di file `config.js`, seluruh tombol WhatsApp, form pendaftaran, dan tracking script di website akan otomatis aktif!

---

## 🖼️ Foto Properti Realistis (Standar Kamera Flagship)

Seluruh foto properti yang ada di `assets/images/` telah dimanipulasi secara fotorealistis dengan pencahayaan alami (*natural morning sunlight*), tekstur aspal/paving nyata, pohon tropis rimbun, dan pantulan kaca alami:

- `rumah-asli.jpg` & `hero-bg.webp`: Fasad tampak depan bangunan rukost.
- `gallery-1.webp` & `tipe-11-kamar.webp`: Tampak sudut arsitektur gedung 3 lantai.
- `gallery-2.webp` & `after-furnished.webp`: Interior kamar tidur full furnished.
- `gallery-3.webp`: Kamar mandi & instalasi water heater.
- `gallery-4.webp`: Koridor akses rukost.
- `tipe-9-kamar.webp`, `tipe-11-kamar.webp`, `tipe-12-kamar.webp`: Showcase tipe unit.
- `denah-9-kamar.webp`, `denah-11-kamar.webp`, `denah-12-kamar.webp`: Blueprint denah lantai.

---

## 🌐 Panduan Upload ke Hostinger / GitHub Pages

### Opsi 1: Upload ke Hostinger (cPanel / File Manager)
1. Login ke akun Hostinger Anda.
2. Buka menu **File Manager** pada domain Anda.
3. Masuk ke folder `public_html/`.
4. Upload file:
   - `index.html`
   - `config.js`
   - Folder `assets/`
5. Website Anda langsung aktif dan dapat diakses dengan domain kustom Anda!

### Opsi 2: Host via GitHub Repository
1. Push folder ini ke repositori GitHub Anda: `Landing Page GREN Propertykost Jatinangor`.
2. Anda bisa menghubungkan repositori GitHub langsung ke Hostinger (fitur Git Auto-Deploy) atau menggunakan GitHub Pages secara gratis.
