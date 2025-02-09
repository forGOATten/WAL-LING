import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

def animate_sequence(waypoints, fig, ax, frames_per_segment=100, interval=50,
                     debris_coords=None, debris_scatter=None, collision_threshold=0.02):
    """
    Animate a point moving sequentially through a list of waypoints in 3D space.
    The waypoint (debris point) will become transparent only when reached.

    Parameters:
      waypoints: List of [x, y, z] coordinates.
      fig: Matplotlib Figure object.
      ax: Matplotlib 3D Axes object.
      frames_per_segment: Number of frames to animate each segment.
      interval: Delay between frames in milliseconds.
      debris_coords: List of debris coordinates (excluding the space station).
      debris_scatter: The scatter plot object for debris.
      collision_threshold: Distance threshold to trigger transparency.

    Returns:
      ani: The FuncAnimation object.
    """

    total_segments = len(waypoints) - 1
    total_frames = total_segments * frames_per_segment

    # Start the red moving dot at the first waypoint
    point, = ax.plot([waypoints[0][0]], [waypoints[0][1]], [waypoints[0][2]],
                     marker='o', markersize=10, color="red")

    # Initialize alpha values for each debris point (fully visible at start)
    if debris_scatter is not None and debris_coords is not None:
        alphas = np.ones(len(debris_coords))  # 1 = fully visible, 0 = invisible

    def update(frame):
        segment = frame // frames_per_segment
        if segment >= total_segments:
            pos = np.array(waypoints[-1])  # Final position
        else:
            frame_in_segment = frame % frames_per_segment
            t = frame_in_segment / frames_per_segment
            start = np.array(waypoints[segment])
            end = np.array(waypoints[segment + 1])
            pos = start + t * (end - start)

        # Update red dot position
        point.set_data([pos[0]], [pos[1]])
        point.set_3d_properties([pos[2]])

        # Only update transparency for the **current waypoint** when reached
        if debris_coords is not None and debris_scatter is not None:
            if segment > 0:  # Ignore space station (waypoints[0])
                debris_index = segment - 1  # Since waypoints[0] is the space station
                debris_target = debris_coords[debris_index]
                if np.linalg.norm(pos - np.array(debris_target)) < collision_threshold:
                    alphas[debris_index] = 0.01  # Make current waypoint transparent
                    debris_scatter.set_alpha(alphas)

        return point,

    ani = FuncAnimation(fig, update, frames=total_frames + 1, interval=interval, blit=False)
    return ani
