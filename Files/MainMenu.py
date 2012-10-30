from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage

class MainMenu:
  def __init__(self, main):
    self.mainImage = OnscreenImage(image = 'Models/gold-texture.jpg', pos = (0, 0, 0.02))
    self.mainImage.setScale(base.win.getXSize(),1,base.win.getYSize())
    
    self.mainFrame = DirectFrame(frameColor=(0,0,0,0),
                                 #(left, right, bottom, top)
                                 frameSize=(-1.2,-0.6,0.9,-0.2 ))
        
    self.start = DirectButton(parent = self.mainFrame,
                              pos = (-1,0,0.4),
                              frameColor = (1,1,1,0),
                              frameSize = (-1,3,-1,1),
                              text = 'Start',
                              text_fg = (1,0,0,1),
                              scale = 0.1,
                              command = main.startGame)
    self.start.guiItem.setActive(True) 
    self.start.bind(DGG.WITHIN, self.mouseOver, [self.start])
    self.start.bind(DGG.WITHOUT, self.mouseOut, [self.start])
    
    self.exit = DirectButton(parent = self.mainFrame,
                              pos = (-1,0,0),
                              frameColor = (1,1,1,0),
                              frameSize = (-1,3,-1,1),
                              text = 'Exit', text_fg = (1,0,0,1),
                              scale = 0.1,
                              command = main.exit)
    self.exit.guiItem.setActive(True) 
    self.exit.bind(DGG.WITHIN, self.mouseOver, [self.exit])
    self.exit.bind(DGG.WITHOUT, self.mouseOut, [self.exit])
    
  def mouseOver(self, frame, mousePos):
    frame['text_fg'] = (0,1,0,1)
  def mouseOut(self, frame, mousePos):
    frame['text_fg'] = (1,0,0,1)
    
  def hide(self):
      self.mainFrame.hide()
      self.mainImage.hide()
      
  def show(self):
      self.mainFrame.show()
      self.mainImage.show()

  def __del__(self):
      self.start.destroy()
      self.exit.destroy()
      self.mainFrame.destroy()
