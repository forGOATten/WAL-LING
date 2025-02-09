import json 
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
from modules import dataLing
from modules import animateLing as anim  # Imports the animate_point function

# -----------------------------------------------------------------
# (Optional TLE data processing code is commented out)
# -----------------------------------------------------------------

def initialisation(): 
       #SPACE STATION COORDINATES
       depot = (0,0,0)

       np.random.seed(datetime.now().second)
       PAYLOADSIZE = 3
       DEBRISSIZE = np.random.randint(60, 100)

       payload = [[a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)], 
              [a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)], 
              [a if np.random.randint(0,2) else -a for a in np.random.rand(PAYLOADSIZE)]]
       debris = [[a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)], 
              [a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)], 
              [a if np.random.randint(0,2) else -a for a in np.random.rand(DEBRISSIZE)]]

       for i in range(len(debris)):
              debris[i].insert(0,depot[i])
       
       return payload, debris, depot 


# Vérification de la traversée
def path_verification(optimized_routes, debris):
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
       #data.verify_obstacle_avoidance(optimized_routes, [depot] + debris, payload)


# Set up the figure and 3D axis
def graphique(debris, payload): 
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

       return fig, ax

if __name__ == "__main__":
       #TODO =================================================================================================
       #Dodge obstacles
       #Delete points or paths when theyre done
       #Send log data to UI => need to make it too
       # =====================================================================================================
       payload, debris, depot = initialisation()

       #Roberts thingies -----------------------------------------------------------------------------------
       #We are gonna take 4 params :
       """
       1- debris => [[int, ..., int]]
       2- depot => (0,0,0)
       3- weights => [int, ..., int]
       4- capacity cap => int
       """
       #Calcul des poids => nb als ...
       weight_debris = [np.random.randint(1, 10) for a in range(len(debris[0]))]
       #capacity_cap = int(statistics.mean(weight_debris))
       capacity_cap = len(debris[0])

       optimized_routes = dataLing.clarke_wright_savings(debris, weight_debris, capacity_cap, payload)

       path_verification(optimized_routes)

       fig, ax = graphique(debris, payload)

       #debris_coords = [[debris[0][i], debris[1][i], debris[2][i]]for i in range(DEBRISSIZE)]
       #waypoints = [depot] + debris_coords

       # Lolo changes -----------------------------------------------------------------------------------------------
       #Modifying waypoints so that it takes the paths generated
       for elem in optimized_routes :
              waypoints = []
              for index in elem :
                     debris_coords = [debris[0][index], debris[1][index], debris[2][index]]

                     #On dessine les lignes
                     if len(waypoints) >= 1:
                            #x, y, z => 0, 1, 2
                            plt.plot([debris_coords[0], waypoints[-1][0]], [debris_coords[1], waypoints[-1][1]], [[debris_coords[2], waypoints[-1][2]]])
                     waypoints.append(debris_coords)
                     
                     ani = anim.animate_sequence(waypoints, fig, ax)
              #We draw the paths on the graphique
              print("waypoints")
              print(len(waypoints))

       # -------------------------------------------------------------------------------------------------------------

       #On dessine 
       # robot goes back to ss       
       waypoints == [0,0,0]
       # Animate the red point moving sequentially through the waypoints.
       #ani = anim.animate_sequence(waypoints, fig, ax)

       plt.legend()
       plt.show()