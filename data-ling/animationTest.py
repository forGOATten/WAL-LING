import json
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np

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



