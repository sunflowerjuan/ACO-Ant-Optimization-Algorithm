import numpy as np

def read_tsplib(filename):
    """Lee un archivo TSPLIB (.tsp) y devuelve coordenadas (x, y)."""
    coords = []
    reading = False
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "EOF":
                break
            if line == "NODE_COORD_SECTION":
                reading = True
                continue
            if reading:
                parts = line.split()
                if len(parts) >= 3:
                    coords.append((float(parts[1]), float(parts[2])))
    return np.array(coords)

def generate_cities(n):
    """Genera coordenadas (x, y) aleatorias para n ciudades."""
    return np.random.rand(n, 2) * 100

def distance_matrix(cities):
    """Calcula la matriz de distancias euclidianas entre las ciudades."""
    n = len(cities)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = np.linalg.norm(cities[i] - cities[j])
    return dist
