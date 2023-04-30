import pygame as pg
import sys
from settings import *
from pygame.locals import *
from map import Map
from player import Player
from raycasting import Raycast
from object_renderer import ObjectRenderer

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.newGame()
    
    def newGame(self):
        self.map = Map(self)
        self.player  = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycast = Raycast(self)

    def update(self):
        self.player.update()
        self.raycast.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(F"{self.clock.get_fps()}")
        icon = pg.image.load("DimensionThree\stop.png")
        pg.display.set_icon(icon)

    def draw(self):
        self.screen.fill('BLACK')
        self.object_renderer.draw()
        #self.map.draw()
        #self.player.draw()
    
    def checkEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                exit()
    
    def run(self):
        while True:
            self.checkEvents()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()