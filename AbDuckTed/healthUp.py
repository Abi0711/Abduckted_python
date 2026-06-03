import pygame
import config

#class that creates 1ups
class HealthUp(object):
    def __init__ (self,x,y):
        self.x = x#x coord
        self.y = y#y coord
        self.image = config.collectible_sprites["bread"]
        self.rect = pygame.Rect(x, y, 30, 30)#create the hitbox rectangle

    def draw(self, screen):
        screen.blit(self.image, (self.x,self.y))#draw image to (x,y) onto the screen
