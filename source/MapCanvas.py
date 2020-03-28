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
    PATH_WIDTH = 1
    BUS_PATH_COL = "purple"
    LRT_PATH_COL = "blue"
    MRT_PATH_COL = "orange"
    WALK_PATH_COL = "green"

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
        """ Creates the entire map canvas GUI
        """
        #Bind the mouse events to allow the dragging of map
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<B1-Motion>", self.move_move)

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
        """ Sets the start point of the map canvas move

        Parameters:
        event (?):    The mouse event
        """
        super().scan_mark(event.x, event.y)

    def move_move(self, event):
        """ Moves the map canvas view to the position the mouse is dragged to

        Parameters:
        event (?):    The mouse event
        """
        super().scan_dragto(event.x, event.y, gain=1)

    def on_click(self, event):
        """ Check if the user has clicked on a node

        Parameters:
        event (?):    The mouse click event
        """
        self.move_start(event)

        items = super().find_closest(super().canvasx(event.x), super().canvasy(event.y), halo=1)
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

    def create_all_map_icons(self):
        """ Goes through all the lists of nodes and renders them as icons onto the map GUI
        """
        for item in self.application.lrt_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_LRT, activeoutline="yellow", tags="node")
            self.node_icons[item.map_icon] = item
        for item in self.application.mrt_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_MRT, activeoutline="yellow", tags="node")
            self.node_icons[item.map_icon] = item
        for item in self.application.bus_stop_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_BUS, activeoutline="yellow", tags="node")
            self.node_icons[item.map_icon] = item
        for item in self.application.hdb_nodes:
            render_x, render_y = self.get_icon_render_pos(item.position.longitude, item.position.lattitude)
            item.map_icon = super().create_rectangle(render_x, render_y, render_x + MapCanvas.NODE_SIZE, render_y + MapCanvas.NODE_SIZE, fill=MapCanvas.NODE_COL_HDB, activeoutline="yellow", tags="node")
            self.node_icons[item.map_icon] = item

    def set_icon_visibility(self, viewable = True, target = "all"):
        """ Sets the visibility of the target list of icons

        Parameters:
        viewable:       Whether the icons should be visible
        target:         The target list of icons
        """
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
        """ Converts a lattitude and longitude to coordinates to be rendered onto the map GUI

        Parameters:
        x:              The longitude
        y:              The lattitude
        """
        render_x = (x - MapCanvas.MAP_BOUNDS_X[0]) / (MapCanvas.MAP_BOUNDS_X[1] - MapCanvas.MAP_BOUNDS_X[0])
        render_y = (y - MapCanvas.MAP_BOUNDS_Y[0]) / (MapCanvas.MAP_BOUNDS_Y[1] - MapCanvas.MAP_BOUNDS_Y[0])
        render_x = render_x * MapCanvas.MAP_SIZE_X
        render_y = render_y * MapCanvas.MAP_SIZE_Y
        return render_x, -render_y

    def get_text_render_pos(self, x1, y1, x2, y2):
        """ Gets a position between 2 longitudes and lattitudes to bee rendered onto the map GUI

        Parameters:
        x1:              The longitude1
        y1:              The lattitude1
        x2:              The longitude2
        y2:              The lattitude2
        """
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return self.get_icon_render_pos(x, y)

    def clear_path(self):
        """ Clears any previously rendered paths on the GUI
        """
        #Clear previous path
        for i in range(len(self.path_lines) - 1, -1, -1):
            super().delete(self.path_lines[i])

    def display_path(self, path: list):
        """Displays a path on the map

        Parameters:
        path:    A list of mapnodes which form the path
        """
        self.clear_path()

        #Render new path
        for i in range(len(path) - 1):
            start_x, start_y = self.get_icon_render_pos(path[i].position.longitude, path[i].position.lattitude)
            end_x, end_y = self.get_icon_render_pos(path[i + 1].position.longitude, path[i + 1].position.lattitude)
            text_x, text_y = self.get_text_render_pos(path[i].position.longitude, path[i].position.lattitude, path[i + 1].position.longitude, path[i + 1].position.lattitude)

            #Get distance and convert to meters
            dist = int(path[i].position.real_distance_from(path[i + 1].position) * 1000)
            line_text = str(dist) + "m"
            if(path[i].node_type == path[i+1].node_type):
                if(path[i].node_type == "bus"):
                    bus_service = -1
                    for c in path[i].connections:
                        if (c[0].node_id == path[i + 1].node_id):
                            if (len(c) > 2):
                                bus_service = c[2]
                                break
                    if (bus_service != -1):
                        self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill=MapCanvas.BUS_PATH_COL, width=MapCanvas.PATH_WIDTH))
                        line_text += "\nBus " + bus_service
                    else:
                        self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill=MapCanvas.WALK_PATH_COL, width=MapCanvas.PATH_WIDTH))
                elif(path[i].node_type == "lrt"):
                    self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill=MapCanvas.LRT_PATH_COL, width=MapCanvas.PATH_WIDTH))
                elif(path[i].node_type == "mrt"):
                    self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill=MapCanvas.MRT_PATH_COL, width=MapCanvas.PATH_WIDTH))
                elif(path[i].node_type == "hdb"):
                    self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill=MapCanvas.WALK_PATH_COL, width=MapCanvas.PATH_WIDTH))
                else:
                    self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill=MapCanvas.WALK_PATH_COL, width=MapCanvas.PATH_WIDTH))
                    print("Unknown node combination: ", path[i].node_type, path[i+1].node_type)
            else:
                #Walking colour line
                self.path_lines.append(super().create_line(start_x, start_y, end_x, end_y, fill=MapCanvas.WALK_PATH_COL, width=MapCanvas.PATH_WIDTH))
            self.path_lines.append(super().create_text(text_x, text_y, text=line_text, font = ('Calibri', 10)))
        for line in self.path_lines:
            super().tag_lower(line, 2)
