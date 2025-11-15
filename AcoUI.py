import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import time
import os

from aco import AntColony
from tsp import generate_cities, distance_matrix, read_tsplib


class ACOApp:
    def __init__(self, root):
        self.root = root
        root.title("Ant Colony Optimization - TSP")
        root.state("zoomed")

        self.stop_flag = False

        #LAYOUT  
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        self.sidebar = ttk.Frame(root, padding=18)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.config(width=340)

        for i in range(60):
            self.sidebar.rowconfigure(i, weight=0)
        self.sidebar.rowconfigure(59, weight=1)

        ttk.Label(self.sidebar, text="ACO - Parámetros",
                  font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))

        #PARAMETROS ACO
        self.section("Parámetros del algoritmo", 1)

        self.make_entry("Hormigas (n_ants):", "20", 2)
        self.make_entry("Alpha (feromona):", "1.0", 4)
        self.make_entry("Beta (heurística):", "5.0", 6)
        self.make_entry("Evaporación:", "0.5", 8)
        self.make_entry("Q (deposición):", "100", 10)

        self.add_separator(12)

        # ALEATORIOS
        self.section("Ciudades aleatorias", 13)

        self.make_entry("Número de ciudades:", "20", 14, attr="city_entry")

        self.add_separator(16)

        # NO ITERACIONES 
        self.section("Iteraciones", 17)

        self.make_entry("Iteraciones:", "50", 18, attr="iter_entry")

        self.add_separator(20)

        #ARCHIVOS
        self.section("Archivo TSPLIB", 21)

        ttk.Button(self.sidebar, text="Cargar archivo TSPLIB",
                   command=self.load_tsplib).grid(row=22, column=0, sticky="ew", pady=3)

        ttk.Button(self.sidebar, text="Eliminar archivo",
                   command=self.remove_tsplib).grid(row=23, column=0, sticky="ew", pady=3)

        self.source_label = ttk.Label(self.sidebar, text="Usando ciudades aleatorias",
                                      foreground="gray")
        self.source_label.grid(row=24, column=0, pady=5)

        self.add_separator(25)


        ttk.Button(self.sidebar, text="Ejecutar ACO",
                   command=self.run_aco,
                   style="Accent.TButton").grid(row=26, column=0, sticky="ew", pady=8)

        stop_btn = tk.Button(self.sidebar, text="DETENER",
                             bg="#b80808", fg="white",
                             font=("Segoe UI", 10, "bold"),
                             command=self.stop_execution)
        stop_btn.grid(row=27, column=0, sticky="ew", pady=4)

        #AREA DE GRAFICOS
        self.fig, (self.ax_map, self.ax_evol) = plt.subplots(1, 2, figsize=(13, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.root.bind("<Configure>", self.on_resize)

        self.cities = None
        self.tsplib_path = None


    # UTILIDADES DE UI

    def section(self, text, row):
        ttk.Label(self.sidebar, text=text,
                  font=("Segoe UI", 11, "bold")).grid(row=row, column=0,
                                                      sticky="w", pady=(10, 5))

    def make_entry(self, label, default, row, attr=None):
        ttk.Label(self.sidebar, text=label).grid(row=row, column=0, sticky="w")
        entry = ttk.Entry(self.sidebar, width=14)
        entry.insert(0, default)
        entry.grid(row=row + 1, column=0, sticky="w", pady=2)

        if attr:
            setattr(self, attr, entry)
        else:
            # nombre automático por label
            name = label.split("(")[0].strip().lower().replace(" ", "_")
            setattr(self, f"{name}_entry", entry)

    def add_separator(self, row):
        ttk.Separator(self.sidebar, orient="horizontal").grid(row=row, column=0,
                                                             sticky="ew", pady=7)

    def on_resize(self, event=None):
        self.fig.tight_layout()
        self.canvas.draw_idle()


    # ARCHIVOS TSPLIB
    def load_tsplib(self):
        default_dir = os.path.join(os.getcwd(), "tsp")
        os.makedirs(default_dir, exist_ok=True)

        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo TSPLIB",
            filetypes=[("TSPLIB files", "*.tsp"), ("All files", "*.*")],
            initialdir=default_dir
        )

        if filepath:
            try:
                self.cities = read_tsplib(filepath)
                self.tsplib_path = filepath
                num = len(self.cities)

                self.source_label.config(text=f"TSPLIB cargado ({num} ciudades)",
                                         foreground="green")

                self.city_entry.config(state="disabled")
                messagebox.showinfo("Archivo cargado", f"{num} ciudades cargadas.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def remove_tsplib(self):
        self.cities = None
        self.tsplib_path = None
        self.city_entry.config(state="normal")
        self.source_label.config(text="Usando ciudades aleatorias", foreground="gray")
        messagebox.showinfo("Archivo eliminado", "Archivo TSPLIB eliminado.")


    # BOTÓN STOP
    def stop_execution(self):
        self.stop_flag = True


    # ALGORITMO ACO
    def run_aco(self):
        self.stop_flag = False

        # Iteraciones
        try:
            n_iterations = int(self.iter_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Iteraciones inválidas.")
            return

        # Ciudades
        if self.cities is not None:
            cities = self.cities
        else:
            try:
                n_cities = int(self.city_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Número de ciudades inválido.")
                return
            cities = generate_cities(n_cities)

        # Parámetros ACO
        try:
            n_ants = int(self.hormigas__entry.get())
            alpha = float(self.alpha__entry.get())
            beta = float(self.beta__entry.get())
            evap = float(self.evaporización__entry.get())
            q = float(self.q__entry.get())
        except Exception:
            messagebox.showerror("Error", "Parámetros ACO inválidos.")
            return

        dist = distance_matrix(cities)
        aco = AntColony(
            dist,
            n_ants=n_ants,
            n_iterations=n_iterations,
            alpha=alpha,
            beta=beta,
            evaporation_rate=evap,
            q=q
        )

        history = []

        def update_plot(iteration, best_route, best_length):
            if self.stop_flag:
                raise KeyboardInterrupt

            self.ax_map.clear()
            self.ax_evol.clear()
            history.append(best_length)

            pheromone = aco.pheromone
            pher_norm = pheromone / max(pheromone.max(), 1e-9)

            for i in range(len(cities)):
                for j in range(i + 1, len(cities)):
                    intensity = pher_norm[i, j]
                    if intensity > 0.01:
                        self.ax_map.plot(
                            [cities[i][0], cities[j][0]],
                            [cities[i][1], cities[j][1]],
                            color=(0, 0, 1, intensity),
                            linewidth=1 + 3 * intensity
                        )

            best_path = cities[best_route + [best_route[0]]]
            self.ax_map.plot(best_path[:, 0], best_path[:, 1], 'r-', linewidth=2.5)
            self.ax_map.scatter(cities[:, 0], cities[:, 1], c='black', s=40)
            self.ax_map.set_title(f"Iteración {iteration+1}/{n_iterations} - Mejor: {best_length:.2f}")

            self.ax_evol.plot(range(1, len(history)+1), history, 'r-o')
            self.ax_evol.set_xlabel("Iteración")
            self.ax_evol.set_ylabel("Distancia mínima")
            self.ax_evol.set_title("Progreso")

            self.fig.tight_layout()
            self.canvas.draw()
            self.root.update()
            time.sleep(0.15)

        try:
            aco.run(callback=update_plot)
        except KeyboardInterrupt:
            messagebox.showinfo("Proceso detenido", "El algoritmo ACO fue detenido por el usuario.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ACOApp(root)
    root.mainloop()
