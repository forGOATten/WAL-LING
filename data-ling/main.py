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
DEBRISSIZE = np.random.randint(5, 100)

# Create random payload and debris coordinates
payload = np.random.uniform(-1, 1, (3, PAYLOADSIZE))
debris = np.random.uniform(-1, 1, (3, DEBRISSIZE))
ss = [0, 0, 0]  # Space station coordinates

# Set up the figure and 3D axis
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, projection="3d")


# Plot the debris points, payload points, and the space station
debris_markers = ax.scatter(debris[0], debris[1], debris[2], label="Debris")
payload_markers = ax.scatter(payload[0], payload[1], payload[2], marker="p", linewidths=3, label="Payload")
ss_marker = ax.scatter([0], [0], [0], marker="P", linewidths=10, label="Space Station")

# Remove tick labels and grid; clear background panes for a cleaner look
ax.set(xticklabels=[], yticklabels=[], zticklabels=[])
ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

# Construct proper waypoints list (moving from the space station to each debris point)
waypoints = [ss] + [[debris[0][i], debris[1][i], debris[2][i]] for i in range(DEBRISSIZE)]

# Debugging: Check waypoint structure
print("Waypoints:", waypoints)
print("Waypoints shape:", np.array(waypoints).shape)


# Animate, making waypoints (debris) transparent only when reached.
ani = anim.animate_sequence(
    waypoints=waypoints,
    fig=fig,
    ax=ax,
    frames_per_segment=100,
    interval=50,
    debris_coords=[list(d) for d in zip(debris[0], debris[1], debris[2])],  # Proper debris list
    debris_scatter=debris_markers,
    collision_threshold=0.02
)

plt.legend()
plt.show()
