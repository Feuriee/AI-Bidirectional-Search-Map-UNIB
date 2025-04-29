import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import webbrowser
import networkx as nx
import openrouteservice
import folium
import os
import time
import math
import tracemalloc
import sys
from itertools import combinations
from datetime import datetime

# === Data Koordinat UNIB ===
coordinates = {
    "Rektorat": [-3.7590495172423495, 102.27231460986346],
    'Masjid Darul Ulum': [-3.757594, 102.267707],
    'Fakultas Hukum': [-3.760628, 102.268349],
    'Magister Akuntansi': [-3.761804, 102.268806],
    'Fakultas Ekonomi dan Bisnis': [-3.7617198090691164, 102.26862389169713],
    'Gedung 1': [-3.760152, 102.270047],
    'GOR UNIB': [-3.760763, 102.267672],
    'Lab. Pertanian': [-3.7585179, 102.2689226],
    'Gedung R UPT Bahasa': [-3.7607479, 102.2703659],
    'Fakultas Pertanian': [-3.7595105, 102.2692443],
    'Klinik Pratama UNIB': [-3.7612637, 102.2719374],
    'Fakultas Ilmu Sosial dan Ilmu Politik': [-3.7591970, 102.2746466],
    'GLT': [-3.7581473, 102.2720357],
    'Lab. Kehutanan dan Ilmu Lingkungan': [-3.7579898, 102.2724654],
    'Danau UNIB': [-3.75821649, 102.27301278],
    'Lab. Bio, Fisika dan Kimia': [-3.75608452, 102.27357731],
    'GB1': [-3.76002480, 102.26986519],
    'GB2': [-3.7578575751002457, 102.274037554275],
    'Perpus UNIB': [-3.75717114, 102.27483064],
    'Fakultas Keguruan dan Ilmu Pendidikan': [-3.75740598, 102.27513947],
    'LPTIK': [-3.75828163, 102.27496492],
    'Lab. FKIP': [-3.75844345, 102.27574886],
    'Fakultas Teknik': [-3.75846893, 102.27665736],
    'Masjid Baitul Hikmah': [-3.75910765, 102.27609130],
    'Gedung Serba Guna': [-3.7579609, 102.2765348],
    'Lab. Terpadu Teknik': [-3.75858798, 102.27719504],
    'Magister FKIP': [-3.7565071, 102.2774714],
    'Stadion UNIB': [-3.7572898, 102.2781438],
    'GB3 dan 4': [-3.7564116, 102.2766278],
    'Gedung PKM': [-3.7565600, 102.2757768],
    'GB5': [-3.7555961, 102.2764859],
    'Fakultas Kedokteran': [-3.7551956, 102.2780187],
    'Fakultas Matematika dan Ilmu Pengetahuan Alam': [-3.7559771, 102.27485175],
    'Gerbang Masuk 1': [-3.759933, 102.267244],
    'Gerbang Masuk 2': [-3.76065782, 102.272668575],
    'Gerbang Masuk 3': [-3.75960389, 102.27510884],
    'Gerbang Keluar 1': [-3.75868214, 102.26694025],
    'Gerbang Keluar 2': [-3.75955438, 102.27518921],
    'Gerbang Keluar 3': [-3.75938105, 102.27624033],
}

# === Kecepatan berdasarkan moda transportasi (dalam m/s) ===
transport_speeds = {
    "Jalan Kaki": 1.4,
    "Sepeda": 4.2,
    "Sepeda Motor": 8.3
}

# === Graph Berdasarkan Jarak Euclidean < 200m ===
def haversine(coord1, coord2):
    R = 6371e3
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

G = nx.Graph()
for a, b in combinations(coordinates, 2):
    dist = haversine(coordinates[a], coordinates[b])
    if dist < 200:
        G.add_edge(a, b, weight=dist)

# === Gerbang Rules ===
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

def filter_graph_by_time(graph, jam, hari):
    gate_status = status_gerbang(jam, hari)
    Gf = nx.Graph()
    for u, v, d in graph.edges(data=True):
        if ("Gerbang" in u and gate_status.get(u, "Buka") != "Buka") or ("Gerbang" in v and gate_status.get(v, "Buka") != "Buka"):
            continue
        Gf.add_edge(u, v, weight=d['weight'])
    return Gf

# === Algoritma ===
client = openrouteservice.Client(key='5b3ce3597851110001cf62486e58c245d2f740bfa1bdd46cbab8ed58')

def get_ors_route(coord1, coord2, transport_mode):
    # Mapping moda transportasi ke profil ORS
    ors_profiles = {
        "Jalan Kaki": "foot-walking",
        "Sepeda": "cycling-regular",
        "Sepeda Motor": "driving-car"  # ORS tidak punya sepeda motor khusus, jadi gunakan driving-car
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

def find_route_bds(start, goal, jam, hari):
    # Start memory tracking
    tracemalloc.start()
    
    # Filter graph based on time and day
    Gf = filter_graph_by_time(G, jam, hari)
    
    start_time = time.time()
    visited = 0  # Track visited nodes for complexity analysis
    
    try:
        # Count visited nodes during algorithm execution
        def bidirectional_shortest_path_with_count(G, source, target):
            nonlocal visited
            if source not in G or target not in G:
                raise nx.NetworkXNoPath(f"Either source {source} or target {target} is not in G")
            
            # Initialize forward and backward frontiers and paths
            forward_paths = {source: [source]}
            backward_paths = {target: [target]}
            forward_seen = {source}
            backward_seen = {target}
            
            # Main search loop
            while forward_paths and backward_paths:
                # Process forward frontier
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
                                    # Found an intersection, build the full path
                                    backward_path = backward_paths[v]
                                    return new_path[:-1] + backward_path[::-1]
                    forward_paths = new_forward_paths
                # Process backward frontier
                else:
                    new_backward_paths = {}
                    for u, path in backward_paths.items():
                        visited += 1
                        for v in G[u]:
                            if v not in backward_seen:
                                backward_seen.add(v)
                                new_path = path + [v]
                                new_backward_paths[v] = new_path
                                if v in forward_seen:
                                    # Found an intersection, build the full path
                                    forward_path = forward_paths[v]
                                    return forward_path + new_path[1:][::-1]
                    backward_paths = new_backward_paths
            
            # No path found
            raise nx.NetworkXNoPath(f"No path between {source} and {target}")
        
        # Run the algorithm with node counting
        path = bidirectional_shortest_path_with_count(Gf, start, goal)
        dist = sum(Gf[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        coords = [coordinates[p] for p in path]
        
    except nx.NetworkXNoPath:
        path = None
        dist = None
        coords = None
    
    # Calculate time complexity approximately as O(E) where E is edges visited
    time_complexity = f"O({visited})"
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Get memory peak
    current, peak = tracemalloc.get_traced_memory()
    
    # Stop memory tracking
    tracemalloc.stop()
    
    return {
        "path": path,
        "coords": coords,
        "dist": dist,
        "time": execution_time,
        "time_complexity": time_complexity,
        "memory_peak": peak / 1024  # KB
    }

def find_route(start, goal, jam, hari, transport_mode, show_map=False):
    if show_map:
        # Menggunakan ORS untuk visual map tetapi tetap dinamai BDS
        start_time = time.time()
        
        # Start memory tracking
        tracemalloc.start()
        
        ors_coords, ors_dist = get_ors_route(coordinates[start], coordinates[goal], transport_mode)
        
        # Kalkulasi penggunaan memori
        current, peak = tracemalloc.get_traced_memory()
        
        # Stop memory tracking
        tracemalloc.stop()
        
        execution_time = time.time() - start_time
        
        # Estimasi time complexity untuk ORS API call: O(1) dari sisi client
        time_complexity = "O(1) - API Call"
        
        return {
            "path": None,  # ORS tidak memberikan path dalam format node
            "coords": ors_coords,
            "dist": ors_dist,
            "time": execution_time,
            "time_complexity": time_complexity,
            "memory_peak": peak / 1024  # KB
        }
    else:
        # Menggunakan BDS murni tanpa visualisasi map
        return find_route_bds(start, goal, jam, hari)

# === GUI ===
class NavigasiKampusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Navigasi Kampus UNIB")
        self.root.geometry("600x750")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
        self.hasil_rute = None
        
    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#1e3d59", height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Navigasi Kampus UNIB", 
                              font=("Arial", 24, "bold"), fg="white", bg="#1e3d59")
        title_label.pack(pady=20)
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Input Frame
        input_frame = tk.LabelFrame(main_frame, text="Input Pencarian", 
                                   font=("Arial", 12, "bold"), bg="#f0f0f0", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Lokasi Frame
        lokasi_frame = tk.Frame(input_frame, bg="#f0f0f0")
        lokasi_frame.pack(fill=tk.X, pady=5)
        
        lokasi_frame.columnconfigure(0, weight=1)
        lokasi_frame.columnconfigure(1, weight=1)
        
        sorted_locations = sorted(coordinates.keys())
        
        # Titik Awal
        awal_label = tk.Label(lokasi_frame, text="Titik Awal", font=("Arial", 11), bg="#f0f0f0")
        awal_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.start_var = tk.StringVar()
        start_combo = ttk.Combobox(lokasi_frame, textvariable=self.start_var, values=sorted_locations, 
                                  state="readonly", width=30)
        start_combo.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        
        # Titik Tujuan
        tujuan_label = tk.Label(lokasi_frame, text="Titik Tujuan", font=("Arial", 11), bg="#f0f0f0")
        tujuan_label.grid(row=0, column=1, sticky="w", pady=5)
        
        self.goal_var = tk.StringVar()
        goal_combo = ttk.Combobox(lokasi_frame, textvariable=self.goal_var, values=sorted_locations, 
                                 state="readonly", width=30)
        goal_combo.grid(row=1, column=1, sticky="w", pady=5)
        
        # Waktu dan Transportasi Frame
        waktu_frame = tk.Frame(input_frame, bg="#f0f0f0")
        waktu_frame.pack(fill=tk.X, pady=10)
        
        waktu_frame.columnconfigure(0, weight=1)
        waktu_frame.columnconfigure(1, weight=1)
        waktu_frame.columnconfigure(2, weight=1)
        
        # Hari
        hari_label = tk.Label(waktu_frame, text="Hari", font=("Arial", 11), bg="#f0f0f0")
        hari_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.day_var = tk.StringVar(value="weekday")
        day_combo = ttk.Combobox(waktu_frame, textvariable=self.day_var, 
                                values=["weekday", "weekend"], state="readonly", width=20)
        day_combo.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        
        # Jam
        jam_label = tk.Label(waktu_frame, text="Jam (0-23)", font=("Arial", 11), bg="#f0f0f0")
        jam_label.grid(row=0, column=1, sticky="w", pady=5)
        
        self.time_var = tk.StringVar(value="10")
        time_entry = ttk.Entry(waktu_frame, textvariable=self.time_var, width=20)
        time_entry.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=5)
        
        # Transportasi
        transport_label = tk.Label(waktu_frame, text="Moda Transportasi", font=("Arial", 11), bg="#f0f0f0")
        transport_label.grid(row=0, column=2, sticky="w", pady=5)
        
        self.transport_var = tk.StringVar(value="Jalan Kaki")
        transport_combo = ttk.Combobox(waktu_frame, textvariable=self.transport_var, 
                                      values=list(transport_speeds.keys()), state="readonly", width=20)
        transport_combo.grid(row=1, column=2, sticky="w", pady=5)
        
        # Display Options Frame
        display_frame = tk.LabelFrame(input_frame, text="Opsi Tampilan", 
                                     font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10)
        display_frame.pack(fill=tk.X, pady=10)
        
        # Tampilkan Map Checkbox
        self.show_map_var = tk.BooleanVar(value=True)
        show_map_check = ttk.Checkbutton(display_frame, text="Tampilkan Map", variable=self.show_map_var)
        show_map_check.grid(row=0, column=0, sticky="w", pady=5)
        
        # Tampilkan Semua Titik Checkbox
        self.show_all_points_var = tk.BooleanVar(value=False)
        show_all_points_check = ttk.Checkbutton(display_frame, text="Tampilkan Semua Titik", 
                                               variable=self.show_all_points_var)
        show_all_points_check.grid(row=0, column=1, sticky="w", pady=5, padx=(20, 0))
        
        # Tampilkan Titik Rute Checkbox
        self.show_route_points_var = tk.BooleanVar(value=False)
        show_route_points_check = ttk.Checkbutton(display_frame, text="Tampilkan Titik Rute", 
                                                 variable=self.show_route_points_var)
        show_route_points_check.grid(row=1, column=0, sticky="w", pady=5)
        
        # Buttons Frame
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Tampilkan Rute Button
        self.route_button = ttk.Button(
            buttons_frame, 
            text="Tampilkan Rute", 
            command=self.show_route,
            style="AccentButton.TButton",
            width=20
        )
        self.route_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Analisis Algoritma Button
        self.analysis_button = ttk.Button(
            buttons_frame, 
            text="Analisis Algoritma", 
            command=self.show_analysis,
            style="TButton",
            width=20
        )
        self.analysis_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Tampilkan Semua Lokasi
        self.show_all_button = ttk.Button(
            buttons_frame, 
            text="Lihat Semua Lokasi", 
            command=self.show_all_locations,
            style="TButton",
            width=20
        )
        self.show_all_button.pack(side=tk.LEFT)
        
        # Results Frame
        self.result_frame = tk.LabelFrame(
            main_frame, 
            text="Hasil", 
            font=("Arial", 12, "bold"), 
            bg="#f0f0f0", 
            padx=10, 
            pady=10
        )
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Results Text
        self.result_text = tk.Text(
            self.result_frame, 
            wrap=tk.WORD, 
            width=50, 
            height=15, 
            font=("Arial", 11),
            bg="#ffffff",
            padx=10,
            pady=10
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Status Bar
        self.status_bar = tk.Label(
            self.root, 
            text="© 2025 Navigasi Kampus UNIB", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=("Arial", 9),
            bg="#e8e8e8"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Apply custom styles
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 11))
        style.configure("AccentButton.TButton", font=("Arial", 11, "bold"), background="#ffc13b")
        
    def validate_inputs(self):
        start = self.start_var.get()
        goal = self.goal_var.get()
        jam_str = self.time_var.get()
        
        if not start or not goal:
            messagebox.showerror("Input Error", "Pilih titik awal dan tujuan!")
            return False
            
        if start == goal:
            messagebox.showerror("Input Error", "Titik awal dan tujuan tidak boleh sama!")
            return False
        
        try:
            jam = int(jam_str)
            if not (0 <= jam <= 23):
                messagebox.showerror("Input Error", "Jam harus antara 0-23!")
                return False
        except ValueError:
            messagebox.showerror("Input Error", "Jam harus berupa angka!")
            return False
            
        return True
    
    def calculate_route(self):
        start = self.start_var.get()
        goal = self.goal_var.get()
        jam = int(self.time_var.get())
        hari = self.day_var.get()
        transport = self.transport_var.get()
        show_map = self.show_map_var.get()
        
        self.status_bar.config(text="Mencari rute... Harap tunggu")
        self.root.update()
        
        # Find route dengan BDS (atau ORS yang dinamai BDS jika show_map=True)
        hasil = find_route(start, goal, jam, hari, transport, show_map)
        self.hasil_rute = hasil
        
        self.status_bar.config(text="© 2025 Navigasi Kampus UNIB")
        return hasil
    
    def show_route(self):
        if not self.validate_inputs():
            return
            
        hasil = self.calculate_route()
        
        if not hasil["coords"]:
            messagebox.showerror("Error", "Rute tidak ditemukan!")
            return
        
        coords = hasil["coords"]
        dist = hasil["dist"]
        transport = self.transport_var.get()
        jam = int(self.time_var.get())
        hari = self.day_var.get()
        
        # Visualisasi jika show_map diaktifkan
        if self.show_map_var.get():
            start = self.start_var.get()
            goal = self.goal_var.get()
            
            # Pilih warna berdasarkan moda transportasi
            route_colors = {
                "Jalan Kaki": "blue",
                "Sepeda": "green",
                "Sepeda Motor": "red"
            }
            color = route_colors.get(transport, "blue")
            
            m = folium.Map(location=coordinates[start], zoom_start=16)
            
            # Tambahkan marker untuk titik awal dan tujuan
            folium.Marker(coordinates[start], tooltip=f"Start: {start}", 
                         icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(coordinates[goal], tooltip=f"Goal: {goal}", 
                         icon=folium.Icon(color='red')).add_to(m)
            
            # Tambahkan polyline untuk rute
            folium.PolyLine(coords, color=color, weight=5, 
                           tooltip=f"BDS - {dist:.2f} m").add_to(m)
            
            # Jika opsi tampilkan semua titik aktif
            if self.show_all_points_var.get():
                for name, coord in coordinates.items():
                    if name != start and name != goal:
                        folium.Marker(
                            coord, 
                            tooltip=name,
                            icon=folium.Icon(color='gray', icon='info-sign', prefix='fa')
                        ).add_to(m)
            
            # Jika opsi tampilkan titik rute aktif dan ada path
            if self.show_route_points_var.get() and hasil["path"]:
                path = hasil["path"]
                # Tampilkan semua titik dalam path kecuali awal dan akhir (sudah ditampilkan)
                for i, point_name in enumerate(path):
                    if i > 0 and i < len(path) - 1:  # Skip awal dan akhir
                        folium.Marker(
                            coordinates[point_name], 
                            tooltip=f"Via: {point_name}",
                            icon=folium.Icon(color='blue', icon='info-sign', prefix='fa')
                        ).add_to(m)
            
            m.save("rute_kampus.html")
            webbrowser.open("file://" + os.path.realpath("rute_kampus.html"))

        # Menampilkan informasi rute pada text widget
        est_time = (dist / transport_speeds[transport]) / 60  # berdasarkan kecepatan transportasi
        gate_stat = status_gerbang(jam, hari)
        gate_info = "\n".join([f"• {k}: {v}" for k, v in gate_stat.items()])

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"INFORMASI RUTE:\n", "header")
        self.result_text.insert(tk.END, f"\nMetode: BDS\n")
        self.result_text.insert(tk.END, f"Moda Transportasi: {transport}\n")
        self.result_text.insert(tk.END, f"Jarak: {dist:.2f} meter\n")
        self.result_text.insert(tk.END, f"Estimasi waktu: {est_time:.2f} menit\n")
        
        # Menampilkan path jika ada
        if hasil["path"]:
            self.result_text.insert(tk.END, f"\nRUTE DETAIL:\n", "header")
            for i, point in enumerate(hasil["path"]):
                if i < len(hasil["path"]) - 1:
                    next_point = hasil["path"][i+1]
                    segment_dist = haversine(coordinates[point], coordinates[next_point])
                    self.result_text.insert(tk.END, f"{i+1}. {point} → {next_point} ({segment_dist:.2f} m)\n")
                else:
                    self.result_text.insert(tk.END, f"{i+1}. {point} (Tujuan)\n")
        
        self.result_text.insert(tk.END, f"\nSTATUS GERBANG:\n", "header")
        self.result_text.insert(tk.END, f"{gate_info}\n")
        
        # Apply text tags
        self.result_text.tag_configure("header", font=("Arial", 11, "bold"))
    
    def show_analysis(self):
        if not self.validate_inputs():
            return
            
        if not self.hasil_rute:
            self.hasil_rute = self.calculate_route()
            
        if not self.hasil_rute["coords"]:
            messagebox.showerror("Error", "Rute tidak ditemukan untuk analisis!")
            return
        
        # Hitung analisis tambahan berdasarkan moda transportasi
        transport = self.transport_var.get()
        dist = self.hasil_rute["dist"]
        
        # Estimasi waktu tempuh dalam menit
        est_time = (dist / transport_speeds[transport]) / 60
        
        # Konsumsi energi dan emisi (simulasi sederhana)
        energy_consumption = {
            "Jalan Kaki": f"{dist * 0.06:.2f} kalori",
            "Sepeda": f"{dist * 0.04:.2f} kalori",
            "Sepeda Motor": f"{dist * 0.05:.2f} liter BBM"
        }
        
        emission = {
            "Jalan Kaki": "0 gram CO2",
            "Sepeda": "0 gram CO2",
            "Sepeda Motor": f"{dist * 0.07:.2f} gram CO2"
        }
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"ANALISIS ALGORITMA:\n", "header")
        self.result_text.insert(tk.END, f"\nModa Transportasi: {transport}\n")
        self.result_text.insert(tk.END, f"Jarak: {dist:.2f} meter\n")
        self.result_text.insert(tk.END, f"Estimasi waktu tempuh: {est_time:.2f} menit\n")
        self.result_text.insert(tk.END, f"Konsumsi energi: {energy_consumption[transport]}\n")
        self.result_text.insert(tk.END, f"Emisi karbon: {emission[transport]}\n\n")
        
        self.result_text.insert(tk.END, f"KOMPLEKSITAS ALGORITMA:\n", "header")
        self.result_text.insert(tk.END, f"Time Complexity: {self.hasil_rute['time_complexity']}\n")
        self.result_text.insert(tk.END, f"Memory Peak: {self.hasil_rute['memory_peak']:.2f} KB\n")
        self.result_text.insert(tk.END, f"Execution Time: {self.hasil_rute['time'] * 1000:.2f} ms\n\n")
        
        self.result_text.insert(tk.END, f"PERBANDINGAN ALGORITMA:\n", "header")
        self.result_text.insert(tk.END, f"BDS vs Dijkstra:\n")
        self.result_text.insert(tk.END, f"• BDS lebih efisien untuk graph berarah non-negatif\n")
        self.result_text.insert(tk.END, f"• BDS mencari dari dua arah sekaligus\n")
        self.result_text.insert(tk.END, f"• Jangkauan pencarian lebih sempit\n\n")
        
        self.result_text.insert(tk.END, f"BDS vs A*:\n")
        self.result_text.insert(tk.END, f"• BDS tidak menggunakan heuristik\n")
        self.result_text.insert(tk.END, f"• A* lebih efisien pada graf tertentu dengan heuristik\n")
        self.result_text.insert(tk.END, f"• BDS lebih sederhana implementasinya\n")
        
        # Apply text tags
        self.result_text.tag_configure("header", font=("Arial", 11, "bold"))

    def show_all_locations(self):
        # Membuat peta dengan semua lokasi
        center_lat = sum(coord[0] for coord in coordinates.values()) / len(coordinates)
        center_lon = sum(coord[1] for coord in coordinates.values()) / len(coordinates)
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=16)
        
        # Tambahkan semua lokasi
        for name, coord in coordinates.items():
            icon_color = 'blue'
            if "Gerbang" in name:
                if "Masuk" in name:
                    icon_color = 'green'
                else:
                    icon_color = 'red'
            
            folium.Marker(
                coord, 
                tooltip=name,
                icon=folium.Icon(color=icon_color)
            ).add_to(m)
        
        # Tambahkan semua edge dari graph dasar
        for u, v in G.edges():
            folium.PolyLine(
                [coordinates[u], coordinates[v]], 
                color='gray', 
                weight=2, 
                opacity=0.5
            ).add_to(m)
        
        m.save("semua_lokasi.html")
        webbrowser.open("file://" + os.path.realpath("semua_lokasi.html"))

# === Main ===
if __name__ == "__main__":
    root = tk.Tk()
    app = NavigasiKampusApp(root)
    root.mainloop()
