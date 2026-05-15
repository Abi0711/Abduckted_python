from wall import Wall
from spike import Spike
from enemy import Enemy
from healthUp import HealthUp
from teleporter import Teleporter
from teleporterType import TeleporterType
from projectile import Projectile
from boss import Boss

class Level:
    def __init__(self):
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
    

        