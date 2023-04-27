import pygame
import numpy as np
from pygame.locals import *
from vector import Vector
from settings import *


class Pacman:
    def __init__(self,game,node):
        self.game = game
        self.name = Pacman
        self.color = WHITE
        self.node = node
        self.speed = 100
        self.directions = {STOP:Vector(0,0), UP:Vector(0,-1), DOWN:Vector(0,1), LEFT:Vector(-1,0), RIGHT:Vector(1,0)}
        self.direction = STOP
        self.radius = 10
        self.target = node
        self.setPosition()
    
    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self,dt):
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if direction == self.direction*-1:
            tmp = self.node
            self.node = self.target
            self.target = tmp
            self.direction*=-1

        if self.overshotTarget():
            self.node = self.target
            self.target  = self.getNewTarget(direction)
            self.direction = STOP
            if self.target is not self.node:
                self.direction = direction
            self.setPosition()
            
    def getNewTarget(self,direction):
        if direction is not STOP:
            if self.node.neighbours[direction] is not None:
                return self.node.neighbours[direction]
        return self.node

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.node.position - self.target.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

        


    def eatPellets(self,pellets):
        for pellet in pellets:
            d = pellet.position - self.position
            ds = d.magnitudeSquared()
            rs = self.radius+pellet.collideRadius
            if ds <=  rs:
                return pellet
        return None

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

    def render(self):
        p = self.position.asInt()
        pygame.draw.circle(self.game.screen,self.color,p,self.radius)