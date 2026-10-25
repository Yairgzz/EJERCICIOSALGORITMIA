import math
import random
import matplotlib.pyplot as plt

# Definimos un conjunto de ciudades y sus coordenadas
cities = {
    "A": (0, 0), "B": (1, 5), "C": (5, 5), "D": (6, 2),
    "E": (3, 1), "F": (2, 3), "G": (4, 4), "H": (5, 1)
}
city_names = list(cities.keys())

def tour_length(route: list[str]) -> float:
    return sum(math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
               for i in range(len(route)))

def two_opt_move(route: list[str], i: int, k: int) -> list[str]:
    """Invierte el subsegmento de la ruta entre los índices i y k."""
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

def run_2opt(initial_route: list[str]):
    """Ejecuta 2-opt hasta alcanzar un óptimo local y cuenta las mejoras."""
    best_route = list(initial_route)
    best_length = tour_length(best_route)
    improvements_count = 0
    improved = True
    
    while improved:
        improved = False
        for i in range(1, len(best_route) - 1):
            for k in range(i + 1, len(best_route)):
                new_route = two_opt_move(best_route, i, k)
                new_length = tour_length(new_route)
                if new_length < best_length:
                    best_route = new_route
                    best_length = new_length
                    improvements_count += 1
                    improved = True
                    break
            if improved:
                break
    return best_route, best_length, improvements_count

def nearest_neighbor_start(cities_dict):
    """Genera una solución inicial usando el heurístico de Vecino Más Cercano."""
    unvisited = list(cities_dict.keys())
    current = unvisited.pop(0)
    route = [current]
    while unvisited:
        next_city = min(unvisited, key=lambda c: math.dist(cities_dict[current], cities_dict[c]))
        unvisited.remove(next_city)
        route.append(next_city)
        current = next_city
    return route

if __name__ == "__main__":
    num_trials = 30
    random_improvements, random_costs = [], []
    nn_improvements, nn_costs = [], []

    for _ in range(num_trials):
        # Escenario 1: Inicialización Aleatoria
        rand_route = list(city_names)
        random.shuffle(rand_route)
        _, r_cost, r_imp = run_2opt(rand_route)
        random_improvements.append(r_imp)
        random_costs.append(r_cost)
        
        # Escenario 2: Inicialización con Vecino Más Cercano
        nn_route = nearest_neighbor_start(cities)
        shift = random.randint(0, len(nn_route) - 1)
        nn_route = nn_route[shift:] + nn_route[:shift]
        _, nn_cost, nn_imp = run_2opt(nn_route)
        nn_improvements.append(nn_imp)
        nn_costs.append(nn_cost)

    # --- VISUALIZACIÓN ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].boxplot([random_improvements, nn_improvements], labels=["Aleatorio", "Vecino Más Cercano"])
    axes[0].set_title("Número de Mejoras (Iteraciones 2-opt)")
    axes[0].set_ylabel("Cantidad de mejoras")
    axes[0].grid(True, linestyle=":", alpha=0.7)

    axes[1].boxplot([random_costs, nn_costs], labels=["Aleatorio", "Vecino Más Cercano"])
    axes[1].set_title("Costo Final de la Ruta (Distancia)")
    axes[1].set_ylabel("Distancia Total")
    axes[1].grid(True, linestyle=":", alpha=0.7)

    plt.suptitle("Ejercicio 3: Análisis de Búsqueda Local (2-opt TSP)", fontsize=14)
    plt.savefig("ejercicio3_tsp.png", dpi=300, bbox_inches='tight')
    plt.show()