import sys
import time
from configurations import *
from Controls import *
from BFS import *
from DFS import *
from Astar import *
from Dijkstra import *
from PathCreator import *

pygame.init()

class PathVisualizer:
    '''
    Constructor to create a GUI object
    '''
    def __init__(self):
        self.DISP = pygame.display.set_mode((WIDTH, HEIGHT)) # Display Object

        self.ACTIVE = True #Boolean to determine if the app is running

        self.CURR_STATUS = 'main menu' #Page GUI is currently on

        self.chosen_algo = ''#User's Algorithm of Choice

        self.grid_square_length = 24 # Each grid square is 24 by 24 huge

        self.image_load() # Load images

        self.num_positional_nodes = 0 #Counter of how many positional nodes exist in the grid. 1 => only starting, 2 => both end and start

        self.is_dragging = 0 #Determine if mouse is being dragged in the application. 1 => yes, 0 => no

        # Start and Ending Positions of Nodes
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # List of coordinates that act as borders
        self.border_positions = BORDERS.copy()




        # Define Main-Menu buttons
        self.BFS = Controller(self, ORANGE, 350, BUTTON_Y, BUTTON_LENGTH, BUTTON_HEIGHT, 'BFS')
        self.DFS = Controller(self, ORANGE, 570, BUTTON_Y, BUTTON_LENGTH, BUTTON_HEIGHT, 'DFS')
        self.ASTAR = Controller(self, ORANGE, 790, BUTTON_Y, BUTTON_LENGTH, BUTTON_HEIGHT, 'A-Star')
        self.DIJKSTRA = Controller(self, ORANGE, 1010, BUTTON_Y, BUTTON_LENGTH, BUTTON_HEIGHT, 'Dijkstra')

        # Define Grid-Menu buttons
        self.POSITIONS = Controller(self, ORANGE, 20, POSITIONAL_HEIGHT, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start/End')
        self.BARRIERS = Controller(self, ORANGE, 20, POSITIONAL_HEIGHT + GRID_BUTTON_HEIGHT + SPACE_LENGTH, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Barrier')
        self.CLEAR = Controller(self, ORANGE, 20, POSITIONAL_HEIGHT + GRID_BUTTON_HEIGHT * 2 + SPACE_LENGTH * 2, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Clear')
        self.FIND_PATH = Controller(self, ORANGE, 20, POSITIONAL_HEIGHT + GRID_BUTTON_HEIGHT * 3 + SPACE_LENGTH * 3, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Find Path')
        self.SWITCH_ALGO = Controller(self, ORANGE, 20, POSITIONAL_HEIGHT + GRID_BUTTON_HEIGHT * 4 + SPACE_LENGTH * 4, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Back')

    def run(self):
        #As long as the GUI is running
        while self.ACTIVE:

            #If the current page is the main menu
            if self.CURR_STATUS == 'main menu':
                self.run_menu()

            #If the current page is the grid window
            if self.CURR_STATUS == 'grid window':
                self.run_gridWindow()

            #If user chooser to draw something
            if self.CURR_STATUS == 'draw S/E' or self.CURR_STATUS == 'draw walls':
                self.node_maker()

            #If the user chooses to visualize the algorithm
            if self.CURR_STATUS == 'start visualizing':
                self.algorithm()

            #After the execution the algorithm, give user a chance to re-use the application
            if self.CURR_STATUS == 'aftermath':
                self.reuse_gui()

        pygame.quit()
        sys.exit()



##### Loading Images
    def image_load(self):
        '''
        ** Helper **
        Loads one image into existence
        '''
        self.main_menu_background = pygame.image.load('main_background.png')


##### Draw Text
    def write_something(self, words, screen, position, size, colour, font_name, centered=False):
        '''
        ** Helper **
        Function to write a text into the GUI..Became too repetitive so I made it into a function
        :param words: String to be displayed
        :param screen: Surface to be drawn
        :param position: Positioning of the string
        :param size: Font size
        :param colour: Colour of the String
        :param font_name: Type of font to be used
        :param centered: Boolean to decide whether string should be centred or not
        :return:
        '''
        font = pygame.font.SysFont(font_name, size) #Make Font Object
        text = font.render(words, False, colour) # Render object with no aliasing
        text_size = text.get_size() #acquires the length and width of the text as a tuple

        #If centred parameter was set to true, then centre the text by adjusting the position with formula below
        if centered:
            position[0] = position[0] - text_size[0] // 2 #Centres the length
            position[1] = position[1] - text_size[1] // 2 #Centres the Width

        screen.blit(text, position) #Display Text in screen

##### Setup for Main Menu
    def design_menu(self):
        '''
        ** Helper **
        Function to create the main menu of the GUI
        '''
        self.DISP.blit(self.main_menu_background, (0, 0)) #Display the background at (0,0)

        # Draw the buttons with AQUAMARINE OUTLINE
        self.BFS.make_controller(AQUAMARINE)
        self.DFS.make_controller(AQUAMARINE)
        self.ASTAR.make_controller(AQUAMARINE)
        self.DIJKSTRA.make_controller(AQUAMARINE)



    def design_hotbar(self):
        '''
        ** Helper **
        Function to create the LHS design of the GUI
        To make it more aesthetic
        '''
        self.DISP.fill(BLACK)
        pygame.draw.rect(self.DISP, BLACK, (0, 0, 240, 768), 0) #Create a black rectangele from (0,0) with 240 Width and 768 Length and base radius = 0


    def grid_maker(self):
        '''
        ** Helper **
        Function to make the grid: 30 x 52 dimensions
        '''
        pygame.draw.rect(self.DISP, BLACK, (240, 0, WIDTH, HEIGHT), 0) #Give Black border
        pygame.draw.rect(self.DISP, VIOLETRED, (264, 24, gWIDTH, gHEIGHT), 0) #Actual Grid

        #Create the grid with 52 columns and 30 rows
        for col in range(52):
            pygame.draw.line(self.DISP, ALICE, (GStart_x + col * self.grid_square_length, GStart_y),
                             (GStart_x + col * self.grid_square_length, GEND_y))
        for row in range(30):
            pygame.draw.line(self.DISP, ALICE, (GStart_x, GStart_y + row * self.grid_square_length),
                             (GEnd_x, GStart_y + row * self.grid_square_length))

    def make_gButtons(self):
        '''
        ** Helper **
        Function to create the buttons in the grid window
        '''

        # Draw them with STEELBLUE outline
        self.POSITIONS.make_controller(STEELBLUE)
        self.BARRIERS.make_controller(STEELBLUE)
        self.CLEAR.make_controller(STEELBLUE)
        self.FIND_PATH.make_controller(STEELBLUE)
        self.SWITCH_ALGO.make_controller(STEELBLUE)



    # Checks for state when button is clicked and changes button colour when hovered over.
    def mod_buttons(self, position, event):
        '''
        ** Helper **
        Provides functionality  and colors to each button in the grid window
        :param position: Mouse positioning
        :param event: event that occured
        '''

        #If the mouse has been pressed
        if event.type == pygame.MOUSEBUTTONDOWN:

            #If the mouse is hovering over positions button
            if self.POSITIONS.isHovering(position):
                self.CURR_STATUS = 'draw S/E' #Update status

            #If the mouse is hovering over barrier button
            elif self.BARRIERS.isHovering(position):
                self.CURR_STATUS = 'draw walls'

            #If the mouse is hovering over the clear button
            elif self.CLEAR.isHovering(position):
                self.clear_grid() #RESET

            #If the mouse is hovering over the find path button
            elif self.FIND_PATH.isHovering(position):
                self.CURR_STATUS = 'start visualizing'

            #If the mouse is hovering over the "go back" button
            elif self.SWITCH_ALGO.isHovering(position):
                self.switch_algorithm() #Go back to the menu

        # If the mouse is just idling over and not clicking
        if event.type == pygame.MOUSEMOTION:

            #If hovering over the position button
            if self.POSITIONS.isHovering(position):
                self.POSITIONS.colour = MINT

            #If hovering over the barrier button
            elif self.BARRIERS.isHovering(position):
                self.BARRIERS.colour = MINT

            #If hovering over the clear button
            elif self.CLEAR.isHovering(position):
                self.CLEAR.colour = MINT

            #If hovering over the find path method
            elif self.FIND_PATH.isHovering(position):
                self.FIND_PATH.colour = MINT

            #If hovering over the go back button
            elif self.SWITCH_ALGO.isHovering(position):
                self.SWITCH_ALGO.colour = MINT

            #Else retain their orig. color
            else:
                self.POSITIONS.colour = ORANGE
                self.BARRIERS.colour = ORANGE
                self.CLEAR.colour = ORANGE
                self.FIND_PATH.colour = ORANGE
                self.SWITCH_ALGO.colour = ORANGE


    def highlight_button(self):
        '''
        ** Helper **
        Function to provide color once something has been chosen
        Once clicked, make them red
        '''
        if self.CURR_STATUS == 'draw S/E':
            self.POSITIONS.colour = GREEN

        elif self.CURR_STATUS == 'draw walls':
            self.BARRIERS.colour = GREEN

    def clear_grid(self):
        '''
        ** Helper **
        Function to clear the board
        '''
        self.num_positional_nodes = 0 #Gets rid of positional node's counter

        # Removes Start and End Nodes Coordinates
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # Reassign to the original borders to get rid of the placed barriers
        self.border_positions = BORDERS.copy()

        # Retain status
        self.CURR_STATUS = 'grid window'

    def switch_algorithm(self):
        '''
        ** Helper **
        Places the user back to the main menu
        '''
        self.num_positional_nodes = 0

        # Start and End Nodes Coordinates
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None


        self.border_positions = BORDERS.copy()

        # Switch Status
        self.CURR_STATUS = 'main menu'




    def run_menu(self):
        '''
        ** Main **
        Puts functionality to the main menu page
        '''

        pygame.display.update() #Update screen
        self.design_menu() #Creates the menu's design

        #Consider all events that occur in the menu page 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ACTIVE = False #Deactivate the menu 

            #Store the position of the mouse into a variable

            position = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button

            #If the mouse has been clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                #If the mouse was hovering over the position of the bfs button
                if self.BFS.isHovering(position):
                    self.chosen_algo = 'bfs'
                    self.CURR_STATUS = 'grid window' #Head to the next window

                #If the mouse was hovering over the position of the dfs
                if self.DFS.isHovering(position):
                    self.chosen_algo = 'dfs'
                    self.CURR_STATUS = 'grid window' #Head to grid window

                #If the mouse was hovering over the position of aStar button
                if self.ASTAR.isHovering(position):
                    self.chosen_algo = 'astar'
                    self.CURR_STATUS = 'grid window' #Head to grid window

                #If the mouse was hovering over the position of dijkstra button
                if self.DIJKSTRA.isHovering(position):
                    self.chosen_algo = 'dijkstra'
                    self.CURR_STATUS = 'grid window' #Head to grid window

            # If the mouse is simply in motion
            if event.type == pygame.MOUSEMOTION:

                #Change the color of the button to aquamarine to have a more dynamic feel

                if self.BFS.isHovering(position):
                    self.BFS.colour = AQUAMARINE

                elif self.DFS.isHovering(position):
                    self.DFS.colour = AQUAMARINE

                elif self.ASTAR.isHovering(position):
                    self.ASTAR.colour = AQUAMARINE

                elif self.DIJKSTRA.isHovering(position):
                    self.DIJKSTRA.colour = AQUAMARINE

                #If none of the buttons are being hovered make them orange
                else:
                    self.BFS.colour = ORANGE
                    self.DFS.colour = ORANGE
                    self.ASTAR.colour = ORANGE
                    self.DIJKSTRA.colour = ORANGE



    def run_gridWindow(self):
        '''
        ** Main **
        Provides functionality to the grid window
        :return:
        '''
        self.design_hotbar() #Designs the hotbar
        self.grid_maker() #Create the grid
        self.make_gButtons() #Create grid buttons
        pygame.display.update() #Update the display

        #Consider all events that occured
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ACTIVE = False
            position = pygame.mouse.get_pos()

            #Modify buttons inside the grid window
            self.mod_buttons(position, event)

    def node_maker(self):
        '''
        Function that sketches the node inside of the created grid
        '''
        self.highlight_button() #Highlighting feature to let user know which button has been pressed

        self.make_gButtons() #Create the grid buttons again to reassign the colors once no longer being pressed

        pygame.display.update() #Update the display

        position = pygame.mouse.get_pos()

        #Consider all the events that happen in the grid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ACTIVE = False #Quits the application

            # Have to redeclare to allow user to click a different button
            # I.E once user clicks on the start/end, then they should be still allowed to place a barrier
            self.mod_buttons(position, event)

            # Establish valid boundaries for the mouse's positioning
            # 264 and 24 is where the grid starts -> lower bound for clickable position
            # 1512 and 744 is where the grid ends -> upper bound for clickable position
            if position[0] > 264 and position[0] < 1512 and position[1] > 24 and position[1] < 744:

                #Compute position of the mouse relative to the grid and not the entire GUI
                #The integer division floors the value to provide a consistent placing
                #Meaning it doesn't matter where in the box we click

                x_grid_pos = (position[0] - 264) // 24
                y_grid_pos = (position[1] - 24) // 24


                #If mouse has been clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_dragging = 1 #Let the application know

                    #If the user pressed the start/end button and there are less than two positional nodes -> No drag feature for positional nodes
                    if self.CURR_STATUS == 'draw S/E' and self.num_positional_nodes < 2:

                        #If no nodes have created and the coordinate next to it is not a recognized border
                        #The drawing of the nodes spans two coordinates (start) -> (end) hence we must check if the end position is acceptable
                        if self.num_positional_nodes == 0 and (x_grid_pos + 1, y_grid_pos + 1) not in self.border_positions:
                            node_colour = YELLOW
                            self.start_x = x_grid_pos + 1
                            self.start_y = y_grid_pos + 1
                            self.num_positional_nodes += 1

                        #If there is a starting node but no ending node
                        #Ensure that starting node and ending node are not placed in the same position
                        elif self.num_positional_nodes == 1 and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_x, self.start_y) and (x_grid_pos + 1, y_grid_pos + 1) not in self.border_positions:
                            node_colour = ROYALBLUE
                            self.end_x = x_grid_pos + 1
                            self.end_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.num_positional_nodes += 1

                        #If there is already two positional nodes, disallow the user from doing something
                        else:
                            continue

                        # Draws the node
                        # Here you can see why we need the relative positioning of the node.
                        # It allows me to pinpoint the exact location of the node in the grid
                        pygame.draw.rect(self.DISP, node_colour, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                # Update status if the mouse is no longer being dragged
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_dragging = 0

                # Checks if mouse button is being held down; drag feature
                if self.is_dragging == 1:

                    # If the user wants to draw some borders
                    if self.CURR_STATUS == 'draw walls':

                        #Check if the position is valid
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.border_positions \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_x, self.start_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_x, self.end_y):

                            #Draw the border
                            pygame.draw.rect(self.DISP, GREY, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                            self.border_positions.append((x_grid_pos + 1, y_grid_pos + 1)) #Append the clicked position in the list of borders

                #Redraw grid lines since they get overshadowed by the nodes new colours!
                for x in range(52):
                    pygame.draw.line(self.DISP, ALICE, (GStart_x + x * self.grid_square_length, GStart_y),
                                     (GStart_x + x * self.grid_square_length, GEND_y))
                for y in range(30):
                    pygame.draw.line(self.DISP, ALICE, (GStart_x, GStart_y + y * self.grid_square_length),
                                     (GEnd_x, GStart_y + y * self.grid_square_length))

#################################### VISUALIZATION FUNCTIONS #########################################

    def algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ACTIVE = False

        ### BFS ###
        start = time.time() #Time object

        if self.chosen_algo == 'bfs':
            self.bfs = BFS(self, self.start_x, self.start_y, self.end_x, self.end_y, self.border_positions) #Make BFS object


            if self.start_x and self.end_x is not None: #Make sure there is a starting/ending node
                self.bfs.BreadthFirst_Search() #Execute the algorithm and store the path in self.bfs.path

            #Workflow:
            #Convert traversed coordinates into directions -> Record directions and store them back as coordinates -> Make path from it
            # If the algortihm was able to find a viable path

            if self.bfs.path_exists:

                #Create a path object and consider and pave a new path based on the self.bfs.path
                self.pave = PathCreator(self.DISP, self.start_x, self.start_y, self.bfs.path, [])
                self.pave.record_coordinates() #Record the coordinates and store them in []
                self.pave.make_path() #Make the path from the recorded coordinates

            else: #If the algorithm cannot find the path
                self.write_something('PATH CANNOT BE FOUND!', self.DISP, [768, 384], 50, RED, FONT_name, centered = True)

        ### DFS ###

        elif self.chosen_algo == 'dfs':
            self.dfs = DepthFirst(self, self.start_x, self.start_y, self.end_x, self.end_y, self.border_positions) #Create a DFS object

            if self.start_x and self.end_x is not None:
                self.dfs.DepthFirst_Search() #Execute Algorithm

            # Make Object for new path
            if self.dfs.route_found: #If we found a path
                self.pave = PathCreator(self.DISP, self.start_x, self.start_y, self.dfs.route, [])
                self.pave.record_coordinates() #Record the coordinates and store them
                self.pave.make_path() #From the recorded coordinates, pave a path

            else:
                self.write_something('PATH CANNOT BE FOUND!', self.DISP, [768, 384], 50, RED, FONT_name, centered = True)

        ### A-STAR ###

        elif self.chosen_algo == 'astar':
            self.astar = AStar(self, self.start_x, self.start_y, self.end_x, self.end_y, self.border_positions) #Make an AStar Object

            if self.start_x and self.end_x is not None:
                self.astar.AStar_Search() #Execute A star algorithm

            if self.astar.route_found:
                self.pave = PathCreator(self.DISP, self.start_x, self.start_y, None, self.astar.route) # Create path object
                self.pave.make_path() #No need to record coordinates since the path is being paved as the search occurs

            else:
                self.write_something('PATH CANNOT BE FOUND', self.DISP, [768, 384], 50, RED, FONT_name, centered=True)

        ### DIJKSTRA ###

        elif self.chosen_algo == 'dijkstra':
            self.dijkstra = Dijkstra(self, self.start_x, self.start_y, self.end_x, self.end_y, self.border_positions)

            if self.start_x and self.end_x is not None:
                self.dijkstra.Dijkstra_Search()

            if self.dijkstra.route_found:
                self.pave = PathCreator(self.DISP, self.start_x, self.start_y, None, self.dijkstra.route)
                self.pave.make_path()

            else:
                self.write_something('PATH CANNOT BE FOUND!', self.DISP, [768, 384], 50, RED, FONT_name, centered=True)

        end = time.time() #Record end time
        self.write_something('Time Taken: ' + str(round(end - start, 3)) + ' seconds', self.DISP, [5, 5], 15, WHITE, FONT_name, False) # Display time taken to execute algorithm

        pygame.display.update() #Update display
        self.CURR_STATUS = 'aftermath' #Update status to aftermath


    def reuse_gui(self):
        '''
        Function to allow the user to re-use the application multiple times
        Otherwise, the user gets stuck in the grid again 
        '''
        self.make_gButtons() #Draw grid buttons 
        pygame.display.update() #Update display 

        #Acquire mouse positioning 
        position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.ACTIVE = False

            #If mouse is moving and is hovering over certain buttons, recolor them for a dynamic feel
            if event.type == pygame.MOUSEMOTION:
                if self.POSITIONS.isHovering(position):
                    self.POSITIONS.colour = MINT
                elif self.BARRIERS.isHovering(position):
                    self.BARRIERS.colour = MINT
                elif self.CLEAR.isHovering(position):
                    self.CLEAR.colour = MINT
                elif self.FIND_PATH.isHovering(position):
                    self.FIND_PATH.colour = MINT
                elif self.SWITCH_ALGO.isHovering(position):
                    self.SWITCH_ALGO.colour = MINT
                else:
                    self.POSITIONS.colour, self.BARRIERS.colour, self.CLEAR.colour, self.FIND_PATH.colour, self.SWITCH_ALGO.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

            #If user clicks these two buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.CLEAR.isHovering(position):
                    self.clear_grid()
                elif self.SWITCH_ALGO.isHovering(position):
                    self.switch_algorithm()



if __name__ == '__main__':
    session = PathVisualizer()
    session.run()
























