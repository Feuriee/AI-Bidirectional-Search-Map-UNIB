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
    'Masjid Darul Ulum': ['Fakultas Hukum', 'Gerbang Masuk 1', 'Gerbang Keluar 1'],
    'Fakultas Hukum' : ['GOR UNIB', 'Gedung 1', 'Magister Akuntansi', 'Masjid Darul Ulum', 'Gerbang Keluar 1'],
    'Magister Akuntansi': ['Fakultas Ekonomi dan Bisnis', 'Gedung 1', 'Fakultas Hukum'],
    'Fakultas Ekonomi dan Bisnis': ['Magister Akuntansi', 'GOR UNIB'],
    'Gedung 1': ['Fakultas Hukum', 'Magister Akuntansi', 'Lab. Pertanian', 'Gedung R UPT Bahasa'],
    'GOR UNIB': ['Fakultas Hukum', 'Fakultas Ekonomi dan Bisnis'],
    'Lab. Pertanian': ['Gedung 1', 'Fakultas Pertanian', 'GLT', 'Rektorat'],
    'Gedung R UPT Bahasa': ['Gedung 1', 'Klinik Pratama UNIB'],
    'Fakultas Pertanian' : ['Lab. Pertanian', 'Lab. Perikanan'],
    'Lab. Perikanan': ['Fakultas Pertanian'],
    'Klinik Pratama UNIB' : ['Gedung R UPT Bahasa', 'Rektorat'],
    'Rektorat' : ['Lab. Pertanian', 'Klinik Pratama UNIB', 'GLT', 'Fakultas Ilmu Sosial dan Ilmu Politik'],
    'Fakultas Ilmu Sosial dan Ilmu Politik': ['GB2', 'Rektorat'],
    'GLT' : ['Lab. Pertanian', 'Rektorat', 'Lab. Kehutanan dan Ilmu Lingkungan', 'Lab. Bio, Fisika dan Kimia'],
    'Lab. Kehutanan dan Ilmu Lingkungan' : ['GLT', 'Danau UNIB', 'Lab. Bio, Fisika dan Kimia', ],
    'Danau UNIB' : ['Lab. Kehutanan dan Ilmu Lingkungan', 'GB2'],
    'Lab. Bio, Fisika dan Kimia' : ['GLT', 'Lab. Kehutanan dan Ilmu Lingkungan', 'GB1', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'],
    'GB1' : ['Lab. Bio, Fisika dan Kimia', 'GB2', 'Perpus UNIB', 'Fakultas Keguruan dan Ilmu Pendidikan', 'LPTIK', 'Gerbang Keluar 2'],
    'GB2' : ['Danau UNIB', 'GB1', 'Perpus UNIB', 'Fakultas Keguruan dan Imu Pendidikan', 'LPTIK', 'Gerbang Keluar 2'],
    'Perpus UNIB' : ['GB1', 'GB2', 'Fakultas Keguruan dan Ilmu Pendidikan', 'LPTIK', 'Gerbang Keluar 2'],
    'Fakultas Keguruan dan Ilmu Pendidikan' : ['Perpus UNIB', 'GB1', 'GB2', 'LPTIK', 'Gerbang Keluar 2'],
    'LPTIK' : ['Lab. FKIP'],
    'Lab. FKIP': ['Fakultas Teknik', 'Gedung Serba Guna'],
    "Fakultas Teknik": ["Gerbang Keluar 3", "Gedung Serba Guna", "Lab. FKIP", "Lab. Terpadu Teknik"],
    'Masjid Baitul Hikmah': ['Gerbang Keluar 3', 'Fakultas Teknik', 'Lab. FKIP'],
    'Gebung Serba Guna': ['Fakultas Teknik', 'Lab. Terpadu Teknik', 'GB3 dan 4', 'Magister FKIP', 'Gedung PKM'],
    'Lab. Terpadu Teknik': ['Gedung Serba Guna', 'GB3 dan 4', 'Magister FKIP'],
    'Magister FKIP': ['Lab. Terpadu Teknik', 'Gedung Serba Guna', 'Stadion UNIB', 'GB5', 'Fakultas Kedokteran'],
    'Stadion UNIB': ['Magister FKIP'],
    'GB3 dan 4': ['Gedung Serba Guna', 'Lab. Terpadu Teknik', 'Magister FKIP', 'GB5', 'Fakultas Kedokteran', 'Gedung PKM'],
    'Gedung PKM': ['GB3 dan 4', 'Gedung Serba Guna'],
    'GB5': ['Magister FKIP', 'GB3 dan 4', 'Fakultas Kedokteran', 'Fakultas Matematika dan Ilmu Pengetahuan Alam'],
    'Fakultas Kedokteran': ['GB5', 'GB3 dan 4', 'Magister FKIP'],
    'Fakultas Matematika dan Ilmu Pengetahuan Alam': ['GB5', 'Lab. Bio, Fisika dan Kimia'],
    'Gerbang Masuk 1': ['Masjid Darul Ulum', 'Fakultas Hukum'],
    'Gerbang Masuk 2' : ['Rektorat'],
    'Gerbang Masuk 3': ['Fakultas Ilmu Sosial dan Ilmu Politik'],
    'Gerbang Keluar 1' : ['Fakultas Hukum'],
    'Gerbang Keluar 2' : ['GB1', 'GB2', 'Perpus UNIB', 'Fakultas Keguruan dan Ilmu Pendidikan'],
    'Gerbang Keluar 3' : ['Masjid Baitul Hikmah'],
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
