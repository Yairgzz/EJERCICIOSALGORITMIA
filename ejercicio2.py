import matplotlib.pyplot as plt

def greedy_knapsack(items, values, weights, W, strategy="density"):
    """
    Resuelve la mochila con enfoque voraz.
    strategy: 'density' (valor/peso) o 'weight' (menor peso primero)
    """
    indexed = list(zip(items, values, weights))
    
    if strategy == "density":
        indexed.sort(key=lambda x: x[1]/x[2], reverse=True)
    elif strategy == "weight":
        indexed.sort(key=lambda x: x[2])  # Ordena de menor a mayor peso
        
    total_val, total_weight, chosen = 0, 0, []
    for item, v, w in indexed:
        if total_weight + w <= W:
            total_weight += w
            total_val += v
            chosen.append(item)
            
    return total_val, total_weight, chosen

if __name__ == "__main__":
    # Instancia de prueba (Contraejemplo donde 'menor peso' falla)
    items = ["A", "B"]
    values = [10, 90]
    weights = [2, 9]
    W = 10  # Capacidad máxima de la mochila

    v1, w1, c1 = greedy_knapsack(items, values, weights, W, "density")
    v2, w2, c2 = greedy_knapsack(items, values, weights, W, "weight")

    print(f"Estrategia Valor/Peso -> Valor total: {v1}, Objetos: {c1}")
    print(f"Estrategia Menor Peso  -> Valor total: {v2}, Objetos: {c2}")

    # --- VISUALIZACIÓN ---
    methods = ["Valor/Peso (Estándar)", "Menor Peso"]
    total_values = [v1, v2]

    plt.figure(figsize=(7, 4))
    bars = plt.bar(methods, total_values, color=['tab:green', 'tab:red'], width=0.5)
    
    plt.ylabel("Valor Total Obtenido", fontsize=11)
    plt.title("Ejercicio 2: Comparación de Criterios Voraces (Mochila)", fontsize=13)
    plt.ylim(0, 105)
    
    # Etiquetas con el valor sobre las barras
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, f"{yval}", ha='center', va='bottom', fontweight='bold')

    plt.grid(axis='y', linestyle=":", alpha=0.7)
    plt.savefig("ejercicio2_knapsack.png", dpi=300, bbox_inches='tight')
    plt.show()