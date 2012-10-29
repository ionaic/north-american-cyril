# TODO python and panda imports
from pandac.PandaModules import * #basic panda
from direct.showbase.DirectObject import DirectObject #event handling

class Level:
    def __init__(self, levelNum, modelPath):
        self.env = loader.loadModel(modelPath)
        self.env.setTwoSided(True)
        self.env.reparentTo(render)
        self.startPos = [0, 0, 0]
        self.startDir = [0, 0, 0]
        self.loadPlayer()
   
    # load the player into the world 
    def loadPlayer(self):
        self.player = Player()
        return
    
    def setStart(self, pos, direction):
        self.startPos = pos
        self.startDir = direction
   
    # replace self.end = pos with collision object? 
    def setEnd(self, pos):
        self.end = pos
        
    def spawnPlayer(self):
        self.player.setPos(pos)
