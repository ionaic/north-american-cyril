from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling

class MapGen(object):
  def __init__(self):
    self.initMap()
    self.initLight()
    
  def initMap(self):
    #Creates grass/sky environment
    self.env = loader.loadModel("Models/Level1")
    self.env.setTwoSided(True)
    self.env.reparentTo(render)
  
  def initLight(self):
    #Loads ambient lighting
    self.ambientLight = AmbientLight("ambientLight")
    self.ambientLight.setColor((0.02, 0.02, 0.02, 1.0))
    self.ambientLightNP = render.attachNewNode(self.ambientLight)
    #the node that calls setLight is what's illuminated by the given light
    render.setLight(self.ambientLightNP)