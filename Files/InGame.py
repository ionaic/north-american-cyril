from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from Play import *


#TODO: pass pause to game class 
class InGame(DirectObject):
  def __init__(self, parent):
    self.active = False
    self.paused = True
    
    self.parent = parent
    
    self.mainFrame = DirectFrame(frameColor=(0,0,0,1) , frameSize=(-0.2,0.2,0.9,-0.2 ))
    self.cont = DirectButton(parent = self.mainFrame, text = ("continue"), pos = (0,0,0.8),scale=.05,command=self.togglePause)
    self.exit = DirectButton(parent = self.mainFrame, text = ("Exit"), pos = (0,0,0),scale=.05,command=parent.exit)
    
    self.deactivate()

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