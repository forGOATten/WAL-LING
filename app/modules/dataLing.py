import numpy as np
from itertools import combinations

def compute_distance_matrix(points):
    """Calcule la matrice des distances sans prendre en compte les obstacles."""
    n = len(points)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i, j] = np.linalg.norm(np.array(points[i]) - np.array(points[j]))
    return dist_matrix

def compute_savings(distance_matrix):
    """Calcule les économies de distance pour chaque paire de débris."""
    savings = []
    n = len(distance_matrix)
    for i, j in combinations(range(1, n), 2):
        s = distance_matrix[0, i] + distance_matrix[0, j] - distance_matrix[i, j]
        savings.append((s, i, j))
    savings.sort(reverse=True, key=lambda x: x[0])
    return savings

def clarke_wright_savings(raw_points, weights, capacity, payload):
    """Implémente l'algorithme de Clarke-Wright Savings sans prise en compte des obstacles."""
    points = [tuple(coord) for coord in zip(raw_points[0], raw_points[1], raw_points[2])]
    
    n = len(points)
    distance_matrix = compute_distance_matrix(points)
    savings = compute_savings(distance_matrix)
    
    routes = {i: [i] for i in range(1, n)}
    load = {i: weights[i - 1] for i in range(1, n)}
    
    for s, i, j in savings:
        if i in routes and j in routes and i != j:
            if load[i] + load[j] <= capacity:
                routes[i].extend(routes[j])
                load[i] += load[j]
                del routes[j]
                del load[j]
    
    final_routes = []
    visited_points = set()
    for route in routes.values():
        final_routes.append([0] + route + [0])
        visited_points.update(route)
    
    all_debris_indices = set(range(1, n))
    missing_points = all_debris_indices - visited_points
    
    if missing_points:
        print(f"⚠️ Points non visités détectés : {missing_points}")
        for point in missing_points:
            final_routes.append([0, point, 0])
    
    return final_routes

# --- Exemple d'utilisation ---
# if __name__ == "__main__":
#     depot = (0, 0, 0)
#     debris = [[2, 5, 7, 8, 3, 6], [3, 4, 1, 6, 8, 9], [1, 2, 3, 4, 5, 6]]
#     weights = [2, 3, 4, 2, 3, 5]
#     capacity = 7
    
#     optimized_routes = clarke_wright_savings_no_obstacles(debris, weights, capacity)
    
#     print("Trajets optimisés :")
#     for route in optimized_routes:
#         print(route)