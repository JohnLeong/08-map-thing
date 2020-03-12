from tkinter import *

import geopandas as geopandas
import fiona  # ; help(fiona.open)
from FrameGUI import *
from MapNode import *


class Application():

    def __init__(self):
        # Initialise map data
        self.bus_stop_nodes = []
        self.lrt_nodes = []
        self.mrt_nodes = []
        self.hdb_nodes = []
        self.all_nodes = []
        self.hdbnames = []
        self.busnames = []
        self.lrtnames = []
        self.load_map_data()

        # Initialise GUI
        self.gui = FrameGUI(Tk(), self)
        self.gui.mainloop()

    ## TODO:Load map data from text files into the varius node lists
    def load_map_data(self):
        # import hdb
        hdb = geopandas.read_file("map/new_hdb.geojson")
        for i in range(0, len(hdb)):
            self.hdb_nodes.append(MapNode(hdb.name, "hdb", hdb.geometry.y[i], hdb.geometry.x[i]))
          #  print(hdb.name[i], hdb.geometry.y[i], hdb.geometry.x[i], "loaded")

        # import bus_stop
        bus = geopandas.read_file("map/new_bus.geojson")

        for i in range(0, len(bus)):
            self.bus_stop_nodes.append(MapNode(bus.name[i], "bus", bus.geometry.y[i], bus.geometry.x[i]))
        #    print(bus.name[i], bus.geometry.y[i], bus.geometry.x[i], "loaded")

        # import lrt
        lrt = geopandas.read_file("map/new_lrt.geojson")

        for i in range(0, len(lrt)):
            self.lrt_nodes.append(MapNode(lrt.name[i], "lrt", lrt.geometry.y[i], lrt.geometry.x[i]))
            print(lrt.name[i], lrt.geometry.x[i], lrt.geometry.y[i], "loaded")

    ## TODO: found on youtube, need modify, need find map link using dictonary https://www.youtube.com/watch?v=Ub4-nG09PFw
    map = {
        'a': {'b': 3, 'c': 4, 'd': 7},
        'b': {'c': 1, 'f': 5},
        'c': {'f': 6, 'd': 2},
        'd': {'e': 3, 'g': 6},
        'e': {'g': 3, 'h': 4},
        'f': {'e': 1, 'h': 8},
        'g': {'h': 2},
        'h': {'g': 2}
    }

    def dijkstra(map, start, end):
        shortest_distance = {}
        track_predecessor = {}
        unseenNodes = map
        infinity = 99999
        track_path = []  # dictionary to record as we trace back our journey

        for node in unseenNodes:
            shortest_distance[node] = infinity

        shortest_distance[start] = 0

        while unseenNodes:
            min_distance_node = None

            for node in unseenNodes:
                if min_distance_node is None:
                    min_distance_node = node

                elif shortest_distance[node] < shortest_distance[min_distance_node]:
                    min_distance_node = node

            path_options = map[min_distance_node].items()

            for child_node, weight in path_options:

                if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                    shortest_distance[child_node] = weight + shortest_distance[min_distance_node]

                    track_predecessor[child_node] = min_distance_node

            unseenNodes.pop(min_distance_node)
        currentNode = end

        while currentNode != start:
            try:
                track_path.insert(0, currentNode)
                currentNode = track_predecessor[currentNode]
            except KeyError:
                print('Path not reachable')
                break
        track_path.insert(0, start)

        if shortest_distance[end] != infinity:
            print('Shortest distance is ' + str(shortest_distance[end]))
            print('And the path is ' + str(track_path))

    dijkstra(map, 'a', 'h')


def get_lrt():
    lrtnames = []
    lrt = geopandas.read_file("map/new_lrt.geojson")

    for i in range(0, len(lrt)):
        lrtnames.append(lrt.name[i])
    return lrtnames

def get_busstop():
    busnames = []
    bus = geopandas.read_file("map/new_bus.geojson")

    for i in range(0, len(bus)):
        busnames.append(bus.name[i])
    return busnames
def get_hdb():
    block = []
    hdb = geopandas.read_file("map/new_hdb.geojson")

    for i in range(0, len(hdb)):
        block.append(hdb.name[i])
    return block