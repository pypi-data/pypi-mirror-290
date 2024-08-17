import pygame
import sys


class Window:
    def __init__(self):
        self.max_width, self.max_height = pygame.display.get_surface().get_size()
        
        self.width = self.max_width*0.6
        self.height = self.max_height*0.6
        
    def show(self):
        screen = pygame.display.set_mode((self.width,self.height))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()