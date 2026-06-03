import os
import pygame

pygame.init()
pygame.mixer.init()
width = 660#width of the screen
height = 510#height of the screen
screen = pygame.display.set_mode((width,height))
settings = {
    "volume": 50,
    "fullscreen": False,
}

soundEffectsFolder = "soundEffects"
spriteFolder = "sprites"
collectiblesFolder = "collectibles"
healthUpFolder = "healthUp"
keyAndLockFolder = "keyAndLock"
enemyFolder = "enemy"
playerFolder = "ted"
teleporterFolder = "teleporter"
backgroundImageFolder = "background"
endSlidesFolder = "endSlides"
openingSlidesFolder = "openingSlides"
teleporterFolder = "teleporter"

enemy_sprites = {
    "spikes": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "spikes.png")).convert_alpha(),
    "lMedium": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "lMedium.png")).convert_alpha(),
    "rMedium": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "rMedium.png")).convert_alpha(),
    "lEasy": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "lEasy.png")).convert_alpha(),
    "rEasy": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "rEasy.png")).convert_alpha(),
    "lBoss": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "lBoss.png")).convert_alpha(),
    "rBoss": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "rBoss.png")).convert_alpha(),
    "lBossFinal": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "lBossFinal.png")).convert_alpha(),
    "rBossFinal": pygame.image.load(os.path.join(spriteFolder, enemyFolder, "rBossFinal.png")).convert_alpha(),
}

duck_sprites = {
    "rDuck":       pygame.transform.scale(pygame.image.load(os.path.join(spriteFolder, playerFolder, "rDuck.png")).convert_alpha(), (44, 44)),
    "lDuck":       pygame.image.load(os.path.join(spriteFolder, playerFolder, "lDuck.png")).convert_alpha(),
    "rShoot":      pygame.image.load(os.path.join(spriteFolder, playerFolder, "rShoot.png")).convert_alpha(),
    "lShoot":      pygame.image.load(os.path.join(spriteFolder, playerFolder, "lShoot.png")).convert_alpha(),
    "rSpaceShoot": pygame.image.load(os.path.join(spriteFolder, playerFolder, "rSpaceShoot.png")).convert_alpha(),
    "lSpaceShoot": pygame.image.load(os.path.join(spriteFolder, playerFolder, "lSpaceShoot.png")).convert_alpha(),
    "rSpace":      pygame.image.load(os.path.join(spriteFolder, playerFolder, "rSpace.png")).convert_alpha(),
    "lSpace":      pygame.image.load(os.path.join(spriteFolder, playerFolder, "lSpace.png")).convert_alpha(),
}

teleporter_sprites = {
    "up": pygame.image.load(os.path.join(spriteFolder, teleporterFolder, "up.png")).convert_alpha(),
    "down": pygame.image.load(os.path.join(spriteFolder, teleporterFolder, "down.png")).convert_alpha(),
}

key_sprites = {
    "key1":    pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, keyAndLockFolder, "keyFrag1.png")).convert_alpha(),
    "key2":    pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, keyAndLockFolder, "keyFrag2.png")).convert_alpha(),
    "bossKey": pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, keyAndLockFolder, "bossKey.png")).convert_alpha(),
    "blueKey": pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, keyAndLockFolder, "blueKey.png")).convert_alpha(),
    "lock":    pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, keyAndLockFolder, "lock.png")).convert_alpha(),
}

collectible_sprites = {
    "bread": pygame.image.load(os.path.join(spriteFolder, collectiblesFolder, healthUpFolder, "bread.png")).convert_alpha(),
}

background_images = {
    "level1": pygame.image.load(os.path.join(backgroundImageFolder, "level1Back.png")).convert_alpha(),
    "level2": pygame.image.load(os.path.join(backgroundImageFolder, "level2Back.png")).convert_alpha(),
}

colours = {
    "green":       (0, 200, 0),
    "red":         (255, 0, 0),
    "brightRed":   (255, 0, 0),
    "brightGreen": (0, 255, 0),
    "yellow":      (248, 255, 149),
    "brightYellow":(239, 255, 0),
    "white":       (255, 255, 255),
    "black":       (0, 0, 0),
}

sounds = {
    "teleport": pygame.mixer.Sound(os.path.join(soundEffectsFolder, "teleporter.wav")),
    "jump":     pygame.mixer.Sound(os.path.join(soundEffectsFolder, "jumpP.wav")),
    "shoot":    pygame.mixer.Sound(os.path.join(soundEffectsFolder, "shoot.wav")),
    "hit":      pygame.mixer.Sound(os.path.join(soundEffectsFolder, "quack.wav")),
    "heal":     pygame.mixer.Sound(os.path.join(soundEffectsFolder, "healthUp.wav")),
}

music = {
    "level1": os.path.join(soundEffectsFolder, "happy.wav"),
    "punch":  os.path.join(soundEffectsFolder, "punch.wav"),
    "victory": os.path.join(soundEffectsFolder, "victory.wav"),
    "happy": os.path.join(soundEffectsFolder, "happy.wav"),
    "main": os.path.join(soundEffectsFolder, "music.mp3"),
}

fonts = {
    "small":  pygame.font.SysFont("berlinsansfb", 20),
    "medium": pygame.font.SysFont("berlinsansfb", 30),
    "large":  pygame.font.SysFont("berlinsansfb", 115),
}

opening_slides = {
    "map": pygame.image.load(os.path.join(spriteFolder, "map.png")).convert_alpha(),
    "s0":  pygame.image.load(os.path.join(openingSlidesFolder, "slide0.png")).convert_alpha(),
    "s1":  pygame.image.load(os.path.join(openingSlidesFolder, "slide1.png")).convert_alpha(),
    "s2":  pygame.image.load(os.path.join(openingSlidesFolder, "slide2.png")).convert_alpha(),
}

ending_slides = {
    "s1":  pygame.image.load(os.path.join(endSlidesFolder, "last1.png")).convert_alpha(),
    "s2":  pygame.image.load(os.path.join(endSlidesFolder, "last2.png")).convert_alpha(),
    "s3":  pygame.image.load(os.path.join(endSlidesFolder, "last3.png")).convert_alpha(),
    "s4":  pygame.image.load(os.path.join(endSlidesFolder, "last4.png")).convert_alpha(),
    "s5":  pygame.image.load(os.path.join(endSlidesFolder, "last5.png")).convert_alpha(),
    "s6":  pygame.image.load(os.path.join(endSlidesFolder, "last6.png")).convert_alpha(),
    "s7":  pygame.image.load(os.path.join(endSlidesFolder, "last7.png")).convert_alpha(),
    "s8":  pygame.image.load(os.path.join(endSlidesFolder, "last8.png")).convert_alpha(),
    "s9":  pygame.image.load(os.path.join(endSlidesFolder, "last9.png")).convert_alpha(),
    "s10": pygame.image.load(os.path.join(endSlidesFolder, "last10.png")).convert_alpha(),
}