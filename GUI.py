import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.task import Task
from Files.Menus.MainMenu import *
from Files.Menus.InGame import *
from main import *

import sys

class World(DirectObject):
  def __init__(self):
    #Turn off default mouse control
    base.disableMouse()
    base.setFrameRateMeter(True)
    #globalClock = ClockObject.getGlobalClock()
    #globalClock.setMode(ClockObject.MLimited)
    #globalClock.setFrameRate(1000)
    #Set windows properties
    #props = WindowProperties()
    #props.setFullscreen(1)
    #props.setSize(int(base.pipe.getDisplayWidth()), int(base.pipe.getDisplayHeight()))
    #base.win.requestProperties(props)
    base.accept("escape", sys.exit)
    
    self.activeMenu = None
    self.mainMenu = MainMenu(self)
    self.inGame = InGame(self)
    
  def startGame(self):
    self.mainMenu.hide()
    self.inGame.activate()
  
  def exit(self):
    sys.exit(0)
    
w = World()
run()