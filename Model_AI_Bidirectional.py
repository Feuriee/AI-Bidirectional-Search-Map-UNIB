import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import folium
import webbrowser
import os
import time
import math
import networkx as nx
import openrouteservice
from itertools import combinations

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

def get_ors_route(coord1, coord2):
    try:
        res = client.directions(
            coordinates=[coord1[::-1], coord2[::-1]],
            profile='foot-walking', format='geojson')
        geometry = res['features'][0]['geometry']['coordinates']
        distance = res['features'][0]['properties']['segments'][0]['distance']
        return [[lat, lon] for lon, lat in geometry], distance
    except:
        return None, None

def find_route(start, goal, jam, hari):
    Gf = filter_graph_by_time(G, jam, hari)
    start_time = time.time()
    ors_coords, ors_dist = get_ors_route(coordinates[start], coordinates[goal])
    if ors_coords:
        return "ORS", ors_coords, ors_dist, time.time() - start_time

    try:
        path = nx.bidirectional_shortest_path(Gf, start, goal)
        dist = sum(Gf[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        coords = [coordinates[p] for p in path]
        return "BDS", coords, dist, time.time() - start_time
    except:
        return None, None, None, None

# === GUI ===
root = tk.Tk()
root.title("Navigasi Kampus UNIB")
root.geometry("750x670")
root.configure(bg="#ffffff")

sorted_locations = sorted(coordinates.keys())

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TCombobox", font=("Segoe UI", 10))
style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

# === Judul Aplikasi ===
title_label = tk.Label(root, text="Navigasi Kampus UNIB", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#333333")
title_label.pack(pady=15)

# === Frame Parameter Input ===
frame_input = ttk.LabelFrame(root, text="Parameter Input")
frame_input.pack(fill="x", padx=20, pady=10)

# Form baris-baris
form_fields = [
    ("Titik Awal:", tk.StringVar()),
    ("Titik Tujuan:", tk.StringVar()),
    ("Hari:", tk.StringVar(value="weekday")),
    ("Jam (0-23):", tk.StringVar(value="10"))
]

for i, (label_text, var) in enumerate(form_fields):
    ttk.Label(frame_input, text=label_text).grid(row=i, column=0, padx=10, pady=8, sticky="w")
    if label_text.startswith("Jam"):
        tk.Entry(frame_input, textvariable=var, width=10).grid(row=i, column=1, padx=10, pady=5, sticky="w")
    else:
        options = ["weekday", "weekend"] if label_text.startswith("Hari") else sorted_locations
        ttk.Combobox(frame_input, textvariable=var, values=options, state="readonly", width=40).grid(row=i, column=1, padx=10, pady=5, sticky="w")

start_var, goal_var, day_var, time_var = [v for _, v in form_fields]

# === Tombol Fungsi ===
frame_button = tk.Frame(root, bg="#ffffff")
frame_button.pack(pady=10)
tk.Button(frame_button, text="Tampilkan Rute", font=("Segoe UI", 10, "bold"), width=25, command=lambda: show_route()).pack()

# === Frame Output ===
frame_output = ttk.LabelFrame(root, text="Hasil Pencarian Rute")
frame_output.pack(fill="both", expand=True, padx=20, pady=10)

output_text = tk.Text(frame_output, height=12, wrap="word", font=("Segoe UI", 10))
output_text.pack(fill="both", expand=True, padx=10, pady=10)

def show_route():
    start, goal = start_var.get(), goal_var.get()
    if not start or not goal or start == goal:
        messagebox.showerror("Error", "Pilih titik awal dan tujuan yang berbeda.")
        return
    try:
        jam = int(time_var.get())
    except ValueError:
        messagebox.showerror("Error", "Jam harus berupa angka.")
        return
    hari = day_var.get()
    method, coords, dist, durasi = find_route(start, goal, jam, hari)
    if coords is None:
        messagebox.showinfo("Info", "Rute tidak ditemukan.")
        return

    m = folium.Map(location=coordinates[start], zoom_start=17)
    folium.Marker(coordinates[start], tooltip=f"Start: {start}", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(coordinates[goal], tooltip=f"Goal: {goal}", icon=folium.Icon(color='red')).add_to(m)
    folium.PolyLine(coords, color='blue', weight=5, tooltip=f"{method} - {dist:.2f} m").add_to(m)
    m.save("rute_kampus.html")
    webbrowser.open("file://" + os.path.realpath("rute_kampus.html"))

    est_time = (dist / 1.4) / 60
    gate_stat = status_gerbang(jam, hari)
    gate_info = "\n".join([f"- {k}: {v}" for k, v in gate_stat.items()])

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Metode: {method}\nJarak: {dist:.2f} meter\nEstimasi waktu: {est_time:.2f} menit\nWaktu eksekusi: {durasi:.4f} detik\n\nStatus Gerbang:\n{gate_info}")

root.mainloop()