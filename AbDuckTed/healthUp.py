import pygame
spriteFolder = "sprites"
collectiblesFolder = "collectibles"
healthUpFolder = "healthUp"
keyAndLockFolder = "keyAndLock"
enemyFolder = "enemy"
playerFolder = "ted"
teleporterFolder = "teleporter"
#class that creates 1ups
class HealthUp(object):
    def __init__ (self,x,y):
        self.x = x#x coord
        self.y = y#y coord
        self.image = pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, healthUpFolder, "bread.png")).convert_alpha()

        self.rect = pygame.Rect(x, y, 30, 30)#create the hitbox rectangle
    def draw(self, screen):
        screen.blit(self.image, (self.x,self.y))#draw image to (x,y) onto the screen
