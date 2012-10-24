from pandac.PandaModules import *
from direct.gui.DirectGui import *

class HUD(object):
  def __init__(self):
    self.createHUD()
    return
    
  def createHUD(self):
    self.frame = DirectFrame(frameSize = (0, 6, 0, 0.35),
      frameColor = (0.4, 0.4, 0.4, 0.0), parent = base.a2dBottomLeft)
  