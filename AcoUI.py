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

        # LAYOUT
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # PANEL IZQUIERDO
        self.sidebar = ttk.Frame(root, padding=12)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        for i in range(30):
            self.sidebar.rowconfigure(i, weight=0)
        self.sidebar.rowconfigure(30, weight=1)

        # PARAMETROS ACO
        ttk.Label(self.sidebar, text="Parámetros ACO", foreground="red",
                  font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 6))

        ttk.Label(self.sidebar, text="Hormigas (n_ants):").grid(row=1, column=0, sticky="w")
        self.ants_entry = ttk.Entry(self.sidebar, width=10)
        self.ants_entry.insert(0, "20")
        self.ants_entry.grid(row=2, column=0, sticky="w", pady=2)

        ttk.Label(self.sidebar, text="Alpha (feromona):").grid(row=3, column=0, sticky="w")
        self.alpha_entry = ttk.Entry(self.sidebar, width=10)
        self.alpha_entry.insert(0, "1.0")
        self.alpha_entry.grid(row=4, column=0, sticky="w", pady=2)

        ttk.Label(self.sidebar, text="Beta (heurística):").grid(row=5, column=0, sticky="w")
        self.beta_entry = ttk.Entry(self.sidebar, width=10)
        self.beta_entry.insert(0, "5.0")
        self.beta_entry.grid(row=6, column=0, sticky="w", pady=2)

        ttk.Label(self.sidebar, text="Evaporación:").grid(row=7, column=0, sticky="w")
        self.evap_entry = ttk.Entry(self.sidebar, width=10)
        self.evap_entry.insert(0, "0.5")
        self.evap_entry.grid(row=8, column=0, sticky="w", pady=2)

        ttk.Label(self.sidebar, text="Q (deposición):").grid(row=9, column=0, sticky="w")
        self.q_entry = ttk.Entry(self.sidebar, width=10)
        self.q_entry.insert(0, "100")
        self.q_entry.grid(row=10, column=0, sticky="w", pady=2)

        self.add_separator(11)

        # ALEATORIOS
        ttk.Label(self.sidebar, text="Ciudades Aleatorias",
                  font=("Segoe UI", 10, "bold")).grid(row=12, column=0, sticky="w", pady=(5, 4))

        ttk.Label(self.sidebar, text="Número de ciudades:").grid(row=13, column=0, sticky="w")
        self.city_entry = ttk.Entry(self.sidebar, width=10)
        self.city_entry.insert(0, "20")
        self.city_entry.grid(row=14, column=0, sticky="w", pady=2)

        self.add_separator(15)

        # NO DE ITERACIONES
        ttk.Label(self.sidebar, text="Iteraciones",
                  font=("Segoe UI", 10, "bold")).grid(row=16, column=0, sticky="w", pady=(5, 4))

        ttk.Label(self.sidebar, text="Número de iteraciones:").grid(row=17, column=0, sticky="w")
        self.iter_entry = ttk.Entry(self.sidebar, width=10)
        self.iter_entry.insert(0, "50")
        self.iter_entry.grid(row=18, column=0, sticky="w", pady=2)

        self.add_separator(19)

        # ARCHIVOS
        ttk.Label(self.sidebar, text="Archivo TSPLIB",
                  font=("Segoe UI", 10, "bold")).grid(row=20, column=0, sticky="w", pady=(5, 4))

        ttk.Button(self.sidebar, text="Cargar TSPLIB", command=self.load_tsplib)\
            .grid(row=21, column=0, sticky="ew", pady=3)

        ttk.Button(self.sidebar, text="Eliminar archivo", command=self.remove_tsplib)\
            .grid(row=22, column=0, sticky="ew", pady=3)

        self.source_label = ttk.Label(self.sidebar, text="Usando ciudades aleatorias",
                                      foreground="gray")
        self.source_label.grid(row=23, column=0, pady=5)

        self.add_separator(24)


        ttk.Button(self.sidebar, text="Ejecutar ACO",
                   command=self.run_aco, style="Accent.TButton")\
            .grid(row=25, column=0, sticky="ew", pady=10)

        self.fig, (self.ax_map, self.ax_evol) = plt.subplots(1, 2, figsize=(13, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.root.bind("<Configure>", self.on_resize)

        self.cities = None
        self.tsplib_path = None


    def add_separator(self, row):
        sep = ttk.Separator(self.sidebar, orient="horizontal")
        sep.grid(row=row, column=0, sticky="ew", pady=7)


    def on_resize(self, event=None):
        self.fig.tight_layout()
        self.canvas.draw_idle()


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

                self.source_label.config(
                    text=f"TSPLIB cargado ({num} ciudades)",
                    foreground="green"
                )

                self.city_entry.config(state="disabled")
                messagebox.showinfo("Archivo cargado", f"{num} ciudades cargadas.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")


    def remove_tsplib(self):
        self.cities = None
        self.tsplib_path = None
        self.city_entry.config(state="normal")
        self.source_label.config(text="Usando ciudades aleatorias", foreground="gray")
        messagebox.showinfo("Archivo eliminado", "Se ha eliminado el archivo TSPLIB.")

    # EJECUTAR EL ALGORITMO
    def run_aco(self):
        try:
            n_iterations = int(self.iter_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Iteraciones inválidas.")
            return

        if self.cities is not None:
            cities = self.cities
        else:
            try:
                n_cities = int(self.city_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Número de ciudades inválido.")
                return
            cities = generate_cities(n_cities)

        try:
            n_ants = int(self.ants_entry.get())
            alpha = float(self.alpha_entry.get())
            beta = float(self.beta_entry.get())
            evap = float(self.evap_entry.get())
            q = float(self.q_entry.get())
        except ValueError:
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

        aco.run(callback=update_plot)


if __name__ == "__main__":
    root = tk.Tk()
    app = ACOApp(root)
    root.mainloop()
