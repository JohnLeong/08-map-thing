import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import MapNode
import pygame
import thorpy

class Application():

    WINDOW_TITLE = "1008 Project"
    ICON_PATH = "images/SIT_logo.png"

    def __init__(self, window_size_x = 1280, window_size_y = 720):
        self.running = True
        self.clock = pygame.time.Clock()
        self.window_size = (window_size_x, window_size_y)

        #Initialise program window
        pygame.init()
        self.window = pygame.display.set_mode((window_size_x, window_size_y))
        pygame.display.set_caption(Application.WINDOW_TITLE)
        pygame.display.set_icon(pygame.image.load(Application.ICON_PATH))
        self.render_surface = pygame.Surface((window_size_x, window_size_y))
        self.gui_surface = pygame.Surface((300, window_size_y))
        self.gui_surface.fill((0, 244, 255))
        self.init_gui()

        #Initialise map data
        self.bus_stop_list = []
        self.lrt_list = []
        self.hdb_list = []

    def init_gui(self):
        self.gui_list = []

        #Add GUI items here
        self.gui_heading = self.add_gui_item(thorpy.make_text("1008 Project", 22, (0, 0, 0)), position = (0, 0))
        self.gui_node_start = thorpy.Inserter(name="Start location: ", value="Write here.")

        self.slider = thorpy.SliderX(100, (12, 35), "My Slider")
        self.button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
        dropdownlist = thorpy.DropDownListLauncher(const_text="Choose:", var_text="", titles=[str(i)*i for i in range(1, 9)])
        self.box = thorpy.Box(elements=[self.slider,self.button, self.gui_node_start, dropdownlist])
        self.menu = thorpy.Menu(self.box)
        for element in self.menu.get_population():
            element.surface = self.gui_surface
        self.box.set_topleft((10, 50))
        self.box.blit()
        self.box.update()

    def add_gui_item(self, gui_item, position = (0, 0), react_to_events = False):
        gui_item.surface = self.gui_surface
        gui_item.set_topleft(position)
        gui_item.blit()
        gui_item.update()
        if (react_to_events == True):
            self.gui_list.append(gui_item)
        return gui_item

    def run(self):
        #The application loop of the program
        while (self.running == True):
            for event in pygame.event.get():
                #Check for closing of window
                if (event.type == pygame.QUIT):
                    self.running = False
                #Update GUI elements
                self.menu.react(event)
                for gui_item in self.gui_list:
                    gui_item.react(event)

            #self.render_surface.fill((146,244,255))
            #self.window.blit(pygame.transform.scale(self.render_surface, self.window_size),(0,0))
            self.render_surface.fill((146,244,255))
            self.window.blit(self.gui_surface, (0,0))
            self.window.blit(self.render_surface, (300,0))
            pygame.display.update()
            self.clock.tick(30)
