from stageType import StageType
import config
import pygame

#class to create interactive blocks
class Interactive(object):
    def __init__(self, x, y):
        self.x=x#x coord
        self.y=y#y coord
        self.locked = False#if the interactive is locked 
        self.image = config.key_sprites["lock"]
        self.rect = pygame.Rect(x, y, 30, 30)#make the rectangle that the sprite is
    #method that is executed when the player interacts with the interactive

    def interact(self, interactive, player, stage):
        global txt#access the global variable txt
        
        if stage.get_level_number() == 0 and stage.get_stage_number() == StageType.LEVEL_1 and player.blueKey:#if the player has a blue key and it is the 1st stage in level 1
            del interactive[:]#delete the interactive in the room
            txt=True#display relevant text
            player.healthChange(8)#add 8hp to the player
            player.blueKey=False#the player no longer has the blue key
            
        elif stage.get_level_number() == 6 and stage.get_stage_number() == StageType.TUTORIAL and player.blueKey:#if the player has a blue key and it is the 4th stage in the tutorial
            del interactive[:]#delete the interactive in the room
            txt=True#display relevant text
            player.healthChange(2)#add 2 hp to the player
            player.blueKey=False#the player no longer has the blue key
            
        elif stage.get_level_number() == 7 and stage.get_stage_number() == StageType.TUTORIAL:#if the player is in the 8th stage in the tutorial
            del interactive[:]#delete the interactive in the room
            player.addKey("blueKey")#add the blue key to the player
            txt=True
            
        elif stage.get_level_number() == 4 and stage.get_stage_number() == StageType.LEVEL_1 and player.bossKey:
            del interactive[:]#delete the interactive from the screen
            player.bossKey=False#player no longer has the boss key on them
            
        elif stage.get_level_number() == 3 and stage.get_stage_number() == StageType.LEVEL_1:
            del interactive[:]#delete the interactive in the room
            player.addKey("blueKey")#add the blue key to the player
            txt=True#display relevant text
            
        else:
            self.locked=True#if the player didn't fulfill any of the requirements above, interactive is locked
            
    #method that draws the interactive to the screen
    def draw(self,screen):
        screen.blit(self.image, (self.x,self.y))#draw image at (x,y) coords
        