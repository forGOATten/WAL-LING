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
                    print(f"⚠️ Obstacle détecté entre {points[i]} et {points[j]}")
                    old_point = points[j]
                    new_point = generate_bypass_point(points[j], obstacles)
                    print(f"🟢 Point de contournement généré : {new_point} pour contourner {old_point}")
                    points[j] = new_point
                dist_matrix[i, j] = np.linalg.norm(np.array(points[i]) - np.array(points[j]))
    return dist_matrix

def check_obstacle_interference(p1, p2, obstacles):
    """Vérifie si un segment entre p1 et p2 traverse un obstacle."""
    p1, p2 = tuple(p1), tuple(p2)
    p1, p2 = np.array(p1), np.array(p2)
    
    if len(obstacles) < 3 or any(len(obstacles[i]) == 0 for i in range(3)):
        return False  # Si les obstacles ne sont pas bien définis, ne pas vérifier
    
    obstacles = [np.array((x, y, z)) for x, y, z in zip(obstacles[0], obstacles[1], obstacles[2])]
    
    for obs in obstacles:
        if np.linalg.norm(p1 - obs) < 1 and np.linalg.norm(p2 - obs) < 1:
            print(f"🚧 Interférence détectée avec obstacle {obs}")
            return True
    return False

def generate_bypass_point(point, obstacles):
    """Génère un point à proximité pour contourner un obstacle."""
    # OFFSET => CONTOURNEMENT -------------------------------------------------------------------------
    offset = np.array([0.0001, -0.0001, 0.0001])
    
    if not isinstance(point, (list, tuple)) or len(point) != 3:
        print(f"❌ Erreur : `point` doit être un triplet (x, y, z) mais a la forme {point}")
        return point  # Ne pas modifier si le format est incorrect
    
    print(f"🔍 Vérification pour le contournement de {point}")
    point = np.array(point)  # S'assurer que le point est bien un tableau numpy
    
    if len(obstacles) < 3 or any(len(obstacles[i]) == 0 for i in range(3)):
        return tuple(point)  # Si obstacles mal définis, ne pas tenter de les éviter
    
    obstacles = [np.array((x, y, z)) for x, y, z in zip(obstacles[0], obstacles[1], obstacles[2])]
    
    for obs in obstacles:
        if np.linalg.norm(point - obs) < 1:
            new_point = tuple(point + offset)
            print(f"🔄 Nouveau point généré : {new_point} pour éviter l'obstacle {obs}")
            return new_point
    print(f"✅ Aucun contournement nécessaire pour {point}")
    return tuple(point)

def compute_savings(distance_matrix):
    """Calcule les économies de distance pour chaque paire de débris."""
    savings = []
    n = len(distance_matrix)
    for i, j in combinations(range(1, n), 2):
        s = distance_matrix[0, i] + distance_matrix[0, j] - distance_matrix[i, j]
        savings.append((s, i, j))
    savings.sort(reverse=True, key=lambda x: x[0])
    return savings

def clarke_wright_savings(raw_points, weights, capacity, obstacles):
    """Implémente l'algorithme de Clarke-Wright Savings pour optimiser les trajets."""
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
