import multiprocessing as mp
import random
import time
import matplotlib.pyplot as plt

def estimate_pi(seed: int, samples: int = 5_000_000) -> float:
    """Monte Carlo: fracción de puntos aleatorios que caen dentro del cuarto de círculo."""
    rng = random.Random(seed)
    inside = sum(rng.random()**2 + rng.random()**2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples

if __name__ == "__main__":
    process_counts = [1, 2, 4, 8]
    seeds = list(range(16))  # 16 tareas independientes para repartir
    
    times = []
    
    print("Ejecutando experimentos de paralelización...")
    for p in process_counts:
        t0 = time.perf_counter()
        # Creamos un Pool de procesos según el número de procesos de la prueba
        with mp.Pool(processes=p) as pool:
            results = pool.map(estimate_pi, seeds)
        t_elapsed = time.perf_counter() - t0
        times.append(t_elapsed)
        print(f"Procesos: {p} | Tiempo: {t_elapsed:.3f} s")
    
    # El speedup es el tiempo secuencial (1 proceso) dividido entre el tiempo paralelo
    t_seq = times[0]
    speedups = [t_seq / t for t in times]
    
    for p, s in zip(process_counts, speedups):
        print(f"Speedup con {p} procesos: {s:.2f}x")
    
    # --- VISUALIZACIÓN ---
    plt.figure(figsize=(8, 5))
    plt.plot(process_counts, speedups, 'o-', color='tab:blue', linewidth=2.5, label="Speedup Real")
    plt.plot(process_counts, process_counts, '--', color='tab:gray', linewidth=1.5, label="Speedup Ideal (Lineal $y=x$)")
    
    plt.xlabel("Número de Procesos", fontsize=12)
    plt.ylabel("Aceleración (Speedup)", fontsize=12)
    plt.title("Ejercicio 1: Aceleración Paralela vs. Número de Procesos", fontsize=14)
    plt.xticks(process_counts)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.7)
    
    # Guardar y mostrar
    plt.savefig("ejercicio1_speedup.png", dpi=300, bbox_inches='tight')
    print("Gráfica guardada exitosamente como 'ejercicio1_speedup.png'.")
    plt.show()