from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from direct.showbase.DirectObject import DirectObject
from direct.showbase.Transitions import Transitions
from direct.task import Task
from Play import *

class InGame(DirectObject):
  def __init__(self, parent):
    self.active = False
    self.paused = True
    
    self.parent = parent
    
    self.mainFrame = DirectFrame(frameColor=(0,0,0,0),
                                 frameSize=(-0.2,0.2,0.4,-0.4 ))
                                 
    self.continueImage = OnscreenImage(image = 'Models/menu/Resume.png', pos = (0,0,0.5), scale = 0.2)
    self.continueImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    self.restartImage = OnscreenImage(image = 'Models/menu/Restart.png', pos = (0,0,0), scale = 0.2)
    self.restartImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    self.exitImage = OnscreenImage(image = 'Models/menu/Exit.png', pos = (0,0,-0.5), scale = 0.2)
    self.exitImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    
    self.cont = DirectButton(parent = self.mainFrame,
                             pos = (0,0,0.5), scale=.2,
                             frameColor = (0,0,0,0),
                             frameSize = (-1,1,-1,1),
                             command = self.togglePause)
    self.cont.guiItem.setActive(True) 
    self.cont.bind(DGG.WITHIN, self.mouseOverContinue, [self.cont])
    self.cont.bind(DGG.WITHOUT, self.mouseOutContinue, [self.cont])
    
    self.restart = DirectButton(parent = self.mainFrame,
                             pos = (0,0,0), scale=.2,
                             frameColor = (0,0,0,0),
                             frameSize = (-1,1,-1,1),
                             command = self.restart)
    self.restart.guiItem.setActive(True) 
    self.restart.bind(DGG.WITHIN, self.mouseOverRestart, [self.restart])
    self.restart.bind(DGG.WITHOUT, self.mouseOutRestart, [self.restart])
    
    self.exit = DirectButton(parent = self.mainFrame,
                             pos = (0,0,-0.5), scale=.2,
                             frameColor = (0,0,0,0),
                             frameSize = (-1,1,-1,1),
                             command = parent.exit)
    self.exit.guiItem.setActive(True) 
    self.exit.bind(DGG.WITHIN, self.mouseOverExit, [self.exit])
    self.exit.bind(DGG.WITHOUT, self.mouseOutExit, [self.exit])
            
    #self.firstTransition = Transitions(loader)
    #self.firstTransition.setFadeColor(0,0,0)
    
    self.continueImage.hide()
    self.restartImage.hide()
    self.exitImage.hide()
      
    self.deactivate()

  #Change text color on mouseover
  def mouseOverContinue(self, frame, mousePos):
    self.continueImage.setImage('Models/menu/Resume2.png')
    self.continueImage.setTransparency(TransparencyAttrib.MMultisampleMask)
  def mouseOutContinue(self, frame, mousePos):
    if self.paused:
        self.continueImage.setImage('Models/menu/Resume.png')
        self.continueImage.setTransparency(TransparencyAttrib.MMultisampleMask)

  def mouseOverRestart(self, frame, mousePos):
    self.restartImage.setImage('Models/menu/Restart2.png')
    self.restartImage.setTransparency(TransparencyAttrib.MMultisampleMask)
  def mouseOutRestart(self, frame, mousePos):
    if self.paused:
        self.restartImage.setImage('Models/menu/Restart.png')
        self.restartImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    
  def mouseOverExit(self, frame, mousePos):
    self.exitImage.setImage('Models/menu/Exit2.png')
    self.exitImage.setTransparency(TransparencyAttrib.MMultisampleMask)
  def mouseOutExit(self, frame, mousePos):
    if self.paused:
        self.exitImage.setImage('Models/menu/Exit.png')
        self.exitImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    
  def activate(self):
    #self.firstTransition.fadeOut(3)
    self.active = True
    self.paused = False
    self.play = Play(self)
    #self.firstTransition.fadeOut(3)
  
  def deactivate(self):
    self.mainFrame.hide()
    self.active = False
    self.paused = True
    
  def togglePause(self):
    self.continueImage.setImage('Models/menu/Resume.png')
    self.continueImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    self.restartImage.setImage('Models/menu/Restart.png')
    self.restartImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    self.play.togglePause()
    
  def restart(self):
    self.restartImage.setImage('Models/menu/Restart.png')
    self.restartImage.setTransparency(TransparencyAttrib.MMultisampleMask)
    self.togglePause()
    self.play.player.die(self.play.level)
    
  def __del__(self):
    self.cont.destroy()
    self.exit.destroy()
    self.mainFrame.destroy()