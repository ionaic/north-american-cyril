from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib

class MainMenu:
  def __init__(self, main):
    self.main = main
    self.mainFrame = DirectFrame(parent = base.render2d, 
                                  frameColor = (1,0,0,0), pos = (0,0,0),
                                  frameSize = (-1,1,-1,1))
    self.mainImage = OnscreenImage(parent = self.mainFrame,
                                   image = 'Models/menu/menu.png', pos = (0, 0, 0))

    self.startImage = OnscreenImage(image = 'Models/menu/Start.png', pos = (-0.8,0,0), scale = 0.3)
    self.startImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    self.exitImage = OnscreenImage(image = 'Models/menu/Exit.png', pos = (0.8,0,0), scale = 0.3)
    self.exitImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    
    self.menuFrame = DirectFrame(frameColor=(0,0,0,0), pos = (0,0,-0.2),
                                 frameSize=(-0.5,0.5,0.7,-0.4 ))
        
    self.start = DirectButton(parent = self.menuFrame,
                              pos = (-0.8,0,0.2),
                              frameColor = (0,0,0,0),
                              frameSize = (-1,1,-1,1),
                              scale = 0.3,
                              command = self.start)
    self.start.guiItem.setActive(True) 
    self.start.bind(DGG.WITHIN, self.mouseOverStart, [self.start])
    self.start.bind(DGG.WITHOUT, self.mouseOutStart, [self.start])
    
    self.exit = DirectButton(parent = self.menuFrame,
                              pos = (0.8,0,0.2),
                              frameColor = (0,0,0,0),
                              frameSize = (-1,1,-1,1),
                              scale = 0.3,
                              command = main.exit)
    self.exit.guiItem.setActive(True) 
    self.exit.bind(DGG.WITHIN, self.mouseOverExit, [self.exit])
    self.exit.bind(DGG.WITHOUT, self.mouseOutExit, [self.exit])
    
  def mouseOverStart(self, frame, mousePos):
    self.startImage.setImage('Models/menu/Start2.png')
    self.startImage.setTransparency(TransparencyAttrib.MMultisampleMask)
  def mouseOutStart(self, frame, mousePos):
    self.startImage.setImage('Models/menu/Start.png')
    self.startImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    
  def mouseOverExit(self, frame, mousePos):
    self.exitImage.setImage('Models/menu/Exit2.png')
    self.exitImage.setTransparency(TransparencyAttrib.MMultisampleMask)
  def mouseOutExit(self, frame, mousePos):
    self.exitImage.setImage('Models/menu/Exit.png')
    self.exitImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    
  def hide(self):
    self.mainFrame.hide()
    self.menuFrame.hide()
      
  def show(self):
    self.mainFrame.show()
    self.menuFrame.show()
    
  def start(self):
    self.hide()
    self.startImage.destroy()
    self.exitImage.destroy()
    self.main.startGame()

  def __del__(self):
      self.start.destroy()
      self.exit.destroy()
      self.mainFrame.destroy()
