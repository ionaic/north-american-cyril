from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling

from Level import *

class MapGen(object):
  maxLevel = 5
  
  def __init__(self, player):
    self.curLev = 4
    self.initMap(player)
    self.initLight()
    
  def initMap(self, player):
    #Creates grass/sky environment
    #self.env = loader.loadModel("Models/Level1")
    #self.env.setTwoSided(True)
    #self.env.reparentTo(render)
    # self.env = Level(self.curLev, player)
    self.env = Level()
  
  def initLight(self):
    #Loads ambient lighting
    self.ambientLight = AmbientLight("ambientLight")
    # self.ambientLight.setColor((0.1, 0.1, 0.1, 1.0))
    self.ambientLight.setColor((0.0, 0.0, 0.0, 1.0))
    self.ambientLightNP = render.attachNewNode(self.ambientLight)
    #the node that calls setLight is what's illuminated by the given light
    render.setLight(self.ambientLightNP)
    
  def nextLevel(self):
    if self.curLev < MapGen.maxLevel:
        self.curLev += 1
        self.initMap()
        self.initLight()
        print("nextlevel")
    else:
        print("maxed out level!")
        # win screen?
