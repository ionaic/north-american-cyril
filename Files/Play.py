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
    self.parent = parent
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
    base.accept("escape", self.pause)
    self.loadModels()
    self.setupCollisions()

    taskMgr.add(self.update, "updateTask")
  
  def pause(self):
    self.props.setCursorHidden(False)
    base.win.requestProperties(self.props)
    taskMgr.remove('updateTask')
    self.parent.pause()
  
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
    #Set the pattern for the event sent on collision
    base.cHandler.setAgainPattern("%fn-again-%in")
    base.cHandler.setInPattern("%fn-into-%in")

    
    self.player.initCollisions()
    
    self.enemy.initCollisions(base.cHandler, self.player)
    
    #base.cTrav.showCollisions(render)

  def update(self, task):
    dt = globalClock.getDt()
    self.player.update(globalClock.getDt())
    self.enemy.update(globalClock.getDt(), self.player)
    return task.cont
    
