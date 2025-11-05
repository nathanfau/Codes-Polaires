import matplotlib.pyplot as plt
import numpy as np
import argparse

def Bhattacharyya(N, epsilon):
    Z = np.zeros(1)
    Z[0] = epsilon
    for _ in range(int(np.log2(N))):
        Z = np.concatenate([Z**2, 2*Z - Z**2])
    return Z

def main():
    parser = argparse.ArgumentParser(description="Tracer les coefficients de Bhattacharyya pour les codes polaires.")
    parser.add_argument("N", type=int, help="Longueur du code (puissance de 2)")
    parser.add_argument("epsilon", type=float, help="Probabilité d'erreur du canal BSC")
    parser.add_argument("--sort", "-s", action="store_true", help="Trier les valeurs de Z avant affichage")

    args = parser.parse_args()

    N = args.N
    epsilon = args.epsilon

    # Vérifie que N est bien une puissance de 2 strictement positive
    if (N & (N - 1)) != 0 or N <= 0:
        raise ValueError("N doit être une puissance de 2 strictement positive.")

    Z = Bhattacharyya(N, epsilon)

    if args.sort:
        Z = np.sort(Z)

    # Tracé du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(Z)), Z, marker='o', linestyle='None', markersize=3)
    plt.xlabel("Index du canal" + (" (trié)" if args.sort else ""))
    plt.ylabel("Coefficient de Bhattacharyya")
    plt.title(f"Coefficients de Bhattacharyya pour N={N}, ε={epsilon}")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()