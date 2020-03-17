from tkinter import *
from tkinter import ttk

class MapCanvas(Canvas):
    BACKGROUND_COLOR = "#00ffff"
    MAP_IMAGE_PATH = "images/p2.png"
    MAP_BOUNDS_X = (103.886964, 103.931548)
    MAP_BOUNDS_Y = (1.385900, 1.421050)
    MAP_SIZE_X = 500 #size of the rendered map image, TEMPORARY
    MAP_SIZE_Y = 500
    NODE_SIZE = 5
    NODE_COL_LRT = "#00ffff"
    NODE_COL_MRT = "#fcba03"
    NODE_COL_BUS = "#ba03fc"
    NODE_COL_HDB = "#30de2a"

    def __init__(self, master, application, frame_gui, size_x, size_y):
        Canvas.__init__(self, master, width = size_x, height = size_y, background = MapCanvas.BACKGROUND_COLOR)
        self.frame_gui = frame_gui
        self.canvas_size_x = size_x
        self.canvas_size_y = size_y
        self.application = application
        self.selected_node = None
        self.path_lines = []
        self.node_icons = {}
        self.create_map()

    def create_map(self):
        #Bind the mouse events to allow the dragging of map
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<B1-Motion>", self.move_move)
        self.bind("<Motion>", self.on_move)

        #Create the map background image
        self.img = PhotoImage(file = MapCanvas.MAP_IMAGE_PATH)
        super().create_image(self.img.width() * 0.5, self.img.height() * -0.5, image=self.img)
        MapCanvas.MAP_SIZE_X = self.img.width()
        MapCanvas.MAP_SIZE_Y = self.img.height()
        self.scan_dragto(0, 500, gain=1)
        self.configure(scrollregion = self.bbox("all"))
        #self.map_canvas.create_rectangle(0, 0, 10, 10, fill="blue")

        self.create_all_map_icons()

    def move_start(self, event):
        """Sets the start point of the map canvas move

        Parameters:
        event (?):    The mouse click event
        """
        super().scan_mark(event.x, event.y)

    def move_move(self, event):
        """Moves the map canvas view to the position the mouse is dragged to

        Parameters:
        event (?):    The mouse click event
        """
        super().scan_dragto(event.x, event.y, gain=1)

    def on_click(self, event):
        self.move_start(event)

        items = super().find_closest(super().canvasx(event.x), super().canvasy(event.y), halo=5)
        item = items[0]
        if (self.selected_node is not None and item == self.selected_node.map_icon and len(items) > 1):
            item = items[1]

        if (item not in self.node_icons.keys()):
            return

        new_selected_node = self.node_icons[item]
        if (self.selected_node is not None):
            render_x, render_y = self.get_icon_render_pos(self.selected_node.position.longitude, self.selected_node.position.lattitude)
            super().coords(self.selected_node.map_icon, render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE)

        x1, y1, x2, y2 = super().coords(item)
        super().coords(item, x1 - MapCanvas.NODE_SIZE * 0.5, y1 - MapCanvas.NODE_SIZE * 0.5, x2 + MapCanvas.NODE_SIZE * 0.5, y2 + MapCanvas.NODE_SIZE * 0.5)
        self.frame_gui.set_node_info(new_selected_node)
        self.selected_node = new_selected_node
        super().tag_raise(new_selected_node)

    def on_move(self, event):
        pass

    def create_all_map_icons(self):
        for item in self.application.lrt_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_LRT, activeoutline="yellow")
            self.node_icons[item.map_icon] = item
        for item in self.application.mrt_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_MRT, activeoutline="yellow")
            self.node_icons[item.map_icon] = item
        for item in self.application.bus_stop_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_BUS, activeoutline="yellow")
            self.node_icons[item.map_icon] = item
        for item in self.application.hdb_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_HDB, activeoutline="yellow")
            self.node_icons[item.map_icon] = item

    def set_icon_visibility(self, viewable = True, target = "all"):
        target_list = None
        if (target == "all"):
            target_list = self.application.all_nodes
        elif (target == "hdb"):
            target_list = self.application.hdb_nodes
        elif (target == "lrt"):
            target_list = self.application.lrt_nodes
        elif (target == "mrt"):
            target_list = self.application.mrt_nodes
        elif (target == "bus"):
            target_list = self.application.bus_stop_nodes
        else:
            print("Could not set icon visibility of target: " + str(target))
            return

        visibility = 'normal' if viewable else 'hidden'
        for item in target_list:
            super().itemconfigure(item.map_icon, state = visibility)

    def get_icon_render_pos(self, x, y):
        render_x = (x - MapCanvas.MAP_BOUNDS_X[0]) / (MapCanvas.MAP_BOUNDS_X[1] - MapCanvas.MAP_BOUNDS_X[0])
        render_y = (y - MapCanvas.MAP_BOUNDS_Y[0]) / (MapCanvas.MAP_BOUNDS_Y[1] - MapCanvas.MAP_BOUNDS_Y[0])
        render_x = render_x * MapCanvas.MAP_SIZE_X
        render_y = render_y * MapCanvas.MAP_SIZE_Y
        return render_x, -render_y

    def display_path(self, path: list):
        """Displays a path on the map

        Parameters:
        path:    A list of mapnodes which form the path
        """
        self.path_lines = []
        #self.set_icon_visibility(viewable = False, target = "all")
        #for i in range(len(path)):
        #    super().itemconfigure(path[i].map_icon, state = 'normal')
        for i in range(len(path) - 1):
            start_x, start_y = self.get_icon_render_pos(path[i].position.longitude, path[i].position.lattitude)
            end_x, end_y = self.get_icon_render_pos(path[i + 1].position.longitude, path[i + 1].position.lattitude)
            self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill="red", width = 1))
