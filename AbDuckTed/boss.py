import pygame
import os
from bossType import BossType
import config

class Boss(pygame.sprite.Sprite):
    def __init__ (self, x, y, width, height, end, health, mode):
        self.x = x#x coordinate
        self.y=y#y coordinate
        self.width = width #width of sprite
        self.height = height#height of sprute
        self.end = end#end of sprite walking path
        self.path = [self.x,self.end]#boundaries of where the enemy can walk
        self.mode=mode#mode = miniboss or Boss
        self.health = health#health of enemy
        
        self.isJump=False#whether the enemy is jumping or not

        self.shootLoop = 1#allows for a break in the bosses shots
        #load in sprites
        self.lMedium = config.enemy_sprites["lMedium"]
        self.rMedium = config.enemy_sprites["rMedium"]
        self.lBoss = config.enemy_sprites["lBoss"]
        self.rBoss = config.enemy_sprites["rBoss"]
        self.lBossFinal = config.enemy_sprites["lBossFinal"]
        self.rBossFinal = config.enemy_sprites["rBossFinal"]
        #if the type of boss is a miniboss or a boss
        if mode == BossType.MINIBOSS:
            self.vel = 2#velocity represents the amount in pixels that the enemy will move
            self.image = self.lMedium#will look like a police weasel but it will be larger than them
            self.jumpCount=8#if the player jumps jumpCount will decrease to make the arc of the jump
        elif mode == BossType.BOSS:
            self.jumpCount=9#if the player jumps jumpCount will decrease to make the arc of the jump
            self.image = self.lBoss
            self.vel = 2#1st level boss will be slower than the final boss
        elif mode == BossType.FINAL_BOSS:
            self.jumpCount=9#if the player jumps jumpCount will decrease to make the arc of the jump
            self.image = self.lBossFinal
            self.vel = 3
                
        self.image.set_colorkey([255,255,255])
        self.image = pygame.transform.scale(self.image, (self.width,self.height))#set the image to the certain width and height
        
    def draw(self, screen, player_x):
        self.move()
        if self.mode==BossType.MINIBOSS:#mini boss should always face to the left
            self.image = self.lMedium
        else:
            if player_x > self.x:#if the player is to the right of the boss
                if self.mode == BossType.BOSS:
                    self.image = self.rBoss#show the boss sprite looking to the right
                else:
                    self.image = self.rBossFinal
            else:#if the player is to the left of the boss
                if self.mode == BossType.BOSS:
                    self.image = self.lBoss
                else:
                    self.image = self.lBossFinal
                   
            
        self.image.set_colorkey([255,255,255])
        self.image = pygame.transform.scale(self.image, (self.width,self.height))#scale the image to the height and width
        screen.blit(self.image, (self.x, self.y))#draw to the screen

    #method that hurts the enemy
    def hit(self):
        self.health-=1    

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
