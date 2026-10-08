import os
import random
from stageType import StageType
import pygame
from player import PlayerSprite
from level import Level
from enemyType import EnemyType
from bossType import BossType
import config
import xml.etree.ElementTree as ET
from stageTracker import StageTracker
#start pygame
os.environ["SDL_VIDEO_CENTERED"]="1"
pygame.init()


#set up display
pygame.display.set_caption("AbDuckTed!")
width = 660#width of the screen
height = 510#height of the screen
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

stage = StageTracker(StageType.TUTORIAL, 0)#create a stage object with the current stage and level

#boolean that allows for text to be shown on the screen according to the stage and level
global txt
txt=False

#The two methods together create a text to be shown on screen
def create_text_object(text, font, colour):
    """
    Render text and create a rectangle for positioning it on the screen.

    The text is rendered with antialiasing enabled and returned together with
    its bounding rectangle. The rectangle can then be adjusted, such as by
    centering it, before the surface is drawn with ``screen.blit``.

    :param str text: The text to render.
    :param pygame.font.Font font: The Pygame font used to render the text.
    :param tuple colour: The RGB colour used for the text.
    :return: A tuple containing the rendered text surface and its rectangle.
    :rtype: tuple
    """
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def show_message(text, top, left, size, colour):
    """
    Display a message on the screen at a specified position, size, and colour.

    :param str text: The message to display.
    :param int top: The vertical position (y-coordinate) for the message.
    :param int left: The horizontal position (x-coordinate) for the message.
    :param int size: The font size for the message.
    :param tuple colour: The RGB colour used for the message.
    """
    my_text = pygame.font.SysFont("berlinsansfb", size)
    text_surface, text_rect = create_text_object(text, my_text, colour)
    #set where the text appears on screen
    text_rect.center = (top, left)
    screen.blit(text_surface, text_rect)

def save_game_to_file():
    """
    Saves the current game state to an XML file named save.xml.
    Saves the current stage, player's health, and key fragments to the XML file.
    """
    root = ET.Element("game_state")
    stage_element = ET.SubElement(root, "stage")
    stage_element.text = str(stage.get_stage_number())
    sub_stage_element = ET.SubElement(root, "level")
    sub_stage_element.text = str(stage.get_level_number())
    health_element = ET.SubElement(root, "health")
    health_element.text = str(player.health)
    key_frag1_element = ET.SubElement(root, "key_frag1")
    key_frag1_element.text = str(player.keyFrag1)
    key_frag2_element = ET.SubElement(root, "key_frag2")
    key_frag2_element.text = str(player.keyFrag2)
    boss_key_element = ET.SubElement(root, "boss_key")
    boss_key_element.text = str(player.bossKey)
    blue_key_element = ET.SubElement(root, "blue_key")
    blue_key_element.text = str(player.blueKey)

    tree = ET.ElementTree(root)
    try:
        tree.write("save.xml", encoding="utf-8", xml_declaration=True)
        show_message("Save successful!", 300, 100, 12, config.colours["white"])
    except IOError:
        show_message("Unable to save. :(", 300, 100, 12, config.colours["white"])

def load_game_from_file():
    """
    Loads the game state from an XML file named save.xml.
    Loads the current stage, player's health, and key fragments from the XML file.
    """
    try:
        tree = ET.parse("save.xml")
        root = tree.getroot()
        stage = StageTracker(StageType(int(root.find("stage").text)), int(root.find("level").text))
        player.health = int(root.find("health").text)
        player.keyFrag1 = root.find("key_frag1").text == "True"
        player.keyFrag2 = root.find("key_frag2").text == "True"
        player.bossKey = root.find("boss_key").text == "True"
        player.blueKey = root.find("blue_key").text == "True"
    except (IOError, ET.ParseError):
        print("No save file available or file error.")


def update_current_stage():
    """
    Reads the current stage's levels from it's relevant save file and saves them to the levels list.
    """
    levels = []
    global stage
    
    if stage.get_stage_number() == StageType.TUTORIAL:
        levels = read_stage_file(levelFileName='tutorial.txt')
    elif stage.get_stage_number() == StageType.LEVEL_1:
        levels = read_stage_file(levelFileName='level1.txt')
    elif stage.get_stage_number() == StageType.LEVEL_2:
        levels = read_stage_file(levelFileName='level2.txt')   
    else:
        levels = read_stage_file(levelFileName='level1.txt')

    return levels
        

def read_stage_file(levelFileName: str):
    """
    Reads the stage 

    :return: a nested list of the levels in a stage. Where each element is a level, each element of a level is a string representing a row of sprites.
    :rtype: list
    """
    levels = []
    level = []
    for line in open(os.path.join(config.levelPath, levelFileName)):
        if line.strip() == "stop":
            levels.append(level)
            level = []
        else:
            level.append(line)      
    return levels


def process_current_level(levels: list):
    """
    Processes the current stage's levels and creates a Level object with walls, enemies, spikes, teleporters, and interactive objects.
    """
    currentStage = Level(levels[stage.get_level_number()])
    return currentStage

def show_button(msg, x, y, width, height, active_colour, inactive_colour, action=None):
    """
    Creates a button on the screen with the specified message, position, size, and colors.

    :param str msg: The message to display on the button.
    :param int x: The x-coordinate of the button's top-left corner.
    :param int y: The y-coordinate of the button's top-left corner.
    :param int width: The width of the button.
    :param int height: The height of the button.
    :param tuple active_colour: The RGB color of the button when hovered over.
    :param tuple inactive_colour: The RGB color of the button when not hovered over.
    :param function action: The function to execute when the button is clicked.
    """

    mouse_position = pygame.mouse.get_pos()
    is_mouse_pressed = pygame.mouse.get_pressed()

    #Creates a hover event
    if x + width > mouse_position[0] > x and y + height > mouse_position[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, width, height))
        if is_mouse_pressed[0] == 1:
            action()
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, width, height))
    #show the text in the middle of the button
    text_surface, text_rect = create_text_object(msg, config.fonts["small"], config.colours["black"])
    text_rect.center = (x+(width/2)), (y+(height/2))
    screen.blit(text_surface, text_rect)
    

def lose():
    """
    Displays the "YOU HAVE DIED" screen and provides options to try again or quit the game.
    """
    go = True
    while go:
        check_quit_event()
        screen.fill(config.colours["black"])
        show_message("YOU HAVE DIED", 320,100,20, config.colours["white"])
        show_message("TRY AGAIN?", 320,200,20, config.colours["white"])
        
        show_button("YES",100, 450, 120, 50, config.colours["brightGreen"], config.colours["green"], load_game)
        show_button("NO", 400, 450, 120, 50, config.colours["brightRed"], config.colours["red"], quit_game)
        pygame.display.update()
    

def show_title_screen():
    """
    Displays the title screen with options for the player to choose from: Tutorial, Load Game, or New Game.
    """
    intro = True
    while intro:
        check_quit_event()
        #load in the background image with the main character sitting on the T
        screen.blit(config.background_images["level1"], (0,0))
        screen.blit(config.duck_sprites["rDuck"], (400,180))

        #display title
        text_surface, text_rect = create_text_object("AbDuckTed", config.fonts["large"], config.colours["yellow"])        
        text_rect.center = (330), (255)
        screen.blit(text_surface, text_rect)
        
        #display button representing the different options the player can choose
        show_button("Tutorial", 100, 450, 120, 50, config.colours["brightYellow"], config.colours["yellow"], tutorial)
        show_button("Load Game", 500, 450, 120, 50, config.colours["brightYellow"], config.colours["yellow"], load_game)
        show_button("New Game", 300, 450, 120, 50, config.colours["brightYellow"], config.colours["yellow"], new_game)

        pygame.display.update()


def check_quit_event():
    """
    Checks for quit events and allows the player to exit the game by pressing the ESC key or closing the window.
    """
    for event in pygame.event.get():
        pygame.event.pump()
        user_input = pygame.key.get_pressed()
        #allows the player to leave the game
        if event.type == pygame.QUIT:
            quit_game()
        if user_input[pygame.K_ESCAPE]:
            quit_game()

def load_game():
    """
    Loads the game state from a save file and starts the game.
    """
    load_game_from_file()
    game()

def new_game():
    """
    Starts a new game and creates a new save file.
    """
    #set to level one and with players health to 10 and no keys
    stage.stage_number = StageType.LEVEL_1
    stage.level_number = 0
    player.health = 10
    player.blueKey = False
    player.bossKey = False
    player.keyFrag1 = False
    player.keyFrag2 = False
    
    save_game_to_file()
    opening_credits()
      
    game()#play game

def opening_credits():
    go = True
    i=0#count how long each screen goes for
    s=0#number of slides
    #start music
    pygame.mixer.music.load(config.music["happy"])
    pygame.mixer.music.play(-1)
    
    while go:
        check_quit_event()

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
            text_surface, text_rect = create_text_object("Well that was a good day at work!", config.fonts["small"], config.colours["black"])        
            text_rect.center = (330), (490)
            screen.blit(text_surface, text_rect)
        if s==1:
            screen.blit(config.opening_slides["s1"],(0,0))
        if s==1 and i==2500:
            pygame.mixer.music.load(config.music["punch"])
            pygame.mixer.music.play(1)
        if s==2:
            screen.blit(config.opening_slides["s2"],(0,0))
        if s==3:
            screen.fill(config.colours["black"])
            text_surface, text_rect = create_text_object("'You sure we got the right guy?'", config.fonts["small"], config.colours["red"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==4:
            screen.fill(config.colours["black"])
            text_surface, text_rect = create_text_object("...*mumble*...", config.fonts["small"], config.colours["yellow"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==5 and i==2000:
            pygame.mixer.music.load(config.music["punch"])
            pygame.mixer.music.play(1)
        if s==5:
            screen.fill(config.colours["black"])
            text_surface, text_rect = create_text_object("'Hey I think he's waking up'", config.fonts["small"], config.colours["red"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==6:
            screen.fill(config.colours["black"])
            text_surface, text_rect = create_text_object("3 HOURS LATER", config.fonts["small"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==7:
            screen.fill(config.colours["black"])
            text_surface, text_rect = create_text_object("'Just chuck him in the cell. We'll deal with him later'", config.fonts["small"], config.colours["yellow"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        
        if s==8:
            screen.fill(config.colours["black"])
            text_surface, text_rect = create_text_object("While I was getting dragged in I saw the map of the fortress", config.fonts["small"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        if s==9:
            screen.fill(config.colours["black"])
            text_surface, text_rect = create_text_object("I heard that the 2 guards have a key or something", config.fonts["small"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
            
        if s==10:
            screen.blit(config.opening_slides["map"], (0,0))
        
        if s==11:
            screen.fill(config.colours["black"])
            #display title
            text_surface, text_rect = create_text_object("I have to get out of here...", config.fonts["small"], config.colours["white"])
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        
        pygame.display.update()
            
def tutorial():
    """
    Starts the tutorial stage. Saves the game state and starts the game.
    """
    #set the level to the tutorial with player's health of 10
    stage.stage_number = StageType.TUTORIAL
    stage.level_number = 0
    player.health=10
    save_game_to_file()
    game()
        
def quit_game():
    """
    Quits the game and closes the Pygame window.
    """
    pygame.quit()
    quit()

def closing_credits():
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
                quit_game()
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_ESCAPE]:
            quit_game()

        
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
            text_surface, text_rect = create_text_object("Fin", config.fonts["medium"], config.colours["white"])
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        if s==10:
            screen.fill(config.colours["black"])

            screen.blit(config.duck_sprites["rDuck"],(300,200))
            text_surface, text_rect = create_text_object("Thanks for playing!", config.fonts["medium"], config.colours["white"])        
            text_rect.center = (330), (255)
            screen.blit(text_surface, text_rect)
        
        pygame.display.update()


def display_keys():
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

def reset_level(currentStage):
    
    if stage.get_stage_number() == StageType.TUTORIAL:#if its the tutorial
        screen.fill(config.colours["black"])
    else:
        if stage.get_stage_number() == StageType.LEVEL_2:
            screen.blit(config.background_images["level2"],(0,0))
        else:
            screen.blit(config.background_images["level1"],(0,0))
        
    #text shown in the tutorial
    if stage.get_stage_number() == StageType.TUTORIAL:
        if stage.get_level_number() == 0:#if stage 1 
            show_message("Use the arrow keys to move and jump",350, 100, 15, config.colours["white"])
            show_message("Press s to save your game",350, 120, 15, config.colours["white"])
            show_message("To move onto the next room exit to the right of the screen",350, 140, 15, config.colours["white"])
        if stage.get_level_number() == 1:#if stage 2
            show_message("Use the space bar to shoot enemies", 350, 100, 15, config.colours["white"])
            show_message("Your health and inventory are in the top left corner", 350, 120, 15, config.colours["white"])
        if stage.get_level_number() == 2:#if stage 3
            show_message("Enemies and spikes will reduce your health", 350, 100, 15, config.colours["white"])
            show_message("Blue teleporters can be used to go down", 350, 120, 15, config.colours["white"])
        if stage.get_level_number() == 5:#if stage 3
            show_message("Orange teleporters can be used to go up", 350, 100, 15, config.colours["white"])
        if stage.get_level_number() == 6:#if stage 7
            show_message("Pick up health by walking over the bread", 330, 100, 15, config.colours["white"])
            show_message("Interact with objects by pressing e when near them", 320, 120, 15, config.colours["white"])
            show_message("Some objects are locked whereas others are open", 320, 140, 15, config.colours["white"])
        if stage.get_level_number() == 7:#if stage 8
            show_message("Exit to the right when you are done!", 350, 100, 15, config.colours["white"])
            show_message("Don't forget to save!", 350, 120, 15, config.colours["white"])

    #draws the walls
    for wall in currentStage.walls:
        pygame.draw.rect(screen, config.colours["white"], wall.rect)
    
    #Draws health Icon in top left corner of screen
    screen.blit(config.collectible_sprites["bread"], (45,0))
    show_message("x" + str(player.health), 90, 15, 15, config.colours["black"])

    display_keys()#displays the keys the player has in the top left corner of the screen
    
    #draws player onto the screen
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(player)
    all_sprites_list.draw(screen)

    global txt
    #displays text if txt is true and if the player is in the right room
    if txt:
        if stage.get_level_number() == 7 and stage.get_stage_number() == StageType.TUTORIAL:
            show_message("You have obtained a blue key!",500, 320, 12, config.colours["white"])
            show_message("Now you can go back to the locked box!",500, 340, 12, config.colours["white"])
        if stage.get_level_number() == 6 and stage.get_stage_number() == StageType.TUTORIAL:
            show_message("You have obtained 2 1-ups!",300, 300, 12, config.colours["white"])

        if stage.get_level_number() == 0 and stage.get_stage_number() == StageType.LEVEL_1:
            show_message("You have obtained 8 1-ups!",150, 400, 12, config.colours["white"])

        if stage.get_level_number() == 2 and stage.get_stage_number() == StageType.LEVEL_1:
            show_message("You have obtained 4 1-ups and a key fragment!",300, 300, 12, config.colours["white"])
            if player.bossKey:
                show_message("You now have a yellow key!",300, 320, 12, config.colours["white"])

        if stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 8:
            show_message("You have obtained 4 1-ups and a key fragment!",300, 300, 12, config.colours["white"])
            if player.bossKey:
                show_message("You now have a yellow key!",300, 320, 12, config.colours["white"])
            
        if stage.get_level_number() == 3 and stage.get_stage_number() == StageType.LEVEL_1:
            show_message("You have obtained a blue key!",150, 40, 12, config.colours["white"])
            
        if stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 5:
            show_message("You have defeated the boss!",330, 300, 12, config.colours["white"])
            show_message("You can now exit the fortress to reach the spaceship to go home!",330, 280, 12, config.colours["white"])
        if stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 5:
            show_message("You have defeated the boss!",330, 280, 12, config.colours["white"])
            show_message("Go to the right to escape the planet!",330, 300, 12, config.colours["white"])
    if stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 0:
        show_message("You're nearly there!",300, 100, 12, config.colours["white"])

    if txt==False and stage.get_stage_number() == StageType.LEVEL_2 and stage.get_level_number() == 5:
        show_message("How dare you disturb me!",330, 100, 16, config.colours["red"])
        show_message("YOU SHALL NOW FACE MY WRATH!",330, 120, 16, config.colours["red"])
    if txt==False and stage.get_stage_number() == StageType.LEVEL_2 and stage.get_level_number() == 5:
        show_message("YOU WILL NOT DEFEAT ME THIS TIME!",330, 100, 16, config.colours["red"])
    
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
            if stage.get_stage_number() == StageType.TUTORIAL and stage.get_level_number() == 6:
                show_message("You need a blue key to open me!",300, 400, 12, config.colours["white"])
                
            if stage.get_level_number() == 0:
                show_message("You need a blue key to open me!",150, 400, 12, config.colours["white"])
            
            if stage.get_level_number() == 4 and stage.get_stage_number() == StageType.LEVEL_1:
                show_message("You need a yellow key to open me!",500, 400, 12, config.colours["white"])
    
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
    levels = update_current_stage()#read from the textfile what level the player is on
    currentLevel = process_current_level(levels)#create a level object with the current level
    #loads music in
    pygame.mixer.music.load(config.music["main"])
    # the -1 is the loops, so here it is infinite
    pygame.mixer.music.play(-1)
    
    global stage
    global txt
    
    loseGame = False#variable used to detect whether the player has lost the game
    
    #if its the 2nd level the players sprite will have a space helmet on
    if stage.get_stage_number() == StageType.LEVEL_2:
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
                quit_game()
        
                
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

        pygame.event.pump()
        user_input = pygame.key.get_pressed()#get the key pressed by the user
        #same code as walls except with the interactives rect instead
        for f in currentLevel.interactive:
            #allows player to be 10 pixels away from the interactive and still be able to interact with it
            if player.rect.y<f.y+30 and player.rect.y+44>f.y:
                if player.rect.x+44>f.x-10 and player.rect.x<f.x+40:
                    if user_input[pygame.K_e]:#if the user pressed e
                        f.interact(currentLevel.interactive, player, stage)#interact with object
                
            if player.rect.colliderect(f.rect):
                if user_input[pygame.K_e]:#if the user pressed e
                    f.interact(currentLevel.interactive, player, stage)#interact with object


        
        #collision detection for the teleporters
        for t in currentLevel.teleUp:
            if player.rect.y<t.y+14 and player.rect.y+44>t.y and teleLoop==0:
                if player.rect.x+44>t.x and player.rect.x<t.x+32:
                    #if the player collides with the teleporter and teleLoop is 0
                    #reset the level and set it 3 levels lower
                    config.sounds["teleport"].play()#play sound effect
                    resetStage(currentLevel)
                    stage.move_to_above_room()
                    currentLevel = process_current_level(levels)
                    #set the players y and x coord
                    player.rect.y = height-60
                    player.rect.x -=10
                    teleLoop = 1#start break
                    
        #collision detection for the teleporters
        for t in currentLevel.teleDown:
            if player.rect.y<t.y+14 and player.rect.y+44>t.y and teleLoop==0:
                if player.rect.x+44>t.x and player.rect.x<t.x+32:
                    config.sounds["teleport"].play()#play sound effect
                    #if the player collides with the teleporter and teleLoop is 0
                    #reset the level and set it 3 levels lower
                    resetStage(currentLevel)
                    stage.move_to_below_room()
                    currentLevel = process_current_level(levels)
                    #set the players y and x coord
                    player.rect.y = 80
                    player.rect.x +=10
                    teleLoop = 1#start break
    
        for e in currentLevel.enemies:#for all enemies in the stage
            if random.randrange(100)==0 and e.mode==EnemyType.MEDIUM:#if the enemy us the police weasel and the random number = 0
                if e.vel<0:#if its facing left
                    f = -1
                else:#if its facing right
                    f=1
                #shiit a bullet in the way that the police weasel is facing
                currentLevel.addEnemyProjectile(e.x+18, e.y+11, 6, config.colours["red"], f)
                
            if player.rect.y<e.y+e.height and player.rect.y+44>e.y and player.hitLoop==0:
                if player.rect.x+44>e.x and player.rect.x<e.x+e.width:
                    #collision detection between the player and an enemy
                    #if they collide players health decreases
                    player.healthChange(-1)
        
        #boss jumping and shooting
        for b in currentLevel.boss:
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

                if len(currentLevel.eBullets)<5:#if theere are less than 5 bullets on the screen allow for another bullet to be made
                    currentLevel.addEnemyProjectile(xShoot, int(b.y+(int(b.height/2))), 9, config.colours["red"],facing)
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
        for bullet in currentLevel.bullets:
            for e in currentLevel.enemies:
                if bullet.y-bullet.radius<e.y+e.height and bullet.y+bullet.radius>e.y:
                    if bullet.x+bullet.radius>e.x and bullet.x-bullet.radius<e.x+e.width:
                        e.hit()
                        if e.health ==0:#if the enemy has no health left delete them from the screen
                            currentLevel.enemies.remove(e)
                        currentLevel.bullets.remove(bullet)#delete the bullet as well
                        
            for e in currentLevel.boss:
                if bullet.y-bullet.radius<e.y+e.height and bullet.y+bullet.radius>e.y:
                    if bullet.x+bullet.radius>e.x and bullet.x-bullet.radius<e.x+e.width:
                        #collision event for the boss and the player's bullet
                        e.hit()#take a hp away from the boss
                        if e.health ==0:#if the boss has no health left delete them from the screen
                            currentLevel.boss.remove(e)
                        currentLevel.bullets.remove(bullet)#delete the bullet as well

                            
        #what happens when you kill the mini bosses and bosses
        if stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 2 and len(currentLevel.boss) == 0 and loot == False:
            #if you kill the first miniboss
            player.addKey("frag1")#add the key fragment
            txt=True#display relevant text
            player.healthChange(4)#add 4 health
            loot=True#player cannot loot this room unless they exit then reenter the room
            
        if stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 8 and len(currentLevel.boss) == 0 and loot == False:
            #if you kill the first miniboss
            player.addKey("frag2")#add the key fragment
            txt=True#display relevant text
            player.healthChange(4)#add 4 health
            loot=True#player cannot loot this room unless they exit then reenter the room
        
        if stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 5 and len(currentLevel.boss) == 0 and loot == False:
            #if you kill the first boss
            txt=True#display relevant text
            player.healthChange(3)#add 3 health
            loot=True#player cannot loot this room unless they exit then reenter the room
            del currentLevel.interactive[:]#delete the interactive blocks so the player can escape

        if stage.get_stage_number() == StageType.LEVEL_2 and stage.get_level_number() == 5 and len(currentLevel.boss) == 0 and loot == False:
            #if you kill the first boss
            txt=True#display relevant text
            del currentLevel.interactive[:]#delete the interactive blocks so the player can escape

        #collision event between the enemies bullets and the player
        for bullet in currentLevel.eBullets:
            if bullet.y-bullet.radius<player.rect.y+44 and bullet.y+bullet.radius>player.rect.y:
                if bullet.x+bullet.radius>player.rect.x and bullet.x-bullet.radius<player.rect.x+44:
                    player.healthChange(-1)#minus a health from the player
                    currentLevel.eBullets.remove(bullet)#delete the bullet from the screen
  
        if user_input[pygame.K_ESCAPE]:
            #if the user presses the escape button
            quit_game()
        if user_input[pygame.K_s]:
            #if the user presses the s button
            save_game_to_file()
            
        #if player wants to shoot
        if user_input[pygame.K_SPACE] and shootLoop==0:
            #if the player presses the space button and there is a break between the shooting
            if player.left:#if the player is facing to the left
                facing = -1
            else:
                facing = 1
            if len(currentLevel.bullets)<5:#if theere are less than 5 bullets on the screen allow for another bullet to be made
                config.sounds["shoot"].play()#play sound effect
                currentLevel.addProjectile(player.rect.x+44, player.rect.y+22, 6, (163,163,194), facing)#make bullet
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
                player.move(0,7, currentLevel)
        else:
            if player.jumpCount >= -8:
                #make the arc for the jump
                player.jump(currentLevel)
                player.jumpCount -= 1
            else: 
                player.jumpCount = 8
                player.isJump = False#jump can happen again
        
        if user_input[pygame.K_LEFT]:
            #if the user presses the left key
            player.move(-5,0, currentLevel)
            player.left = True#change sprite to face left
            
            if player.rect.x < -44:
                #if the player goes off the screen
                resetStage(currentLevel)#reset level
                loot=False#loot can happen again in the level
                stage.move_to_left_room()
                currentLevel = process_current_level(levels)#read level
                player.rect.x = width-44#set the player to be on the right of the screen
            
        if user_input[pygame.K_RIGHT]:
            player.move(5,0, currentLevel)
            player.left = False
            if player.rect.x > width-40:
                resetStage(currentLevel)#reset level contents
                loot=False#loot can happen again in the level
                #if the player finishes the tutorial
                if stage.get_stage_number() == StageType.TUTORIAL and stage.get_level_number() == 7:
                    running=False#stop the game

                #if the player finishes the 1st level
                elif stage.get_stage_number() == StageType.LEVEL_1 and stage.get_level_number() == 5:
                    stage.move_onto_next_stage()
                    player.space=True
                    levels = update_current_stage()
                    currentLevel = process_current_level(levels)
                    player.setPos(40,player.rect.y)
                    
                elif stage.get_stage_number() == StageType.LEVEL_2 and stage.get_level_number() == 5:
                    #if the player has finished the second level
                    running = False
                    closing_credits()
                else:
                    stage.move_to_right_room()
                    currentLevel = process_current_level(levels)#read level
                    player.rect.x = 2#set the player to be on the left of the screen
                
        reset_level(currentLevel)#reset the screen
        pygame.display.flip()
        
    if loseGame == True:#if the player lost the game
        lose()


show_title_screen()