import time
import tracemalloc
from collections import deque

def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]
    
    forward_queue = deque([start])
    backward_queue = deque([goal])
    
    forward_visited = {start: None}
    backward_visited = {goal: None}
    
    while forward_queue and backward_queue:
        # Expand dari sisi awal
        if forward_queue:
            node = forward_queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in forward_visited:
                    forward_visited[neighbor] = node
                    forward_queue.append(neighbor)
                    if neighbor in backward_visited:
                        return construct_path(forward_visited, backward_visited, neighbor)
        
        # Expand dari sisi tujuan
        if backward_queue:
            node = backward_queue.popleft()
            for neighbor in graph.get(node, []):
                if neighbor not in backward_visited:
                    backward_visited[neighbor] = node
                    backward_queue.append(neighbor)
                    if neighbor in forward_visited:
                        return construct_path(forward_visited, backward_visited, neighbor)
    
    return None

def construct_path(forward_visited, backward_visited, meeting_point):
    path = []
    # Dari awal ke titik temu
    node = meeting_point
    while node is not None:
        path.append(node)
        node = forward_visited.get(node)
    path.reverse()
    
    # Dari titik temu ke tujuan
    node = backward_visited.get(meeting_point)
    while node is not None:
        path.append(node)
        node = backward_visited.get(node)
    
    return path

def bfs(graph, start, goal):
    queue = deque([start])
    visited = set()
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        if node not in visited:
            visited.add(node)
            queue.extend(graph.get(node, []))
    return False

graph = {
    'Masjid Darul Ulum': {'Fakultas Hukum': 100, 'Gerbang Masuk 1': 80, 'Gerbang Keluar 1': 120},
    'Fakultas Hukum': {'GOR UNIB': 150, 'Gedung 1': 200, 'Magister Akuntansi': 170, 'Masjid Darul Ulum': 100, 'Gerbang Keluar 1': 110, 'Gerbang Masuk 1': 90},
    'Magister Akuntansi': {'Fakultas Ekonomi dan Bisnis': 160, 'Gedung 1': 140, 'Fakultas Hukum': 170},
    'Fakultas Ekonomi dan Bisnis': {'Magister Akuntansi': 160, 'GOR UNIB': 180},
    'Gedung 1': {'Fakultas Hukum': 200, 'Magister Akuntansi': 140, 'Lab. Pertanian': 180, 'Gedung R UPT Bahasa': 130},
    'GOR UNIB': {'Fakultas Hukum': 150, 'Fakultas Ekonomi dan Bisnis': 180},
    'Lab. Pertanian': {'Gedung 1': 180, 'Fakultas Pertanian': 120, 'GLT': 150, 'Rektorat': 200},
    'Gedung R UPT Bahasa': {'Gedung 1': 130, 'Klinik Pratama UNIB': 100},
    'Fakultas Pertanian': {'Lab. Pertanian': 120, 'Lab. Perikanan': 90},
    'Lab. Perikanan': {'Fakultas Pertanian': 90},
    'Klinik Pratama UNIB': {'Gedung R UPT Bahasa': 100, 'Rektorat': 150},
    'Rektorat': {'Lab. Pertanian': 200, 'Klinik Pratama UNIB': 150, 'GLT': 100, 'Fakultas Ilmu Sosial dan Ilmu Politik': 120, 'Gerbang Masuk 2': 100},
    'Fakultas Ilmu Sosial dan Ilmu Politik': {'GB2': 100, 'Rektorat': 120, 'Gerbang Masuk 3': 90},
    'GLT': {'Lab. Pertanian': 150, 'Rektorat': 100, 'Lab. Kehutanan dan Ilmu Lingkungan': 140, 'Lab. Bio, Fisika dan Kimia': 180},
    'Lab. Kehutanan dan Ilmu Lingkungan': {'GLT': 140, 'Danau UNIB': 130, 'Lab. Bio, Fisika dan Kimia': 110},
    'Danau UNIB': {'Lab. Kehutanan dan Ilmu Lingkungan': 130, 'GB2': 110},
    'Lab. Bio, Fisika dan Kimia': {'GLT': 180, 'Lab. Kehutanan dan Ilmu Lingkungan': 110, 'GB1': 100, 'Fakultas Matematika dan Ilmu Pengetahuan Alam': 160},
    'GB1': {'Lab. Bio, Fisika dan Kimia': 100, 'GB2': 80, 'Perpus UNIB': 90, 'Fakultas Keguruan dan Ilmu Pendidikan': 110, 'LPTIK': 150, 'Gerbang Keluar 2': 120},
    'GB2': {'Danau UNIB': 110, 'GB1': 80, 'Perpus UNIB': 90, 'Fakultas Keguruan dan Imu Pendidikan': 100, 'LPTIK': 150, 'Gerbang Keluar 2': 120, 'Fakultas Ilmu Sosial dan Ilmu Politik': 100},
    'Perpus UNIB': {'GB1': 90, 'GB2': 90, 'Fakultas Keguruan dan Ilmu Pendidikan': 80, 'LPTIK': 100, 'Gerbang Keluar 2': 110},
    'Fakultas Keguruan dan Ilmu Pendidikan': {'Perpus UNIB': 80, 'GB1': 110, 'GB2': 100, 'LPTIK': 90, 'Gerbang Keluar 2': 100},
    'LPTIK': {'Lab. FKIP': 130, 'GB1': 150, 'GB2': 150, 'Perpus UNIB': 100, 'Fakultas Keguruan dan Ilmu Pendidikan': 90},
    'Lab. FKIP': {'Fakultas Teknik': 140, 'Gedung Serba Guna': 150, 'LPTIK': 130, 'Masjid Baitul Hikmah': 130},
    'Fakultas Teknik': {'Gerbang Keluar 3': 90, 'Gedung Serba Guna': 100, 'Lab. FKIP': 140, 'Lab. Terpadu Teknik': 130, 'Masjid Baitul Hikmah': 100},
    'Masjid Baitul Hikmah': {'Gerbang Keluar 3': 80, 'Fakultas Teknik': 100, 'Lab. FKIP': 130},
    'Gedung Serba Guna': {'Fakultas Teknik': 100, 'Lab. Terpadu Teknik': 90, 'GB3 dan 4': 120, 'Magister FKIP': 130, 'Gedung PKM': 140, 'Lab. FKIP': 150},
    'Lab. Terpadu Teknik': {'Gedung Serba Guna': 90, 'GB3 dan 4': 110, 'Magister FKIP': 100, 'Fakultas Teknik': 130},
    'Magister FKIP': {'Lab. Terpadu Teknik': 100, 'Gedung Serba Guna': 130, 'Stadion UNIB': 200, 'GB5': 140, 'Fakultas Kedokteran': 120},
    'Stadion UNIB': {'Magister FKIP': 200},
    'GB3 dan 4': {'Gedung Serba Guna': 120, 'Lab. Terpadu Teknik': 110, 'Magister FKIP': 100, 'GB5': 90, 'Fakultas Kedokteran': 100, 'Gedung PKM': 80},
    'Gedung PKM': {'GB3 dan 4': 80, 'Gedung Serba Guna': 140},
    'GB5': {'Magister FKIP': 140, 'GB3 dan 4': 90, 'Fakultas Kedokteran': 100, 'Fakultas Matematika dan Ilmu Pengetahuan Alam': 160},
    'Fakultas Kedokteran': {'GB5': 100, 'GB3 dan 4': 100, 'Magister FKIP': 120},
    'Fakultas Matematika dan Ilmu Pengetahuan Alam': {'GB5': 160, 'Lab. Bio, Fisika dan Kimia': 160},
    'Gerbang Masuk 1': {'Masjid Darul Ulum': 80, 'Fakultas Hukum': 90},
    'Gerbang Masuk 2': {'Rektorat': 100},
    'Gerbang Masuk 3': {'Fakultas Ilmu Sosial dan Ilmu Politik': 90},
    'Gerbang Keluar 1': {'Fakultas Hukum': 110, 'Masjid Darul Ulum': 120},
    'Gerbang Keluar 2': {'GB1': 120, 'GB2': 120, 'Perpus UNIB': 110, 'Fakultas Keguruan dan Ilmu Pendidikan': 100},
    'Gerbang Keluar 3': {'Masjid Baitul Hikmah': 80, 'Fakultas Teknik': 90}
}

# --------------------
# INPUT DARI USER
# --------------------
print("=== Penelusuran Rute Kampus UNIB ===")
print("Daftar lokasi:")
for i, key in enumerate(graph.keys(), 1):
    print(f"{i}. {key}")

start = input("\nMasukkan titik awal: ")
goal = input("Masukkan tujuan akhir: ")

# --------------------
# EKSEKUSI DENGAN PENGUKURAN WAKTU DAN MEMORI
# --------------------
if start not in graph or goal not in graph:
    print("Lokasi tidak valid. Pastikan penulisan sesuai daftar.")
else:
    tracemalloc.start()  # Mulai pemantauan memori
    start_time = time.time()  # Mulai pengukuran waktu

    if bfs(graph, start, goal):
        print(f"\n✅ Ada jalur yang menghubungkan {start} dan {goal}")
        shortest_path = bidirectional_search(graph, start, goal)
        print("🛣  Rute Terpendek:")
        print(" -> ".join(shortest_path))
    else:
        print(f"\n❌ TIDAK ADA jalur yang menghubungkan {start} dan {goal}")

    end_time = time.time()  # Selesai pengukuran waktu
    current_memory, peak_memory = tracemalloc.get_traced_memory()  # Ambil data memori
    tracemalloc.stop()  # Hentikan pemantauan memori

    execution_time = end_time - start_time  # Hitung waktu eksekusi dalam detik

    # --------------------
    # ANALISIS WAKTU DAN RUANG
    # --------------------
    print("\n=== ANALISIS ALGORITMA ===")
    print("Algoritma       : Bidirectional Search")
    print(f"Time Complexity : {execution_time:.6f} detik")
    print(f"Space Complexity: {peak_memory / 1024:.2f} KB (memori puncak yang digunakan)")
