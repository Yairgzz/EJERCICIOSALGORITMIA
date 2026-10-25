import itertools
import math
import random
import matplotlib.pyplot as plt

def mst_prim(points: list[tuple[float, float]]) -> dict[int, list[int]]:
    """Algoritmo de Prim desde la ciudad 0; retorna el árbol como {nodo: [hijos]}."""
    best = {v: (math.dist(points[0], points[v]), 0) for v in range(1, len(points))}
    children = {v: [] for v in range(len(points))}
    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)
        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]:
                best[u] = (d, v)
    return children

def preorder(children: dict[int, list[int]], root: int = 0) -> list[int]:
    """Recorrido en preorden del MST para generar un tour válido del TSP."""
    return [root] + [c for child in children[root] for c in preorder(children, child)]

def tour_length(points, tour) -> float:
    return sum(math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))

def two_opt_post(points, route):
    """Post-procesamiento rápido 2-opt para mejorar el tour del MST."""
    best_route = list(route)
    best_length = tour_length(points, best_route)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_route) - 1):
            for k in range(i + 1, len(best_route)):
                new_route = best_route[:i] + best_route[i:k + 1][::-1] + best_route[k + 1:]
                new_length = tour_length(points, new_route)
                if new_length < best_length:
                    best_route = new_route
                    best_length = new_length
                    improved = True
                    break
            if improved:
                break
    return best_route, best_length

if __name__ == "__main__":
    random.seed(10)
    num_instances = 100
    n_cities = 9
    
    ratios = []
    mst_costs = []
    mst_2opt_costs = []
    brute_costs = []
    
    for _ in range(num_instances):
        points = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n_cities)]
        
        # 1. Solución MST Aproximada
        tree = mst_prim(points)
        approx_tour = preorder(tree)
        c_approx = tour_length(points, approx_tour)
        
        # 2. MST + Post-procesamiento 2-opt
        _, c_mst_2opt = two_opt_post(points, approx_tour)
        
        # 3. Óptimo Exacto (Fuerza Bruta para 9 ciudades)
        optimal_tour = min(((0,) + p for p in itertools.permutations(range(1, n_cities))),
                           key=lambda t: tour_length(points, t))
        c_opt = tour_length(points, optimal_tour)
        
        ratios.append(c_approx / c_opt)
        mst_costs.append(c_approx)
        mst_2opt_costs.append(c_mst_2opt)
        brute_costs.append(c_opt)

    print(f"Razón de aproximación promedio: {sum(ratios)/len(ratios):.3f}")
    print(f"Razón máxima observada: {max(ratios):.3f} (Límite teórico <= 2)")

    # --- VISUALIZACIÓN ---
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # 1. Histograma de la razón de aproximación
    axes[0].hist(ratios, bins=15, color="tab:purple", edgecolor="black", alpha=0.7)
    axes[0].axvline(2.0, color="red", linestyle="--", linewidth=2, label="Límite Teórico (2.0)")
    axes[0].set_title("Distribución de la Razón de Aproximación ($C_{mst} / C_{opt}$)")
    axes[0].set_xlabel("Razón de Aproximación")
    axes[0].set_ylabel("Frecuencia")
    axes[0].legend()
    axes[0].grid(True, linestyle=":", alpha=0.7)
    
    # 2. Boxplot comparativo de costos
    axes[1].boxplot([mst_costs, mst_2opt_costs, brute_costs], labels=["MST Puro", "MST + 2-opt", "Óptimo (Bruta)"])
    axes[1].set_title("Comparación de Costos entre Métodos")
    axes[1].set_ylabel("Costo (Distancia Total)")
    axes[1].grid(True, linestyle=":", alpha=0.7)
    
    plt.suptitle("Ejercicio 5: Análisis de Razón de Aproximación y Post-procesamiento", fontsize=14)
    plt.savefig("ejercicio5_mst.png", dpi=300, bbox_inches='tight')
    plt.show()