from configurations import *

class BFS():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, borders):
        '''
        Constructor to make BFS object
        :param app: Gui object
        :param start_node_x: starting node x
        :param start_node_y: starting node y
        :param end_node_x: ending node x
        :param end_node_y: ending node y
        :param borders: list of recognized borders
        '''
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.borders = borders
        self.visited = [(self.start_node_x, self.start_node_y)]
        self.path = None #String representing each movement
        self.path_exists = False

    def draw_path(self, i, j):
        '''
        Helper that draws the path while executing BFS
        :param i: The x-coordinate of the currently traversed coordinates
        :param j: The y-coordinate of the currently traversed coordinates
        :return:
        '''
        # Draw each node the app is visiting as it is searching SIMULTNEOUSLY
        pygame.draw.rect(self.app.DISP, TAN, (i * 24 + 240, j * 24, 24, 24), 0)

        ##### Redraw start/end nodes on top of all routes as they get overriden
        pygame.draw.rect(self.app.DISP, YELLOW, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.DISP, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        # Redraw grid (for aesthetic purposes lol)
        for col in range(52):
            pygame.draw.line(self.app.DISP, ALICE, (GStart_x + col * 24, GStart_y), (GStart_x + col * 24, GEND_y))
        for row in range(30):
            pygame.draw.line(self.app.DISP, ALICE, (GStart_x, GStart_y + row * 24), (GEnd_x, GStart_y + row * 24))

        pygame.display.update()

    def is_Valid_Step(self, step):
        '''
        Helper that determines if the step reached a border or a visited node
        :param move:
        :return: a boolean deciding the validity of
        '''
        if step not in self.borders and step not in self.visited:
            self.visited.append(step)
            return True
        return False

    def reached_dest(self, curr_location):
        '''
        Helper to determine if the end node has been reached
        :param curr_location: the current location
        :return: a boolean deciding if end has been reached
        '''
        if curr_location == (self.end_node_x, self.end_node_y):
            return True
        return False

    def BreadthFirst_Search(self):
        '''
        The algorithm itself
        :return:
        '''

        #Helper Variables + Data Structure
        queue = [(self.start_node_x, self.start_node_y)] #Keeps track of current node we're in -> Will always contain 4 entries max.
        moves_queue = [''] #Keeps track of all the movements made ,for example: "L R L U", Order here doesn't matter because of the spread
        first_out = ''
        first_moves = ''

        #While queue is not empty
        while len(queue) > 0:
            # Parent variables of parent nodes at the given time
            first_out = queue.pop(0) #Removes the very first entry in the queue
            first_moves = moves_queue.pop(0) #Remove the current movements and store into this variable

            #Track movements -> Allows for a "spread out pattern"
            for step in ['L', 'R', 'U', 'D']: #Each node only has 4 possible directions to go to!

                #Create a new move from each direction starting from left per iteration

                i, j = first_out #Consider the first entry of the queue
                if step == 'L':
                    i -= 1
                elif step == 'R':
                    i += 1
                elif step == 'U':
                    j -= 1
                elif step == 'D':
                    j += 1

                #Keeps track of all movements as a one concatenated string
                #Add the first first move as the step as one string
                latest_moves = first_moves + step

                #Check if the step was valid
                if self.is_Valid_Step((i, j)):
                    self.draw_path(i, j) #Draw the path
                    queue.append((i, j)) #Add into queue
                    moves_queue.append(latest_moves) #Add into helper as the last entry

                #If we reached the destination
                if self.reached_dest((i, j)):
                    self.path = latest_moves #Convert the coordinates into strings -> The results will be stored here
                    self.path_exists = True
                    break

            if self.path_exists:
                break

