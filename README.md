
## 🚀 SEARCH MAP UNIB USING BIDIRECTIONAL SEARCH

---

### 👥 Anggota Kelompok 6
| Nama | GitHub |
|------|--------|
| [Agyl Wendi Pratama] | (https://github.com/likeazwee) |
| [Habib Al-Qodri] | (https://github.com/HabibAlQodri) |
| [Muhammad Ryan Al-Habsy] | (https://github.com/Starcres) |
| [Sidik Bagus Firmansyah] | (https://github.com/SiDiQ-KuN) |
| [Yohanes Adi Prasetya]| (https://github.com/Feuriee) |

---

## Algoritma
1. TAMPILKAN daftar lokasi dalam graf kampus UNIB

2. INPUT titik_awal dari pengguna
3. INPUT tujuan_akhir dari pengguna

4. JIKA titik_awal atau tujuan_akhir tidak ada dalam graf:
       TAMPILKAN pesan error "Lokasi tidak valid"

5. JALANKAN pengukuran waktu dan penggunaan memori
    a. MULAI pengukuran waktu
    b. MULAI pelacakan penggunaan memori

6. CEK apakah ada jalur dari titik_awal ke tujuan_akhir dengan BFS:
       JIKA TIDAK ADA:
           TAMPILKAN "Tidak ada jalur"
       JIKA ADA:
           JALANKAN algoritma Bidirectional Search:
               - INISIALISASI dua antrian pencarian: dari awal dan dari akhir
               - INISIALISASI dua dictionary untuk jejak kunjungan dari kedua arah
               - SELAMA kedua antrian tidak kosong:
                   a. EXPAND satu node dari antrian awal:
                       - Tambahkan neighbor yang belum dikunjungi
                       - Jika ditemukan di sisi lain, hentikan dan BANGUN rute
                   b. EXPAND satu node dari antrian akhir:
                       - Tambahkan neighbor yang belum dikunjungi
                       - Jika ditemukan di sisi lain, hentikan dan BANGUN rute

           KONSTRUKSI rute terpendek dari titik_awal ke tujuan_akhir melalui titik_temu

           TAMPILKAN rute terpendek

7. SELESAIKAN pengukuran waktu dan memori
8. HITUNG waktu eksekusi
9. TAMPILKAN hasil analisis:
       - Nama algoritma
       - Waktu eksekusi
       - Penggunaan memori puncak
