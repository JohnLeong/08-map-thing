from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from MapCanvas import *
import Application as app
import Strings

class FrameGUI(Frame):
    WINDOW_TITLE = "1008 Project"           #The text to display in the window title
    WINDOW_MIN_WIDTH = 700                  #The minimum width of the window
    WINDOW_MIN_HEIGHT = 300                 #The minimum height of the window
    ICON_PATH = "images/sit_icon.ico"       #The file path of the image used as the window icon
    ENTRY_VALID_COL = "#d0ffc9"             #The color for the entry GUI element when it is valid
    ENTRY_INVALID_COL = "White"             #The color for the entry GUI element when it is invalid

    def __init__(self, master, application):
        self.application = application
        self.selected_node = None
        self.create_window(master)
        self.create_gui()

    def create_window(self, master):
        """ Creates the tkinter window along with the GUI elements

        Parameters:
        master:         The root tkinter object
        """
        Frame.__init__(self, master)
        master.title(FrameGUI.WINDOW_TITLE)
        master.minsize(FrameGUI.WINDOW_MIN_WIDTH, FrameGUI.WINDOW_MIN_HEIGHT)
        master.iconbitmap(FrameGUI.ICON_PATH)
        #master.resizable(False, False)
        self.pack(anchor = "w", padx = (10, 10), pady = (10, 10))

    def create_gui(self):
        """ Creates all the GUI to be rendered onto the program window
        """
        #Tab controls
        self.tab_control = ttk.Notebook(self)
        self.tab_control.grid(row = 0, column = 0, sticky = "w")

        #Change font for tab
        s = ttk.Style()
        s.configure('TNotebook.Tab', font = ('Calibri', 10, 'bold'))

        "----------------------------------------------------------------------------------------------------------"
        #Map tab, tab01
        self.map_tab = Frame(self.tab_control)
        self.map_tab.grid(row = 0, column = 0, sticky = "w")
        self.tab_control.add(self.map_tab, text = "Map")

        #Left side panel
        self.left_panel_frame = Frame(self.map_tab)
        self.left_panel_frame.grid(row = 0, column = 0, sticky = "nsew", padx = 10)

        #Scroll canvas
        self.left_panel_canvas = Canvas(self.left_panel_frame, width = 300, height = 500)
        self.left_panel_scrollbar = Scrollbar(self.left_panel_frame, orient="vertical", command=self.left_panel_canvas.yview)
        self.left_panel_inner_frame = Frame(self.left_panel_canvas)
        self.left_panel_canvas.create_window(0, 0, anchor = 'nw', window = self.left_panel_inner_frame)

        "----------------------------------------------------------------------------------------------------------"
        self.map_control_frame = LabelFrame(self.left_panel_inner_frame, text = "Map controls", font = ('Calibri', 9, 'bold'), width = 800)
        self.map_control_frame.grid(row = 0, column = 0, sticky = "nws", padx = 10)
        self.map_control_frame.grid_rowconfigure(0, minsize=5) #For padding at the top
        self.map_control_frame.grid_columnconfigure(0, minsize=255)

        #Start point selection GUI
        self.start_point_label = Label(self.map_control_frame, text = "Select starting point", font = ('Calibri', 9))
        self.start_point_label.grid(row = 1, column = 0, sticky = "w", padx = 10)
        self.start_point_entry_text = StringVar()
        self.start_point_entry = Entry(self.map_control_frame, textvariable=self.start_point_entry_text)
        self.start_point_entry.grid(row = 2, column = 0, sticky="we", padx = 10)
        self.start_point_list_frame = Frame(self.map_control_frame)
        self.start_point_list_frame.grid(row = 3, column = 0, sticky="we", padx = 10)
        self.start_point_list = Listbox(self.start_point_list_frame, width = 40, height = 6, font = ('Calibri', 9))
        self.start_point_list.grid(row = 0, column = 0, sticky="we")
        self.start_point_list_scrollbar = ttk.Scrollbar(self.start_point_list_frame, orient = VERTICAL)
        self.start_point_list_scrollbar.configure(command = self.start_point_list.yview)
        self.start_point_list_scrollbar.grid(row = 0, column = 1, sticky = "ns")
        self.start_point_list.configure(yscrollcommand = self.start_point_list_scrollbar.set)

        #Add all nodes to starting listbox
        self.start_point_list.insert(END, "--------MRT/LRT--------")
        self.add_nodes_to_listbox(self.application.lrt_nodes, self.start_point_list)
        # self.start_point_list.insert(END, "----------BUS----------")
        # self.add_nodes_to_listbox(self.application.bus_stop_nodes, self.start_point_list)
        # self.start_point_list.insert(END, "----------HDB----------")
        # self.add_nodes_to_listbox(self.application.hdb_nodes, self.start_point_list)

        #End point selection GUI
        self.end_point_label = Label(self.map_control_frame, text = "Select ending point", font = ('Calibri', 9))
        self.end_point_label.grid(row = 4, column = 0, sticky = "w", padx = 10)
        self.end_point_entry_text = StringVar()
        self.end_point_entry = Entry(self.map_control_frame, textvariable=self.end_point_entry_text)
        self.end_point_entry.grid(row = 5, column = 0, sticky="we", padx = 10)
        self.end_point_list_frame = Frame(self.map_control_frame)
        self.end_point_list_frame.grid(row = 6, column = 0, sticky="we", padx = 10)
        self.end_point_list = Listbox(self.end_point_list_frame, width = 40, height = 6, font = ('Calibri', 9))
        self.end_point_list.grid(row = 0, column = 0, sticky="we")
        self.end_point_list_scrollbar = ttk.Scrollbar(self.end_point_list_frame, orient = VERTICAL)
        self.end_point_list_scrollbar.configure(command = self.end_point_list.yview)
        self.end_point_list_scrollbar.grid(row = 0, column = 1, sticky = "ns")
        self.end_point_list.configure(yscrollcommand = self.end_point_list_scrollbar.set)

        #Add all nodes to ending listbox
        self.end_point_list.insert(END, "--------MRT/LRT--------")
        self.add_nodes_to_listbox(self.application.lrt_nodes, self.end_point_list)
        self.end_point_list.insert(END, "----------BUS----------")
        self.add_nodes_to_listbox(self.application.bus_stop_nodes, self.end_point_list)
        self.end_point_list.insert(END, "----------HDB----------")
        self.add_nodes_to_listbox(self.application.hdb_nodes, self.end_point_list)

        self.path_type_label = Label(self.map_control_frame, text="Preferred path", font = ('Calibri', 9))
        self.path_type_label.grid(row = 7, column = 0, sticky="w", padx = 10)
        self.path_type_options = ["Sheltered/Fastest", "Cheapest"]
        self.path_type_string = StringVar()
        self.path_type_string.set(self.path_type_options[0])
        self.path_type_selection = OptionMenu(self.map_control_frame, self.path_type_string, *self.path_type_options)
        self.path_type_selection.grid(row = 8, column = 0, sticky="we", padx = 10)
        self.find_path_button = Button(self.map_control_frame, text = "Find path", command = lambda: self.application.find_path(self.path_type_string.get()))
        self.find_path_button.grid(row = 9, column = 0, sticky="we", padx = 10, pady = 10)

        "----------------------------------------------------------------------------------------------------------"
        #Node info
        self.node_info_frame = LabelFrame(self.left_panel_inner_frame, text = "Node info", font = ('Calibri', 9, 'bold'))
        self.node_info_frame.grid(row = 1, column = 0, sticky = "nsew", padx = 10)
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
        #Path info
        self.path_info_frame = LabelFrame(self.left_panel_inner_frame, text = "Path info", font = ('Calibri', 9, 'bold'))
        self.path_info_frame.grid(row = 2, column = 0, sticky = "nwse", padx = 10)
        self.path_info_frame.grid_rowconfigure(0, minsize=5) #For padding at the top

        self.path_info_start = Label(self.path_info_frame, text = "Start point: ", font = ('Calibri', 9))
        self.path_info_start.grid(row = 0, column = 0, sticky = "w", padx = 10)
        self.path_info_end = Label(self.path_info_frame, text = "End point: ", font = ('Calibri', 9))
        self.path_info_end.grid(row = 1, column = 0, sticky = "w", padx = 10)
        self.path_info_dist = Label(self.path_info_frame, text = "Total distance: ", font = ('Calibri', 9))
        self.path_info_dist.grid(row = 2, column = 0, sticky = "w", padx = 10)
        self.path_info_walk_dist = Label(self.path_info_frame, text = "Walking distance: ", font = ('Calibri', 9))
        self.path_info_walk_dist.grid(row = 3, column = 0, sticky = "w", padx = 10)
        self.path_info_bus_dist = Label(self.path_info_frame, text = "Bus distance: ", font = ('Calibri', 9))
        self.path_info_bus_dist.grid(row = 4, column = 0, sticky = "w", padx = 10)
        self.path_info_mrt_dist = Label(self.path_info_frame, text = "MRT/LRT distance: ", font = ('Calibri', 9))
        self.path_info_mrt_dist.grid(row = 5, column = 0, sticky = "w", padx = 10)
        self.path_info_travel_cost = Label(self.path_info_frame, text = "Travel costs: ", font = ('Calibri', 9))
        self.path_info_travel_cost.grid(row = 6, column = 0, sticky = "w", padx = 10)
        self.path_info_calories = Label(self.path_info_frame, text = "Calories burnt: ", font = ('Calibri', 9))
        self.path_info_calories.grid(row = 7, column = 0, sticky = "w", padx = 10)

        self.path_info_button_frame = Frame(self.path_info_frame)
        self.path_info_button_frame.grid(row = 8, column = 0, sticky="we", padx = 5)
        self.path_info_clear_button = Button(self.path_info_button_frame, text = "Clear path", command=self.application.clear_path_info)
        self.path_info_clear_button.grid(row = 0, column = 0, sticky="we", padx = 5)
        self.path_info_save_button = Button(self.path_info_button_frame, text = "Save path info", command=self.save_path_info)
        self.path_info_save_button.grid(row = 0, column = 1, sticky="we", padx = 5)
        self.path_info_load_button = Button(self.path_info_button_frame, text = "Load path info", command=self.load_path_info)
        self.path_info_load_button.grid(row = 0, column = 2, sticky="we", padx = 5)

        "----------------------------------------------------------------------------------------------------------"
        #Map options
        self.map_options_frame = LabelFrame(self.left_panel_inner_frame, text = "Map options", font = ('Calibri', 9, 'bold'), width = 800)
        self.map_options_frame.grid(row = 3, column = 0, sticky = "nwse", padx = 10)
        self.map_options_frame.grid_rowconfigure(0, minsize=5) #For padding at the top

        #Start point selection GUI
        self.checkbox_lrt_val = IntVar()
        self.checkbox_lrt = Checkbutton(self.map_options_frame, text = "LRT/MRT nodes", variable = self.checkbox_lrt_val, command = self.show_lrt_nodes)
        self.checkbox_lrt.grid(row = 0, column = 0, sticky = "w")
        self.checkbox_lrt.select()
        self.checkbox_mrt_val = IntVar()
        # self.checkbox_mrt = Checkbutton(self.map_options_frame, text = "MRT nodes", variable = self.checkbox_mrt_val, command = self.show_mrt_nodes)
        # self.checkbox_mrt.grid(row = 0, column = 1, sticky = "w")
        # self.checkbox_mrt.select()
        self.checkbox_bus_val = IntVar()
        self.checkbox_bus = Checkbutton(self.map_options_frame, text = "Bus nodes", variable = self.checkbox_bus_val, command = self.show_bus_nodes)
        self.checkbox_bus.grid(row = 0, column = 1, sticky = "w")
        self.checkbox_bus.select()
        self.checkbox_hdb_val = IntVar()
        self.checkbox_hdb = Checkbutton(self.map_options_frame, text = "HDB nodes", variable = self.checkbox_hdb_val, command = self.show_hdb_nodes)
        self.checkbox_hdb.grid(row = 1, column = 0, sticky = "w")
        self.checkbox_hdb.select()

        self.left_panel_canvas.update_idletasks()
        self.left_panel_canvas.configure(scrollregion = self.left_panel_canvas.bbox('all'), yscrollcommand = self.left_panel_scrollbar.set)
        self.left_panel_canvas.grid(row = 0, column = 0, sticky = "nsew")
        self.left_panel_scrollbar.grid(row = 0, column = 1, sticky = "ns")
        "----------------------------------------------------------------------------------------------------------"
        #Map canvas
        self.map_canvas = MapCanvas(self.map_tab, self.application, self, 600, 500)
        self.map_canvas.grid(row = 0, column = 1, sticky = "w")
        "----------------------------------------------------------------------------------------------------------"
        #Credits tab, tab02
        self.credits_tab = Frame(self.tab_control)
        self.credits_tab.grid(row = 0, column = 0, sticky = "w")
        self.tab_control.add(self.credits_tab, text = "Credits")

        self.credits_info_frame = LabelFrame(self.credits_tab, text="Project Info", font = ('Calibri', 9, 'bold'))
        self.credits_info_frame.grid(row = 0, column = 0, sticky = "w", padx = 10)
        self.credits_info_label = Label(self.credits_info_frame, text=Strings.STR_PROJECT_INFO, font = ('Calibri', 9), justify=LEFT)
        self.credits_info_label.grid(row = 0, column = 0, sticky = "w", padx = 10)

        self.credits_member_frame = LabelFrame(self.credits_tab, text="Team members", font = ('Calibri', 9, 'bold'))
        self.credits_member_frame.grid(row = 1, column = 0, sticky = "w", padx = 10)
        self.credits_member_label_1 = Label(self.credits_member_frame, text=Strings.STR_MEMBER_01)
        self.credits_member_label_1.grid(row = 0, column = 0, sticky = "w")
        self.credits_member_label_2 = Label(self.credits_member_frame, text=Strings.STR_MEMBER_02)
        self.credits_member_label_2.grid(row = 1, column = 0, sticky = "w")
        self.credits_member_label_3 = Label(self.credits_member_frame, text=Strings.STR_MEMBER_03)
        self.credits_member_label_3.grid(row = 2, column = 0, sticky = "w")
        self.credits_member_label_4 = Label(self.credits_member_frame, text=Strings.STR_MEMBER_04)
        self.credits_member_label_4.grid(row = 3, column = 0, sticky = "w")
        self.credits_member_label_5 = Label(self.credits_member_frame, text=Strings.STR_MEMBER_05)
        self.credits_member_label_5.grid(row = 4, column = 0, sticky = "w")
        self.credits_member_label_6 = Label(self.credits_member_frame, text=Strings.STR_MEMBER_06)
        self.credits_member_label_6.grid(row = 5, column = 0, sticky = "w")
        "----------------------------------------------------------------------------------------------------------"
        #callbacks for when user manually inputs values to the start and and point entries
        self.start_point_entry_text.trace("w", lambda *_, sv=self.start_point_entry_text: self.callback_start(sv))
        self.end_point_entry_text.trace("w", lambda *_, sv=self.end_point_entry_text: self.callback_end(sv))

        #binding of each selection of start and end node list boxes to 'single clicks'
        #function will run when user makes a new click in the list box
        self.start_point_list.bind('<ButtonRelease-1>', self.search_and_set_start_node)
        self.end_point_list.bind('<ButtonRelease-1>', self.search_and_set_end_node)

    def set_node_info(self, node):
        """ Gets the information from a specified node and displays it on the GUI

        Parameters:
        node:           The target node
        """
        self.selected_node = node
        self.node_info_name["text"] = "Name: " + str(node.node_name)
        self.node_info_type["text"] = "Type: " + str(node.node_type)
        self.node_info_lat["text"] = "Lattitude: " + str(node.position.lattitude)
        self.node_info_long["text"] = "Longitude: " + str(node.position.longitude)

    def set_start_node(self):
        """ Takes the currently selected node and sets it as the start point
        """
        if (self.selected_node):
            self.start_point_entry_text.set(str(self.selected_node.node_name))
            self.start_point_entry.config({"background": FrameGUI.ENTRY_VALID_COL})
            self.application.selected_start_node = self.selected_node

    def set_end_node(self):
        """ Takes the currently selected node and sets it as the end point
        """
        if (self.selected_node):
            self.end_point_entry_text.set(str(self.selected_node.node_name))
            self.end_point_entry.config({"background": FrameGUI.ENTRY_VALID_COL})
            self.application.selected_end_node = self.selected_node

    def unset_start_node(self):
        """ Unsets the current start node and clears the start entry box
        """
        self.start_point_entry.config({"background": FrameGUI.ENTRY_INVALID_COL})
        self.application.selected_start_node = None

    def unset_end_node(self):
        """ Unsets the current end node and clears the end entry box
        """
        self.end_point_entry.config({"background": FrameGUI.ENTRY_INVALID_COL})
        self.application.selected_end_node = None

    def show_lrt_nodes(self):
        """ Toggles the visibility of the lrt nodes
        """
        self.map_canvas.set_icon_visibility(self.checkbox_lrt_val.get(), "lrt")
    def show_mrt_nodes(self):
        """ Toggles the visibility of the mrt nodes
        """
        self.map_canvas.set_icon_visibility(self.checkbox_mrt_val.get(), "mrt")
    def show_hdb_nodes(self):
        """ Toggles the visibility of the hdb nodes
        """
        self.map_canvas.set_icon_visibility(self.checkbox_hdb_val.get(), "hdb")
    def show_bus_nodes(self):
        """ Toggles the visibility of the bus nodes
        """
        self.map_canvas.set_icon_visibility(self.checkbox_bus_val.get(), "bus")

    def callback_start(self, sv):
        """ Callback function that will be called when the start textbox(Entry) is updated
        """
        self.unset_start_node()
        usertext = str(sv.get())
        self.start_point_list.delete(0, END)

        self.start_point_list.insert(END, "----------LRT----------")
        self.add_names_to_listbox(usertext, self.application.lrt_nodes, self.start_point_list)
        # self.start_point_list.insert(END, "----------BUS----------")
        # self.add_names_to_listbox(usertext, self.application.bus_stop_nodes, self.start_point_list)
        # self.start_point_list.insert(END, "----------HDB----------")
        # self.add_names_to_listbox(usertext, self.application.hdb_nodes, self.start_point_list)

    def callback_end(self, sv):
        """ Callback function that will be called when the end textbox(Entry) is updated
        """
        self.unset_end_node()
        usertext = str(sv.get())
        self.end_point_list.delete(0, END)

        self.end_point_list.insert(END, "----------LRT----------")
        self.add_names_to_listbox(usertext, self.application.lrt_nodes, self.end_point_list)
        self.end_point_list.insert(END, "----------BUS----------")
        self.add_names_to_listbox(usertext, self.application.bus_stop_nodes, self.end_point_list)
        self.end_point_list.insert(END, "----------HDB----------")
        self.add_names_to_listbox(usertext, self.application.hdb_nodes, self.end_point_list)

    def add_names_to_listbox(self, name, target_list, target_listbox):
        """ Iterates through a target list for nodes that have a name containing a specified string
            Populates the target listbox with nodes that match

        Parameters:
        name:               The string to search for in the nodes
        target_list:        The target list to look through
        target_listbox:     The target listbox to populate
        """
        name = name.lower()
        for i in range(len(target_list)):
            if name in target_list[i].node_name.lower():
                target_listbox.insert(END, target_list[i].node_name)

    def add_nodes_to_listbox(self, target_list, target_listbox):
        """ Iterates through a target list and adds all of them into a target listbox

        Parameters:
        target_list:        The target list to look through
        target_listbox:     The target listbox to populate
        """
        for i in range(len(target_list)):
            target_listbox.insert(END, target_list[i].node_name)

    def search_and_set_start_node(self, event):
        """ Gets the selected text in the start listbox and searches through the all_nodes array
            for node with the same node name
        """
        index = self.start_point_list.curselection()
        seltext = self.start_point_list.get(index)
        if (len(seltext) < 0 or seltext[0] == "-"):
            return

        #Binary search through the all_nodes array to find the node corr. to listbox selection name
        nodestart = self.application.bin_search_all_nodes(seltext)

        # append the selection text to textbox
        self.start_point_entry.delete(0, END)
        self.start_point_entry.insert(0, nodestart.node_name)

        #assign node as the selected start node
        self.application.selected_start_node = nodestart
        self.start_point_entry.config({"background": FrameGUI.ENTRY_VALID_COL})

    def search_and_set_end_node(self, event):
        """ Gets the selected text in the end listbox and searches through the all_nodes array
            for node with the same node name
        """
        index = self.end_point_list.curselection()
        seltext = self.end_point_list.get(index)
        if (len(seltext) < 0 or seltext[0] == "-"):
            return

        #bin search through the all_nodes array to find the node corr. to listbox selection name
        nodeend = self.application.bin_search_all_nodes(seltext)

        #append the selection text to textbox
        self.end_point_entry.delete(0, END)
        self.end_point_entry.insert(0, nodeend.node_name)

        #assign node as selected end node
        self.application.selected_end_node = nodeend
        self.end_point_entry.config({"background": FrameGUI.ENTRY_VALID_COL})

    def save_path_info(self):
        """ Callback function for when the user clicks the save path button
            Displays a file dialog for the user to select a save path
            Checks that the selected save path is valid
        """
        file_path = filedialog.asksaveasfilename(initialdir = "/", title = "Save as", defaultextension=".txt", filetypes = (("Path info files","*.txt"),("all files","*.*")))
        if(len(file_path) < 1):
            messagebox.showerror("Invalid file path", "File not saved")
        else:
            result = self.application.save_path_info(file_path)


    def load_path_info(self):
        """ Callback function for when the user clicks the load path button
            Displays a file dialog for the user to select a file to load
            Checks that the selected file is valid
        """
        file_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("Path info files","*.txt"),("all files","*.*")))
        if(len(file_path) < 1):
            messagebox.showerror("Invalid file path", "File not loaded")
        else:
            self.application.load_path_info(file_path)

    def clear_path_info(self):
        """ Clears the path info GUI
        """
        self.map_canvas.clear_path()
        self.path_info_start["text"] = "Start point: "
        self.path_info_end["text"] = "End_point: "
        self.path_info_dist["text"] = "Total distance: "
        self.path_info_walk_dist["text"] = "Walking distance: "
        self.path_info_bus_dist["text"] = "Bus distance: "
        self.path_info_mrt_dist["text"] = "MRT/LRT distance: "
        self.path_info_travel_cost["text"] = "Travel costs: "
        self.path_info_calories["text"] = "Calories burnt: "

    def display_path_info(self, path):
        """ Displays the path info of a specified path onto the GUI

        Parameters:
        path:               The target list of nodes which form a path
        """
        total_dist, walking_dist, bus_dist, lrt_dist = app.Application.find_path_distance(path)
        self.path_info_start["text"] = "Start point: " + path[0].node_name
        self.path_info_end["text"] = "End point: " + path[-1].node_name

        self.path_info_dist["text"] = "Total distance: " + str(round(total_dist, 3)) + "km"
        self.path_info_walk_dist["text"] = "Walking distance: " + str(round(walking_dist, 3)) + "km"
        self.path_info_bus_dist["text"] = "Bus distance: " + str(round(bus_dist, 3)) + "km"
        self.path_info_mrt_dist["text"] = "MRT/LRT distance: " + str(round(lrt_dist, 3)) + "km"

        ## TODO: Calculate travel costs based on distance
        # TODO: Calculate calories burnt from walking
        self.path_info_travel_cost["text"] = "Travel costs: "
        self.path_info_calories["text"] = "Calories burnt: " + str(app.Application.calculate_calories_burnt(walking_dist * 1000))
