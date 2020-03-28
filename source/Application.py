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
    LRT_SERVICES_FILE_PATH  = "map/LRTServiceRoute.json"
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
        """ Loads all the map data from their respective files
        """
        # Import hdb data
        with open(Application.HDB_FILE_PATH) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')

            for row in read_csv:
                new_node = MapNode(row[0], row[1], "hdb", float(row[2]), float(row[3]))
                self.hdb_nodes.append(new_node)
                self.all_nodes.append(new_node)
                self.all_nodes_dict[new_node.node_id] = new_node
                print(new_node.node_id, new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        # Import bus stop data
        with open(Application.BUS_STOP_FILE_PATH) as jsonfile:
            data = json.load(jsonfile)

            features = data["features"]
            for item in features:
                new_node = MapNode(item["id"], item["properties"]["name"], "bus", item["geometry"]["coordinates"][1], item["geometry"]["coordinates"][0])
                self.bus_stop_nodes.append(new_node)
                self.all_nodes.append(new_node)
                self.all_nodes_dict[new_node.node_id] = new_node
                print(new_node.node_id, new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        # Import lrt
        lrt = geopandas.read_file(Application.LRT_FILE_PATH)
        for i in range(0, len(lrt)):
            new_node = MapNode(lrt.id[i].split("/")[1], lrt.name[i], "lrt", lrt.geometry.y[i], lrt.geometry.x[i])
            self.lrt_nodes.append(new_node)
            self.all_nodes.append(new_node)
            self.all_nodes_dict[new_node.node_id] = new_node
            print(new_node.node_id, new_node.node_name, new_node.position.lattitude, new_node.position.longitude, "loaded")

        #Sort the all_nodes list to be be used for BINARY SEARCH
        self.all_nodes.sort(key=lambda x: x.node_name)

        #Create all node edges
        self.create_edge_connections()

    def create_edge_connections(self):
        """ Creates the directed edges for all nodes
            Bus service routes are also loaded in and treated as directed edges
        """
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
                            self.all_nodes_dict[service[i][j]].connections.append((self.all_nodes_dict[service[i][j + 1]], weight * 0.4, "Bus " + service_num))

        #Create LRT service connections
        with open(Application.LRT_SERVICES_FILE_PATH) as jsonfile:
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
                            print("LRT " + service[i][j] + " not found")
                            break
                        else:
                            weight = self.all_nodes_dict[service[i][j]].position.real_distance_from(self.all_nodes_dict[service[i][j + 1]].position)
                            self.all_nodes_dict[service[i][j]].connections.append((self.all_nodes_dict[service[i][j + 1]], weight * 0.4, "LRT " + service_num))

        #Go through all nodes annd create directed edges to each other if they are within the threshold distance
        for node in self.all_nodes:
            for other in self.all_nodes:
                if(node.node_id == other.node_id):
                    continue
                dist = node.position.distance_from_sqr(other.position)
                if(dist > Application.SHELTER_DIST_THRESHOLD):
                    pass
                else:
                    node.connections.append((other, dist * Application.SHELTER_DIST_MODIFIER))


    def find_path(self, preferred):
        """ Checks for valid start/end nodes annd displays error messages if invalid
            Runs the pathfinding algorithm if everything is valid

            Parameters:
            preferred:     The preferred pathfinding type
        """
        #Check for a valid start node
        if (self.selected_start_node == None):
            messagebox.showerror("Error finding path", "Please select a valid start point!")
            return
        #Check for a valid end node
        if (self.selected_end_node == None):
            messagebox.showerror("Error finding path", "Please select a valid end point!")
            return
        #Check that start and end nodes are different
        if (self.selected_start_node == self.selected_end_node):
            messagebox.showerror("Error finding path", "Start and end point must be different!")
            return

        #Begin pathfinding algorithm
        print("Finding path from '" + str(self.selected_start_node.node_name) + "' to '" + str(self.selected_end_node.node_name) + "'");
        self.path = Pathfinding.find_path_astar(self.selected_start_node, self.selected_end_node, ignore_buses=False if preferred != "Cheapest" else True)
        print("Astart path of length " + str(len(self.path)) + " found")

        #Update path info if a path was found
        if (len(self.path) > 0):
            self.gui.display_path_info(self.path)
            self.gui.map_canvas.display_path(self.path)

    def bin_search_all_nodes(self, selectedtext):
        """ Uses binary search to look through the all_nodes list for a node with a matching name

        Parameters:
        selectedtext:     The name of the node to look for
        """
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
        """ Clears the stored previous path info and the MapCanvas path drawing
        """
        self.path.clear()
        self.gui.clear_path_info()

    def save_path_info(self, file_path):
        """ Saves the current displayed path to a text file

        Parameters:
        file_path:      The location to export the path info to
        """
        if (len(self.path) < 1):
            messagebox.showerror("Invalid path info", "No path to save")
            return
        f = open(file_path, "w+")
        for i in range(len(self.path)):
            f.write(self.path[i].node_id + "\n")
        f.close()
        print("File saved to: " + file_path)

    def load_path_info(self, file_path):
        """ Loads a file containing a path info and displays it onto the GUI

        Parameters:
        file_path:      The location of the file to import
        """
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
    def calculate_calories_burnt(meters):
        """ Estimates the number of calories that would be burnt from walking a specified distance

        Parameters:
        meters:         The walking distance in meters
        """
        CALORIES_PER_METER = 0.062150403977625
        return int(meters * CALORIES_PER_METER)

    @staticmethod
    def find_path_distance(path):
        """ Calculates the total walking/lrt/mrt/bus distance travelled in a speecified path

        Parameters:
        path:           A list of nodes which form a path
        """
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
                elif(path[i].node_type == "lrt"):
                    lrt_dist += dist_to_next
                else:
                    print("Unknown node combination:", path[i].node_type, path[i + 1].node_type)
            else:
                walking_dist += dist_to_next

        return total_dist, walking_dist, bus_dist, lrt_dist

    @staticmethod
    def lrtCostCalculation(lrtdist):
        """ Calculates the cost of taking the LRT over a specified distance

        Parameters:
        lrtdist:          The distance travelled by LRT in km
        """
        distLrtCost=[0, 0.92,1.02]
        if (lrtdist != 0 ):
                if (lrtdist <= 3.2):
                    return distLrtCost[1]
                elif(lrtdist >3.2 and lrtdist<4.3):
                    return distLrtCost[2]
        else:
            return distLrtCost[0]

    @staticmethod
    def busCostCalculation(busdist):
        """ Calculates the cost of taking the bus over a specified distance

        Parameters:
        busdist:          The distance travelled by bus in km
        """
        distBusCost = [0,0.92, 1.02, 1.12, 1.22, 1.31, 1.38, 1.44, 1.48, 1.52, 1.56, 1.60, 1.64, 1.72, 1.76, 1.80, 1.84, 1.87, 1.90, 1.93, 1.96, 1.98, 2.00]
        if (busdist != 0):
                if (busdist <= 3.2):
                    return distBusCost[1]
                elif (busdist > 3.2 and busdist < 4.3):
                    return distBusCost[2]
                elif (busdist > 4.2 and busdist < 5.3):
                    return distBusCost[3]
                elif (busdist > 5.2 and busdist < 6.3):
                    return distBusCost[4]
                elif (busdist > 6.2 and busdist < 7.3):
                    return distBusCost[5]
                elif (busdist > 7.2 and busdist < 8.3):
                    return distBusCost[6]
                elif (busdist > 8.2 and busdist < 9.3):
                    return distBusCost[7]
                elif (busdist > 9.2 and busdist < 10.3):
                    return distBusCost[8]
                elif (busdist > 10.2 and busdist < 11.3):
                    return distBusCost[9]
                elif (busdist > 11.2 and busdist < 12.3):
                    return distBusCost[10]
                elif (busdist > 12.2 and busdist < 13.3):
                    return distBusCost[11]
                elif (busdist > 13.2 and busdist < 14.3):
                    return distBusCost[12]
                elif (busdist > 14.2 and busdist < 15.3):
                    return distBusCost[13]
                elif (busdist > 15.2 and busdist < 16.3):
                    return distBusCost[14]
                elif (busdist > 16.2 and busdist < 17.3):
                    return distBusCost[15]
                elif (busdist > 17.2 and busdist < 18.3):
                    return distBusCost[16]
                elif (busdist > 18.2 and busdist < 19.3):
                    return distBusCost[17]
                elif (busdist > 19.2 and busdist < 20.3):
                    return distBusCost[18]
                elif (busdist > 20.2 and busdist < 21.3):
                    return distBusCost[19]
                elif (busdist > 21.2 and busdist < 22.3):
                    return distBusCost[20]
                elif (busdist > 22.2 and busdist < 23.3):
                    return distBusCost[21]
                elif (busdist > 23.2 and busdist < 24.3):
                    return distBusCost[22]
                elif (busdist > 24.2 and busdist < 25.3):
                    return distBusCost[23]
        else:
            return distBusCost[0]
