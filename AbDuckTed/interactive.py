# import os
# import pygame

# spriteFolder = "sprites"
# collectiblesFolder = "collectibles"
# healthUpFolder = "healthUp"
# keyAndLockFolder = "keyAndLock"
# enemyFolder = "enemy"
# playerFolder = "ted"
# teleporterFolder = "teleporter"

# #class to create interactive blocks
# class Interactive(object):
#     def __init__(self, x, y):
#         self.x=x#x coord
#         self.y=y#y coord
#         self.locked = False#if the interactive is locked 
#         self.image = pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, keyAndLockFolder, "lock.png")).convert_alpha()#load in sprite
#         self.rect = pygame.Rect(x, y, 30, 30)#make the rectangle that the sprite is
#     #method that is executed when the player interacts with the interactive
#     def interact(self, interactive):
#         global txt#access the global variable txt
        
#         if stage[1]==0 and stage [0] ==1 and player.blueKey:#if the player has a blue key and it is the 1st stage in level 1
#             del interactive[:]#delete the interactive in the room
#             txt=True#display relevant text
#             player.healthChange(8)#add 8hp to the player
#             player.blueKey=False#the player no longer has the blue key
            
#         elif stage[1]==6 and stage[0]==0 and player.blueKey:#if the player has a blue key and it is the 4th stage in the tutorial
#             del interactive[:]#delete the interactive in the room
#             txt=True#display relevant text
#             player.healthChange(2)#add 2 hp to the player
#             player.blueKey=False#the player no longer has the blue key
            
#         elif stage[1]==7 and stage[0]==0:#if the player is in the 8th stage in the tutorial
#             del interactive[:]#delete the interactive in the room
#             player.addKey("blueKey")#add the blue key to the player
#             txt=True
            
#         elif stage[1]==4 and stage[0]==1 and player.bossKey:
#             del interactive[:]#delete the interactive from the screen
#             player.bossKey=False#player no longer has the boss key on them
            
#         elif stage[1]==3 and stage[0]==1:
#             del interactive[:]#delete the interactive in the room
#             player.addKey("blueKey")#add the blue key to the player
#             txt=True#display relevant text
            
#         else:
#             self.locked=True#if the player didn't fulfill any of the requirements above, interactive is locked
            
#     #method that draws the interactive to the screen
#     def draw(self,screen):
#         screen.blit(self.image, (self.x,self.y))#draw image at (x,y) coords
        
