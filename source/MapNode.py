from Coords import *

class MapNode():
    def __init__(self, node_id, node_name, node_type, lattitude, longitude):
        self.node_id = node_id                          #The id of this node
        self.node_name = node_name                      #The name of this node : bus stop 51367, lrt sumang, hdb 835
        self.node_type = node_type                      #The type of node this is : hdb, busstop, mrt, lrt
        self.position = Coords(lattitude, longitude)    #The position of this node on the map
        self.connections = []                           #A list of directed edges containing the next node and weight. Eg.(node156, 30)
        self.map_icon = None
        self.reset_pathfinding_data()

    def reset_pathfinding_data(self):
        self.g = 0      #Distance from start
        self.h = 0      #Distance to end
        self.parent = None
