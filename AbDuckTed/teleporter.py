import os
import pygame
from teleporterType import TeleporterType

spriteFolder = "sprites"
teleporterFolder = "teleporter"
#Creates teleporters
class Teleporter(object):
    def __init__ (self,x,y,direction):
        self.x = x
        self.y = y + 10 # add 10 so that the teleporter shows on the ground
        if direction == TeleporterType.UP:# if it is a teleporter going up
            self.image = pygame.image.load(os.path.join(spriteFolder, teleporterFolder, "up.png")).convert_alpha()
        if direction == TeleporterType.DOWN:# if it is a teleporter going down image is a different sprite
            self.image = pygame.image.load(os.path.join(spriteFolder, teleporterFolder, "down.png")).convert_alpha()

    def draw(self,screen):
        screen.blit(self.image, (self.x,self.y))#draw image at (x,y) to the screen
        