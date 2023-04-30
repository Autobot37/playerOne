from settings import *
import pygame as pg
from pygame.math import Vector2 

class Player:
    def __init__(self,engine):
        self.engine = engine
        self.thing = engine.wad_data.things[0]
        self.pos = self.thing.pos
        self.angle = self.thing.angle

    def update(self):
        pass