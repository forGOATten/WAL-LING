import json
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import statistics
import data
import data2

# data = []
# with open('TLE_data.json') as file:
#     contents = file.read()
#     data = json.loads(contents)

# types = []
# for type in [a['OBJECT_TYPE'] for a in data]:
#     if type not in types:
#         types.append(type)
# types.sort()
# print(types)
# ['DEBRIS', 'PAYLOAD', 'ROCKET BODY']
# now = datetime.now(timezone.utc)

# debris = []
# rocketbody = []
# payload = []

# for obj in data:
#     space_obj = EarthSatellite(obj['TLE_LINE1'], obj['TLE_LINE2'], obj['INTLDES'], load.timescale())
#     ts = load.timescale()
#     t = space_obj.epoch #ts.utc(now.year, now.month, now.day, now.hour, now.minute, now.second)
#     position = space_obj.at(t).position.km  # (x, y, z) in km
#     data[data.index(obj)]["XYZ"] = tuple(position.tolist())
#     match(obj['OBJECT_TYPE']):
#         case "DEBRIS":
#             debris.append(tuple(position.tolist()))
#         case "ROCKET BODY":
#             rocketbody.append(tuple(position.tolist()))
#         case "PAYLOAD":
#             payload.append(tuple(position.tolist()))
# deb = [[d[0] for d in debris], [d[1] if debris.index(d)%2 else -d[1] for d in debris], [d[2] for d in debris]]
# pl = [[p[0] for p in payload], [p[1] if payload.index(p)%2 else -p[1] for p in payload], [p[2] for p in payload]]
# with open('TLE_data.json', 'w') as file:
#     file.write(json.)
np.random.seed(datetime.now().second)
PAYLOADSIZE = 3
DEBRISSIZE = np.random.randint(60,100)

payload = [[a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)], 
           [a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)], 
           [a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)]]
debris = [[a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)], 
          [a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)], 
          [a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)]]


#Roberts thingies -----------------------------------------------------------------------------------
#We are gonna take 4 params :
"""
1- debris => [[int, ..., int]]
2- depot => (0,0,0)
3- weights => [int, ..., int]
4- capacity cap => int
"""
#Point init
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
    
# Vérification des obstacles
#data2.verify_obstacle_avoidance(optimized_routes, [depot] + debris, payload)

#Printing station ===================================================================================================
# print("debrits :")
# print(debris)
# print("poids :")
# print(weight_debris)
# print(len(weight_debris))
# print(len(debris[0]))
# print(capacity_cap)
#print("routes optimisées :")
#print(optimized_routes)
#=======================================================================================================================
# ---------------------------------------------------------------------------------------------------


fig = plt.figure(figsize=(10, 10))
ax = fig.subplots(subplot_kw={"projection": "3d"})

ax.scatter(debris[0], debris[1], debris[2],
           label="Debris")
ax.scatter(payload[0], payload[1], payload[2], 
           marker="p",
           linewidths=3,
           label="Payload")
ax.scatter([0],[0],[0],
           marker="P",
           linewidths=10,
           label="Space Station")

ax.set(xticklabels=[],
       yticklabels=[],
       zticklabels=[])

ax.grid(False)

# Remove pane backgrounds
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

plt.show()


