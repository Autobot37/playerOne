import pygame
import numpy
from settings import *
from pygame.locals import *
from vector import Vector
from player import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from entity import Entity

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.background = pygame.surface.Surface(RES).convert()
        self.frame_iteration=0
    
    def startGame(self):
        icon = pygame.image.load("grid\lightning(1).jpg")
        pygame.display.set_icon(icon)
        self.background.fill('BLACK')
        self.nodes = NodeGroup("grid\maze.txt")
        self.nodes.setupPortalPair((0,17), (27,17))
        self.pacman = Pacman(self,self.nodes.getPacmanNode())
        self.pellets = PelletGroup("grid\maze.txt")
        self.entity = Entity(self, self.nodes.getGhostNode())

    def update(self,action):
        pygame.display.set_caption(f"{self.clock.get_fps():.2f}")
        dt = self.clock.tick(60)/1000
        reward,game_over,done = self.pacman.updateBot(dt,action)
        self.entity.update(dt)
        self.pellets.update(dt)
        self.checkPellet(self.pellets.pelletList)
        self.checkEvents()
        self.render()
        return reward,game_over,done
    
    def render(self):
        self.screen.blit(self.background,(0,0))
        self.pacman.render()
        self.entity.render()
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        pygame.display.update()
    
    def checkPellet(self,pellets):
        pellet = self.pacman.eatPellets(pellets)
        if pellet is not None:
            pellets.remove(pellet)
            self.pellets.numEaten+=1
    
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def reset(self):
        self.startGame()
        self.score = 0
        self.frame_iteration = 0

    def play_step(self,action):
        self.startGame()
        self.frame_iteration+=1
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        
        reward,game_over,done = self.update(action)
        reward += self.pellets.numEaten
        return reward,game_over,done
    
    def is_collision(self): return False

