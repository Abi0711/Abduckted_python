import wall as Wall
import spike as Spike
import enemy as Enemy

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
        self.walls.append(Wall(wx,wy))

    def addEnemy(self, x, y, width, height, end, health, mode):
        self.enemies.append(Enemy(x, y, width, height, end, health, mode))

    def addSpike(self, x, y):
        self.spikes.append(Spike(x, y))

        