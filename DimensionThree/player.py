from settings import *
import pygame as pg
import math

class Player:
    def __init__(self,game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.speed = PLAYER_SPEED

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx,dy=0,0
        speed = self.speed
        speed_sin = speed*sin_a
        speed_cos = speed*cos_a

        key = pg.key.get_pressed()
        if key[pg.K_w]:
            dx+=speed_cos
            dy+=speed_sin
        if key[pg.K_s]:
            dx+= -speed_cos
            dy+= -speed_sin
        if key[pg.K_a]:
            dy+=-speed_cos
            dx+=speed_sin
        if key[pg.K_d]:
            dy+=speed_cos
            dx+=-speed_sin
        
        self.check_wall_collision(dx, dy)

        if key[pg.K_LEFT]:
            self.angle -= self.game.delta_time*PLAYER_ROT_SPEED
        if key[pg.K_RIGHT]:
            self.angle += self.game.delta_time*PLAYER_ROT_SPEED
        self.angle %= math.tau
    
    def checkWall(self,x,y):
        return (x,y) not in self.game.map.world_map
    
    def check_wall_collision(self,dx,dy):
        scale = PLAYER_SIZE_SCALE/(self.game.delta_time+0.00001)
        if self.checkWall(int(self.x+dx*scale), int(self.y)):
            self.x+=dx
        if self.checkWall(int(self.x), int(self.y+dy*scale)):
            self.y+=dy
            
    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT  or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH,HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL,min(MOUSE_MAX_REL,self.rel))
        self.angle += self.rel*MOUSE_SENSITIVITY*self.game.delta_time
    


    def draw(self):
        pg.draw.line(self.game.screen,'RED',(self.x*100,self.y*100),(self.x*100+WIDTH*math.cos(self.angle),self.y*100+WIDTH*math.sin(self.angle)),2)
        pg.draw.circle(self.game.screen, 'WHITE', (self.x*100,self.y*100), 15)

    def update(self):
        self.movement()
        #self.mouse_control()
    
    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)