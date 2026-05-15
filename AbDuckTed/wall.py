import pygame

#a class for walls / blocks to jump onto
class Wall(object):
    def __init__(self, wx, wy):
        self.rect = pygame.Rect(wx, wy, 30, 30)#Create the rectangle for what it looks like
