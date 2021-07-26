from configurations import *

class Controller():
    '''
    Constructor to make a controller
    '''
    def __init__(self, gui, colour, x, y, width, height, text=''):
        self.gui = gui
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def make_controller(self, outline = None):
        '''
        Function that makes a controller with a certain color of outline along with its true color
        Also creates the text and places it in the middle of the button
        '''
        if outline:
            pygame.draw.rect(self.gui.DISP, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0) #Create outline
            pygame.draw.rect(self.gui.DISP, self.colour, (self.x, self.y, self.width, self.height), 0) #Create actual box

        #If text is not empty
        if self.text != '':
            font = pygame.font.SysFont(FONT_name, 28)
            text = font.render(self.text, 1, BLACK)
            #Places the text in the middle with this formula
            self.gui.DISP.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isHovering(self, position):
        '''
        Function that identifies if the position is considered to be a part of the controller
        :param position: position of the mouse
        :return: A boolean deciding if the position is valid
        '''
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if position[0] > self.x and position[0] < self.x + self.width:
            if position[1] > self.y and position[1] < self.y + self.height:
                return True
        return False