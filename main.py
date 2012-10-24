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
    #globalClock = ClockObject.getGlobalClock()
    #globalClock.setMode(ClockObject.MLimited)
    #globalClock.setFrameRate(1000)
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
    
    base.cHandler = CollisionHandlerEvent()
    base.queue = CollisionHandlerQueue()
    #Set the pattern for the event sent on collision
    #base.cHandler.setInPattern("%fn-into-%in")
<<<<<<< HEAD
    #base.cHandler.setInPattern("into")
    base.cHandler.setInPattern("collide-%in")
=======
    base.cHandler.setInPattern("into")
    base.cHandler.setAgainPattern("%fn-into-%in")

    
    self.player.initCollisions()
>>>>>>> Added hand and light models
    
    self.player.initCollisions()
    self.enemy.initCollisions(base.cHandler, self.player)
    #base.cTrav.showCollisions(render)

  def update(self, task):
    dt = globalClock.getDt()
    self.player.update(globalClock.getDt())
    self.enemy.update(globalClock.getDt(), self.player)
    return task.cont
    
w = World()
run()
