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

## Ejecucion y visualizacion

Clona el repositorio con el comando

```bash
git clone https://github.com/sunflowerjuan/ACO-Ant-Optimization-Algorithm.git
```

Ejecuta la aplicación con:

```bash
cd ACO-Ant-Optimization-Algorithm
python main.py
```

Durante la ejecución, la interfaz muestra:

**Gráfico izquierdo:**

![lchart](img/Lchart.png)

- Las ciudades (nodos).

- Las rutas más intensas en feromonas (líneas azules).

- La mejor ruta actual (línea roja).

**Gráfico derecho:**

![lchart](img/Rchart.png)

Evolución del mejor costo (distancia mínima) a lo largo de las iteraciones.

La simulación se actualiza dinámicamente, con una breve pausa entre iteraciones para apreciar el progreso de las hormigas.

### Instancias TSPLIB

Para cumplir con los casos de prueba 51, 100 y 200 ciudades, tenemos los archivos .tsp dentro de la carpeta tsp/. con los ejemplos:

- eil51.tsp (51 ciudades)

- kroA100.tsp (100 ciudades)

- kroA200.tsp (200 ciudades)

Si deseas hacer mas pruebas 2D descargarlos desde el repositorio oficial:

https://github.com/mastqe/tsplib/blob/master/kroA200.tsp

## Autor:

- Juan Sebastian Barajas Vargas
