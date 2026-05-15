import pygame

#Creating bullets
class Projectile(object):
    def __init__ (self, x, y, radius, color, facing):
        self.x = x#x coord
        self.y=y#y coord
        self.radius = radius # how big the bullet is
        self.color = color#colour of the bullet
        
        self.facing = facing#what way the person shooting is facing
        #facing = -1 or 1
        
        self.vel = 7*facing#velocity is by how much the bullet moves
        #if negative then it moves to the left
        #if positive it moves to the right

    def draw(self, screen, level):
        if self.x<630 and self.x>30:
            self.x += self.vel#if the bullet is within the boundaries of the screen keep it moving                        
        else:#if the bullet is outside of the screen
            if self in level.bullets:#if the bullet belongs to the player
                #delete the bullet from the screen
                level.bullets.pop(level.bullets.index(self))
            if self in level.eBullets:
                #delete the bullet from the screen
                level.eBullets.pop(level.eBullets.index(self))

        #collision with walls
        for w in level.walls:
            if self.y-self.radius<w.rect.y+30 and self.y+self.radius>w.rect.y:
                if self.x+self.radius>w.rect.x and self.x-self.radius<w.rect.x+30:
                    #if the bullet collides with a wall delete it
                    if self in level.bullets:#if the bullet belongs to the player
                        #delete the bullet from the screen
                        level.bullets.pop(level.bullets.index(self))
                    if self in level.eBullets:
                        #delete the bullet from the screen
                        level.eBullets.pop(level.eBullets.index(self))
        
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)#draw the circle to the screen
