from tkinter import *
from tkinter import ttk
from MapCanvas import *
import Application as app


class FrameGUI(Frame):
    WINDOW_TITLE = "1008 Project"
    WINDOW_MIN_WIDTH = 700
    WINDOW_MIN_HEIGHT = 300
    ICON_PATH = "images/sit_icon.ico"

    def __init__(self, master, application):
        self.application = application
        self.selected_node = None
        self.create_window(master)
        self.create_gui()

    def create_window(self, master):
        Frame.__init__(self, master)
        master.title(FrameGUI.WINDOW_TITLE)
        master.minsize(FrameGUI.WINDOW_MIN_WIDTH, FrameGUI.WINDOW_MIN_HEIGHT)
        master.iconbitmap(FrameGUI.ICON_PATH)
        #master.resizable(False, False)
        self.pack(anchor = "w", padx = (10, 10), pady = (10, 10))

    def create_gui(self):
        """ Creates all the GUI to be rendered onto the program window
            Add new GUI elements here
        """
        self.lrtstop = []
        self.lrtstop = app.get_lrt()
        self.busstop = []
        self.busstop = app.get_busstop()
        self.hdb = []
        self.hdb = app.get_hdb()

        #Tab controls
        self.tab_control = ttk.Notebook(self)
        self.tab_control.grid(row = 0, column = 0, sticky = "w")

        #Change font for tab
        s = ttk.Style()
        s.configure('TNotebook.Tab', font = ('Calibri', 10, 'bold'))

        "----------------------------------------------------------------------------------------------------------"
        #Map tab
        self.map_tab = Frame(self.tab_control)
        self.map_tab.grid(row = 0, column = 0, sticky = "w")
        self.tab_control.add(self.map_tab, text = "Tab 01")

        #Left side panel
        self.left_panel_frame = Frame(self.map_tab)
        self.left_panel_frame.grid(row = 0, column = 0, sticky = "nsew", padx = 10)

        self.map_control_frame = LabelFrame(self.left_panel_frame, text = "Map controls", font = ('Calibri', 9, 'bold'), width = 800)
        self.map_control_frame.grid(row = 0, column = 0, sticky = "nws", padx = 10)
        self.map_control_frame.grid_rowconfigure(0, minsize=5) #For padding at the top
        self.map_control_frame.grid_columnconfigure(0, minsize=255) #For padding at the top

        #Start point selection GUI
        self.start_point_label = Label(self.map_control_frame, text = "Select starting point", font = ('Calibri', 9))
        self.start_point_label.grid(row = 1, column = 0, sticky = "w", padx = 10)
        self.start_point_entry_text = StringVar()
        self.start_point_entry = Entry(self.map_control_frame, textvariable=self.start_point_entry_text)
        self.start_point_entry.grid(row = 2, column = 0, sticky="we", padx = 10)
        self.start_point_list = Listbox(self.map_control_frame, width = 25, height = 5, font = ('Calibri', 9))
        self.start_point_list.grid(row = 3, column = 0, sticky="we", padx = 10)

        #TEMPORARY
        self.start_point_list.insert(END, "----------LRT----------")
        for i in range(0, len(self.lrtstop)):
            self.start_point_list.insert(END, self.lrtstop[i])
        self.start_point_list.insert(END, "----------BUS----------")
        for i in range(0, len(self.busstop)):
            self.start_point_list.insert(END, self.busstop[i])
        self.start_point_list.insert(END, "----------HDB----------")
        for i in range(0, len(self.hdb)):
            self.start_point_list.insert(END, self.hdb[i])

        #End point selection GUI
        self.end_point_label = Label(self.map_control_frame, text = "Select ending point", font = ('Calibri', 9))
        self.end_point_label.grid(row = 4, column = 0, sticky = "w", padx = 10)
        self.end_point_entry_text = StringVar()
        self.end_point_entry = Entry(self.map_control_frame, textvariable=self.end_point_entry_text)
        self.end_point_entry.grid(row = 5, column = 0, sticky="we", padx = 10)
        self.end_point_list = Listbox(self.map_control_frame, width = 25, height = 5, font = ('Calibri', 9))
        self.end_point_list.grid(row = 6, column = 0, sticky="we", padx = 10)
        #TEMPORARY
        """
        self.start_point_list.insert(END, "----------LRT----------")
        for i in range(0, len(self.lrtstop)):
            self.start_point_list.insert(END, self.lrtstop[i])
        self.start_point_list.insert(END, "----------BUS----------")
        for i in range(0, len(self.busstop)):
            self.start_point_list.insert(END, self.busstop[i])
        self.start_point_list.insert(END, "----------HDB----------")
        for i in range(0, len(self.hdb)):
            self.start_point_list.insert(END, self.hdb[i])"""

        self.map_control_frame.grid_rowconfigure(7, minsize=10)
        self.find_path_button = Button(self.map_control_frame, text = "Find path", command = self.application.find_path)
        self.find_path_button.grid(row = 8, column = 0, sticky="we", padx = 10)

        "----------------------------------------------------------------------------------------------------------"
        #Node info
        self.node_info_frame = LabelFrame(self.left_panel_frame, text = "Node info", font = ('Calibri', 9, 'bold'))
        self.node_info_frame.grid(row = 1, column = 0, sticky = "n", padx = 10)
        self.node_info_frame.grid_rowconfigure(0, minsize=5) #For padding at the top
        self.node_info_frame.grid_columnconfigure(0, minsize=255) #For padding at the top

        self.node_info_name = Label(self.node_info_frame, text = "Name: ", font = ('Calibri', 9))
        self.node_info_name.grid(row = 0, column = 0, sticky = "w", padx = 10)
        self.node_info_type = Label(self.node_info_frame, text = "Type: ", font = ('Calibri', 9))
        self.node_info_type.grid(row = 1, column = 0, sticky = "w", padx = 10)
        self.node_info_lat = Label(self.node_info_frame, text = "Lattitude: ", font = ('Calibri', 9))
        self.node_info_lat.grid(row = 2, column = 0, sticky = "w", padx = 10)
        self.node_info_long = Label(self.node_info_frame, text = "Longitude: ", font = ('Calibri', 9))
        self.node_info_long.grid(row = 3, column = 0, sticky = "w", padx = 10)

        self.node_info_button_frame = Frame(self.node_info_frame)
        self.node_info_button_frame.grid(row = 4, column = 0, sticky="we", padx = 5)
        self.node_info_start_button = Button(self.node_info_button_frame, text = "Set start", command = self.set_start_node)
        self.node_info_start_button.grid(row = 0, column = 0, sticky="we", padx = 5)
        self.node_info_end_button = Button(self.node_info_button_frame, text = "Set end", command = self.set_end_node)
        self.node_info_end_button.grid(row = 0, column = 1, sticky="we", padx = 5)

        "----------------------------------------------------------------------------------------------------------"
        #Map options
        self.map_options_frame = LabelFrame(self.left_panel_frame, text = "Map options", font = ('Calibri', 9, 'bold'), width = 800)
        self.map_options_frame.grid(row = 2, column = 0, sticky = "nwse", padx = 10)
        self.map_options_frame.grid_rowconfigure(0, minsize=5) #For padding at the top
        #self.map_options_frame.grid_columnconfigure(0, minsize=255) #For padding at the top

        #Start point selection GUI
        self.checkbox_lrt_val = IntVar()
        self.checkbox_lrt = Checkbutton(self.map_options_frame, text = "LRT nodes", variable = self.checkbox_lrt_val, command = self.show_lrt_nodes)
        self.checkbox_lrt.grid(row = 0, column = 0, sticky = "w")
        self.checkbox_lrt.select()
        self.checkbox_mrt_val = IntVar()
        self.checkbox_mrt = Checkbutton(self.map_options_frame, text = "MRT nodes", variable = self.checkbox_mrt_val, command = self.show_mrt_nodes)
        self.checkbox_mrt.grid(row = 0, column = 1, sticky = "w")
        self.checkbox_mrt.select()
        self.checkbox_bus_val = IntVar()
        self.checkbox_bus = Checkbutton(self.map_options_frame, text = "bus nodes", variable = self.checkbox_bus_val, command = self.show_bus_nodes)
        self.checkbox_bus.grid(row = 1, column = 0, sticky = "w")
        self.checkbox_bus.select()
        self.checkbox_hdb_val = IntVar()
        self.checkbox_hdb = Checkbutton(self.map_options_frame, text = "HDB nodes", variable = self.checkbox_hdb_val, command = self.show_hdb_nodes)
        self.checkbox_hdb.grid(row = 1, column = 1, sticky = "w")
        self.checkbox_hdb.select()
        "----------------------------------------------------------------------------------------------------------"
        #Map canvas
        self.map_canvas = MapCanvas(self.map_tab, self.application, self, 800, 500)
        self.map_canvas.grid(row = 0, column = 1, sticky = "w")
    #TEMP TO REMOVE
    def create_test_path(self):
        path = []
        for i in range(10):
            path.append(self.application.all_nodes[i])
        self.display_path(path)

    def display_path(self, path):
        self.map_canvas.display_path(path)

    def set_node_info(self, node):
        self.selected_node = node

        self.node_info_name["text"] = "Name: " + str(node.node_name)
        self.node_info_type["text"] = "Type: " + str(node.node_type)
        self.node_info_lat["text"] = "Lattitude: " + str(node.position.lattitude)
        self.node_info_long["text"] = "Longitude: " + str(node.position.longitude)

    def set_start_node(self):
        self.application.selected_start_node = self.selected_node
        self.start_point_entry_text.set(str(self.selected_node.node_name))

    def set_end_node(self):
        self.application.selected_end_node = self.selected_node
        self.end_point_entry_text.set(str(self.selected_node.node_name))

    def show_lrt_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_lrt_val.get(), "lrt")
    def show_mrt_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_mrt_val.get(), "mrt")
    def show_hdb_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_hdb_val.get(), "hdb")
    def show_bus_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_bus_val.get(), "bus")
