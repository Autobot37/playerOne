import pygame
from pygame.locals import *
from vector import Vector
from settings import *
from entity import Entity
from modes import ModeController

class Ghost(Entity):
    def __init__(self,node,pacman=None):
        Entity.__init__(self,node)
        self.name = GHOST
        self.points = 20
        self.goal = None
        self.directionMethod = self.randomDirection
        self.pacman= pacman
        self.mode = ModeController(self)