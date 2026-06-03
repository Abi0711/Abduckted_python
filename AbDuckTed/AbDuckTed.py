import os
import random
import pygame
from player import PlayerSprite
from level import Level
from teleporterType import TeleporterType
from enemyType import EnemyType
from bossType import BossType
import config

#start pygame
os.environ["SDL_VIDEO_CENTERED"]="1"
pygame.init()


#set up display
pygame.display.set_caption("AbDuckTed!")
width = 660#width of the screen
height = 510#height of the screen
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

levels=[[]]#holds the level layout
stage = [0,0]#keeps track of the current level and stage the player is on

#boolean that allows for text to be shown on the screen according to the stage and level
global txt
txt=False

#class to create interactive blocks
class Interactive(object):
    def __init__(self, x, y):
        self.x=x#x coord
        self.y=y#y coord
        self.locked = False#if the interactive is locked 
        self.image = config.key_sprites["lock"]
        self.rect = pygame.Rect(x, y, 30, 30)#make the rectangle that the sprite is
    #method that is executed when the player interacts with the interactive
    def interact(self, interactive):
        global txt#access the global variable txt
        
        if stage[1]==0 and stage [0] ==1 and player.blueKey:#if the player has a blue key and it is the 1st stage in level 1
            del interactive[:]#delete the interactive in the room
            txt=True#display relevant text
            player.healthChange(8)#add 8hp to the player
            player.blueKey=False#the player no longer has the blue key
            
        elif stage[1]==6 and stage[0]==0 and player.blueKey:#if the player has a blue key and it is the 4th stage in the tutorial
            del interactive[:]#delete the interactive in the room
            txt=True#display relevant text
            player.healthChange(2)#add 2 hp to the player
            player.blueKey=False#the player no longer has the blue key
            
        elif stage[1]==7 and stage[0]==0:#if the player is in the 8th stage in the tutorial
            del interactive[:]#delete the interactive in the room
            player.addKey("blueKey")#add the blue key to the player
            txt=True
            
        elif stage[1]==4 and stage[0]==1 and player.bossKey:
            del interactive[:]#delete the interactive from the screen
            player.bossKey=False#player no longer has the boss key on them
            
        elif stage[1]==3 and stage[0]==1:
            del interactive[:]#delete the interactive in the room
            player.addKey("blueKey")#add the blue key to the player
            txt=True#display relevant text
            
        else:
            self.locked=True#if the player didn't fulfill any of the requirements above, interactive is locked
            
    #method that draws the interactive to the screen
    def draw(self,screen):
        screen.blit(self.image, (self.x,self.y))#draw image at (x,y) coords
        
#The two methods together create a text to be shown on screen
def text_objects(text, font, colour):
        textSurface = font.render(text, True, colour)
        return textSurface, textSurface.get_rect()

def message_display(text, top, left, size, colour):
        #set font & size
        my_text = pygame.font.SysFont("berlinsansfb", size)
        #create text objects
        text_surface, text_rect = text_objects(text, my_text, colour)
        #set where the text appears on screen
        text_rect.center = (top), (left)
        screen.blit(text_surface, text_rect)
        
#method that saves the game into a textfile
def saveGame():
    try:
        saveFile = open("save.txt", "w")
        #open the file that holds the information for saved files

        #print to the file all necessary info
        #the stages, players health, what keys the player has
        saveFile.write(str(stage[0])+"\n")
        saveFile.write(str(stage[1])+"\n")
        saveFile.write(str(player.health)+"\n")
        saveFile.write(str(player.keyFrag1)+"\n")
        saveFile.write(str(player.keyFrag2)+"\n")
        saveFile.write(str(player.bossKey)+"\n")
        saveFile.write(str(player.blueKey))
        #close the file
        print("Save successful!")
        saveFile.close()
    except IOError:
        # if there is an error
        print("Unable to save. :(")
        
        
#loads where the player was last according to what was saved in the textfile
def loadGame():
    try:
        saveFile = open("save.txt", "r")
        #open the file to read it
        
        i = 0#i keeps track of the lines in the file
        
        #will save the level at [0] and individual stage at [1]
        for line in saveFile:
            
            i+=1
            
            key=False#will determine whether the player has the key or not
            
            if line.strip() =="False":#if the line in the file equals to false
                key = False
            if line.strip()=="True":#if the line in the file equals to true
                key= True
            
            if i==3:
                #if it is the 3rd line in the file the line represents the player's health
                player.health = int(line)
                
            elif i==4:
                if key:
                    #if it is the 4th line in the file and the line is true
                    player.addKey("frag1")#add key fragment to player
                    
            elif i==5:
                if key:
                    #if it is the 5th line in the file and the line is true
                    player.addKey("frag2")#add key fragment to player
            elif i==6:
                if key:
                    #if it is the 6th line in the file and the line is true
                    player.addKey("frag1")#add key fragment to player
                    player.addKey("frag2")#add key fragment to player
                    #by adding both key fragments it will create the boss key
            elif i==7:
                if key:
                    #if it is the 7th line in the file and the line is true
                    player.addKey("blue")#add blue key
                break
                
            else:
                stage[i-1]=int(line)
                #will save the level at [0] and individual stage at [1]
        #close file
        saveFile.close()
    except IOError:
        print("No save file available.")
        #if there is no file under the name save.txt
    except ValueError:
        #if there is a file error
        print("File error.")

#method that reads the stages in an individual level
def levelProgress():
    del levels[:]
    #delete all stages in the array
    global stage
    
    level=[]#represents an individual stage
    levelPath = "levelLayouts"
    if stage[0] ==0:#if it is the tutorial
        #open file and read line for line
        for line in open(os.path.join(levelPath, 'tutorial.txt')):
            if line.strip() =="stop":#if the line equals stop, the entire stage will be added to levels
                levels.append(level)
                level = []#level will be blank, ready to copy another stage
            else:
                level.append(line)#add line to level
                
    elif stage[0] ==1:#if its the 1st level
        for line in open(os.path.join(levelPath, 'level1.txt')):
            if line.strip() =="stop":
                levels.append(level)
                level = []
            else:
                level.append(line)
                
    elif stage[0] ==2:#if its the 2nd level
        for line in open(os.path.join(levelPath, 'level2.txt')):
            if line.strip() =="stop":
                levels.append(level)
                level = []
            else:
                level.append(line)
                
    else:#if the level is a weird number set the player to the first level
        for line in open(os.path.join(levelPath, 'level1.txt')):
            if line.strip() =="stop":
                levels.append(level)
                level = []
            else:
                level.append(line)

#method interprets the stage and brings it to life
def processCurrentStage():
    x=y=0
    
    temp = levels[stage[1]]#read the current stage the player is at
    currentStage = Level()
    for row in temp:
        #for each row in the level
        for col in row: 
            #for individual letters consisting in the rows
            if col == "W":#add a wall
                currentStage.addWall(x, y)
                
            elif col == "E":#add a police weasel
                currentStage.addEnemy(x, y-10, 32, 40, x+(30*4), 5, EnemyType.MEDIUM)
                
            elif col == "e":#add an ordinary weasel
                currentStage.addEnemy(x, y-10, 32, 40, x+(30*4), 3, EnemyType.EASY)
                
            elif col == "S":#add a spike
                currentStage.addSpike(x, y)
                
            elif col == "H":#add 1-up
               currentStage.addHealthUp(x, y)
                
            elif col == "D":#add teleporter that goes down
                currentStage.addTeleporter(x, y, TeleporterType.DOWN)
                
            elif col =="U":#add teleporter that goes down
                currentStage.addTeleporter(x, y, TeleporterType.UP)
                
            elif col == "I":#add interactive object
                currentStage.addInteractive(Interactive(x, y))
                
            elif col == "b":#add miniboss
                currentStage.addBoss(x, y - 20, 64, 80, x + (30 * 4), 25, BossType.MINIBOSS)
                
            elif col == "B":#add boss
                currentStage.addBoss(x, y - 20, 64, 80, x + (30 * 11), 55, BossType.BOSS)

            elif col == "F":#add boss
                currentStage.addBoss(x, y - 20, 64, 80, x + (30 * 11), 55, BossType.FINAL_BOSS)
            
            x += 30 #add 30pixels to x so the entities are different coordinates, reads from left to right
        y += 30#add 30 pixels to work downwards from screen, reads from top to bottom
        x=0
    return currentStage
        
#Creates a button
def Button(msg, x, y, w, h, a, ia, loop,action=None):
    mouse = pygame.mouse.get_pos()
    #position of where user has clicked
    click = pygame.mouse.get_pressed()
    #whether a person has clicked or not
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(screen, a, (x, y, w, h))
        #Creates a hover event
        if click[0] ==1:
            action()
            #if the player clicks anywhere within the button, execute action
    else:
        pygame.draw.rect(screen, ia, (x, y, w, h))#if player doesn't hover over button it is inactive
    #show the text in the middle of the button
    text_surface, text_rect = text_objects(msg, config.fonts["small"], config.colours["black"])
    text_rect.center = (x+(w/2)), (y+(h/2))
    screen.blit(text_surface, text_rect)#draw text ontop of rectangle
    
#function will run when the player loses all life
#user will get the choice to restart the game or quit
def lose():
    go = True
    while go:
        for event in pygame.event.get():
            pygame.event.pump()
            user_input = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                quitGame()
            if user_input[pygame.K_ESCAPE]:
                quitGame()
                
                #if player wants to quit it will quit the game
        #display text on a config.colours["black"] screen
        screen.fill(config.colours["black"])
        message_display("YOU HAVE DIED", 320,100,20, config.colours["white"])
        message_display("TRY AGAIN?", 320,200,20, config.colours["white"])
        
        #display buttons on screen
        Button("YES",100, 450, 120, 50, config.colours["brightGreen"], config.colours["green"], go,gameLoad)
        Button("NO", 400, 450, 120, 50, config.colours["brightRed"], config.colours["red"], go, quitGame)

        #update the screen
        pygame.display.update()
    
#method that shows the title screen
def intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            pygame.event.pump()
            user_input = pygame.key.get_pressed()
            #allows the player to leave the game
            if event.type == pygame.QUIT:
                quitGame()
            if user_input[pygame.K_ESCAPE]:
                quitGame()
        #load in the background image with the main character sitting on the T
        screen.blit(config.background_images["level1"], (0,0))
        screen.blit(config.duck_sprites["rDuck"], (400,180))

        #display title
        text_surface, text_rect = text_objects("AbDuckTed", config.fonts["large"], config.colours["yellow"])        
        text_rect.center = (330), (255)
        screen.blit(text_surface, text_rect)
        
        #display button representing the different options the player can choose
        Button("Tutorial", 100, 450, 120, 50, config.colours["brightYellow"], config.colours["yellow"], intro, tutorial)
        Button("Load Game", 500, 450, 120, 50, config.colours["brightYellow"], config.colours["yellow"], intro, gameLoad)
        Button("New Game", 300, 450, 120, 50, config.colours["brightYellow"], config.colours["yellow"], intro, gameNew)

        pygame.display.update()


#loads a game from previous save
def gameLoad():
    loadGame()
    game()
        
#starts a new game and save file
def gameNew():
    #set to level one and with players health to 10 and no keys
    stage[0] = 1
    stage[1] = 0
    player.health = 10
    player.blueKey = False
    player.bossKey = False
    player.keyFrag1 = False
    player.keyFrag2 = False
    
    saveGame()
    go = True
    i=0#count how long each screen goes for
    s=0#number of slides
    #start music
    pygame.mixer.music.load(config.music["happy"])
    pygame.mixer.music.play(-1)
    
    while go:
        for event in pygame.event.get():
            pygame.event.pump()
            user_input = pygame.key.get_pressed()
            #allows the player to leave the game
            if event.type == pygame.QUIT:
                quitGame()
            if user_input[pygame.K_ESCAPE]:
                quitGame()

        #loop allowing for different times for the different slides
                
        #the second and third slide is shorter than the other slides
        if s==1 and i==4000:#show this slide less
            s+=1
            i=0
        elif s==2 and i==2000:#show this slide less
            s+=1
            i=0
        elif s>=7 and i==7000:#if its the 7th or more slide show the slide for longer
            s+=1
            i=0
            if s==12:
                #stop the slides and start the gameplay
                go=False
        elif i==5000 and s!=1 and s!=2 and s<7:
            #for the other slides if it hits 5000 loops go onto the next slide
            s+=1
            i=0
        else:
            i+=1
        
        #if statements that determine what picture is being displayed
        if s==0:
            screen.blit(config.opening_slides["s0"],(0,0))
            text_surface, text_rect = text_objects("Well that was a good day at work!", config.fonts["small"], config.colours["black"])        
            text_rect.center = (330), (490)
            screen.blit(text_surface, text_rect)
        if s==1:
            screen.blit(config.opening_slides["s1"],(0,0))
        if s==1 and i==2500:
            #pygame.mixer.music.load(os.path.join(soundEffectsFolder, "punch.wav")) TODo
            config.sounds["punch"]
            pygame.mixer.music.play(1)
        if s==2:
            screen.blit(config.opening_slides["s2"],(0,0))
        if s==3:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("'You sure we got the right guy?'", config.fonts["small"], config.colours["red"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==4:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("...*mumble*...", config.fonts["small"], config.colours["yellow"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==5 and i==2000:
            #pygame.mixer.music.load(os.path.join(soundEffectsFolder, "punch.wav"))
            config.sounds["punch"]
            pygame.mixer.music.play(1)
        if s==5:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("'Hey I think he's waking up'", config.fonts["small"], config.colours["red"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==6:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("3 HOURS LATER", config.fonts["small"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==7:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("'Just chuck him in the cell. We'll deal with him later'", config.fonts["small"], config.colours["yellow"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        
        if s==8:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("While I was getting dragged in I saw the map of the fortress", config.fonts["small"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        if s==9:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("I heard that the 2 guards have a key or something", config.fonts["small"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==10:
            screen.blit(config.opening_slides["map"], (0,0))
        
        if s==11:
            screen.fill(config.colours["black"])
            #display title
            text_surface, text_rect = text_objects("I have to get out of here...", config.fonts["small"], config.colours["white"])
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        
        pygame.display.update()
        
    game()#play game

#tutorial
def tutorial():
    #set the level to the tutorial with player's health of 10
    stage[0]=0
    stage[1]=0
    player.health=10
    saveGame()
    game()
        
#method that quits the game and program
def quitGame():
    pygame.quit()
    quit()

def finishGame():
    go = True
    i=0#count how long it goes for
    s=0#number of slides
    #loads music in
    pygame.mixer.music.load(config.music["victory"])
    # the -1 is the loops, so here it is infinite
    pygame.mixer.music.play(-1)
    while go:
        
        for event in pygame.event.get():
            pygame.event.pump()
            
            #allows the player to leave the game
            if event.type == pygame.QUIT:
                quitGame()
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_ESCAPE]:
            quitGame()

        
        if i==2000:#for the other slides if it hits 5000 loops go onto the next slide
            if s==10:
                i=0
            else:
                s+=1
                i=0
        else:
            i+=1
        
        #if statements that determine what picture is being displayed
        if s==0:
            screen.blit(config.ending_slides["s1"],(0,0))
            
        if s==1:
            screen.blit(config.ending_slides["s2"],(0,0))
        if s==2:
            screen.blit(config.ending_slides["s3"],(0,0))
        if s==3:
            screen.blit(config.ending_slides["s4"],(0,0))
        if s==4:
            screen.blit(config.ending_slides["s5"],(0,0))
        if s==5:
            screen.blit(config.ending_slides["s6"],(0,0))
        if s==6:
            screen.blit(config.ending_slides["s7"],(0,0))
        if s==7:
            screen.blit(config.ending_slides["s9"],(0,0))
        if s==8:
            screen.blit(config.ending_slides["s10"],(0,0))
        if s==9:
            screen.fill(config.colours["black"])
            text_surface, text_rect = text_objects("Fin", config.fonts["medium"], config.colours["white"])
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        if s==10:
            screen.fill(config.colours["black"])

            screen.blit(config.duck_sprites["rDuck"],(300,200))
            text_surface, text_rect = text_objects("Thanks for playing!", config.fonts["medium"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        
        pygame.display.update()

#resets the screen
def reset(currentStage):
    
    if stage[0] ==0:#if its the first stage
        screen.fill(config.colours["black"])
    else:
        if stage [0]==2:
            screen.blit(config.background_images["level2"],(0,0))
        else:
            screen.blit(config.background_images["level1"],(0,0))
        
    #text shown in the tutorial
    if stage[0]==0:
        if stage[1]==0:#if stage 1 
            message_display("Use the arrow keys to move and jump",350, 100, 15, config.colours["white"])
            message_display("Press s to save your game",350, 120, 15, config.colours["white"])
            message_display("To move onto the next room exit to the right of the screen",350, 140, 15, config.colours["white"])
        if stage[1]==1:#if stage 2
            message_display("Use the space bar to shoot enemies", 350, 100, 15, config.colours["white"])
            message_display("Your health and inventory are in the top left corner", 350, 120, 15, config.colours["white"])
        if stage[1]==2:#if stage 3
            message_display("Enemies and spikes will reduce your health", 350, 100, 15, config.colours["white"])
            message_display("Blue teleporters can be used to go down", 350, 120, 15, config.colours["white"])
        if stage[1]==5:#if stage 3
            message_display("Orange teleporters can be used to go up", 350, 100, 15, config.colours["white"])
        if stage[1]==6:#if stage 7
            message_display("Pick up health by walking over the bread", 330, 100, 15, config.colours["white"])
            message_display("Interact with objects by pressing e when near them", 320, 120, 15, config.colours["white"])
            message_display("Some objects are locked whereas others are open", 320, 140, 15, config.colours["white"])
        if stage[1]==7:#if stage 8
            message_display("Exit to the right when you are done!", 350, 100, 15, config.colours["white"])
            message_display("Don't forget to save!", 350, 120, 15, config.colours["white"])

    #draws the walls
    for wall in currentStage.walls:
        pygame.draw.rect(screen, config.colours["white"], wall.rect)
    
    #Draws health Icon in top left corner of screen
    screen.blit(config.collectible_sprites["bread"], (45,0))
    message_display("x" + str(player.health), 90, 15, 15, config.colours["black"])

    #draws the keys the player currently has
    i=0#variable is used to detect how many keys the player has and print them with space between them
    if player.keyFrag1:
        i+=1
        screen.blit(config.key_sprites["key1"], (100+30*i,4))
    if player.keyFrag2:
        i+=1
        screen.blit(config.key_sprites["key2"], (100+30*i,4))
    if player.bossKey:
        i+=1
        screen.blit(config.key_sprites["bossKey"], (100+30*i,4))
    if player.blueKey:
        i+=1
        screen.blit(config.key_sprites["blueKey"], (100+30*i,4))
    #change player sprite
    player.change()

    #draws player onto the screen
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(player)
    all_sprites_list.draw(screen)

    global txt
    #displays text if txt is true and if the player is in the right room
    if txt:
        if stage[1]==7 and stage[0]==0:
            message_display("You have obtained a blue key!",500, 320, 12, config.colours["white"])
            message_display("Now you can go back to the locked box!",500, 340, 12, config.colours["white"])
        if stage[1]==6 and stage[0]==0:
            message_display("You have obtained 2 1-ups!",300, 300, 12, config.colours["white"])
        
        if stage[1]==0 and stage[0]==1:
            message_display("You have obtained 8 1-ups!",150, 400, 12, config.colours["white"])
            
        if stage[1]==2 and stage[0]==1:
            message_display("You have obtained 4 1-ups and a key fragment!",300, 300, 12, config.colours["white"])
            if player.bossKey:
                message_display("You now have a yellow key!",300, 320, 12, config.colours["white"])

        if stage[0]==1 and stage[1]==8:
            message_display("You have obtained 4 1-ups and a key fragment!",300, 300, 12, config.colours["white"])
            if player.bossKey:
                message_display("You now have a yellow key!",300, 320, 12, config.colours["white"])
            
        if stage[1]==3 and stage[0]==1:
            message_display("You have obtained a blue key!",150, 40, 12, config.colours["white"])
            
        if stage[0]==1 and stage[1]==5:
            message_display("You have defeated the boss!",330, 300, 12, config.colours["white"])
            message_display("You can now exit the fortress to reach the spaceship to go home!",330, 280, 12, config.colours["white"])
        if stage[0]==2 and stage[1]==5:
            message_display("You have defeated the boss!",330, 280, 12, config.colours["white"])
            message_display("Go to the right to escape the planet!",330, 300, 12, config.colours["white"])
    if stage[0]==2 and stage[1]==0:
        message_display("You're nearly there!",300, 100, 12, config.colours["white"])

    if txt==False and stage[0]==1 and stage[1]==5:
        message_display("How dare you disturb me!",330, 100, 16, config.colours["red"])
        message_display("YOU SHALL NOW FACE MY WRATH!",330, 120, 16, config.colours["red"])
    if txt==False and stage[0]==2 and stage[1]==5:
        message_display("YOU WILL NOT DEFEAT ME THIS TIME!",330, 100, 16, config.colours["red"])
    
    # drawing everything on the screen
    #draw 1-up
    for up in currentStage.ups:
        up.draw(screen)
    #draw enemies
    for enemy in currentStage.enemies:
        enemy.draw(screen)
    #draw all interactives
    for i in currentStage.interactive:
        i.draw(screen)
        #if the interactive is locked display the following messages
        if i.locked:
            if stage[0]==0 and stage[1]==6:
                message_display("You need a blue key to open me!",300, 400, 12, config.colours["white"])
                
            if stage[1]==0:
                message_display("You need a blue key to open me!",150, 400, 12, config.colours["white"])
            
            if stage[1]==4 and stage[0]==1:
                message_display("You need a yellow key to open me!",500, 400, 12, config.colours["white"])
    
    #draw bullets
    for bullet in currentStage.bullets:
        bullet.draw(screen, currentStage)

    #draw boss
    for b in currentStage.boss:
        b.draw(screen, player.rect.x)
        
    #draw the enemies bullets
    for b in currentStage.eBullets:
        b.draw(screen, currentStage)
        
    #draw the spikes
    for s in currentStage.spikes:
        s.draw(screen)
        
    #draw teleporters going up
    for t in currentStage.teleUp:
        t.draw(screen)

    #draw teleporters going down 
    for t in currentStage.teleDown:
        t.draw(screen)
        
    pygame.display.flip()

#deletes all items in the level to prepare for the next level
def resetStage(level):
    #deletes the contents of the arrays
    level.resetStage()
    #txt is set to False meaning that the text it previously displayedis no longer displayed
    global txt
    txt=False

#initialise the player
player = PlayerSprite()

#where the game takes place
def game():
    currentStage = Level()
    resetStage(currentStage)#reset the level
    levelProgress()#read from the textfile what level the player is on
    currentStage = processCurrentStage()#read the stages

    #loads music in
    pygame.mixer.music.load(config.music["main"])
    # the -1 is the loops, so here it is infinite
    pygame.mixer.music.play(-1)
    
    global stage
    global txt
    
    loseGame = False#variable used to detect whether the player has lost the game
    
    #if its the 2nd level the players sprite will have a space helmet on
    if stage[0]==2:
        player.space=True
    else:
        player.space=False

    running = True#if running is false it stops the game
    loot=False#varaiable that allows the player only to take loot once from a boss
    
    shootLoop = 0#int that allows for a break in a player's shots
    teleLoop = 0#int that allows for a break in the player using the teleporters
    
    #set the players position in the room at (40,50)
    player.setPos(40,50)
    
    while running:
        #if the player is dead
        if player.health==0:
            #stop the game
            running = False
            loseGame=True
        
        
        pygame.event.pump()
        
        user_input = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        
                
        #running 60 FPS
        clock.tick(60)
        #allows for a break in shooting so the player cannot spam shoot
        if shootLoop> 0:
            shootLoop+=1
        if shootLoop >10:
            player.shoot=False
            shootLoop = 0

        #Allows for a break in getting hit
        if player.hitLoop> 0:
            player.hitLoop+=1
        if player.hitLoop >70:
            player.hitLoop = 0
            
            
        #allows for a break in using the teleporter
        if teleLoop > 0:
            teleLoop+=1
        if teleLoop >150:
            teleLoop = 0
        
        #collision detection for the teleporters
        for t in currentStage.teleUp:
            if player.rect.y<t.y+14 and player.rect.y+44>t.y and teleLoop==0:
                if player.rect.x+44>t.x and player.rect.x<t.x+32:
                    #if the player collides with the teleporter and teleLoop is 0
                    #reset the level and set it 3 levels lower
                    config.sounds["teleport"].play()#play sound effect
                    resetStage(currentStage)
                    stage[1]-=3
                    currentStage = processCurrentStage()
                    #set the players y and x coord
                    player.rect.y = height-60
                    player.rect.x -=10
                    teleLoop = 1#start break
                    
        #collision detection for the teleporters
        for t in currentStage.teleDown:
            if player.rect.y<t.y+14 and player.rect.y+44>t.y and teleLoop==0:
                if player.rect.x+44>t.x and player.rect.x<t.x+32:
                    config.sounds["teleport"].play()#play sound effect
                    #if the player collides with the teleporter and teleLoop is 0
                    #reset the level and set it 3 levels lower
                    resetStage(currentStage)
                    stage[1]+=3
                    currentStage = processCurrentStage()
                    #set the players y and x coord
                    player.rect.y = 80
                    player.rect.x +=10
                    teleLoop = 1#start break
    
        for e in currentStage.enemies:#for all enemies in the stage
            if random.randrange(100)==0 and e.mode==EnemyType.MEDIUM:#if the enemy us the police weasel and the random number = 0
                if e.vel<0:#if its facing left
                    f = -1
                else:#if its facing right
                    f=1
                #shiit a bullet in the way that the police weasel is facing
                currentStage.addEnemyProjectile(e.x+18, e.y+11, 6, config.colours["red"], f)
                
            if player.rect.y<e.y+e.height and player.rect.y+44>e.y and player.hitLoop==0:
                if player.rect.x+44>e.x and player.rect.x<e.x+e.width:
                    #collision detection between the player and an enemy
                    #if they collide players health decreases
                    player.healthChange(-1)
        
        #boss jumping and shooting
        for b in currentStage.boss:
            
            if player.rect.y<b.y+b.height and player.rect.y+44>b.y and player.hitLoop==0:
                if player.rect.x+44>b.x and player.rect.x<b.x+b.width:
                    #if the player collides with the boss take 1 health away from the player
                    player.healthChange(-1)
            #so there is a break in the enemies shots
            if b.shootLoop>0:
                b.shootLoop+=1
            if b.shootLoop >4:
                b.shootLoop = 0    
            
            if random.randrange(30)==0 and b.shootLoop==0:#if a random number from 0-30 is 0 then the boss will shoot
                facing = 1
                xShoot = b.x
                if player.rect.x>b.x:#if the player is to the right of the boss
                    facing = 1#shoot to the right
                    
                else:#if the player is to the right of the boss
                    facing = -1#shoot left
                    xShoot=b.x+b.width#shot will come from the very left of the sprite

                if len(currentStage.eBullets)<5:#if theere are less than 5 bullets on the screen allow for another bullet to be made
                    currentStage.addEnemyProjectile(xShoot, int(b.y+(int(b.height/2))), 9, config.colours["red"],facing)
                b.shootLoop = 1
                
            #boss jumping
            if not(b.isJump) and random.randrange(50)==0:
                #if a random number from 0-50 is 0 and the boss isn't already jumping
                b.isJump = True#make the boss jump
                
            #if the boss is currently jumping
            if b.isJump:
                if b.mode==BossType.MINIBOSS and b.jumpCount >= -8:
                    i=0.7
                    b.y-=(b.jumpCount * abs(b.jumpCount)) * i
                    b.jumpCount -= 1
                elif (b.mode==BossType.BOSS or b.mode==BossType.FINAL_BOSS) and b.jumpCount>= -9:
                    i=0.5
                    b.y-=(b.jumpCount * abs(b.jumpCount)) * i
                    b.jumpCount -= 1
                else:
                    if b.mode == BossType.MINIBOSS:
                        b.jumpCount = 8
                    else:
                        b.jumpCount = 9
                    b.isJump = False

            else:#gravity for the enemy
                if b.y+b.height< 477:
                    b.y+=7

        
        #collision detection between the bullets and any of the enemies
        for bullet in currentStage.bullets:
            for e in currentStage.enemies:
                if bullet.y-bullet.radius<e.y+e.height and bullet.y+bullet.radius>e.y:
                    if bullet.x+bullet.radius>e.x and bullet.x-bullet.radius<e.x+e.width:
                        e.hit()
                        if e.health ==0:#if the enemy has no health left delete them from the screen
                            currentStage.enemies.remove(e)
                        currentStage.bullets.remove(bullet)#delete the bullet as well
                        
            for e in currentStage.boss:
                if bullet.y-bullet.radius<e.y+e.height and bullet.y+bullet.radius>e.y:
                    if bullet.x+bullet.radius>e.x and bullet.x-bullet.radius<e.x+e.width:
                        #collision event for the boss and the player's bullet
                        e.hit()#take a hp away from the boss
                        if e.health ==0:#if the boss has no health left delete them from the screen
                            currentStage.boss.remove(e)
                        currentStage.bullets.remove(bullet)#delete the bullet as well

                            
        #what happens when you kill the mini bosses and bosses
        if stage[0]==1 and stage[1]==2 and len(currentStage.boss)==0 and loot==False:
            #if you kill the first miniboss
            player.addKey("frag1")#add the key fragment
            txt=True#display relevant text
            player.healthChange(4)#add 4 health
            loot=True#player cannot loot this room unless they exit then reenter the room
            
        if stage[0]==1 and stage[1]==8 and len(currentStage.boss)==0 and loot==False:
            #if you kill the first miniboss
            player.addKey("frag2")#add the key fragment
            txt=True#display relevant text
            player.healthChange(4)#add 4 health
            loot=True#player cannot loot this room unless they exit then reenter the room
        
        if stage[0]==1 and stage[1]==5 and len(currentStage.boss)==0 and loot==False:
            #if you kill the first boss
            txt=True#display relevant text
            player.healthChange(3)#add 3 health
            loot=True#player cannot loot this room unless they exit then reenter the room
            del currentStage.interactive[:]#delete the interactive blocks so the player can escape

        if stage[0]==2 and stage[1]==5 and len(currentStage.boss)==0 and loot==False:
            #if you kill the first boss
            txt=True#display relevant text
            del currentStage.interactive[:]#delete the interactive blocks so the player can escape

        #collision event between the enemies bullets and the player
        for bullet in currentStage.eBullets:
            if bullet.y-bullet.radius<player.rect.y+44 and bullet.y+bullet.radius>player.rect.y:
                if bullet.x+bullet.radius>player.rect.x and bullet.x-bullet.radius<player.rect.x+44:
                    player.healthChange(-1)#minus a health from the player
                    currentStage.eBullets.remove(bullet)#delete the bullet from the screen
  
        if user_input[pygame.K_ESCAPE]:
            #if the user presses the escape button
            quitGame()
        if user_input[pygame.K_s]:
            #if the user presses the s button
            saveGame()
            
        #if player wants to shoot
        if user_input[pygame.K_SPACE] and shootLoop==0:
            #if the player presses the space button and there is a break between the shooting
            if player.left:#if the player is facing to the left
                facing = -1
            else:
                facing = 1
            if len(currentStage.bullets)<5:#if theere are less than 5 bullets on the screen allow for another bullet to be made
                config.sounds["shoot"].play()#play sound effect
                currentStage.addProjectile(player.rect.x+44, player.rect.y+22, 6, (163,163,194), facing)#make bullet
                player.shoot = True#show a different sprite when shooting
            shootLoop = 1#player has shot
            

        #player movement
        if not(player.isJump):
            if user_input[pygame.K_UP]:
                #if the user presses the up key, jump
                config.sounds["jump"].play()#play sound effect
                player.isJump = True
               
            elif player.rect.y < (height-30):
                #gravity for the player
                player.move(0,7, currentStage)
        else:
            if player.jumpCount >= -8:
                #make the arc for the jump
                player.move(0,-(player.jumpCount * abs(player.jumpCount)) * 0.7, currentStage)
                player.jumpCount -= 1
                
            else: 
                player.jumpCount = 8
                player.isJump = False#jump can happen again
                
        
        if user_input[pygame.K_LEFT]:
            #if the user presses the left key
            player.move(-5,0, currentStage)
            player.left = True#change sprite to face left
            
            if player.rect.x < -44:
                #if the player goes off the screen
                resetStage(currentStage)#reset level
                loot=False#loot can happen again in the level
                stage[1]-=1#go to the stage to the left of the current stage
                currentStage = processCurrentStage()#read level
                player.rect.x = width-44#set the player to be on the right of the screen
            
        if user_input[pygame.K_RIGHT]:
            player.move(5,0, currentStage)
            player.left = False
            if player.rect.x > width-40:
                resetStage(currentStage)#reset level contents
                loot=False#loot can happen again in the level
                #if the player finishes the tutorial
                if stage[0]==0 and stage[1]==7:
                    running=False#stop the game

                #if the player finishes the 1st level
                elif stage[0]==1 and stage[1]==5:
                    
                    stage[0]=2#go to the sencond level stage 1
                    stage[1]=0
                    player.space=True
                    levelProgress()
                    currentStage = processCurrentStage()
                    player.setPos(40,player.rect.y)
                    
                elif stage[0]==2 and stage[1]==5:
                    #if the player has finished the second level
                    running = False
                    finishGame()
                else:
                    
                    stage[1]+=1  #go to the stage to the right of the current stage                  
                    currentStage = processCurrentStage()#read level
                    player.rect.x = 2#set the player to be on the left of the screen
                
        reset(currentStage)#reset the screen
        pygame.display.flip()
        
    if loseGame == True:#if the player lost the game
        lose()#execute method


intro()#execute the intro         
