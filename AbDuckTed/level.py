from bossType import BossType
from enemyType import EnemyType
from wall import Wall
from spike import Spike
from enemy import Enemy
from healthUp import HealthUp
from teleporter import Teleporter
from teleporterType import TeleporterType
from projectile import Projectile
from boss import Boss
from interactiveObject import Interactive

class Level:
    def __init__(self, unprocessed_level: list):
        self.bullets = []#keeps the players bullets
        self.eBullets = []#keeps the enemies bullets
        self.enemies = []#keeps the enemies 
        self.boss = []#keeps the bosses
        self.walls=[]#keeps the track of the walls that are drawn on screen
        self.spikes = []#keeps the spikes
        self.ups = []#keeps the 1-ups on screen
        self.teleDown = []#keeps the teleporters going down
        self.teleUp = []#keeps the teleporters going up
        self.interactive = []#keeps the interactives
        
        x=y=0
        for row in unprocessed_level:
            #for each row in the level
            for col in row: 
                #for individual letters consisting in the rows
                if col == "W":#add a wall
                    self.addWall(x, y)
                    
                elif col == "E":#add a police weasel
                    self.addEnemy(x, y-10, 32, 40, x+(30*4), 5, EnemyType.MEDIUM)
                    
                elif col == "e":#add an ordinary weasel
                    self.addEnemy(x, y-10, 32, 40, x+(30*4), 3, EnemyType.EASY)
                    
                elif col == "S":#add a spike
                    self.addSpike(x, y)
                    
                elif col == "H":#add 1-up
                    self.addHealthUp(x, y)
                    
                elif col == "D":#add teleporter that goes down
                    self.addTeleporter(x, y, TeleporterType.DOWN)
                    
                elif col =="U":#add teleporter that goes down
                    self.addTeleporter(x, y, TeleporterType.UP)
                    
                elif col == "I":#add interactive object
                    self.addInteractive(Interactive(x, y))
                    
                elif col == "b":#add miniboss
                    self.addBoss(x, y - 20, 64, 80, x + (30 * 4), 25, BossType.MINIBOSS)
                    
                elif col == "B":#add boss
                    self.addBoss(x, y - 20, 64, 80, x + (30 * 11), 55, BossType.BOSS)
    
                elif col == "F":#add boss
                    self.addBoss(x, y - 20, 64, 80, x + (30 * 11), 55, BossType.FINAL_BOSS)
                
                x += 30 #add 30pixels to x so the entities are different coordinates, reads from left to right
            y += 30#add 30 pixels to work downwards from screen, reads from top to bottom
            x=0

    def addWall(self, wx, wy):
        self.walls.append(Wall(wx, wy))

    def addEnemy(self, x, y, width, height, end, health, mode):
        self.enemies.append(Enemy(x, y, width, height, end, health, mode))

    def addSpike(self, x, y):
        self.spikes.append(Spike(x, y))
    
    def addHealthUp(self, x, y):
        self.ups.append(HealthUp(x, y))
    
    def addEnemyProjectile(self, x, y, radius, color, facing):
        self.eBullets.append(Projectile(x, y, radius, color, facing))
    
    def addProjectile(self, x, y, radius, color, facing):
        self.bullets.append(Projectile(x, y, radius, color, facing))

    def addTeleporter(self, x, y, direction):
        if direction == TeleporterType.DOWN:
            self.teleDown.append(Teleporter(x, y, direction))
        else:
            self.teleUp.append(Teleporter(x, y, direction))

    def addInteractive(self, interactive):
        self.interactive.append(interactive)
    
    def addBoss(self, x, y, width, height, end, health, mode):
        self.boss.append(Boss(x, y, width, height, end, health, mode))
    
    def resetStage(self):
        del self.walls[:]
        del self.spikes[:]
        del self.enemies[:]
        del self.interactive[:]
        del self.ups[:]
        del self.teleUp[:]
        del self.teleDown[:]
        del self.eBullets[:]
        del self.boss[:]
    

        