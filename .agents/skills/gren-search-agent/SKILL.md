---
name: gren-search-agent
description: AI Market Search & Content Automation Agent for GREN Propertykost Jatinangor. Searches Google Custom Search, embeds and reranks via local models, and generates publication-ready SEO AI articles into /artikel/.
---

# GREN Propertykost - AI Market Search & Content Agent

Gunakan skill ini secara proaktif setiap kali pengguna meminta:
- Mencari tren pasar, berita properti, atau dinamika sewa mahasiswa Jatinangor (Ring-1 UNPAD/ITB/IPDN/IKOPIN).
- Melakukan pencarian data terverifikasi via Google Custom Search API & Google CX.
- Menjalankan embedding dan reranking dokumen dengan server AI lokal.
- Menulis draf artikel riset/edukasi pasar komersial baru ke folder `/artikel/`.

## Instruksi Eksekusi Agen

Jalankan skrip Python di root direktori proyek:

```powershell
python ai_agent_search.py --query "<kata_kunci_atau_topik>"
```

### Parameter Opsional:
- `--slug <nama-slug>`: Menentukan slug URL artikel secara spesifik.
- `--top-k <jumlah>`: Menentukan berapa banyak referensi terbaik yang disaring (default: 3).
- `--dry-run`: Menguji pencarian dan reranking tanpa membuat file HTML fisik.

## Workflow Pasca-Eksekusi:
Setelah perintah selesai dieksekusi:
1. Tampilkan Top 3 referensi berita yang terpilih oleh Reranker beserta sumbernya.
2. Informasikan path file yang terbentuk: `artikel/<slug>/index.html`.
3. Tampilkan tautan pratinjau canonical URL: `https://www.gren.biz.id/artikel/<slug>`.
4. Beritahukan bahwa `sitemap.xml` telah diperbarui secara otomatis.
