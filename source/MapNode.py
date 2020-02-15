from vector import *

class MapNode():
    def __init__(self, node_name, node_type, lattitude, longitude):
        self.node_name = node_name                      #The name of this node : bus stop 51367, lrt sumang, hdb 835
        self.node_type = node_type                      #The type of node this is : hdb, busstop, mrt, lrt
        self.position = Vector(longitude, lattitude)    #The position of this node on the map
        self.connections = []                           #A list of tuples containing a node and weight. Eg.(node156, 30)
        self.map_icon = None

    def set_position(self, lattitude, longitude):
        self.position = Vector(longitude, lattitude)    #The position of this node on the map

    def get_lattitude(self):
        return self.position.y

    def get_longitude(self):
        return self.position.x
