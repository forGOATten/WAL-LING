import json
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone
import numpy as np
import json
import matplotlib.pyplot as plt
import statistics
import data
import data2

# Chargement des données
with open('WAL-LING/TLE_data.json') as file:
    data = json.load(file)

# Initialisation des listes pour stocker les coordonnées
debris = []
payload = []

# Charger le timescale
ts = load.timescale()

# Extraction des positions
for obj in data:
    space_obj = EarthSatellite(obj['TLE_LINE1'], obj['TLE_LINE2'], obj['INTLDES'], ts)
    t = space_obj.epoch  # Temps de l'objet
    position = space_obj.at(t).position.km  # Coordonnées (x, y, z) en km

    # Ajouter les positions aux listes correspondantes
    if obj['OBJECT_TYPE'] == "DEBRIS":
        debris.append(position)
    elif obj['OBJECT_TYPE'] == "PAYLOAD":
        payload.append(position)

# Transformer en format souhaité : [[x1, x2, ...], [y1, y2, ...], [z1, z2, ...]]
debris = np.array(debris).T.tolist()  # Transpose pour séparer x, y, z
payload = np.array(payload).T.tolist()  # Même traitement pour les payloads

depot = (0,0,0)
#Calcul des poids => nb als ...
weight_debris = [np.random.randint(1, 10) for a in range(len(debris[0]))]
#capacity_cap = int(statistics.mean(weight_debris))
capacity_cap = len(debris[0])

optimized_routes = data2.clarke_wright_savings(debris, weight_debris, capacity_cap, payload)

# Vérification de la traversée
print("Trajets optimisés :")
for route in optimized_routes:
       print(route)
    
all_debris_indices = set(range(1, len(debris[0])))
visited_points = set()
for route in optimized_routes:
       visited_points.update(route[1:-1])
missing_points = all_debris_indices - visited_points
if missing_points:
       print(f"⚠️ Attention : Les points suivants ne sont pas inclus dans les trajets : {missing_points}")
else:
       print("✅ Tous les débris ont été inclus dans les trajets.")