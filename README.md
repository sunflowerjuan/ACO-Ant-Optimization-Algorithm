# Ant Colony Optimization (ACO) - TSP

Este proyecto implementa el algoritmo de optimización por colonia de hormigas (Ant Colony Optimization, ACO) para resolver el Problema del Viajante (TSP).

El TSP consiste en encontrar la ruta más corta que visita todas las ciudades una vez y regresa al punto inicial. El enfoque de ACO se basa en el comportamiento colectivo de las hormigas reales, que depositan feromonas para marcar caminos más eficientes, generando una forma de búsqueda probabilística cooperativa.

## Estructura del Proyecto

```
aco_tsp/
│
├── aco.py
├── tsp.py
├── main.py
├── tsp/                # Instancias TSPLIB preguardadas
│   ├── eil51.tsp       # Instancia de 51 ciudades
│   ├── kroA100.tsp     # Instancia de 100 ciudades
│   └── tsp200.tsp      # Instancia de 200 ciudades
└── README.md
```

## Prerequisitos

El proyecto usa Python 3.9+ y las siguientes dependencias:

```bash
pip install numpy matplotlib
```

Ejecuta la aplicación con:

```bash
python main.py
```
