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
        self.selected_start_node = None
        self.selected_end_node = None
        self.load_map_data()

        # Initialise GUI
        self.gui = FrameGUI(Tk(), self)
        self.gui.mainloop()

    def load_map_data(self):
        # import hdb
         #TEMP comment out first because very slow
        # hdb = geopandas.read_file("map/new_hdb.geojson")
        # for i in range(0, len(hdb)):
        #     new_node = MapNode(hdb.name[i], "hdb", hdb.geometry.y[i], hdb.geometry.x[i])
        #     self.hdb_nodes.append(new_node)
        #     self.all_nodes.append(new_node)
        #     print(new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        # import bus_stop
        bus = geopandas.read_file("map/new_bus.geojson")
        for i in range(0, len(bus)):
            new_node = MapNode(bus.name[i], "bus", bus.geometry.y[i], bus.geometry.x[i])
            self.bus_stop_nodes.append(new_node)
            self.all_nodes.append(new_node)
            print(new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        # import lrt
        lrt = geopandas.read_file("map/new_lrt.geojson")
        for i in range(0, len(lrt)):
            new_node = MapNode(lrt.name[i], "lrt", lrt.geometry.y[i], lrt.geometry.x[i])
            self.lrt_nodes.append(new_node)
            self.all_nodes.append(new_node)
            print(new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        #for sorting the all_nodes array that will be used for BINARY SEARCH
        self.all_nodes.sort(key=lambda x: x.node_name)

        #TEMPORARY ONLY(prints all node names in all_nodes array
        for i in self.all_nodes:
            print("This is node name: " + i.node_name)



    def find_path(self):
        if (self.selected_start_node == None):
            messagebox.showerror("Error finding path", "Please select a valid start point!")
            return
        if (self.selected_end_node == None):
            messagebox.showerror("Error finding path", "Please select a valid end point!")
            return
        if (self.selected_start_node == self.selected_end_node):
            messagebox.showerror("Error finding path", "Start and end point must be different!")
            return

        print("Finding path from '" + str(self.selected_start_node.node_name) + "' to '" + str(self.selected_end_node.node_name) + "'");
        #path = self.dijkstra(self.selected_start_node, self.selected_end_node)
        path = []
        for i in range(10):
            path.append(self.all_nodes[i])

        messagebox.showerror("Hi", "This path is only a placeholder to preview the drawing of lines")
        self.gui.display_path_info(path)
        self.gui.map_canvas.display_path(path)

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

    @staticmethod
    def find_path_distance(path):
        total_dist = walking_dist = bus_dist = lrt_dist = 0

        for i in range(len(path) - 1):
            dist_to_next = path[i].position.real_distance_from(path[i + 1].position)
            total_dist += dist_to_next
            if (path[i].node_type == path[i + 1].node_type):
                if (path[i].node_type == "bus"):
                    bus_dist += dist_to_next
                elif (path[i].node_type == "lrt"):
                    lrt_dist += dist_to_next
                else:
                    print("Unknown node combination:", path[i].node_type, path[i + 1].node_type)
            else:
                walking_dist += dist_to_next

        return total_dist, walking_dist, bus_dist, lrt_dist
