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
    self.initModels()
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
  
  def initModels(self):
    self.map = MapGen()
    self.player = Player(self)
    self.enemies = []
    self.startLevel(1)
  
  #level number, next = true if next level (false = respawning)
  def startLevel(self, level, next = True):
    #Clear render
    self.player.clearItems()
    
    #If next level, load level map
    
      #and initialize enemies
    if next:
      enemy = Enemy( (0,0,3), [(0,-10,3), (0,10,3)] )
      self.enemies.append(enemy)
    
    pos = (-10,-10,3) #level.spawnPos
    walls = 3 #level.walls
    lights = 3 #level.lights
    #Spawn player using spawn (spawn pos, max walls, max lights)
    self.player.spawn(pos,walls,lights)
    if not next:
      #enemies = list of enemies in level
      for enemy in self.enemies:
        enemy.respawn()
    
    
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
    for enemy in self.enemies:
      enemy.initCollisions(self.player)
    
    #base.cTrav.showCollisions(render)

  def update(self, task):
    dt = globalClock.getDt()
    self.player.update(globalClock.getDt())
    for enemy in self.enemies:
      enemy.update(globalClock.getDt(), self.player)
    return task.cont
    
