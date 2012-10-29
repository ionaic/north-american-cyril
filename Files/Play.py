import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
from direct.actor.Actor import Actor #animated models
from direct.interval.IntervalGlobal import * #compound intervals
from direct.task import Task #update functions
from Files.MapGen import *
from Files.Player import *
from Files.Enemy import *

# multisampling
loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 1")

import math, sys, random

class World(DirectObject):
  def __init__(self):
    #Turn off default mouse control
    base.disableMouse()
    base.setFrameRateMeter(True)
    #Set windows properties
    props = WindowProperties()
    props.setCursorHidden(True)
    props.setFullscreen(1)
    props.setSize(int(base.pipe.getDisplayWidth()), int(base.pipe.getDisplayHeight()))
    props.setMouseMode(WindowProperties.MRelative)
    base.win.requestProperties(props)
    base.accept("escape", sys.exit)
    self.loadModels()
    self.setupCollisions()

    taskMgr.add(self.update, "updateTask")
    
  def loadModels(self):
    self.map = MapGen()
    self.player = Player()
    self.enemy = Enemy()
    
  def setupCollisions(self): 
    #Make a collision traverser, set it to default   
    base.cTrav = CollisionTraverser()
    base.pusher = CollisionHandlerPusher()
    
    self.cHandler = CollisionHandlerEvent()
    self.cQueue = CollisionHandlerQueue()
    #Set the pattern for the event sent on collision
    self.cHandler.setInPattern("collide-%in")
    self.cHandler.setAgainPattern("%fn-into-%in")
    
    self.player.initCollisions(base.pusher, self.cHandler, self.cQueue)
    self.enemy.initCollisions(self.cHandler, self.player)

  def update(self, task):
    dt = globalClock.getDt()
    self.player.update(globalClock.getDt())
    self.enemy.update(globalClock.getDt(), self.player, self.cQueue)
    return task.cont
    
    
    
import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #event handling
from direct.actor.Actor import Actor #animated models
from direct.interval.IntervalGlobal import * #compound intervals
from direct.task import Task #update functions
from MapGen import *
from Player import *
from Enemy import *

# multisampling
loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 1")

import math, sys, random

class Play(DirectObject):
  def __init__(self, parent):
    #Turn off default mouse control
    base.disableMouse()
    base.setFrameRateMeter(True)
    #globalClock = ClockObject.getGlobalClock()
    #globalClock.setMode(ClockObject.MLimited)
    #globalClock.setFrameRate(1000)
    #Set windows properties
    self.props = WindowProperties()
    self.props.setCursorHidden(True)
    #props.setFullscreen(1)
    #props.setSize(int(base.pipe.getDisplayWidth()), int(base.pipe.getDisplayHeight()))
    self.props.setMouseMode(WindowProperties.MRelative)
    base.win.requestProperties(self.props)
    self.parent = parent
    base.accept("escape", self.togglePause)
    self.loadModels()
    self.setupCollisions()

    self.task = taskMgr.add(self.update, "updateTask")
  
  def togglePause(self):
    if self.parent.paused:
      self.props.setCursorHidden(True)
      base.win.requestProperties(self.props)
      base.win.movePointer(0, base.win.getXSize()/2, base.win.getYSize()/2)
      taskMgr.add(self.task)
      self.parent.mainFrame.hide()
      self.parent.paused = False 
    else:
      self.props.setCursorHidden(False)
      base.win.requestProperties(self.props)
      taskMgr.remove(self.task)
      self.parent.mainFrame.show()
      self.parent.paused = True
  
  def loadModels(self):
    self.map = MapGen()
    self.player = Player()
    self.enemy = Enemy()
    
  def setupCollisions(self): 
    #Make a collision traverser, set it to default   
    base.cTrav = CollisionTraverser()
    base.itemTrav = CollisionTraverser()
    base.pusher = CollisionHandlerPusher()
    
    base.cHandler = CollisionHandlerEvent()
    base.queue = CollisionHandlerQueue()
    base.eQueue = CollisionHandlerQueue()
    #Set the pattern for the event sent on collision
    base.cHandler.setAgainPattern("%fn-again-%in")
    base.cHandler.setInPattern("%fn-into-%in")

    
    self.player.initCollisions()
    self.enemy.initCollisions(self.player)
    
    #base.cTrav.showCollisions(render)

  def update(self, task):
    dt = globalClock.getDt()
    self.player.update(globalClock.getDt())
    self.enemy.update(globalClock.getDt(), self.player)
    return task.cont
    
