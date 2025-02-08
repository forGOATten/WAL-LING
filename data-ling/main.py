import json
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np

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
ss = [0,0,0]

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


