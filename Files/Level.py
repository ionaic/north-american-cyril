# TODO python and panda imports
from pandac.PandaModules import * #basic panda
from direct.showbase.DirectObject import DirectObject #event handling

import Player

class Level:
    def __init__(self, levelNum):
        self.loadLevel(levelNum)
        self.startPos = [0, 0, 0]
        self.startDir = [0, 0, 0]
        self.loadPlayer()
        self.numLights = 3
        self.numWalls = 3

    def loadLevel(self, levelNum):
        if levelNum == 1:
            self.env = loader.loadModel("Models/lv1")
        elif levelNum == 2:
            self.env = loader.loadModel("Models/lv2")
        elif levelNum == 3:
            self.env = loader.loadModel("Models/lv3")
        elif levelNum == 4:
            self.env = loader.loadModel("Models/lv4")
        elif levelNum == 5:
            self.env = loader.loadModel("Models/lv5")
            self.env.setScale(2)
        else:
            self.env = loader.loadModel("Models/lv1")

        self.env.setTwoSided(True)
        self.env.reparentTo(render)
   
    # load the player into the world 
    def loadPlayer(self):
        #self.player = Player()
        return

    def loadLights(self):
        return

    def setStart(self, pos, direction):
        self.startPos = pos
        self.startDir = direction
   
    # replace self.end = pos with collision object? 
    def setEnd(self, pos):
        self.end = pos
        
    def spawnPlayer(self):
        self.player.setPos(pos)
