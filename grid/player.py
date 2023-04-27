import pygame
import numpy as np
from pygame.locals import *
from vector import Vector
from settings import *
from entity import Entity
from nodes import *

class Pacman(Entity):
    def __init__(self,game,node):
        Entity.__init__(self, node) 
        self.game = game
        self.name = Pacman
        self.color = WHITE
        self.node = node
        self.directions = {STOP:Vector(0,0), UP:Vector(0,-1), DOWN:Vector(0,1), LEFT:Vector(-1,0), RIGHT:Vector(1,0)}
        self.direction = STOP
        self.radius = 10
        self.target = node
        self.speed = 1000
        self.collideradius = 5
        

    def updateBot(self,action):
        dir = np.argmax(action)
        if(dir==1): self.direction = LEFT
        elif(dir==2): self.direction = UP
        else: self.direction = RIGHT
        self.position+=self.directions[self.direction]*self.speed
        if self.position.asTuple() not in self.game.nodes.nodeslist.keys():
            return -1,True,-1
        else:
            return 1,False,1

    def scatter(self):
        self.goal = Vector()

    def chase(self):
        self.goal = self.pacman.position

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
   
    def eatpellets(self,pellets):
        for pellet in pellets:
            d = self.position - pellet.position
            ds = d.magnitudeSquared()
            rs = (pellet.radius+self.collideradius)**2
            if ds <= rs:
                return pellet
        return None



















    def update(self, dt):	
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbours[PORTAL] is not None:
                self.node = self.node.neighbours[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()


    

    































































    
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

   