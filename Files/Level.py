from pandac.PandaModules import * #basic panda
from direct.showbase.DirectObject import DirectObject #event handling

import Player

class Level:
  def __init__(self):
      self.start = [0, 0, 0]
      self.initLight()
      self.envScale = 5
      
  def initLight(self):
    #Loads ambient lighting
    self.ambientLight = AmbientLight("ambientLight")
    # self.ambientLight.setColor((0.1, 0.1, 0.1, 1.0))
    self.ambientLight.setColor((0.01, 0.01, 0.01, 1.0))
    self.ambientLightNP = render.attachNewNode(self.ambientLight)
    #the node that calls setLight is what's illuminated by the given light
    render.setLight(self.ambientLightNP)
        

  def loadLevel(self, levelNum):
    if levelNum == 1:
        self.env = loader.loadModel("Models/world1")
    elif levelNum == 2:
        self.env = loader.loadModel("Models/world2")
    elif levelNum == 3:
        self.env = loader.loadModel("Models/world3")
    elif levelNum == 4:
        self.env = loader.loadModel("Models/world5")
        self.env.setZ(-5)
    elif levelNum == 5:
        self.env = loader.loadModel("Models/world4")
    else:
        self.env = loader.loadModel("Models/world1")

    self.setItems(levelNum)
    self.setStart()
    self.setTorches()
    # environments are small, make them larger
    self.env.setScale(self.envScale)
    self.env.setTwoSided(True)
    self.env.reparentTo(render)
 
  def setStart(self):
    playerSpawn = self.env.find('*/start')
    pos = LPoint3f(playerSpawn.getX(), playerSpawn.getY(), 0.)
    self.playerPos = playerSpawn.getPos() * self.envScale
    
    self.enemies = []
    enemies = self.env.findAllMatches('*/enemy?')
    for enemy in enemies:
      eSpawn = LPoint3f(enemy.getX(), enemy.getY(), 0) * self.envScale
      ePath = self.env.findAllMatches("*/%s?"%enemy.getName())
      AiPath = [eSpawn]
      for vertex in ePath:
        pos = LPoint3f(vertex.getX(), vertex.getY(), 0)
        AiPath.append(pos * self.envScale)
      eTuple = (eSpawn, AiPath)
      print eTuple
      self.enemies.append( (eSpawn, AiPath) )
  
  def setTorches(self):
    torches = self.env.findAllMatches('*/torch')
    for torch in torches:
      torchPos = torch.getPos() * self.envScale
      
  
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
