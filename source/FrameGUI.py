from tkinter import *
from tkinter import ttk
from MapCanvas import *

class FrameGUI(Frame):
    WINDOW_TITLE = "1008 Project"
    WINDOW_MIN_WIDTH = 700
    WINDOW_MIN_HEIGHT = 300
    ICON_PATH = "images/sit_icon.ico"

    def __init__(self, master, application):
        self.application = application
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
        self.start_point_entry = Entry(self.map_control_frame)
        self.start_point_entry.grid(row = 2, column = 0, sticky="we", padx = 10)
        self.start_point_list = Listbox(self.map_control_frame, width = 25, height = 5, font = ('Calibri', 9))
        self.start_point_list.grid(row = 3, column = 0, sticky="we", padx = 10)
        #TEMPORARY
        self.start_point_list.insert(END, "bus stop 1")
        self.start_point_list.insert(END, "mrt 1")
        self.start_point_list.insert(END, "hdb 1")

        #End point selection GUI
        self.end_point_label = Label(self.map_control_frame, text = "Select ending point", font = ('Calibri', 9))
        self.end_point_label.grid(row = 4, column = 0, sticky = "w", padx = 10)
        self.end_point_entry = Entry(self.map_control_frame)
        self.end_point_entry.grid(row = 5, column = 0, sticky="we", padx = 10)
        self.end_point_list = Listbox(self.map_control_frame, width = 25, height = 5, font = ('Calibri', 9))
        self.end_point_list.grid(row = 6, column = 0, sticky="we", padx = 10)
        #TEMPORARY
        self.end_point_list.insert(END, "bus stop 1")
        self.end_point_list.insert(END, "mrt 1")
        self.end_point_list.insert(END, "hdb 1")

        "----------------------------------------------------------------------------------------------------------"
        #Map options
        self.map_options_frame = LabelFrame(self.left_panel_frame, text = "Map options", font = ('Calibri', 9, 'bold'), width = 800)
        self.map_options_frame.grid(row = 1, column = 0, sticky = "n", padx = 10)
        self.map_options_frame.grid_rowconfigure(0, minsize=5) #For padding at the top
        self.map_options_frame.grid_columnconfigure(0, minsize=255) #For padding at the top

        #Start point selection GUI
        self.checkbox_lrt_val = IntVar()
        self.checkbox_lrt = Checkbutton(self.map_options_frame, text = "Show LRT nodes", variable = self.checkbox_lrt_val, command = self.show_lrt_nodes)
        self.checkbox_lrt.grid(row = 0, column = 0, sticky = "w")
        self.checkbox_lrt.select()
        self.checkbox_mrt_val = IntVar()
        self.checkbox_mrt = Checkbutton(self.map_options_frame, text = "Show MRT nodes", variable = self.checkbox_mrt_val, command = self.show_mrt_nodes)
        self.checkbox_mrt.grid(row = 1, column = 0, sticky = "w")
        self.checkbox_mrt.select()
        self.checkbox_bus_val = IntVar()
        self.checkbox_bus = Checkbutton(self.map_options_frame, text = "Show bus nodes", variable = self.checkbox_bus_val, command = self.show_bus_nodes)
        self.checkbox_bus.grid(row = 2, column = 0, sticky = "w")
        self.checkbox_bus.select()
        self.checkbox_hdb_val = IntVar()
        self.checkbox_hdb = Checkbutton(self.map_options_frame, text = "Show HDB nodes", variable = self.checkbox_hdb_val, command = self.show_hdb_nodes)
        self.checkbox_hdb.grid(row = 3, column = 0, sticky = "w")
        self.checkbox_hdb.select()

        "----------------------------------------------------------------------------------------------------------"
        #Map canvas
        self.map_canvas = MapCanvas(self.map_tab, self.application, 800, 500)
        self.map_canvas.grid(row = 0, column = 1, sticky = "w")

    def show_lrt_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_lrt_val.get(), "lrt")
    def show_mrt_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_mrt_val.get(), "mrt")
    def show_hdb_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_hdb_val.get(), "hdb")
    def show_bus_nodes(self):
        self.map_canvas.set_icon_visibility(self.checkbox_bus_val.get(), "bus")
