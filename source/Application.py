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
        self.load_map_data()

        # Initialise GUI
        self.gui = FrameGUI(Tk(), self)
        self.gui.mainloop()

    ## TODO:Load map data from text files into the varius node lists
    def load_map_data(self):
        # import hdb
        hdb = geopandas.read_file("map/hdb.geojson")
        for i in range(0, len(hdb)):
             self.hdb_nodes.append(MapNode(hdb.name, "hdb", hdb.geometry.y[i], hdb.geometry.x[i]))
             print(hdb.name[i], hdb.geometry.y[i], hdb.geometry.x[i], "loaded")

        # import bus_stop
        bus = geopandas.read_file("map/bus_stop.geojson")

        for i in range(0, len(bus)):
            self.bus_stop_nodes.append(MapNode(bus.name[i], "bus", bus.geometry.y[i], bus.geometry.x[i]))
            print(bus.name[i], bus.geometry.y[i], bus.geometry.x[i], "loaded")

        # import lrt
        lrt = geopandas.read_file("map/lrt.geojson")

        for i in range(0, len(lrt)):
            self.lrt_nodes.append(MapNode(lrt.name[i], "lrt", lrt.geometry.y[i], lrt.geometry.x[i]))
            print(lrt.name[i], lrt.geometry.x[i], lrt.geometry.y[i], "loaded")

    def test_function(self):
        print("Hi")