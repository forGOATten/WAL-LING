import numpy as np
from itertools import combinations

def compute_distance_matrix(points, obstacles):
    """Calcule la matrice des distances en tenant compte des obstacles."""
    n = len(points)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                direct_distance = np.linalg.norm(np.array(points[i]) - np.array(points[j]))
                if check_obstacle_interference(tuple(points[i]), tuple(points[j]), obstacles):
                    points[j] = generate_bypass_point(points[j], obstacles)
                dist_matrix[i, j] = np.linalg.norm(np.array(points[i]) - np.array(points[j]))
    return dist_matrix

def check_obstacle_interference(p1, p2, obstacles):
    """Vérifie si un segment entre p1 et p2 traverse un obstacle."""
    p1, p2 = np.array(p1), np.array(p2)  # Conversion explicite en tableaux NumPy de taille (3,)
    obstacles = [tuple(coord) for coord in zip(obstacles[0], obstacles[1], obstacles[2])]  # Conversion en liste de tuples
    for obs in obstacles:
        obs = np.array(obs)  # Conversion explicite de l'obstacle en tableau NumPy
        if np.linalg.norm(p1 - obs) < 1 and np.linalg.norm(p2 - obs) < 1:
            return True
    return False

def generate_bypass_point(point, obstacles):
    """Génère un point à proximité pour contourner un obstacle."""
    offset = np.array([1, -1, 1])  # Petit décalage (à ajuster si besoin)
    obstacles = [tuple(coord) for coord in zip(obstacles[0], obstacles[1], obstacles[2])]
    for obs in obstacles:
        if np.linalg.norm(np.array(point) - np.array(obs)) < 1:
            return tuple(np.array(point) + offset)
    return point

def compute_savings(distance_matrix):
    """Calcule les économies de distance pour chaque paire de débris."""
    savings = []
    n = len(distance_matrix)
    for i, j in combinations(range(1, n), 2):  # Exclut le dépôt (index 0)
        s = distance_matrix[0, i] + distance_matrix[0, j] - distance_matrix[i, j]
        savings.append((s, i, j))
    savings.sort(reverse=True, key=lambda x: x[0])  # Trier par gain décroissant
    return savings

def clarke_wright_savings(raw_points, weights, capacity, obstacles):
    """Implémente l'algorithme de Clarke-Wright Savings pour optimiser les trajets en contournant les obstacles."""
    points = [tuple(coord) for coord in zip(raw_points[0], raw_points[1], raw_points[2])]
    
    n = len(points)
    distance_matrix = compute_distance_matrix(points, obstacles)
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

def verify_obstacle_avoidance(routes, points, obstacles):
    """Vérifie si tous les trajets évitent les obstacles."""
    obstacles = [tuple(coord) for coord in zip(obstacles[0], obstacles[1], obstacles[2])]
    for route in routes:
        for i in range(len(route) - 1):
            p1, p2 = tuple(points[route[i]]), tuple(points[route[i + 1]])
            if check_obstacle_interference(p1, p2, obstacles):
                print(f"⚠️ Problème : Le segment {p1} -> {p2} traverse un obstacle !")
                return False
    print("✅ Tous les trajets contournent correctement les obstacles.")
    return True