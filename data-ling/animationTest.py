import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

def animate_point(i, j, fig, ax, frames=100, interval=50):
    """
    Animate a point moving linearly from point i to point j in 3D space.
    (This function is kept for reference.)
    """
    i = np.array(i)
    j = np.array(j)
    
    point, = ax.plot([i[0]], [i[1]], [i[2]], marker='o', markersize=10, color="red")
    
    def update(frame):
        t = frame / frames
        pos = i + t * (j - i)
        point.set_data([pos[0]], [pos[1]])
        point.set_3d_properties([pos[2]])
        return point,
    
    ani = FuncAnimation(fig, update, frames=frames+1, interval=interval, blit=False)
    return ani

def animate_sequence(waypoints, fig, ax, frames_per_segment=100, interval=50):
    """
    Animate a point moving sequentially through a list of waypoints in 3D space.
    Each segment between consecutive waypoints is animated over `frames_per_segment` frames.

    Parameters:
        waypoints: List of points (each is [x, y, z]).
        fig: matplotlib Figure object.
        ax: matplotlib 3D Axes object.
        frames_per_segment: Number of frames to animate each segment.
        interval: Delay between frames in milliseconds.

    Returns:
        ani: The FuncAnimation object.
    """
    # Total number of segments and frames
    total_segments = len(waypoints) - 1
    total_frames = total_segments * frames_per_segment

    # Start the animation at the first waypoint
    point, = ax.plot([waypoints[0][0]], [waypoints[0][1]], [waypoints[0][2]], 
                     marker='o', markersize=10, color="red")
    
    def update(frame):
        # Determine which segment we’re animating
        segment = frame // frames_per_segment
        if segment >= total_segments:
            # Ensure the final frame is exactly at the last waypoint
            pos = np.array(waypoints[-1])
        else:
            frame_in_segment = frame % frames_per_segment
            t = frame_in_segment / frames_per_segment
            start = np.array(waypoints[segment])
            end = np.array(waypoints[segment+1])
            pos = start + t * (end - start)
        point.set_data([pos[0]], [pos[1]])
        point.set_3d_properties([pos[2]])
        return point,
    
    ani = FuncAnimation(fig, update, frames=total_frames+1, interval=interval, blit=False)
    return ani
