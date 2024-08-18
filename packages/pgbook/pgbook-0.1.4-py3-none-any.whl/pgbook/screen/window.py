import pygame
import sys
from ..eventlist.thinglist import ThingList

class Window:
    def __init__(self):
        pygame.init()
        infoObject = pygame.display.Info()
        self.max_width = infoObject.current_w
        self.max_height = infoObject.current_h
        #self.max_width, self.max_height = pygame.display.get_surface().get_size()
        
        self.width = self.max_width*0.6
        self.height = self.max_height*0.6
        self.MaxFps = 60
        
        self.check = ThingList()
        self.event = ThingList()
        
        @self.event.connect(name='QuitCheckThing')
        def Quit(event):
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    def show(self):
        screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        while True:
            self.clock.tick(self.MaxFps)
            for event in pygame.event.get():
                self.event.did(event)
            self.check.did()