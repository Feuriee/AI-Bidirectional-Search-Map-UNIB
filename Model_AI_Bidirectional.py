import time, tracemalloc
from collections import deque

# Graph dengan jarak antar lokasi (dalam meter)
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
        m_point = expand(f_queue, f_visited, b_visited)
        if m_point: return construct_path(graph, f_visited, b_visited, m_point)
        m_point = expand(b_queue, b_visited, f_visited)
        if m_point: return construct_path(graph, f_visited, b_visited, m_point)
    return None, 0

def construct_path(graph, f_visited, b_visited, meet):
    path, node, total_dist = [], meet, 0
    while node: path.append(node); prev = f_visited[node]; total_dist += graph.get(prev, {}).get(node, 0) if prev else 0; node = prev
    path.reverse(); node = b_visited[meet]
    while node: path.append(node); prev = b_visited[node]; total_dist += graph[node][prev] if prev else 0; node = prev
    return path, total_dist

def bfs(graph, start, goal):
    queue, visited = deque([start]), set()
    while queue:
        node = queue.popleft()
        if node == goal: return True
        if node not in visited:
            visited.add(node)
            queue.extend(graph.get(node, {}).keys())
    return False

print("=== Penelusuran Rute Kampus UNIB ===")
print("Daftar lokasi:")
for i, key in enumerate(graph.keys(), 1):
    print(f"{i}. {key}")

start = input("\nMasukkan titik awal: ")
goal = input("Masukkan tujuan akhir: ")

if start not in graph or goal not in graph:
    print("Lokasi tidak valid. Pastikan penulisan sesuai daftar.")
else:
    tracemalloc.start()
    t0 = time.time()
    if bfs(graph, start, goal):
        print(f"\n✅ Ada jalur dari {start} ke {goal}")
        path, dist = bidirectional_search(graph, start, goal)
        print("🛣  Rute Terpendek:")
        print(" -> ".join(path))
        speed = 1.4  # m/s
        waktu = dist / speed
        menit, detik = divmod(int(waktu), 60)
        print(f"📏 Total Jarak: {dist} meter")
        print(f"⏱️ Estimasi waktu tempuh: {menit} menit {detik} detik")
    else:
        print(f"\n❌ TIDAK ADA jalur dari {start} ke {goal}")
    t1 = time.time()
    mem_now, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print("\n=== ANALISIS ALGORITMA ===")
    print("Algoritma       : Bidirectional Search")
    print(f"Time Complexity : {t1 - t0:.6f} detik")
    print(f"Space Complexity: {mem_peak / 1024:.2f} KB (memori puncak)")
