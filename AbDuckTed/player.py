import pygame
import config

#main player class
class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #initialise different sprites to be used for animation
        self.hit = config.sounds["hit"]
        self.heal = config.sounds["heal"]
        self.rDuck = config.duck_sprites["rDuck"]
        self.lDuck = config.duck_sprites["lDuck"]
        self.rShoot = config.duck_sprites["rShoot"]
        self.lShoot = config.duck_sprites["lShoot"]
        self.rSpaceShoot = config.duck_sprites["rSpaceShoot"]
        self.lSpaceShoot = config.duck_sprites["lSpaceShoot"]
        self.rSpace = config.duck_sprites["rSpace"]
        self.lSpace = config.duck_sprites["lSpace"]
                
        self.image = self.rDuck
        self.image.set_colorkey([255,255,255])
        self.image = pygame.transform.scale(self.image, (44,44))
        self.rect = self.image.get_rect()
    
        self.shoot = False #boolean that represents whether the player is currently shooting
        self.space = False #boolean that represents whether the player is in space/the 2nd level
        self.left = False #boolean that represents whether the player is currently facing left
        self.isJump = False #boolean that represents whether the player is jumping

        #keys that the player can obtain
        self.bossKey = False
        self.keyFrag1 = False
        self.keyFrag2 = False
        self.blueKey =False
        
        self.hitLoop = 0 # loop that allows the player to have a grace period between hits
        self.health = 10#player's health
        self.jumpCount = 8 # if the player jumps jumpCount will decrease to make the arc of the jump

    #method that sets the position of the player at position (x,y)
    def setPos(self, x, y):
        self.rect = pygame.Rect(x, y, 44, 44)
        
    #method that changes the players health by adding change
    def healthChange(self, change):
        if change<0 and self.hitLoop==0:
            self.hit.play()
            self.hitLoop=1
            self.health += change
        if change>0:
            self.health += change
        
    #method that adds a key to the player
    def addKey(self, key):
        if key=="frag1":
            self.keyFrag1=True#1st key fragment has been obtained
            if self.keyFrag2 and self.keyFrag1:#if both key fragments have been obtained create the boss Key
                    self.bossKey = True
                    self.keyFrag1=False
                    self.keyFrag2=False
        elif key == "frag2":#2nd key fragment has been obtained
            self.keyFrag2=True
            if self.keyFrag2 and self.keyFrag1:#if both key fragments have been obtained create the boss Key
                self.bossKey = True
                self.keyFrag1=False
                self.keyFrag2=False
        else:
            self.blueKey=True#blue key has been obtained
            
    #method that changes the different sprites of the player
    def change(self):
        #if the player is in space show the sprite that has the helmet on
        if self.space:
            #if it is level 2 the duck will have a space suit on
            if self.left:
                #if the player is going left
                if self.shoot:
                    #if the player has shot
                    self.image = self.lSpaceShoot
                else:
                    self.image = self.lSpace
            else:
                #if the player is going right
                if self.shoot:
                    self.image = self.rSpaceShoot 
                else:
                    self.image = self.rSpace
        else:
            #if it is the tutorial or level 1 the player won't have the space suit on
            if self.left:
                if self.shoot:
                    self.image = self.lShoot
                else:
                    self.image = self.lDuck
            else:
                if self.shoot:
                    self.image = self.rShoot

                else:
                    self.image = self.rDuck
        self.image.set_colorkey([255,255,255])
        self.image = pygame.transform.scale(self.image, (44,44))#sets the image to 44x44 pixels
    #method that moves the player 
    def move(self,dx,dy, currentStage):
        if dx!=0:
            self.move_single_axis(dx,0, currentStage)
        if dy!=0:
            self.move_single_axis(0,dy, currentStage)

    #method that moves the player in a direction with a collision detection for walls, spikes and the interactives
    def move_single_axis(self, dx, dy, level):
        self.rect.x +=dx
        self.rect.y +=dy
        #collsion with walls
        for wall in level.walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:#Moving right, collide with left side of wall
                    self.rect.right = wall.rect.left
                if dx < 0:#moving left, collide with right side of wall
                    self.rect.left = wall.rect.right
                if dy > 0:#Moving down, collide with top of wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:#moving up, collide with the bottom of the wall
                    self.rect.top = wall.rect.bottom

        #collsion with spikes
        for s in level.spikes:
            if self.rect.colliderect(s.rect):
                if dx > 0:#Moving right, collide with left side of spike
                    self.rect.right = s.rect.left
                if dx < 0:#moving left, collide with right side of spike
                    self.rect.left = s.rect.right
                if dy > 0:#Moving down, collide with top of spike
                    self.rect.bottom = s.rect.top
                if dy < 0:#moving up, collide with the bottom of the spike
                    self.rect.top = s.rect.bottom
                self.healthChange(-1)
        #same code as walls except with the health rect instead
        for h in level.ups:
            if self.rect.colliderect(h.rect):
                self.heal.play()
                self.healthChange(1)
                level.ups.remove(h)    
        pygame.event.pump()
        user_input = pygame.key.get_pressed()#get the key pressed by the user
        #same code as walls except with the interactives rect instead
        for f in level.interactive:
            #allows player to be 10 pixels away from the interactive and still be able to interact with it
            
            if self.rect.y<f.y+30 and self.rect.y+44>f.y:
                if self.rect.x+44>f.x-10 and self.rect.x<f.x+40:
                    if user_input[pygame.K_e]:#if the user pressed e
                        f.interact(level.interactive)#interact with object
                
            if self.rect.colliderect(f.rect):
                if dx > 0:#Moving right, collide with left side of spike
                    self.rect.right = f.rect.left
                if dx < 0:#moving left, collide with right side of spike
                    self.rect.left = f.rect.right
                if dy > 0:#Moving down, collide with top of spike
                    self.rect.bottom = f.rect.top
                if dy < 0:#moving up, collide with the bottom of the spike
                    self.rect.top = f.rect.bottom
                if user_input[pygame.K_e]:#if the user pressed e
                    f.interact(level.interactive)#interact with object

