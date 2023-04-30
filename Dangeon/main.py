import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from pygame.locals import *
from wad_reader import WADReader
from wad_data import WADData
import sys
from settings import *
from map_renderer import MapRenderer
from player import Player
from bsp import BSP

class DoomEngine:
    def __init__(self,wad_path = "C:\\Users\\SHIVA SINGH\\Documents\\GitHub\\playerOne\\Dangeon\\wad\\DOOM1.WAD"):
        self.wadpath = wad_path
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.dt = 1/60
        self.on_init()
    
    def on_init(self):
        self.wad_reader =  WADReader(self.wadpath)
        self.wad_data = WADData(self,map_name='E1M8')
        self.map_renderer = MapRenderer(self)
        self.player = Player(self)
        self.bsp = BSP(self)

    
    def update(self):
        self.player.update()
        self.bsp.update()
        self.dt = self.clock.tick()
        pg.display.set_caption(f"{self.clock.get_fps()}")
        icon = pg.image.load("Dangeon\menu.png")
        pg.display.set_icon(icon)

    def draw(self):
        self.screen.fill('black')
        self.map_renderer.draw()
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                exit()
    
    def run(self):
        while True:
            self.update()
            self.check_events()
            self.draw()
            
        pg.quit()
        sys.exit()
            


if __name__ == '__main__':
    dg = DoomEngine()
    dg.run()
    