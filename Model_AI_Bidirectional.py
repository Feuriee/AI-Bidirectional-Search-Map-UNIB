import tkinter as tk
from tkinter import ttk, messagebox
import time
import tracemalloc
from collections import deque
import datetime

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

# Kecepatan moda transportasi dalam meter/detik
transport_speeds = {
    'Jalan Kaki': 1.4,
    'Sepeda': 5.0,
    'Sepeda Motor': 8.3
}

def get_modified_graph(day_type, time_hour):
    modified_graph = {key: value.copy() for key, value in graph.items()}
    
    # Malam hari (18:00 - 06:00)
    if time_hour < 6 or time_hour >= 18:
        # Hapus gerbang yang tutup dari graph
        for node in list(modified_graph.keys()):
            # Hapus koneksi ke gerbang-gerbang yang tutup
            if node in ['Gerbang Masuk 1', 'Gerbang Keluar 1', 'Gerbang Masuk 2', 'Gerbang Keluar 3']:
                # Hapus koneksi dari node lain ke gerbang tutup
                for other_node in modified_graph:
                    if node in modified_graph[other_node]:
                        del modified_graph[other_node][node]
    
    # Hari kerja (Senin - Jumat)
    if day_type == "Weekday":
        # Ubah Gerbang Keluar 2 menjadi gerbang masuk
        if 'Gerbang Keluar 2' in modified_graph:
            # Tidak ada perubahan khusus selain nama, logika penggunaan tetap sama
            pass
    
    # Weekend
    elif day_type == "Weekend":
        # Tutup Gerbang Keluar 3
        if 'Gerbang Keluar 3' in modified_graph:
            for node in modified_graph:
                if 'Gerbang Keluar 3' in modified_graph[node]:
                    del modified_graph[node]['Gerbang Keluar 3']
    
    return modified_graph

def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start], 0
    
    # Inisialisasi antrian dan kunjungan dari depan dan belakang
    f_queue, b_queue = deque([start]), deque([goal])
    f_visited, b_visited = {start: None}, {goal: None}
    
    while f_queue and b_queue:
        # Fungsi untuk memperluas pencarian dari satu arah
        def expand(queue, visited, other_visited):
            node = queue.popleft()
            for neighbor in graph.get(node, {}):
                if neighbor not in visited:
                    visited[neighbor] = node
                    queue.append(neighbor)
                    if neighbor in other_visited:
                        return neighbor
            return None
        
        # Ekspansi dari depan
        meeting_point = expand(f_queue, f_visited, b_visited)
        if meeting_point:
            return construct_path(graph, f_visited, b_visited, meeting_point)
        
        # Ekspansi dari belakang
        meeting_point = expand(b_queue, b_visited, f_visited)
        if meeting_point:
            return construct_path(graph, f_visited, b_visited, meeting_point)
    
    return None, 0

def construct_path(graph, f_visited, b_visited, meet):
    # Konstruksi jalur dari awal ke titik temu
    path, node, total_dist = [], meet, 0
    while node:
        path.append(node)
        prev = f_visited[node]
        total_dist += graph.get(prev, {}).get(node, 0) if prev else 0
        node = prev
    
    # Balik jalur karena kita merunutnya dari akhir ke awal
    path.reverse()
    
    # Konstruksi jalur dari titik temu ke tujuan
    node = b_visited[meet]
    while node:
        path.append(node)
        prev = b_visited[node]
        total_dist += graph[node][prev] if prev else 0
        node = prev
    
    return path, total_dist

def bfs(graph, start, goal):
    # Cek apakah ada jalur dari start ke goal
    queue, visited = deque([start]), set()
    while queue:
        node = queue.popleft()
        if node == goal:
            return True
        if node not in visited:
            visited.add(node)
            queue.extend(graph.get(node, {}).keys())
    return False

def calculate_complexity_metrics(graph):
    # Calculate graph metrics for complexity analysis
    node_count = len(graph)
    edge_count = sum(len(edges) for edges in graph.values())
    
    # Calculate average branching factor
    branching_factor = edge_count / node_count if node_count > 0 else 0
    
    return {
        'node_count': node_count,
        'edge_count': edge_count,
        'branching_factor': branching_factor
    }

def run_algorithm_analysis(graph, start, goal):
    results = {}
    
    # Check path eksis
    tracemalloc.start()
    start_time = time.time()
    
    # Cek apakah ada algoritma yang berjalan
    connected = bfs(graph, start, goal)
    if not connected:
        tracemalloc.stop()
        return None
    
    # Run bidirectional search
    path, distance = bidirectional_search(graph, start, goal)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Store results
    results['path'] = path
    results['distance'] = distance
    results['time'] = end_time - start_time
    results['memory'] = peak / 1024  # KB
    
    # Kalkulasi complexity metrics
    metrics = calculate_complexity_metrics(graph)
    results['node_count'] = metrics['node_count']
    results['edge_count'] = metrics['edge_count']
    results['branching_factor'] = metrics['branching_factor']
    
    # Panjang path
    results['path_length'] = len(path) if path else 0
    
    return results

class UnibRouteFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pencari Rute Kampus UNIB")
        self.root.geometry("800x620")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame utama
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(expand=True, fill="both")
        
        # Judul
        title_label = ttk.Label(main_frame, text="Pencari Rute Kampus UNIB", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")
        
        # Frame untuk input
        input_frame = ttk.LabelFrame(main_frame, text="Parameter Input", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        
        # Lokasi awal
        ttk.Label(input_frame, text="Lokasi Awal:").grid(row=0, column=0, sticky="w", pady=5)
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(input_frame, textvariable=self.start_var, width=30)
        self.start_combo['values'] = list(graph.keys())
        self.start_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Lokasi tujuan
        ttk.Label(input_frame, text="Lokasi Tujuan:").grid(row=1, column=0, sticky="w", pady=5)
        self.goal_var = tk.StringVar()
        self.goal_combo = ttk.Combobox(input_frame, textvariable=self.goal_var, width=30)
        self.goal_combo['values'] = list(graph.keys())
        self.goal_combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Pilihan transportasi
        ttk.Label(input_frame, text="Moda Transportasi:").grid(row=2, column=0, sticky="w", pady=5)
        self.transport_var = tk.StringVar(value="Jalan Kaki")
        transport_frame = ttk.Frame(input_frame)
        transport_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        modes = list(transport_speeds.keys())
        for i, mode in enumerate(modes):
            ttk.Radiobutton(transport_frame, text=mode, variable=self.transport_var, value=mode).grid(row=0, column=i, padx=5)
        
        # Frame untuk waktu dan hari
        time_frame = ttk.LabelFrame(main_frame, text="Pengaturan Waktu & Hari", padding="10")
        time_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5)
        
        # Pilihan hari
        ttk.Label(time_frame, text="Hari:").grid(row=0, column=0, sticky="w", pady=5)
        self.day_var = tk.StringVar(value="Weekend")
        day_frame = ttk.Frame(time_frame)
        day_frame.grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Radiobutton(day_frame, text="Hari Kerja (Sen-Jum)", variable=self.day_var, value="Weekday").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(day_frame, text="Akhir Pekan (Sab-Min)", variable=self.day_var, value="Weekend").grid(row=0, column=1, padx=5)
        
        # Pilihan waktu
        ttk.Label(time_frame, text="Waktu:").grid(row=1, column=0, sticky="w", pady=5)
        
        time_input_frame = ttk.Frame(time_frame)
        time_input_frame.grid(row=1, column=1, sticky="w", pady=5)
        
        self.hour_var = tk.StringVar(value="08")
        self.minute_var = tk.StringVar(value="00")
        
        ttk.Label(time_input_frame, text="Jam:").grid(row=0, column=0, sticky="w")
        hour_combo = ttk.Combobox(time_input_frame, textvariable=self.hour_var, width=5)
        hour_combo['values'] = [f"{i:02d}" for i in range(24)]
        hour_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(time_input_frame, text="Menit:").grid(row=0, column=2, sticky="w")
        minute_combo = ttk.Combobox(time_input_frame, textvariable=self.minute_var, width=5)
        minute_combo['values'] = [f"{i:02d}" for i in range(0, 60, 5)]
        minute_combo.grid(row=0, column=3, padx=5)
        
        # Frame untuk tombol-tombol
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Tombol Cari Rute
        find_button = ttk.Button(button_frame, text="Cari Rute", command=self.find_route)
        find_button.grid(row=0, column=0, padx=10)
        
        # Tombol Analisis
        analyze_button = ttk.Button(button_frame, text="Tampilkan Analisis Algoritma", command=self.show_analysis)
        analyze_button.grid(row=0, column=1, padx=10)
        
        # Tombol Reset
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset)
        reset_button.grid(row=0, column=2, padx=10)
        
        # Frame untuk output
        self.output_frame = ttk.LabelFrame(main_frame, text="Hasil", padding="10")
        self.output_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=5)
        
        # Text widget untuk output
        self.output_text = tk.Text(self.output_frame, wrap="word", width=80, height=15)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.output_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        self.output_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Inisialisasi variabel untuk menyimpan hasil analisis
        self.analysis_results = None
        
    def find_route(self):
        start_location = self.start_var.get()
        goal_location = self.goal_var.get()
        transport_mode = self.transport_var.get()
        day_type = self.day_var.get()
        time_hour = int(self.hour_var.get())
        
        if not start_location or not goal_location:
            messagebox.showerror("Error", "Silakan pilih lokasi awal dan tujuan")
            return
        
        # Hapus output sebelumnya
        self.output_text.delete(1.0, tk.END)
        
        # Perbarui status
        self.status_var.set(f"Mencari rute dari {start_location} ke {goal_location}...")
        self.root.update()
        
        # Dapatkan graph yang dimodifikasi berdasarkan waktu dan hari
        current_graph = get_modified_graph(day_type, time_hour)
        
        # Cek apakah kedua lokasi ada di graph yang dimodifikasi
        if start_location not in current_graph or goal_location not in current_graph:
            self.output_text.insert(tk.END, "Satu atau kedua lokasi yang dipilih tidak dapat diakses pada waktu yang ditentukan.\n")
            self.status_var.set("Pencarian rute gagal - lokasi tidak dapat diakses")
            return
        
        # Cek apakah ada jalur
        if not bfs(current_graph, start_location, goal_location):
            self.output_text.insert(tk.END, f"❌ Tidak ditemukan rute dari {start_location} ke {goal_location} pada waktu yang ditentukan.\n")
            self.status_var.set("Rute tidak ditemukan")
            return
        
        # Temukan rute
        path, distance = bidirectional_search(current_graph, start_location, goal_location)
        
        if path:
            # Hitung waktu berdasarkan moda transportasi
            speed = transport_speeds[transport_mode]
            time_seconds = distance / speed
            minutes, seconds = divmod(int(time_seconds), 60)
            
            # Tampilkan hasil
            self.output_text.insert(tk.END, f"✅ Rute ditemukan dari {start_location} ke {goal_location}\n\n")
            self.output_text.insert(tk.END, "🛣️ Rute:\n")
            self.output_text.insert(tk.END, " -> ".join(path) + "\n\n")
            self.output_text.insert(tk.END, f"📏 Total Jarak: {distance} meter\n")
            self.output_text.insert(tk.END, f"🚶 Moda Transportasi: {transport_mode}\n")
            self.output_text.insert(tk.END, f"⏱️ Estimasi Waktu: {minutes} menit {seconds} detik\n\n")
            
            # Informasi waktu dan hari
            time_str = f"{self.hour_var.get()}:{self.minute_var.get()}"
            self.output_text.insert(tk.END, f"⏰ Waktu: {time_str}\n")
            self.output_text.insert(tk.END, f"📅 Hari: {day_type}\n\n")
            
            # Informasi status gerbang
            self.output_text.insert(tk.END, "🚧 Status Gerbang:\n")
            if time_hour < 6 or time_hour >= 18:
                self.output_text.insert(tk.END, "- Gerbang Masuk 1: Tutup (18:00-06:00)\n")
                self.output_text.insert(tk.END, "- Gerbang Keluar 1: Tutup (18:00-06:00)\n")
                self.output_text.insert(tk.END, "- Gerbang Masuk 2: Tutup (18:00-06:00)\n")
                self.output_text.insert(tk.END, "- Gerbang Keluar 3: Tutup (18:00-06:00)\n")
                self.output_text.insert(tk.END, "- Gerbang Masuk 3: Buka\n")
                self.output_text.insert(tk.END, "- Gerbang Keluar 2: Buka\n")
            else:
                self.output_text.insert(tk.END, "- Gerbang Masuk 1: Buka\n")
                self.output_text.insert(tk.END, "- Gerbang Keluar 1: Buka\n")
                self.output_text.insert(tk.END, "- Gerbang Masuk 2: Buka\n")
                self.output_text.insert(tk.END, "- Gerbang Masuk 3: Buka\n")
                
                if day_type == "Hari Kerja":
                    self.output_text.insert(tk.END, "- Gerbang Keluar 2: Digunakan sebagai pintu masuk (Hari Kerja)\n")
                    self.output_text.insert(tk.END, "- Gerbang Keluar 3: Buka\n")
                else:  # Akhir Pekan
                    self.output_text.insert(tk.END, "- Gerbang Keluar 2: Buka\n")
                    self.output_text.insert(tk.END, "- Gerbang Keluar 3: Tutup (Akhir Pekan)\n")
            
            # Jalankan analisis
            self.analysis_results = run_algorithm_analysis(current_graph, start_location, goal_location)
            
            self.status_var.set("Rute berhasil ditemukan")
        else:
            self.output_text.insert(tk.END, f"❌ Tidak ditemukan rute dari {start_location} ke {goal_location}.\n")
            self.status_var.set("Rute tidak ditemukan")
    
    def show_analysis(self):
        if not self.analysis_results:
            messagebox.showinfo("Analisis", "Silakan cari rute terlebih dahulu sebelum melihat analisis.")
            return
        
        # Buat jendela baru untuk analisis
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Analisis Algoritma")
        analysis_window.geometry("600x500")
        
        # Buat frame untuk konten analisis
        analysis_frame = ttk.Frame(analysis_window, padding=10)
        analysis_frame.pack(expand=True, fill='both')
        
        # Text widget untuk hasil
        text_output = tk.Text(analysis_frame, wrap="word", width=70, height=25)
        text_output.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(analysis_frame, orient="vertical", command=text_output.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_output.configure(yscrollcommand=scrollbar.set)
        
        # Format nilai kompleksitas
        node_count = self.analysis_results['node_count']
        edge_count = self.analysis_results['edge_count']
        branching_factor = self.analysis_results['branching_factor']
        path_length = self.analysis_results['path_length']
        
        # Display results
        # Menampilkan hasil
        text_output.insert(tk.END, "=== ANALISIS ALGORITMA ===\n\n")
        text_output.insert(tk.END, "Algoritma: Pencarian Dua Arah (Bidirectional Search)\n\n")

        text_output.insert(tk.END, "Properti Graf:\n")
        text_output.insert(tk.END, f"- Jumlah simpul (nodes): {node_count}\n")
        text_output.insert(tk.END, f"- Jumlah sisi (edges): {edge_count}\n")
        text_output.insert(tk.END, f"- Rata-rata faktor percabangan: {branching_factor:.2f}\n")
        text_output.insert(tk.END, f"- Panjang jalur: {path_length} simpul\n\n")

        text_output.insert(tk.END, "Metode Pengukuran Performa:\n")
        text_output.insert(tk.END, f"- Waktu eksekusi: {self.analysis_results['time']:.6f} detik\n")
        text_output.insert(tk.END, f"- Penggunaan memori: {self.analysis_results['memory']:.2f} KB\n\n")

        # Configure grid weights
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(0, weight=1)
        
        # Add a close button
        close_button = ttk.Button(analysis_frame, text="Tutup", command=analysis_window.destroy)
        close_button.grid(row=1, column=0, pady=10)
    
    def reset(self):
        # Reset all input fields
        self.start_var.set("")
        self.goal_var.set("")
        self.transport_var.set("Jalan Kaki")
        self.day_var.set("Weekend")
        self.hour_var.set("08")
        self.minute_var.set("00")
        
        # Clear output text
        self.output_text.delete(1.0, tk.END)
        
        # Reset status
        self.status_var.set("Ready")
        
        # Reset analysis results
        self.analysis_results = None

if __name__ == "__main__":
    root = tk.Tk()
    app = UnibRouteFinderApp(root)
    root.mainloop()
