from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText

class HUD(object):
  def __init__(self, walls, lights):
    self.initHUD(walls, lights)
    self.initEnergy()
    
  def initHUD(self, walls, lights):
    self.wallsText = OnscreenText(text = 'Walls:', pos = (-1.1, 0.86),
      scale = 0.08, fg = (1,1,1,1))
    self.lightsText = OnscreenText(text = 'Lights:', pos = (-1.1, 0.77),
      scale = 0.08, fg = (1,1,1,1))
    self.wallsLeft = OnscreenText(text = str(walls), pos = (-0.92, 0.86),
      scale = 0.08, fg = (1,1,1,1), mayChange = True)
    self.lightsLeft = OnscreenText(text = str(lights), pos = (-0.92, 0.77),
      scale = 0.08, fg = (1,1,1,1), mayChange = True)
      
    self.energyText = OnscreenText(text = 'Energy:', pos = (0.9, -0.86),
      scale = 0.08, fg = (1,1,1,1))
    self.energyLeft = OnscreenText(text = '100', pos = (1.1, -0.86),
      scale = 0.08, fg = (1,1,1,1), mayChange = True)
      
  def initEnergy(self):
    self.gen = MeshDrawer2D()
    self.gen.setBudget(500)
    self.genNode = self.gen.getRoot()
    self.genNode.reparentTo(render)
      
  def updateHUD(self, walls, lights):
    self.wallsLeft.setText(str(walls))
    self.lightsLeft.setText(str(lights))
    
  def updateEnergy(self, energy):
    self.energyLeft.setText(str(int(energy)))