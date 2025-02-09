import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

def animate_sequence(waypoints, fig, ax, frames_per_segment=20, interval=10):
    """
    Animate a point moving sequentially through a list of waypoints in 3D space,
    while tracking fuel consumption and refueling at the base station (0,0,0).
    """
    total_segments = len(waypoints) - 1
    
    if total_segments < 1:
        print("Error: Not enough waypoints to animate.")
        return None
    
    total_frames = total_segments * frames_per_segment
    
    point, = ax.plot([waypoints[0][0]], [waypoints[0][1]], [waypoints[0][2]], 
                     marker='o', markersize=10, color="red")
    
    fuel = 100  # Start with full fuel
    fuel_depletion_rate = 100 / max(total_frames, 1)  # Avoid division by zero
    
    fuel_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12)
    
    def update(frame):
        nonlocal fuel
        segment = frame // frames_per_segment
        if segment >= total_segments:
            pos = np.array(waypoints[-1])
        else:
            frame_in_segment = frame % frames_per_segment
            t = frame_in_segment / frames_per_segment
            start = np.array(waypoints[segment])
            end = np.array(waypoints[segment+1])
            pos = start + t * (end - start)
        
        point.set_data([pos[0]], [pos[1]])
        point.set_3d_properties([pos[2]])
        
        # Decrease fuel per frame
        fuel -= fuel_depletion_rate
        
        # Refuel if back at base (0,0,0)
        if np.allclose(pos, [0, 0, 0], atol=0.1):
            fuel = 100
        
        # Clear the previous text before updating
        fuel_text.set_text("")
        fuel_text.set_text(f"Fuel: {fuel:.1f}%")
        
        return point, fuel_text
    
    ani = FuncAnimation(fig, update, frames=total_frames+1, interval=interval, blit=False)
    return ani
