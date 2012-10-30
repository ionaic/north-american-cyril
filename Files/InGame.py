from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from Play import *

class InGame(DirectObject):
  def __init__(self, parent):
    self.active = False
    self.paused = True
    
    self.parent = parent
    
    self.mainFrame = DirectFrame(frameColor=(0,0,0,0),
                                 frameSize=(-0.2,0.2,0.4,-0.4 ))
    self.cont = DirectButton(parent = self.mainFrame,
                             text = ("Continue"),
                             pos = (0,0,0.2), scale=.1,
                             frameColor = (1,1,1,0),
                             text_fg = (1,0,0,1),
                             command = self.togglePause)
    self.cont.guiItem.setActive(True) 
    self.cont.bind(DGG.WITHIN, self.mouseOver, [self.cont])
    self.cont.bind(DGG.WITHOUT, self.mouseOut, [self.cont])
    
    self.exit = DirectButton(parent = self.mainFrame,
                             text = ("Exit"),
                             pos = (0,0,-0.2), scale=.1,
                             frameColor = (1,1,1,0),
                             text_fg = (1,0,0,1),
                             command = parent.exit)
    self.exit.guiItem.setActive(True) 
    self.exit.bind(DGG.WITHIN, self.mouseOver, [self.exit])
    self.exit.bind(DGG.WITHOUT, self.mouseOut, [self.exit])
    
    self.deactivate()

  #Change text color on mouseover
  def mouseOver(self, frame, mousePos):
    frame['text_fg'] = (0,1,0,1)
  def mouseOut(self, frame, mousePos):
    frame['text_fg'] = (1,0,0,1)
    
  def activate(self):
    self.active = True
    self.paused = False
    self.run = Play(self)
  
  def deactivate(self):
    self.mainFrame.hide()
    self.active = False
    self.paused = True
    
  def togglePause(self):
    self.run.togglePause()
    
  def __del__(self):
    self.cont.destroy()
    self.exit.destroy()
    self.mainFrame.destroy()