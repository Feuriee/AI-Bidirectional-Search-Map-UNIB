# Dokumentasi Kode Sistem Navigasi Kampus UNIB

## Ikhtisar
Repositori ini berisi kode sumber untuk sistem navigasi kampus Universitas Bengkulu (UNIB). Sistem ini menggunakan algoritma Pencarian Dua Arah (Bidirectional Search/BDS) untuk menemukan rute optimal antara lokasi-lokasi kampus dan menawarkan berbagai mode transportasi.

## Daftar Isi
- [Dependensi](#dependensi)
- [Struktur Kode Sumber](#struktur-kode-sumber)
- [Struktur Data](#struktur-data)
- [Algoritma Inti](#algoritma-inti)
- [Implementasi GUI](#implementasi-gui)
- [API Eksternal](#api-eksternal)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)

## Dependensi
Aplikasi ini memerlukan pustaka Python berikut:
```
tkinter          - Framework GUI
networkx         - Struktur data graf dan algoritma
openrouteservice - API rute eksternal
folium           - Visualisasi peta interaktif
os               - Operasi sistem file
time             - Pengukuran kinerja
math             - Perhitungan matematis
tracemalloc      - Pelacakan penggunaan memori
itertools        - Generator kombinasi
datetime         - Penanganan tanggal dan waktu
```

## Struktur Kode Sumber

Kode sumber diorganisir menjadi beberapa bagian logis:

1. **Definisi Data**
   - Koordinat lokasi kampus
   - Kecepatan transportasi
   - Konstruksi graf

2. **Komponen Algoritma**
   - Perhitungan jarak Haversine
   - Implementasi Pencarian Dua Arah
   - Penyaringan gerbang berdasarkan waktu
   - Pencarian rute

3. **Komponen GUI**
   - Jendela aplikasi utama
   - Formulir input
   - Tampilan hasil
   - Visualisasi peta

4. **Alat Analisis**
   - Metrik kinerja algoritma
   - Statistik rute

## Struktur Data

### Koordinat Lokasi
Sistem menggunakan kamus untuk menyimpan koordinat geografis (lintang, bujur) untuk semua lokasi kampus:
```python
coordinates = {
    "Rektorat": [-3.7590495172423495, 102.27231460986346],
    'Masjid Darul Ulum': [-3.757594, 102.267707],
    # ... lokasi lainnya
}
```

### Kecepatan Transportasi
Mode transportasi yang berbeda memiliki kecepatan yang berbeda (dalam m/s):
```python
transport_speeds = {
    "Jalan Kaki": 1.4,    # Berjalan
    "Sepeda": 4.2,        # Sepeda
    "Sepeda Motor": 8.3   # Sepeda Motor
}
```

### Model Graf
Kampus dimodelkan sebagai graf di mana:
- Simpul mewakili lokasi kampus
- Tepi mewakili jalur langsung antara lokasi
- Hanya lokasi dalam radius 200m yang terhubung
- Bobot tepi mewakili jarak Haversine

```python
G = nx.Graph()
for a, b in combinations(coordinates, 2):
    dist = haversine(coordinates[a], coordinates[b])
    if dist < 200:
        G.add_edge(a, b, weight=dist)
```

## Algoritma Inti

### Jarak Haversine
Rumus Haversine menghitung jarak lingkaran besar antara dua titik pada bola:

```python
def haversine(coord1, coord2):
    R = 6371e3
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
```

### Logika Status Gerbang
Gerbang kampus memiliki jam operasional berbeda berdasarkan waktu dan hari:

```python
def status_gerbang(jam, hari):
    status = {g: "Tutup" for g in [
        "Gerbang Masuk 1", "Gerbang Masuk 2", "Gerbang Masuk 3",
        "Gerbang Keluar 1", "Gerbang Keluar 2", "Gerbang Keluar 3"]}

    if 7 <= jam < 18:
        for g in status:
            status[g] = "Buka"
    else:
        status["Gerbang Masuk 3"] = "Buka"
        status["Gerbang Keluar 2"] = "Buka"

    if hari == "weekend":
        status["Gerbang Keluar 3"] = "Tutup (Akhir Pekan)"

    return status
```

### Graf Terfilter Berdasarkan Waktu
Graf difilter berdasarkan status gerbang:

```python
def filter_graph_by_time(graph, jam, hari):
    gate_status = status_gerbang(jam, hari)
    Gf = nx.Graph()
    for u, v, d in graph.edges(data=True):
        if ("Gerbang" in u and gate_status.get(u, "Buka") != "Buka") or 
           ("Gerbang" in v and gate_status.get(v, "Buka") != "Buka"):
            continue
        Gf.add_edge(u, v, weight=d['weight'])
    return Gf
```

### Pencarian Dua Arah
Algoritma BDS mencari dari sumber dan target secara bersamaan:

```python
def bidirectional_shortest_path_with_count(G, source, target):
    # Inisialisasi struktur pencarian maju dan mundur
    forward_paths = {source: [source]}
    backward_paths = {target: [target]}
    forward_seen = {source}
    backward_seen = {target}
    
    # Lacak simpul yang dikunjungi untuk analisis algoritma
    visited = 0
    
    # Loop pencarian utama
    while forward_paths and backward_paths:
        # Proses frontier yang lebih kecil terlebih dahulu untuk efisiensi
        if len(forward_paths) <= len(backward_paths):
            new_forward_paths = {}
            for u, path in forward_paths.items():
                visited += 1
                for v in G[u]:
                    if v not in forward_seen:
                        forward_seen.add(v)
                        new_path = path + [v]
                        new_forward_paths[v] = new_path
                        if v in backward_seen:
                            # Menemukan perpotongan - bangun jalur lengkap
                            return new_path[:-1] + backward_paths[v][::-1]
            forward_paths = new_forward_paths
        else:
            # Proses yang sama untuk pencarian mundur
            new_backward_paths = {}
            for u, path in backward_paths.items():
                visited += 1
                for v in G[u]:
                    if v not in backward_seen:
                        backward_seen.add(v)
                        new_path = path + [v]
                        new_backward_paths[v] = new_path
                        if v in forward_seen:
                            # Menemukan perpotongan - bangun jalur lengkap
                            return forward_paths[v] + new_path[1:][::-1]
            backward_paths = new_backward_paths
    
    # Tidak ada jalur yang ditemukan
    raise nx.NetworkXNoPath(f"Tidak ada jalur antara {source} dan {target}")
```

### Pencarian Rute
Fungsi pencarian rute utama menggabungkan algoritma-algoritma:

```python
def find_route(start, goal, jam, hari, transport_mode, show_map=False):
    if show_map:
        # Gunakan OpenRouteService untuk visualisasi
        ors_coords, ors_dist = get_ors_route(coordinates[start], 
                                          coordinates[goal], transport_mode)
        return {
            "path": None,
            "coords": ors_coords,
            "dist": ors_dist,
            # ... metrik kinerja
        }
    else:
        # Gunakan algoritma BDS
        return find_route_bds(start, goal, jam, hari)
```

## Implementasi GUI

GUI diimplementasikan menggunakan Tkinter dengan pendekatan berbasis kelas:

```python
class NavigasiKampusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Navigasi Kampus UNIB")
        self.root.geometry("600x750")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
        self.hasil_rute = None
```

### Komponen Utama
1. **Frame Header** - Judul aplikasi
2. **Frame Input** - Pemilihan lokasi, pengaturan waktu, mode transportasi
3. **Frame Tombol** - Tombol aksi
4. **Frame Hasil** - Tampilan teks hasil rute
5. **Status Bar** - Informasi status aplikasi

### Metode Kunci
- `setup_ui()` - Menginisialisasi semua komponen UI
- `validate_inputs()` - Memvalidasi input pengguna
- `calculate_route()` - Melakukan perhitungan rute
- `show_route()` - Menampilkan rute pada peta dan dalam teks
- `show_analysis()` - Menampilkan analisis kinerja algoritma

## API Eksternal

### OpenRouteService (ORS)
Aplikasi menggunakan ORS untuk visualisasi berbasis peta:

```python
client = openrouteservice.Client(key='5b3ce3597851110001cf62486e58c245d2f740bfa1bdd46cbab8ed58')

def get_ors_route(coord1, coord2, transport_mode):
    # Pemetaan ke profil ORS
    ors_profiles = {
        "Jalan Kaki": "foot-walking",
        "Sepeda": "cycling-regular",
        "Sepeda Motor": "driving-car"
    }
    
    try:
        res = client.directions(
            coordinates=[coord1[::-1], coord2[::-1]],
            profile=ors_profiles[transport_mode], format='geojson')
        geometry = res['features'][0]['geometry']['coordinates']
        distance = res['features'][0]['properties']['segments'][0]['distance']
        return [[lat, lon] for lon, lat in geometry], distance
    except Exception as e:
        print(f"ORS Error: {e}")
        return None, None
```

### Folium
Folium digunakan untuk membuat peta interaktif untuk visualisasi rute:

```python
m = folium.Map(location=coordinates[start], zoom_start=17)
folium.Marker(coordinates[start], tooltip=f"Start: {start}", 
              icon=folium.Icon(color='green')).add_to(m)
folium.Marker(coordinates[goal], tooltip=f"Goal: {goal}", 
              icon=folium.Icon(color='red')).add_to(m)
folium.PolyLine(coords, color=color, weight=5, 
                tooltip=f"BDS - {dist:.2f} m").add_to(m)
m.save("rute_kampus.html")
webbrowser.open("file://" + os.path.realpath("rute_kampus.html"))
```

## Menjalankan Aplikasi

Titik masuk aplikasi ada di bagian bawah skrip:

```python
if __name__ == "__main__":
    root = tk.Tk()
    app = NavigasiKampusApp(root)
    root.mainloop()
```

Untuk menjalankan aplikasi:
1. Pastikan semua dependensi terinstal: `pip install -r requirements.txt`
2. Jalankan skrip utama: `python navigasi_kampus.py`
3. GUI akan muncul, memungkinkan Anda memilih titik awal dan akhir, mode transportasi, dan pengaturan waktu
4. Klik "Tampilkan Rute" untuk menampilkan rute atau "Analisis Algoritma" untuk melihat metrik kinerja

## Analisis Kinerja

Aplikasi menganalisis kinerja algoritma:
- Kompleksitas waktu
- Penggunaan memori
- Waktu eksekusi
- Statistik jalur (jarak, estimasi waktu)
- Perkiraan konsumsi energi dan emisi karbon

## Metode Perhitungan Jarak

1. **Rumus Haversine** - Digunakan untuk menghitung jarak lingkaran besar antara dua titik di permukaan Bumi:
   ```python
   def haversine(coord1, coord2):
       R = 6371e3  # Radius Bumi dalam meter
       lat1, lon1 = map(math.radians, coord1)
       lat2, lon2 = map(math.radians, coord2)
       dlat = lat2 - lat1
       dlon = lon2 - lon1
       a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
       return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
   ```
   Rumus ini menghitung jarak terpendek antara dua titik pada bentuk bola (Bumi) menggunakan koordinat latitude dan longitude.

2. **Bobot Tepi Graf** - Sistem menggunakan jarak Euclidean (jarak garis lurus) kurang dari 200m untuk membangun graf:
   ```python
   for a, b in combinations(coordinates, 2):
       dist = haversine(coordinates[a], coordinates[b])
       if dist < 200:
           G.add_edge(a, b, weight=dist)
   ```

## Algoritma Pencarian Rute

1. **Algoritma Bidirectional Shortest Path (BDS)** - Metode utama pencarian jalur:
   ```python
   def bidirectional_shortest_path_with_count(G, source, target):
       # Inisialisasi frontier dan jalur maju dan mundur
       forward_paths = {source: [source]}
       backward_paths = {target: [target]}
       forward_seen = {source}
       backward_seen = {target}
       
       # Loop pencarian utama
       while forward_paths and backward_paths:
           # Proses frontier maju
           # Proses frontier mundur
           # Kembalikan jalur ketika pertemuan ditemukan
   ```
   Algoritma ini melakukan pencarian secara simultan dari titik awal dan titik akhir, bertemu di tengah untuk menemukan jalur terpendek.

2. **API OpenRouteService** - Digunakan ketika visualisasi peta diaktifkan:
   ```python
   def get_ors_route(coord1, coord2, transport_mode):
       # Memetakan moda transportasi ke profil ORS
       ors_profiles = {
           "Jalan Kaki": "foot-walking",
           "Sepeda": "cycling-regular",
           "Sepeda Motor": "driving-car"
       }
       
       # Panggilan API untuk mendapatkan rute
       res = client.directions(
           coordinates=[coord1[::-1], coord2[::-1]],
           profile=ors_profiles[transport_mode], format='geojson')
   ```

## Perhitungan Waktu dan Kecepatan

1. **Konstanta Kecepatan Transportasi** - Didefinisikan untuk berbagai moda transportasi:
   ```python
   transport_speeds = {
       "Jalan Kaki": 1.4,  # m/detik
       "Sepeda": 4.2,      # m/detik
       "Sepeda Motor": 8.3  # m/detik
   }
   ```

2. **Estimasi Waktu Tempuh** - Dihitung dari jarak dan kecepatan:
   ```python
   est_time = (dist / transport_speeds[transport]) / 60  # Konversi detik ke menit
   ```

## Perhitungan Konsumsi Energi dan Emisi

1. **Rumus Konsumsi Energi** - Model linear sederhana berdasarkan jarak:
   ```python
   energy_consumption = {
       "Jalan Kaki": f"{dist * 0.06:.2f} kalori",
       "Sepeda": f"{dist * 0.04:.2f} kalori",
       "Sepeda Motor": f"{dist * 0.05:.2f} liter BBM"
   }
   ```

2. **Perhitungan Emisi Karbon** - Juga berdasarkan jarak:
   ```python
   emission = {
       "Jalan Kaki": "0 gram CO2",
       "Sepeda": "0 gram CO2",
       "Sepeda Motor": f"{dist * 0.07:.2f} gram CO2"
   }
   ```

## Pengukuran Performa Algoritma

1. **Kompleksitas Waktu** - Dilacak sebagai O(node yang dikunjungi):
   ```python
   time_complexity = f"O({visited})"
   ```

2. **Waktu Eksekusi** - Diukur menggunakan modul time:
   ```python
   start_time = time.time()
   # Eksekusi algoritma
   execution_time = time.time() - start_time
   ```

3. **Penggunaan Memori** - Dilacak menggunakan tracemalloc:
   ```python
   tracemalloc.start()
   # Eksekusi algoritma
   current, peak = tracemalloc.get_traced_memory()
   memory_peak = peak / 1024  # KB
   tracemalloc.stop()
   ```

Aplikasi ini menggunakan kombinasi teori graf, perhitungan geografis, dan model fisika sederhana untuk menyediakan layanan navigasi dan menganalisis berbagai pilihan transportasi di seluruh kampus UNIB.

## Perbandingan Hasil Percobaan
**Perbandingan antara jarak dan time complexity**
| Jarak (Meter) | Time Complexity (Detik) |
|---------------|-------------------------|
| 0             | 0.001001                |
| 100           | 0.002012                |
| 200           | 0.002120                |
| 300           | 0.002502                |
| 400           | 0.002112                |
| 500           | 0.002612                |

**Perbandingan antara jumlah node dan time complexity**
| Nodes         | Time Complexity (Detik) |
|---------------|-------------------------|
| 0             | 0.001001                |
| 1             | 0.001333                |
| 2             | 0.001502                |
| 3             | 0.002112                |
| 4             | 0.002612                |
| 5             | 0.003012                |

**Perbandingan antara Jarak dan alokasi memori**
| Jarak (Meter) | Alokasi Memori (KB)     |
|---------------|-------------------------|
| 0             | 0.95                    |
| 100           | 2.22                    |
| 200           | 2.22                    |
| 300           | 2.45                    |
| 400           | 2.48                    |
| 500           | 2.69                    |

**Perbandingan antara nodes dan alokasi memori**

| Nodes         | Alokasi Memori (KB)     |
|---------------|-------------------------|
| 0             | 0.95                    |
| 1             | 2.22                    |
| 2             | 2.22                    |
| 3             | 2.32                    |
| 4             | 2.45                    |
| 5             | 2.69                    |


### Kesimpulan
***Berdasarkan hasil percobaan yang dilakukan terhadap algoritma pencarian rute Bidirectional Search, diperoleh beberapa kesimpulan sebagai berikut:***
1. Pengaruh Jarak terhadap Kompleksitas Waktu
    - Terdapat peningkatan time complexity seiring bertambahnya jarak yang ditempuh. Meskipun fluktuatif, hal ini disebabkan oleh bertambahnya ruang pencarian yang harus dieksplorasi oleh algoritma.
2. Pengaruh Jumlah Node terhadap Kompleksitas Waktu
    - Jumlah simpul (nodes) yang dilalui berbanding lurus dengan time complexity. Saat jumlah node meningkat, waktu komputasi juga meningkat secara bertahap.
3. Pengaruh Jarak terhadap Alokasi Memori
   - Alokasi memori juga meningkat seiring bertambahnya jarak. Hal ini dapat terjadi karena pencarian jarak yang lebih jauh membutuhkan lebih banyak struktur data.
4. Pengaruh Jumlah Node terhadap Alokasi Memori
   - Sama seperti pada kompleksitas waktu, jumlah node juga mempengaruhi alokasi memori. Penambahan jumlah node menyebabkan kebutuhan memori bertambah secara bertahap, meskipun pada beberapa titik terlihat adanya plateau         yang menandakan bahwa penggunaan memori tidak selalu naik secara linier.

# Kesimpulan dari Algoritma Navigasi Kampus UNIB

Berdasarkan analisis terhadap kode sumber aplikasi Navigasi Kampus UNIB, dapat disimpulkan beberapa hal tentang algoritma yang digunakan:

1. **Algoritma Utama: Bidirectional Shortest Path (BDS)**
   - Algoritma ini bekerja dengan melakukan pencarian dari dua arah secara bersamaan (dari titik awal dan titik tujuan)
   - Efisien untuk jaringan yang luas karena memiliki kompleksitas waktu lebih rendah daripada algoritma pencarian satu arah tradisional
   - Meminimalkan ruang pencarian dengan menemukan titik pertemuan di tengah perjalanan

2. **Representasi Data dengan Graf**
   - Lokasi kampus direpresentasikan sebagai node dalam graf berbobot
   - Koneksi antara lokasi (dengan jarak < 200m) direpresentasikan sebagai edge dengan bobot jarak
   - Struktur data ini memungkinkan penerapan algoritma pencarian jalur secara efisien

3. **Optimasi berdasarkan Waktu dan Kondisi**
   - Algoritma mempertimbangkan status gerbang kampus (buka/tutup) berdasarkan jam dan hari
   - Graf difilter secara dinamis berdasarkan waktu pencarian untuk memastikan rute melalui gerbang yang sedang buka

4. **Kinerja dan Performa**
   - Kompleksitas waktu diukur dalam O(n) di mana n adalah jumlah node yang dikunjungi
   - Penggunaan memori dan waktu eksekusi diukur secara presisi menggunakan tracemalloc dan modul time
   - Untuk kasus visualisasi, algoritma menggunakan OpenRouteService API sebagai alternatif yang lebih ringan

5. **Fleksibilitas Moda Transportasi**
   - Algoritma memperhitungkan berbagai moda transportasi dengan kecepatan berbeda
   - Estimasi waktu tempuh disesuaikan berdasarkan moda transportasi yang dipilih
   - Perhitungan tambahan untuk konsumsi energi dan emisi karbon memberikan perspektif tambahan bagi pengguna

Secara keseluruhan, algoritma BDS yang diimplementasikan dalam aplikasi ini merupakan solusi yang efisien dan tepat untuk navigasi kampus, dengan kemampuan adaptasi terhadap berbagai faktor seperti waktu, kondisi gerbang, dan moda transportasi. Pendekatan bidirectional memungkinkan pencarian jalur yang lebih cepat dibandingkan algoritma pencarian satu arah konvensional, yang sangat bermanfaat untuk pengguna yang membutuhkan navigasi real-time di lingkungan kampus UNIB.
