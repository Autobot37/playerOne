import pygame as pg

mini_map = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,2,2,2,2,0,0,0,2,2,2,0,0,2],
    [2,0,0,0,0,0,2,0,0,0,0,0,0,2,0,2],
    [2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,2],
    [2,0,0,2,2,2,2,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,2,0,0,0,2,0,0,0,0,0,0,0,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
]

class Map:
    def __init__(self,game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.createWorld()
    
    def createWorld(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen,'WHITE',(pos[0]*100,pos[1]*100,100,100),2)
        for pos in self.world_map]

    

    
