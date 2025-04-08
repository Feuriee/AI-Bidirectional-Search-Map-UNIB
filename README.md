
## 🚀 SEARCH MAP UNIB USING BIDIRECTIONAL SEARCH

---

### 👥 Anggota Kelompok 6
| Nama | GitHub |
|------|--------|
| [Agyl Wendi Pratama] | (https://github.com/likeazwee) |
| [Habib Al-Qodri] | (https://github.com/HabibAlQodri) |
| [Muhammad Ryan Al-Habsy] | (https://github.com/Starcres) |
| [Sidik Bagus Firmansyah] | (https://github.com/Sidiqkun) |
| [Yohanes Adi Prasetya]| (https://github.com/Feuriee) |

---

## Algoritma
1. Tampilkan semua lokasi yang tersedia dalam graf kampus UNIB

2. Minta pengguna memasukkan titik awal
3. Minta pengguna memasukkan tujuan akhir

4. Jika salah satu lokasi tidak ada dalam graf:
     Tampilkan pesan "Lokasi tidak valid, pastikan penulisan sesuai daftar."

5. Mulai proses pengukuran performa:
     a. Catat waktu mulai
     b. Aktifkan pelacakan penggunaan memori

6. Cek apakah kedua lokasi terhubung menggunakan BFS:
     - Jika tidak terhubung:
         Tampilkan "❌ Tidak ada jalur antara titik awal dan tujuan"
     - Jika terhubung:
         Lakukan pencarian rute dengan **Bidirectional Search**:
           - Inisialisasi dua antrian pencarian (dari titik awal dan dari tujuan)
           - Simpan riwayat kunjungan dari kedua arah
           - Selama kedua antrian masih ada isi:
               a. Ambil satu node dari sisi awal, jelajahi semua tetangganya
                   - Jika ketemu node yang juga sudah dikunjungi dari sisi tujuan:
                     Berarti jalur ditemukan!
               b. Lakukan hal serupa dari sisi tujuan
           - Jika ditemukan titik pertemuan:
               Bangun rute terpendek dari titik awal ke tujuannya

         Tampilkan rute terpendek hasil pencarian

7. Setelah selesai pencarian:
     a. Catat waktu selesai
     b. Ambil data penggunaan memori puncak

8. Hitung waktu eksekusi total

9. Tampilkan ringkasan hasil analisis:
     - Algoritma yang digunakan
     - Waktu proses
     - Memori maksimum yang digunakan
