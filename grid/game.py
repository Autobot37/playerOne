import pygame
import numpy
from settings import *
from pygame.locals import *
from vector import Vector
from player import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghost import Ghost

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.clock = pygame.time.Clock()
        self.background = pygame.surface.Surface(RES).convert()
        self.startGame()
    
    def startGame(self):
        icon = pygame.image.load("grid\lightning(1).jpg")
        pygame.display.set_icon(icon)
        self.background.fill('BLACK')
        self.nodes = NodeGroup("grid\maze.txt")
        self.nodes.setupPortalPair((0,17), (27,17))
        self.pellets = PelletGroup("grid\maze.txt")
        self.newPac()
        self.ghost = Ghost(self.nodes.getPacmanNode(),self.pacman)

    def newPac(self):
        self.pacman = Pacman(self,self.nodes.getGhostNode())



    def update(self):
        pygame.display.set_caption(f"{self.clock.get_fps():.2f}")
        dt = self.clock.tick(60)/1000
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkGhostEvents()
        
        self.checkEvents()
        self.render()


    
    def render(self):
        self.screen.blit(self.background,(0,0))
        
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()

    def checkPelletEvents(self):
        pellet  = self.pacman.eatpellets(self.pellets.pellets)
        if pellet:
            self.pellets.numEaten +=1
            self.pellets.pellets.remove(pellet)
    
    def checkGhostEvents(self):
        if self.pacman.collideGhost(self.ghost):
            self.newPac()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
    
    def play_step(self,move):
        reward,done,score = self.pacman.updateBot(move)
        return reward, done, score

    def get_state(self, game):
        state = [
            game.pacman.position.copy().asInt(),
            game.ghost.position.copy().asInt()
        ]
        

if __name__ == "__main__":
    game = Game()
    print(game.get_state(game))


    
    