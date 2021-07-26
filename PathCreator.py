from configurations import *

class PathCreator():
    def __init__(self, surface, start_x, start_y, path, coordinates):
        '''

        :param surface: Surface to draw the path
        :param start_x: starting x
        :param start_y: starting y
        :param path: String containing directions
        :param coordinates:
        '''
        self.surface = surface
        self.start_x = start_x
        self.start_node_y = start_y
        self.path = path
        self.coordinates = coordinates

    # Only to be used by DFS and BFS
    def record_coordinates(self):
        x = self.start_x
        y = self.start_node_y

        #Iterate through each direction stored in self.path
        for step in self.path:
            if step == 'L':
                x -= 1
            elif step == 'R':
                x += 1
            elif step == 'U':
                y -= 1
            elif step == 'D':
                y += 1
            self.coordinates.append((x, y)) #Append each traversed coordinates into the list

    def make_path(self):
        self.coordinates.pop() #We don't include the ending node as a path
        for (x_pos, y_pos) in self.coordinates:
            #y_pos * 24 because the path begins in the same level as the starting node always and we don't want to cover the ending node
            pygame.draw.rect(self.surface, SPRINGGREEN, (x_pos*24 + 240, y_pos*24, 24, 24), 0)
