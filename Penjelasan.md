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
### 2. INPUT titik_awal dari pengguna

### 3. INPUT tujuan_akhir dari pengguna

📄 Kode:
```python
start = input("Masukkan titik awal: ")
goal = input("Masukkan tujuan akhir: ")
```
### 4. JIKA titik_awal atau tujuan_akhir tidak ada dalam graf:

TAMPILKAN pesan error "Lokasi tidak valid"

📄 Kode:
```python
if start not in graph or goal not in graph:
    print("Lokasi tidak valid. Pastikan penulisan sesuai daftar.")
```

### 5. JALANKAN pengukuran waktu dan penggunaan memori
📄 Kode:
```python
tracemalloc.start()
start_time = time.time()
```

### 6. CEK apakah ada jalur dari titik_awal ke tujuan_akhir dengan BFS:

JIKA TIDAK ADA:

TAMPILKAN "Tidak ada jalur"

JIKA ADA:

JALANKAN algoritma Bidirectional Search

📄 Kode:
4. JIKA titik_awal atau tujuan_akhir tidak ada dalam graf:

TAMPILKAN pesan error "Lokasi tidak valid"

📄 Kode:

```python
if bfs(graph, start, goal):
    print(f"\n✅ Ada jalur yang menghubungkan {start} dan {goal}")
    shortest_path = bidirectional_search(graph, start, goal)
    print("🛣  Rute Terpendek:")
    print(" -> ".join(shortest_path))
else:
    print(f"\n❌ TIDAK ADA jalur yang menghubungkan {start} dan {goal}")
```

### 7. Algoritma Bidirectional Search

📄 Kode Inti:
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

### 8. SELESAIKAN pengukuran waktu dan memori

### 9. HITUNG waktu eksekusi
### 10. TAMPILKAN hasil analisis

📄 Kode:
```python
end_time = time.time()
current_memory, peak_memory = tracemalloc.get_traced_memory()
tracemalloc.stop()

execution_time = end_time - start_time

print("\n=== ANALISIS ALGORITMA ===")
print("Algoritma       : Bidirectional Search")
print(f"Time Complexity : {execution_time:.6f} detik")
print(f"Space Complexity: {peak_memory / 1024:.2f} KB")
```
