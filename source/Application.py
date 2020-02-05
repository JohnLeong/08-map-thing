from tkinter import *
from FrameGUI import *
from MapNode import *

class Application():

    def __init__(self):
        #Initialise map data
        self.bus_stop_nodes = []
        self.lrt_nodes = []
        self.mrt_nodes = []
        self.hdb_nodes = []
        self.all_nodes = []
        self.load_map_data()

        #Initialise GUI
        self.gui = FrameGUI(Tk(), self)
        self.gui.mainloop()

    ## TODO:Load map data from text files into the varius node lists
    def load_map_data(self):
        #TEMPORARY
        self.lrt_nodes.append(MapNode("Soo Teck LRT", "lrt", 1.405392, 103.897285))
        self.lrt_nodes.append(MapNode("Sumang LRT", "lrt", 1.408428, 103.898619))
        self.lrt_nodes.append(MapNode("Nibong", "lrt", 1.411841, 103.900335))
        self.lrt_nodes.append(MapNode("Nibfsdfdsong", "lrt", 1.39693, 103.90888))

    def test_function(self):
        print("Hi")
