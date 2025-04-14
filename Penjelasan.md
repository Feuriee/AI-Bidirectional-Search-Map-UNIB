# Penjelasan Pseudocode & Kode Program
**Proyek: Sistem Navigasi Kampus UNIB dengan Algoritma Bidirectional Search**

---

## Pseudocode Utama & Penjelasan

Berikut adalah alur logika program dalam bentuk pseudocode yang diimplementasikan di `main.py`.

---

### 1. TAMPILKAN daftar lokasi dalam graf kampus UNIB

📄 **Kode:**
```python
print("Daftar Lokasi:")
for lokasi in graph.keys():
    print("-", lokasi)
```

## 2. Pilihan moda Transportasi 
```python
    'Jalan Kaki': 1.4,
    'Sepeda': 5.0,
    'Sepeda Motor': 8.3
```

## 3. Modifikasi Waktu dan Kondisi
```python
def get_modified_graph(day_type, time_hour):
    modified_graph = {key: value.copy() for key, value in graph.items()}
```

## 4. Algoritma Bidirectional Search (BDS)
```python
def bidirectional_search(graph, start, goal):
    if start == goal: return [start], 0
    f_queue, b_queue = deque([start]), deque([goal])
    f_visited, b_visited = {start: None}, {goal: None}
    while f_queue and b_queue:
        def expand(queue, visited, other_visited):
            node = queue.popleft()
            for neighbor in graph.get(node, {}):
                if neighbor not in visited:
                    visited[neighbor] = node
                    queue.append(neighbor)
                    if neighbor in other_visited:
                        return neighbor
            return None
```

## 5. Menjalankan Algoritma Analisis
```python
def run_algorithm_analysis(graph, start, goal):
    results = {}
    
    # Check if path exists
    tracemalloc.start()
    start_time = time.time()
```

## 6. GUI dengan Tkinter
```python
class UnibRouteFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencari Rute Kampus UNIB")
        self.root.geometry("800x620")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
```

## 7. Input User
```python
        # Frame untuk input
        input_frame = ttk.LabelFrame(main_frame, text="Parameter Input", padding="10")
        
        # Lokasi awal
        ttk.Label(input_frame, text="Lokasi Awal:").grid(row=0, column=0, sticky="w", pady=5)
```

## 8. Mencari Lokasi atau rute secara bidirectional
```python
    def find_route(self):
        start_location = self.start_var.get()
        goal_location = self.goal_var.get()
        transport_mode = self.transport_var.get()
        day_type = self.day_var.get()
        time_hour = int(self.hour_var.get())
```

## 9. Hitung analisis algoritma
```python
    def show_analysis(self):
        if not self.analysis_results:
            messagebox.showinfo("Analisis", "Silakan cari rute terlebih dahulu sebelum melihat analisis.")
            return
```

## 10. Menjalankan fungsi Main dan default
```python
if __name__ == "__main__":
    root = tk.Tk()
    app = UnibRouteFinderApp(root)
    root.mainloop()
```

# Perhitungan Algoritma bidirectional
**Algoritma Bidirectional Search (BDS) bekerja dengan melakukan pencarian dua arah secara simultan: dari titik awal (start) dan titik tujuan (goal). Proses dihentikan saat pencarian dari dua arah bertemu di satu titik (disebut meet_point). Berikut adalah proses perhitungan yang dilakukan:**

## 📌 Langkah-Langkah:
1. Inisialisasi dua antrian (queue) untuk pencarian maju dan mundur.
2. Lakukan pencarian dari kedua arah secara bergantian.
3. Periksa pertemuan antara dua pencarian (jika simpul ditemukan di kedua arah).
4. Rekonstruksi rute dari start → meet_point → goal.
5. Hitung total jarak dengan menjumlahkan bobot antar simpul dalam rute.
6. Hitung estimasi waktu berdasarkan moda transportasi yang dipilih.
7. Analisis performa algoritma:
   - Waktu komputasi (execution time)
   - Penggunaan memori (memory usage)

## Metode Hitung
1. Total jarak antar nodes
    - Total Jarak (b) = Σ jarak antara dua simpul bertetangga di rute
2. Hitung total jarak antar tempat
   - Waktu Tempuh (v) (jam) = Total Jarak (km) / Kecepatan (km/h)
   - Waktu Tempuh (v) (menit) = Waktu Tempuh (jam) × 60
3. Waktu eksekusi
   - Execution Time (d) = waktu_akhir - waktu_mulai
4. Penggunaan Memori
   - Memory Usage (memo) = peak memory (bytes) / 1024 (untuk konversi ke KB)
5. Time complexity
   - Bidirectional Search: O(b^(d/2))
- Karena dua pencarian dilakukan hingga d/2, maka total kompleksitasnya adalah:
   - O(b^(d/2)) + O(b^(d/2)) = O(2 * b^(d/2)) = O(b^(d/2))

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
