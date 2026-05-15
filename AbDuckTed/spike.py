import os
import pygame
spriteFolder = "sprites"
enemyFolder = "enemy"

#class that creates a Spike object
class Spike(object):
    def __init__ (self, x, y):
        self.x = x#x coord
        self.y = y + 26 # add 26 so that it appearts on the floor
        self.image = pygame.image.load(os.path.join(spriteFolder, enemyFolder, "spikes.png")).convert_alpha()#load in sprite
        self.rect = pygame.Rect(self.x, self.y, 30, 4)#spikes rectangle

    #draw the spike to the screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))#draw the spike at the (x,y) coord

