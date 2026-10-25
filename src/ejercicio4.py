import math
import random
import time
import matplotlib.pyplot as plt

# Mismas ciudades del ejercicio anterior para mantener coherencia
cities = {
    "A": (0, 0), "B": (1, 5), "C": (5, 5), "D": (6, 2),
    "E": (3, 1), "F": (2, 3), "G": (4, 4), "H": (5, 1)
}
city_names = list(cities.keys())

def tour_length(route: list[str]) -> float:
    return sum(math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
               for i in range(len(route)))

def two_opt_move(route: list[str], i: int, k: int) -> list[str]:
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

def simulated_annealing(initial_route, schedule_type="exponential"):
    current_route = list(initial_route)
    current_cost = tour_length(current_route)
    
    best_route = list(current_route)
    best_cost = current_cost
    
    # Parámetros iniciales
    T = 100.0
    T_min = 0.01
    alpha = 0.98 if schedule_type == "exponential" else 0.5
    
    costs_history = []
    
    while T > T_min:
        # Generar vecino aleatorio usando 2-opt en dos índices aleatorios
        i = random.randint(1, len(current_route) - 2)
        k = random.randint(i + 1, len(current_route) - 1)
        neighbor = two_opt_move(current_route, i, k)
        neighbor_cost = tour_length(neighbor)
        
        delta = neighbor_cost - current_cost
        
        # Si es mejor, o si pasa la prueba probabilística de aceptación si es peor
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_route = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best_route = list(current_route)
                best_cost = current_cost
                
        costs_history.append(current_cost)
        
        # Esquema de enfriamiento
        if schedule_type == "exponential":
            T *= alpha
        elif schedule_type == "linear":
            T -= alpha
            
    return best_route, best_cost, costs_history

if __name__ == "__main__":
    random.seed(42)
    initial_route = list(city_names)
    random.shuffle(initial_route)
    
    # Ejecutar esquema exponencial
    t0 = time.perf_counter()
    best_exp_route, best_exp_cost, hist_exp = simulated_annealing(initial_route, "exponential")
    t_exp = time.perf_counter() - t0
    
    # Ejecutar esquema lineal
    t0 = time.perf_counter()
    best_lin_route, best_lin_cost, hist_lin = simulated_annealing(initial_route, "linear")
    t_lin = time.perf_counter() - t0
    
    print(f"Exponencial -> Costo: {best_exp_cost:.2f} | Tiempo: {t_exp:.4f} s | Iteraciones: {len(hist_exp)}")
    print(f"Lineal      -> Costo: {best_lin_cost:.2f} | Tiempo: {t_lin:.4f} s | Iteraciones: {len(hist_lin)}")
    
    # --- VISUALIZACIÓN ---
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # 1. Curva de convergencia (Costo vs Iteraciones)
    axes[0].plot(hist_exp, label="Exponencial ($T = T \\times \\alpha$)", color="tab:blue")
    axes[0].plot(hist_lin, label="Lineal ($T = T - \\alpha$)", color="tab:orange", alpha=0.8)
    axes[0].set_title("Curva de Convergencia (Costo vs. Iteraciones)")
    axes[0].set_xlabel("Iteraciones")
    axes[0].set_ylabel("Costo (Distancia Total)")
    axes[0].legend()
    axes[0].grid(True, linestyle=":", alpha=0.7)
    
    # 2. Gráfica comparativa de Desempeño Final
    schemes = ["Exponencial", "Lineal"]
    costs = [best_exp_cost, best_lin_cost]
    
    axes[1].bar(schemes, costs, color=["tab:blue", "tab:orange"], width=0.4)
    axes[1].set_title("Calidad de la Solución Final (Costo Mínimo)")
    axes[1].set_ylabel("Distancia Total")
    axes[1].set_ylim(min(costs) - 1, max(costs) + 1 if max(costs) != min(costs) else min(costs) + 2)
    axes[1].grid(axis='y', linestyle=":", alpha=0.7)
    
    plt.suptitle("Ejercicio 4: Ajuste de Parámetros en Simulated Annealing", fontsize=14)
    plt.savefig("ejercicio4_sa.png", dpi=300, bbox_inches='tight')
    plt.show()