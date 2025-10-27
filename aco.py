import numpy as np
import random

class AntColony:
    def __init__(self, distance_matrix, n_ants, n_iterations, alpha=1.0, beta=5.0, evaporation_rate=0.5, q=100):
        self.distances = distance_matrix
        self.pheromone = np.ones(self.distances.shape) / len(distance_matrix)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q

    def _route_length(self, route):
        return sum(self.distances[route[i % len(route)], route[(i + 1) % len(route)]] for i in range(len(route)))

    def _choose_next_city(self, current_city, unvisited):
        pheromone = self.pheromone[current_city, unvisited] ** self.alpha
        visibility = (1 / self.distances[current_city, unvisited]) ** self.beta
        probs = pheromone * visibility
        probs /= probs.sum()
        return np.random.choice(unvisited, p=probs)

    def run(self, callback=None):
        n_cities = len(self.distances)
        best_route = None
        best_length = float('inf')
        history = []

        for iteration in range(self.n_iterations):
            all_routes = []
            all_lengths = []

            for _ in range(self.n_ants):
                route = [random.randint(0, n_cities - 1)]
                while len(route) < n_cities:
                    unvisited = list(set(range(n_cities)) - set(route))
                    next_city = self._choose_next_city(route[-1], unvisited)
                    route.append(next_city)
                all_routes.append(route)
                all_lengths.append(self._route_length(route))

            # Actualizar feromonas
            self.pheromone *= (1 - self.evaporation_rate)
            for route, length in zip(all_routes, all_lengths):
                for i in range(n_cities):
                    a, b = route[i % n_cities], route[(i + 1) % n_cities]
                    self.pheromone[a, b] += self.q / length
                    self.pheromone[b, a] += self.q / length

            # Mejor ruta
            iteration_best = min(all_lengths)
            if iteration_best < best_length:
                best_length = iteration_best
                best_route = all_routes[np.argmin(all_lengths)]

            history.append(best_length)

            if callback:
                callback(iteration, best_route, best_length)

        return best_route, best_length, history
