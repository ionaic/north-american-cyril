from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText

class HUD(object):
  def __init__(self, walls, lights):
    self.initHUD(walls, lights)
    
  def initHUD(self, walls, lights):
    self.wallsText = OnscreenText(text = 'Walls:', pos = (-1.1, 0.86)
      , scale = 0.08, fg = (1,1,1,1), mayChange = True)
    self.lightsText = OnscreenText(text = 'Lights:', pos = (-1.1, 0.77)
      , scale = 0.08, fg = (1,1,1,1), mayChange = True)
    self.wallsLeft = OnscreenText(text = str(walls), pos = (-0.92, 0.86)
      , scale = 0.08, fg = (1,1,1,1))
    self.lightsLeft = OnscreenText(text = str(lights), pos = (-0.92, 0.77)
      , scale = 0.08, fg = (1,1,1,1))
      
  def updateHUD(self, walls, lights):
    self.wallsLeft.setText(str(walls))
    self.lightsLeft.setText(str(lights))