from tkinter import *
from tkinter import messagebox

import geopandas as geopandas
import fiona  # ; help(fiona.open)
from FrameGUI import *
from MapNode import *
from Pathfinding import *
import math as math
import csv
import json

class Application():
    HDB_FILE_PATH = "map/new_hdb.csv"
    BUS_STOP_FILE_PATH = "map/BusStop.geojson"
    BUS_SERVICES_FILE_PATH = "map/BusServiceRoute.json"
    LRT_FILE_PATH = "map/new_lrt.geojson"
    SHELTER_DIST_THRESHOLD = 0.0000058
    SHELTER_DIST_MODIFIER = 500000.2

    def __init__(self):
        # Initialise map data
        self.bus_stop_nodes = []
        self.lrt_nodes = []
        self.mrt_nodes = []
        self.hdb_nodes = []
        self.all_nodes = []
        self.all_nodes_dict = {}
        self.selected_start_node = None
        self.selected_end_node = None
        self.path = []
        self.load_map_data()

        # Initialise GUI
        self.gui = FrameGUI(Tk(), self)
        self.gui.mainloop()

    def load_map_data(self):
        # import hdb
        with open(Application.HDB_FILE_PATH) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')

            for row in read_csv:
                new_node = MapNode(row[0], row[1], "hdb", float(row[2]), float(row[3]))
                self.hdb_nodes.append(new_node)
                self.all_nodes.append(new_node)
                self.all_nodes_dict[new_node.node_id] = new_node
                print(new_node.node_id, new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        # file_name = "D:/SIT/ICT1008/1008 Project/source/map/new_hdb_test.csv"
        # f = open(file_name, "w+")
        # for i in range(0, len(self.hdb_nodes)):
        #     f.write("\"" + self.hdb_nodes[i].node_id + "\",\"" + self.hdb_nodes[i].node_name + "\",\"" + str(self.hdb_nodes[i].position.lattitude) + "\",\"" + str(self.hdb_nodes[i].position.longitude) + "\"\n")
        # f.close()

        # import bus_stop
        with open(Application.BUS_STOP_FILE_PATH) as jsonfile:
            data = json.load(jsonfile)

            features = data["features"]
            for item in features:
                new_node = MapNode(item["id"], item["properties"]["name"], "bus", item["geometry"]["coordinates"][1], item["geometry"]["coordinates"][0])
                self.bus_stop_nodes.append(new_node)
                self.all_nodes.append(new_node)
                self.all_nodes_dict[new_node.node_id] = new_node
                print(new_node.node_id, new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        # import lrt
        lrt = geopandas.read_file(Application.LRT_FILE_PATH)
        for i in range(0, len(lrt)):
            new_node = MapNode(lrt.id[i].split("/")[1], lrt.name[i], "lrt", lrt.geometry.y[i], lrt.geometry.x[i])
            self.lrt_nodes.append(new_node)
            self.all_nodes.append(new_node)
            self.all_nodes_dict[new_node.node_id] = new_node
            print(new_node.node_id, new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        #for sorting the all_nodes array that will be used for BINARY SEARCH
        self.all_nodes.sort(key=lambda x: x.node_name)

        self.create_edge_connections()

        #TEMPORARY ONLY(prints all node names in all_nodes array
        # for i in self.all_nodes:
        #     print("This is node name: " + i.node_name)

    def create_edge_connections(self):
        #Create bus service connections
        with open(Application.BUS_SERVICES_FILE_PATH) as jsonfile:
            data = json.load(jsonfile)

            #Loop through all bus services
            for service_num, service in data.items():
                #Loop through all routes in each servic
                for i in range(1, len(service)):
                    #Don't add route if there is only 1 stop
                    if (len(service[i]) < 2):
                        continue
                    #Created directed edges for each bus stop in the route
                    for j in range(len(service[i]) - 1):
                        if (service[i][j] not in self.all_nodes_dict):
                            print("Bus stop " + service[i][j] + " not found")
                            break
                        else:
                            weight = self.all_nodes_dict[service[i][j]].position.real_distance_from(self.all_nodes_dict[service[i][j + 1]].position)
                            self.all_nodes_dict[service[i][j]].connections.append((self.all_nodes_dict[service[i][j + 1]], weight * 0.4, service_num))
                            #print("Connection from", self.all_nodes_dict[service[i][j]].node_id, "to", self.all_nodes_dict[service[i][j + 1]].node_id)

        for node in self.all_nodes:
            for other in self.all_nodes:
                if(node.node_id == other.node_id):
                    continue
                dist = node.position.distance_from_sqr(other.position)
                if(dist > Application.SHELTER_DIST_THRESHOLD):
                    pass
                    #node.connections.append((other, dist * 1000.0))
                else:
                    node.connections.append((other, dist * Application.SHELTER_DIST_MODIFIER))


    def find_path(self, preferred):
        print(preferred)
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
        self.path = Pathfinding.find_path_astar(self.selected_start_node, self.selected_end_node, ignore_buses=False if preferred != "Cheapest" else True)
        print("Astart path of length " + str(len(self.path)) + " found")

        # for p in self.path:
        #     print(p.node_name, p.node_id)
        if (len(self.path) > 0):
            self.gui.display_path_info(self.path)
            self.gui.map_canvas.display_path(self.path)

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

    def clear_path_info(self):
        self.path.clear()
        self.gui.clear_path_info()

    def save_path_info(self, file_path):
        if (len(self.path) < 1):
            messagebox.showerror("Invalid path info", "No path to save")
            return
        f = open(file_path, "w+")
        for i in range(len(self.path)):
            f.write(self.path[i].node_id + "\n")
        f.close()
        print("File saved to: " + file_path)

    def load_path_info(self, file_path):
        f = open(file_path, 'r')
        lines = f.readlines()
        for line in lines:
            node_id = line.strip()
            if (node_id not in self.all_nodes_dict):
                messagebox.showerror("Invalid path info", "File could not be loaded")
                f.close()
                return
            self.path.append(self.all_nodes_dict[node_id])
        f.close()
        self.gui.display_path_info(self.path)
        self.gui.map_canvas.display_path(self.path)

    @staticmethod
    def find_path_distance(path):
        total_dist = walking_dist = bus_dist = lrt_dist = 0

        for i in range(len(path) - 1):
            dist_to_next = path[i].position.real_distance_from(path[i + 1].position)
            total_dist += dist_to_next
            if (path[i].node_type == path[i + 1].node_type):
                if (path[i].node_type == "bus"):
                    connection_found = False
                    for c in path[i].connections:
                        if (c[0].node_id == path[i + 1].node_id):
                            if (len(c) > 2):
                                connection_found = True
                                break
                    if (connection_found):
                        bus_dist += dist_to_next
                    else:
                        walking_dist += dist_to_next
                elif(path[i].node_type == "hdb"):
                    walking_dist += dist_to_next
                else:
                    print("Unknown node combination:", path[i].node_type, path[i + 1].node_type)
            else:
                walking_dist += dist_to_next

        return total_dist, walking_dist, bus_dist, lrt_dist
