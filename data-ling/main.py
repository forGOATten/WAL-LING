import json 
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import animationTest as anim  # Imports the animate_point function

# -----------------------------------------------------------------
# (Optional TLE data processing code is commented out)
# -----------------------------------------------------------------

np.random.seed(datetime.now().second)
PAYLOADSIZE = 3
DEBRISSIZE = np.random.randint(60, 100)

# Create random payload and debris coordinates
payload = [
    [a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)], 
    [a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)], 
    [a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)]
]
debris = [
    [a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)], 
    [a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)], 
    [a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)]
]
ss = [0, 0, 0]  # Space station coordinates

# Set up the figure and 3D axis
fig = plt.figure(figsize=(5, 5))
ax = fig.subplots(subplot_kw={"projection": "3d"})

# Plot the debris points, payload points, and the space station
ax.scatter(debris[0], debris[1], debris[2],
           label="Debris")
ax.scatter(payload[0], payload[1], payload[2], 
           marker="p",
           linewidths=3,
           label="Payload")
ax.scatter([0], [0], [0],
           marker="P",
           linewidths=10,
           label="Space Station")

# Remove tick labels and grid; clear background panes for a cleaner look
ax.set(xticklabels=[], yticklabels=[], zticklabels=[])
ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False


debris_coords = [[debris[0][i], debris[1][i], debris[2][i]]for i in range(DEBRISSIZE)]
waypoints = [ss] + debris_coords

# robot goes back to ss       
waypoints == [0,0,0]
# Animate the red point moving sequentially through the waypoints.
ani = anim.animate_sequence(waypoints, fig, ax)

plt.legend()
plt.show()
