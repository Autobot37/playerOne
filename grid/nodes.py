from vector import Vector
from settings import *
import pygame 
import numpy as np

class Node:
    def __init__(self,x,y):
        self.position = Vector(x, y)
        self.neighbours = {UP:None,DOWN:None,LEFT:None,RIGHT:None,PORTAL:None}

    def render(self,screen):
        for nei in self.neighbours.values():
            if nei is not None:
                line_start = self.position.asInt()
                line_end = nei.position.asInt()
                pygame.draw.line(screen, 'WHITE', line_start, line_end)
        pygame.draw.circle(screen, 'WHITE', self.position.asInt(), 5)

class NodeGroup:
    def __init__(self,level):
        self.level = level
        self.nodeslist = {}
        self.nodesymbol = ['+','P','n']
        self.pathsymbol = ['.','-','/','p']
        data = self.readData(level)
        self.createNodeTable(data)
        self.connectVertically(data)
        self.connectHoriz(data)

    def readData(self,level):
        return np.loadtxt(level,'<U1')
    
    def createNodeTable(self,data):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodesymbol:
                    x, y = self.constructKey(col, row)
                    self.nodeslist[(x,y)] = Node(x,y)
    
    def constructKey(self,x,y):
        return x*TILEWIDTH, y*TILEHEIGHT

    def connectHoriz(self,data):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodesymbol:
                    if key is None:
                        key = self.constructKey(col, row)
                    else:
                        otherkey = self.constructKey(col, row)
                        self.nodeslist[key].neighbours[RIGHT]=self.nodeslist[otherkey]
                        self.nodeslist[otherkey].neighbours[LEFT]=self.nodeslist[key]
                        key = otherkey
                elif data[row][col] not in self.pathsymbol:
                    key = None
    
    def connectVertically(self,data):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodesymbol:
                    if key is None:
                        key = self.constructKey(col, row)
                    else:
                        otherkey = self.constructKey(col, row)
                        self.nodeslist[key].neighbours[DOWN]=self.nodeslist[otherkey]
                        self.nodeslist[otherkey].neighbours[UP]=self.nodeslist[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathsymbol:
                    key = None
    
    def getPacmanNode(self):
        nodes = list(self.nodeslist.values())
        return nodes[0]
        
    def getGhostNode(self):
        nodes = list(self.nodeslist.values())
        return nodes[3]
        
    def setupPortalPair(self,key1,key2):
        key1  = self.constructKey(*key1)
        key2 = self.constructKey(*key2)
        if key1 in self.nodeslist.keys() and key2 in self.nodeslist.keys():
            self.nodeslist[key1].neighbours[PORTAL] = self.nodeslist[key2]
            self.nodeslist[key2].neighbours[PORTAL] = self.nodeslist[key1]
    
    def render(self,screen):
        for node in self.nodeslist.values():
            node.render(screen)
        


