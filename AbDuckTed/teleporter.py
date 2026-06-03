from teleporterType import TeleporterType
import config


#Creates teleporters
class Teleporter(object):
    def __init__ (self,x,y,direction):
        self.x = x
        self.y = y + 10 # add 10 so that the teleporter shows on the ground
        if direction == TeleporterType.UP:# if it is a teleporter going up
            self.image = config.teleporter_sprites["up"]
        if direction == TeleporterType.DOWN:# if it is a teleporter going down image is a different sprite
            self.image = config.teleporter_sprites["down"]

    def draw(self,screen):
        screen.blit(self.image, (self.x,self.y))#draw image at (x,y) to the screen
        