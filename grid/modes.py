from settings import *

class MainMode:
    def __init__(self):
        self.timer = 0
        self.scatter()
        self.mode = CHASE

    def update(self,dt):
        self.timer+=dt
        if self.timer>=self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()
    
    def scatter(self):
        self.mode = SCATTER
        self.time = 2
        self.timer = 0
    
    def chase(self):
        self.mode = CHASE
        self.time = 5
        self.timer = 0

class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity 

    def update(self, dt):
        self.mainmode.update(dt)
        self.current = self.mainmode.mode   
