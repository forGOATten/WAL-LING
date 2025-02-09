import json 
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import statistics
import data
import data2
import data3
import animationTest as anim  # Imports the animate_point function
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation

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
def path_verification(optimized_routes):
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


#V2
def animate_path(points_list):
    #Anime un carré rouge suivant un chemin défini par 'points_list' en 3D.

    # Convertir la liste de listes en numpy array pour faciliter la manipulation
    points = np.array(points_list, dtype=float)

    # Initialisation de la figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Initialisation du carré rouge
    square = ax.scatter([], [], [], c='r', s=100)

    # Ligne pour le chemin suivi
    path_line, = ax.plot([], [], [], 'b-', linewidth=2)  # Bleu pour le chemin

    # Définition des limites de l'espace 3D
    ax.set_xlim(np.min(points[:, 0]) - 1, np.max(points[:, 0]) + 1)
    ax.set_ylim(np.min(points[:, 1]) - 1, np.max(points[:, 1]) + 1)
    ax.set_zlim(np.min(points[:, 2]) - 1, np.max(points[:, 2]) + 1)

    # Liste pour stocker les points déjà visités
    visited_x, visited_y, visited_z = [], [], []

    # Fonction d'initialisation de l'animation
    def init():
        square._offsets3d = ([], [], [])
        path_line.set_data([], [])
        path_line.set_3d_properties([])
        return square, path_line

    # Fonction de mise à jour de l'animation
    def update(frame):
        x, y, z = points[frame]

        # Mise à jour de la position du carré
        square._offsets3d = ([x], [y], [z])

        # Mise à jour du chemin suivi
        visited_x.append(x)
        visited_y.append(y)
        visited_z.append(z)
        path_line.set_data(visited_x, visited_y)
        path_line.set_3d_properties(visited_z)

        # Arrêter l'animation quand tous les points sont parcourus
        if frame == len(points) - 1:
            ani.event_source.stop()

        return square, path_line

    # Création de l'animation
    ani = FuncAnimation(fig, update, frames=len(points), init_func=init, blit=False, interval=500)

    plt.show()

if __name__ == "__main__":
       # Liste de points (exemple)
       points = np.array([[0, 0, 0], [1.5, 2.0, 3.0], [2.5, 3.0, 1.0], [0, 0, 0]])

       payload, debris, depot = initialisation()
       weight_debris = [np.random.randint(1, 10) for a in range(len(debris[0]))]
       capacity_cap = len(debris[0])
       optimized_routes = data3.clarke_wright_savings(debris, weight_debris, capacity_cap, payload)
       path_verification(optimized_routes)
       alt = []
       for path in optimized_routes :
              waypoints = []
              color = np.random.rand(3,) 
              for point_index in path :
                     #We take the index of the path
                     #We transform it into a list of coords
                     #The loop gives us a list of list of points => [[0,0,0], [np.float, np.float, np.float], ..., [0,0,0]]
                     debris_coords = [debris[0][point_index], debris[1][point_index], debris[2][point_index]]
                     #print(debris_coords)
                     #animate_path(debris_coords)

                     #On dessine les lignes
                     if len(waypoints) >= 1:
                            zgeg = True
                            #x, y, z => 0, 1, 2
                            #plt.plot([debris_coords[0], waypoints[-1][0]], [debris_coords[1], waypoints[-1][1]], [[debris_coords[2], waypoints[-1][2]]], color=color)
                     waypoints.append(debris_coords)
              alt.extend(waypoints)
       animate_path(alt)

    # Lancer l'animation
    #animate_path(points)




# if __name__ == "__main__":
#        #TODO =================================================================================================
#        #Dodge obstacles
#        #Delete points or paths when theyre done
#        #Send log data to UI => need to make it too
#        # =====================================================================================================
#        payload, debris, depot = initialisation()

#        #Roberts thingies -----------------------------------------------------------------------------------
#        #We are gonna take 4 params :
#        """
#        1- debris => [[int, ..., int]]
#        2- depot => (0,0,0)
#        3- weights => [int, ..., int]
#        4- capacity cap => int
#        """
#        #Calcul des poids => nb als ...
#        weight_debris = [np.random.randint(1, 10) for a in range(len(debris[0]))]
#        #capacity_cap = int(statistics.mean(weight_debris))
#        capacity_cap = len(debris[0])

#        optimized_routes = data3.clarke_wright_savings(debris, weight_debris, capacity_cap, payload)

#        path_verification(optimized_routes)

#        fig, ax = graphique(debris, payload)

#        #debris_coords = [[debris[0][i], debris[1][i], debris[2][i]]for i in range(DEBRISSIZE)]
#        #waypoints = [depot] + debris_coords

#        # Lolo changes -----------------------------------------------------------------------------------------------
#        #Modifying waypoints so that it takes the paths generated

#        print(optimized_routes)
#        #optimized_routes = [[int, ..., int], [int, ..., int]] => ints = index
#        for path in optimized_routes :
              
#               waypoints = []
#               color = np.random.rand(3,) 
#               for point_index in path :
#                      #We take the index of the path
#                      #We transform it into a list of coords
#                      #The loop gives us a list of list of points => [[0,0,0], [np.float, np.float, np.float], ..., [0,0,0]]
#                      debris_coords = [debris[0][point_index], debris[1][point_index], debris[2][point_index]]

#                      #On dessine les lignes
#                      if len(waypoints) >= 1:
#                             #x, y, z => 0, 1, 2
#                             plt.plot([debris_coords[0], waypoints[-1][0]], [debris_coords[1], waypoints[-1][1]], [[debris_coords[2], waypoints[-1][2]]], color=color)
#                      waypoints.append(debris_coords)
              
#               print("navigating path :")
#               print(waypoints)
#               ani = anim.animate_sequence(waypoints, fig, ax)
#               #We draw the paths on the graphique
#               print("waypoints")
#               print(len(waypoints))

#        # -------------------------------------------------------------------------------------------------------------

#        #On dessine 
#        # robot goes back to ss       
#        waypoints == [0,0,0]
#        # Animate the red point moving sequentially through the waypoints.
#        #ani = anim.animate_sequence(waypoints, fig, ax)

#        plt.legend()
#        plt.show()