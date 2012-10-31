# TODO python and panda imports 
from pandac.PandaModules import * #basic panda
from direct.showbase.DirectObject import DirectObject #event handling

import Player

class Level:
    def __init__(self, levelNum, player):
        self.loadLevel(levelNum)
        # self.start = [0, 0, 0]
        self.setItems(levelNum)
        self.startDir = [0, 0, 0]
        self.setStart(self.startDir)
        # temp = player
        self.loadPlayer(player)
        

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
        else:
            self.env = loader.loadModel("Models/lv1")

        # environments are small, make them larger
        self.env.setScale(5)
        self.env.setTwoSided(True)
        self.env.reparentTo(render)
   
    # load the player into the world 
    def loadPlayer(self, player):
        self.player = player
        self.player.spawn(self.start, self.numWalls, self.numLights)
        return

    def loadLights(self):
        return

    def setStart(self, direction):
        self.start = self.loadColObj(self.env, "start").node().getSolid(0).getCollisionOrigin()
        self.startDir = direction
   
    # replace self.end = pos with collision object? 
    def setEnd(self):
        self.end = self.loadColObj(self.env, "exit")
        # self.end.setFromCollideMask(BitMask32.allOn())
        self.end.setIntoCollideMask(BitMask32.allOn())
        self.endNP = self.env.attachNewNode(self.end)
        base.cTrav.addCollider(self.endNP, base.cHandler)

        
    def loadColObj(self, model, name):
        cNode = model.find("**/"+name)
        if cNode.getNumNodes() < 1:
            raise ValueError("Couldn't find " + name + " in " + model.getName())
        elif cNode.node().isGeomNode():
            raise ValueError(name + " is a geometry node!")
        else:
            collider = model.attachNewNode(CollisionNode(name))

            collider.setPos(cNode.getPos())
            collider.node().addSolid(cNode.node().getSolid(0))
            origin = cNode.node().getSolid(0).getCollisionOrigin()
            return collider
    
    # def nextLevel(self):
        # if 1:
    
    def setItems(self, levelNum):#, lights, walls):
        if levelNum == 1:
            self.numLights = 5
            self.numWalls = 5
        elif levelNum == 2:
            self.numLights = 5
            self.numWalls = 5
        elif levelNum == 3:
            self.numLights = 5
            self.numWalls = 5
        elif levelNum == 4:
            self.numLights = 5
            self.numWalls = 5
        elif levelNum == 5:
            self.numLights = 5
            self.numWalls = 5
        else:
            self.numLights = 5
            self.numWalls = 5
        # self.numLights = lights
        # self.numWalls = walls
