import math

class Sensor:
    def __init__(self):
        self.raycount = 8
        self.raylength = 100
        self.rayspread = math.pi/2
        self.readings = []
