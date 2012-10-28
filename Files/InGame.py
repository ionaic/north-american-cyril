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
    self.cont = DirectButton(parent = self.mainFrame, text = ("continue"), pos = (0,0,0.8),scale=.05,command=self.unpause)
    self.exit = DirectButton(parent = self.mainFrame, text = ("Exit"), pos = (0,0,0),scale=.05,command=parent.exit)
    
    self.accept( "escape", self.pause )
    self.unpause()
    self.deactivate()

  def activate(self):
    self.active = True
    self.run = Play(self)
  
  def deactivate(self):
    self.active = False
  
  def unpause(self):
    self.mainFrame.hide()
    self.paused = False
      
  def pause(self):
    self.mainFrame.show()
    self.paused = True
  
  #TODO: somehow to pause game
  def go(self):
    print 'go'
    if not self.active:
      return
    if self.paused:
      self.unpause()
    else:
      self.pause()
  
  def __del__(self):
    self.cont.destroy()
    self.exit.destroy()
    self.mainFrame.destroy()