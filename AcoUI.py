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
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="nsew")
        for i in range(6):
            self.frame.rowconfigure(i, weight=0)
        self.frame.rowconfigure(6, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text="Número de ciudades:").grid(row=0, column=0, sticky="e")
        self.city_entry = ttk.Entry(self.frame, width=8)
        self.city_entry.insert(0, "15")
        self.city_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(self.frame, text="Iteraciones:").grid(row=1, column=0, sticky="e")
        self.iter_entry = ttk.Entry(self.frame, width=8)
        self.iter_entry.insert(0, "50")
        self.iter_entry.grid(row=1, column=1, sticky="w")

        ttk.Button(self.frame, text="Cargar TSPLIB", command=self.load_tsplib).grid(row=2, column=0, pady=4, sticky="ew")
        ttk.Button(self.frame, text="Eliminar archivo", command=self.remove_tsplib).grid(row=2, column=1, pady=4, sticky="ew")

        ttk.Button(self.frame, text="Ejecutar ACO", command=self.run_aco).grid(row=3, column=0, columnspan=2, pady=4)

        self.source_label = ttk.Label(self.frame, text="Usando ciudades generadas aleatoriamente", foreground="gray")
        self.source_label.grid(row=4, column=0, columnspan=2, pady=5)

        
        self.fig, (self.ax_map, self.ax_evol) = plt.subplots(1, 2, figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=6, column=0, columnspan=2, sticky="nsew")

        self.root.bind("<Configure>", self.on_resize)

        self.cities = None
        self.tsplib_path = None

    def on_resize(self, event=None):
        """Reajusta los gráficos cuando cambia el tamaño de la ventana."""
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def load_tsplib(self):
        """Permite seleccionar y cargar un archivo TSPLIB"""
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
                    text=f"Archivo TSPLIB cargado ({num} ciudades)",
                    foreground="green"
                )
                self.city_entry.config(state="disabled")
                messagebox.showinfo("Archivo cargado", f"Se cargaron {num} ciudades desde:\n{filepath}")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo TSPLIB:\n{e}")

    def remove_tsplib(self):
        """Elimina el archivo cargado y vuelve al modo aleatorio"""
        if self.cities is not None:
            self.cities = None
            self.tsplib_path = None
            self.city_entry.config(state="normal")
            self.source_label.config(
                text="Usando ciudades generadas aleatoriamente",
                foreground="gray"
            )
            messagebox.showinfo("Archivo eliminado", "Se ha eliminado el archivo TSPLIB cargado.")

    def run_aco(self):
        """Ejecuta el algoritmo ACO"""
        try:
            n_iterations = int(self.iter_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El número de iteraciones debe ser un número entero.")
            return

        if self.cities is not None:
            cities = self.cities
        else:
            try:
                n_cities = int(self.city_entry.get())
            except ValueError:
                messagebox.showerror("Error", "El número de ciudades debe ser un número entero.")
                return
            cities = generate_cities(n_cities)

        dist = distance_matrix(cities)
        aco = AntColony(dist, n_ants=len(cities), n_iterations=n_iterations)
        history = []

        def update_plot(iteration, best_route, best_length):
            self.ax_map.clear()
            self.ax_evol.clear()
            history.append(best_length)

            pheromone = aco.pheromone
            max_pher = pheromone.max() if pheromone.max() > 0 else 1
            pheromone_norm = pheromone / max_pher

            # Dibujar feromonas
            for i in range(len(cities)):
                for j in range(i + 1, len(cities)):
                    intensity = pheromone_norm[i, j]
                    if intensity > 0.01:
                        self.ax_map.plot(
                            [cities[i][0], cities[j][0]],
                            [cities[i][1], cities[j][1]],
                            color=(0, 0, 1, intensity),
                            linewidth=1 + 3 * intensity
                        )

            # Mejor ruta
            best_path = cities[best_route + [best_route[0]]]
            self.ax_map.plot(best_path[:, 0], best_path[:, 1], 'r-', linewidth=2.5)
            self.ax_map.scatter(cities[:, 0], cities[:, 1], c='black', s=40)
            self.ax_map.set_title(f"Iteración {iteration+1}/{n_iterations} - Mejor: {best_length:.2f}")

            # Evolución
            self.ax_evol.plot(range(1, len(history)+1), history, 'r-o')
            self.ax_evol.set_title("Evolución del mejor costo")
            self.ax_evol.set_xlabel("Iteración")
            self.ax_evol.set_ylabel("Distancia mínima")

            self.fig.tight_layout()
            self.canvas.draw()
            self.root.update()
            time.sleep(0.2)

        aco.run(callback=update_plot)


if __name__ == "__main__":
    root = tk.Tk()
    app = ACOApp(root)
    root.mainloop()
