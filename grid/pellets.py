from vector import Vector
from settings import *
import pygame 
import numpy as np
class Pellet:
    def __init__(self,row,col):
        self.position = Vector(col*TILEWIDTH,row*TILEHEIGHT)
        self.radius = int(4*TILEWIDTH/16)
        self.collideRadius = int(4*TILEWIDTH/16)
        self.points = 10
        self.visible = True
        self.color = BLUE

    def render(self,screen):
        if self.visible:
            pygame.draw.circle(screen,self.color,self.position.asInt(),4)

class PowerPellet(Pellet):
    def __init__(self,row,col):
        Pellet.__init__(self,row,col)
        self.radius = int(8*TILEWIDTH/16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0
        self.color = RED
        
    def update(self,dt):
        self.timer+=dt
        if self.timer>=self.flashTime:
            self.visible = not self.visible
            self.timer = 0
    
class PelletGroup:
    def __init__(self,file):
        self.pellets = []
        self.powerpellets = []
        self.createPelletList(file)
        self.numEaten = 0
    
    def update(self,dt):
        for p in self.powerpellets:
            p.update(dt)
    
    def render(self,screen):
        if self.visible:
            pygame.draw.circle(screen,self.color,self.position.asInt(),4)

    
    def createPelletList(self,file):
        data = np.loadtxt(file,'<U1')
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in ['.','+']:
                    self.pellets.append(Pellet(row, col))
                elif data[row][col] in ['P','p']:
                    self.powerpellets.append(PowerPellet(row, col))
                    self.pellets.append(Pellet(row, col))
    
    def isEmpty(self):
        return len(self.pellets) == 0
    
    def render(self,screen):
        for pellet in self.pellets:
            pellet.render(screen)
            for pellet in self.powerpellets:
                pellet.render(screen)



