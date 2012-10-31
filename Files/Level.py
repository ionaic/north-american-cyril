from pandac.PandaModules import * #basic panda
from direct.showbase.DirectObject import DirectObject #event handling

import Player

class Level:
  def __init__(self):
      self.start = [0, 0, 0]
      self.initLight()
      
  def initLight(self):
    #Loads ambient lighting
    self.ambientLight = AmbientLight("ambientLight")
    self.ambientLight.setColor((0.1, 0.1, 0.1, 1.0))
    #self.ambientLight.setColor((0.01, 0.01, 0.01, 1.0))
    self.ambientLightNP = render.attachNewNode(self.ambientLight)
    #the node that calls setLight is what's illuminated by the given light
    render.setLight(self.ambientLightNP)
        

  def loadLevel(self, levelNum):
    if levelNum == 1:
        self.env = loader.loadModel("Models/World_1")
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

    self.setItems(levelNum)
    self.setStart()
    # environments are small, make them larger
    self.env.setScale(5)
    self.env.setTwoSided(True)
    self.env.reparentTo(render)
 
  # load the player into the world 
  def loadPlayer(self, player):
      #self.player = player
      #self.player.spawn(self.start, self.numWalls, self.numLights)
      return

  def loadLights(self):
      return

  def setStart(self):
    print 'x'
    print self.env.findAllMatches('**/**')
    return
    self.start = self.loadObj(self.env, "playerSpawn").node().getSolid(0).getCollisionOrigin()
    #self.startDir = direction
 
  # replace self.end = pos with collision object? 
  def setEnd(self):
    self.end = self.loadObj(self.env, "exit")
    # self.end.setFromCollideMask(BitMask32.allOn())
    self.end.setIntoCollideMask(BitMask32.allOn())
    self.endNP = self.env.attachNewNode(self.end)
    base.cTrav.addCollider(self.endNP, base.cHandler)

      
  def loadObj(self, model, name):
    return
    print '\n\n\n',model.findAllMatches("***")
    print 'rawr\n\n'
    return
    cNode = model.find("**/"+name)
    if cNode.getNumNodes() < 1:
        raise ValueError("Couldn't find " + name + " in " + model.getName())
    else:
        print cNode.getPos(render)
        return
        collider = model.attachNewNode(CollisionNode(name))

        collider.setPos(cNode.getPos())
        collider.node().addSolid(cNode.node().getSolid(0))
        origin = cNode.node().getSolid(0).getCollisionOrigin()
        return collider

  # def nextLevel(self):
      # if 1:
  
  def setItems(self, levelNum):
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
