from tkinter import *
from tkinter import messagebox

import geopandas as geopandas
import fiona  # ; help(fiona.open)
from FrameGUI import *
from MapNode import *
import math as math

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
        self.selected_start_node = None
        self.selected_end_node = None
        self.load_map_data()

        # Initialise GUI
        self.gui = FrameGUI(Tk(), self)
        self.gui.mainloop()

    ## TODO:Load map data from text files into the varius node lists
    def load_map_data(self):
        # import hdb
         #TEMP comment out first because very slow
        # hdb = geopandas.read_file("map/new_hdb.geojson")
        # for i in range(0, len(hdb)):
        #     new_node = MapNode(hdb.name[i], "hdb", hdb.geometry.y[i], hdb.geometry.x[i])
        #     self.hdb_nodes.append(new_node)
        #     self.all_nodes.append(new_node)
        #     self.hdbnames.append(hdb.name[i])
        #     print(hdb.name[i], hdb.geometry.y[i], hdb.geometry.x[i], "loaded")

        # import bus_stop
        bus = geopandas.read_file("map/new_bus.geojson")

        for i in range(0, len(bus)):
            new_node = MapNode(bus.name[i], "bus", bus.geometry.y[i], bus.geometry.x[i])
            self.bus_stop_nodes.append(new_node)
            self.all_nodes.append(new_node)
            self.busnames.append(bus.name[i])
            print(bus.name[i], bus.geometry.y[i], bus.geometry.x[i], "loaded")

        # import lrt
        lrt = geopandas.read_file("map/new_lrt.geojson")

        for i in range(0, len(lrt)):
            new_node = MapNode(lrt.name[i], "lrt", lrt.geometry.y[i], lrt.geometry.x[i])
            self.lrt_nodes.append(new_node)
            self.all_nodes.append(new_node)
            self.lrtnames.append(lrt.name[i])
            print(lrt.name[i], lrt.geometry.x[i], lrt.geometry.y[i], "loaded")


        #for sorting the all_nodes array that will be used for BINARY SEARCH
        self.all_nodes.sort(key=lambda x: x.node_name)

        #TEMPORARY ONLY(prints all node names in all_nodes array
        for i in self.all_nodes:
            print("This is node name: " + i.node_name)



    def find_path(self):
        if (self.selected_start_node == None):
            messagebox.showerror("Error finding path", "Please select a start point!")
            return
        if (self.selected_end_node == None):
            messagebox.showerror("Error finding path", "Please select an end point!")
            return
        if (self.selected_start_node == self.selected_end_node):
            messagebox.showerror("Error finding path", "Start and end point must be different!")
            return

        print("Finding path from '" + str(self.selected_start_node.node_name) + "' to '" + str(self.selected_end_node.node_name) + "'");
        #self.dijkstra(self.selected_start_node, self.selected_end_node)



    #binary search algorithm
    def bin_search_all_nodes(self, selectedtext):
        start = 0
        end = (len(self.all_nodes))-1
        while start <= end:
            mid = int((start + end) / 2)
            n = self.all_nodes[mid]

            #if text is smaller, look left
            if n.node_name > selectedtext:
                end = mid - 1
            #if text is larger, look right
            elif n.node_name < selectedtext:
                start = mid + 1
            #if text is middle, return the node
            else:
                print("found")
                return n

#distance between start and end node in a straight line
def distance(latStart,lonStart,latEnd,lonEnd):
    R = 6373.0 #radius of earth
    lat1 = math.radians(latStart)
    lon1 = math.radians(lonStart)
    lat2 = math.radians(latEnd)
    lon2 = math.radians(lonEnd)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance