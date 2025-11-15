import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class HelpWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ayuda - Algoritmo ACO")
        self.geometry("700x540")
        self.resizable(False, False)

        container = ttk.Frame(self, padding=15)
        container.pack(fill="both", expand=True)

        try:
            img = Image.open("img/logo.png")         
            img = img.resize((70, 70), Image.LANCZOS) 
            self.logo = ImageTk.PhotoImage(img)
        except Exception:
            self.logo = None

        header = ttk.Frame(container)
        header.pack(anchor="w", pady=(0, 10))

        if self.logo:
            logo_label = ttk.Label(header, image=self.logo)
            logo_label.pack(side="left", padx=(0, 10))

        title = ttk.Label(
            header,
            text="Ayuda del Algoritmo ACO y Parámetros",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(side="left")

        text = (
            "1. ¿Qué es el algoritmo ACO?\n"
            "   El algoritmo Ant Colony Optimization (ACO) es una metaheurística inspirada\n"
            "   en el comportamiento real de las hormigas al buscar comida. Las hormigas\n"
            "   depositan feromonas que guían a otras hormigas hacia rutas cada vez más\n"
            "   eficientes. Con el tiempo, la ruta más corta recibe más feromona y se vuelve\n"
            "   la más utilizada. "
            "   En esta simulación, ACO se usa para resolver el Problema del Viajante (TSP),\n"
            "   donde se busca la ruta más corta que recorra todas las ciudades una sola vez\n"
            "   y vuelva al punto inicial. Es un problema NP-Hard, por lo que se usan\n"
            "   heurísticas como ACO para obtener buenas soluciones en tiempo razonable.\n\n"

            "3. Parámetros ajustables y cómo afectan la simulación:\n\n"

            "   - n_ants (Número de hormigas):\n"
            "       Más hormigas = exploración más amplia, pero mayor tiempo de cómputo.\n"
            "       Pocas hormigas = menos exploración, riesgo de caer en malas soluciones.\n\n"

            "   - Alpha (importancia de la feromona):\n"
            "       Valores altos → las hormigas siguen rutas ya exploradas.\n"
            "       Valores bajos → la feromona tiene poco peso.\n"
            "       Recomendado: 0.5 – 2.0\n\n"

            "   - Beta (importancia de la heurística / distancia):\n"
            "       Alto β → las hormigas priorizan las ciudades más cercanas.\n"
            "       Bajo β → decisión más aleatoria.\n"
            "       Recomendado: 2 – 8\n\n"

            "   - Evaporación:\n"
            "       Controla qué tan rápido desaparece la feromona.\n"
            "       Mayor evaporación → evita quedar atrapado en una ruta.\n"
            "       Menor evaporación → favorece la explotación.\n\n"

            "   - Q (Cantidad de feromona depositada):\n"
            "       Controla cuánto refuerzo reciben las rutas buenas.\n"
            "       Q muy alto → la feromona se satura.\n"
            "       Q muy bajo → el aprendizaje es lento.\n\n"

            "4. Cómo usar la interfaz:\n"
            "   - Puedes generar ciudades aleatorias o cargar un archivo TSPLIB.\n"
            "   - Ajusta los parámetros del ACO según tu necesidad.\n"
            "   - Presiona Ejecutar ACO para iniciar la simulación.\n"
            "   - El botón DETENER permite interrumpir el proceso.\n\n"
        )

        text_widget = tk.Text(container, wrap="word", font=("Segoe UI", 10), height=26)
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)
