import pygame
from enemyType import EnemyType
import config

spriteFolder = "sprites"
enemyFolder = "enemy"
#Enemy class
class Enemy(pygame.sprite.Sprite):
    
    def __init__ (self,x,y,width,height,end, health, mode):
        self.x = x#x coordinate the player will be at
        self.y=y#y coordinate the player will be at
        self.width = width #width of sprite
        self.height = height#height of sprite
        self.end = end#end of sprite walking path
        self.path = [self.x,self.end]#boundaries of where the enemy can walk
        self.mode=mode#mode = easy or medium
        self.health = health#health of the enemy
        #sprites to load in
        self.rEasy = config.enemy_sprites["rEasy"]
        self.lEasy = config.enemy_sprites["lEasy"]
        self.rMedium = config.enemy_sprites["rMedium"]
        self.lMedium = config.enemy_sprites["lMedium"]
        #if the enemy is an easy enemy
        if mode==EnemyType.EASY:
            #image will be of the original weasel
            self.image = self.rEasy
            #the speed at which the enemy moves is faster than the police weasel
            self.vel = 3
        else:
            #image will be of the police weasel
            self.image = self.rMedium
            #speed is slower than the ordinary weasel
            self.vel = 2
        self.image.set_colorkey([255,255,255])
        self.image = pygame.transform.scale(self.image, (self.width,self.height))#scale the image to the preferred width and height
        self.rect = self.image.get_rect()

    #method that draws the enemy on screen
    def draw(self, screen):
        self.move()
        if self.vel>0:
            #if the velocity is greater than 0 it means that the player is moving to the right
            #if the type of weasel is easy it will display the ordinary weasel facing the right
            if self.mode==EnemyType.EASY:
                self.image = self.rEasy               
            else:
                self.image = self.rMedium
        else:
            #if the weasel is moving to the left display the appropriate sprites
            if self.mode==EnemyType.EASY:
                self.image = self.lEasy                
            else:
                self.image = self.lMedium
        self.image.set_colorkey([255,255,255])
        self.image = pygame.transform.scale(self.image, (self.width,self.height))#scale the image to the preferred width and height
        screen.blit(self.image, (self.x, self.y))#draw enemy at coordinate (x,y)

    #method that hurts the enemy
    def hit(self):
        self.health-=1#health minus 1

    #method that moves the enemy
    def move(self):
        if self.vel>0:
            #if the enemy is moving right
            if self.x+ self.vel<self.path[1]:
                #if the enemy hasn't reached the end of their path then keep on moving right
                self.x += self.vel
            else:
                #changes direction
                #will minus pixels from x coord making it move left
                self.vel = self.vel * -1
        else:
            #if the enemy is moving left
            if self.x-self.vel>self.path[0]:
                #if the enemy hasn't walked back to the start of their path then keep moving left
                self.x += self.vel
            else:
                #changes direction
                self.vel = self.vel * -1
