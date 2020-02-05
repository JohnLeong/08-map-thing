from tkinter import *
from tkinter import ttk

class FrameGUI(Frame):
    WINDOW_TITLE = "1008 Project"
    WINDOW_MIN_WIDTH = 700
    WINDOW_MIN_HEIGHT = 300
    ICON_PATH = "images/sit_icon.ico"

    NODE_SIZE = 10
    MAP_BOUNDS_X = (103.886964, 103.931048)
    MAP_BOUNDS_Y = (1.385900, 1.421450)
    MAP_SIZE_X = 500 #size of the rendered map image, TEMPORARY
    MAP_SIZE_Y = 500

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
        #Map controls frame
        self.map_tab = Frame(self.tab_control)
        self.map_tab.grid(row = 0, column = 0, sticky = "w")
        self.map_tab.grid_rowconfigure(0, minsize = 10)
        self.tab_control.add(self.map_tab, text = "Tab 01")

        self.map_control_frame = LabelFrame(self.map_tab, text = "Map controls", font = ('Calibri', 9, 'bold'), width = 800)
        self.map_control_frame.grid(row = 0, column = 0, sticky = "nw", padx = 10)
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
        #Map canvas
        self.map_canvas = Canvas(self.map_tab, width=400, height=300, background="#00ffff")
        self.map_canvas.grid(row = 0, column = 1, sticky = "w")
        self.map_canvas.bind("<ButtonPress-1>", self.move_start)
        self.map_canvas.bind("<B1-Motion>", self.move_move)

        #TEMPORARY
        self.img = PhotoImage(file="images/p2.png")
        self.map_canvas.create_image(self.img.width() * 0.5, self.img.height() * -0.5, image=self.img)
        FrameGUI.MAP_SIZE_X = self.img.width()
        FrameGUI.MAP_SIZE_Y = self.img.height()
        self.map_canvas.scan_dragto(0, 400, gain=1)
        #self.map_canvas.create_rectangle(0, 0, 10, 10, fill="blue")

        self.create_all_map_icons()
        self.draw_all_map_icons()

    def move_start(self, event):
        """Sets the start point of the map canvas move

        Parameters:
        event (?):    The mouse click event
        """
        self.map_canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        """Moves the map canvas view to the position the mouse is dragged to

        Parameters:
        event (?):    The mouse click event
        """
        self.map_canvas.scan_dragto(event.x, event.y, gain=1)

    def create_all_map_icons(self):
        for item in self.application.lrt_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.x, item.position.y)
            print(item.node_name)
            print(render_x)
            print(render_y)
            item.map_icon = self.map_canvas.create_rectangle(render_x, render_y, render_x + FrameGUI.NODE_SIZE, render_y + FrameGUI.NODE_SIZE, fill="blue")

    def draw_all_map_icons(self):
        self.draw_hdb_icons()
        self.draw_mrt_icons()
        self.draw_lrt_icons()
        self.draw_bus_icons()

    def draw_hdb_icons(self, viewable = True):
        pass

    def draw_mrt_icons(self, viewable = True):
        pass

    def draw_lrt_icons(self, viewable = True):
        pass

    def draw_bus_icons(self, viewable = True):
        pass

    def get_icon_render_pos(self, x, y):
        render_x = (x - FrameGUI.MAP_BOUNDS_X[0]) / (FrameGUI.MAP_BOUNDS_X[1] - FrameGUI.MAP_BOUNDS_X[0])
        render_y = (y - FrameGUI.MAP_BOUNDS_Y[0]) / (FrameGUI.MAP_BOUNDS_Y[1] - FrameGUI.MAP_BOUNDS_Y[0])
        render_x = render_x * FrameGUI.MAP_SIZE_X
        render_y = render_y * FrameGUI.MAP_SIZE_Y
        return render_x, -render_y
