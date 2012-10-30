from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling

import Level

class MapGen(object):
  maxLevel = 5
  
  def __init__(self):
    self.curLev = 5
    self.initMap()
    self.initLight()
    
  def initMap(self):
    #Creates grass/sky environment
    #self.env = loader.loadModel("Models/Level1")
    #self.env.setTwoSided(True)
    #self.env.reparentTo(render)
    self.env = Level.Level(self.curLev)
  
  def initLight(self):
    #Loads ambient lighting
    self.ambientLight = AmbientLight("ambientLight")
    self.ambientLight.setColor((0.1, 0.1, 0.1, 1.0))
    #self.ambientLight.setColor((0.01, 0.01, 0.01, 1.0))
    self.ambientLightNP = render.attachNewNode(self.ambientLight)
    #the node that calls setLight is what's illuminated by the given light
    render.setLight(self.ambientLightNP)
    
  def nextLevel(self):
    if self.curLev < MapGen.maxLevel:
        self.curLev += 1
        self.initMap()
        self.initLight()
