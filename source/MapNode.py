from vector import *

class MapNode():
    def __init__(self, node_name, node_type, lattitude, longitude):
        self.node_name = node_name                      #The name of this node : bus stop 51367, lrt sumang, hdb 835
        self.node_type = node_type                      #The type of node this is : hdb, busstop, mrt, lrt
        self.position = Vector(longitude, lattitude)    #The position of this node on thee map
        self.connections = []                           #The list of MapNodes connected to this node
        self.map_icon = None
